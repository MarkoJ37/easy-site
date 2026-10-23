// Local static test server; PHP source must never be returned to the browser.
import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';

const root = resolve('dist');
const types = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp',
  '.woff': 'font/woff', '.woff2': 'font/woff2', '.xml': 'application/xml', '.txt': 'text/plain' };
export const server = createServer(async (request, response) => {
  try {
    const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    const target = resolve(root, '.' + pathname);
    if (target !== root && !target.startsWith(root + sep)) {
      response.writeHead(403).end(); return;
    }
    if (extname(target).toLowerCase() === '.php') {
      response.writeHead(503, { 'Content-Type': 'application/json' });
      response.end(JSON.stringify({ ok: false, error: 'Slanje upita je dostupno na produkcionom serveru.' }));
      return;
    }
    const file = (await stat(target)).isDirectory() ? resolve(target, 'index.html') : target;
    const content = await readFile(file);
    response.writeHead(200, { 'Content-Type': types[extname(file)] || 'application/octet-stream' });
    response.end(content);
  } catch {
    response.writeHead(404).end('Nije pronađeno');
  }
}).listen(4321, '127.0.0.1', () => console.log('Test server: http://127.0.0.1:4321'));
