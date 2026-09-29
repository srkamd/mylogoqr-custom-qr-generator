const CACHE_NAME = 'mylogoqr-cache-v4';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/blog',
  '/blog.html',
  '/styles.css',
  '/app.js',
  '/how-to-use',
  '/how-to-use.html',
  '/about',
  '/about.html',
  '/contact',
  '/contact.html',
  '/privacy',
  '/privacy.html',
  '/terms',
  '/terms.html',
  '/whatsapp-qr-code-generator',
  '/wifi-qr-code-generator',
  '/text-qr-code-generator',
  '/vcard-qr-code-generator',
  '/app_icon.jpg',
  '/profile.jpg',
  '/url_preview.jpg',
  '/whatsapp_preview.jpg',
  '/wifi_preview.jpg',
  '/text_preview.jpg',
  '/vcard_preview.jpg'
];

// Install Event - cache essential assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[Service Worker] Pre-caching static assets');
      return cache.addAll(ASSETS_TO_CACHE);
    }).then(() => self.skipWaiting())
  );
});

// Activate Event - clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('[Service Worker] Removing old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event - network-falling-back-to-cache or cache-first for styles/libraries
self.addEventListener('fetch', (event) => {
  // Only handle HTTP/S requests (skip extension queries, etc.)
  if (!event.request.url.startsWith('http')) return;

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        // Return cached resource, but fetch update in background (Stale-While-Revalidate)
        fetch(event.request).then((networkResponse) => {
          if (networkResponse.status === 200) {
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, networkResponse));
          }
        }).catch(() => {/* Ignore network errors if offline */});
        return cachedResponse;
      }
      return fetch(event.request);
    })
  );
});
