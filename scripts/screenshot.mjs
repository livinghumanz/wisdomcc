import { chromium } from 'playwright';

const base = process.env.BASE || 'http://127.0.0.1:8001';
const out = process.env.SHOT;
const pages = [
  ['home', '/'], ['about', '/About/'], ['courses', '/Course-Services/'],
  ['gallery', '/Gallery/'], ['preschool', '/preschool/'], ['faculty', '/Faculty-portal/'],
];
const viewports = [['desktop', 1440, 900], ['mobile', 390, 844]];

const browser = await chromium.launch();
for (const [vname, width, height] of viewports) {
  const ctx = await browser.newContext({ viewport: { width, height } });
  const page = await ctx.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));
  for (const [name, path] of pages) {
    await page.goto(base + path, { waitUntil: 'load', timeout: 45000 }).catch(e => errors.push(path + ': ' + e.message));
    await page.waitForTimeout(1200);
    await page.screenshot({ path: `${out}/${name}_${vname}.png`, fullPage: true });
    // horizontal overflow check
    const overflow = await page.evaluate(() => ({
      scrollW: document.documentElement.scrollWidth,
      clientW: document.documentElement.clientWidth,
    }));
    if (overflow.scrollW > overflow.clientW + 1) {
      errors.push(`${path} [${vname}] H-OVERFLOW scrollW=${overflow.scrollW} clientW=${overflow.clientW}`);
    }
  }
  await ctx.close();
  if (errors.length) console.log(`\n== ${vname} issues ==\n` + errors.join('\n'));
}
await browser.close();
console.log('\ndone');
