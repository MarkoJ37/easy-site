// Run against the local PHP server only; no real messages or credentials.
import assert from 'node:assert/strict';
const url = 'http://127.0.0.1:8765/api/upit.php';
const valid = { ime: 'Test', telefon: '0611234567', poruka: 'Lokalna provera', ts: String(Math.floor(Date.now() / 1000) - 10) };
const get = await fetch(url, { headers: { Accept: 'application/json' } });
assert.equal(get.status, 405);
assert.equal(get.headers.get('allow'), 'POST');
for (const [body, status] of [[valid, 503], [{ ...valid, website: 'spam' }, 422], [{ ...valid, ts: String(Math.floor(Date.now() / 1000)) }, 422], [{ ...valid, email: 'bad' }, 422]]) {
  const response = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(body) });
  assert.equal(response.status, status);
  assert.equal((await response.json()).ok, false);
}
const native = await fetch(url, { method: 'POST', body: new URLSearchParams({ ...valid, poruka: '<script>alert(1)</script>' }) });
assert.equal(native.status, 503);
const html = await native.text();
assert(html.includes('&lt;script&gt;alert(1)&lt;/script&gt;'));
assert(!html.includes('<script>alert(1)</script>'));
assert(html.includes('Pokušajte ponovo'));
console.log('6 HTTP endpoint checks passed; missing config fails safely; native form retains and escapes text.');
