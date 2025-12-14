# src/indicators/__init__.py
"""
Módulos para el cálculo de indicadores e índices sintéticos.

- nutrition: índice sintético de densidad de nutrientes críticos
  a partir de OpenFoodFacts.
"""

from .nutrition import (
    NUTRIENT_COLUMNS_DEFAULT,
    compute_percentile_bounds,
    add_off_nutrient_index,
)

__all__ = [
    "NUTRIENT_COLUMNS_DEFAULT",
    "compute_percentile_bounds",
    "add_off_nutrient_index",
]