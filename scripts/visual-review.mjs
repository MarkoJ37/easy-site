import { chromium } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';

mkdirSync('artifacts/visual', { recursive: true });
const browser = await chromium.launch({ channel: process.platform === 'win32' ? 'chrome' : undefined });
const diagnostics = [];
for (const width of [360, 768, 1440]) {
  const page = await browser.newPage({ viewport: { width, height: 960 } });
  const failures = [];
  page.on('requestfailed', req => failures.push({ url: req.url(), error: req.failure()?.errorText }));
  await page.goto('http://127.0.0.1:4321/');
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: `artifacts/visual/hero-${width}.png` });
  await page.locator('#cene').scrollIntoViewIfNeeded();
  await page.waitForTimeout(400);
  await page.locator('#cene').screenshot({ path: `artifacts/visual/pricing-${width}.png` });
  await page.locator('#kontakt').scrollIntoViewIfNeeded();
  await page.waitForTimeout(400);
  await page.locator('#kontakt').screenshot({ path: `artifacts/visual/contact-${width}.png` });
  diagnostics.push({ width, failures, fonts: await page.evaluate(() => [...document.fonts].map(f => ({ family: f.family, weight: f.weight, status: f.status }))) });
  await page.goto('http://127.0.0.1:4321/shop');
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: `artifacts/visual/catalog-${width}.png` });
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.locator('[data-product]:visible [data-upit]').first().click();
  await page.waitForTimeout(300);
  const inputTop = await page.locator('#ime').evaluate(el => el.getBoundingClientRect().top);
  const filterBottom = await page.locator('#shop-filters').evaluate(el => el.getBoundingClientRect().bottom);
  if (inputTop < filterBottom) throw new Error(`Shop form covered by sticky filters at ${width}`);
  diagnostics.push({ width, inputTop, filterBottom });
  await page.close();
}
await browser.close();
writeFileSync('artifacts/visual/diagnostics.json', JSON.stringify(diagnostics, null, 2));
console.log('Visual screenshots and font/network diagnostics saved.');
