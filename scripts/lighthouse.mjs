import lighthouse from 'lighthouse';
import { chromium } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';

mkdirSync('artifacts/lighthouse', { recursive: true });
const browser = await chromium.launch({ channel: process.platform === 'win32' ? 'chrome' : undefined,
  args: ['--remote-debugging-port=9224'] });
try {
  for (const [name, path] of [['home', '/'], ['shop', '/shop']]) {
    if (process.argv[2] && process.argv[2] !== name) continue;
    const result = await lighthouse(`http://127.0.0.1:4321${path}`, {
      port: 9224, output: ['html', 'json'], logLevel: 'error',
      onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'],
    });
    writeFileSync(`artifacts/lighthouse/${name}.html`, result.report[0]);
    writeFileSync(`artifacts/lighthouse/${name}.json`, result.report[1]);
    console.log(name, Object.fromEntries(Object.entries(result.lhr.categories).map(([key, value]) => [key, Math.round(value.score * 100)])));
  }
} finally { await browser.close(); }
