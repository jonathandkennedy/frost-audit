const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');
(async () => {
  const html = 'file://' + path.resolve('report/frost-law-group-search-audit.html');
  const shots = process.argv[2];
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1100, height: 1300 } });
  await page.goto(html, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
  if (shots) {
    await page.screenshot({ path: `${shots}/top.png` });
    const n = await page.evaluate(() => document.querySelectorAll('figure').length);
    for (let i = 0; i < n; i++) {
      const el = page.locator('figure').nth(i);
      await el.screenshot({ path: `${shots}/fig_${String(i).padStart(2, '0')}.png` });
    }
    await page.locator('#summary').screenshot({ path: `${shots}/summary.png` });
    await page.locator('#channels .channel').first().screenshot({ path: `${shots}/channel.png` });
    await page.locator('#site1 .tblwrap').first().screenshot({ path: `${shots}/table_pages.png` });
    console.log('figures:', n);
  }
  await page.emulateMedia({ media: 'print' });
  await page.pdf({ path: 'report/frost-law-group-search-audit.pdf', format: 'Letter', printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true, headerTemplate: '<div></div>', footerTemplate: '<div style="font-size:9px;color:#7c8694;width:100%;text-align:center;font-family:sans-serif">Frost Law Group Search Audit · <span class="pageNumber"></span> / <span class="totalPages"></span></div>', margin: { top: '14mm', bottom: '16mm', left: '12mm', right: '12mm' } });
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
