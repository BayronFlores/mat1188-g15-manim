"""
params.py — Contrato común del Grupo 15 (MAT1188, EID Manim 2026)

Tema: Integral nula con regiones no nulas.
Ejemplo principal: tasa neta de un buffer de red, r(t) = t^2 - 4t + 3 (MB/s),
en t in [0, 3] s.  Ejemplo complementario: f(x) = x^3 - 4x en [-2, 2].
Pregunta central: ¿Cómo puede una integral valer cero aunque existan
regiones con área positiva?

REGLAS
- Este archivo se fija entre los tres integrantes y NO se modifica sin
  acuerdo de todos. Las tres escenas lo importan: así funciones, intervalos,
  colores y valores de n son idénticos en todo el video.
- No depende de Manim: se puede importar y probar desde cualquier lugar.
  Para verificar los datos matemáticos: `python params.py`
- Los colores son strings hex, que Manim acepta directamente.

USO EN UNA ESCENA
    from params import MAIN, SYM, N_VALUES, POS_COLOR, NEG_COLOR
    from params import riemann_sum, sample_points, partition
"""

from fractions import Fraction

# ---------------------------------------------------------------------------
# 1. Identificación (para README, ficha y créditos)
# ---------------------------------------------------------------------------
CURSO = "MAT1188 - Cálculo Intermedio"
GRUPO = 15
TEMA = "Integral nula con regiones no nulas"
PREGUNTA_CENTRAL = (
    "¿Cómo puede una integral valer cero aunque existan "
    "regiones con área positiva?"
)

# ---------------------------------------------------------------------------
# 2. Ejemplos matemáticos
#    Cada ejemplo agrupa: función f, antiderivada F (solo para verificar),
#    intervalo [a, b] y los valores exactos esperados.
# ---------------------------------------------------------------------------

class Ejemplo:
    def __init__(self, nombre, f, F, a, b, integral_exacta, area_exacta,
                 ceros, etiqueta_f, var="x", unidad_f="", unidad_var="",
                 unidad_acum="", contexto=""):
        self.nombre = nombre
        self.f = f                          # función del ejemplo
        self.F = F                          # antiderivada (verificación)
        self.a = a                          # extremo izquierdo
        self.b = b                          # extremo derecho
        self.integral_exacta = integral_exacta  # ∫ f  (con signo)
        self.area_exacta = area_exacta          # ∫ |f| (área geométrica)
        self.ceros = ceros                  # puntos donde f cambia de signo
        self.etiqueta_f = etiqueta_f        # texto LaTeX para MathTex
        self.var = var                      # nombre de la variable (x o t)
        self.unidad_f = unidad_f            # unidad de f (p. ej. "MB/s")
        self.unidad_var = unidad_var        # unidad de la variable ("s")
        self.unidad_acum = unidad_acum      # unidad de la integral ("MB")
        self.contexto = contexto            # lectura del ejemplo

# Ejemplo principal (NO simétrico, con contexto):
#   r(t) = t^2 - 4t + 3  [MB/s]  en t in [0, 3] s
#   Tasa neta de un buffer de red = llegada - salida.
#   F(t) = t^3/3 - 2t^2 + 3t
#   [0, 1] -> r >= 0 -> el buffer gana   +4/3 MB
#   [1, 3] -> r <= 0 -> el buffer pierde -4/3 MB
#   ∫ = 0 MB (el buffer termina igual) y área geométrica = 8/3 MB
#   (tráfico total movido). Unidades: (MB/s)·s = MB.
MAIN = Ejemplo(
    nombre="principal",
    f=lambda t: t**2 - 4 * t + 3,
    F=lambda t: t**3 / 3 - 2 * t**2 + 3 * t,
    a=0.0,
    b=3.0,
    integral_exacta=Fraction(0),
    area_exacta=Fraction(8, 3),
    ceros=(1.0, 3.0),
    etiqueta_f=r"r(t)=t^2-4t+3",
    var="t",
    unidad_f="MB/s",
    unidad_var="s",
    unidad_acum="MB",
    contexto="Tasa neta de un buffer de red: llegada menos salida",
)

# Ejemplo complementario (simétrico, función impar): f(x) = x^3 - 4x en [-2, 2]
#   F(x) = x^4/4 - 2x^2
#   ∫ = 0  y  área geométrica = 8
SYM = Ejemplo(
    nombre="simétrico",
    f=lambda x: x**3 - 4 * x,
    F=lambda x: x**4 / 4 - 2 * x**2,
    a=-2.0,
    b=2.0,
    integral_exacta=Fraction(0),
    area_exacta=Fraction(8),
    ceros=(-2.0, 0.0, 2.0),
    etiqueta_f=r"f(x)=x^3-4x",
)

EJEMPLOS = (MAIN, SYM)

# ---------------------------------------------------------------------------
# 3. Sumas de Riemann
# ---------------------------------------------------------------------------
N_VALUES = (4, 8, 16, 32)       # refinamientos que se muestran en el video

# Criterio ÚNICO de punto muestra para todo el video:
#   "izquierdo" | "derecho" | "medio"
SAMPLE_MODE = "medio"


def delta_x(a, b, n):
    """Ancho de cada subintervalo: Δx = (b - a) / n."""
    return (b - a) / n


def partition(a, b, n):
    """Puntos de la partición: x_i = a + i·Δx, i = 0..n."""
    dx = delta_x(a, b, n)
    return [a + i * dx for i in range(n + 1)]


def sample_points(a, b, n, mode=None):
    """Puntos muestra x_i* (i = 1..n) según SAMPLE_MODE (o `mode`)."""
    mode = mode or SAMPLE_MODE
    xs = partition(a, b, n)
    if mode == "izquierdo":
        return xs[:-1]
    if mode == "derecho":
        return xs[1:]
    if mode == "medio":
        return [(xs[i] + xs[i + 1]) / 2 for i in range(n)]
    raise ValueError(f"mode inválido: {mode}")


def riemann_terms(ej, n, mode=None):
    """Lista de aportes f(x_i*)·Δx (con signo), uno por subintervalo."""
    dx = delta_x(ej.a, ej.b, n)
    return [ej.f(x) * dx for x in sample_points(ej.a, ej.b, n, mode)]


def riemann_sum(ej, n, mode=None):
    """Suma de Riemann S_n = Σ f(x_i*)·Δx  (con signo)."""
    return sum(riemann_terms(ej, n, mode))


def riemann_abs_sum(ej, n, mode=None):
    """Σ |f(x_i*)|·Δx: aproxima el ÁREA GEOMÉTRICA (sin signo)."""
    return sum(abs(t) for t in riemann_terms(ej, n, mode))


# ---------------------------------------------------------------------------
# 4. Estilo visual (idéntico en las tres escenas)
# ---------------------------------------------------------------------------
POS_COLOR = "#3B82F6"      # aportes positivos (sobre el eje)  -> azul
NEG_COLOR = "#EF4444"      # aportes negativos (bajo el eje)   -> rojo
CURVE_COLOR = "#FACC15"    # gráfica de f
AXIS_COLOR = "#E5E7EB"
SUM_COLOR = "#34D399"      # total de la suma / resultado
BG_COLOR = "#0F172A"       # fondo oscuro
FILL_OPACITY = 0.6

FONT = "DejaVu Sans"       # fuente de Text(); fórmulas con MathTex
PIXEL_WIDTH = 1920
PIXEL_HEIGHT = 1080
FPS = 30

# ---------------------------------------------------------------------------
# 5. Tiempos del video (segundos)  — total objetivo ≈ 5:15 (rango 4:00-6:00)
# ---------------------------------------------------------------------------
DURACION_PARTE = {
    "parte1": 105,   # Presentación + teoría
    "parte2": 105,   # Ejemplo principal r(t) = t^2 - 4t + 3
    "parte3": 105,   # Integral vs. área, ejemplo simétrico, respuesta, créditos
}
DURACION_TOTAL = sum(DURACION_PARTE.values())

# Nombres de los clips que cada persona entrega (MP4 con su propio audio)
CLIPS = ("parte1.mp4", "parte2.mp4", "parte3.mp4")

# ---------------------------------------------------------------------------
# 6. Autoverificación:  python params.py
# ---------------------------------------------------------------------------
def verificar():
    assert 240 <= DURACION_TOTAL <= 360, "El video debe durar entre 4 y 6 min"

    for ej in EJEMPLOS:
        # ∫ con signo vía antiderivada (Teorema Fundamental, Parte II)
        integral = ej.F(ej.b) - ej.F(ej.a)
        assert abs(integral - float(ej.integral_exacta)) < 1e-12, ej.nombre

        # área geométrica = suma de |∫| en cada tramo entre ceros
        cortes = sorted(set(ej.ceros) | {ej.a, ej.b})
        area = sum(abs(ej.F(c2) - ej.F(c1))
                   for c1, c2 in zip(cortes, cortes[1:]))
        assert abs(area - float(ej.area_exacta)) < 1e-12, ej.nombre

    print(f"Grupo {GRUPO} — {TEMA}")
    print(f"Criterio de punto muestra: {SAMPLE_MODE}")
    print(f"Duración total planificada: {DURACION_TOTAL // 60}:"
          f"{DURACION_TOTAL % 60:02d}\n")

    for ej in EJEMPLOS:
        print(f"[{ej.nombre}] {ej.etiqueta_f}  en [{ej.a}, {ej.b}]")
        u = f" {ej.unidad_acum}" if ej.unidad_acum else ""
        print(f"  ∫ exacta = {ej.integral_exacta}{u}   "
              f"área exacta = {ej.area_exacta}{u}")
        print(f"  {'n':>4} {'Δx':>10} {'S_n (con signo)':>18} "
              f"{'Σ|f|Δx (área)':>16}")
        for n in N_VALUES:
            print(f"  {n:>4} {delta_x(ej.a, ej.b, n):>10.5f} "
                  f"{riemann_sum(ej, n):>18.8f} "
                  f"{riemann_abs_sum(ej, n):>16.8f}")
        print()
    print("OK: parámetros consistentes.")

if __name__ == "__main__":
    verificar()