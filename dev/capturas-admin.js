/*
 * Capturas del panel de administradora en modo de prueba (solo desarrollo).
 * Uso: node dev/capturas-admin.js <carpeta_salida> [prefijo] [ancho]
 */
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..'), OUT = process.argv[2] || '/tmp', PREFIX = process.argv[3] || 'a', WIDTH = +(process.argv[4] || 1024);
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.jpg': 'image/jpeg', '.png': 'image/png', '.ttf': 'font/ttf' };
const server = http.createServer((req, res) => {
  const file = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});
(async () => {
  await new Promise(r => server.listen(8768, r));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: WIDTH, height: 1300 } });
  const errors = []; page.on('pageerror', e => errors.push(e.message)); page.on('dialog', d => d.dismiss());
  await page.route(/gstatic\.com|firebaseio\.com|cdnjs\.cloudflare\.com/, r => r.abort());
  await page.route(/fonts\.googleapis\.com/, r => r.fulfill({ contentType: 'text/css', body: "@font-face{font-family:'Archivo Black';src:url(http://localhost:8768/dev/ArchivoBlack.ttf) format('truetype');}" }));
  await page.addInitScript(fs.readFileSync(path.join(__dirname, 'mock-firebase.js'), 'utf8'));
  await page.addInitScript(() => { Object.defineProperty(window, 'firebase', { value: window.firebase, writable: false }); });
  if (process.env.FAKE_TIME && page.clock) await page.clock.install({ time: new Date(process.env.FAKE_TIME) });
  await page.goto('http://localhost:8768/admin.html'); await page.waitForTimeout(2500);
  const shot = async (n, full) => page.screenshot({ path: path.join(OUT, `${PREFIX}_${n}.png`), fullPage: !!full });
  await shot('00_login');
  for (const [n, s] of [['01_dashboard', 'dashboard'], ['02_clientes', 'clientes'], ['03_planificacion', 'planificacion'], ['04_finanzas', 'finanzas'], ['05_portal', 'portal-content']]) {
    await page.evaluate(x => showScreen(x), s); await page.waitForTimeout(900); await shot(n, true);
  }
  console.log('errores:', JSON.stringify(errors.slice(0, 8)));
  await browser.close(); server.close();
})();
