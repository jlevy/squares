---
type: is
id: is-01m44m1exp7fav03ypcwwzv04z
title: index.html is 2.67 MB of its own content (299 KB gzipped)
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m42xfwp06kzm2b390dx1cw17
created_at: 2026-10-04T23:29:59.734Z
updated_at: 2026-10-04T23:29:59.734Z
---
Live check on e19be6bb0 (2026-10-04, exact deployed bytes): with the shared shell gone, index.html is still 2.67 MB raw / 299 KB gzip, grown from 2.32 MB when #340 moved the atlas above Recent Results. Profile what the bytes are (atlas SVGs, inline data) and cut; synopsis.html 1.54 MB and frontier.html 1.68 MB likewise (see think-44tv for their main-thread time).
