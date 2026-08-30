const CACHE='mth-reader-v34-book14';
const CORE=['index.html','styles.css?v=20260730-mobile','app.js?v=20260830-book14','data/words.js?v=20260830-book14','manifest.webmanifest','assets/images/cover.jpg'];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET'||e.request.headers.has('range'))return;
  if(e.request.mode==='navigate'){
    e.respondWith(caches.match('index.html').then(cached=>{
      const fresh=fetch(e.request).then(response=>{if(response.status===200)caches.open(CACHE).then(cache=>cache.put('index.html',response.clone()));return response}).catch(()=>cached);
      return cached||fresh;
    }));
    return;
  }
  e.respondWith(caches.match(e.request).then(cached=>{
    if(cached)return cached;
    return fetch(e.request).then(response=>{if(response.status===200){const copy=response.clone();caches.open(CACHE).then(cache=>cache.put(e.request,copy))}return response});
  }));
});
