# src/etl/files.py
from __future__ import annotations

from pathlib import Path
from typing import Union

import duckdb

PathLike = Union[str, Path]


# ---------------------------------------------------------------------------
# RUTAS DEL PROYECTO
# ---------------------------------------------------------------------------

# Punto de partida: este archivo está en <raíz>/src/etl/files.py
# parents[0] = etl, parents[1] = src, parents[2] = raíz del repo
_PROJECT_ROOT = Path(__file__).resolve().parents[2]


def project_root() -> Path:
    """
    Devuelve la ruta a la raíz del repositorio del TFM.

    Se asume que la estructura es:

        <raíz>/
          ├─ src/
          ├─ data_raw/
          ├─ data_processed/
          ├─ notebooks/
          └─ dashboard/

    Returns
    -------
    pathlib.Path
        Ruta absoluta a la raíz del proyecto.
    """
    return _PROJECT_ROOT


def data_raw_path(*parts: PathLike) -> Path:
    """
    Construye una ruta dentro de data_raw a partir de segmentos.

    Ejemplo:
        data_raw_path("openfoodfacts", "en.openfoodfacts.org.products.csv")
    """
    return project_root() / "data_raw" / Path(*parts)


def data_processed_path(*parts: PathLike) -> Path:
    """
    Construye una ruta dentro de data_processed a partir de segmentos.

    Ejemplo:
        data_processed_path("openfoodfacts", "openfoodfacts_subset.parquet")
    """
    return project_root() / "data_processed" / Path(*parts)


def notebooks_path(*parts: PathLike) -> Path:
    """
    Construye una ruta dentro de notebooks a partir de segmentos.

    Ejemplo:
        notebooks_path("pipelines", "01_pre_etl_openfoodfacts.ipynb")
    """
    return project_root() / "notebooks" / Path(*parts)


# ---------------------------------------------------------------------------
# CONEXIÓN A DUCKDB
# ---------------------------------------------------------------------------


def connect_duckdb(db_path: str = ":memory:") -> duckdb.DuckDBPyConnection:
    """
    Crea una conexión a DuckDB.

    Parámetros
    ----------
    db_path : str, opcional
        Ruta al archivo .duckdb. Por defecto ':memory:' para
        trabajar en memoria.

    Returns
    -------
    duckdb.DuckDBPyConnection
        Conexión lista para ejecutar sentencias SQL.

    Ejemplo
    -------
    >>> from src.etl.files import connect_duckdb, data_raw_path
    >>> con = connect_duckdb()
    >>> csv_path = data_raw_path("eurostat", "prc_hicp_aind_tabular.tsv")
    >>> con.execute(\"\"\"SELECT * FROM read_csv_auto(?)
    ...               LIMIT 5\"\"\", [str(csv_path)]).df()
    """
    return duckdb.connect(database=db_path, read_only=False)
