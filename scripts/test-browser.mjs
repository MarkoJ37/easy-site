// Keep server ownership in this process so test teardown also works on Windows.
import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { fileURLToPath } from 'node:url';
import { server } from '../tests/serve.mjs';

await once(server, 'listening');
const runner = fileURLToPath(new URL('../node_modules/@playwright/test/cli.js', import.meta.url));
const child = spawn(process.execPath, [runner, 'test', ...process.argv.slice(2)], {
  stdio: 'inherit', env: { ...process.env, EASY_TEST_SERVER: '1' },
});
try {
  const [code] = await once(child, 'exit');
  process.exitCode = code ?? 1;
} finally {
  server.closeAllConnections();
  server.close();
}
