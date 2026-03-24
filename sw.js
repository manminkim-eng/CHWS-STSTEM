/* ════════════════════════════════════════════
   MANMIN 냉온수 배관 관경 산정 시스템
   Service Worker — Ver 2.0
   캐시 전략: Cache First → Network Fallback
   오프라인 완전 지원
════════════════════════════════════════════ */

const CACHE_NAME      = 'manmin-pipe-v2';
const OFFLINE_URL     = './index.html';

// 캐시할 정적 자원 목록
const PRECACHE_URLS = [
  './',
  './index.html',
  './manifest.json',
  './favicon.ico',
  './icons/icon-192x192.png',
  './icons/icon-512x512.png',
  './icons/apple-touch-icon.png',
];

// ── 설치: 핵심 파일 사전 캐시 ──
self.addEventListener('install', event => {
  console.log('[SW] 설치 중...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[SW] 사전 캐시 저장');
        return cache.addAll(PRECACHE_URLS);
      })
      .then(() => self.skipWaiting())
      .catch(err => console.warn('[SW] 사전 캐시 실패:', err))
  );
});

// ── 활성화: 구버전 캐시 삭제 ──
self.addEventListener('activate', event => {
  console.log('[SW] 활성화');
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => key !== CACHE_NAME)
          .map(key => {
            console.log('[SW] 구캐시 삭제:', key);
            return caches.delete(key);
          })
      )
    ).then(() => self.clients.claim())
  );
});

// ── Fetch: Cache First 전략 ──
self.addEventListener('fetch', event => {
  // POST / chrome-extension 등 무시
  if (event.request.method !== 'GET') return;
  if (!event.request.url.startsWith('http')) return;

  // Google Fonts / CDN: Network First (인터넷 있으면 최신, 없으면 캐시)
  const isExternal = (
    event.request.url.includes('fonts.googleapis.com') ||
    event.request.url.includes('fonts.gstatic.com') ||
    event.request.url.includes('cdn.jsdelivr.net') ||
    event.request.url.includes('cdnjs.cloudflare.com')
  );

  if (isExternal) {
    event.respondWith(networkFirstStrategy(event.request));
    return;
  }

  // 로컬 파일: Cache First
  event.respondWith(cacheFirstStrategy(event.request));
});

// Cache First: 캐시 우선, 없으면 네트워크 요청 후 캐시 저장
async function cacheFirstStrategy(request) {
  const cached = await caches.match(request);
  if (cached) return cached;

  try {
    const response = await fetch(request);
    if (response && response.status === 200 && response.type !== 'opaque') {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch (err) {
    // 오프라인 폴백
    const fallback = await caches.match(OFFLINE_URL);
    return fallback || new Response('오프라인 상태입니다. 앱을 한 번 온라인에서 열어주세요.', {
      status: 503,
      headers: { 'Content-Type': 'text/html; charset=utf-8' }
    });
  }
}

// Network First: 네트워크 우선, 실패 시 캐시
async function networkFirstStrategy(request) {
  try {
    const response = await fetch(request);
    if (response && response.status === 200) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch (err) {
    const cached = await caches.match(request);
    return cached || new Response('', { status: 503 });
  }
}

// ── 메시지: SKIP_WAITING (강제 업데이트) ──
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    console.log('[SW] 강제 업데이트 적용');
    self.skipWaiting();
  }
});
