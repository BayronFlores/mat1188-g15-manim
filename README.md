# mat1188-g15-manim

Proyecto de visualización con Manim Community — MAT1188 Cálculo Intermedio, Grupo 15.
Tema: _Integral nula con regiones no nulas_.

| Dato                   | Detalle                                                                        |
| ---------------------- | ------------------------------------------------------------------------------ |
| Curso                  | MAT1188 – Cálculo Intermedio                                                   |
| Grupo                  | 15                                                                             |
| Tema                   | Integral nula con regiones no nulas                                            |
| Pregunta central       | ¿Cómo puede una integral valer cero aunque existan regiones con área positiva? |
| Ejemplo principal      | Tasa neta de un buffer de red, `r(t) = t² − 4t + 3` MB/s en `[0, 3]` s         |
| Ejemplo complementario | `f(x) = x³ − 4x` en `[−2, 2]`                                                  |

### Integrantes

| N.° | Nombre completo                            | Cuenta de GitHub                                | Parte del video               |
| --- | ------------------------------------------ | ----------------------------------------------- | ----------------------------- |
| 1   | Bayron Rodrigo Flores Riquelme             | [BayronFlores](https://github.com/BayronFlores) | 1. Presentación y teoría      |
| 2   | Rodrigo Ignacio Sebastián Gutiérrez Vielma | [b3divere](https://github.com/b3divere)         | 2. Ejemplo principal          |
| 3   | José Ignacio Jiménez Contreras             | [JJ3972433](https://github.com/JJ3972433)       | 3. Integral vs. área y cierre |

Todos los datos matemáticos (funciones, intervalos, `n`, punto muestra, colores y tiempos) están en `params.py`,
que las tres escenas importan. Cada carpeta de parte tiene su propio `README.md` con el detalle de su escena.

---

## 1. Requisitos e instalación (hacer una sola vez)

Probado con **Manim Community v0.22.0** en Windows (Python 3.14, MiKTeX) y en Linux (Python 3.12).

| #   | Programa                                         | Versión        | Para qué sirve               | Obligatorio           |
| --- | ------------------------------------------------ | -------------- | ---------------------------- | --------------------- |
| 1   | Python                                           | 3.9 o superior | Ejecutar `params.py` y Manim | Sí                    |
| 2   | Manim Community                                  | 0.22.0         | Renderizar las escenas       | Sí                    |
| 3   | LaTeX (MiKTeX en Windows, TeX Live en Linux/Mac) | actual         | Fórmulas `MathTex`           | Sí                    |
| 4   | Fuente DejaVu Sans                               | incluida       | Texto de las escenas         | No (está en `fonts/`) |

### Paso a paso (Windows)

1. **Python.** Instalar desde https://www.python.org/downloads/ y **marcar "Add python.exe to PATH"**.
2. **Manim.** En una terminal nueva:
   ```
   pip install manim==0.22.0
   ```
3. **MiKTeX.** Instalar desde https://miktex.org/download.

> Usar **una sola terminal** para todo el proceso. Si se instaló algo, **cerrar y abrir** la terminal antes de comprobar.

---

## 2. Comprobaciones antes de renderizar

Ejecutar en la terminal, dentro de la **carpeta raíz del repositorio** (la que contiene `params.py`):

| Comprobación    | Comando             | Resultado esperado                        |
| --------------- | ------------------- | ----------------------------------------- |
| Python          | `python --version`  | `Python 3.9` o superior                   |
| pip             | `pip --version`     | muestra una versión                       |
| Manim           | `manim --version`   | `Manim Community v0.22.0` (o superior)    |
| LaTeX           | `latex --version`   | muestra versión de MiKTeX / TeX Live      |
| dvisvgm         | `dvisvgm --version` | muestra una versión                       |
| Datos del grupo | `python params.py`  | termina en `OK: parámetros consistentes.` |

Si todas dan el resultado esperado, se puede renderizar.

---

## 3. Cómo renderizar

Las escenas están en carpetas por integrante y todas importan `params.py` (que está en la raíz). Por eso se ejecutan
**siempre desde la raíz del repositorio**, con la raíz en la ruta de Python (`PYTHONPATH`).

### Escenas del proyecto

| Parte                         | Archivo                                              | Clase de la escena     | Duración |
| ----------------------------- | ---------------------------------------------------- | ---------------------- | -------- |
| 1. Presentación y teoría      | `parte1_teoria/escena_teoria.py`                     | `EscenaTeoria`         | 105 s    |
| 2. Ejemplo principal          | `parte2_ejemplo/escena_ejemplo.py`                   | `EscenaEjemplo`        | 105 s    |
| 3. Integral vs. área y cierre | `parte3_area_vs_integral/escena_area_vs_integral.py` | `EscenaAreaVsIntegral` | 105 s    |

Ejemplo completo (parte 1, en PowerShell):

```
$env:PYTHONPATH="."
python params.py
manim -ql parte1_teoria\escena_teoria.py EscenaTeoria
```

Las escenas no tienen audio: la voz de cada integrante se graba aparte y se une al video de su parte.

### Comando general

Reemplazar `<archivo>` y `<Clase>` por los de la escena que se quiere renderizar (ver tabla).

**CMD (símbolo del sistema):**

```
set PYTHONPATH=.
python params.py
manim -ql <archivo> <Clase>
```

**PowerShell:**

```
$env:PYTHONPATH="."
python params.py
manim -ql <archivo> <Clase>
```

**Linux / macOS:**

```
PYTHONPATH=. python params.py
PYTHONPATH=. manim -ql <archivo> <Clase>
```

### Calidad y salida

- `-ql` = prueba rápida. `params.py` fija 1920×1080 a 30 fps, así que el resultado queda en
  `media/videos/<nombre_del_archivo>/1080p30/`.
- **Versión final:** cambiar `-ql` por `-qh` y, si se quiere, dar nombre al video con `-o <nombre>`:
  `manim -qh -o <nombre> <archivo> <Clase>`
- La primera vez tarda varios minutos (compila cada fórmula con LaTeX); las siguientes reutilizan `media/Tex`
  y son más rápidas.
- Señal de éxito: la consola termina con `Rendered <Clase>` y la ruta del `.mp4`.

---

## 4. Referencias

- **Apunte base.** Higueras, N., Oyarzo, F. y Matus, V. (2026). _Introducción a la integral_. Cálculo Intermedio (Blackboard).
- **Fuentes matemáticas complementarias.**
  1. Strang, G. y Herman, E. (2016). _Calculus Volume 1_, §5.2 «The Definite Integral». OpenStax. https://openstax.org/books/calculus-volume-1
  2. **[COMPLETAR]** Autor o institución, título, año y enlace.
- **Documentación de Manim.** Manim Community Developers. _Manim Community v0.22.0, documentación oficial_. https://docs.manim.community **[COMPLETAR]** año y sección consultada.
- **Recursos adaptados.** **[COMPLETAR]** Origen, autor y enlace, o «Ninguno». Recurso incluido en el repositorio: fuente DejaVu Sans (licencia libre en `fonts/LICENSE-DejaVu.txt`). https://dejavu-fonts.github.io

---

## 5. Declaración de uso de IA

El grupo declara que utilizó IA. La herramienta fue **Claude (Anthropic)**, usada por los tres integrantes. La
finalidad, las partes apoyadas y cómo se verificó cada uso están en la declaración de cada integrante:

| Integrante | Herramienta        | Declaración completa                                                                |
| ---------- | ------------------ | ----------------------------------------------------------------------------------- |
| Bayron     | Claude (Anthropic) | [`parte1_teoria/README.md`](parte1_teoria/README.md), sección 5                     |
| Rodrigo    | Claude (Anthropic) | [`parte2_ejemplo/README.md`](parte2_ejemplo/README.md), sección 7                   |
| José       | Claude (Anthropic) | [`parte3_area_vs_integral/README.md`](parte3_area_vs_integral/README.md), sección 7 |

La IA no reemplazó las fuentes ni la comprensión del proyecto.
