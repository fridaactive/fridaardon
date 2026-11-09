/*
 * Capturas del portal de clientas en modo de prueba (solo para desarrollo).
 * Uso: node dev/capturas.js <carpeta_salida> [prefijo]
 * Sirve el repositorio en localhost, bloquea Firebase real e inyecta
 * dev/mock-firebase.js con una clienta inventada.
 */
const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const OUT = process.argv[2] || '/tmp';
const PREFIX = process.argv[3] || 'p';
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.css': 'text/css' };

const server = http.createServer((req, res) => {
  const file = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});

(async () => {
  await new Promise(r => server.listen(8766, r));
  const browser = await chromium.launch();
  const errors = [];
  const mock = fs.readFileSync(path.join(__dirname, 'mock-firebase.js'), 'utf8');
  const page = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => errors.push(e.message));
  page.on('dialog', d => d.dismiss());
  await page.route(/gstatic\.com|firebaseio\.com|googleapis\.com\/identitytoolkit|emailjs/, r => r.abort());
  // Google Fonts está bloqueado en este entorno: se sirve la Archivo Black local para ver la letra real.
  await page.route(/fonts\.googleapis\.com/, r => r.fulfill({ contentType: 'text/css', body: "@font-face{font-family:'Archivo Black';src:url(http://localhost:8766/dev/ArchivoBlack.ttf) format('truetype');}" }));
  await page.addInitScript(mock);
  await page.addInitScript(() => {
    // El mock define window.firebase; evita que los <script> de Firebase lo pisen.
    Object.defineProperty(window, 'firebase', { value: window.firebase, writable: false, configurable: false });
  });
  await page.goto('http://localhost:8766/index.html');
  await page.waitForTimeout(2500);
  const shot = async (name, full) => page.screenshot({ path: path.join(OUT, `${PREFIX}_${name}.png`), fullPage: !!full });

  await shot('01_pantalla_inicial');
  await page.evaluate(() => typeof showScreen === 'function' && showScreen('screen-dashboard'));
  await page.waitForTimeout(800);
  await shot('02_inicio', true);
  await page.evaluate(() => showTab('tab-rutina')); await page.waitForTimeout(400);
  await shot('02b_rutina', true);
  const day = await page.$('#rutina-content summary.rt-day-summary');
  if (day) { await day.click(); await page.waitForTimeout(600); await shot('03_dia', true); }
  await page.evaluate(() => showTab('tab-perfil')); await page.waitForTimeout(500); await shot('04_perfil', true);
  await page.evaluate(() => showTab('tab-beneficios')); await page.waitForTimeout(500); await shot('05_beneficios', true);
  await page.evaluate(() => typeof openChatModal === 'function' && openChatModal()); await page.waitForTimeout(500); await shot('06_chat');
  await page.evaluate(() => typeof closeChatModal === 'function' && closeChatModal());
  // Ventanas: categoría y perfil de beneficio, ficha, historial de un ejercicio, video y temporizador
  const tile = await page.$('.benef-cat-tile:not(.hero)');
  if (tile) { await tile.click(); await page.waitForTimeout(600); await shot('07_beneficio_categoria'); }
  const card = await page.$('#benef-category-modal .benef-card');
  if (card) { await card.click(); await page.waitForTimeout(250); await shot('08a_regalo_caja'); await page.waitForTimeout(800); await shot('08b_regalo_confeti'); await page.waitForTimeout(1400); await shot('08_beneficio_detalle', true); }
  await page.evaluate(() => { ['benef-profile-modal', 'benef-category-modal'].forEach(id => { const m = document.getElementById(id); if (m) m.style.display = 'none'; }); });
  await page.evaluate(() => typeof openFichaModal === 'function' && openFichaModal()); await page.waitForTimeout(600); await shot('09_ficha');
  await page.evaluate(() => { const m = document.getElementById('ficha-modal'); if (m) m.style.display = 'none'; });
  await page.evaluate(() => typeof openExProgressModal === 'function' && openExProgressModal('d1', 'e1', 'Sentadilla búlgara')); await page.waitForTimeout(600); await shot('10_historial');
  await page.evaluate(() => { const m = document.getElementById('ex-progress-modal'); if (m) m.style.display = 'none'; });
  await page.evaluate(() => typeof showExerciseVideo === 'function' && showExerciseVideo('', 'Baja controlado, rodilla alineada con el pie.', false, 60, 'Sentadilla búlgara', 'd1', 'e1')); await page.waitForTimeout(600); await shot('11_video');
  console.log('errores:', JSON.stringify(errors.slice(0, 10)));
  await browser.close();
  server.close();
})();
