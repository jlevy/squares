---
type: is
id: is-01m4jk4be5gt8mqhrhkaytes7f
title: "Import squarepacker: c*(k) < 43.06 k^{3/8} + 2e-5 (k >= 4e26) and c*(k) < 20.668 k^{2/5} + 0.623 (k >= 1.6e7) (#471)"
kind: task
status: in_progress
priority: 1
version: 2
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
hold: null
hold_until: null
created_at: 2026-10-10T09:43:27.941Z
updated_at: 2026-10-10T09:49:28.458Z
started_at: 2026-10-10T09:49:28.457Z
---
Issue https://github.com/jlevy/squares/issues/471 (opened 2026-10-09). Preprint Zenodo 10.5281/zenodo.23256655 v1.0 and squarepacker/k2-minus-c-upper. Theorems 1.1, 1.2, 1.4 (c*(k) <= 8 ceil(sqrt(k-4)) - 1, k >= 6) and 1.6 (finite c*(10^5..10^8) bounds with packings as data). Relates to X-049, asymptotic-waste-bounds.yaml and #414's lower bounds (think-6ptr, think-u1kq). Stage 1 triage and the mathematical review by Fable at max; interval-arithmetic replay priced before any run.
