# Genera dev/prueba-modo-entreno.html: el portal con datos de prueba (sin
# Firebase real) y la rutina de Jocelyn, para probar el modo entreno.
# Uso: python3 dev/hacer-prueba-modo-entreno.py
import json, re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
html = (root / 'index.html').read_text()
mock = (root / 'dev/mock-firebase.js').read_text()
rut = json.loads((root / 'contenido/rutinas/clientes/jocelyn.json').read_text())
n = 0
for di, d in enumerate(rut['days']):
    d['id'] = 'd%d' % di
    for bi, b in enumerate(d['blocks']):
        b['id'] = 'b%d%d' % (di, bi)
        for e in b['exercises']:
            e['id'] = 'e%d' % n; n += 1
html = re.sub(r'<script src="https://www\.gstatic\.com/firebasejs/[^"]+"></script>\n?', '', html)
html = re.sub(r'<script src="https://cdn\.jsdelivr\.net/npm/@emailjs[^"]+"></script>\n?', '', html)
inject = ('<base href="/">\n<meta name="robots" content="noindex">\n<script>\n' + mock +
  '\nwindow.__MOCK_DATA__.rutinas["demo-client"] = ' + json.dumps(rut, ensure_ascii=False) + ';\n'
  'Object.defineProperty(window, "firebase", { value: window.firebase, writable: false });\n'
  'window.emailjs = { init: function(){}, send: function(){ return Promise.resolve(); } };\n'
  'window.addEventListener("load", function(){ setTimeout(function(){ try { showTab("tab-rutina"); } catch(e){} }, 1500); });\n</script>\n')
html = html.replace('<head>', '<head>\n' + inject, 1)
html = html.replace('<title>', '<title>PRUEBA · ', 1)
(root / 'dev/prueba-modo-entreno.html').write_text(html)
print('ok', len(html))
