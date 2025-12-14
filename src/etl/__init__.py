# src/etl/__init__.py
"""
Funciones de apoyo para los procesos ETL del proyecto.

Ejemplo de uso desde un notebook:

    from src.etl.files import data_raw_path, data_processed_path
    raw_path = data_raw_path("openfoodfacts", "en.openfoodfacts.org.products.csv")
    processed_path = data_processed_path("openfoodfacts", "openfoodfacts_subset.parquet")
"""

from .files import (
    project_root,
    data_raw_path,
    data_processed_path,
    notebooks_path,
    connect_duckdb,
)

__all__ = [
    "project_root",
    "data_raw_path",
    "data_processed_path",
    "notebooks_path",
    "connect_duckdb",
]