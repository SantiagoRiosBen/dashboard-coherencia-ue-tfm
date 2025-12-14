# src/viz/quadrants.py
from __future__ import annotations

from typing import Literal

import pandas as pd

QuadrantLabel = Literal["Q1", "Q2", "Q3", "Q4"]


def classify_quadrant(
    x: float,
    y: float,
    x_ref: float,
    y_ref: float,
) -> QuadrantLabel:
    """
    Clasifica un punto (x, y) en uno de cuatro cuadrantes
    respecto a los valores de referencia (x_ref, y_ref).

            y
            ↑
       Q2   |   Q1
            |
    --------+--------→ x
       Q3   |   Q4
            |

    Convención:
    - Q1: x >= x_ref, y >= y_ref
    - Q2: x <  x_ref, y >= y_ref
    - Q3: x <  x_ref, y <  y_ref
    - Q4: x >= x_ref, y <  y_ref
    """
    if x >= x_ref and y >= y_ref:
        return "Q1"
    if x < x_ref and y >= y_ref:
        return "Q2"
    if x < x_ref and y < y_ref:
        return "Q3"
    return "Q4"


def quadrant_series(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    x_ref: float | None = None,
    y_ref: float | None = None,
) -> pd.Series:
    """
    Devuelve una serie con el cuadrante de cada fila de df.

    Si no se proporcionan x_ref o y_ref, se usan las medianas
    de las columnas correspondientes.

    Esto es útil si quieres, por ejemplo, colorear países en Power BI
    según su cuadrante (aunque la lógica de color se define allí).

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame con las columnas x_col y y_col.
    x_col, y_col : str
        Nombres de las columnas que se usan como ejes.
    x_ref, y_ref : float, opcional
        Valores de referencia; si son None, se usan las medianas.

    Returns
    -------
    pd.Series
        Serie con etiquetas 'Q1', 'Q2', 'Q3' o 'Q4'.
    """
    if x_ref is None:
        x_ref = float(df[x_col].median())
    if y_ref is None:
        y_ref = float(df[y_col].median())

    return df.apply(
        lambda row: classify_quadrant(
            x=row[x_col],
            y=row[y_col],
            x_ref=x_ref,
            y_ref=y_ref,
        ),
        axis=1,
    )