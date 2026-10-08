# GPT desde cero

Un GPT construido pieza por pieza, en Python: **la misma arquitectura que GPT-3, pero en miniatura**, para entender
cada parte programándola. Es el código de la serie de videos **GPT desde cero** del canal
[@ai.explicada](https://www.youtube.com/@ai.explicada).

Cada video tiene su notebook (el código tal cual aparece en pantalla, con las explicaciones) y suma una pieza al
paquete `gptdc`, que al final de la serie es el GPT completo.

## Videos

| # | Video | Notebook | Qué suma a `gptdc` |
|---|-------|----------|--------------------|
| 1 | El tokenizador: BPE desde cero, entrenado con el Quijote | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/maximiranda/gpt-desde-cero/blob/main/notebooks/01_tokenizador.ipynb) | `tokenizador.py`, `datos.py` |
| 2 | *Próximamente:* los números se vuelven vectores y programamos un primer modelo que aprende | | |

## Cómo usarlo

**En Colab** (sin instalar nada): el botón "Abrir en Colab" de cada video, y *Entorno de ejecución → Ejecutar todas*.

**Solo el paquete**, en Colab o en tu computadora:

```bash
pip install git+https://github.com/maximiranda/gpt-desde-cero
```

**En tu computadora**, con los notebooks (Python 3.9 o más nuevo):

```bash
git clone https://github.com/maximiranda/gpt-desde-cero.git
cd gpt-desde-cero
pip install -r requirements.txt
jupyter notebook notebooks/01_tokenizador.ipynb   # o usa el paquete directamente:
```

```python
from gptdc.datos import quijote
from gptdc.tokenizador import Tokenizador

tok = Tokenizador.entrenar(quijote(), fusiones=500)    # ~1 minuto
tok.piezas("Don Quijote le mandó un mensaje a Sancho")  # ['D', 'on', ' Quijote', ' le', ' man', 'd', 'ó', ...]
tok.codificar("Don Quijote")                            # [24, 110, 206]
```

## Estructura

```
notebooks/   un notebook por video
gptdc/       el GPT que vamos construyendo (cada video suma una pieza)
```

Cada video tiene además una etiqueta (`video-01`, `video-02`, …) con el código exactamente como estaba ese día,
aunque el repositorio siga creciendo.

## Textos

El Quijote se descarga de [Project Gutenberg](https://www.gutenberg.org/ebooks/2000) (dominio público) la primera
vez que se usa; no está guardado en el repositorio.

## Licencia

Código bajo licencia [MIT](LICENSE): úsalo libremente, citando la fuente.
