---
type: is
id: is-01m1yex1kxj181nwapj400tray
title: "kpress: math_text_font option, attribute stamping, asset wiring, init hook"
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
created_at: 2026-09-07T17:33:21.916Z
updated_at: 2026-09-07T17:43:59.698Z
closed_at: 2026-09-07T17:43:59.697Z
close_reason: Moved to the kpress tracker as kpr-ai4c (the feature lives in vendor/kpress on squares/page-fixes; see vendor/kpress/docs/math-text-face.plan.md).
resolution: canceled
duplicate_of: null
---
RenderOptions.math_text_font (prose|katex, default prose), document options, page.html.jinja data-kpress-math-text, public contract; add katex-text-metrics.js to KATEX_JS_ASSETS before katex-init.js; katex-init.js applies katex.__setFontMetrics per face before renderMathInElement when the attribute is prose and the font mode is not system.
