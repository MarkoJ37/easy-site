// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://easy.rs',
  output: 'static',
  trailingSlash: 'ignore',
  integrations: [
    sitemap({
      // /hvala is a post-submit confirmation carrying noindex — keep it out of
      // the sitemap too, so the two signals don't contradict each other.
      filter: (page) => !page.includes('/hvala'),
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
  build: {
    // public/api/upit.php must land at dist/api/upit.php untouched — Astro copies
    // public/ verbatim, so nothing here may rewrite or hash it.
    assets: '_assets',
  },
});
