---
type: is
id: is-01m1qetyt6c0fdnz8e8e0x4f64
title: "Markdown article: the renderer reads the Markdown and renders it through kpress"
kind: task
status: open
priority: 1
version: 4
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
parent_id: is-01m1qekyhf4hjcavbdm3xya0bt
created_at: 2026-09-05T00:17:32.485Z
updated_at: 2026-09-05T00:41:25.188Z
---
render_certificate_page.py stamps the ARTICLE block per certificate inside the Markdown, substitutes placeholders, renders once with kpress.format.markdown.parse_markdown (trusted, math auto), and inserts the body into an HTML shell that keeps head, styles and scripts. The page's boot typesets kpress's math markup (.kpress-math-render, stripping \( \) and \[ \]) alongside .tex spans; CSS targets h2 instead of .section-head; the old template shrinks to the shell. Waits on the exactness pass, which edits the same renderer.
