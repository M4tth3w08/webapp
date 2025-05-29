const CACHE_NAME = "bodyenergym-cache-v1";
const urlsToCache = [
  "/",
  "/static/style.css",        // aggiungi altri asset se usati
  "/static/script.js",
  "/static/icons/icon-192.png",
  "/static/icons/icon-512.png"
];

// Installazione: cache iniziale
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

// Attivazione: pulizia cache vecchie
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keyList =>
      Promise.all(
        keyList.map(key => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      )
    )
  );
});

// Fetch: serve dalla cache se offline
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});