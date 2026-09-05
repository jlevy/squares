---
type: is
id: is-01m1qf8k3hmest4sspvcntae9s
title: "Certificate page: Figure 2 shows both bounds on one number line, with no switch"
kind: task
status: open
priority: 2
version: 1
labels:
  - explainer
  - pr-79
dependencies: []
parent_id: is-01m1qekyhf4hjcavbdm3xya0bt
created_at: 2026-09-05T00:24:59.247Z
updated_at: 2026-09-05T00:24:59.247Z
---
Review feedback on PR #79. The number line becomes shared: the prior bound 3.788854…, a mark for each certificate (19/5 = 3.8 and 381/100 = 3.81), the best known packing 3.877084…, and the band from the headline bound to the packing. It leaves the per-certificate block, so it has no switch; the renderer emits the marks for every certificate (as coarsening_svg does for bars) and the caption's gap figures come from the headline. Done inside the renderer refactor to Markdown.
