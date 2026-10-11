---
type: is
id: is-01m42xfwp06kzm2b390dx1cw17
title: "Site: page weight, speed and readability"
kind: epic
status: open
priority: 1
version: 18
labels: []
dependencies: []
child_order_hints:
  - is-01m42xhs1mmqpv12d1j74rrvey
  - is-01m42xhvh42fy1x77cd5j8c0dc
  - is-01m42xhxk4awqq1jmgzykwdct1
  - is-01m42xhzkhgcrhah1b41gpjxf4
  - is-01m42xj1dc4ez804wdvcv0t2yd
  - is-01m44m1dkx2sb29pw359yn4rja
  - is-01m44m1exp7fav03ypcwwzv04z
  - is-01m44mqjvxyxc9w7h44fsxvkb9
  - is-01m44mv6v2h464asddwmm4qhj5
  - is-01m44mv85w82m8a9grq8rrfe8f
  - is-01m44mv9jff8sbw3fng71h3871
  - is-01m44mvawpdyqh6jg7x1nq3k33
  - is-01m44mvzamht1e9gcp0bs57f2f
  - is-01m44rnqpqb3fxdr4p5npk31b2
  - is-01m44rnrzq46x3k8wts9ztf075
created_at: 2026-10-04T07:36:40.896Z
updated_at: 2026-10-05T00:50:59.703Z
---
Every page inlined ~1.8 MB (0.95 MB gzip) of faces, KaTeX, kpress CSS/JS; a reader re-downloaded it on every page (measured 2026-10-04 with measure_site_pages load --network fast-4g --after index.html: 1.0-1.3 MB per page, cold or warm). Move it to content-hashed files under assets/ (devtools/site_assets.py), in phases.
