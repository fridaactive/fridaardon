import json, os, subprocess, sys
sys.path.insert(0, '/home/user/fridaardon/video-studio/scripts')
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import enfasis
S = '/tmp/claude-0/-home-user-fridaardon/594e97b7-6785-521b-a31a-141cacec037b/scratchpad'
D = S + '/ptm'; O = D + '/out'; SFX = S + '/portal/sfx2'
W, H, FPS = 1080, 1920, 30
TONE = "eq=contrast=1.1:saturation=1.15:gamma=0.92"
# (inicio, fin) en la base; 'voz' conserva el audio
CLIPS = [(79.1,79.55),(38.9,39.35),(13.1,13.55),(30.2,30.65),(76.2,76.65),(36.1,36.55),(67.1,69.6),
         (0.0,1.5),(2.75,4.2),(8.0,9.8),(12.8,14.5),(16.0,17.8),(19.8,21.6),(21.9,23.6),(24.7,26.6),(27.1,29.2),(29.7,31.8),(35.6,37.6),
         (38.6,40.6),(41.1,46.2,'voz'),(47.6,48.8,'voz'),(49.0,51.2),(58.0,59.9),(60.2,62.8),(64.0,65.8),(75.5,78.0),(78.4,80.6),
         (32.2,34.6),(70.2,72.4)]
os.chdir(O)
starts = []; t = 0
lst = open('l.txt', 'w')
for i, c in enumerate(CLIPS):
    a, b = c[0], c[1]; d = round(b - a, 3); starts.append(t); t += d
    out = f's{i:02d}.mov'
    zoom = ',scale=1240:2204,crop=1080:1920' if i < 6 else ''
    if len(c) > 2:
        cmd = f'ffmpeg -nostdin -v error -y -ss {a} -t {d} -i {D}/base.mov -vf "{TONE},scale=1080:1920,fps=30,format=yuv420p" -af "highpass=f=90,afade=t=in:d=0.04,afade=t=out:st={d-0.05}:d=0.05" -ar 44100 -ac 2 -c:v libx264 -preset fast -crf 8 -pix_fmt yuv420p -c:a pcm_s16le {out}'
    else:
        cmd = f'ffmpeg -nostdin -v error -y -ss {a} -t {d} -i {D}/base.mov -f lavfi -t {d} -i anullsrc=r=44100:cl=stereo -vf "{TONE},scale=1080:1920{zoom},fps=30,format=yuv420p" -map 0:v -map 1:a -c:v libx264 -preset fast -crf 8 -pix_fmt yuv420p -c:a pcm_s16le {out}'
    subprocess.run(cmd, shell=True, check=True)
    lst.write(f"file '{O}/{out}'\n")
lst.close()
DUR = t
subprocess.run(f'ffmpeg -nostdin -v error -y -f concat -safe 0 -i l.txt -c:v copy -af loudnorm=I=-16:TP=-1.5 -c:a pcm_s16le -ar 44100 base.mov', shell=True, check=True)
json.dump({'starts': starts, 'dur': DUR}, open('tiempos.json', 'w'))
st = lambda i: starts[i]

# ---- textos ----
FONT = '/tmp/claude-0/-home-user-fridaardon/594e97b7-6785-521b-a31a-141cacec037b/scratchpad/fonts/Montserrat%5Bwght%5D.ttf'
f_sub = ImageFont.truetype(FONT, 58); f_sub.set_variation_by_name('Bold')
f_emo = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)
# voz del review: tiempos reales de las palabras
tr = json.load(open(D + '/tr.json'))
def tvoz(word):
    for x in tr:
        if x['word'] == word and 41 <= x['start'] <= 49:
            return x
SUBS = [  # (inicio, fin, texto)
 (st(7)+0.05, st(9)-0.05, "Empiezo estudiando y trabajando"),
 (st(9)+0.1, st(12)-0.05, "Después, a entrenar"),
 (st(12)+0.05, st(14)-0.05, "En días así necesito comer algo saludable, pero que de verdad me nutra"),
 (st(14)+0.05, st(17)-0.05, "Así que paso por mi almuerzo a Productos Tu Madre"),
 (st(17)+0.05, st(18)-0.05, "Y para acompañar, mi shake"),
]
c13 = CLIPS[19][0]; c14 = CLIPS[20][0]
v = lambda w, base, s0: s0 + tvoz(w)['start'] - base
SUBS += [(v('esta', c13, st(19)), st(20), "Esta vez me pedí el Santorini bowl"),
         (st(20) + 0.05, st(21) - 0.05, "¡Qué rico!")]
SUBS += [(st(21)+0.05, st(24)-0.05, "Después, sesión a domicilio con mi clienta"),
         (st(24)+0.05, st(27)-0.05, "Y cierro el día con mi clase de ciclo"),
         (st(27)+0.05, st(28)-0.05, "Si pasas por Tu Madre, pide el Santorini bowl y después me cuentas"),
         (st(28)+0.1, DUR, "Nos vemos")]
# la palabra "Santorini" del review lleva brillo
t_santorini = v('santorini', c13, st(19))

def es_emoji(ch): return ord(ch) > 0x2500
def ancho(pal):
    w = 0
    for ch in pal: w += (f_emo.getlength(ch) * 58 / 109 * 0.95) if es_emoji(ch) else f_sub.getlength(ch)
    return w
def lineas(texto, maxw=880):
    out, cur = [], []
    for p in texto.split():
        if cur and ancho(' '.join(cur + [p])) > maxw: out.append(cur); cur = []
        cur.append(p)
    if cur: out.append(cur)
    return out
CACHE = {}
def palabra_img(p):
    if p in CACHE: return CACHE[p]
    w = int(ancho(p)) + 30; h = 100
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = 10
    for ch in p:
        if es_emoji(ch):
            e = Image.new('RGBA', (140, 140), (0, 0, 0, 0)); ImageDraw.Draw(e).text((0, 0), ch, font=f_emo, embedded_color=True)
            e = e.crop(e.getbbox()) if e.getbbox() else e
            sc = 52 / max(1, e.height); e = e.resize((max(1, int(e.width * sc)), max(1, int(e.height * sc))), Image.LANCZOS)
            im.alpha_composite(e, (int(x), 28)); x += e.width + 4
        else:
            d.text((x, 70), ch, font=f_sub, fill=(255, 255, 255, 255), anchor='ls'); x += f_sub.getlength(ch)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(im.getchannel('A').filter(ImageFilter.GaussianBlur(6)).point(lambda a: int(a * .75)))
    full = Image.new('RGBA', im.size, (0, 0, 0, 0)); full.alpha_composite(sh, (2, 4)); full.alpha_composite(im)
    CACHE[p] = full; return full
# preparar posiciones y tiempos de cada palabra
PLAN = []
for a, b, texto in SUBS:
    ls = lineas(texto); n = sum(len(l) for l in ls)
    dt = min(0.22, max(0.08, (b - a) * 0.55 / max(1, n)))
    y0 = 1150 - (len(ls) * 78) // 2; k = 0; items = []
    for li, l in enumerate(ls):
        tot = sum(ancho(p) for p in l) + 18 * (len(l) - 1); x = (W - tot) / 2
        for p in l:
            items.append((a + k * dt, int(x) - 10, y0 + li * 78 - 20, p)); x += ancho(p) + 18; k += 1
    PLAN.append((a, b, items))
f_card = ImageFont.truetype(FONT, 50); f_card.set_variation_by_name('ExtraBold')
CARDS_OFF = [(st(7), st(9) - 0.1, '☀️', 'Mañana: estudio y trabajo'), (st(9), st(12) - 0.1, '💪', 'Mi entreno'),
         (st(12), st(19) - 0.1, '🥗', 'Almuerzo en Tu Madre'), (st(21), st(24) - 0.1, '🏠', 'Clienta a domicilio'),
         (st(24), st(27) - 0.1, '🚴', '6:00 p. m. · Clase de ciclo')]
def card_img(emo, txt):
    e = Image.new('RGBA', (140, 140), (0, 0, 0, 0)); ImageDraw.Draw(e).text((0, 0), emo, font=f_emo, embedded_color=True)
    e = e.crop(e.getbbox()); sc = 50 / e.height; e = e.resize((int(e.width * sc), 50), Image.LANCZOS)
    tw = int(f_card.getlength(txt)); w = 36 + e.width + 16 + tw + 40; h = 96
    im = Image.new('RGBA', (w + 20, h + 24), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((10, 16, w + 10, h + 16), radius=48, fill=(0, 0, 0, 120))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    d.rounded_rectangle((10, 10, w + 10, h + 10), radius=48, fill=(28, 85, 229, 255))
    im.alpha_composite(e, (46, 10 + (h - 50) // 2))
    d.text((46 + e.width + 16, 10 + h // 2), txt, font=f_card, fill=(255, 255, 255, 255), anchor='lm')
    return im
CARDS = []  # Frida: el cuadro azul repite lo que dice el subtítulo
CARD_IMG = []
EN = (enfasis.preparar("Un día conmigo siendo|*fitness coach*", "amarillo"), st(6) + 0.05, st(7) - 0.05)
os.makedirs('fr', exist_ok=True)
for fi in range(int(DUR * FPS)):
    t = fi / FPS; frame = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    (lin, pos), a, b = EN
    if a <= t < b: frame.alpha_composite(enfasis.componer(lin, pos, t - a, b - a))
    for (a, b, _, _), im0 in zip(CARDS, CARD_IMG):
        if not (a <= t < b): continue
        p = (t - a) * FPS / 9; sc = 0 if p <= 0 else (0.5 + 0.7 * p / 0.6 if p < 0.6 else (1.2 - 0.2 * (p - 0.6) / 0.4 if p < 1 else 1))
        fo = min(1, (b - t) * FPS / 5)
        if sc <= 0: continue
        im = im0.resize((max(1, int(im0.width * sc)), max(1, int(im0.height * sc))), Image.LANCZOS) if sc != 1 else im0.copy()
        if fo < 1: im.putalpha(im.getchannel('A').point(lambda v: int(v * fo)))
        cx, cy = 60 + im0.width // 2, 300 + im0.height // 2
        frame.alpha_composite(im, (cx - im.width // 2, cy - im.height // 2))
    for a, b, items in PLAN:
        if not (a <= t < b): continue
        fo = min(1, (b - t) * FPS / 4)
        for ta, x, y, p in items:
            if t < ta: continue
            pr = min(1, (t - ta) * FPS / 4)
            im = palabra_img(p)
            if pr < 1 or fo < 1:
                im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * pr * fo)))
            frame.alpha_composite(im, (x, y + int((1 - pr) * 10)))
    frame.save(f'fr/f{fi:04d}.png', compress_level=1)
# sonidos (los favoritos de Frida, pocos)
ev = [('subida', max(0, st(6) - 1.6), 0.7), ('destello_magico', st(6) + 0.08, 0.6), ('whoosh_grave', st(9) - 0.15, 0.8), ('whoosh_grave', st(12) - 0.15, 0.8),
      ('brillo_doble', t_santorini, 0.55), ('whoosh_grave', st(21) - 0.15, 0.8), ('whoosh_grave', st(24) - 0.15, 0.8),
      ('cierre', st(28) + 0.1, 0.65)] + [('pop_suave', a + 0.05, 0.6) for a, _, _, _ in CARDS]
json.dump(ev, open('sfx.json', 'w'))
ins = '-i base.mov'; fl = ''; mix = '[0:a]'
for n, (nm, tt, vol) in enumerate(ev, 1):
    ins += f' -i {SFX}/{nm}.wav'; ms = int(tt * 1000); fl += f'[{n}:a]volume={vol},adelay={ms}|{ms},aformat=channel_layouts=stereo[s{n}];'; mix += f'[s{n}]'
n = len(ev) + 1
cmd = (f'ffmpeg -nostdin -v error -y {ins} -framerate 30 -i fr/f%04d.png -filter_complex "{fl}{mix}amix=inputs={n}:normalize=0:duration=first,alimiter=limit=0.9[a];[0:v][{n}:v]overlay=0:0:format=auto,format=yuv420p[v]" '
       f'-map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 14 -profile:v high -tune film -x264-params aq-mode=3 -r 30 -c:a aac -b:a 256k -movflags +faststart {D}/reel_un_dia_conmigo_v5.mp4')
subprocess.run(cmd, shell=True, check=True)
print('duración', round(DUR, 2), 'subtítulos', len(SUBS), 'sonidos', len(ev))
