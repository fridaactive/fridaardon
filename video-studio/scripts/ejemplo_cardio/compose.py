import json, os, sys
sys.path.insert(0, '/home/user/fridaardon/video-studio/scripts')
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import enfasis
W, H, FPS = 1080, 1920, 30
D = 31.733
TR = '/tmp/claude-0/-home-user-fridaardon/594e97b7-6785-521b-a31a-141cacec037b/scratchpad/cardio/tr/'
SUBF = ImageFont.truetype('/home/user/fridaardon/video-studio/fonts/ArchivoBlack.ttf', 44)

# énfasis (Fraunces + Norican, amarillo)
EN = []
for frase, a, b in [("Me pasé años en la|*caminadora*", 0.08, 1.62), ("esperando un cuerpo que|*nunca llegó*", 1.72, 3.28),
                    ("Pesas como|*base*|cardio como|*complemento*", 28.35, 31.73)]:
    EN.append((enfasis.preparar(frase, "amarillo"), a, b))

# subtítulos con las palabras reales de Frida
def palabras(clip, c0, c1, g0):
    w = json.load(open(TR + clip + '.json'))
    return [(g0 + x['start'] - c0, g0 + x['end'] - c0, x['word']) for x in w if c0 - 0.05 <= x['start'] < c1]
ws = palabras('IMG_7500', 2.80, 7.15, 3.3) + palabras('IMG_7505', 2.35, 6.90, 7.3667) + palabras('IMG_7505', 8.28, 10.03, 11.9167) + palabras('IMG_7553', 5.20, 13.25, 20.3667)
fix = {'está': 'estás'}
ws = [(a, b, fix.get(t, t)) for a, b, t in ws]
# "si así más que" (7553) se escucha como "sí o sí tienes que"
out = []; i = 0
while i < len(ws):
    if ws[i][2] == 'si' and i + 3 < len(ws) and ws[i+1][2] == 'así' and ws[i+2][2] == 'más':
        out += [(ws[i][0], ws[i][1], 'sí o sí'), (ws[i+2][0], ws[i+3][1], 'tienes que')]; i += 4
    else:
        out.append(ws[i]); i += 1
ws = out
# trozos escritos a mano (no cruzan cortes), con los tiempos reales de cada palabra
PLAN = [(5, "Y OJO, QUE NO VENGO"), (7, "A DECIR QUE EL CARDIO ES MALO,"), (2, "AL CONTRARIO"),
        (6, "PERO SI QUIERES BAJAR DE PESO"), (5, "Y ESTÁS HACIENDO SOLAMENTE CARDIO,"),
        (5, "ESTÁS HACIENDO LAS COSAS MAL"),
        (5, "ASÍ QUE SI QUIERES EMPEZAR"), (4, "A BAJAR DE PESO"), (6, "Y EMPEZAR A VERTE MÁS DEFINIDA,"),
        (3, "SÍ O SÍ TIENES QUE EMPEZAR"), (4, "A LEVANTAR MÁS PESO")]
assert sum(n for n, _ in PLAN) == len(ws), (sum(n for n, _ in PLAN), len(ws), [w[2] for w in ws])
subs, k = [], 0
for n, txt in PLAN:
    grupo = ws[k:k+n]; k += n
    subs.append([grupo[0][0], grupo[-1][1] + 0.25, txt])
for i in range(len(subs) - 1):
    subs[i][1] = min(subs[i][1], subs[i+1][0])
for x in subs:
    for lim in (7.4, 13.5, 28.25):
        if x[0] < lim < x[1]: x[1] = lim
json.dump(subs, open('subs.json', 'w'), ensure_ascii=False, indent=0)

def sub_img(txt):
    w = int(SUBF.getlength(txt)) + 40; h = 90
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sh = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((w//2, 48), txt, font=SUBF, fill=(0, 0, 0, 255), anchor='mm', stroke_width=4, stroke_fill=(0, 0, 0, 255))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    d.text((w//2, 45), txt, font=SUBF, fill=(255, 255, 255, 255), anchor='mm')
    return im
SUBIMG = {s[2]: sub_img(s[2]) for s in subs}

os.makedirs('fr', exist_ok=True)
for f in range(int(D * FPS)):
    t = f / FPS
    p = f'txt/t{f:04d}.png'
    frame = Image.open(p).convert('RGBA') if os.path.exists(p) else Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for (lin, pos), a, b in EN:
        if a <= t < b:
            frame.alpha_composite(enfasis.componer(lin, pos, t - a, b - a))
    for a, b, txt in subs:
        if a <= t < b:
            im = SUBIMG[txt]
            if im.width > W - 80:
                sc = (W - 80) / im.width; im = im.resize((int(im.width*sc), int(im.height*sc)), Image.LANCZOS)
            frame.alpha_composite(im, ((W - im.width)//2, 1440))
    frame.save(f'fr/f{f:04d}.png', compress_level=1)
print('subtítulos:', len(subs))
