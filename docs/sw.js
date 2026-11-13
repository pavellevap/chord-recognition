// Service worker for the installed app (built into docs/sw.js by scripts/build-standalone.sh).
// The page itself is fetched network-first, so a new version shows up on the next launch
// while online; everything else is served from cache so the app also opens offline.
const VERSION = 'c4abf5da2caf';
const SHELL = `shell-${VERSION}`;
const RUNTIME = 'runtime-v1';
const SHELL_FILES = ['./', './manifest.webmanifest', './icon-192.png', './icon-512.png', './icon-maskable-512.png', './icon-180.png'];
const CDN = ['https://cdn.jsdelivr.net/npm/vexflow@4.2.5/build/cjs/vexflow-bravura.js'];

self.addEventListener('install', (e) => {
  e.waitUntil((async () => {
    await (await caches.open(SHELL)).addAll(SHELL_FILES);
    const rt = await caches.open(RUNTIME);
    await Promise.all(CDN.map(async (u) => {
      try { if (!(await rt.match(u))) { const r = await fetch(u, { mode: 'cors' }); if (r.ok) await rt.put(u, r); } } catch (err) { /* cached on first use instead */ }
    }));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', (e) => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k.startsWith('shell-') && k !== SHELL) await caches.delete(k);
    await self.clients.claim();
  })());
});

const timeout = (ms) => new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), ms));

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (req.mode === 'navigate') {
    // network first (with a short timeout on bad connections), cached page offline
    e.respondWith((async () => {
      const cache = await caches.open(SHELL);
      try {
        const res = await Promise.race([fetch(req), timeout(4000)]);
        if (res.ok) cache.put('./', res.clone());
        return res;
      } catch (err) {
        return (await cache.match('./')) || Response.error();
      }
    })());
    return;
  }
  const sameOrigin = url.origin === self.location.origin;
  if (sameOrigin || /^(cdn\.jsdelivr\.net|fonts\.googleapis\.com|fonts\.gstatic\.com)$/.test(url.hostname)) {
    // cache first; fill the cache on first use
    e.respondWith((async () => {
      const cache = await caches.open(sameOrigin ? SHELL : RUNTIME);
      const hit = await cache.match(req);
      if (hit) return hit;
      const res = await fetch(req);
      if (res.ok || res.type === 'opaque') cache.put(req, res.clone());
      return res;
    })());
  }
});
