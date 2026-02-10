# Probability-Calculator
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-22c55e?style=flat)
![Status](https://img.shields.io/badge/status-active-22c55e?style=flat)
![Terminal](https://img.shields.io/badge/interface-terminal-black?style=flat)

> 🇺🇸 [English](#english) | 🇪🇸 [Español](#español)

---

<a name="english"></a>
## 🇺🇸 English

An interactive terminal-based probability calculator built with Python. Compute probabilities for discrete and continuous distributions through a clean, menu-driven interface — no statistics background required.

### ✨ Features

- **Discrete Distributions**
  - Binomial — probability of *k* successes in *n* trials
  - Poisson — probability of *k* events given a rate λ
- **Continuous Distributions**
  - Normal — PDF, CDF and Z-score calculations
  - Exponential — probability over time/distance intervals
- Interactive terminal menu powered by `rich`
- Input validation with clear error messages
- Results displayed with the underlying formula used

### 📸 Demo

> *(Add a screenshot or GIF of your terminal here)*
> 
> Tip: Use [asciinema](https://asciinema.org/) or [terminalizer](https://www.terminalizer.com/) to record your terminal.

### 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/probability-calculator
cd probability-calculator

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

### ▶️ Usage

```bash
python main.py
```

Once launched, navigate the menu using arrow keys and press Enter to select an option.

### 📖 Usage Examples

**Binomial Distribution**
```
What is the probability of getting exactly 3 heads in 10 coin flips?

  Distribution : Binomial
  n (trials)   : 10
  k (successes): 3
  p (prob.)    : 0.5

  ✔ P(X = 3) = 0.1172
  Formula: C(10,3) × 0.5³ × 0.5⁷
```

**Normal Distribution**
```
What is the probability that X < 75, given μ=70 and σ=5?

  Distribution : Normal
  x            : 75
  μ (mean)     : 70
  σ (std dev)  : 5

<a name="español"></a>
## 🇪🇸 Español

Calculadora de probabilidades interactiva para terminal, construida con Python. Calcula probabilidades para distribuciones discretas y continuas a través de una interfaz de menú intuitiva — sin necesidad de conocimientos avanzados en estadística.

### ✨ Funcionalidades

- **Distribuciones Discretas**
  - Binomial — probabilidad de *k* éxitos en *n* intentos
  - Poisson — probabilidad de *k* eventos dado una tasa λ
- **Distribuciones Continuas**
  - Normal — cálculo de PDF, CDF y Z-score
  - Exponencial — probabilidad en intervalos de tiempo o distancia
- Menú interactivo en terminal usando `rich`
- Validación de entradas con mensajes de error claros
- Resultados mostrados junto a la fórmula utilizada

### 📸 Demo

> *(Agrega aquí una captura de pantalla o GIF de tu terminal)*
>
> Tip: Usa [asciinema](https://asciinema.org/) o [terminalizer](https://www.terminalizer.com/) para grabar tu terminal.

### 🚀 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/probability-calculator
cd probability-calculator

# (Opcional) Crear un entorno virtual
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### ▶️ Uso

```bash
python main.py
```

Una vez iniciado, navega el menú con las teclas de flecha y presiona Enter para seleccionar una opción.

### 📖 Ejemplos de Uso

**Distribución Binomial**
```
¿Cuál es la probabilidad de obtener exactamente 3 caras en 10 lanzamientos?

  Distribución : Binomial
  n (intentos) : 10
  k (éxitos)   : 3
  p (prob.)    : 0.5

  ✔ P(X = 3) = 0.1172
  Fórmula: C(10,3) × 0.5³ × 0.5⁷
```

**Distribución Normal**
```
¿Cuál es la probabilidad de que X < 75, con μ=70 y σ=5?

  Distribución : Normal
  x            : 75
  μ (media)    : 70
  σ (desv. est): 5

  ✔ P(X < 75) = 0.8413
  Z-score: (75 - 70) / 5 = 1.0
```
  ✔ P(X < 75) = 0.8413
  Z-score: (75 - 70) / 5 = 1.0
```
