---
type: is
id: is-01m1s8sr67yznpq3w4g48zd23c
title: "kpress upstream: print stylesheet releases the viewport but not html and body"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-05T17:10:30.343Z
updated_at: 2026-09-05T17:10:30.343Z
---
Found 2026-09-05 while making the explainer printable. kpress's page-reset.css sets html, body { height: 100%; overflow: hidden } for the scrolling shell, and print.css releases .kpress-viewport (block-size auto, overflow visible, transform none) but never those two elements. Chromium therefore paginates from a single viewport of content: the explainer printed as 1 page with about nine tenths of the document absent, deterministically at every browser viewport height tested. The host page can defend itself with @media print { html, body { height: auto; overflow: visible } }, which is what packing/devtools/templates/explainer-shell.html now does, but the fix belongs in kpress's print.css. Related, also found: print.css forces its light tokens on :root and .kpress but not .kpress-page-main, so a dark-mode reader prints prose on a dark ground; and kpress's @page margin boxes for the running footer and page number are inert in Chromium, which has never implemented CSS Paged Media margin boxes.
