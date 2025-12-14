# src/viz/__init__.py
"""
Funciones de apoyo para la interpretación visual de indicadores.

- quadrants: clasificación sencilla por cuadrantes para lecturas
  del tipo "alto/bajo" en dos dimensiones.
"""

from .quadrants import classify_quadrant, quadrant_series

__all__ = ["classify_quadrant", "quadrant_series"]