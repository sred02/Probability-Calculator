"""
calculators/discrete.py — Distribuciones de Probabilidad Discretas
===================================================================

Este módulo implementa cálculos para distribuciones de probabilidad discretas:
  - Binomial  : probabilidad de k éxitos en n ensayos independientes
  - Poisson   : probabilidad de k eventos en un intervalo de tiempo/espacio

Todas las funciones retornan probabilidades entre 0 y 1.

Fundamento matemático:
  Binomial : P(X = k) = C(n,k) × p^k × (1-p)^(n-k)
             donde C(n,k) = n! / (k! × (n-k)!)

  Poisson  : P(X = k) = (λ^k × e^-λ) / k!
             donde λ (lambda) es la tasa promedio de eventos

Dependencias:
  - math  : funciones matemáticas estándar (factorial, exp, comb)
  - scipy : usada como respaldo para validar resultados (opcional)

Uso ejemplo:
  >>> from calculators.discrete import binomial, poisson
  >>> binomial(n=10, k=3, p=0.5)
  0.1171875
  >>> poisson(lam=4.0, k=2)
  0.14653...

Autor  : Tu Nombre
GitHub : https://github.com/tu-usuario
"""

# ─────────────────────────────────────────────
#  Importaciones
# ─────────────────────────────────────────────
import math
from typing import Union

# scipy es opcional — se usa solo para verificación en tests
try:
    from scipy.stats import binom, poisson as poisson_scipy
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False


# ══════════════════════════════════════════════════════════════════════
#  FUNCIONES AUXILIARES — COMBINATORIA
# ══════════════════════════════════════════════════════════════════════

def factorial(n: int) -> int:
    """
    Calcula el factorial de n (n!).

    Parámetros:
        n (int): número entero no negativo

    Retorna:
        int: n! = n × (n-1) × (n-2) × ... × 1

    Raises:
        ValueError: si n es negativo

    Ejemplos:
        >>> factorial(0)
        1
        >>> factorial(5)
        120

    Notas:
        - Por definición, 0! = 1
        - Usa math.factorial en vez de implementación manual para velocidad
        - Para n grandes (n > 170) puede causar overflow en algunos sistemas
    """
    if n < 0:
        raise ValueError(f"Factorial no está definido para números negativos (recibido: {n})")
    
    return math.factorial(n)


def combinations(n: int, k: int) -> int:
    """
    Calcula el coeficiente binomial C(n, k) = "n choose k".

    Representa el número de formas de elegir k elementos de un conjunto de n,
    sin importar el orden.

    Fórmula:
        C(n, k) = n! / (k! × (n-k)!)

    Parámetros:
        n (int): tamaño total del conjunto
        k (int): número de elementos a elegir

    Retorna:
        int: número de combinaciones posibles

    Raises:
        ValueError: si k > n o si n o k son negativos

    Ejemplos:
        >>> combinations(5, 2)
        10
        >>> combinations(10, 3)
        120

    Casos especiales:
        - C(n, 0) = 1  (una forma de no elegir nada)
        - C(n, n) = 1  (una forma de elegir todo)
        - C(n, k) = C(n, n-k)  (simetría)

    Implementación:
        Usa math.comb (Python 3.8+) que es optimizada y evita overflow
        al no calcular factoriales completos innecesariamente.
    """
    if n < 0 or k < 0:
        raise ValueError(f"n y k deben ser no negativos (recibido: n={n}, k={k})")
    
    if k > n:
        raise ValueError(f"k no puede ser mayor que n (recibido: k={k}, n={n})")
    
    # math.comb disponible desde Python 3.8+
    # Es más eficiente que calcular n! / (k! × (n-k)!)
    return math.comb(n, k)


# ══════════════════════════════════════════════════════════════════════
#  DISTRIBUCIÓN BINOMIAL
# ══════════════════════════════════════════════════════════════════════

def binomial(n: int, k: int, p: float) -> float:
    """
    Calcula la probabilidad de obtener exactamente k éxitos en n ensayos
    independientes, donde cada ensayo tiene probabilidad p de éxito.

    Fórmula:
        P(X = k) = C(n,k) × p^k × (1-p)^(n-k)

    Parámetros:
        n (int)  : número total de ensayos/intentos (n ≥ 1)
        k (int)  : número de éxitos deseados (0 ≤ k ≤ n)
        p (float): probabilidad de éxito en cada ensayo (0 ≤ p ≤ 1)

    Retorna:
        float: probabilidad de obtener exactamente k éxitos (entre 0 y 1)

    Raises:
        ValueError: si los parámetros están fuera de rango válido

    Ejemplos de uso:
        # Lanzar una moneda 10 veces, probabilidad de 3 caras
        >>> binomial(n=10, k=3, p=0.5)
        0.1171875

        # Responder 20 preguntas al azar (4 opciones), prob. de 5 correctas
        >>> binomial(n=20, k=5, p=0.25)
        0.2023...

    Casos extremos:
        - Si p = 0: solo P(X=0) = 1, todas las demás son 0
        - Si p = 1: solo P(X=n) = 1, todas las demás son 0
        - Si k > n: retorna 0 (imposible más éxitos que intentos)

    Notas de implementación:
        Para evitar overflow con números muy grandes, se calcula usando:
        1. C(n,k) con math.comb (optimizado)
        2. Multiplicación directa de potencias
        Esto es más estable que calcular factoriales completos.
    """
    # ── Validaciones de entrada ──
    if n < 1:
        raise ValueError(f"n debe ser ≥ 1 (recibido: {n})")
    
    if k < 0:
        raise ValueError(f"k debe ser ≥ 0 (recibido: {k})")
    
    if k > n:
        # Técnicamente no es error, simplemente es probabilidad 0
        return 0.0
    
    if not 0 <= p <= 1:
        raise ValueError(f"p debe estar entre 0 y 1 (recibido: {p})")

    # ── Casos especiales para optimización ──
    if p == 0.0:
        # Si p=0, solo es posible tener 0 éxitos
        return 1.0 if k == 0 else 0.0
    
    if p == 1.0:
        # Si p=1, solo es posible tener n éxitos
        return 1.0 if k == n else 0.0

    # ── Cálculo principal ──
    # P(X = k) = C(n,k) × p^k × (1-p)^(n-k)
    
    coef = combinations(n, k)           # C(n,k)
    prob_success = p ** k               # p^k
    prob_failure = (1 - p) ** (n - k)   # (1-p)^(n-k)
    
    result = coef * prob_success * prob_failure

    return result


def binomial_cumulative(n: int, k: int, p: float) -> float:
    """
    Calcula la probabilidad acumulada P(X ≤ k) para una distribución binomial.

    Es decir, la probabilidad de obtener k o menos éxitos.

    Fórmula:
        P(X ≤ k) = Σ(i=0 hasta k) P(X = i)
                 = Σ(i=0 hasta k) C(n,i) × p^i × (1-p)^(n-i)

    Parámetros:
        n (int)  : número total de ensayos
        k (int)  : número máximo de éxitos
        p (float): probabilidad de éxito por ensayo

    Retorna:
        float: probabilidad acumulada P(X ≤ k)

    Ejemplos:
        # Probabilidad de obtener 3 o menos caras en 10 lanzamientos
        >>> binomial_cumulative(n=10, k=3, p=0.5)
        0.171875

    Uso típico:
        Calcular "al menos" o "como máximo" cierto número de éxitos:
        - P(X ≤ k)       : binomial_cumulative(n, k, p)
        - P(X ≥ k)       : 1 - binomial_cumulative(n, k-1, p)
        - P(a ≤ X ≤ b)   : binomial_cumulative(n, b, p) - binomial_cumulative(n, a-1, p)
    """
    # Validar parámetros (binomial() ya valida, pero mejor explícito)
    if k < 0:
        return 0.0
    if k >= n:
        k = n  # P(X ≤ n) = 1 siempre

    # Sumar P(X = i) para i desde 0 hasta k
    cumulative = sum(binomial(n, i, p) for i in range(k + 1))
    
    return cumulative


# ══════════════════════════════════════════════════════════════════════
#  DISTRIBUCIÓN DE POISSON
# ══════════════════════════════════════════════════════════════════════

def poisson(lam: float, k: int) -> float:
    """
    Calcula la probabilidad de que ocurran exactamente k eventos en un
    intervalo de tiempo o espacio, dada una tasa promedio λ (lambda).

    La distribución de Poisson modela eventos raros o dispersos:
      - Llamadas telefónicas por hora
      - Errores de impresión por página
      - Clientes llegando a una tienda por minuto
      - Partículas radioactivas desintegradas por segundo

    Fórmula:
        P(X = k) = (λ^k × e^-λ) / k!

    Parámetros:
        lam (float): tasa promedio de eventos en el intervalo (λ > 0)
        k   (int)  : número de eventos a calcular (k ≥ 0)

    Retorna:
        float: probabilidad de obtener exactamente k eventos

    Raises:
        ValueError: si lam ≤ 0 o k < 0

    Ejemplos:
        # Si un call center recibe 4 llamadas/hora en promedio,
        # ¿cuál es la probabilidad de recibir exactamente 2 en la próxima hora?
        >>> poisson(lam=4.0, k=2)
        0.14653...

        # Si hay 0.5 errores tipográficos por página en promedio,
        # ¿probabilidad de encontrar 0 errores en una página?
        >>> poisson(lam=0.5, k=0)
        0.60653...

    Propiedades de Poisson:
        - Media = Varianza = λ
        - Apropiada cuando n es grande y p es pequeña en binomial
        - Aproximación: Binomial(n,p) ≈ Poisson(λ=np) si n≥20 y p≤0.05

    Casos extremos:
        - Si λ → 0: P(X=0) → 1, todas las demás → 0
        - Si λ es grande y k=λ: alcanza el máximo de la distribución
        - k muy grande con λ pequeña: probabilidad cercana a 0

    Notas de implementación:
        Para evitar overflow con k! grande, se puede usar:
          P(X = k) = e^(-λ) × λ^k / k!
                   = e^(-λ) × Π(i=1 hasta k) λ/i
        Pero math.factorial es suficiente para k razonables (<170).
    """
    # ── Validaciones de entrada ──
    if lam <= 0:
        raise ValueError(f"λ (lambda) debe ser > 0 (recibido: {lam})")
    
    if k < 0:
        raise ValueError(f"k debe ser ≥ 0 (recibido: {k})")

    # ── Caso especial: k muy grande con λ pequeña ──
    # Para evitar cálculos innecesarios si la probabilidad es prácticamente 0
    if k > 1000 and lam < 10:
        return 0.0

    # ── Cálculo principal ──
    # P(X = k) = (λ^k × e^-λ) / k!
    
    numerator = (lam ** k) * math.exp(-lam)  # λ^k × e^-λ
    denominator = factorial(k)                # k!
    
    result = numerator / denominator

    return result


def poisson_cumulative(lam: float, k: int) -> float:
    """
    Calcula la probabilidad acumulada P(X ≤ k) para una distribución de Poisson.

    Fórmula:
        P(X ≤ k) = Σ(i=0 hasta k) P(X = i)
                 = Σ(i=0 hasta k) (λ^i × e^-λ) / i!

    Parámetros:
        lam (float): tasa promedio de eventos
        k   (int)  : número máximo de eventos

    Retorna:
        float: probabilidad acumulada P(X ≤ k)

    Ejemplos:
        # Probabilidad de recibir 3 o menos llamadas si λ=4
        >>> poisson_cumulative(lam=4.0, k=3)
        0.43347...

    Uso típico:
        - P(X ≤ k)       : poisson_cumulative(lam, k)
        - P(X ≥ k)       : 1 - poisson_cumulative(lam, k-1)
        - P(X > k)       : 1 - poisson_cumulative(lam, k)
    """
    if k < 0:
        return 0.0

    # Sumar P(X = i) para i desde 0 hasta k
    cumulative = sum(poisson(lam, i) for i in range(k + 1))
    
    return cumulative


# ══════════════════════════════════════════════════════════════════════
#  FUNCIONES DE ESTADÍSTICAS DESCRIPTIVAS
#  Útiles para calcular media, varianza y desviación estándar
# ══════════════════════════════════════════════════════════════════════

def binomial_mean(n: int, p: float) -> float:
    """
    Calcula la media (valor esperado) de una distribución binomial.

    Fórmula:
        E[X] = n × p

    Parámetros:
        n (int)  : número de ensayos
        p (float): probabilidad de éxito

    Retorna:
        float: número esperado de éxitos

    Ejemplo:
        # En 100 lanzamientos de moneda, esperamos ~50 caras
        >>> binomial_mean(100, 0.5)
        50.0
    """
    return n * p


def binomial_variance(n: int, p: float) -> float:
    """
    Calcula la varianza de una distribución binomial.

    Fórmula:
        Var(X) = n × p × (1-p)

    Parámetros:
        n (int)  : número de ensayos
        p (float): probabilidad de éxito

    Retorna:
        float: varianza de la distribución

    Ejemplo:
        >>> binomial_variance(100, 0.5)
        25.0
    """
    return n * p * (1 - p)


def binomial_std(n: int, p: float) -> float:
    """
    Calcula la desviación estándar de una distribución binomial.

    Fórmula:
        σ = √(n × p × (1-p))

    Parámetros:
        n (int)  : número de ensayos
        p (float): probabilidad de éxito

    Retorna:
        float: desviación estándar

    Ejemplo:
        >>> binomial_std(100, 0.5)
        5.0
    """
    return math.sqrt(binomial_variance(n, p))


def poisson_mean(lam: float) -> float:
    """
    Calcula la media de una distribución de Poisson.

    En Poisson, media = λ (por definición).

    Parámetros:
        lam (float): tasa de eventos

    Retorna:
        float: media = λ
    """
    return lam


def poisson_variance(lam: float) -> float:
    """
    Calcula la varianza de una distribución de Poisson.

    En Poisson, varianza = λ (una propiedad única de esta distribución).

    Parámetros:
        lam (float): tasa de eventos

    Retorna:
        float: varianza = λ
    """
    return lam


def poisson_std(lam: float) -> float:
    """
    Calcula la desviación estándar de una distribución de Poisson.

    Fórmula:
        σ = √λ

    Parámetros:
        lam (float): tasa de eventos

    Retorna:
        float: desviación estándar

    Ejemplo:
        >>> poisson_std(4.0)
        2.0
    """
    return math.sqrt(lam)


# ══════════════════════════════════════════════════════════════════════
#  UTILIDADES DE VERIFICACIÓN (SOLO PARA DESARROLLO/TESTING)
# ══════════════════════════════════════════════════════════════════════

def _verify_with_scipy(func_name: str, params: dict, our_result: float) -> None:
    """
    Función interna para verificar nuestros resultados contra scipy.
    
    Solo se ejecuta si scipy está disponible.
    Útil durante desarrollo para validar implementación.
    
    NO usar en producción — es solo para debugging.
    """
    if not SCIPY_AVAILABLE:
        return
    
    tolerance = 1e-10  # Diferencia aceptable por redondeo
    
    if func_name == "binomial":
        scipy_result = binom.pmf(params["k"], params["n"], params["p"])
    elif func_name == "poisson":
        scipy_result = poisson_scipy.pmf(params["k"], params["lam"])
    else:
        return
    
    diff = abs(our_result - scipy_result)
    
    if diff > tolerance:
        print(f"⚠️  ADVERTENCIA: Diferencia detectada en {func_name}")
        print(f"   Nuestra implementación: {our_result}")
        print(f"   SciPy:                  {scipy_result}")
        print(f"   Diferencia:             {diff}")


# ══════════════════════════════════════════════════════════════════════
#  TESTING RÁPIDO — Solo ejecuta si corres este archivo directamente
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🧪 Probando calculators/discrete.py\n")
    print("=" * 60)
    
    # ── Test Binomial ──
    print("\n📊 BINOMIAL:")
    print("10 lanzamientos de moneda, probabilidad de exactamente 3 caras:")
    n, k, p = 10, 3, 0.5
    result = binomial(n, k, p)
    print(f"  P(X = {k}) = {result:.6f}  ({result * 100:.2f}%)")
    print(f"  Media esperada: {binomial_mean(n, p):.1f}")
    print(f"  Desv. estándar: {binomial_std(n, p):.2f}")
    
    if SCIPY_AVAILABLE:
        _verify_with_scipy("binomial", {"n": n, "k": k, "p": p}, result)
    
    # ── Test Poisson ──
    print("\n📊 POISSON:")
    print("Call center con 4 llamadas/hora promedio, prob. de exactamente 2:")
    lam, k = 4.0, 2
    result = poisson(lam, k)
    print(f"  P(X = {k}) = {result:.6f}  ({result * 100:.2f}%)")
    print(f"  Media: {poisson_mean(lam):.1f}")
    print(f"  Desv. estándar: {poisson_std(lam):.2f}")
    
    if SCIPY_AVAILABLE:
        _verify_with_scipy("poisson", {"lam": lam, "k": k}, result)
    
    # ── Test Combinatoria ──
    print("\n🔢 COMBINATORIA:")
    print(f"  C(10, 3) = {combinations(10, 3)}")
    print(f"  5! = {factorial(5)}")
    
    print("\n" + "=" * 60)
    print("✅ Tests completados. Si scipy está instalado, se muestran comparaciones.")
