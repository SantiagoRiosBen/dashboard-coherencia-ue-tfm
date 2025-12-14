# src/indicators/nutrition.py
from __future__ import annotations

from typing import Dict, Iterable, Tuple

import numpy as np
import pandas as pd

# Columnas típicas de OpenFoodFacts usadas en el TFM
NUTRIENT_COLUMNS_DEFAULT = (
    "energy_100g",
    "sugars_100g",
    "saturated-fat_100g",
    "sodium_100g",
)

# Mapeo a los nombres de columnas normalizadas que describes en la memoria
NORMALIZED_COLUMN_NAMES = {
    "energy_100g": "s_energy",
    "sugars_100g": "s_sugars",
    "saturated-fat_100g": "s_satfat",
    "sodium_100g": "s_sodium",
}


def compute_percentile_bounds(
    df: pd.DataFrame,
    nutrient_cols: Iterable[str] = NUTRIENT_COLUMNS_DEFAULT,
    lower: float = 5.0,
    upper: float = 95.0,
) -> Dict[str, Tuple[float, float]]:
    """
    Calcula percentiles inferiores y superiores para cada nutriente.

    Se utiliza para recortar valores extremos y escalar entre 0 y 1.

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame con las columnas de nutrientes.
    nutrient_cols : iterable of str
        Nombres de columnas de nutrientes a procesar.
    lower : float
        Percentil inferior (porcentaje).
    upper : float
        Percentil superior (porcentaje).

    Returns
    -------
    dict
        Diccionario {columna: (p_lower, p_upper)}.
    """
    bounds: Dict[str, Tuple[float, float]] = {}

    for col in nutrient_cols:
        series = df[col].dropna().astype(float)
        if series.empty:
            raise ValueError(
                f"No hay datos no nulos para la columna '{col}' "
                "al calcular percentiles."
            )

        p_low, p_high = np.percentile(series, [lower, upper])
        # En caso extremo de p_low == p_high, evitamos división por cero
        if p_low == p_high:
            p_high = p_low + 1e-9

        bounds[col] = (float(p_low), float(p_high))

    return bounds


def _normalize_with_bounds(
    series: pd.Series, bounds: Tuple[float, float]
) -> pd.Series:
    """
    Normaliza una serie entre 0 y 1 utilizando límites de percentil,
    truncando por debajo de 0 y por encima de 1.
    """
    low, high = bounds
    scaled = (series.astype(float) - low) / (high - low)
    return scaled.clip(lower=0.0, upper=1.0)


def add_off_nutrient_index(
    df: pd.DataFrame,
    nutrient_cols: Iterable[str] = NUTRIENT_COLUMNS_DEFAULT,
    bounds: Dict[str, Tuple[float, float]] | None = None,
    index_col: str = "off_nutrient_index",
) -> tuple[pd.DataFrame, Dict[str, Tuple[float, float]]]:
    """
    Añade al DataFrame columnas normalizadas y el índice sintético OFF.

    Pasos:
    1. Calcula (o recibe) percentiles 5 y 95 para cada nutriente.
    2. Normaliza cada nutriente entre 0 y 1, truncando en [0, 1].
    3. Calcula la media de las columnas normalizadas y la multiplica por 100.

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame de OpenFoodFacts ya filtrado (UE, 2015–2023, etc.).
    nutrient_cols : iterable of str
        Columnas de nutrientes a limitar.
    bounds : dict, opcional
        Diccionario de percentiles precomputados {col: (p5, p95)}.
        Si es None, se calculan a partir de `df`.
    index_col : str
        Nombre de la columna del índice sintético resultante.

    Returns
    -------
    df_out : pd.DataFrame
        Copia del DataFrame original con columnas adicionales:
        - columnas normalizadas (p. ej., s_energy, s_sugars, s_satfat, s_sodium)
        - índice sintético en la columna `index_col`.
    bounds : dict
        Diccionario de límites de percentiles utilizado.

    Ejemplo
    -------
    >>> df_off, bounds = add_off_nutrient_index(df_off_raw)
    >>> df_off[[\"s_energy\", \"s_sugars\", \"s_satfat\", \"s_sodium\", \"off_nutrient_index\"]].head()
    """
    df_out = df.copy()

    if bounds is None:
        bounds = compute_percentile_bounds(df_out, nutrient_cols)

    normalized_cols = []

    for col in nutrient_cols:
        if col not in df_out.columns:
            raise KeyError(f"Columna de nutriente no encontrada: '{col}'")

        normalized_col = NORMALIZED_COLUMN_NAMES.get(col, f"s_{col}")
        df_out[normalized_col] = _normalize_with_bounds(df_out[col], bounds[col])
        normalized_cols.append(normalized_col)

    # Media de las columnas normalizadas * 100
    df_out[index_col] = df_out[normalized_cols].mean(axis=1) * 100.0

    return df_out, bounds