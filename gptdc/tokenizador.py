"""Tokenizador BPE (Byte Pair Encoding) — GPT desde cero, video 1.

Es el mismo algoritmo del notebook `notebooks/01_tokenizador.ipynb`, ordenado para reusarlo en los videos
siguientes:

    from gptdc.datos import quijote
    from gptdc.tokenizador import Tokenizador

    tok = Tokenizador.entrenar(quijote(), fusiones=500)   # ~1 minuto
    ids = tok.codificar("Don Quijote le mandó un mensaje a Sancho")
    tok.decodificar(ids)                                   # vuelve al texto original
    tok.piezas("Don Quijote")                              # ['D', 'on', ' Quijote']
"""
import re
from collections import Counter

# Los trozos en que se corta el texto antes de BPE (las fusiones nunca cruzan de un trozo a otro):
# un espacio opcional seguido de letras; o un espacio opcional seguido de signos; o espacios.
PATRON = r" ?\w+| ?[^\w\s]+|\s+"


def contar_pares(partes, trozos):
    """Cuántas veces aparece cada par de piezas vecinas. Cada trozo distinto se recorre una sola vez
    y suma `veces` (cuántas veces aparece en el texto)."""
    pares = Counter()
    for t, veces in trozos.items():
        p = partes[t]
        for a, b in zip(p, p[1:]):
            pares[a, b] += veces
    return pares


def fusionar(piezas, par, nueva):
    """Reemplaza cada aparición de `par` (dos piezas vecinas) por la pieza `nueva`."""
    resultado = []
    i = 0
    while i < len(piezas):
        if piezas[i:i + 2] == list(par):
            resultado.append(nueva)
            i += 2
        else:
            resultado.append(piezas[i])
            i += 1
    return resultado


class Tokenizador:
    """Un tokenizador BPE: las letras de partida y la lista de fusiones, en el orden en que se aprendieron."""

    def __init__(self, letras, fusiones):
        self.fusiones = [tuple(par) for par in fusiones]
        self.vocab = sorted(letras) + [a + b for a, b in self.fusiones]
        self.numero = {pieza: i for i, pieza in enumerate(self.vocab)}
        self._cortados = {}   # memoria: cada trozo distinto se corta una sola vez

    @classmethod
    def entrenar(cls, texto, fusiones=500):
        """Aprende `fusiones` fusiones sobre `texto`: contar pares, fusionar el más frecuente, repetir."""
        trozos = Counter(re.findall(PATRON, texto))
        partes = {t: list(t) for t in trozos}
        aprendidas = []
        for _ in range(fusiones):
            par = contar_pares(partes, trozos).most_common(1)[0][0]
            for t in partes:
                partes[t] = fusionar(partes[t], par, par[0] + par[1])
            aprendidas.append(par)
        return cls(set(texto), aprendidas)

    def piezas(self, texto):
        """Corta `texto` en tokens: trozos, letras y las fusiones aplicadas en orden.
        Un libro repite mucho los mismos trozos (" de", " la", " Sancho"): cada trozo distinto se corta una
        sola vez y se guarda, así codificar el Quijote entero tarda segundos y no minutos."""
        piezas = []
        for t in re.findall(PATRON, texto):
            if t not in self._cortados:
                p = list(t)
                for par in self.fusiones:
                    p = fusionar(p, par, par[0] + par[1])
                self._cortados[t] = p
            piezas += self._cortados[t]
        return piezas

    def codificar(self, texto):
        """El texto como lista de números (la posición de cada pieza en el vocabulario).
        Ojo: una letra que no estaba en el texto de entrenamiento (un emoji, "中") no tiene número
        — es el problema del capítulo 5 del video, que GPT resuelve empezando desde bytes."""
        return [self.numero[p] for p in self.piezas(texto)]

    def decodificar(self, numeros):
        """Vuelve de los números al texto."""
        return "".join(self.vocab[n] for n in numeros)

    def __len__(self):
        return len(self.vocab)
