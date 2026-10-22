---
type: is
id: is-01m5jr2gpy49zr55rdh1cqaghc
title: Fewer render-blocking stylesheets per page
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m5jr2cr74kbbn71j05pqsgkd
created_at: 2026-10-22T21:25:32.510Z
updated_at: 2026-10-22T21:25:32.510Z
---
Every page links 11-12 stylesheets (~400 KB uncompressed: kpress 162 KB, site 137 KB). GitHub Pages serves max-age=600, so after ten minutes each navigation revalidates every one before first paint. Concatenating the shared sheets into one would turn that into a single conditional request.
