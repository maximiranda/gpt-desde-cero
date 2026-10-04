"""Los textos que usa la serie.

    from gptdc.datos import quijote
    texto = quijote()   # el Quijote completo, de Project Gutenberg (dominio público)
"""
from pathlib import Path
from urllib.request import urlretrieve

URL_QUIJOTE = "https://www.gutenberg.org/cache/epub/2000/pg2000.txt"


def quijote(archivo="quijote.txt"):
    """Devuelve el texto del Quijote, sin el encabezado ni el pie de Project Gutenberg.
    La primera vez lo descarga y lo guarda en `archivo`."""
    if not Path(archivo).exists():
        urlretrieve(URL_QUIJOTE, archivo)
    crudo = open(archivo, encoding="utf-8").read()
    texto = crudo[crudo.index("*** START"):crudo.index("*** END")]
    return texto[texto.index("\n") + 1:]
