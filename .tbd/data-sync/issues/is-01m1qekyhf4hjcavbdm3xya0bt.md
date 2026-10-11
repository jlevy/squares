---
type: is
id: is-01m1qekyhf4hjcavbdm3xya0bt
title: "Certificate page: the article is written in Markdown and math, formatted by flowmark, rendered by kpress"
kind: epic
status: closed
priority: 1
version: 15
labels:
  - explainer
  - pr-79
  - kpress
dependencies: []
parent_id: is-01m1pnpwvpjydts81pffmp1nt7
child_order_hints:
  - is-01m1qetyf74k13wjcjg2g7h0k4
  - is-01m1qetyt6c0fdnz8e8e0x4f64
  - is-01m1qetz5309tjmjz9xtd2bmq6
  - is-01m1qetzfmdebbpwyndp0r04bn
  - is-01m1qf8k3hmest4sspvcntae9s
  - is-01m1qftmrhbdfp5t6nr5jvjsrt
  - is-01m1qg06zaztgchtzp7brgse9j
  - is-01m1qg07ansgqkzh7xrv7h7mz0
  - is-01m1qg6n672ctfv617p88ahwsf
  - is-01m1qg6njkp049tx31g4jsg5dw
  - is-01m1qg6ny5eqkwqhx7b50ykv97
  - is-01m1qgbyc4rznp7phdzepvwqew
created_at: 2026-09-05T00:13:42.830Z
updated_at: 2026-10-06T08:34:57.183Z
closed_at: 2026-10-06T08:34:57.183Z
close_reason: "Done: all 12 children are closed; the explainer article is Markdown with LaTeX math, formatted by flowmark and rendered by kpress (packing/devtools/templates/n11-lower-bounds-explainer-article.md and render_n11_lower_bounds_explainer.py on origin/main)."
resolution: null
duplicate_of: null
---
Direction on PR #79. The prose leaves the HTML template for a Markdown source with $…$ math, [^n] footnotes and {{placeholders}} for derived numbers, with the interactive figures as raw HTML blocks; flowmark-rs 0.4.0 formats it (math spans stay whole); the renderer substitutes per certificate and renders through kpress's Markdown renderer, then stitches in the scripts. The HTML template shrinks to a shell (head, styles, scripts).
