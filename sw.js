/* ═══════════════════════════════════════════════════════════════
   MANMIN PWA — Service Worker v2.1
   냉온수 배관 관경 산정 시스템 [MANMIN-Ver2.0]
   ═══════════════════════════════════════════════════════════════ */

const CACHE_NAME    = 'manmin-pipe-v2';
const STATIC_CACHE  = 'manmin-static-v2';
const DYNAMIC_CACHE = 'manmin-dynamic-v2';

/* ── 설치 시 반드시 캐시할 핵심 파일 ── */
const PRECACHE_URLS = [
  './',
  './index.html',
  './manifest.json',
  './favicon.ico',
  './icons/icon-192x192.png',
  './icons/icon-512x512.png',
  './icons/apple-touch-icon.png',
];

/* ── 외부 CDN (네트워크 우선, 실패 시 캐시) ── */
const CDN_ORIGINS = [
  'cdn.jsdelivr.net',
  'fonts.googleapis.com',
  'fonts.gstatic.com',
  'cdnjs.cloudflare.com',
];

/* ════════════════════════════════
   INSTALL — 핵심 파일 Pre-cache
   ════════════════════════════════ */
self.addEventListener('install', event => {
  console.log('[SW] Install v2');
  event.waitUntil(
    caches.open(STATIC_CACHE).then(cache => {
      return cache.addAll(PRECACHE_URLS).catch(err => {
        console.warn('[SW] Pre-cache 일부 실패 (정상):', err);
      });
    }).then(() => self.skipWaiting())
  );
});

/* ════════════════════════════════
   ACTIVATE — 구버전 캐시 정리
   ════════════════════════════════ */
self.addEventListener('activate', event => {
  console.log('[SW] Activate v2');
  const validCaches = [CACHE_NAME, STATIC_CACHE, DYNAMIC_CACHE];
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(k => !validCaches.includes(k))
            .map(k => { console.log('[SW] 구버전 삭제:', k); return caches.delete(k); })
      )
    ).then(() => self.clients.claim())
  );
});

/* ════════════════════════════════
   FETCH — 캐싱 전략 분기
   ════════════════════════════════ */
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  /* 비-GET 요청 무시 */
  if (request.method !== 'GET') return;

  /* CDN — Network First (실패 시 Cache Fallback) */
  if (CDN_ORIGINS.some(o => url.hostname.includes(o))) {
    event.respondWith(networkFirstStrategy(request, DYNAMIC_CACHE));
    return;
  }

  /* 동일 오리진 — Cache First (없으면 네트워크 후 저장) */
  if (url.origin === self.location.origin) {
    event.respondWith(cacheFirstStrategy(request));
    return;
  }
});

/* ── Cache First ── */
async function cacheFirstStrategy(request) {
  const cached = await caches.match(request);
  if (cached) return cached;

  try {
    const response = await fetch(request);
    if (response && response.status === 200) {
      const cache = await caches.open(STATIC_CACHE);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    /* 오프라인 + 캐시 없음 → index.html 반환 */
    const fallback = await caches.match('./index.html');
    return fallback || new Response('오프라인 상태입니다.', {
      status: 503,
      headers: { 'Content-Type': 'text/plain; charset=utf-8' }
    });
  }
}

/* ── Network First ── */
async function networkFirstStrategy(request, cacheName) {
  try {
    const response = await fetch(request);
    if (response && response.status === 200) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    const cached = await caches.match(request);
    return cached || new Response('', { status: 503 });
  }
}

/* ════════════════════════════════
   MESSAGE — skipWaiting 지원
   ════════════════════════════════ */
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    console.log('[SW] skipWaiting 수신 → 즉시 활성화');
    self.skipWaiting();
  }
});

/* ════════════════════════════════
   PUSH — 알림 (선택적)
   ════════════════════════════════ */
self.addEventListener('push', event => {
  const data = event.data ? event.data.json() : {};
  event.waitUntil(
    self.registration.showNotification(data.title || '냉온수 배관 산정', {
      body: data.body || '업데이트가 있습니다.',
      icon: './icons/icon-192x192.png',
      badge: './icons/icon-96x96.png',
    })
  );
});
