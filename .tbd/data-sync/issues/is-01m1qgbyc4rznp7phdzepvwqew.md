---
type: is
id: is-01m1qgbyc4rznp7phdzepvwqew
title: One article body for 381/100; only the figures switch certificates
kind: task
status: closed
priority: 1
version: 2
labels:
  - explainer
  - pr-79
dependencies: []
parent_id: is-01m1qekyhf4hjcavbdm3xya0bt
created_at: 2026-09-05T00:44:17.666Z
updated_at: 2026-09-05T01:21:54.421Z
closed_at: 2026-09-05T01:21:54.420Z
close_reason: Commit 77c441c4, verified in the browser.
resolution: null
duplicate_of: null
---
Direction on PR #79. Replace the opening's expository paragraph with: 'The proof described here covers a bound of $s(11) \ge 381/100$. For illustration, some of the figures below show a looser bound $s(11) \ge 19/5$, and a toggle on the figure lets you select the tighter precision so you can compare the results.' Then drop the per-certificate stamping of prose: the article body is rendered once with the headline certificate's numbers (381/100), and only the certificate-specific figures (atoms, prover, shrink, coarsening) are stamped per certificate inside BEGIN:FIGURE/END:FIGURE blocks wrapped in <div class="cert-figure" data-cert="…" hidden>, with the switch toggling figure copies; the per-certificate scripts stay per figure set. The figures' own captions may carry their certificate's numbers. Renderer (expand over FIGURE blocks instead of ARTICLE; prose placeholders from the headline facts) and Markdown (markers around figures) change together.
