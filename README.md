# mat1188-g15-manim

Proyecto de visualización con Manim Community — MAT1188 Cálculo Intermedio, Grupo 15.
Tema: _Integral nula con regiones no nulas_.

---

## 1. Requisitos e instalación (hacer una sola vez)

Probado con **Manim Community v0.22.0** en Windows (Python 3.14, MiKTeX) y en Linux (Python 3.12).

| #   | Programa                                         | Versión        | Para qué sirve               | Obligatorio |
| --- | ------------------------------------------------ | -------------- | ---------------------------- | ----------- |
| 1   | Python                                           | 3.9 o superior | Ejecutar `params.py` y Manim | Sí          |
| 2   | Manim Community                                  | 0.22.0         | Renderizar las escenas       | Sí          |
| 3   | LaTeX (MiKTeX en Windows, TeX Live en Linux/Mac) | actual         | Fórmulas `MathTex`           | Sí          |

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

| Parte                         | Archivo                                              | Clase de la escena | Duración |
| ----------------------------- | ---------------------------------------------------- | ------------------ | -------- |
| 1. Presentación y teoría      | `parte1_teoria/escena_teoria.py`                     | _(completar)_      | 105 s    |
| 2. Ejemplo principal          | `parte2_ejemplo/escena_ejemplo.py`                   | _(completar)_      | 105 s    |
| 3. Integral vs. área y cierre | `parte3_area_vs_integral/escena_area_vs_integral.py` | _(completar)_      | 105 s    |

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
