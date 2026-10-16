"""
escena_ejemplo.py — Rodrigo (Grupo 15, MAT1188)
Parte 2 del video (~105 s): ejemplo principal
    r(t) = t^2 - 4t + 3  [MB/s]  en t in [0, 3] s

Renderizar desde la raíz del repositorio:
    PowerShell:  $env:PYTHONPATH="."
                 py -m manim -qh parte2_ejemplo/escena_ejemplo.py EscenaEjemplo
Parámetros de params.py usados:
    MAIN, N_VALUES, delta_x, sample_points, riemann_terms, riemann_sum,
    POS_COLOR, NEG_COLOR, SUM_COLOR, CURVE_COLOR, AXIS_COLOR, BG_COLOR,
    FILL_OPACITY, FONT, PIXEL_WIDTH, PIXEL_HEIGHT, FPS
"""

from contextlib import ExitStack
from pathlib import Path

from manim import *
from params import (MAIN, N_VALUES, POS_COLOR, NEG_COLOR, SUM_COLOR,
                    CURVE_COLOR, AXIS_COLOR, BG_COLOR, FILL_OPACITY, FONT,
                    PIXEL_WIDTH, PIXEL_HEIGHT, FPS,
                    delta_x, sample_points, riemann_terms, riemann_sum)

config.pixel_width = PIXEL_WIDTH
config.pixel_height = PIXEL_HEIGHT
config.frame_rate = FPS
config.background_color = BG_COLOR

# Fuente comun (params.FONT = "DejaVu Sans") incluida en <raiz>/fonts/
RUTA_FUENTES = Path(__file__).resolve().parent.parent / "fonts"
ARCHIVOS_FUENTE = ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf")

# --- Constantes propias de esta escena (posiciones y tamaños) ---------------
AXES_SHIFT = LEFT * 3.3 + DOWN * 0.4
PANEL_X = 2.5                 # x del borde izquierdo del panel derecho
TABLE_COLS = (0.0, 0.9, 2.7)  # desplazamientos de las columnas n, dt, S_n
TABLE_TOP = 0.15              # y del encabezado de la tabla
ROW_STEP = 0.55               # separación vertical entre filas
SUMA_Y = 1.25                 # y central del bloque con la sumatoria
LIM_Y = -2.9                  # y de "S_n -> 0 MB"
ESPERA_N = (2.5, 2, 2, 2.5)  # pausa (s) tras la fila de cada n
NOMBRE_VOZ = "Rodrigo Gutiérrez" 


class EscenaEjemplo(Scene):
    def construct(self):
        with ExitStack() as pila:
            for nombre in ARCHIVOS_FUENTE:
                ruta = RUTA_FUENTES / nombre
                if ruta.exists():
                    pila.enter_context(register_font(str(ruta)))
                else:
                    print(f"[AVISO] no se encontro {ruta}")
            self.animar()

    def animar(self):
        c = MAIN.ceros[0]     # t = 1: donde r cambia de signo
        # Voz identificada en la esquina superior izquierda (visible todo el clip)
        voz = Text(NOMBRE_VOZ, font=FONT, font_size=18, color=AXIS_COLOR)
        voz.to_corner(UL, buff=0.3)

        # ------------------------------------------------------------------
        # 1) Apertura (0-22 s): retoma la pregunta con que cierra la Parte 1
        # ------------------------------------------------------------------
        titulo = Text("Ejemplo principal: buffer de red", font=FONT,
                      font_size=40).to_edge(UP)
        formula = MathTex(MAIN.etiqueta_f, r"\ \text{MB/s}",
                          font_size=48).next_to(titulo, DOWN, buff=0.4)
        contexto = Text("r(t) = llegada − salida", font=FONT,
                        font_size=30, color=AXIS_COLOR)
        # pregunta con que cierra la Parte 1 (se retoma tal cual)
        pregunta = Text("¿Cuánto vale la integral en nuestro buffer?",
                        font=FONT, font_size=30, color=SUM_COLOR)
        pregunta.next_to(titulo, DOWN, buff=0.35)
        formula.next_to(pregunta, DOWN, buff=0.4)
        contexto.next_to(formula, DOWN, buff=0.35)
        # por qué la integral: acumula la tasa en el tiempo
        integral = MathTex(rf"\int_{int(MAIN.a)}^{int(MAIN.b)} r(t)\,dt",
                           font_size=48)
        acumula = Text("acumula la tasa: (MB/s)·s = MB", font=FONT,
                       font_size=26, color=AXIS_COLOR)
        acumula_g = VGroup(integral, acumula).arrange(DOWN, buff=0.25)
        acumula_g.next_to(contexto, DOWN, buff=0.6)

        self.play(Write(titulo), FadeIn(voz), run_time=1.5)
        self.play(Write(pregunta), run_time=2)
        self.wait(3)
        self.play(Write(formula), run_time=2)
        self.play(FadeIn(contexto, shift=UP * 0.2))
        self.wait(6)
        self.play(Write(acumula_g), run_time=1.5)
        self.wait(3.5)
        self.play(FadeOut(pregunta, contexto, acumula_g),
                  formula.animate.scale(0.7).next_to(
                      titulo, DOWN, buff=0.2), run_time=1.5)

        # ------------------------------------------------------------------
        # 2) Ejes y gráfica con sus datos (22-45 s)
        # ------------------------------------------------------------------
        axes = Axes(
            x_range=[0, 3.5, 1], y_range=[-1.5, 3.5, 1],
            x_length=7.4, y_length=4.4,
            axis_config={"color": AXIS_COLOR, "include_tip": True},
        ).shift(AXES_SHIFT)
        axes.x_axis.add_numbers([1, 2, 3], font_size=24)
        axes.y_axis.add_numbers([-1, 1, 2, 3], font_size=24)
        x_lab = Text(f"t ({MAIN.unidad_var})", font=FONT, font_size=24)
        x_lab.next_to(axes.x_axis.get_end(), DOWN, buff=0.25)
        y_lab = Text(f"r(t) ({MAIN.unidad_f})", font=FONT, font_size=24)
        y_lab.next_to(axes.y_axis.get_end(), RIGHT, buff=0.2)
        curva = axes.plot(MAIN.f, x_range=[MAIN.a, MAIN.b],
                          color=CURVE_COLOR)
        self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab), run_time=3)
        self.play(Create(curva), run_time=3)
        self.wait(0.5)

        # Datos que explican la forma de la gráfica (todos salen de MAIN):
        #  - r(0): donde corta el eje vertical
        #  - los ceros de r: donde corta el eje horizontal (t = 1 y t = 3)
        #  - el vértice: punto medio de los ceros (simetría de la parábola)
        t_v = sum(MAIN.ceros) / len(MAIN.ceros)
        dot_y = Dot(axes.c2p(MAIN.a, MAIN.f(MAIN.a)), color=CURVE_COLOR)
        lbl_y = Text(f"r(0) = {MAIN.f(MAIN.a):.0f}", font=FONT, font_size=22,
                     color=AXIS_COLOR).next_to(dot_y, RIGHT, buff=0.15)
        dots_z = VGroup(*[Dot(axes.c2p(z, 0), color=CURVE_COLOR)
                          for z in MAIN.ceros])
        lbls_z = VGroup(*[
            Text(f"t = {z:.0f}", font=FONT, font_size=22,
                 color=AXIS_COLOR).next_to(axes.c2p(z, 0), UR, buff=0.1)
            for z in MAIN.ceros])
        factor = MathTex(r"r(t)=(t-1)(t-3)", font_size=40)
        factor.move_to(RIGHT * (PANEL_X + factor.width / 2) + UP * 0.9)
        dot_v = Dot(axes.c2p(t_v, MAIN.f(t_v)), color=CURVE_COLOR)
        lbl_v = Text(f"mínimo: ({t_v:.0f}, {MAIN.f(t_v):.0f})".replace(
            "-", "−"), font=FONT, font_size=22, color=AXIS_COLOR)
        lbl_v.next_to(dot_v, DOWN, buff=0.15)
        anotaciones = VGroup(dot_y, lbl_y, dots_z, lbls_z, factor,
                             dot_v, lbl_v)

        self.play(FadeIn(dot_y), FadeIn(lbl_y), run_time=1)
        self.wait(3)
        self.play(FadeIn(dots_z), FadeIn(lbls_z), FadeIn(factor),
                  run_time=1.5)
        self.wait(4.5)
        self.play(FadeIn(dot_v), FadeIn(lbl_v), run_time=1)
        self.wait(5.5)

        # ------------------------------------------------------------------
        # 3) Dos tramos con signo (45-71,5 s): [0,1] gana, [1,3] pierde
        # ------------------------------------------------------------------
        area_pos = axes.get_area(curva, x_range=(MAIN.a, c),
                                 color=POS_COLOR, opacity=FILL_OPACITY)
        area_neg = axes.get_area(curva, x_range=(c, MAIN.b),
                                 color=NEG_COLOR, opacity=FILL_OPACITY)
        lbl_pos = Text("r ≥ 0: el buffer gana", font=FONT, font_size=22,
                       color=POS_COLOR).move_to(axes.c2p(0.55, 2.7))
        lbl_neg = Text("r ≤ 0: el buffer pierde", font=FONT, font_size=22,
                       color=NEG_COLOR).move_to(axes.c2p(2.0, -1.35))

        Fdef = MathTex(r"F(t)=\tfrac{t^3}{3}-2t^2+3t", font_size=34)
        calc_pos = MathTex(r"F(1)-F(0)=\tfrac{4}{3}\ \text{MB}",
                           font_size=34, color=POS_COLOR)
        calc_neg = MathTex(r"F(3)-F(1)=-\tfrac{4}{3}\ \text{MB}",
                           font_size=34, color=NEG_COLOR)
        total = MathTex(r"\tfrac{4}{3}+\left(-\tfrac{4}{3}\right)=0\ \text{MB}",
                        font_size=38, color=SUM_COLOR)
        panel = VGroup(Fdef, calc_pos, calc_neg, total).arrange(
            DOWN, aligned_edge=LEFT, buff=0.45)
        panel.move_to(RIGHT * (PANEL_X + panel.width / 2) + UP * 0.6)

        self.play(FadeOut(anotaciones), FadeIn(area_pos), FadeIn(lbl_pos),
                  run_time=2)
        self.wait(1.5)
        self.play(FadeIn(area_neg), FadeIn(lbl_neg), run_time=2)
        self.wait(1.5)
        self.play(Write(Fdef), run_time=2)
        self.wait(4)
        self.play(Write(calc_pos), run_time=2)
        self.wait(2.5)
        self.play(Write(calc_neg), run_time=2)
        self.wait(2.5)
        self.play(Write(total), run_time=2)
        self.play(Indicate(total, color=SUM_COLOR), run_time=1.5)
        self.wait(1)

        # ------------------------------------------------------------------
        # 4) Pasar a sumas de Riemann (71,5-99,5 s)
        # ------------------------------------------------------------------
        self.play(FadeOut(area_pos, area_neg, lbl_pos, lbl_neg, panel),
                  run_time=1.5)

        def rectangulos(n):
            dx = delta_x(MAIN.a, MAIN.b, n)
            grupo = VGroup()
            for x, aporte in zip(sample_points(MAIN.a, MAIN.b, n),
                                 riemann_terms(MAIN, n)):
                p0 = axes.c2p(x - dx / 2, 0)
                p1 = axes.c2p(x + dx / 2, MAIN.f(x))
                rect = Rectangle(
                    width=abs(p1[0] - p0[0]),
                    height=max(abs(p1[1] - p0[1]), 1e-4),
                    stroke_width=1.2, stroke_color=WHITE,
                    fill_color=POS_COLOR if aporte > 0 else NEG_COLOR,
                    fill_opacity=FILL_OPACITY,
                )
                rect.move_to((p0 + p1) / 2)
                grupo.add(rect)
            return grupo

        suma_def = MathTex(r"S_n=\sum_{i=1}^{n} r(t_i^*)\,\Delta t",
                           font_size=36)
        dt_def = MathTex(r"\Delta t=\frac{3-0}{n}", r",\quad t_i^*=\text{punto medio}",
                         font_size=30)
        cabecera_txt = VGroup(suma_def, dt_def).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3)
        cabecera_txt.move_to(RIGHT * (PANEL_X + cabecera_txt.width / 2)
                             + UP * SUMA_Y)
        self.play(Write(suma_def), run_time=2)
        self.play(Write(dt_def), run_time=2)

        # Encabezado de la tabla
        heads = VGroup(*[
            Text(t, font=FONT, font_size=24, color=AXIS_COLOR)
            for t in ("n", "Δt (s)", "S_n (MB)")
        ])
        for h, dxoff in zip(heads, TABLE_COLS):
            h.move_to(UP * TABLE_TOP)
            h.align_to(RIGHT * (PANEL_X + dxoff), LEFT)
        self.play(FadeIn(heads))

        filas = []
        rects_actuales = None
        for k, n in enumerate(N_VALUES):
            nuevos = rectangulos(n)
            if rects_actuales is None:
                self.play(Create(nuevos), run_time=2.5)
            else:
                self.play(ReplacementTransform(rects_actuales, nuevos),
                          run_time=2)
            rects_actuales = nuevos

            dx = delta_x(MAIN.a, MAIN.b, n)
            Sn = riemann_sum(MAIN, n)
            fila = VGroup(
                Text(str(n), font=FONT, font_size=24),
                Text(f"{dx:.4f}", font=FONT, font_size=24),
                # signo con "−" (menos tipográfico) para que se lea como
                # número negativo y no como una resta
                Text(f"{Sn:+.5f}".replace("-", "−"), font=FONT,
                     font_size=24, color=SUM_COLOR),
            )
            y = TABLE_TOP - ROW_STEP * (k + 1)
            for celda, dxoff in zip(fila, TABLE_COLS):
                celda.move_to(RIGHT * (PANEL_X + dxoff) + UP * y)
                celda.align_to(RIGHT * (PANEL_X + dxoff), LEFT)
            filas.append(fila)
            self.play(FadeIn(fila, shift=LEFT * 0.2), run_time=1)
            self.wait(ESPERA_N[min(k, len(ESPERA_N) - 1)])

        # ------------------------------------------------------------------
        # 5) Respuesta e interpretación (99,5-105 s)
        # ------------------------------------------------------------------
        caja = SurroundingRectangle(filas[-1][2], color=SUM_COLOR, buff=0.12)
        lim = MathTex(r"S_n\to 0\ \text{MB}", font_size=40, color=SUM_COLOR)
        lim.move_to(RIGHT * (PANEL_X + 1.6) + UP * LIM_Y)
        conclusion = Text("El buffer termina igual que empezó",
                          font=FONT, font_size=28, color=SUM_COLOR)
        conclusion.to_edge(DOWN, buff=0.5)
        self.play(Create(caja), Write(lim), run_time=2)
        self.play(FadeIn(conclusion, shift=UP * 0.2))
        self.wait(2.5)