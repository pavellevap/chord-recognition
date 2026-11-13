#!/bin/sh
# Builds the installable standalone app in docs/ for GitHub Pages:
#   docs/index.html  index.html wrapped in a full document, plus manifest, icons and service worker
#   docs/sw.js       service worker (offline cache), versioned by the page's content
# index.html is written for the claude.ai Artifact skeleton (no doctype/head of its own).
# In a normal browser tab, or installed as an app, the page can use the microphone
# (Play on guitar); history is then kept on the device. Icons: scripts/make-icons.py.
set -e
cd "$(dirname "$0")/.."
mkdir -p docs
{
  printf '%s' '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
  printf '%s' '<link rel="manifest" href="manifest.webmanifest"><meta name="theme-color" content="#e8ecf0" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#10141a" media="(prefers-color-scheme: dark)"><link rel="icon" href="icon-192.png"><link rel="apple-touch-icon" href="icon-180.png"><meta name="mobile-web-app-capable" content="yes">'
  printf '%s' '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,-apple-system,"Segoe UI",sans-serif}img{max-width:100%}[hidden]{display:none!important}</style></head><body>'
  cat index.html
  printf '%s' '<script>if("serviceWorker"in navigator)addEventListener("load",function(){navigator.serviceWorker.register("sw.js").catch(function(){})})</script>'
  printf '%s\n' '</body></html>'
} > docs/index.html
VERSION=$(sha1sum docs/index.html docs/manifest.webmanifest | sha1sum | cut -c1-12)
sed "s/__VERSION__/$VERSION/" scripts/sw.template.js > docs/sw.js
touch docs/.nojekyll
echo "wrote docs/index.html and docs/sw.js (version $VERSION)"
