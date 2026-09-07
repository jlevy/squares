---
type: is
id: is-01m1yex0s2g4tnkv0y6yvzj8t8
title: "kpress: metrics generator devtool and katex-text-metrics.js asset"
kind: task
status: closed
priority: 2
version: 5
spec_path: vendor/kpress/docs/math-text-face.plan.md
labels:
  - kpress
dependencies:
  - type: blocks
    target: is-01m1yex25m1041rt6630t2r02p
  - type: blocks
    target: is-01m1yex2mzwdbqw5dk0k1qh4y6
parent_id: is-01m1ycfpc3pv67mt54g7857vk6
created_at: 2026-09-07T17:33:21.057Z
updated_at: 2026-09-07T17:43:59.040Z
closed_at: 2026-09-07T17:43:59.039Z
close_reason: Moved to the kpress tracker as kpr-g93o (the feature lives in vendor/kpress on squares/page-fixes; see vendor/kpress/docs/math-text-face.plan.md).
resolution: canceled
duplicate_of: null
---
devtools/katex_text_metrics.py in kpress: read katex.min.js base tables and the reading-face woff2 files, rewrite the swapped code points (digits and Latin letters) with depth, height, italic overhang and width, keep skew; write static/katex/katex-text-metrics.js defining globalThis.kpressKatexTextMetrics; --check for freshness wired into make lint; fontTools in the dev group.
