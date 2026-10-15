"""
escena_area_vs_integral.py — Parte 3 (José): integral frente a área y cierre.
Grupo 15, MAT1188 (EID Manim 2026).  Tramo del video: 3:30–5:15 (105 s).

Bloques (tiempos relativos al inicio del clip):
    A  0–20 s   Traspaso: el buffer de red, regiones azul/roja, integral = 0 MB
    B 20–45 s   Integral frente a área: reflejo de la región roja, 8/3 MB
    C 45–68 s   Ejemplo simétrico x^3 - 4x: la simetría explica la cancelación
    D 68–82 s   Respuesta a la pregunta central y limitación
    E 82–105 s  Créditos

Todo dato matemático (funciones, intervalos, n, colores, tiempos) viene de
params.py. Aquí solo hay constantes de posición y los textos de los créditos.

Ejecutar SIEMPRE desde la raíz del repositorio, con la raíz en PYTHONPATH:
    PowerShell:  $env:PYTHONPATH="."
                 manim -ql parte3_area_vs_integral\\escena_area_vs_integral.py EscenaAreaVsIntegral
"""

import textwrap
from contextlib import ExitStack
from fractions import Fraction
from pathlib import Path

from manim import *
from params import (MAIN, SYM, N_VALUES, POS_COLOR, NEG_COLOR, CURVE_COLOR,
                    AXIS_COLOR, SUM_COLOR, BG_COLOR, FILL_OPACITY,
                    PIXEL_WIDTH, PIXEL_HEIGHT, FPS, FONT, DURACION_PARTE,
                    CURSO, GRUPO, TEMA, PREGUNTA_CENTRAL, riemann_abs_sum)

config.pixel_width = PIXEL_WIDTH
config.pixel_height = PIXEL_HEIGHT
config.frame_rate = FPS
config.background_color = BG_COLOR

# Fuente común (params.FONT = "DejaVu Sans") incluida en <raiz>/fonts/
RUTA_FUENTES = Path(__file__).resolve().parent.parent / "fonts"
ARCHIVOS_FUENTE = ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf")

# ---------------------------------------------------------------------------
# Constantes propias de esta escena (posiciones y tiempos de bloque)
# ---------------------------------------------------------------------------
FIN_BLOQUE = {                       # segundo del clip en que termina cada bloque
    "A": 20,
    "B": 45,
    "C": 68,
    "D": 82,
    "E": DURACION_PARTE["parte3"],   # 105 s
}

EJES_ANCHO = 6.2
EJES_ALTO = 4.4
EJES_POS = LEFT * 3.2 + DOWN * 0.5   # ejes a la izquierda
PANEL_X = 3.6                        # panel de fórmulas a la derecha
FILAS = (1.9, 0.7, -0.5, -1.5, -2.6)  # alturas (y) de las 5 filas del panel
ANCHO_PANEL = 6.4
TAM_FORMULA = 36

# Créditos (completar lo marcado como PENDIENTE antes de renderizar la versión final)
FUENTE_APUNTE = ("Apunte base: Higueras, N., Oyarzo, F. y Matus, V. (2026). "
                 "Introducción a la integral. Cálculo Intermedio (Blackboard).")
FUENTE_OPENSTAX = ("Strang, G. y Herman, E. (2016). Calculus Volume 1, §5.2 "
                   "The Definite Integral. OpenStax. "
                   "openstax.org/books/calculus-volume-1")
FUENTE_RODRIGO = "PENDIENTE: fuente matemática complementaria de Rodrigo (autor, título, año, enlace)"
FUENTE_MANIM = ("Manim Community Developers. Manim Community v0.22.0, "
                "documentación oficial. docs.manim.community")
FUENTE_DEJAVU = "DejaVu Fonts (licencia libre). dejavu-fonts.github.io"
IA_JOSE = ("Uso de IA (José): Claude (Anthropic), como apoyo para el código de esta "
           "escena y la revisión de cálculos; verificado con params.py y renders.")
IA_BAYRON = "Uso de IA (Bayron): PENDIENTE"
IA_RODRIGO = "Uso de IA (Rodrigo): PENDIENTE"


# ---------------------------------------------------------------------------
# Funciones auxiliares (no dibujan nada por sí solas)
# ---------------------------------------------------------------------------
def fraccion_tex(valor, con_signo=False):
    """Número (float o Fraction) -> LaTeX: 4/3 -> \\tfrac{4}{3}; 0 -> 0."""
    fr = Fraction(valor).limit_denominator(1000)
    signo = "-" if fr < 0 else ("+" if con_signo else "")
    fr = abs(fr)
    if fr.denominator == 1:
        cuerpo = str(fr.numerator)
    else:
        cuerpo = rf"\tfrac{{{fr.numerator}}}{{{fr.denominator}}}"
    return signo + cuerpo


def decimal_tex(x, cifras=3):
    """2.6654 -> '2{,}665' (coma decimal en LaTeX)."""
    return f"{x:.{cifras}f}".replace(".", "{,}")


def cortes(ej):
    """Extremos del intervalo y puntos donde f cambia de signo, ordenados."""
    return sorted(set(ej.ceros) | {ej.a, ej.b})


def valor_tramo(ej, c1, c2):
    """Integral exacta en [c1, c2] con la antiderivada (verificación)."""
    return ej.F(c2) - ej.F(c1)


def nombre_funcion(ej):
    """'r(t)' o 'f(x)', tomado de la etiqueta del ejemplo."""
    return ej.etiqueta_f.split("=")[0]


def integral_tex(ej, absoluto=False):
    """\\int_a^b f(x) dx  (o con |f|), con a y b tomados del ejemplo."""
    a, b = int(ej.a), int(ej.b)
    cuerpo = f"|{nombre_funcion(ej)}|" if absoluto else nombre_funcion(ej)
    return rf"\int_{{{a}}}^{{{b}}} {cuerpo}\,d{ej.var}"


def unidad_tex(ej):
    return rf"\ \text{{{ej.unidad_acum}}}" if ej.unidad_acum else ""


def texto(contenido, tam=30, color=WHITE, ancho=None):
    if ancho:
        contenido = textwrap.fill(contenido, ancho)
    return Text(contenido, font=FONT, font_size=tam, color=color)


def formula(tex, y_fila, color=WHITE, tam=TAM_FORMULA):
    m = MathTex(tex, font_size=tam, color=color)
    if m.width > ANCHO_PANEL:
        m.scale_to_fit_width(ANCHO_PANEL)
    return m.move_to(RIGHT * PANEL_X + UP * y_fila)


def construir_grafica(ej, y_min, y_max):
    """Ejes, curva, regiones coloreadas por signo y sus etiquetas de valor."""
    ejes = Axes(
        x_range=[ej.a, ej.b, 1],
        y_range=[y_min, y_max, 1],
        x_length=EJES_ANCHO,
        y_length=EJES_ALTO,
        tips=False,
        axis_config={"color": AXIS_COLOR, "include_numbers": True,
                     "font_size": 22},
    ).shift(EJES_POS)
    curva = ejes.plot(ej.f, x_range=[ej.a, ej.b], color=CURVE_COLOR)

    x_tex = ej.var + (rf"\ (\text{{{ej.unidad_var}}})" if ej.unidad_var else "")
    y_tex = nombre_funcion(ej) + (rf"\ (\text{{{ej.unidad_f}}})" if ej.unidad_f else "")
    nombres = ejes.get_axis_labels(
        x_label=MathTex(x_tex, font_size=26, color=AXIS_COLOR),
        y_label=MathTex(y_tex, font_size=26, color=AXIS_COLOR),
    )

    positivas, negativas = VGroup(), VGroup()
    et_pos, et_neg = VGroup(), VGroup()
    puntos = cortes(ej)
    for c1, c2 in zip(puntos, puntos[1:]):
        medio = (c1 + c2) / 2
        es_pos = ej.f(medio) > 0
        region = ejes.get_area(
            curva, x_range=(c1, c2),
            color=POS_COLOR if es_pos else NEG_COLOR, opacity=FILL_OPACITY,
        )
        etiqueta = MathTex(
            fraccion_tex(valor_tramo(ej, c1, c2), con_signo=True) + unidad_tex(ej),
            font_size=28, color=WHITE,
        ).move_to(ejes.c2p(medio, ej.f(medio) * 0.4))
        (positivas if es_pos else negativas).add(region)
        (et_pos if es_pos else et_neg).add(etiqueta)

    return {"ejes": ejes, "curva": curva, "nombres": nombres,
            "pos": positivas, "neg": negativas,
            "et_pos": et_pos, "et_neg": et_neg}


# ---------------------------------------------------------------------------
# Escena
# ---------------------------------------------------------------------------
class EscenaAreaVsIntegral(Scene):

    def construct(self):
        with ExitStack() as pila:
            for nombre in ARCHIVOS_FUENTE:
                ruta = RUTA_FUENTES / nombre
                if ruta.exists():
                    pila.enter_context(register_font(str(ruta)))
                else:
                    print(f"[AVISO] no se encontro {ruta}")
            self.animar()

    # -- control de tiempo: cada animación declara su duración y se lleva la cuenta
    def jugar(self, *animaciones, run_time=1.0):
        self.play(*animaciones, run_time=run_time)
        self.reloj += run_time

    def hasta(self, segundo, bloque):
        resto = segundo - self.reloj
        if resto > 0.01:
            self.wait(resto)
            self.reloj = segundo
        else:
            print(f"[AVISO] el bloque {bloque} termina en {self.reloj:.1f} s "
                  f"(objetivo {segundo} s): recortar animaciones")

    def limpiar(self, conservar=()):
        salientes = [FadeOut(m) for m in self.mobjects if m not in conservar]
        if salientes:
            self.jugar(*salientes, run_time=1.0)

    def animar(self):
        self.reloj = 0.0
        voz = texto("José", tam=26, color=AXIS_COLOR).to_corner(UL)

        self.bloque_a(voz)
        self.bloque_b()
        self.bloque_c(voz)
        self.bloque_d(voz)
        self.bloque_e()

    # ------------------------------------------------------------------ A
    def bloque_a(self, voz):
        self.g = construir_grafica(MAIN, -2, 4)
        g = self.g
        self.encabezado = texto("Retomamos el buffer de red", tam=34).to_edge(UP)

        self.jugar(FadeIn(voz), Write(self.encabezado), run_time=1.5)
        self.jugar(Create(g["ejes"]), Write(g["nombres"]), run_time=2.0)
        self.jugar(Create(g["curva"]), run_time=2.0)
        self.jugar(FadeIn(g["pos"]), Write(g["et_pos"]), run_time=1.5)
        self.jugar(FadeIn(g["neg"]), Write(g["et_neg"]), run_time=1.5)

        self.f_integral = formula(
            integral_tex(MAIN) + "=" + fraccion_tex(MAIN.integral_exacta)
            + unidad_tex(MAIN), FILAS[0], color=SUM_COLOR)
        self.pregunta = texto("¿Significa que no pasó nada?", tam=32).move_to(
            RIGHT * PANEL_X + UP * FILAS[2])
        self.jugar(Write(self.f_integral), run_time=2.0)
        self.jugar(FadeIn(self.pregunta), run_time=1.5)
        self.hasta(FIN_BLOQUE["A"], "A")

    # ------------------------------------------------------------------ B
    def bloque_b(self):
        g = self.g
        encabezado_b = texto("Integral frente a área", tam=34).to_edge(UP)
        self.jugar(FadeOut(self.pregunta),
                   ReplacementTransform(self.encabezado, encabezado_b),
                   run_time=1.0)

        # área = ∫|f| = suma de los valores absolutos de cada tramo
        tramos = [abs(valor_tramo(MAIN, c1, c2))
                  for c1, c2 in zip(cortes(MAIN), cortes(MAIN)[1:])]
        f_area = formula(
            integral_tex(MAIN, absoluto=True) + "=" + fraccion_tex(MAIN.area_exacta)
            + unidad_tex(MAIN), FILAS[1], color=SUM_COLOR)
        self.jugar(Write(f_area), run_time=2.5)

        # reflejo de la región roja sobre el eje: lo negativo pasa a contar positivo
        origen = g["ejes"].c2p(0, 0)
        copia = g["neg"].copy()
        reflejo = (g["neg"].copy().flip(RIGHT, about_point=origen)
                   .set_fill(SUM_COLOR, opacity=FILL_OPACITY))
        self.jugar(Transform(copia, reflejo), run_time=3.0)

        f_suma = formula(
            "+".join(fraccion_tex(t) for t in tramos) + "="
            + fraccion_tex(MAIN.area_exacta) + unidad_tex(MAIN), FILAS[2])
        self.jugar(Write(f_suma), run_time=2.5)

        trafico = texto("= tráfico total que se movió", tam=28, color=SUM_COLOR).move_to(
            RIGHT * PANEL_X + UP * FILAS[3])
        self.jugar(FadeIn(trafico), run_time=1.5)

        n = N_VALUES[-1]
        aprox = riemann_abs_sum(MAIN, n)
        f_riemann = formula(
            rf"\sum_{{i=1}}^{{{n}}} |r(t_i^*)|\,\Delta t \approx "
            + decimal_tex(aprox) + unidad_tex(MAIN), FILAS[4], tam=30)
        self.jugar(Write(f_riemann), run_time=2.5)
        self.encabezado = encabezado_b
        self.hasta(FIN_BLOQUE["B"], "B")

    # ------------------------------------------------------------------ C
    def bloque_c(self, voz):
        self.limpiar(conservar=(voz,))
        encabezado_c = texto("Otro ejemplo: una función impar", tam=34).to_edge(UP)
        g = construir_grafica(SYM, -4, 4)

        self.jugar(Write(encabezado_c), run_time=1.0)
        self.jugar(Create(g["ejes"]), Write(g["nombres"]), run_time=1.5)
        self.jugar(Create(g["curva"]), run_time=1.5)
        self.jugar(FadeIn(g["pos"]), Write(g["et_pos"]), run_time=1.5)
        self.jugar(FadeIn(g["neg"]), Write(g["et_neg"]), run_time=1.5)

        f_def = formula(SYM.etiqueta_f, FILAS[0])
        f_impar = formula(r"f(-x)=-f(x)\ \Rightarrow\ \text{impar}", FILAS[1])
        self.jugar(Write(f_def), Write(f_impar), run_time=2.0)

        # simetría: la región azul, girada 180° sobre el origen, cae sobre la roja
        origen = g["ejes"].c2p(0, 0)
        punto = Dot(origen, color=AXIS_COLOR)
        sombra = (g["pos"].copy().set_fill(AXIS_COLOR, opacity=0.5)
                  .set_stroke(width=0))
        self.jugar(FadeIn(punto), FadeIn(sombra), run_time=0.5)
        self.jugar(Rotate(sombra, angle=PI, about_point=origen), run_time=3.0)
        self.jugar(FadeOut(sombra), FadeOut(punto), run_time=0.5)

        f_int = formula(integral_tex(SYM) + "=" + fraccion_tex(SYM.integral_exacta),
                        FILAS[2], color=SUM_COLOR)
        f_area = formula(integral_tex(SYM, absoluto=True) + "="
                         + fraccion_tex(SYM.area_exacta), FILAS[3], color=SUM_COLOR)
        self.jugar(Write(f_int), run_time=2.0)
        self.jugar(Write(f_area), run_time=2.0)

        n = N_VALUES[-1]
        f_riemann = formula(
            rf"\sum_{{i=1}}^{{{n}}} |f(x_i^*)|\,\Delta x \approx "
            + decimal_tex(riemann_abs_sum(SYM, n)), FILAS[4], tam=30)
        self.jugar(Write(f_riemann), run_time=2.0)
        self.hasta(FIN_BLOQUE["C"], "C")

    # ------------------------------------------------------------------ D
    def bloque_d(self, voz):
        self.limpiar(conservar=(voz,))
        encabezado_d = texto("Respuesta a la pregunta central", tam=34).to_edge(UP)
        pregunta = texto(PREGUNTA_CENTRAL, tam=32, color=CURVE_COLOR, ancho=48
                         ).move_to(UP * 1.9)
        respuesta = texto(
            "Porque la integral es el límite de sumas con signo:\n"
            "los aportes positivos y los negativos se compensan.",
            tam=30).move_to(UP * 0.2)
        limite = MathTex(
            r"\int_a^b f(x)\,dx=\lim_{n\to\infty}\sum_{i=1}^{n} f(x_i^*)\,\Delta x",
            font_size=40, color=SUM_COLOR).move_to(DOWN * 1.2)
        limitacion = texto(
            "Pero integral cero no significa que f sea nula\n"
            "ni que el área sea cero.", tam=28, color=NEG_COLOR).move_to(DOWN * 2.8)

        self.jugar(Write(encabezado_d), run_time=1.0)
        self.jugar(Write(pregunta), run_time=3.0)
        self.jugar(FadeIn(respuesta), run_time=2.0)
        self.jugar(Write(limite), run_time=2.5)
        self.jugar(FadeIn(limitacion), run_time=2.0)
        self.hasta(FIN_BLOQUE["D"], "D")

    # ------------------------------------------------------------------ E
    def bloque_e(self):
        self.limpiar()
        titulo = texto("Créditos", tam=36).to_edge(UP)
        lineas = [
            f"{CURSO} · Grupo {GRUPO}",
            f"Tema: {TEMA}",
            FUENTE_APUNTE, FUENTE_OPENSTAX, FUENTE_RODRIGO,
            FUENTE_MANIM, FUENTE_DEJAVU,
            IA_JOSE, IA_BAYRON, IA_RODRIGO,
        ]
        items = VGroup(*[texto(l, tam=20, ancho=95) for l in lineas])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        if items.width > 12.8:
            items.scale_to_fit_width(12.8)
        if items.height > 6.0:
            items.scale_to_fit_height(6.0)
        items.next_to(titulo, DOWN, buff=0.35)

        self.jugar(Write(titulo), run_time=1.0)
        self.jugar(LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.35),
                   run_time=6.0)
        self.hasta(FIN_BLOQUE["E"], "E")