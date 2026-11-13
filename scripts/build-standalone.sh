#!/bin/sh
# Builds docs/index.html, a standalone copy of the app for GitHub Pages.
# index.html is written for the claude.ai Artifact skeleton (no doctype/head of its own),
# so this wraps it in an equivalent document. In a normal browser tab the page can use
# the microphone (Play on guitar); history is then kept in that browser only.
set -e
cd "$(dirname "$0")/.."
mkdir -p docs
{
  printf '%s' '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,-apple-system,"Segoe UI",sans-serif}img{max-width:100%}[hidden]{display:none!important}</style></head><body>'
  cat index.html
  printf '%s\n' '</body></html>'
} > docs/index.html
touch docs/.nojekyll
echo "wrote docs/index.html"
