"""
main.py — Punto de entrada de la Calculadora de Probabilidades
===============================================================

Este módulo gestiona toda la interfaz interactiva de terminal.
Se encarga de:
  - Mostrar el menú principal y los submenús de cada distribución
  - Solicitar y validar los parámetros del usuario
  - Llamar a los módulos de cálculo correspondientes
  - Mostrar los resultados con formato visual usando `rich`

Flujo general:
  main() → show_main_menu() → [distribución elegida] → get_params() → show_result()

Dependencias externas:
  - rich  : para colores, tablas y paneles en terminal
            instalar con: pip install rich

Dependencias internas:
  - calculators.discrete    : cálculos de Binomial y Poisson
  - calculators.continuous  : cálculos de Normal y Exponencial
  - utils.validators        : validación de entradas del usuario

Autor  : Tu Nombre
GitHub : https://github.com/tu-usuario
"""

# ─────────────────────────────────────────────
#  Importaciones estándar de Python
# ─────────────────────────────────────────────
import sys                  # Para sys.exit() al cerrar el programa

# ─────────────────────────────────────────────
#  Importaciones de rich (UI de terminal)
# ─────────────────────────────────────────────
from rich.console import Console        # Motor principal de impresión con estilos
from rich.panel import Panel            # Cuadros/paneles con bordes decorativos
from rich.table import Table            # Tablas con columnas y filas estilizadas
from rich.text import Text              # Texto con múltiples estilos en la misma línea
from rich.prompt import Prompt          # Entrada de usuario estilizada
from rich.rule import Rule              # Líneas horizontales decorativas
from rich.padding import Padding        # Espaciado alrededor de elementos
from rich import print as rprint        # print() con soporte de markup [bold], [red], etc.

# ─────────────────────────────────────────────
#  Importaciones internas del proyecto
#  (se activarán cuando crees esos módulos)
# ─────────────────────────────────────────────
# from calculators.discrete import binomial, poisson
# from calculators.continuous import normal, exponential
# from utils.validators import validate_probability, validate_positive_int

# ─────────────────────────────────────────────
#  Instancia global de Console
#  Usamos `console.print()` en lugar de `print()`
#  para aprovechar todos los estilos de rich
# ─────────────────────────────────────────────
console = Console()


# ══════════════════════════════════════════════════════════════════════
#  CONSTANTES DE CONFIGURACIÓN
#  Centralizar estos valores facilita cambiarlos sin buscar en el código
# ══════════════════════════════════════════════════════════════════════

APP_NAME    = "🎲 Probability Calculator"
APP_VERSION = "v1.0.0"
APP_AUTHOR  = "Sred"

# Colores del tema — cámbialos aquí para personalizar toda la app
COLOR_PRIMARY   = "cyan"        # Títulos y elementos destacados
COLOR_SECONDARY = "magenta"     # Submenús y etiquetas
COLOR_SUCCESS   = "green"       # Resultados positivos / confirmaciones
COLOR_WARNING   = "yellow"      # Advertencias y validaciones
COLOR_ERROR     = "red"         # Errores y entradas inválidas
COLOR_DIM       = "dim white"   # Texto secundario / ayuda

# Opciones del menú principal
# Formato: (clave que escribe el usuario, etiqueta visible, descripción breve)
MAIN_MENU_OPTIONS = [
    ("1", "Binomial Distribution",    "P(X = k) — successes in n trials"),
    ("2", "Poisson Distribution",     "P(X = k) — events in an interval"),
    ("3", "Normal Distribution",      "P(X < x) — continuous bell curve"),
    ("4", "Exponential Distribution", "P(X < x) — time between events"),
    ("0", "Exit",                     "Close the calculator"),
]


# ══════════════════════════════════════════════════════════════════════
#  FUNCIONES DE INTERFAZ — PANTALLAS Y COMPONENTES VISUALES
# ══════════════════════════════════════════════════════════════════════

def clear_screen() -> None:
    """
    Limpia la pantalla imprimiendo líneas en blanco.

    Se evita usar os.system('clear') para mantener compatibilidad
    entre sistemas operativos sin depender de comandos de shell.
    """
    console.print("\n" * 2)


def show_header() -> None:
    """
    Muestra el encabezado principal de la aplicación.

    Imprime el nombre, versión y autor dentro de un panel decorativo.
    Se llama al inicio de cada pantalla para mantener el contexto visual.

    Ejemplo de output:
    ┌─────────────────────────────────────┐
    │   🎲 Probability Calculator  v1.0.0 │
    │           by Tu Nombre             │
    └─────────────────────────────────────┘
    """
    title = Text()
    title.append(APP_NAME,    style=f"bold {COLOR_PRIMARY}")
    title.append(f"  {APP_VERSION}", style=COLOR_DIM)

    subtitle = Text(f"by {APP_AUTHOR}", style=COLOR_DIM, justify="center")

    # Panel de rich: `expand=False` para que no ocupe todo el ancho
    console.print(Panel(
        title + "\n" + subtitle,
        border_style=COLOR_PRIMARY,
        expand=False,
        padding=(1, 4),
    ))


def show_main_menu() -> None:
    """
    Renderiza el menú principal con todas las distribuciones disponibles.

    Construye una tabla de rich con tres columnas:
      - Número de opción
      - Nombre de la distribución
      - Descripción breve de lo que calcula

    No retorna nada — solo imprime en pantalla.
    """
    # Encabezado de sección
    console.print(Rule(f"[{COLOR_SECONDARY}] Select a Distribution [/]"))
    console.print()

    # Tabla con las opciones del menú
    table = Table(
        show_header=True,
        header_style=f"bold {COLOR_SECONDARY}",
        border_style=COLOR_DIM,
        padding=(0, 2),
    )

    table.add_column("Option", style=f"bold {COLOR_PRIMARY}", width=8)
    table.add_column("Distribution",                          width=30)
    table.add_column("Calculates",  style=COLOR_DIM,          width=40)

    for key, label, description in MAIN_MENU_OPTIONS:
        # La opción 0 (Exit) se muestra con estilo diferente
        row_style = COLOR_ERROR if key == "0" else "white"
        table.add_row(f"[{key}]", label, description, style=row_style)

    console.print(table)
    console.print()


def show_result_panel(
    distribution: str,
    params: dict,
    formula: str,
    result: float,
) -> None:
    """
    Muestra el resultado de un cálculo en un panel estructurado.

    Parámetros:
        distribution (str)  : nombre de la distribución (ej. "Binomial")
        params       (dict) : diccionario con los parámetros usados
                              ej. {"n": 10, "k": 3, "p": 0.5}
        formula      (str)  : fórmula aplicada en texto plano
                              ej. "C(10,3) × 0.5³ × 0.5⁷"
        result       (float): probabilidad calculada entre 0 y 1

    Ejemplo de output:
    ╭─── Binomial Distribution ────────────────╮
    │  Parameters: n=10, k=3, p=0.5            │
    │  Formula   : C(10,3) × 0.5³ × 0.5⁷      │
    │                                          │
    │  ✔  P(X = k) = 0.1172  (11.72%)          │
    ╰──────────────────────────────────────────╯
    """
    # Construir la línea de parámetros: "n=10, k=3, p=0.5"
    params_str = ", ".join(f"{k}={v}" for k, v in params.items())

    # Construir el texto del resultado con porcentaje incluido
    result_text = Text()
    result_text.append("  ✔  ", style=f"bold {COLOR_SUCCESS}")
    result_text.append("Result = ", style="bold white")
    result_text.append(f"{result:.4f}", style=f"bold {COLOR_SUCCESS}")
    result_text.append(f"  ({result * 100:.2f}%)", style=COLOR_DIM)

    # Contenido completo del panel
    content = (
        f"[{COLOR_DIM}]Distribution :[/] [{COLOR_PRIMARY}]{distribution}[/]\n"
        f"[{COLOR_DIM}]Parameters   :[/] {params_str}\n"
        f"[{COLOR_DIM}]Formula      :[/] [italic]{formula}[/]\n\n"
    )

    console.print(Panel(
        content + result_text.markup,
        title=f"[bold {COLOR_SUCCESS}] Result [/]",
        border_style=COLOR_SUCCESS,
        padding=(1, 2),
    ))


def show_error(message: str) -> None:
    """
    Muestra un mensaje de error formateado.

    Parámetros:
        message (str): descripción del error a mostrar al usuario

    Ejemplo de output:
      ✘  Invalid input: probability must be between 0 and 1.
    """
    console.print(f"\n  [{COLOR_ERROR}]✘  Invalid input:[/] {message}\n")


def ask_continue() -> bool:
    """
    Pregunta al usuario si desea realizar otro cálculo.

    Retorna:
        bool: True si el usuario quiere continuar, False para salir.

    El prompt acepta 'y' o 'n' (case-insensitive).
    Cualquier entrada distinta se interpreta como 'n'.
    """
    console.print()
    answer = Prompt.ask(
        f"  [{COLOR_SECONDARY}]Calculate again?[/] (y/n)",
        default="y",
    )
    return answer.strip().lower() == "y"


# ══════════════════════════════════════════════════════════════════════
#  FUNCIONES DE CAPTURA DE PARÁMETROS
#  Cada distribución tiene su propia función `get_*_params()`
#  porque los parámetros necesarios son distintos para cada una.
#  Todas retornan un dict o None si el usuario cancela.
# ══════════════════════════════════════════════════════════════════════

def get_float_input(prompt_text: str, min_val: float = None, max_val: float = None) -> float | None:
    """
    Solicita un número decimal al usuario con validación de rango.

    Parámetros:
        prompt_text (str)          : texto del prompt que ve el usuario
        min_val     (float | None) : valor mínimo permitido (inclusive)
        max_val     (float | None) : valor máximo permitido (inclusive)

    Retorna:
        float : el valor ingresado si es válido
        None  : si el usuario escribe 'q' para cancelar

    Notas:
        - Sigue pidiendo el valor hasta recibir uno válido o 'q'
        - Muestra un mensaje de ayuda con el rango permitido
    """
    # Construir indicación de rango para el prompt
    range_hint = ""
    if min_val is not None and max_val is not None:
        range_hint = f"[{COLOR_DIM}] ({min_val} – {max_val})[/]"
    elif min_val is not None:
        range_hint = f"[{COLOR_DIM}] (min: {min_val})[/]"

    while True:
        raw = Prompt.ask(f"  {prompt_text}{range_hint}")

        # Opción de cancelar
        if raw.strip().lower() == "q":
            return None

        # Intentar convertir a float
        try:
            value = float(raw)
        except ValueError:
            show_error("Please enter a valid number. Type 'q' to cancel.")
            continue

        # Validar rango
        if min_val is not None and value < min_val:
            show_error(f"Value must be ≥ {min_val}.")
            continue
        if max_val is not None and value > max_val:
            show_error(f"Value must be ≤ {max_val}.")
            continue

        return value


def get_int_input(prompt_text: str, min_val: int = 0) -> int | None:
    """
    Solicita un número entero positivo al usuario con validación.

    Parámetros:
        prompt_text (str) : texto del prompt
        min_val     (int) : valor mínimo permitido (por defecto 0)

    Retorna:
        int  : el entero ingresado si es válido
        None : si el usuario escribe 'q' para cancelar

    Notas:
        - Rechaza decimales (1.5 no es válido como entero)
        - Sigue pidiendo hasta recibir un valor válido o 'q'
    """
    while True:
        raw = Prompt.ask(f"  {prompt_text} [{COLOR_DIM}](integer ≥ {min_val})[/]")

        if raw.strip().lower() == "q":
            return None

        # Verificar que no sea decimal
        if "." in raw:
            show_error("This parameter must be a whole number (integer), not decimal.")
            continue

        try:
            value = int(raw)
        except ValueError:
            show_error("Please enter a valid whole number. Type 'q' to cancel.")
            continue

        if value < min_val:
            show_error(f"Value must be ≥ {min_val}.")
            continue

        return value


def get_binomial_params() -> dict | None:
    """
    Solicita los parámetros necesarios para la distribución Binomial.

    Parámetros requeridos:
        n (int)   : número total de intentos (n ≥ 1)
        k (int)   : número de éxitos deseados (0 ≤ k ≤ n)
        p (float) : probabilidad de éxito en cada intento (0 ≤ p ≤ 1)

    Retorna:
        dict : {"n": int, "k": int, "p": float}
        None : si el usuario cancela en cualquier punto (escribe 'q')

    Ejemplo de uso:
        params = get_binomial_params()
        if params:
            result = binomial(**params)
    """
    console.print(f"\n  [{COLOR_PRIMARY}]Binomial Distribution[/] — P(X = k)")
    console.print(f"  [{COLOR_DIM}]Type 'q' at any prompt to cancel[/]\n")

    # Solicitar n
    n = get_int_input("n — total number of trials", min_val=1)
    if n is None:
        return None

    # Solicitar k (no puede ser mayor que n)
    k = get_int_input(f"k — number of successes (max {n})", min_val=0)
    if k is None:
        return None

    if k > n:
        show_error(f"k ({k}) cannot be greater than n ({n}).")
        return None

    # Solicitar p
    p = get_float_input("p — probability of success per trial", min_val=0.0, max_val=1.0)
    if p is None:
        return None

    return {"n": n, "k": k, "p": p}


def get_poisson_params() -> dict | None:
    """
    Solicita los parámetros necesarios para la distribución de Poisson.

    Parámetros requeridos:
        lam (float) : tasa promedio de eventos en el intervalo (λ > 0)
        k   (int)   : número de eventos a calcular (k ≥ 0)

    Retorna:
        dict : {"lam": float, "k": int}
        None : si el usuario cancela

    Nota sobre el nombre 'lam':
        Se usa 'lam' en lugar de 'lambda' porque 'lambda' es
        una palabra reservada en Python.
    """
    console.print(f"\n  [{COLOR_PRIMARY}]Poisson Distribution[/] — P(X = k)")
    console.print(f"  [{COLOR_DIM}]Type 'q' at any prompt to cancel[/]\n")

    lam = get_float_input("λ (lambda) — average rate of events", min_val=0.0001)
    if lam is None:
        return None

    k = get_int_input("k — number of events to calculate", min_val=0)
    if k is None:
        return None

    return {"lam": lam, "k": k}


def get_normal_params() -> dict | None:
    """
    Solicita los parámetros necesarios para la distribución Normal.

    Parámetros requeridos:
        x     (float) : valor hasta el cual calcular P(X < x)
        mu    (float) : media de la distribución (μ)
        sigma (float) : desviación estándar (σ > 0)

    Retorna:
        dict : {"x": float, "mu": float, "sigma": float}
        None : si el usuario cancela

    Calcula:
        P(X < x) usando la función de distribución acumulada (CDF)
    """
    console.print(f"\n  [{COLOR_PRIMARY}]Normal Distribution[/] — P(X < x)")
    console.print(f"  [{COLOR_DIM}]Type 'q' at any prompt to cancel[/]\n")

    x = get_float_input("x — value to evaluate")
    if x is None:
        return None

    mu = get_float_input("μ (mu) — mean of the distribution")
    if mu is None:
        return None

    sigma = get_float_input("σ (sigma) — standard deviation", min_val=0.0001)
    if sigma is None:
        return None

    return {"x": x, "mu": mu, "sigma": sigma}


def get_exponential_params() -> dict | None:
    """
    Solicita los parámetros necesarios para la distribución Exponencial.

    Parámetros requeridos:
        x     (float) : valor hasta el cual calcular P(X < x), x ≥ 0
        lam   (float) : tasa de eventos λ (inverso de la media), λ > 0

    Retorna:
        dict : {"x": float, "lam": float}
        None : si el usuario cancela

    Calcula:
        P(X < x) = 1 - e^(-λx)
    """
    console.print(f"\n  [{COLOR_PRIMARY}]Exponential Distribution[/] — P(X < x)")
    console.print(f"  [{COLOR_DIM}]Type 'q' at any prompt to cancel[/]\n")

    x = get_float_input("x — time/distance value", min_val=0.0)
    if x is None:
        return None

    lam = get_float_input("λ (lambda) — event rate (1 / mean)", min_val=0.0001)
    if lam is None:
        return None

    return {"x": x, "lam": lam}


# ══════════════════════════════════════════════════════════════════════
#  FUNCIONES DE CÁLCULO (PLACEHOLDERS)
#  Estas funciones están preparadas para recibir los resultados
#  de los módulos calculators/ cuando los crees.
#  Por ahora simulan un resultado para que el menú sea funcional.
# ══════════════════════════════════════════════════════════════════════

def handle_binomial(params: dict) -> None:
    """
    Orquesta el cálculo y visualización de la distribución Binomial.

    Parámetros:
        params (dict): {"n": int, "k": int, "p": float}

    Flujo:
        1. Llama al calculador (por conectar)
        2. Construye la fórmula legible
        3. Llama a show_result_panel() con todo listo

    TODO: reemplazar el resultado simulado por:
        from calculators.discrete import binomial
        result = binomial(params["n"], params["k"], params["p"])
    """
    # ── Resultado simulado hasta conectar calculators/discrete.py ──
    result = 0.1172  # Placeholder

    formula = f"C({params['n']},{params['k']}) × {params['p']}^{params['k']} × {1 - params['p']}^{params['n'] - params['k']}"

    show_result_panel(
        distribution="Binomial",
        params=params,
        formula=formula,
        result=result,
    )


def handle_poisson(params: dict) -> None:
    """
    Orquesta el cálculo y visualización de la distribución de Poisson.

    Parámetros:
        params (dict): {"lam": float, "k": int}

    TODO: reemplazar el resultado simulado por:
        from calculators.discrete import poisson
        result = poisson(params["lam"], params["k"])
    """
    result = 0.1804  # Placeholder

    formula = f"(e^-{params['lam']} × {params['lam']}^{params['k']}) / {params['k']}!"

    show_result_panel(
        distribution="Poisson",
        params={"λ": params["lam"], "k": params["k"]},
        formula=formula,
        result=result,
    )


def handle_normal(params: dict) -> None:
    """
    Orquesta el cálculo y visualización de la distribución Normal.

    Parámetros:
        params (dict): {"x": float, "mu": float, "sigma": float}

    TODO: reemplazar el resultado simulado por:
        from calculators.continuous import normal_cdf
        result = normal_cdf(params["x"], params["mu"], params["sigma"])
    """
    result = 0.8413  # Placeholder

    z = (params["x"] - params["mu"]) / params["sigma"]
    formula = f"Φ(z)  where  z = ({params['x']} - {params['mu']}) / {params['sigma']} = {z:.2f}"

    show_result_panel(
        distribution="Normal",
        params={"x": params["x"], "μ": params["mu"], "σ": params["sigma"]},
        formula=formula,
        result=result,
    )


def handle_exponential(params: dict) -> None:
    """
    Orquesta el cálculo y visualización de la distribución Exponencial.

    Parámetros:
        params (dict): {"x": float, "lam": float}

    TODO: reemplazar el resultado simulado por:
        from calculators.continuous import exponential_cdf
        result = exponential_cdf(params["x"], params["lam"])
    """
    result = 0.6321  # Placeholder

    formula = f"1 - e^(-{params['lam']} × {params['x']})"

    show_result_panel(
        distribution="Exponential",
        params={"x": params["x"], "λ": params["lam"]},
        formula=formula,
        result=result,
    )


# ══════════════════════════════════════════════════════════════════════
#  ROUTER — Despacha la opción elegida al handler correspondiente
# ══════════════════════════════════════════════════════════════════════

# Mapea cada opción del menú a su función de parámetros y su handler.
# Usar un diccionario evita un bloque if/elif largo y facilita agregar
# nuevas distribuciones en el futuro con solo añadir una entrada aquí.
DISTRIBUTION_ROUTER = {
    "1": (get_binomial_params,    handle_binomial),
    "2": (get_poisson_params,     handle_poisson),
    "3": (get_normal_params,      handle_normal),
    "4": (get_exponential_params, handle_exponential),
}


def route_selection(choice: str) -> bool:
    """
    Ejecuta el flujo completo para la distribución seleccionada.

    Parámetros:
        choice (str): clave del menú ("1", "2", "3", "4" o "0")

    Retorna:
        bool: False si el usuario eligió salir ("0"), True en cualquier otro caso.

    Flujo por cada distribución:
        1. Obtiene la función de parámetros y el handler del router
        2. Llama a get_params() — si retorna None, el usuario canceló
        3. Si hay parámetros, llama al handler para calcular y mostrar
    """
    if choice == "0":
        return False  # Señal de salida para el loop principal

    if choice not in DISTRIBUTION_ROUTER:
        show_error("Invalid option. Please choose a number from the menu.")
        return True

    get_params, handler = DISTRIBUTION_ROUTER[choice]

    # Solicitar parámetros — puede retornar None si el usuario cancela
    params = get_params()

    if params is None:
        console.print(f"\n  [{COLOR_WARNING}]Calculation cancelled.[/]\n")
        return True

    # Ejecutar cálculo y mostrar resultado
    console.print()
    handler(params)

    return True


# ══════════════════════════════════════════════════════════════════════
#  FUNCIÓN PRINCIPAL — Loop de la aplicación
# ══════════════════════════════════════════════════════════════════════

def main() -> None:
    """
    Punto de entrada y loop principal de la aplicación.

    Ciclo de vida:
        1. Muestra encabezado y menú principal
        2. Lee la opción del usuario
        3. Despacha al handler correspondiente via route_selection()
        4. Pregunta si continuar → vuelve a 1, o muestra despedida y sale

    Control de salida:
        - Opción "0" en el menú
        - Responder "n" en ask_continue()
        - Ctrl+C (KeyboardInterrupt) — manejado gracefully
    """
    try:
        while True:
            clear_screen()
            show_header()
            show_main_menu()

            # Leer la opción del usuario
            choice = Prompt.ask(
                f"  [{COLOR_PRIMARY}]Enter option[/]",
                choices=[opt[0] for opt in MAIN_MENU_OPTIONS],
                show_choices=False,
            )

            console.print()

            # Despachar y verificar si continuar
            should_continue = route_selection(choice)

            if not should_continue:
                break   # El usuario eligió Exit

            # Preguntar si desea otro cálculo
            if not ask_continue():
                break

    except KeyboardInterrupt:
        # Ctrl+C — salida limpia sin traceback
        console.print()

    finally:
        # Mensaje de despedida — siempre se ejecuta al salir
        console.print(f"\n  [{COLOR_DIM}]Thanks for using {APP_NAME}. Goodbye! 👋[/]\n")
        sys.exit(0)


# ══════════════════════════════════════════════════════════════════════
#  ENTRY POINT
#  Este bloque garantiza que main() solo se ejecute cuando el archivo
#  se corre directamente (python main.py), no cuando se importa como
#  módulo desde otro archivo.
# ══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    main()
