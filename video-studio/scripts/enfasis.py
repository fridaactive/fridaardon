"""Frase de énfasis: combinación de serifa gruesa y suave (Fraunces) + cursiva de pincel (Mr Dafoe).

Inspirada en la referencia "Make fitness Reels that everyone Copies" que le encantó a Frida.
Se usa para frases importantes: portada, gancho, cierre y fotos.

Las líneas se escriben separadas por "|". Una línea entre asteriscos va en cursiva de pincel:
    "Pesas como|*base*|cardio como|*complemento*"

Uso:
    python3 enfasis.py "Pesas como|*base*|cardio como|*complemento*" salida.png
    python3 enfasis.py "..." salida.png --colores amarillo --foto foto.jpg     # texto sobre una foto
    python3 enfasis.py "..." salida.mov --video 3                               # animación con transparencia (3 s)

Colores: crema (todo crema, como la referencia), amarillo (serifa blanca + cursiva amarilla),
azul (serifa crema + cursiva azul con borde blanco).
"""
import argparse
import os
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
SERIF = os.path.join(AQUI, "..", "fonts", "Fraunces.ttf")
# Cursivas que le gustaron a Frida (nombre: archivo, tamaño). Mr Dafoe la descartó: "parece escrita de carta".
CURSIVAS = {
    "norican": ("Norican.ttf", 205),
    "playball": ("Playball.ttf", 205),
}
SCRIPT = os.path.join(AQUI, "..", "fonts", "Norican.ttf")
W, H, FPS = 1080, 1920, 30

CREMA, BLANCO, AMARILLO, AZUL = (245, 236, 203), (255, 255, 255), (247, 214, 77), (28, 85, 229)
COLORES = {
    "crema": ((240, 233, 215), (240, 233, 215), None),
    "amarillo": (BLANCO, AMARILLO, None),
    "azul": (CREMA, AZUL, BLANCO),
}

# Reglas de diseño sacadas de la referencia:
TAM_SERIF = 165        # serifa grande, minúsculas con la primera en mayúscula
EJES_SERIF = [48, 720, 100, 0]  # Fraunces: tamaño óptico 48, peso 720, suavidad 100 (puntas redondas), sin "wonky"
TRACKING = -5          # letras de la serifa un poco más juntas
TAM_SCRIPT = 175       # la cursiva queda del alto de la serifa
ANCHO_MAX = 920        # nunca tocar los bordes (deja margen para la interfaz de Instagram)
PASO_SERIF = 128       # interlineado muy apretado: las líneas casi se tocan
PASO_SCRIPT = 128
GIRO_SCRIPT = 3        # la cursiva sube apenas hacia la derecha y sus trazos se cruzan con la serifa


def serif(tam):
    f = ImageFont.truetype(SERIF, tam)
    f.set_variation_by_axes(EJES_SERIF)
    return f


def ancho_serif(texto, f):
    return sum(f.getlength(c) for c in texto) + TRACKING * (len(texto) - 1)


def capa_linea(texto, es_script, color_s, color_c, borde):
    """Dibuja una línea (con su sombra) en una capa transparente."""
    if es_script:
        tam = TAM_SCRIPT
        while ImageFont.truetype(SCRIPT, tam).getlength(texto) > ANCHO_MAX:
            tam -= 10
        fuente, color = ImageFont.truetype(SCRIPT, tam), color_c
    else:
        tam = TAM_SERIF
        while ancho_serif(texto, serif(tam)) > ANCHO_MAX:
            tam -= 6
        fuente, color = serif(tam), color_s
    w, h = int(fuente.getlength(texto)) + 160, 420
    capa = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    if es_script:
        extra = {"stroke_width": 5, "stroke_fill": borde} if borde else {}
        d.text((w // 2, h // 2), texto, font=fuente, fill=color, anchor="mm", **extra)
    else:
        x = w / 2 - ancho_serif(texto, fuente) / 2
        for letra in texto:                       # letra por letra para juntar el espaciado
            d.text((x, h // 2), letra, font=fuente, fill=color, anchor="lm")
            x += fuente.getlength(letra) + TRACKING
    alfa = capa.split()[3].filter(ImageFilter.GaussianBlur(8)).point(lambda a: int(a * 0.45))
    sombra = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sombra.putalpha(alfa)
    if es_script:
        capa = capa.rotate(GIRO_SCRIPT, resample=Image.BICUBIC)
        sombra = sombra.rotate(GIRO_SCRIPT, resample=Image.BICUBIC)
    final = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    final.alpha_composite(sombra, (3, 6))
    final.alpha_composite(capa)
    return final


def preparar(frase, colores):
    color_s, color_c, borde = COLORES[colores]
    lineas = []
    for parte in frase.split("|"):
        parte = parte.strip()
        es_script = parte.startswith("*") and parte.endswith("*")
        lineas.append((capa_linea(parte.strip("*"), es_script, color_s, color_c, borde), es_script))
    alto = sum(PASO_SCRIPT if s else PASO_SERIF for _, s in lineas)
    y = (H - alto) // 2 + 60
    pos = []
    for capa, s in lineas:
        pos.append(((W - capa.width) // 2, y - capa.height // 2))
        y += PASO_SCRIPT if s else PASO_SERIF
    return lineas, pos


def componer(lineas, pos, t=None, dur=None):
    """Sin t: imagen fija. Con t: cada línea entra en orden, subiendo y apareciendo."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for i, ((capa, s), (x, y)) in enumerate(zip(lineas, pos)):
        if t is None:
            img.alpha_composite(capa, (x, y))
            continue
        p = min(max((t - i * 0.18) / 0.35, 0), 1)          # una línea cada 0.18 s
        fin = min(max((dur - t) / 0.25, 0), 1)             # salida suave al final
        if p <= 0:
            continue
        e = 1 - (1 - p) ** 3
        c = capa.copy()
        c.putalpha(c.split()[3].point(lambda a: int(a * e * fin)))
        img.alpha_composite(c, (x, y + int((1 - e) * 40)))
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frase")
    ap.add_argument("salida")
    ap.add_argument("--colores", default="crema", choices=COLORES)
    ap.add_argument("--cursiva", default="norican", choices=CURSIVAS)
    ap.add_argument("--foto", help="foto de fondo (se recorta a 1080x1920)")
    ap.add_argument("--video", type=float, help="duración en segundos: genera .mov con transparencia")
    a = ap.parse_args()
    global SCRIPT, TAM_SCRIPT
    archivo, TAM_SCRIPT = CURSIVAS[a.cursiva]
    SCRIPT = os.path.join(AQUI, "..", "fonts", archivo)
    lineas, pos = preparar(a.frase, a.colores)

    if a.video:
        with tempfile.TemporaryDirectory() as tmp:
            n = int(a.video * FPS)
            for f in range(n):
                componer(lineas, pos, f / FPS, a.video).save(f"{tmp}/{f:04d}.png")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{tmp}/%04d.png",
                            "-c:v", "qtrle", a.salida], check=True)
        return

    img = componer(lineas, pos)
    if a.foto:
        foto = Image.open(a.foto).convert("RGBA")
        esc = max(W / foto.width, H / foto.height)
        foto = foto.resize((int(foto.width * esc), int(foto.height * esc)))
        foto = foto.crop(((foto.width - W) // 2, (foto.height - H) // 2, (foto.width + W) // 2, (foto.height + H) // 2))
        foto.alpha_composite(img)
        img = foto.convert("RGB")
    img.save(a.salida)


if __name__ == "__main__":
    main()
