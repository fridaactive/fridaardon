/*
 * Graba un video corto navegando el portal en modo de prueba (solo desarrollo).
 * Uso: node dev/video-demo.js <carpeta_salida>
 */
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..'), OUT = process.argv[2] || '/tmp';
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.jpg': 'image/jpeg', '.png': 'image/png', '.ttf': 'font/ttf' };
const server = http.createServer((req, res) => {
  const file = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});
(async () => {
  await new Promise(r => server.listen(8766, r));
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, recordVideo: { dir: OUT, size: { width: 390, height: 844 } }, hasTouch: true });
  const page = await ctx.newPage();
  await page.route(/gstatic\.com|firebaseio\.com|emailjs/, r => r.abort());
  await page.route(/fonts\.googleapis\.com/, r => r.fulfill({ contentType: 'text/css', body: "@font-face{font-family:'Archivo Black';src:url(http://localhost:8766/dev/ArchivoBlack.ttf) format('truetype');}" }));
  await page.addInitScript(fs.readFileSync(path.join(__dirname, 'mock-firebase.js'), 'utf8'));
  await page.addInitScript(() => { Object.defineProperty(window, 'firebase', { value: window.firebase, writable: false }); });
  await page.goto('http://localhost:8766/index.html');
  await page.waitForTimeout(2200);
  await page.evaluate(() => { showScreen('screen-dashboard'); showTab('tab-rutina'); showTab('tab-inicio'); });
  await page.waitForTimeout(1600);
  const wait = ms => page.waitForTimeout(ms);
  await page.click('.in-hero'); await wait(1500);
  await page.mouse.wheel(0, -2000); await wait(300);
  await page.click('.bnav-btn[data-tab="tab-perfil"]'); await wait(1300);
  await page.click('.bnav-btn[data-tab="tab-beneficios"]'); await wait(1200);
  const tile = await page.$('.benef-cat-tile:not(.hero)'); if (tile) { await tile.click(); await wait(1300); }
  await page.evaluate(() => { var b = document.querySelector('#benef-category-modal .bp-back-btn'); if (b) b.click(); }); await wait(800);
  await page.click('.bnav-btn[data-tab="tab-inicio"]'); await wait(1600);
  await page.click('.chat-fab'); await wait(1400);
  await ctx.close(); await browser.close(); server.close();
})();
