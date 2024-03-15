// service-worker.js

importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');

if (workbox) {
    // Cache HTML, CSS, JavaScript files
    workbox.routing.registerRoute(
        /\.(?:html|css|js)$/,
        new workbox.strategies.NetworkFirst()
    );

    // Cache images
    workbox.routing.registerRoute(
        /\.(?:png|jpg|jpeg|svg|gif)$/,
        new workbox.strategies.CacheFirst({
            cacheName: 'images',
            plugins: [
                new workbox.expiration.ExpirationPlugin({
                    maxEntries: 20,
                    maxAgeSeconds: 7 * 24 * 60 * 60, // 1 week
                }),
            ],
        })
    );
} else {
    console.error('Workbox could not be loaded. No offline support.');
}
