# Parte 3 — Integral frente a área y cierre

**Grupo 15 · MAT1188 Cálculo Intermedio · Integrante: José**
Tramo del video: 3:30–5:15 (105 s) · Escena: `escena_area_vs_integral.py` · Clase: `EscenaAreaVsIntegral`

Pregunta central del grupo: *¿Cómo puede una integral valer cero aunque existan regiones con área positiva?*

Esta parte recibe el resultado de la parte 2 (la integral del buffer vale 0 MB), lo contrasta con el área
geométrica, muestra un segundo ejemplo donde la simetría explica la cancelación, responde la pregunta
central y cierra con los créditos.

---

## 1. Resumen matemático

**Integral con signo.** La integral definida es el límite de sumas de Riemann con signo:

$$\int_a^b f(x)\,dx=\lim_{n\to\infty}\sum_{i=1}^{n} f(x_i^*)\,\Delta x,\qquad \Delta x=\frac{b-a}{n}$$

Donde `f < 0`, cada aporte `f(x_i*)Δx` es negativo y resta. Por eso los tramos sobre el eje (azul) y bajo el
eje (rojo) pueden compensarse.

**Área geométrica.** Cuenta todo como positivo:

$$\text{área}=\int_a^b |f(x)|\,dx=\sum_{\text{tramos}}\left|\int_{c_k}^{c_{k+1}} f(x)\,dx\right|$$

donde `c_k` son los extremos del intervalo y los puntos donde `f` cambia de signo (`ceros` en `params.py`).

**Ejemplo principal (no simétrico)** — tasa neta de un buffer de red, `r(t) = t² − 4t + 3` MB/s en `[0, 3]` s,
con antiderivada `F(t) = t³/3 − 2t² + 3t`:

| Tramo | Cálculo | Valor |
|---|---|---|
| `[0, 1]` (r ≥ 0) | `F(1) − F(0) = 4/3 − 0` | `+4/3` MB (el buffer gana) |
| `[1, 3]` (r ≤ 0) | `F(3) − F(1) = 0 − 4/3` | `−4/3` MB (el buffer pierde) |
| Integral | `4/3 + (−4/3)` | `0` MB |
| Área | `\|4/3\| + \|−4/3\|` | `8/3` MB ≈ 2,667 MB (tráfico total movido) |

Unidades: `(MB/s)·s = MB`. Con puntos medios y `n = 32`: `Σ|r(t_i*)|Δt ≈ 2,665` MB, que se acerca a `8/3`.

**Ejemplo complementario (simétrico)** — `f(x) = x³ − 4x` en `[−2, 2]`, con `F(x) = x⁴/4 − 2x²`.
`f` es impar (`f(−x) = −f(x)`), con ceros en `−2, 0, 2`:

| Tramo | Cálculo | Valor |
|---|---|---|
| `[−2, 0]` (f ≥ 0) | `F(0) − F(−2) = 0 − (4 − 8)` | `+4` |
| `[0, 2]` (f ≤ 0) | `F(2) − F(0) = (4 − 8) − 0` | `−4` |
| Integral | `4 + (−4)` | `0` |
| Área | `4 + 4` | `8` |

La región azul, girada 180° alrededor del origen, coincide con la roja: esa es la causa visual de la
cancelación. Con puntos medios la suma con signo da exactamente 0 para todo `n`, porque los puntos muestra
son simétricos respecto de 0 y `f` es impar, así que sus aportes se anulan de a pares. La suma
`Σ|f(x_i*)|Δx` con `n = 32` da `≈ 8,016` y se acerca al área 8.

**Respuesta a la pregunta central.** Una integral puede valer 0 porque es un límite de sumas *con signo*:
los aportes positivos y negativos se compensan, aunque cada región tenga área positiva.

**Limitación.** `∫ f = 0` no implica que `f` sea la función nula, ni que el área sea cero. En ambos ejemplos
la integral es 0 y el área es positiva (`8/3` y `8`).

---

## 2. Qué hace la escena, bloque por bloque

La escena divide los 105 s en cinco bloques. Cada bloque termina en un segundo fijo (`FIN_BLOQUE`), para que
la narración grabada coincida con la animación.

| Bloque | Tiempo | Qué se ve | Método |
|---|---|---|---|
| A. Traspaso | 0–20 s | Gráfica de `r(t)` con la región azul (`+4/3 MB`) y la roja (`−4/3 MB`); resultado `∫ r dt = 0 MB`; pregunta «¿Significa que no pasó nada?» | `bloque_a` |
| B. Integral frente a área | 20–45 s | `∫\|r\| dt = 8/3 MB`; la región roja se refleja sobre el eje y se vuelve verde; `4/3 + 4/3 = 8/3`; «tráfico total que se movió»; `Σ\|r(t_i*)\|Δt ≈ 2,665` | `bloque_b` |
| C. Ejemplo simétrico | 45–68 s | Gráfica de `x³ − 4x`; una sombra gris de la región azul gira 180° sobre el origen y cae sobre la roja; `∫ f = 0`, `∫\|f\| = 8`, `Σ\|f(x_i*)\|Δx ≈ 8,016` | `bloque_c` |
| D. Respuesta y límite | 68–82 s | Pregunta central, respuesta, límite de sumas con signo y la limitación | `bloque_d` |
| E. Créditos | 82–105 s | Pantalla de créditos | `bloque_e` |

### Cómo está organizado el código

- **Funciones auxiliares** (arriba del archivo): no dibujan por sí solas.
  - `cortes(ej)`: extremos del intervalo y ceros de `f`, ordenados. Define dónde cambia el signo.
  - `valor_tramo(ej, c1, c2)`: integral exacta en un tramo, `F(c2) − F(c1)`, solo para etiquetar los valores.
  - `fraccion_tex(valor)`: convierte `1,3333…` en `\tfrac{4}{3}` para mostrarlo como fracción.
  - `integral_tex(ej, absoluto)`: arma el texto LaTeX de `∫ f dx` o `∫ |f| dx` con los límites de `ej.a` y `ej.b`.
  - `construir_grafica(ej, y_min, y_max)`: crea los ejes, la curva, y una región por cada tramo entre ceros,
    coloreada por su signo (azul si `f > 0` en el punto medio del tramo, rojo si `f < 0`), con su etiqueta de valor.
- **Clase `EscenaAreaVsIntegral`**: `construct` carga las fuentes y llama a `animar`, que ejecuta los cinco bloques.
  - `jugar(...)`: reproduce una animación y suma su duración a un reloj interno.
  - `hasta(segundo)`: espera lo que falte para que el bloque termine en el segundo previsto. Si un bloque se
    pasa, imprime `[AVISO]` en la consola.
  - `limpiar()`: hace desaparecer lo que hay en pantalla entre bloques.

### Las dos animaciones clave

- **Reflejo (bloque B):** `Transform(copia, reflejo)`, donde `reflejo` es la región roja reflejada sobre el
  eje horizontal (`flip(RIGHT, about_point=origen)`) y pintada de verde. Muestra que, al tomar el área, lo
  negativo pasa a contar como positivo.
- **Giro de 180° (bloque C):** `Rotate(sombra, angle=PI, about_point=origen)`. La región azul copiada, girada
  alrededor del origen, cae sobre la roja: es la simetría de una función impar.

---

## 3. Parámetros de `params.py` que usa esta escena

| Parámetro | Qué representa | Dónde se usa |
|---|---|---|
| `MAIN`, `SYM` | Ejemplo principal y ejemplo simétrico | Toda la escena |
| `MAIN.f`, `SYM.f` | La función `r(t)` o `f(x)` | La curva y el punto medio de cada tramo |
| `.a`, `.b` | Extremos del intervalo `[a, b]` | Ejes, curva y límites de la integral |
| `.F` | Antiderivada (solo verificación) | Valor exacto de cada tramo (`F(c2) − F(c1)`) |
| `.ceros` | Puntos donde `f` cambia de signo | Separa las regiones sobre y bajo el eje |
| `.integral_exacta`, `.area_exacta` | `∫ f` y `∫ \|f\|` exactos | Los resultados que se muestran en pantalla |
| `.etiqueta_f`, `.var`, `.unidad_*` | Nombre de la función, variable y unidades (MB/s, s, MB) | Rótulos de ejes y de resultados |
| `N_VALUES` (último valor, `32`) | Refinamiento de la partición | La aproximación `Σ\|f\|Δx` |
| `riemann_abs_sum` | `Σ\|f(x_i*)\|Δx`, aproximación del área | Las líneas `≈ 2,665` y `≈ 8,016` |
| `POS_COLOR`, `NEG_COLOR` | Azul = aporte positivo, rojo = negativo | Relleno de las regiones |
| `CURVE_COLOR`, `AXIS_COLOR`, `SUM_COLOR` | Curva, ejes, resultado | Estilo común del video |
| `BG_COLOR`, `FILL_OPACITY` | Fondo oscuro y opacidad del relleno | Estilo común |
| `PIXEL_WIDTH`, `PIXEL_HEIGHT`, `FPS` | 1920×1080 a 30 fps | Configuración de Manim |
| `FONT` | DejaVu Sans, cargada desde `fonts/` | Todos los textos |
| `DURACION_PARTE["parte3"]` | 105 s | Segundo final del bloque E |
| `CURSO`, `GRUPO`, `TEMA`, `PREGUNTA_CENTRAL` | Datos del grupo | Créditos y bloque D |

Constantes propias de esta escena (posiciones y tiempos): `FIN_BLOQUE`, `EJES_*`, `PANEL_X`, `FILAS`.

---

## 4. Pantalla de créditos

El bloque E arma una lista de textos (`Text`, con la fuente `FONT`) a partir de constantes definidas al inicio
del archivo. Se ordenan hacia abajo con `arrange(DOWN)`, se ajustan al tamaño de la pantalla con
`scale_to_fit_width` y `scale_to_fit_height`, y entran con `LaggedStart(FadeIn(...))`.

Recursos citados:
- Apunte base: Higueras, N., Oyarzo, F. y Matus, V. (2026). *Introducción a la integral*. Cálculo Intermedio.
- Strang, G. y Herman, E. (2016). *Calculus Volume 1*, §5.2 «The Definite Integral». OpenStax.
  https://openstax.org/books/calculus-volume-1
- Segunda fuente matemática complementaria: ver README de la parte 2.
- Manim Community v0.22.0, documentación oficial. https://docs.manim.community
- DejaVu Fonts (licencia libre). https://dejavu-fonts.github.io
- Declaración de uso de IA de los tres integrantes.

---

## 5. Cómo renderizar

Siempre desde la **raíz del repositorio** (donde está `params.py`), con la raíz en `PYTHONPATH`.
Antes de renderizar, ejecutar `python params.py`: debe terminar en `OK: parámetros consistentes.`

**PowerShell**
```
$env:PYTHONPATH="."
python params.py
manim -ql parte3_area_vs_integral\escena_area_vs_integral.py EscenaAreaVsIntegral
```

**CMD**
```
set PYTHONPATH=.
python params.py
manim -ql parte3_area_vs_integral\escena_area_vs_integral.py EscenaAreaVsIntegral
```

**Linux / macOS**
```
PYTHONPATH=. python params.py
PYTHONPATH=. manim -ql parte3_area_vs_integral/escena_area_vs_integral.py EscenaAreaVsIntegral
```

- `-ql` es la prueba rápida. Para la versión final se usa `-qh`.
- El video queda en `media/videos/escena_area_vs_integral/1080p30/EscenaAreaVsIntegral.mp4` y no tiene audio:
  la voz se graba aparte y se une al video para exportar `parte3.mp4`.
- La duración total es de 105 s. Si la consola muestra `[AVISO]`, algún bloque se pasó de su tiempo.

---

## 6. Verificación

- `python params.py` confirma `∫ = 0` y las áreas `8/3` y `8` con la antiderivada, y muestra las sumas para
  `n = 4, 8, 16, 32`.
- Los valores de cada tramo (`±4/3` y `±4`) se calcularon a mano con `F` y coinciden con los que muestra la
  escena (que los obtiene de `F` en `params.py`).
- Los números que se dicen en el guion (`guion_parte3.md`) coinciden con esa salida.

---

## 7. Declaración de uso de IA (José)

**Herramienta:** Claude (Anthropic).

**Para qué la usé:**
- Entender la pauta, la rúbrica y el reparto de tareas del EID.
- Escribir el código de la escena de Manim de mi parte (`escena_area_vs_integral.py`).
- Redactar un borrador de este README y del guion (`guion_parte3.md`).
- Explicarme los cálculos de los ejemplos y cómo se aplican en la animación.

**Partes apoyadas:** el código de `escena_area_vs_integral.py`, el borrador de este README y el borrador del
guion. La IA no reemplazó las fuentes: el apunte base, OpenStax y la documentación de Manim se citan en los
créditos.

**Cómo verifiqué lo que usé:**
- Ejecuté `python params.py` en mi computador y terminó en `OK: parámetros consistentes.`
- Rendericé la escena en mi computador con Manim v0.22.0 y revisé el video bloque por bloque.
- Comprobé a mano los valores de cada tramo con las antiderivadas: `F(0) = 0`, `F(1) = 4/3`, `F(3) = 0` para
  el ejemplo principal; `F(−2) = −4`, `F(0) = 0`, `F(2) = −4` para el simétrico.
- Comparé los números que aparecen en pantalla y en el guion con la salida de `python params.py`.
