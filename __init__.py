"""
calculators — Módulo de Cálculos de Probabilidad
=================================================

Este paquete contiene las implementaciones matemáticas de todas
las distribuciones de probabilidad soportadas por la aplicación.

Módulos:
  - discrete.py   : Binomial, Poisson
  - continuous.py : Normal, Exponencial

Uso:
  from calculators.discrete import binomial, poisson
  from calculators.continuous import normal_cdf, exponential_cdf
"""

# Hacer que las funciones principales estén disponibles directamente
# desde `import calculators`

from .discrete import (
    binomial,
    binomial_cumulative,
    poisson,
    poisson_cumulative,
)

# Las funciones continuous se importarán cuando ese módulo esté listo
# from .continuous import (
#     normal_cdf,
#     exponential_cdf,
# )

__all__ = [
    # Discrete
    "binomial",
    "binomial_cumulative",
    "poisson", 
    "poisson_cumulative",
    # Continuous (por activar)
    # "normal_cdf",
    # "exponential_cdf",
]
