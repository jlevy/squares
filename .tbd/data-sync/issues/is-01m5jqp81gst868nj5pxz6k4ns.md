---
type: is
id: is-01m5jqp81gst868nj5pxz6k4ns
title: "check_added_blobs: skip the per-blob zlib pass for blobs whose stored_size_bound is under the per-blob ceiling (#461 near the 30 s deadline under load)"
kind: task
status: open
priority: 3
version: 1
labels:
  - performance
dependencies: []
created_at: 2026-10-22T21:18:50.415Z
updated_at: 2026-10-22T21:18:50.415Z
---
From #406's lane (21:20Z 22 Oct): in a working clone at load 6-7, #461's guard run took 23.6-30.2 s against the 30 s deadline; the pack was 1.8 s of it, the rest the per-blob zlib pass. At load 2 it took 18 s. Skipping blobs whose stored_size_bound is already under the per-blob ceiling would cut most of the pass. Measure on CI's fresh clone (the reference, per review K2).
