"""Biblioteca de sonidos del Estudio Frida Active, sintetizados desde cero (originales, sin derechos de terceros).

Uso: python3 sonidos.py carpeta_salida
Genera un .wav (44.1 kHz) por sonido y catalogo.json con nombre, categoría y descripción.
Los ids de sonidos anteriores (whoosh_suave, pop, brillo, etc.) se mantienen para no perder los votos.
"""
import json
import os
import sys

import numpy as np
from scipy import signal
from scipy.io import wavfile

SR = 44100
rng = np.random.default_rng(7)


def t_(d):
    return np.arange(int(SR * d)) / SR


def ruido(d, color="white"):
    n = rng.standard_normal(int(SR * d))
    if color == "pink":
        b, a = [0.049922035, -0.095993537, 0.050612699, -0.004408786], [1, -2.494956002, 2.017265875, -0.522189400]
        n = signal.lfilter(b, a, n)
    if color == "brown":
        n = np.cumsum(n)
        n = n - signal.savgol_filter(n, 2001 if len(n) > 2001 else (len(n) // 2) * 2 - 1, 2)
    return n / (np.max(np.abs(n)) + 1e-9)


def banda(x, lo, hi, orden=2):
    lo, hi = max(lo, 20), min(hi, SR / 2 - 100)
    sos = signal.butter(orden, [lo, hi], btype="band", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


def barrido(x, f0, f1, ancho=0.9, pasos=60):
    """Filtro pasa-banda cuyo centro va de f0 a f1 (efecto de aire que pasa)."""
    n = len(x)
    out = np.zeros(n)
    win = np.hanning(2 * (n // pasos) + 1)
    hop = n // pasos
    for i in range(pasos):
        c = f0 * (f1 / f0) ** (i / (pasos - 1))
        seg = banda(x, c * (1 - ancho / 2), c * (1 + ancho / 2))
        a, b = max(0, i * hop - hop), min(n, i * hop + hop + 1)
        w = win[: b - a] if len(win) >= b - a else np.ones(b - a)
        out[a:b] += seg[a:b] * w
    return out


def env_ar(n, ataque, caida, curva=2.0):
    t = np.linspace(0, 1, n)
    pico = ataque / (ataque + caida)
    e = np.where(t < pico, (t / pico) ** curva, ((1 - t) / (1 - pico)) ** curva)
    return e


def reverb(x, cola=0.8, mezcla=0.3):
    ir = ruido(cola) * np.exp(-t_(cola) * 6 / cola)
    ir = banda(ir, 300, 9000)
    w = signal.fftconvolve(x, ir)[: len(x) + int(SR * cola)]
    seco = np.concatenate([x, np.zeros(len(w) - len(x))])
    return (1 - mezcla) * seco + mezcla * w / (np.max(np.abs(w)) + 1e-9) * np.max(np.abs(x))


def campana(f, d, decay=4.0, parciales=((1, 1), (2.76, .4), (5.4, .2), (8.9, .1))):
    t = t_(d)
    s = sum(a * np.sin(2 * np.pi * f * k * t) * np.exp(-t * decay * (1 + k / 3)) for k, a in parciales)
    return s * np.minimum(1, t * 400)


def mezclar(*partes):
    n = max(int(inicio * SR) + len(p) for inicio, p in partes)
    out = np.zeros(n)
    for inicio, p in partes:
        i = int(inicio * SR)
        out[i:i + len(p)] += p[: n - i]
    return out


def norm(x, pico=0.85):
    return x / (np.max(np.abs(x)) + 1e-9) * pico


SONIDOS = []


def sonido(id_, nom, cat, desc):
    def dec(f):
        SONIDOS.append((id_, nom, cat, desc, f))
        return f
    return dec


# ---------- Transiciones (whoosh) ----------
@sonido("whoosh_suave", "Whoosh suave", "Transiciones", "Aire que pasa, el clásico.")
def _():
    x = barrido(ruido(0.5, "pink"), 500, 3000)
    return x * env_ar(len(x), 0.55, 0.45)


@sonido("whoosh_rapido", "Whoosh rápido", "Transiciones", "Corto y agudo, con energía.")
def _():
    x = barrido(ruido(0.28), 1200, 6000)
    return x * env_ar(len(x), 0.5, 0.5)


@sonido("whoosh_grave", "Whoosh grave", "Transiciones", "Profundo, para el gym o el carro.")
def _():
    x = barrido(ruido(0.7, "pink"), 150, 900, ancho=1.2)
    return x * env_ar(len(x), 0.55, 0.45)


@sonido("whoosh_largo", "Whoosh largo", "Transiciones", "Lento y elegante, para cambios de lugar.")
def _():
    x = barrido(ruido(1.1, "pink"), 300, 2500)
    return reverb(x * env_ar(len(x), 0.6, 0.4, 1.6), 0.6, 0.25)


@sonido("whoosh_doble", "Whoosh doble", "Transiciones", "Ida y vuelta, para dos cortes seguidos.")
def _():
    a = barrido(ruido(0.3, "pink"), 600, 3500)
    a = a * env_ar(len(a), 0.5, 0.5)
    return mezclar((0, a), (0.22, a * 0.8))


@sonido("whoosh_eco", "Whoosh con eco", "Transiciones", "Whoosh con cola espaciosa, más cinematográfico.")
def _():
    x = barrido(ruido(0.45, "pink"), 400, 4000)
    return reverb(x * env_ar(len(x), 0.6, 0.4), 1.3, 0.45)


@sonido("whoosh_sube", "Whoosh que sube", "Transiciones", "El aire sube de tono, anticipa algo.")
def _():
    x = barrido(ruido(0.8, "pink"), 200, 6000, pasos=80)
    return x * env_ar(len(x), 0.85, 0.15, 1.5)


@sonido("whoosh_baja", "Whoosh que baja", "Transiciones", "El aire baja de tono, para cerrar una escena.")
def _():
    x = barrido(ruido(0.7, "pink"), 5000, 250, pasos=80)
    return x * env_ar(len(x), 0.2, 0.8, 1.6)


@sonido("swipe_tela", "Swipe de tela", "Transiciones", "Como mover ropa o una toalla rápido.")
def _():
    x = banda(ruido(0.22), 1500, 9000) * (0.6 + 0.4 * np.sin(2 * np.pi * 45 * t_(0.22)))
    return x * env_ar(len(x), 0.35, 0.65)


@sonido("viento", "Ráfaga de viento", "Transiciones", "Suave y natural, para tomas al aire libre.")
def _():
    x = barrido(ruido(1.4, "brown"), 200, 700, ancho=1.0, pasos=40)
    return x * env_ar(len(x), 0.5, 0.5, 1.3)


# ---------- Palabra clave: pops y clics ----------
@sonido("pop", "Pop", "Palabra clave", "Pop con brillo, el de las mayúsculas azules.")
def _():
    t = t_(0.25)
    return 0.55 * np.sin(2 * np.pi * t * (450 + 3200 * np.exp(-t * 40))) * np.exp(-t * 18)


@sonido("pop_suave", "Pop suave", "Palabra clave", "Más discreto y grave.")
def _():
    t = t_(0.2)
    return 0.5 * np.sin(2 * np.pi * t * (300 + 1200 * np.exp(-t * 60))) * np.exp(-t * 25)


@sonido("burbuja", "Burbuja", "Palabra clave", "Pop redondito que sube, tierno.")
def _():
    t = t_(0.18)
    f = 500 + 1400 * (1 - np.exp(-t * 30))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 22) * np.minimum(1, t * 300)


@sonido("gota", "Gota de agua", "Palabra clave", "Gota limpia, va con temas de hidratación o comida.")
def _():
    t = t_(0.3)
    f = 900 + 1800 * np.exp(-t * 35)
    return np.sin(2 * np.pi * np.cumsum(f[::-1][::-1]) / SR) * np.exp(-t * 14) * np.minimum(1, t * 500)


@sonido("clic", "Clic", "Palabra clave", "Clic seco, como tocar la pantalla.")
def _():
    x = banda(ruido(0.05), 2000, 8000) * np.exp(-t_(0.05) * 120)
    return x + 0.4 * np.sin(2 * np.pi * 2500 * t_(0.05)) * np.exp(-t_(0.05) * 150)


@sonido("chasquido", "Chasquido", "Palabra clave", "Snap de dedos, para un ¡listo!")
def _():
    x = banda(ruido(0.12), 1800, 6000) * np.exp(-t_(0.12) * 60)
    return reverb(x, 0.25, 0.2)


@sonido("tecla", "Tecla", "Palabra clave", "Tecla de computadora, para escenas de trabajo.")
def _():
    a = banda(ruido(0.06), 1500, 7000) * np.exp(-t_(0.06) * 90)
    b = banda(ruido(0.05), 800, 4000) * np.exp(-t_(0.05) * 110) * 0.6
    return mezclar((0, a), (0.045, b))


@sonido("boing", "Boing", "Palabra clave", "Rebote divertido, para algo gracioso.")
def _():
    t = t_(0.5)
    f = 180 + 120 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 4) + 80 * t
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5) * np.minimum(1, t * 200)


@sonido("tic", "Tic", "Palabra clave", "Clic cortito para listas o números.")
def _():
    t = t_(0.08)
    return 0.4 * np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 90)


# ---------- Palabra clave: brillos ----------
@sonido("brillo", "Brillo", "Brillos", "Campanita suave para la cursiva crema.")
def _():
    t = t_(0.7)
    return 0.16 * (np.sin(2 * np.pi * 1318 * t) + 0.7 * np.sin(2 * np.pi * 1975 * t) + 0.5 * np.sin(2 * np.pi * 2637 * t)) * np.exp(-t * 6) * np.minimum(1, t * 60)


@sonido("brillo_doble", "Brillo doble", "Brillos", "Dos notas, un poco más alegre.")
def _():
    return mezclar((0, campana(1568, 0.7, 7, ((1, 1),))), (0.09, campana(2093, 0.7, 6, ((1, 1),))))


@sonido("destello_magico", "Destello mágico", "Brillos", "Campanitas que suben, como polvo de estrellas.")
def _():
    notas = [1047, 1319, 1568, 2093, 2637, 3136]
    return reverb(mezclar(*[(i * 0.055, campana(f, 0.6, 7) * 0.5) for i, f in enumerate(notas)]), 0.9, 0.35)


@sonido("estrella", "Estrella", "Brillos", "Brillo que vibra, para algo especial.")
def _():
    t = t_(1.0)
    s = sum(np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) for f in (2637, 3136, 3951, 4699))
    return s * (0.5 + 0.5 * np.sin(2 * np.pi * 14 * t)) * np.exp(-t * 3.5) * np.minimum(1, t * 30)


@sonido("ding", "Ding", "Brillos", "Notificación limpia, para un dato importante.")
def _():
    return reverb(campana(1760, 1.0, 3.5, ((1, 1), (2, .25), (3, .1))), 0.5, 0.2)


@sonido("campana", "Campana", "Brillos", "Campana más grave y cálida.")
def _():
    return reverb(campana(660, 1.6, 2.2), 0.8, 0.25)


@sonido("arpa", "Arpa que sube", "Brillos", "Arpegio rápido, para un antes y después.")
def _():
    notas = [523, 659, 784, 1047, 1319, 1568, 2093]
    pl = lambda f: np.sin(2 * np.pi * f * t_(0.8)) * np.exp(-t_(0.8) * 5) * np.minimum(1, t_(0.8) * 800)
    return reverb(mezclar(*[(i * 0.045, pl(f) * 0.4) for i, f in enumerate(notas)]), 0.8, 0.3)


# ---------- Impactos ----------
@sonido("golpe_grave", "Golpe grave", "Impactos", "Boom profundo, para una frase fuerte.")
def _():
    t = t_(0.9)
    s = np.sin(2 * np.pi * np.cumsum(45 + 90 * np.exp(-t * 18)) / SR) * np.exp(-t * 5)
    return s + 0.2 * banda(ruido(0.9), 100, 800) * np.exp(-t * 25)


@sonido("golpe_suave", "Golpe suave", "Impactos", "Thud apagado, sutil.")
def _():
    t = t_(0.35)
    return np.sin(2 * np.pi * np.cumsum(70 + 60 * np.exp(-t * 30)) / SR) * np.exp(-t * 14)


@sonido("pesa", "Pesa metálica", "Impactos", "Clank de metal, como un disco de pesas.")
def _():
    t = t_(0.9)
    s = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, a, d in ((523, 1, 6), (1371, .6, 8), (2290, .4, 10), (3610, .25, 12)))
    return s + 0.5 * banda(ruido(0.9), 2000, 9000) * np.exp(-t * 60)


@sonido("aplauso", "Aplauso", "Impactos", "Una palmada, para celebrar.")
def _():
    x = banda(ruido(0.2), 700, 5000) * np.exp(-t_(0.2) * 35)
    return reverb(x, 0.3, 0.2)


@sonido("cierre", "Cierre", "Impactos", "Golpe grave con brillo, para terminar el video.")
def _():
    return mezclar((0, norm(SONIDOS_F["golpe_grave"]()) * 0.9), (0.02, norm(campana(1047, 1.2, 3)) * 0.3))


# ---------- Tensión y ritmo ----------
@sonido("subida", "Subida", "Tensión y ritmo", "Sube y sube antes de revelar algo.")
def _():
    t = t_(1.6)
    tono = np.sin(2 * np.pi * np.cumsum(200 + 900 * (t / 1.6) ** 2) / SR) * 0.3
    aire = barrido(ruido(1.6, "pink"), 300, 7000, pasos=80)
    return (tono + aire) * (t / 1.6) ** 2


@sonido("latido", "Latido", "Tensión y ritmo", "Dos latidos, para el cardio o un momento intenso.")
def _():
    t = t_(0.18)
    b = np.sin(2 * np.pi * np.cumsum(55 + 40 * np.exp(-t * 30)) / SR) * np.exp(-t * 22)
    return mezclar((0, b), (0.22, b * 0.75), (0.85, b), (1.07, b * 0.75))


@sonido("tictac", "Tic-tac", "Tensión y ritmo", "Reloj, para hablar del tiempo o la rutina.")
def _():
    a = np.sin(2 * np.pi * 2200 * t_(0.04)) * np.exp(-t_(0.04) * 160)
    b = np.sin(2 * np.pi * 1700 * t_(0.04)) * np.exp(-t_(0.04) * 160)
    return mezclar(*[(i * 0.5, a if i % 2 == 0 else b) for i in range(4)])


@sonido("camara", "Cámara de fotos", "Tensión y ritmo", "Obturador, para fotos o un antes y después.")
def _():
    a = banda(ruido(0.05), 1500, 8000) * np.exp(-t_(0.05) * 90)
    b = banda(ruido(0.07), 800, 6000) * np.exp(-t_(0.07) * 70)
    return mezclar((0, a), (0.07, b))


SONIDOS_F = {s[0]: s[4] for s in SONIDOS}


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    cat = []
    for id_, nom, c, desc, f in SONIDOS:
        x = norm(np.asarray(f(), dtype=float), 0.8)
        fade = min(len(x), int(0.01 * SR))
        x[-fade:] *= np.linspace(1, 0, fade)
        wavfile.write(os.path.join(out, id_ + ".wav"), SR, (x * 32767).astype(np.int16))
        cat.append({"id": id_, "nom": nom, "cat": c, "desc": desc})
    json.dump(cat, open(os.path.join(out, "catalogo.json"), "w"), ensure_ascii=False, indent=1)
    print(len(cat), "sonidos")


if __name__ == "__main__":
    main()
