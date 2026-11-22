"""Textos v4 (inspirado en la referencia): frase base pequeña + palabra clave marcada.

Cada línea es una lista de segmentos [estilo, texto, (retraso opcional)]:
  base  -> Archivo Black blanca, pequeña. Aparece con un desvanecido suave al inicio del bloque.
  serif -> Instrument Serif cursiva crema, más grande. Aparece con 'pop' (y lleva sonido).
  bold  -> Archivo Black azul con borde blanco, más grande. Aparece con 'pop' (y lleva sonido).
Escribe también events.txt con el momento de cada palabra marcada, para poner su sonido.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
WHITE, CREAM, BLUE, NAVY = (255, 255, 255, 255), (245, 236, 203, 255), (28, 85, 229, 255), (13, 27, 62, 255)


def seg_img(text, font, fill, stroke=0, stroke_fill=None):
    ascent, descent = font.getmetrics()
    w = int(font.getlength(text)) + 2 * stroke + 40
    h = ascent + descent + 40
    base = 20 + ascent
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((22 + stroke, base + 4), text, font=font, fill=(0, 0, 0, 255), anchor="ls",
                            stroke_width=stroke + 3, stroke_fill=(0, 0, 0, 255))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)))
    ImageDraw.Draw(img).text((20 + stroke, base), text, font=font, fill=fill, anchor="ls",
                             stroke_width=stroke, stroke_fill=stroke_fill)
    return img, base


def pop(p):
    if p <= 0:
        return 0.0
    if p >= 1:
        return 1.0
    return 0.5 + 0.7 * (p / 0.6) if p < 0.6 else 1.2 - 0.2 * ((p - 0.6) / 0.4)


def with_alpha(im, a):
    if a >= 1:
        return im
    im = im.copy()
    im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
    return im


def main(spec_path, out_dir, events_path):
    spec = json.load(open(spec_path))
    fonts = spec["fonts"]
    total = int(round(spec["duration"] * FPS))
    os.makedirs(out_dir, exist_ok=True)
    events, blocks = [], []

    for b in spec["blocks"]:
        size = b.get("size", 50)
        styles = {
            "base": (ImageFont.truetype(fonts["base"], size), WHITE, 0, None),
            "serif": (ImageFont.truetype(fonts["serif"], int(size * 1.75)), CREAM, 0, None),
            "bold": (ImageFont.truetype(fonts["base"], int(size * 1.3)), BLUE, 5, WHITE),
        }
        items, y = [], b.get("y", 380)
        for line in b["lines"]:
            rendered = []
            for seg in line:
                kind, text = seg[0], seg[1]
                f, fill, st, sf = styles[kind]
                im, base = seg_img(text, f, fill, st, sf)
                delay = seg[2] if len(seg) > 2 else (0.0 if kind == "base" else 0.3)
                rendered.append([kind, im, base, delay])
            gap = int(size * 0.25) - 40
            line_w = sum(r[1].width for r in rendered) + gap * (len(rendered) - 1)
            max_base = max(r[2] for r in rendered)
            x = (W - line_w) // 2
            for kind, im, base, delay in rendered:
                items.append((kind, im, x, y + (max_base - base), delay))
                if kind != "base":
                    events.append((kind, round(b["start"] + delay, 3)))
                x += im.width + gap
            tall = max(r[1].height for r in rendered)
            y += int(tall * 0.62)
        blocks.append({"start": b["start"], "end": b["end"], "items": items})

    for f in range(total):
        t = f / FPS
        frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for blk in blocks:
            if not (blk["start"] <= t < blk["end"]):
                continue
            fade_out = min(1.0, (blk["end"] - t) * FPS / 5)
            for kind, im, x, y, delay in blk["items"]:
                local = (t - blk["start"] - delay) * FPS
                if kind == "base":
                    p = min(1.0, max(0.0, local / 6))
                    if p <= 0:
                        continue
                    frame.alpha_composite(with_alpha(im, p * fade_out), (x, y + int((1 - p) * 18)))
                else:
                    p = local / 8
                    s = pop(p)
                    if s <= 0:
                        continue
                    sw, sh = max(1, int(im.width * s)), max(1, int(im.height * s))
                    sc = with_alpha(im.resize((sw, sh), Image.LANCZOS), min(1.0, p * 3) * fade_out)
                    frame.alpha_composite(sc, (x + im.width // 2 - sw // 2, y + im.height // 2 - sh // 2))
        frame.save(os.path.join(out_dir, f"t{f:04d}.png"), compress_level=1)

    with open(events_path, "w") as fh:
        for kind, t in events:
            fh.write(f"{kind} {t}\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
