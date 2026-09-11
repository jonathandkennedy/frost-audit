// Renders report/frost-law-group-search-audit.html to PDF in two passes
// (full-bleed LLG cover without margins, then the body with a branded
// running header/footer) and merges them. Optional argv[2]: a directory for
// review screenshots.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');
const { execFileSync } = require('child_process');
(async () => {
  const html = 'file://' + path.resolve('report/frost-law-group-search-audit.html');
  const shots = process.argv[2];
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1100, height: 1300 } });
  await page.goto(html, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
  if (shots) {
    await page.locator('.cover-dark').screenshot({ path: `${shots}/cover.png` });
    await page.locator('#summary').screenshot({ path: `${shots}/summary.png` });
    await page.locator('#authority figure').first().screenshot({ path: `${shots}/diagram.png` });
    await page.locator('.closing').screenshot({ path: `${shots}/closing.png` });
    await page.locator('#how figure').first().screenshot({ path: `${shots}/flow.png` });
  }
  const tile = await page.evaluate(() => document.querySelector('#llg-tile').getAttribute('src'));
  await page.emulateMedia({ media: 'print' });
  // pass 1: the cover, full bleed
  await page.evaluate(() => document.documentElement.classList.add('pdf-cover'));
  await page.addStyleTag({ content: '@page{size:Letter;margin:0}' });
  await page.pdf({ path: 'report/_cover.pdf', preferCSSPageSize: true, printBackground: true, pageRanges: '1' });
  // pass 2: the body with running header/footer
  await page.evaluate(() => { document.documentElement.classList.remove('pdf-cover'); document.documentElement.classList.add('pdf-body'); });
  await page.addStyleTag({ content: '@page{size:Letter;margin:17mm 12mm 16mm 12mm}' });
  const base = 'font-family:Helvetica,Arial,sans-serif;font-size:7px;letter-spacing:.16em;text-transform:uppercase;color:#7a7390;width:100%;box-sizing:border-box;padding:0 12mm;display:flex;align-items:center;justify-content:space-between;';
  const headerTemplate = `<div style="${base}margin-top:5mm"><div style="display:flex;align-items:center;gap:7px"><img src="${tile}" style="height:16px;width:auto;border-radius:3px"><span style="font-weight:700;color:#5b21b6">Legal Leads Group</span><span>· Search audit</span></div><div>Frost Law Group, LLC</div></div>`;
  const footerTemplate = `<div style="${base}margin-bottom:5mm"><div>Confidential · prepared for Frost Law Group</div><div style="color:#5b21b6;font-weight:700">Page <span class="pageNumber"></span> / <span class="totalPages"></span></div><div>LLG · September 2026</div></div>`;
  await page.pdf({ path: 'report/_body.pdf', preferCSSPageSize: true, printBackground: true, displayHeaderFooter: true, headerTemplate, footerTemplate });
  await browser.close();
  execFileSync('python3', ['build/merge_pdf.py'], { stdio: 'inherit' });
})().catch(e => { console.error(e); process.exit(1); });
