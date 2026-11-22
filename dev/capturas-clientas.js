/*
 * Capturas de "Mis clientas" del panel (solo desarrollo): lista, perfil y editor de rutina.
 * Uso: node dev/capturas-clientas.js <carpeta_salida> [prefijo] [ancho]
 */
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..'), OUT = process.argv[2] || '/tmp', PREFIX = process.argv[3] || 'c', WIDTH = +(process.argv[4] || 1024);
const server = http.createServer((req, res) => {
  const file = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); return res.end(); }
  fs.createReadStream(file).pipe(res);
});
(async () => {
  await new Promise(r => server.listen(8770, r));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: WIDTH, height: 1100 } });
  const errors = []; page.on('pageerror', e => errors.push(e.message)); page.on('dialog', d => d.dismiss());
  await page.route(/gstatic\.com|firebaseio\.com|cdnjs\.cloudflare\.com/, r => r.abort());
  await page.route(/fonts\.googleapis\.com/, r => r.fulfill({ contentType: 'text/css', body: "@font-face{font-family:'Archivo Black';src:url(http://localhost:8770/dev/ArchivoBlack.ttf) format('truetype');}" }));
  await page.addInitScript(fs.readFileSync(path.join(__dirname, 'mock-firebase.js'), 'utf8'));
  await page.addInitScript(() => { Object.defineProperty(window, 'firebase', { value: window.firebase, writable: false }); });
  await page.addInitScript(() => { try { sessionStorage.setItem('fa_auth_v2', '1'); } catch (e) {} });
  await page.goto('http://localhost:8770/admin.html'); await page.waitForTimeout(2500);
  const shot = async (n, full) => page.screenshot({ path: path.join(OUT, `${PREFIX}_${n}.png`), fullPage: !!full });
  await page.evaluate(() => showScreen('clientes')); await page.waitForTimeout(900); await shot('01_lista', true);
  for (const [cid, n] of [['demo-client', '02_perfil_rutinaperso'], ['demo-lucia', '03_perfil_presencial']]) {
    await page.evaluate(id => openAdminClientProfile(id), cid); await page.waitForTimeout(900); await shot(n);
    const tabs = await page.$$eval('#acp-content [onclick^="acpSwitchTab"]', els => els.map(e => e.getAttribute('onclick')));
    for (const t of tabs) { await page.evaluate(code => eval(code), t); await page.waitForTimeout(500); await shot(n + '_' + t.match(/'(\w+)'/)[1]); }
    await page.evaluate(() => closeAdminClientProfile());
  }
  await page.evaluate(() => openRutinaEditor('demo-client')); await page.waitForTimeout(1200); await shot('04_editor', true);
  console.log('errores:', JSON.stringify(errors.slice(0, 8)));
  await browser.close(); server.close();
})();
