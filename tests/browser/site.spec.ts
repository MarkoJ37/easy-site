import { expect, test } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { mkdirSync } from 'node:fs';

for (const width of [360, 768, 1440]) {
  for (const route of ['/', '/shop', '/privatnost', '/hvala']) {
    test(`${route} at ${width}px: layout, links, accessibility`, async ({ page }) => {
      await page.setViewportSize({ width, height: 900 });
      const errors: string[] = [];
      page.on('pageerror', error => errors.push(error.message));
      page.on('requestfailed', request => errors.push(`${request.url()}: ${request.failure()?.errorText}`));
      await page.goto(route);
      await page.evaluate(() => document.fonts.ready);
      await expect(page.locator('h1')).toBeVisible();
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
      expect(await page.locator('img').evaluateAll(images => images.every(image => image instanceof HTMLImageElement && image.complete && image.naturalWidth > 0))).toBe(true);
      const broken = await page.locator('a[href^="#"]').evaluateAll(links => links.map(a => a.getAttribute('href')!).filter(href => !document.getElementById(href.slice(1))));
      expect(broken).toEqual([]);
      await expect(page.locator('nav[aria-label="Glavna navigacija"] a[href="/#kontakt"]')).toHaveCount(2);
      // Scroll the actual page so section-entry transitions finish before capture.
      await page.evaluate(async () => {
        for (let y = 0; y < document.body.scrollHeight; y += 600) {
          window.scrollTo({ top: y, behavior: 'instant' });
          await new Promise(resolve => setTimeout(resolve, 70));
        }
        window.scrollTo({ top: 0, behavior: 'instant' });
      });
      await page.waitForTimeout(350);
      const audit = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
      expect(audit.violations.map(v => ({ id: v.id, nodes: v.nodes.map(n => n.target) }))).toEqual([]);
      expect(errors).toEqual([]);
      mkdirSync('artifacts/visual', { recursive: true });
      await page.screenshot({ path: `artifacts/visual/${route === '/' ? 'home' : route.slice(1)}-${width}.png`, fullPage: true });
    });
  }
}

test('mobile navigation closes with Escape and reaches home sections from shop', async ({ page }) => {
  await page.setViewportSize({ width: 360, height: 800 });
  await page.goto('/shop');
  await page.locator('#nav-toggle').click();
  await expect(page.locator('#nav-toggle')).toHaveAttribute('aria-expanded', 'true');
  await page.keyboard.press('Escape');
  await expect(page.locator('#nav-toggle')).toHaveAttribute('aria-expanded', 'false');
  await page.locator('#nav-toggle').click();
  await page.locator('#nav-mobile a[href="/#cene"]').click();
  await expect(page).toHaveURL(/\/#cene$/);
  await expect(page.locator('#cene')).toBeInViewport();
});

test('catalog paging, accessible filtering, accent-free search and inquiry selection', async ({ page }) => {
  await page.goto('/shop');
  await expect(page.locator('[data-product]:visible')).toHaveCount(12);
  const first = await page.locator('[data-product]:visible h3').first().textContent();
  await page.locator('#shop-next').click();
  await expect(page.locator('#shop-page')).toHaveText('Strana 2 / 13');
  expect(await page.locator('[data-product]:visible h3').first().textContent()).not.toBe(first);
  await page.getByRole('button', { name: 'Softver i licence', exact: true }).click();
  await expect(page.locator('[data-product]:visible')).toHaveCount(3);
  await expect(page.getByRole('button', { name: 'Softver i licence', exact: true })).toHaveAttribute('aria-pressed', 'true');
  await page.getByRole('button', { name: 'Sve', exact: true }).click();
  await page.locator('#shop-search').fill('tastatura');
  expect(await page.locator('[data-product]:visible').count()).toBeGreaterThan(0);
  const name = await page.locator('[data-product]:visible h3').first().textContent();
  await page.locator('[data-product]:visible [data-upit]').first().click();
  await expect(page.locator('#upit-proizvod')).toHaveValue(name!);
  await expect(page.locator('#ime')).toBeFocused();
  await page.locator('#upit-clear').click();
  await expect(page.locator('#upit-proizvod')).toHaveValue('');
  await page.locator('#shop-search').fill('zzzz-no-product');
  await expect(page.locator('#shop-empty')).toBeVisible();
});

test('failed form preserves text; only confirmed success redirects', async ({ page }) => {
  await page.goto('/');
  await page.locator('#ime').fill('Test korisnik');
  await page.locator('#telefon').fill('0611234567');
  await page.locator('#poruka').fill('Provera forme bez stvarne isporuke.');
  await page.route('**/api/upit.php', route => route.fulfill({ status: 503, json: { ok: false, error: 'Probajte ponovo.' } }));
  await page.locator('#upit-submit').click();
  await expect(page.locator('#upit-error')).toHaveText('Probajte ponovo.');
  await expect(page.locator('#poruka')).toHaveValue('Provera forme bez stvarne isporuke.');
  await expect(page.locator('#upit-submit')).toBeEnabled();
  await page.unroute('**/api/upit.php');
  await page.route('**/api/upit.php', route => route.fulfill({ status: 200, json: { ok: false } }));
  await page.locator('#upit-submit').click();
  await expect(page.locator('#upit-error')).toBeVisible();
  await expect(page).not.toHaveURL(/hvala/);
  await page.unroute('**/api/upit.php');
  await page.route('**/api/upit.php', route => route.fulfill({ status: 200, json: { ok: true } }));
  await page.locator('#upit-submit').click();
  await expect(page).toHaveURL(/hvala/);
});
