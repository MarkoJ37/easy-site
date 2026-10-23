// Renders public/og.jpg (1200×630): the real logo, one-colour white, on --ink.
// No re-typeset wordmark, no imagery, no extra copy. Run: node scripts/build-og.mjs
import { chromium } from 'playwright';
import { readFile } from 'node:fs/promises';

// The raster lockup, drawn at its native 439px so nothing is resampled. (logo/logo.svg
// is an auto-trace that garbles "computers" — not usable until a proper vector exists.)
const png = await readFile(new URL('../public/logo.png', import.meta.url));
const logo = `data:image/png;base64,${png.toString('base64')}`;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
// brightness(0) invert(1) turns every opaque pixel white and keeps the alpha, so
// the knocked-out "e" in the mark still shows the navy field through it.
await page.setContent(`<!doctype html>
  <body style="margin:0;width:1200px;height:630px;display:grid;place-items:center;background:#0f2c4e">
    <img src="${logo}" style="width:439px;height:174px;filter:brightness(0) invert(1)">
  </body>`);
await page.waitForLoadState('load');
await page.screenshot({ path: 'public/og.jpg', type: 'jpeg', quality: 90 });
await browser.close();
console.log('public/og.jpg written');
