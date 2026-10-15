"""
escena_teoria.py — Parte 1 del video (Bayron): presentación y teoría.
MAT1188 Cálculo Intermedio · EID Manim 2026 · Grupo 15
Tema: Integral nula con regiones no nulas.

Contenido (0:00 – 1:45, 105 s):
    S1  0:00-0:14  Presentación: grupo, tema y pregunta central.
    S2  0:14-0:36  Situación: tasa neta de un buffer de red r(t) = t^2 - 4t + 3.
    S3  0:36-0:54  Partición: Δt = (b - a)/n y punto muestra (punto medio).
    S4  0:54-1:14  Rectángulos con altura positiva y negativa: aportes con signo.
    S5  1:14-1:36  Suma de Riemann, límite e integral definida; símbolos y
                   condición de continuidad.
    S6  1:36-1:45  Integral (con signo) vs. área geométrica; pase a Rodrigo.

Todo dato matemático (función, intervalo, n, punto muestra, colores, textos)
se importa desde params.py. Aquí solo se definen constantes de maquetación.

"""

import textwrap
from contextlib import ExitStack
from pathlib import Path

from manim import *

from params import (
    MAIN, N_VALUES,
    POS_COLOR, NEG_COLOR, CURVE_COLOR, AXIS_COLOR, SUM_COLOR, BG_COLOR,
    FILL_OPACITY, PIXEL_WIDTH, PIXEL_HEIGHT, FPS, FONT,
    CURSO, GRUPO, TEMA, PREGUNTA_CENTRAL, DURACION_PARTE,
    delta_x, partition, sample_points, riemann_terms, riemann_sum,
)

config.pixel_width = PIXEL_WIDTH
config.pixel_height = PIXEL_HEIGHT
config.frame_rate = FPS
config.background_color = BG_COLOR

# ---------------------------------------------------------------------------
# Constantes propias de esta escena (maquetación; no van en params.py)
# ---------------------------------------------------------------------------
INTEGRANTES = "Bayron Flores · Rodrigo Gutiérrez · Jose Jiménez"
VOZ = "Voz: Bayron Flores"
EVENTO = "EID Manim 2026"

# Instantes de fin de cada sección (s). El último sale de params.DURACION_PARTE.
T1, T2, T3, T4, T5 = 14, 36, 54, 74, 96
T_FIN = DURACION_PARTE["parte1"]          # 105 s

PANEL_W = 5.4                              # ancho máximo del panel derecho

# Fuente del contrato (params.FONT = "DejaVu Sans") incluida en el repositorio,
# en <raíz>/fonts/. Así no hace falta instalarla en el sistema.
RUTA_FUENTES = Path(__file__).resolve().parent.parent / "fonts"
ARCHIVOS_FUENTE = ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf")


def coma(x, d=4, signo=False):
    """Número con coma decimal para usar dentro de MathTex: 0{,}75."""
    s = f"{x:+.{d}f}" if signo else f"{x:.{d}f}"
    return s.replace(".", "{,}")


class EscenaTeoria(Scene):
    # ------------------------------------------------------------------ util
    def hasta(self, t):
        """Espera hasta el instante t (s) del clip, para sincronizar con la voz."""
        resto = t - self.renderer.time
        if resto > 0.034:
            self.wait(resto)
        elif resto < -0.05:
            print(f"[AVISO] se pasó {-resto:.2f} s del instante {t} s")

    def limpiar(self, rt=0.6):
        """Borra todo salvo la etiqueta de voz."""
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.tag],
                  run_time=rt)

    def panel(self, *mobs, buff=0.3):
        """Apila mobjects en columna a la derecha del gráfico."""
        g = VGroup(*mobs).arrange(DOWN, aligned_edge=LEFT, buff=buff)
        if g.width > PANEL_W:
            g.scale_to_fit_width(PANEL_W)
        g.to_edge(RIGHT, buff=0.5).shift(UP * 0.3)
        return g

    # ------------------------------------------------------------- principal
    def construct(self):
        # register_font carga los .ttf solo mientras dura este bloque.
        with ExitStack() as pila:
            for nombre in ARCHIVOS_FUENTE:
                ruta = RUTA_FUENTES / nombre
                if ruta.exists():
                    pila.enter_context(register_font(str(ruta)))
                else:
                    print(f"[AVISO] no se encontró {ruta}")
            self.animar()

    def animar(self):
        self.tag = Text(VOZ, font=FONT, font_size=22, color=AXIS_COLOR)
        self.tag.to_corner(UL, buff=0.3)
        self.add(self.tag)

        self.s1_presentacion()
        self.s2_situacion()
        self.s3_particion()
        self.s4_aportes()
        self.s5_integral()
        self.s6_integral_vs_area()
        self.hasta(T_FIN)

    # ---------------------------------------------------- S1: presentación
    def s1_presentacion(self):
        a, b = MAIN.a, MAIN.b
        cero = MAIN.ceros[0]

        # --- fondo: cuadrícula muy tenue + línea divisoria
        rejilla = NumberPlane(
            x_range=[-8, 8, 1], y_range=[-5, 5, 1],
            background_line_style={"stroke_color": AXIS_COLOR,
                                   "stroke_opacity": 0.07, "stroke_width": 1},
            faded_line_ratio=0,
            axis_config={"stroke_opacity": 0, "include_ticks": False},
        ).set_z_index(-5)
        divisoria = Line(UP * 2.9 + LEFT * 0.1, DOWN * 1.9 + LEFT * 0.1,
                         color=AXIS_COLOR, stroke_width=1.5,
                         stroke_opacity=0.35)

        # --- columna derecha: marca, título, subtítulo, pregunta
        marca = VGroup(
            Square(0.16, fill_color=POS_COLOR, fill_opacity=1, stroke_width=0),
            Square(0.16, fill_color=NEG_COLOR, fill_opacity=1, stroke_width=0),
            Text(CURSO.upper(), font=FONT, font_size=20, color=AXIS_COLOR),
        ).arrange(RIGHT, buff=0.14)

        lineas_t = textwrap.fill(TEMA, 20).split("\n")
        titulo = VGroup(*[Text(l, font=FONT, font_size=42, weight=BOLD)
                          for l in lineas_t]).arrange(DOWN, aligned_edge=LEFT,
                                                      buff=0.12)
        acento = Line(ORIGIN, RIGHT * 1.3, color=CURVE_COLOR, stroke_width=6)
        subtitulo = Text(f"Grupo {GRUPO}  ·  {EVENTO}", font=FONT,
                         font_size=20, color=AXIS_COLOR)
        bloque_t = VGroup(titulo, acento, subtitulo).arrange(
            DOWN, aligned_edge=LEFT, buff=0.28)

        etiqueta_q = Text("PREGUNTA CENTRAL", font=FONT, font_size=17,
                          color=SUM_COLOR, weight=BOLD)
        texto_q = VGroup(*[Text(l, font=FONT, font_size=24) for l in
                           textwrap.fill(PREGUNTA_CENTRAL, 30).split("\n")]
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        barra_q = Line(texto_q.get_corner(UL) + LEFT * 0.25,
                       texto_q.get_corner(DL) + LEFT * 0.25,
                       color=SUM_COLOR, stroke_width=4)
        pregunta = VGroup(etiqueta_q, VGroup(barra_q, texto_q)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2)

        derecha = VGroup(marca, bloque_t, pregunta).arrange(
            DOWN, aligned_edge=LEFT, buff=0.5)
        if derecha.width > 6.2:
            derecha.scale_to_fit_width(6.2)
        derecha.move_to(RIGHT * 3.5 + UP * 0.35)

        # --- columna izquierda: gráfica gancho con regiones azul / roja
        ax = Axes(
            x_range=[0, 3.4, 1], y_range=[-1.4, 3.4, 1],
            x_length=5.2, y_length=3.6,
            axis_config={"color": AXIS_COLOR, "include_tip": True,
                         "tip_width": 0.15, "tip_height": 0.15,
                         "include_ticks": False},
        ).move_to(LEFT * 3.65 + UP * 0.55)
        curva = ax.plot(MAIN.f, x_range=[a, b], color=CURVE_COLOR,
                        stroke_width=5)
        area_pos = ax.get_area(curva, x_range=(a, cero), color=POS_COLOR,
                               opacity=0.55).set_stroke(width=0)
        area_neg = ax.get_area(curva, x_range=(cero, MAIN.ceros[1]),
                               color=NEG_COLOR, opacity=0.55
                               ).set_stroke(width=0)
        mas = Text("+", font=FONT, font_size=40, color=WHITE,
                   weight=BOLD).move_to(ax.c2p(0.38, 0.85))
        menos = Text("−", font=FONT, font_size=40, color=WHITE,
                     weight=BOLD).move_to(ax.c2p(2.0, -0.45))
        gancho = MathTex(
            rf"\int_{{{int(a)}}}^{{{int(b)}}} r({MAIN.var})\,d{MAIN.var}\ =\ ?",
            font_size=44, color=SUM_COLOR).move_to(LEFT * 3.65 + DOWN * 2.2)

        # --- franja inferior: integrantes
        nombres = [n.strip() for n in INTEGRANTES.split("·")]
        chips = VGroup()
        for nombre in nombres:
            t = Text(nombre, font=FONT, font_size=21)
            caja = RoundedRectangle(
                corner_radius=0.2, width=t.width + 0.55, height=t.height + 0.4,
                stroke_color=SUM_COLOR, stroke_width=2,
                fill_color=SUM_COLOR, fill_opacity=0.12)
            chips.add(VGroup(caja, t))
        chips.arrange(RIGHT, buff=0.3).move_to(DOWN * 3.4)

        # --- animación (voz: 0-5 s grupo y nombres; 5-8.5 tema; 8.5-14 pregunta)
        self.play(FadeIn(rejilla), FadeIn(divisoria),
                  FadeIn(marca, shift=DOWN * 0.15), run_time=1.0)       # 1.0
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in chips],
                              lag_ratio=0.25), run_time=1.6)            # 2.6 nombres
        self.play(FadeIn(ax), run_time=0.8)                             # 3.4
        self.play(Create(curva), run_time=1.5)                          # 4.9
        self.hasta(5)
        self.play(Write(titulo), run_time=1.6)                          # 6.6 tema
        self.play(FadeIn(acento, shift=RIGHT * 0.3), FadeIn(subtitulo),
                  run_time=0.5)                                         # 7.1
        self.hasta(7.2)
        self.play(FadeIn(area_pos), FadeIn(area_neg), FadeIn(mas),
                  FadeIn(menos), run_time=1.1)                          # 8.3 regiones
        self.hasta(8.5)
        self.play(FadeIn(pregunta, shift=UP * 0.2), run_time=1.5)       # 10.0 pregunta
        self.hasta(10.8)
        self.play(FadeIn(gancho, shift=UP * 0.15), run_time=0.9)        # 11.7
        self.play(Indicate(gancho, color=SUM_COLOR, scale_factor=1.08),
                  run_time=1.0)                                         # 12.7
        self.hasta(T1 - 0.6)
        self.limpiar(0.6)

    # ------------------------------------------------- S2: situación (buffer)
    def s2_situacion(self):
        a, b = MAIN.a, MAIN.b
        cero = MAIN.ceros[0]                      # donde r cambia de signo
        u_f, u_t = MAIN.unidad_f, MAIN.unidad_var

        ax = Axes(
            x_range=[0, 3.5, 1], y_range=[-1.5, 3.5, 1],
            x_length=6.6, y_length=4.8,
            axis_config={"color": AXIS_COLOR, "include_tip": True,
                         "tip_width": 0.18, "tip_height": 0.18},
            x_axis_config={"numbers_to_include": [0, 1, 2, 3],
                           "font_size": 24},
            y_axis_config={"numbers_to_include": [-1, 1, 2, 3],
                           "font_size": 24},
        )
        ax.to_edge(LEFT, buff=0.6).shift(DOWN * 0.25)
        ax.x_axis.numbers.set_z_index(10)
        lab_x = MathTex(rf"{MAIN.var}\ [\mathrm{{{u_t}}}]", font_size=28,
                        color=AXIS_COLOR).next_to(ax.x_axis.get_end(), DOWN,
                                                  buff=0.2)
        lab_y = MathTex(rf"r({MAIN.var})\ [\mathrm{{{u_f}}}]", font_size=28,
                        color=AXIS_COLOR).next_to(ax.y_axis.get_top(), RIGHT,
                                                  buff=0.3)
        curva = ax.plot(MAIN.f, x_range=[a, b], color=CURVE_COLOR,
                        stroke_width=4)
        area_pos = ax.get_area(curva, x_range=(a, cero), color=POS_COLOR,
                               opacity=0.3)
        area_neg = ax.get_area(curva, x_range=(cero, MAIN.ceros[1]),
                               color=NEG_COLOR, opacity=0.3)
        area_pos.set_stroke(width=0)
        area_neg.set_stroke(width=0)

        t1 = Text("Buffer de red", font=FONT, font_size=32, color=SUM_COLOR,
                  weight=BOLD)
        t2 = MathTex(r"r(t)=\text{llegada}-\text{salida}", font_size=34)
        t3 = MathTex(MAIN.etiqueta_f + rf"\ \ [\mathrm{{{u_f}}}]",
                     font_size=36, color=CURVE_COLOR)
        t4 = MathTex(rf"t\in[{int(a)},{int(b)}]\ \mathrm{{{u_t}}}",
                     font_size=34)
        t5 = Text("r > 0 :  el buffer gana datos", font=FONT, font_size=26,
                  color=POS_COLOR)
        t6 = Text("r < 0 :  el buffer pierde datos", font=FONT, font_size=26,
                  color=NEG_COLOR)
        p2 = self.panel(t1, t2, t3, t4, t5, t6, buff=0.35)

        self.play(FadeIn(ax), run_time=1.5)                     # 14 -> 15.5
        self.play(FadeIn(lab_x), FadeIn(lab_y), FadeIn(t1), run_time=1.0)
        self.play(FadeIn(t2), run_time=1.0)                     # llegada-salida
        self.hasta(21)
        self.play(Create(curva), FadeIn(t3), FadeIn(t4), run_time=2.5)
        self.hasta(28.5)
        self.play(FadeIn(area_pos), FadeIn(t5), run_time=1.0)   # r positiva
        self.hasta(32)
        self.play(FadeIn(area_neg), FadeIn(t6), run_time=1.0)   # r negativa
        self.hasta(T2)

        # se conservan para las secciones siguientes
        self.ax, self.curva = ax, curva
        self.lab_x, self.lab_y = lab_x, lab_y
        self.s2_a_borrar = VGroup(area_pos, area_neg, t1, t2, t3, t4, t5, t6)

    # ------------------------------------------- S3: partición y punto muestra
    def s3_particion(self):
        ax = self.ax
        a, b = MAIN.a, MAIN.b
        n = N_VALUES[0]                                  # n = 4
        dx = delta_x(a, b, n)                            # 0,75 s
        xs = partition(a, b, n)
        ms = sample_points(a, b, n)                      # puntos medios

        ticks = VGroup(*[Line(ax.c2p(x, -0.12), ax.c2p(x, 0.12),
                              color=WHITE, stroke_width=3) for x in xs])
        brace = Brace(Line(ax.c2p(xs[0], 0), ax.c2p(xs[1], 0)),
                      direction=DOWN, buff=0.5, color=AXIS_COLOR)
        brace_lab = MathTex(rf"\Delta t={coma(dx, 2)}\ \mathrm{{{MAIN.unidad_var}}}",
                            font_size=26).next_to(brace, DOWN, buff=0.1).shift(RIGHT * 0.8)

        d1 = MathTex(rf"\Delta t=\frac{{b-a}}{{n}}=\frac{{{int(b)}-{int(a)}}}{{{n}}}"
                     rf"={coma(dx, 2)}\ \mathrm{{{MAIN.unidad_var}}}",
                     font_size=34)
        d2 = MathTex(rf"n={n}\ \text{{subintervalos de ancho igual}}",
                     font_size=30)
        d3 = MathTex(r"t_i^{*}=\text{punto medio de }[t_{i-1},\,t_i]",
                     font_size=30, color=SUM_COLOR)
        d4 = MathTex(rf"t_1^{{*}}={coma(ms[0], 3)}\ \mathrm{{s}},\quad "
                     rf"r(t_1^{{*}})={coma(MAIN.f(ms[0]), 3)}\ \mathrm{{{MAIN.unidad_f}}}",
                     font_size=28)
        p3 = self.panel(d2, d1, d3, d4, buff=0.4)

        dots = VGroup(*[Dot(ax.c2p(m, MAIN.f(m)), radius=0.07, color=WHITE)
                        for m in ms])
        dots.set_z_index(5)
        drops = VGroup(*[DashedLine(ax.c2p(m, 0), ax.c2p(m, MAIN.f(m)),
                                    color=WHITE, stroke_width=2,
                                    dash_length=0.08) for m in ms])
        lab_m1 = MathTex(r"(t_1^{*},\,r(t_1^{*}))", font_size=22).next_to(
            dots[0], RIGHT, buff=0.12)

        self.play(FadeOut(self.s2_a_borrar), run_time=0.8)          # 36.8
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.2),
                  FadeIn(d2), run_time=2.0)                         # 38.8
        self.hasta(39.5)
        self.play(FadeIn(d1), run_time=1.5)
        self.hasta(43)
        self.play(GrowFromCenter(brace), FadeIn(brace_lab), run_time=1.2)
        self.hasta(45.5)
        self.play(FadeIn(d3), run_time=1.0)                         # punto muestra
        self.play(FadeIn(dots[0]), Create(drops[0]), FadeIn(lab_m1),
                  FadeIn(d4), run_time=1.2)
        self.hasta(49.5)
        self.play(LaggedStart(*[FadeIn(dots[i]) for i in range(1, n)],
                              lag_ratio=0.3),
                  LaggedStart(*[Create(drops[i]) for i in range(1, n)],
                              lag_ratio=0.3), run_time=2.0)
        self.hasta(T3)

        self.ticks, self.brace, self.brace_lab = ticks, brace, brace_lab
        self.dots, self.drops, self.lab_m1 = dots, drops, lab_m1
        self.s3_a_borrar = VGroup(d1, d2, d3, d4, lab_m1, brace, brace_lab)

    # ------------------------------- S4: rectángulos y aportes con signo
    def s4_aportes(self):
        ax = self.ax
        a, b = MAIN.a, MAIN.b
        n = N_VALUES[0]
        xs = partition(a, b, n)
        ms = sample_points(a, b, n)
        aportes = riemann_terms(MAIN, n)                 # f(t*)·Δt con signo
        Sn = riemann_sum(MAIN, n)

        rects = VGroup()
        for i, (m, ap) in enumerate(zip(ms, aportes)):
            h = MAIN.f(m)
            color = POS_COLOR if ap > 0 else NEG_COLOR
            rects.add(Polygon(
                ax.c2p(xs[i], 0), ax.c2p(xs[i], h),
                ax.c2p(xs[i + 1], h), ax.c2p(xs[i + 1], 0),
                stroke_color=color, stroke_width=2,
                fill_color=color, fill_opacity=FILL_OPACITY))
        lab_r1 = MathTex(r"r(t_1^{*})\,\Delta t", font_size=24).move_to(
            rects[0].get_center())

        head = MathTex(r"\text{aporte}_i=r(t_i^{*})\,\Delta t", font_size=32)
        lineas = VGroup()
        for i, ap in enumerate(aportes, start=1):
            color = POS_COLOR if ap > 0 else NEG_COLOR
            lineas.add(MathTex(
                rf"r(t_{i}^{{*}})\,\Delta t={coma(ap, 4, signo=True)}\ "
                rf"\mathrm{{{MAIN.unidad_acum}}}", font_size=28, color=color))
        suma = MathTex(
            rf"S_{{{n}}}=\sum_{{i=1}}^{{{n}}} r(t_i^{{*}})\,\Delta t"
            rf"={coma(Sn, 4)}\ \mathrm{{{MAIN.unidad_acum}}}",
            font_size=30, color=SUM_COLOR)
        nota = Text(f"n = {n} es una aproximación gruesa", font=FONT,
                    font_size=22, color=AXIS_COLOR)
        p4 = self.panel(head, *lineas, suma, nota, buff=0.28)

        self.play(FadeOut(self.s3_a_borrar), FadeOut(self.drops),
                  run_time=0.6)                                     # 54.6
        self.play(FadeIn(rects[0]), FadeIn(lab_r1), FadeIn(head),
                  run_time=1.2)                                     # aporte = altura x ancho
        self.hasta(59.5)
        self.play(FadeIn(lineas[0]), run_time=1.0)                  # positivo, azul
        self.hasta(63)
        self.play(LaggedStart(*[FadeIn(r) for r in rects[1:]], lag_ratio=0.4),
                  run_time=2.0)                                     # negativos, rojo
        self.play(LaggedStart(*[FadeIn(l) for l in lineas[1:]], lag_ratio=0.4),
                  run_time=2.0)
        self.hasta(68)
        self.play(FadeIn(suma), FadeIn(nota), run_time=1.5)         # S_n con signo
        self.play(Indicate(suma, color=SUM_COLOR, scale_factor=1.05),
                  run_time=1.0)
        self.hasta(T4)

    # ----------------------------- S5: suma -> límite -> integral definida
    def s5_integral(self):
        self.limpiar(0.8)                                           # 74.8

        sn = MathTex(r"S_n=\sum_{i=1}^{n} f(x_i^{*})\,\Delta x", font_size=44)
        sn.move_to(UP * 2.9)
        flecha = MathTex(r"\Downarrow\quad n\to\infty,\quad \Delta x\to 0",
                         font_size=32, color=CURVE_COLOR).move_to(UP * 2.0)
        integral = MathTex(r"\int_a^b", r"f(x)", r"\,dx",
                           r"=\lim_{n\to\infty}\sum_{i=1}^{n} f(x_i^{*})\,\Delta x",
                           font_size=46)
        integral.move_to(UP * 0.8)
        condicion = Text("Condición: f continua en [a, b]", font=FONT,
                         font_size=28, color=SUM_COLOR).move_to(DOWN * 0.3)

        filas = [
            (MathTex(r"\int", font_size=40),
             "signo de integral: viene de «suma»", 0),
            (MathTex(r"a,\ b", font_size=36),
             "límites de integración (extremos del intervalo)", 0),
            (MathTex(r"f(x)", font_size=36),
             "integrando: la función (altura o tasa)", 1),
            (MathTex(r"dx", font_size=36),
             "variable de integración", 2),
        ]
        filas_mob = []
        for k, (sim, texto, _) in enumerate(filas):
            y = -1.2 - 0.72 * k
            sim.move_to([-4.2, y, 0])
            txt = Text(texto, font=FONT, font_size=26)
            txt.move_to([-3.3, y, 0], aligned_edge=LEFT)
            filas_mob.append(VGroup(sim, txt))

        self.play(FadeIn(sn), run_time=1.2)                         # 76
        self.play(FadeIn(flecha), run_time=1.0)
        self.hasta(79)
        self.play(FadeIn(condicion), run_time=1.0)                  # continua
        self.play(Write(integral), run_time=3.0)                    # integral definida
        self.hasta(86.5)
        for (sim, texto, parte), fila, t_ini in zip(
                filas, filas_mob, (86.5, 89, 91.5, 93.5)):
            self.hasta(t_ini)
            self.play(FadeIn(fila),
                      Indicate(integral[parte], color=CURVE_COLOR),
                      run_time=1.2)
        self.hasta(T5)

    # ------------------------------- S6: integral (con signo) vs. área
    def s6_integral_vs_area(self):
        self.limpiar(0.6)                                           # 96.6

        def col(titulo, color, formula, signo):
            t = Text(titulo, font=FONT, font_size=30, color=color, weight=BOLD)
            f = MathTex(formula, font_size=48)
            leyenda = VGroup(
                Text("azul", font=FONT, font_size=26, color=POS_COLOR),
                Text(signo, font=FONT, font_size=30),
                Text("rojo", font=FONT, font_size=26, color=NEG_COLOR),
            ).arrange(RIGHT, buff=0.25)
            g = VGroup(t, f, leyenda).arrange(DOWN, buff=0.4)
            caja = SurroundingRectangle(g, buff=0.4, color=AXIS_COLOR,
                                        corner_radius=0.15)
            return VGroup(caja, g)

        izq = col("Integral definida", SUM_COLOR, r"\int_a^b f(x)\,dx", "−")
        der = col("Área geométrica", CURVE_COLOR, r"\int_a^b |f(x)|\,dx", "+")
        izq.move_to(LEFT * 3.4 + UP * 0.6)
        der.move_to(RIGHT * 3.4 + UP * 0.6)
        sub_i = Text("acumulación con signo", font=FONT, font_size=24,
                     color=AXIS_COLOR).next_to(izq, DOWN, buff=0.25)
        sub_d = Text("todo cuenta en positivo", font=FONT, font_size=24,
                     color=AXIS_COLOR).next_to(der, DOWN, buff=0.25)
        pregunta = Text("¿Cuánto vale la integral en nuestro buffer?",
                        font=FONT, font_size=32).move_to(DOWN * 2.5)
        pase = Text("Continúa Rodrigo Gutiérrez  →", font=FONT, font_size=28,
                    color=CURVE_COLOR).next_to(pregunta, DOWN, buff=0.35)

        self.play(FadeIn(izq), FadeIn(sub_i), run_time=1.2)         # 97.8
        self.hasta(99.5)
        self.play(FadeIn(der), FadeIn(sub_d), run_time=1.2)         # 100.7
        self.hasta(101.5)
        self.play(FadeIn(pregunta), run_time=1.0)
        self.hasta(103.2)
        self.play(FadeIn(pase), run_time=0.8)
        self.hasta(T_FIN)