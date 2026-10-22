---
type: is
id: is-01m5jr2fjt4wp8zryw7wceq0hw
title: Retry cross-document view transitions on real hardware
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m5jr2cr74kbbn71j05pqsgkd
created_at: 2026-10-22T21:25:31.354Z
updated_at: 2026-10-22T21:25:31.354Z
---
@view-transition {navigation: auto} with view-transition-name on the header was tested 2026-10-22 in headless Chromium (software rendering): first frame 0.8-1.2 s after the click even with prerender, versus ~30 ms without. Likely exaggerated by headless compositing; re-measure on a GPU-backed browser after prerender lands before adopting.
