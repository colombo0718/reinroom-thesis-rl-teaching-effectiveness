import { chromium } from 'playwright-chromium';
import { mkdirSync } from 'fs';

mkdirSync('_shots', { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const pages = [11, 15, 24, 26, 31];
for (const n of pages) {
  await page.goto(`http://localhost:3030/${n}`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);
  await page.screenshot({ path: `_shots/page${n}.png`, fullPage: false });
  console.log(`saved page ${n}`);
}
await browser.close();
