---
type: is
id: is-01m1q3fnfcc4fczm88xazv21kq
title: "kpress: name the tint roles instead of open-coding color-mix"
kind: task
status: open
priority: 2
version: 3
labels:
  - kpress-upstream
dependencies: []
parent_id: is-01m1q3fmvn9py28rcm0q3jadvk
created_at: 2026-09-04T20:59:08.139Z
updated_at: 2026-09-04T21:00:06.772Z
---
kpress open-codes `color-mix` on its own doc roles at 16 sites across `components.css` and `document.css`, at 12 distinct percentages of four roles: link at 8/10/20/72%, danger at 8/10/42/45/84%, muted at 18/45/70/85%. Two are the same intent at different strengths (danger 10% fill against danger 45% border in `.kpress-math`), so the inconsistency already sits inside kpress, not only in consumers. Building `packing/devtools/templates/certificate_page.html` here meant writing the same expression again for accent and danger washes.

Proposal: name the recurring tints as tokens beside the roles they derive from in `style-tokens.css` (`--kpress-doc-accent-wash`, `--kpress-doc-danger-wash`, `--kpress-doc-danger-edge`) and use them at the existing sites. Consumers then tint by role name instead of guessing a percentage.
