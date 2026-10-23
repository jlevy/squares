---
type: is
id: is-01m5k93vknqqa0ve9qvbvpjv8y
title: Keep shared assets cached across deploys (service worker for /assets/)
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m5jr2cr74kbbn71j05pqsgkd
created_at: 2026-10-23T02:23:22.224Z
updated_at: 2026-10-23T02:23:22.224Z
---
Measured 2026-10-23 on squaremath.org: GitHub Pages serves every file with cache-control: max-age=600 and an ETag built from the deploy time (e.g. "6adac02e-815c"), and the site deploys every 10-20 minutes (00:45, 00:53, 01:06, 01:19, 01:26, 01:49, 02:02 on 23 Oct). So after any deploy a returning reader re-downloads all fonts and stylesheets even though /assets/ names are content-hashed and unchanged; with font-display: block the text is hidden while they arrive (production, cold cache: 0-370 ms of nav-bar-only frames per navigation). GitHub Pages cannot set headers. A service worker that serves /assets/<name>.<16-hex>.<ext> cache-first (immutable by construction) and leaves HTML network-first fixes this in every browser without changing typography. Measure before/after with think-15b4.
