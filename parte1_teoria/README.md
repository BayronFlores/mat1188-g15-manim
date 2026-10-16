# Parte 1 — Presentación y teoría

**Grupo 15 · MAT1188 Cálculo Intermedio · Integrante: Bayron**
Tramo del video: 0:00–1:45 (105 s) · Escena: `escena_teoria.py` · Clase: `EscenaTeoria`

Pregunta central del grupo: _¿Cómo puede una integral valer cero aunque existan regiones con área positiva?_

Esta parte abre el video. Presenta al grupo, el tema y la pregunta central; plantea la situación del buffer de
red; construye paso a paso la suma de Riemann con signo hasta llegar a la integral definida; y termina
contrastando la integral con el área geométrica para dar paso a la parte 2 (Rodrigo).

---

## 1. Resumen matemático

**Situación.** Un buffer de red recibe y envía datos. Su tasa neta es

$$r(t)=\text{llegada}-\text{salida}=t^2-4t+3\quad[\mathrm{MB/s}],\qquad t\in[0,3]\ \mathrm{s}$$

- Si `r > 0`, el buffer gana datos (tramo `[0, 1]`).
- Si `r < 0`, el buffer pierde datos (tramo `[1, 3]`).

**Partición y punto muestra.** Se divide `[a, b]` en `n` subintervalos de igual ancho:

$$\Delta t=\frac{b-a}{n}=\frac{3-0}{4}=0{,}75\ \mathrm{s}\qquad (n=4)$$

El punto muestra `t_i*` es el **punto medio** de cada subintervalo: `0,375 · 1,125 · 1,875 · 2,625` s.

**Aportes con signo.** Cada rectángulo aporta `r(t_i*)·Δt` (altura por ancho). Si `r(t_i*) < 0`, el aporte es
negativo y resta. Con `n = 4`:

| i   | `t_i*` | `r(t_i*)` (MB/s) | Aporte `r(t_i*)Δt` (MB) | Color |
| --- | ------ | ---------------- | ----------------------- | ----- |
| 1   | 0,375  | +1,6406          | +1,2305                 | azul  |
| 2   | 1,125  | −0,2344          | −0,1758                 | rojo  |
| 3   | 1,875  | −0,9844          | −0,7383                 | rojo  |
| 4   | 2,625  | −0,6094          | −0,4570                 | rojo  |
|     |        | **Suma `S_4`**   | **≈ −0,1406**           |       |

`S_4` es una aproximación gruesa; la parte 2 la refina con más subintervalos.

**Suma de Riemann → integral definida.** Al hacer `n → ∞` (y `Δx → 0`):

$$\int_a^b f(x)\,dx=\lim_{n\to\infty}\sum_{i=1}^{n} f(x_i^*)\,\Delta x,\qquad \Delta x=\frac{b-a}{n}$$

con la condición de que `f` sea continua en `[a, b]`. Símbolos: `∫` (viene de «suma»), `a, b` (límites de
integración), `f(x)` (integrando: altura o tasa) y `dx` (variable de integración).

**Integral con signo frente a área geométrica** (idea que se deja planteada para las partes 2 y 3):

$$\int_a^b f(x)\,dx\ \ (\text{acumulación con signo})\qquad\text{vs.}\qquad \int_a^b |f(x)|\,dx\ \ (\text{todo cuenta en positivo})$$

La escena cierra con la pregunta «¿Cuánto vale la integral en nuestro buffer?», que responde Rodrigo.

---

## 2. Qué hace la escena, sección por sección

La escena divide los 105 s en seis secciones. Cada una termina en un segundo fijo (`T1`…`T5` y `T_FIN`),
para que la narración grabada coincida con la animación. La función `hasta(t)` espera lo que falte para llegar
a ese instante; si una sección se pasa de su tiempo, imprime `[AVISO]` en la consola.

| Sección               | Tiempo   | Qué se ve                                                                                                                          | Método                |
| --------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| S1. Presentación      | 0–14 s   | Marca del curso, integrantes, gráfica gancho con región azul (+) y roja (−), título del tema, pregunta central y `∫₀³ r(t) dt = ?` | `s1_presentacion`     |
| S2. Situación         | 14–36 s  | Ejes `t` [s] y `r(t)` [MB/s]; «Buffer de red», `r(t) = llegada − salida`, la curva y las regiones `r > 0` (azul) y `r < 0` (rojo)  | `s2_situacion`        |
| S3. Partición         | 36–54 s  | Marcas de la partición, `Δt = (b − a)/n = 0,75 s`, llave con el ancho, puntos medios `t_i*` con líneas punteadas                   | `s3_particion`        |
| S4. Aportes con signo | 54–74 s  | Rectángulos azules (positivo) y rojos (negativo), aporte de cada uno y suma `S_4`                                                  | `s4_aportes`          |
| S5. Suma → integral   | 74–96 s  | `S_n`, flecha `n → ∞`, integral definida, condición de continuidad y significado de `∫`, `a, b`, `f(x)` y `dx`                     | `s5_integral`         |
| S6. Integral vs. área | 96–105 s | Dos tarjetas: «Integral definida» (`∫ f dx`, azul − rojo) y «Área geométrica» (`∫ \|f\| dx`, azul + rojo); pase a Rodrigo          | `s6_integral_vs_area` |

Los ejes y la curva se crean en S2 y se reutilizan hasta S4; entre secciones cambian solo las regiones, los
puntos y los rectángulos, así la partición se dibuja sobre la misma función. `limpiar()` borra todo menos la
etiqueta «Voz: Bayron Flores» al pasar de S4 a S5 y de S5 a S6.

---

## 3. Parámetros de `params.py` que usa esta escena

Todo dato matemático se importa de `params.py`; en la escena solo se definen constantes de maquetación
(`INTEGRANTES`, `VOZ`, `EVENTO`, `T1`–`T5`, `T_FIN`, `PANEL_W`). Colores, fondo, resolución (1920×1080 a 30 fps)
y fuente (DejaVu Sans) también vienen de `params.py`.

| Parámetro                                          | Qué representa                                   | Dónde se usa           |
| -------------------------------------------------- | ------------------------------------------------ | ---------------------- |
| `MAIN` (`f`, `a`, `b`, `ceros`, `var`, `unidad_*`) | Ejemplo principal: función, intervalo y unidades | Toda la escena         |
| `N_VALUES[0]`                                      | `n = 4`, partición gruesa de esta parte          | S3 y S4                |
| `delta_x`, `partition`, `sample_points`            | `Δt`, extremos de la partición y puntos medios   | S3 y S4                |
| `riemann_terms`, `riemann_sum`                     | Aportes `r(t_i*)Δt` y suma `S_n`                 | S4                     |
| `DURACION_PARTE["parte1"]`                         | 105 s                                            | Instante final `T_FIN` |
| `CURSO`, `GRUPO`, `TEMA`, `PREGUNTA_CENTRAL`       | Datos del grupo                                  | S1                     |

---

## 4. Cómo renderizar

Desde la **raíz del repositorio** (donde está `params.py`), con la raíz en `PYTHONPATH`.
Antes de renderizar, ejecutar `python params.py`: debe terminar en `OK: parámetros consistentes.`

```
$env:PYTHONPATH="."
python params.py
manim -ql parte1_teoria\escena_teoria.py EscenaTeoria
```

Ese bloque es para PowerShell. En CMD se usa `set PYTHONPATH=.`; en Linux/macOS, `PYTHONPATH=. manim ...` y
rutas con `/`.

- `-ql` es la prueba rápida; para la versión final se usa `-qh`.
- La fuente DejaVu Sans se carga desde `fonts/` en la raíz del repositorio, así que no hace falta instalarla.
- El video queda en `media/videos/escena_teoria/1080p30/EscenaTeoria.mp4` y no tiene audio: la voz se graba
  aparte y se une al video para exportar `parte1.mp4`.

---

## 5. Declaración de uso de IA (Bayron)

**Herramienta:** Claude (Anthropic).

**Para qué la usé:**

- Para el reparto de tareas del EID.
- Escribir el código de la escena de Manim de mi parte (`escena_teoria.py`).
- Redactar un borrador de este README.
- Explicarme la construcción de la suma de Riemann y cómo se aplica en la animación.

**Partes apoyadas:** el código de `escena_teoria.py`, el borrador de este README.
La IA no reemplazó las fuentes: todas las fuentes utilizadas se citan en los créditos del video (parte 3).

**Cómo verifiqué lo que usé:**

- Ejecuté `python params.py` en mi computador y terminó en `OK: parámetros consistentes.`
- Rendericé la escena con Manim y revisé el video sección por sección, sin avisos `[AVISO]`.
- Comprobé a mano `Δt = 0,75`, los puntos medios y los aportes de la tabla de la sección 1.
- Comparé los números que aparecen en pantalla y en el guion con la salida de `python params.py`.
