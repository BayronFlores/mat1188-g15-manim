# Parte 2 — Ejemplo principal

**Grupo 15 · MAT1188 Cálculo Intermedio · Integrante: Rodrigo**
Tramo del video: desde 1:45 (≈115 s; el reparto prevé 105 s) · Escena: `escena_ejemplo.py` · Clase: `EscenaEjemplo`

Pregunta central del grupo: _¿Cómo puede una integral valer cero aunque existan regiones con área positiva?_

Esta parte continúa desde la pregunta con que cierra la parte 1 («¿Cuánto vale la integral en nuestro buffer?»).
Explica qué es la tasa neta `r(t)` y por qué se integra, justifica la forma de su gráfica, calcula la integral
de forma exacta con una antiderivada, la comprueba con sumas de Riemann para `n = 4, 8, 16, 32` y entrega el
resultado (0 MB) a la parte 3 (José), que lo contrasta con el área geométrica.

---

## 1. Resumen matemático

**Situación.** Un buffer de red recibe y envía datos. Sea `B(t)` los MB almacenados en el instante `t`. La tasa
neta de cambio es

$$r(t)=\text{llegada}-\text{salida}=B'(t)=t^2-4t+3\quad[\mathrm{MB/s}],\qquad t\in[0,3]\ \mathrm{s}$$

Solo importa la diferencia entre lo que entra y lo que sale, porque lo que queda guardado es esa diferencia.
Si `r > 0` el buffer gana datos; si `r < 0` los pierde. Como `B' = r`, el cambio total del buffer es

$$B(3)-B(0)=\int_0^3 r(t)\,dt\qquad\text{(Teorema Fundamental del Cálculo)}$$

Unidades: `(MB/s)·s = MB`. `r(t)` es un modelo elegido por el grupo, no un dato medido: se escogió para que la
tasa cambie de signo.

**Por qué la gráfica es así.**

| Dato | Cómo se obtiene | Valor |
|---|---|---|
| Forma | Polinomio de grado 2 con coeficiente de `t²` igual a `1 > 0` | Parábola que abre hacia arriba |
| Corte con el eje vertical | `r(0) = 0 − 0 + 3` | `(0, 3)` |
| Cortes con el eje horizontal | `r(t) = (t − 1)(t − 3) = 0`; con la fórmula cuadrática, `t = (4 ± √(16 − 12))/2` | `t = 1` y `t = 3` |
| Vértice | `t = −b/(2a) = 2` (punto medio de los ceros); `r(2) = 4 − 8 + 3` | Mínimo en `(2, −1)` |
| Signo | Entre los ceros la parábola queda bajo el eje | `r ≥ 0` en `[0, 1]` y `r ≤ 0` en `[1, 3]` |

**Antiderivada y cálculo exacto.** Una antiderivada es `F(t) = t³/3 − 2t² + 3t`, porque `F'(t) = t² − 4t + 3`.
Con `F(0) = 0`, `F(1) = 1/3 − 2 + 3 = 4/3` y `F(3) = 9 − 18 + 9 = 0`:

| Tramo | Cálculo | Valor |
|---|---|---|
| `[0, 1]` (r ≥ 0) | `F(1) − F(0) = 4/3 − 0` | `+4/3` MB (el buffer gana) |
| `[1, 3]` (r ≤ 0) | `F(3) − F(1) = 0 − 4/3` | `−4/3` MB (el buffer pierde) |
| Integral | `4/3 + (−4/3)` | `0` MB |

**Por qué da exactamente 0, y no por simetría.** `F(t) = t³/3 − 2t² + 3t = t(t − 3)²/3`, así que `F(0) = 0` y
`F(3) = 0`: la antiderivada vuelve a su valor inicial y `F(3) − F(0) = 0`. El extremo `b = 3` es justo el valor
que cumple eso. La parábola es simétrica respecto de `t = 2`, pero el intervalo `[0, 3]` no lo es; por eso este
ejemplo se distingue del simétrico `x³ − 4x` en `[−2, 2]` de la parte 3.

**Sumas de Riemann con punto medio.** Se usa el criterio común de `params.py` (`SAMPLE_MODE = "medio"`):

$$\Delta t=\frac{3-0}{n},\qquad t_i^*=\left(i-\tfrac12\right)\Delta t,\qquad S_n=\sum_{i=1}^{n} r(t_i^*)\,\Delta t\quad[\mathrm{MB}]$$

| n | Δt (s) | Sₙ (MB) |
|---|---|---|
| 4 | 0,75 | −0,14062 |
| 8 | 0,375 | −0,03516 |
| 16 | 0,1875 | −0,00879 |
| 32 | 0,09375 | −0,00220 |

Los aportes de `n = 4` (uno por rectángulo) están en la tabla del README de la parte 1: `S_4 ≈ −0,1406`.
Las cuatro filas coinciden con la salida de `python params.py`.

**Por qué las sumas tienden a 0.** Como `r` es cuadrática, con punto medio se cumple exactamente

$$S_n=-\frac{9}{4n^2}\qquad\left(\text{error de la regla del punto medio: }\frac{(b-a)\,h^2\,r''}{24}=\frac{3\cdot(3/n)^2\cdot 2}{24}=\frac{9}{4n^2}\right)$$

Al duplicar `n`, `S_n` queda dividida por 4, y `S_n → 0` cuando `n → ∞`, que es el valor de la integral. Con `n`
finito `S_n` no es exactamente 0; es una aproximación.

**Interpretación.** Lo que el buffer gana entre 0 y 1 (+4/3 MB) lo pierde entre 1 y 3 (−4/3 MB): las
contribuciones se compensan exactamente y el buffer termina igual que empezó. El tráfico total que se movió
(`8/3` MB) lo presenta la parte 3.

---

## 2. Qué hace la escena, sección por sección

La escena tiene cinco secciones dentro de `animar`, marcadas con comentarios numerados. Los tiempos salen de la
suma de los `run_time` y de los `wait` de cada sección (no hay un reloj que fuerce el segundo final), y suman
≈ 115,5 s.

| Sección | Tiempo aprox. | Qué se ve |
|---|---|---|
| 1. Apertura | 0–22 s | Título, la pregunta «¿Cuánto vale la integral en nuestro buffer?», `r(t) = t² − 4t + 3` MB/s, «llegada − salida» y `∫₀³ r(t) dt` con «acumula la tasa: (MB/s)·s = MB» |
| 2. Gráfica | 22–45 s | Ejes `t` [s] y `r(t)` [MB/s], la curva y sus datos: punto `r(0) = 3`, ceros `t = 1` y `t = 3` con `r(t) = (t − 1)(t − 3)`, y el mínimo `(2, −1)` |
| 3. Dos tramos y cálculo exacto | 45–71 s | Región azul en `[0, 1]` (el buffer gana) y roja en `[1, 3]` (pierde); `F(t)`, `F(1) − F(0) = 4/3 MB`, `F(3) − F(1) = −4/3 MB` y el total `0 MB` |
| 4. Sumas de Riemann | 71–106,5 s | `S_n`, `Δt = 3/n` y la tabla de `n`, `Δt` y `S_n`; los rectángulos pasan de `n = 4` a 8, 16 y 32 |
| 5. Respuesta | 106,5–115,5 s | Recuadro verde en `S_32`, `S_n → 0 MB` y «El buffer termina igual que empezó» |

### Cómo está organizado el código

- **`construct`**: carga la fuente común (`register_font` dentro de un `ExitStack`) y llama a `animar`.
- **`animar`**: ejecuta las cinco secciones en orden. Los ejes y la curva se crean en la sección 2 y se reutilizan
  hasta la 4; entre secciones cambian las anotaciones, las regiones y los rectángulos.
- **`rectangulos(n)`**: construye un `VGroup` con un `Rectangle` por subintervalo. El ancho es `Δt`, la altura es
  `r(t_i*)` y el color depende del signo del aporte `r(t_i*)Δt` (azul si es positivo, rojo si es negativo).
- **`anotaciones`**: un `VGroup` con los puntos y rótulos de la sección 2, que se retira de una vez al pasar a la 3.
- **`ESPERA_N`**: tupla con la pausa tras la fila de cada `n`, para ajustar la voz sin tocar el resto.
- **Tabla**: los valores de `S_n` se escriben con el signo «−» (menos tipográfico) y con espacio entre columnas
  para que se lean como números negativos y no como restas.

### Las animaciones clave

- **Refinamiento (sección 4):** `ReplacementTransform(rects_actuales, nuevos)` convierte los rectángulos de un
  `n` en los más angostos del `n` siguiente, y se ve cómo siguen mejor la curva.
- **Cancelación (sección 3):** al aparecer las regiones azul y roja, y luego `F(1) − F(0)` y `F(3) − F(1)`,
  `Indicate(total)` resalta que la suma con signo es 0.

---

## 3. Parámetros de `params.py` que usa esta escena

Los datos matemáticos se importan de `params.py`; en la escena solo se definen constantes de maquetación
(`AXES_SHIFT`, `PANEL_X`, `TABLE_COLS`, `TABLE_TOP`, `ROW_STEP`, `SUMA_Y`, `LIM_Y`, `ESPERA_N`).

| Parámetro | Qué representa | Dónde se usa |
|---|---|---|
| `MAIN` | Ejemplo principal: función, intervalo, ceros y unidades | Toda la escena |
| `MAIN.f` | La función `r(t)` | La curva, `r(0)`, el mínimo y la altura de cada rectángulo |
| `MAIN.a`, `MAIN.b` | Extremos `0` y `3` del intervalo | Ejes, curva, límites de `∫` y `Δt` |
| `MAIN.ceros` | Puntos donde `r` cambia de signo (`1` y `3`) | Puntos `t = 1` y `t = 3`; corte entre región azul y roja; el mínimo se ubica en su punto medio |
| `MAIN.etiqueta_f` | Texto LaTeX de `r(t)` | Fórmula de la apertura |
| `MAIN.unidad_var`, `MAIN.unidad_f` | Unidades `s` y `MB/s` | Rótulos de los ejes |
| `MAIN.F` | Antiderivada (solo verificación) | No se usa en la escena; sirve para comprobar `+4/3` y `−4/3` MB |
| `N_VALUES` | `n = 4, 8, 16, 32` | Rectángulos y filas de la tabla |
| `delta_x` | `Δt = (b − a)/n` | Columna `Δt` y ancho de los rectángulos |
| `sample_points` | Puntos medios `t_i*` | Centro de cada rectángulo |
| `riemann_terms` | Aportes `r(t_i*)Δt` con signo | Color de cada rectángulo |
| `riemann_sum` | Suma de Riemann `S_n` | Columna `S_n` de la tabla |
| `POS_COLOR`, `NEG_COLOR` | Azul = aporte positivo, rojo = negativo | Regiones y rectángulos |
| `SUM_COLOR`, `CURVE_COLOR`, `AXIS_COLOR` | Resultado, curva, ejes y textos auxiliares | Estilo común del video |
| `BG_COLOR`, `FILL_OPACITY` | Fondo oscuro y opacidad del relleno | Estilo común |
| `PIXEL_WIDTH`, `PIXEL_HEIGHT`, `FPS` | 1920×1080 a 30 fps | Configuración de Manim |
| `FONT` | DejaVu Sans, cargada desde `fonts/` | Todos los textos |

**Textos que se escriben a mano.** Las fórmulas que se muestran en pantalla (`r(t) = (t − 1)(t − 3)`, `F(t)`,
`4/3`, `Δt = (3 − 0)/n`) están escritas en LaTeX dentro de la escena, no se calculan desde `params.py`. Sus valores
se verificaron con `MAIN.F` y `MAIN.f`; si el grupo cambiara el ejemplo, habría que actualizar esos textos.

---

## 4. Cómo renderizar

Siempre desde la **raíz del repositorio** (donde está `params.py`), con la raíz en `PYTHONPATH`.
Antes de renderizar, ejecutar `python params.py`: debe terminar en `OK: parámetros consistentes.`

**PowerShell**
```
$env:PYTHONPATH="."
python params.py
manim -ql parte2_ejemplo\escena_ejemplo.py EscenaEjemplo
```

Si PowerShell no reconoce `manim`, se ejecuta a través de Python: `py -m manim -ql parte2_ejemplo\escena_ejemplo.py EscenaEjemplo`.

**CMD:** `set PYTHONPATH=.` y los mismos comandos. **Linux / macOS:** `PYTHONPATH=. manim ...` y rutas con `/`.

- Requiere Python 3.13 y Manim Community v0.22.0 (`pip install manim==0.22.0`), y una distribución de LaTeX
  (por ejemplo MiKTeX), porque las fórmulas usan `MathTex`.
- `-ql` es la prueba rápida. Para la versión final se usa `-qh`.
- La fuente DejaVu Sans se carga desde `fonts/` en la raíz del repositorio; si no está, la escena imprime
  `[AVISO]` y sigue con la fuente por defecto.
- El video queda en `media/videos/escena_ejemplo/1080p30/EscenaEjemplo.mp4` y no tiene audio: la voz se graba
  aparte y se une al video para exportar `parte2.mp4`.
- La duración es de ≈ 115 s, unos 10 s más que los 105 s del reparto; el total del video sigue dentro de 4:00–6:00.

---

## 5. Fuentes

Las dos fuentes matemáticas complementarias son OpenStax y Dawkins; coinciden con las de la pantalla de créditos
(parte 3).

- Apunte base: Higueras, N., Oyarzo, F. y Matus, V. (2026). _Introducción a la integral_. Cálculo Intermedio.
- Strang, G. y Herman, E. (2016). _Calculus Volume 1_, §5.2 «The Definite Integral». OpenStax.
  https://openstax.org/books/calculus-volume-1
- Dawkins, P. (2026). _Calculus I – Definition of the Definite Integral_. Paul's Online Notes.
  https://tutorial.math.lamar.edu/Classes/CalcI/DefnOfDefiniteIntegral.aspx
- Manim Community v0.22.0, documentación oficial. https://docs.manim.community
- DejaVu Fonts (licencia libre). https://dejavu-fonts.github.io

**Qué respalda cada una en esta parte.** OpenStax §5.2: la integral definida como límite de sumas de Riemann con
signo (lo que se aplica con `n = 4, 8, 16, 32`). Dawkins: la integral definida como «área neta» entre la gráfica y
el eje, y el contraste entre el valor neto y el total (por ejemplo, desplazamiento neto frente a distancia total),
que corresponde a «el buffer termina igual» frente al tráfico total que presenta la parte 3.

---

## 6. Verificación

- Rendericé la escena con Manim v0.22.0 (Python 3.13) en mi computador y revisé el video; tras verlo ajusté la
  posición de la sumatoria y de la tabla, y el espaciado entre columnas.
- Los valores del ejemplo (`F(0) = 0`, `F(1) = 4/3`, `F(3) = 0`, `r(0) = 3`, `r(2) = −1`) y la identidad
  `F(t) = t(t − 3)²/3` se comprobaron con la función y la antiderivada de `params.py` (`MAIN.f`, `MAIN.F`).
- Las sumas `S_4, S_8, S_16, S_32` coinciden con `−9/(4n²)` y con las cifras de la nota de verificación del reparto
  (`S_4 = −0,1406`, `S_8 = −0,0352`, `S_16 = −0,0088`, `S_32 = −0,0022`).
- Los números del guion base (`guion_parte2.md`) corresponden a esa tabla.

---

## 7. Declaración de uso de IA (Rodrigo)

**Resumen (texto de los créditos del video):**

> Rodrigo usó Claude (Anthropic) para apoyarse al momento de hacer el código de su escena y ajustarlo tras ver el video, realizar preguntas acerca de su guion y si este iba acorde a lo que se explicaba en el video, entender el problema y la gráfica, resolver errores de instalación de Manim. La IA no reemplazó las fuentes, que se citan en los créditos. Verificó los resultados revisando el video renderizado y comprobando los valores y las sumas del ejemplo.

**Detalle:**

**Herramienta:** Claude (Anthropic).

**Para qué la usé:**
- Entender el reparto de tareas y qué debía explicar en mi parte.
- Escribir el código de la escena de Manim (`escena_ejemplo.py`) y ajustar su posición, espaciado y tiempos según
  lo que pedí al ver el video renderizado.
- Redactar un borrador del guion (`guion_parte2.md`) y de este README.
- Explicarme el problema, la forma de la gráfica y la solución, para poder explicarlos con mis palabras.
- Resolver errores de instalación y ejecución de Manim (PowerShell y LaTeX).
- Buscar y comprobar los datos de la segunda fuente matemática (Dawkins).

**Partes apoyadas:** el código de `escena_ejemplo.py`, el borrador del guion, el borrador de este README y la
búsqueda de la segunda fuente. La IA no reemplazó las fuentes: el apunte base, OpenStax, Dawkins y la documentación
de Manim se citan en la sección 5 y en los créditos del video (parte 3).

**Cómo verifiqué lo que usé:** ver la sección 6.