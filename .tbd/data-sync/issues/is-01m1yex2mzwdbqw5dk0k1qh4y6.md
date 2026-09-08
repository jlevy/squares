---
type: is
id: is-01m1yex2mzwdbqw5dk0k1qh4y6
title: "squares: explainer integration of the math text face"
kind: task
status: closed
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels:
  - kpress
  - explainer
dependencies:
  - type: blocks
    target: is-01m1yex3gzj2xpc74rfrghd7bg
  - type: blocks
    target: is-01m1yex3xxxgrft8mdxgbf2pxw
  - type: blocks
    target: is-01m1yex4abjf79dwc50e4f2nrs
parent_id: is-01m1ycfpc3pv67mt54g7857vk6
hold: null
hold_until: null
created_at: 2026-09-07T17:33:22.974Z
updated_at: 2026-09-07T19:10:42.499Z
closed_at: 2026-09-07T19:10:42.498Z
close_reason: "Landed in jlevy/squares#114 (44d4e768): gitlink bump, renderer inlining of the composite and metrics, checks green."
resolution: null
duplicate_of: null
---
Bump vendor/kpress gitlink; extend inline_font_urls to ../katex/fonts/; inline katex-text-metrics.js before the page's own KaTeX calls in render_explainer.py; run render_explainer --check, render_explainer_pdf --check, check_print_layout, inspect_explainer_typography --check-supporting; confirm the Pages workflow needs no change.

## Notes

Blocked on the kpress feature landing on squares/page-fixes (kpress epic kpr-sc4f, tasks kpr-g93o, kpr-c4oz, kpr-ai4c). Unblock by bumping the vendor/kpress gitlink to the commit that carries it.
