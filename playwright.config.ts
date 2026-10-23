import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/browser',
  fullyParallel: false,
  workers: 1,
  timeout: 60000,
  reporter: 'list',
  use: {
    baseURL: 'http://127.0.0.1:4321',
    channel: process.platform === 'win32' ? 'chrome' : undefined,
    trace: 'retain-on-failure',
  },
  webServer: process.env.EASY_TEST_SERVER === '1' ? undefined : {
    command: 'node tests/serve.mjs',
    url: 'http://127.0.0.1:4321',
    reuseExistingServer: !process.env.CI,
  },
});
