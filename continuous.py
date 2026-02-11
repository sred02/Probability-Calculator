"""
calculators/continuous.py — Distribuciones de Probabilidad Continuas
=====================================================================

Este módulo implementa cálculos para distribuciones de probabilidad continuas:
  - Normal (Gaussiana) : la famosa curva de campana
  - Exponencial        : tiempo entre eventos en procesos de Poisson

A diferencia de las distribuciones discretas, estas trabajan con intervalos
en lugar de valores puntuales. Calculamos principalmente la CDF (Función de
Distribución Acumulada) que representa P(X ≤ x).

Fundamento matemático:

  Normal:
    PDF: f(x) = (1 / (σ√(2π))) × e^(-(x-μ)²/(2σ²))
    CDF: Φ(x) = ∫[-∞ hasta x] f(t) dt
         (no tiene forma cerrada, se calcula numéricamente)
    
    Estandarización: Z = (X - μ) / σ
                     Si X ~ N(μ, σ²) → Z ~ N(0, 1)

  Exponencial:
    PDF: f(x) = λe^(-λx)  para x ≥ 0
    CDF: F(x) = 1 - e^(-λx)
    Media: 1/λ
    Desv. estándar: 1/λ

Dependencias:
  - math  : exp, sqrt, pi, erf (error function)
  - scipy : usada como respaldo para validar resultados (opcional)

Uso ejemplo:
  >>> from calculators.continuous import normal_cdf, exponential_cdf
  >>> normal_cdf(x=75, mu=70, sigma=5)
  0.8413447460685429
  >>> exponential_cdf(x=2.0, lam=0.5)
  0.6321205588285577

Autor  : Tu Nombre
GitHub : https://github.com/tu-usuario
"""

# ─────────────────────────────────────────────
#  Importaciones
# ─────────────────────────────────────────────
import math
from typing import Tuple

# scipy es opcional — se usa solo para verificación en tests
try:
    from scipy.stats import norm, expon
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False


# ══════════════════════════════════════════════════════════════════════
#  DISTRIBUCIÓN NORMAL (GAUSSIANA)
# ══════════════════════════════════════════════════════════════════════

def _standard_normal_cdf(z: float) -> float:
    """
    Calcula la CDF de la distribución normal estándar N(0,1).

    Usa la función de error (erf) de la biblioteca math para el cálculo.

    Fórmula:
        Φ(z) = (1/2) × [1 + erf(z / √2)]

    Parámetros:
        z (float): valor estandarizado (Z-score)

    Retorna:
        float: P(Z ≤ z) donde Z ~ N(0,1)

    Notas:
        - erf(x) es la función de error: erf(x) = (2/√π) ∫[0 hasta x] e^(-t²) dt
        - Esta función es interna, no está diseñada para uso directo
        - La precisión es alta (error < 1e-15) usando math.erf
    """
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def normal_pdf(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    """
    Calcula la función de densidad de probabilidad (PDF) de la distribución normal.

    La PDF NO es una probabilidad, sino una densidad. Para obtener probabilidades,
    usa normal_cdf().

    Fórmula:
        f(x) = (1 / (σ√(2π))) × e^(-(x-μ)²/(2σ²))

    Parámetros:
        x     (float): valor a evaluar
        mu    (float): media de la distribución (por defecto 0)
        sigma (float): desviación estándar (por defecto 1, debe ser > 0)

    Retorna:
        float: densidad en el punto x

    Raises:
        ValueError: si sigma ≤ 0

    Ejemplos:
        # Máximo de la curva en μ=0, σ=1
        >>> normal_pdf(0, mu=0, sigma=1)
        0.3989...

        # Altura en x=70 si μ=70, σ=5
        >>> normal_pdf(70, mu=70, sigma=5)
        0.0797...

    Uso típico:
        Graficar la curva de campana o calcular la verosimilitud de una observación.
        Para calcular probabilidades de intervalos, usa normal_cdf().
    """
    if sigma <= 0:
        raise ValueError(f"σ (sigma) debe ser > 0 (recibido: {sigma})")

    # Cálculo de la PDF
    coefficient = 1.0 / (sigma * math.sqrt(2.0 * math.pi))
    exponent = -0.5 * ((x - mu) / sigma) ** 2
    
    return coefficient * math.exp(exponent)


def normal_cdf(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    """
    Calcula P(X ≤ x) para una distribución normal con media μ y desviación σ.

    Esta es la función principal para calcular probabilidades con la normal.

    Proceso:
        1. Estandariza: z = (x - μ) / σ
        2. Calcula Φ(z) usando la normal estándar N(0,1)
        3. Retorna la probabilidad

    Parámetros:
        x     (float): valor hasta el cual calcular la probabilidad
        mu    (float): media de la distribución (por defecto 0)
        sigma (float): desviación estándar (por defecto 1, debe ser > 0)

    Retorna:
        float: P(X ≤ x), probabilidad entre 0 y 1

    Raises:
        ValueError: si sigma ≤ 0

    Ejemplos de uso:
        # Altura de personas: μ=170cm, σ=10cm
        # ¿Probabilidad de medir ≤ 180cm?
        >>> normal_cdf(180, mu=170, sigma=10)
        0.8413...

        # Notas de examen: μ=70, σ=10
        # ¿Probabilidad de sacar ≤ 85?
        >>> normal_cdf(85, mu=70, sigma=10)
        0.9331...

        # Normal estándar: P(Z ≤ 1.96) ≈ 0.975
        >>> normal_cdf(1.96, mu=0, sigma=1)
        0.9750...

    Calcular otros tipos de probabilidades:
        - P(X > a)       : 1 - normal_cdf(a, mu, sigma)
        - P(a < X ≤ b)   : normal_cdf(b, mu, sigma) - normal_cdf(a, mu, sigma)
        - P(|X - μ| ≤ k) : normal_cdf(mu+k, mu, sigma) - normal_cdf(mu-k, mu, sigma)
    """
    if sigma <= 0:
        raise ValueError(f"σ (sigma) debe ser > 0 (recibido: {sigma})")

    # Estandarizar a N(0,1)
    z = (x - mu) / sigma
    
    # Usar la CDF de la normal estándar
    return _standard_normal_cdf(z)


def normal_ppf(p: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    """
    Calcula el percentil (inverso de la CDF) de la distribución normal.

    Función inversa de normal_cdf: dado una probabilidad p, encuentra x tal que
    P(X ≤ x) = p.

    Parámetros:
        p     (float): probabilidad entre 0 y 1
        mu    (float): media de la distribución (por defecto 0)
        sigma (float): desviación estándar (por defecto 1)

    Retorna:
        float: valor x tal que P(X ≤ x) = p

    Raises:
        ValueError: si p no está en (0, 1) o sigma ≤ 0
        ImportError: si scipy no está disponible (se requiere para esta función)

    Ejemplos:
        # ¿Qué nota necesito para estar en el top 10%? (μ=70, σ=10)
        >>> normal_ppf(0.90, mu=70, sigma=10)
        82.81...

        # Percentil 95 de la normal estándar
        >>> normal_ppf(0.95, mu=0, sigma=1)
        1.6448...

    Notas:
        Esta función requiere scipy porque calcular la inversa de la normal
        no tiene una fórmula cerrada y requiere métodos numéricos avanzados.
        Si scipy no está disponible, se lanza ImportError.
    """
    if not 0 < p < 1:
        raise ValueError(f"p debe estar entre 0 y 1 (recibido: {p})")
    
    if sigma <= 0:
        raise ValueError(f"σ (sigma) debe ser > 0 (recibido: {sigma})")

    if not SCIPY_AVAILABLE:
        raise ImportError(
            "normal_ppf requiere scipy. Instala con: pip install scipy"
        )

    # Usar scipy para calcular la inversa
    return norm.ppf(p, loc=mu, scale=sigma)


def z_score(x: float, mu: float, sigma: float) -> float:
    """
    Calcula el Z-score (valor estandarizado) de x.

    El Z-score representa cuántas desviaciones estándar está x de la media.

    Fórmula:
        z = (x - μ) / σ

    Parámetros:
        x     (float): valor a estandarizar
        mu    (float): media de la distribución
        sigma (float): desviación estándar

    Retorna:
        float: número de desviaciones estándar desde la media

    Raises:
        ValueError: si sigma ≤ 0

    Ejemplos:
        # Si μ=100, σ=15 (IQ), ¿cuántas σ's es 130?
        >>> z_score(130, mu=100, sigma=15)
        2.0

        # Valor exactamente en la media
        >>> z_score(70, mu=70, sigma=10)
        0.0

    Interpretación:
        - z = 0  : valor en la media
        - z > 0  : valor por encima de la media
        - z < 0  : valor por debajo de la media
        - |z| > 2: valor inusual (fuera de ~95% de los datos)
        - |z| > 3: valor muy raro (fuera de ~99.7% de los datos)
    """
    if sigma <= 0:
        raise ValueError(f"σ (sigma) debe ser > 0 (recibido: {sigma})")

    return (x - mu) / sigma


def normal_interval(confidence: float, mu: float = 0.0, sigma: float = 1.0) -> Tuple[float, float]:
    """
    Calcula el intervalo de confianza simétrico alrededor de la media.

    Retorna (a, b) tal que P(a ≤ X ≤ b) = confidence.

    Parámetros:
        confidence (float): nivel de confianza entre 0 y 1 (ej. 0.95 para 95%)
        mu         (float): media de la distribución (por defecto 0)
        sigma      (float): desviación estándar (por defecto 1)

    Retorna:
        Tuple[float, float]: (límite_inferior, límite_superior)

    Raises:
        ValueError: si confidence no está en (0, 1) o sigma ≤ 0
        ImportError: si scipy no está disponible

    Ejemplos:
        # Intervalo del 95% para N(100, 15)
        >>> normal_interval(0.95, mu=100, sigma=15)
        (70.6..., 129.4...)

        # Intervalo del 99% para N(0, 1)
        >>> normal_interval(0.99, mu=0, sigma=1)
        (-2.57..., 2.57...)

    Uso típico:
        Encontrar el rango donde caen el 95% de los valores en una distribución normal.
    """
    if not 0 < confidence < 1:
        raise ValueError(f"confidence debe estar entre 0 y 1 (recibido: {confidence})")

    # Probabilidad en cada cola
    alpha = (1 - confidence) / 2

    # Percentiles
    lower = normal_ppf(alpha, mu, sigma)
    upper = normal_ppf(1 - alpha, mu, sigma)

    return (lower, upper)


# ══════════════════════════════════════════════════════════════════════
#  DISTRIBUCIÓN EXPONENCIAL
# ══════════════════════════════════════════════════════════════════════

def exponential_pdf(x: float, lam: float) -> float:
    """
    Calcula la función de densidad de probabilidad (PDF) de la distribución exponencial.

    La exponencial modela el tiempo hasta que ocurre el primer evento en un
    proceso de Poisson (tiempo entre llegadas, vida útil de componentes, etc.).

    Fórmula:
        f(x) = λ × e^(-λx)  para x ≥ 0
        f(x) = 0            para x < 0

    Parámetros:
        x   (float): valor a evaluar (debe ser ≥ 0)
        lam (float): tasa de eventos λ (debe ser > 0)

    Retorna:
        float: densidad en el punto x

    Raises:
        ValueError: si lam ≤ 0

    Ejemplos:
        # Densidad en x=2 para λ=0.5
        >>> exponential_pdf(2.0, lam=0.5)
        0.1839...

        # En x=0, la densidad es máxima = λ
        >>> exponential_pdf(0, lam=0.5)
        0.5

    Propiedades:
        - La exponencial es "sin memoria": P(X > s+t | X > s) = P(X > t)
        - Media = 1/λ
        - Mediana = ln(2)/λ ≈ 0.693/λ
        - Moda = 0 (valor más probable)
    """
    if lam <= 0:
        raise ValueError(f"λ (lambda) debe ser > 0 (recibido: {lam})")

    if x < 0:
        return 0.0

    return lam * math.exp(-lam * x)


def exponential_cdf(x: float, lam: float) -> float:
    """
    Calcula P(X ≤ x) para una distribución exponencial con tasa λ.

    Esta es la función principal para calcular probabilidades con la exponencial.

    Fórmula:
        F(x) = 1 - e^(-λx)  para x ≥ 0
        F(x) = 0            para x < 0

    Parámetros:
        x   (float): valor hasta el cual calcular la probabilidad
        lam (float): tasa de eventos λ (debe ser > 0)

    Retorna:
        float: P(X ≤ x), probabilidad entre 0 y 1

    Raises:
        ValueError: si lam ≤ 0

    Ejemplos de uso:
        # Componente con vida media de 2 años (λ = 0.5)
        # ¿Probabilidad de que falle antes de 3 años?
        >>> exponential_cdf(3.0, lam=0.5)
        0.7768...

        # Tiempo entre llamadas promedio = 5 min (λ = 0.2)
        # ¿Probabilidad de esperar ≤ 10 min?
        >>> exponential_cdf(10.0, lam=0.2)
        0.8646...

        # En x=0, la probabilidad es siempre 0
        >>> exponential_cdf(0, lam=0.5)
        0.0

    Calcular otros tipos de probabilidades:
        - P(X > a)       : 1 - exponential_cdf(a, lam)
        - P(a < X ≤ b)   : exponential_cdf(b, lam) - exponential_cdf(a, lam)

    Relación con Poisson:
        Si el número de eventos en un intervalo sigue Poisson(λ),
        entonces el tiempo entre eventos sigue Exponencial(λ).
    """
    if lam <= 0:
        raise ValueError(f"λ (lambda) debe ser > 0 (recibido: {lam})")

    if x < 0:
        return 0.0

    # F(x) = 1 - e^(-λx)
    return 1.0 - math.exp(-lam * x)


def exponential_ppf(p: float, lam: float) -> float:
    """
    Calcula el percentil (inverso de la CDF) de la distribución exponencial.

    Dado una probabilidad p, encuentra x tal que P(X ≤ x) = p.

    Fórmula:
        x = -ln(1 - p) / λ

    Parámetros:
        p   (float): probabilidad entre 0 y 1
        lam (float): tasa de eventos λ (debe ser > 0)

    Retorna:
        float: valor x tal que P(X ≤ x) = p

    Raises:
        ValueError: si p no está en (0, 1) o lam ≤ 0

    Ejemplos:
        # ¿Cuánto tiempo antes del 90% de las fallas? (λ=0.5)
        >>> exponential_ppf(0.90, lam=0.5)
        4.605...

        # Mediana (50%) de la distribución
        >>> exponential_ppf(0.50, lam=0.5)
        1.386...

    Uso típico:
        Determinar garantías de productos, SLAs, o plazos basados en percentiles.
    """
    if not 0 < p < 1:
        raise ValueError(f"p debe estar entre 0 y 1 (recibido: {p})")
    
    if lam <= 0:
        raise ValueError(f"λ (lambda) debe ser > 0 (recibido: {lam})")

    # x = -ln(1 - p) / λ
    return -math.log(1 - p) / lam


def exponential_mean(lam: float) -> float:
    """
    Calcula la media (valor esperado) de una distribución exponencial.

    Fórmula:
        E[X] = 1 / λ

    Parámetros:
        lam (float): tasa de eventos

    Retorna:
        float: media de la distribución

    Raises:
        ValueError: si lam ≤ 0

    Ejemplo:
        # Si λ = 0.5 eventos/hora, tiempo promedio entre eventos = 2 horas
        >>> exponential_mean(0.5)
        2.0
    """
    if lam <= 0:
        raise ValueError(f"λ (lambda) debe ser > 0 (recibido: {lam})")

    return 1.0 / lam


def exponential_variance(lam: float) -> float:
    """
    Calcula la varianza de una distribución exponencial.

    Fórmula:
        Var(X) = 1 / λ²

    Parámetros:
        lam (float): tasa de eventos

    Retorna:
        float: varianza de la distribución

    Raises:
        ValueError: si lam ≤ 0

    Ejemplo:
        >>> exponential_variance(0.5)
        4.0
    """
    if lam <= 0:
        raise ValueError(f"λ (lambda) debe ser > 0 (recibido: {lam})")

    return 1.0 / (lam ** 2)


def exponential_std(lam: float) -> float:
    """
    Calcula la desviación estándar de una distribución exponencial.

    Fórmula:
        σ = 1 / λ

    Parámetros:
        lam (float): tasa de eventos

    Retorna:
        float: desviación estándar

    Ejemplo:
        >>> exponential_std(0.5)
        2.0

    Nota interesante:
        En la exponencial, σ = μ (la desviación estándar es igual a la media).
    """
    if lam <= 0:
        raise ValueError(f"λ (lambda) debe ser > 0 (recibido: {lam})")

    return 1.0 / lam


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
    
    if func_name == "normal_cdf":
        scipy_result = norm.cdf(params["x"], loc=params["mu"], scale=params["sigma"])
    elif func_name == "exponential_cdf":
        scipy_result = expon.cdf(params["x"], scale=1/params["lam"])
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
    print("🧪 Probando calculators/continuous.py\n")
    print("=" * 60)
    
    # ── Test Normal ──
    print("\n📊 DISTRIBUCIÓN NORMAL:")
    print("Alturas de personas: μ=170cm, σ=10cm")
    x, mu, sigma = 180, 170, 10
    result = normal_cdf(x, mu, sigma)
    z = z_score(x, mu, sigma)
    print(f"  P(X ≤ {x}) = {result:.6f}  ({result * 100:.2f}%)")
    print(f"  Z-score: {z:.2f}")
    print(f"  Media: {mu} cm")
    print(f"  Desv. estándar: {sigma} cm")
    
    if SCIPY_AVAILABLE:
        _verify_with_scipy("normal_cdf", {"x": x, "mu": mu, "sigma": sigma}, result)
    
    # ── Test Exponencial ──
    print("\n📊 DISTRIBUCIÓN EXPONENCIAL:")
    print("Tiempo entre llamadas: λ=0.5 llamadas/minuto")
    x, lam = 2.0, 0.5
    result = exponential_cdf(x, lam)
    print(f"  P(X ≤ {x} min) = {result:.6f}  ({result * 100:.2f}%)")
    print(f"  Tiempo promedio entre llamadas: {exponential_mean(lam):.1f} min")
    print(f"  Desv. estándar: {exponential_std(lam):.1f} min")
    
    if SCIPY_AVAILABLE:
        _verify_with_scipy("exponential_cdf", {"x": x, "lam": lam}, result)
    
    # ── Test Z-scores ──
    print("\n🔢 Z-SCORES (Normal estándar N(0,1)):")
    test_values = [0, 1, 1.96, 2.58]
    for z in test_values:
        prob = normal_cdf(z, mu=0, sigma=1)
        print(f"  Φ({z:5.2f}) = {prob:.6f}  ({prob * 100:.2f}%)")
    
    # ── Test Regla 68-95-99.7 ──
    print("\n📏 REGLA 68-95-99.7 (Regla empírica):")
    mu_test, sigma_test = 100, 15
    for k in [1, 2, 3]:
        lower = mu_test - k * sigma_test
        upper = mu_test + k * sigma_test
        prob = normal_cdf(upper, mu_test, sigma_test) - normal_cdf(lower, mu_test, sigma_test)
        print(f"  P({lower} ≤ X ≤ {upper}) = {prob:.6f}  ({prob * 100:.2f}%)")
        print(f"    Esperado para ±{k}σ: {[68.27, 95.45, 99.73][k-1]:.2f}%")
    
    print("\n" + "=" * 60)
    print("✅ Tests completados. Si scipy está instalado, se muestran comparaciones.")
