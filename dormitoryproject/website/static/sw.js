let cache_name = 'pwaDormitory'
let filesToCache = [
    './template/base.html',
    'css/css-bootstrap/bootstrap.css',
    'css/ext-style.css',
    'js/js-bootstrap/jquery.min.js',
    'js/js-bootstrap/bootstrap.bundle.js',
    'js/ext-js.js'
];

self.addEventListener('install', function(e) {
    e.waitUntil(
        caches.open(cache_name).then(function(cache) {
            return cache.addAll(filesToCache);
        })
    );
});

self.addEventListener('fetch', function (e) {
    e.respondWith(
        caches.match(e.request).then(function(response) {
            return response || fetch(e.request);
        })
    );
});