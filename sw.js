// Service worker de Personal Hub -- mismo patrón que Edgy Gestión
// (Fase 31b): cachea la cáscara de la app para que abra rápido, pero
// nunca intercepta pedidos a Supabase ni a ningún CDN externo (los
// scripts de React/antd/etc. se sirven de unpkg.com, no del mismo
// origin) -- se filtra por origin en el fetch handler, así los datos y
// las librerías siempre vienen frescos.
//
// Rutas relativas (./) porque este sitio vive en un subpath de GitHub
// Pages (https://<usuario>.github.io/Edgy-Prop-Trading-Hub/), no en la
// raíz del dominio.
//
// Importante: subir CACHE_NAME (v1 -> v2 -> v3...) en cada entrega
// grande de cambios de la app shell, si no el navegador no detecta que
// hay una versión nueva y la app instalada queda pegada a la vieja.
const CACHE_NAME = 'personal-hub-v1'
const APP_SHELL = ['./', './index.html', './icon-192.png', './icon-512.png', './manifest.json']

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL)))
  self.skipWaiting()
})

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))),
  )
  self.clients.claim()
})

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url)
  if (url.origin !== self.location.origin) return

  if (event.request.mode === 'navigate') {
    event.respondWith(fetch(event.request).catch(() => caches.match('./index.html')))
    return
  }
  event.respondWith(caches.match(event.request).then((resp) => resp || fetch(event.request)))
})

// -- Notificaciones push (recordatorios de medicación/turnos) --------
// El payload lo arma la Edge Function de Supabase que revisa qué
// recordatorio venció (ver supabase/functions/enviar-recordatorios).
// Se espera JSON: { title, body, url } -- si el payload no es JSON
// válido, se muestra un aviso genérico en vez de romper.
self.addEventListener('push', (event) => {
  let data = { title: 'Personal Hub', body: 'Tenés un recordatorio pendiente.', url: './' }
  if (event.data) {
    try {
      data = { ...data, ...event.data.json() }
    } catch (e) {
      data.body = event.data.text() || data.body
    }
  }
  event.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: './icon-192.png',
      badge: './icon-192.png',
      data: { url: data.url || './' },
    }),
  )
})

self.addEventListener('notificationclick', (event) => {
  event.notification.close()
  const targetUrl = event.notification.data?.url || './'
  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clientList) => {
      for (const client of clientList) {
        if (client.url.includes(self.location.origin) && 'focus' in client) return client.focus()
      }
      if (self.clients.openWindow) return self.clients.openWindow(targetUrl)
    }),
  )
})
