---
type: is
id: is-01m1qetyt6c0fdnz8e8e0x4f64
title: "Markdown article: the renderer reads the Markdown and renders it through kpress"
kind: task
status: closed
priority: 1
version: 6
labels:
  - explainer
  - pr-79
dependencies:
  - type: blocks
    target: is-01m1qf8k3hmest4sspvcntae9s
  - type: blocks
    target: is-01m1qg6n672ctfv617p88ahwsf
  - type: blocks
    target: is-01m1qg6ny5eqkwqhx7b50ykv97
  - type: blocks
    target: is-01m1qgbyc4rznp7phdzepvwqew
parent_id: is-01m1qekyhf4hjcavbdm3xya0bt
created_at: 2026-09-05T00:17:32.485Z
updated_at: 2026-09-05T01:15:13.469Z
closed_at: 2026-09-05T01:15:13.468Z
close_reason: Commit b5e81669.
resolution: null
duplicate_of: null
---
render_certificate_page.py stamps the ARTICLE block per certificate inside the Markdown, substitutes placeholders, renders once with kpress.format.markdown.parse_markdown (trusted, math auto), and inserts the body into an HTML shell that keeps head, styles and scripts. The page's boot typesets kpress's math markup (.kpress-math-render, stripping \( \) and \[ \]) alongside .tex spans; CSS targets h2 instead of .section-head; the old template shrinks to the shell. Waits on the exactness pass, which edits the same renderer.
