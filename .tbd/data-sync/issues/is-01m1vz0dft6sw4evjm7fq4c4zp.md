---
type: is
id: is-01m1vz0dft6sw4evjm7fq4c4zp
title: Guard cutting separation and retained scaled bounds outside the floating-point envelope
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m1vyfpzegaxyp52t4bfx85md
created_at: 2026-09-06T18:17:06.298Z
updated_at: 2026-09-06T18:50:57.029Z
closed_at: 2026-09-06T18:50:57.029Z
close_reason: "Implemented in PR #100 on codex/adversarial-review-fixes. Final commit 237d9386 passed hosted CI and pre-push validation; counterexample regressions and the 20000-case independent oracle replay passed. The separate missing-witness follow-up think-aenh remains open under epic think-hmtc."
resolution: null
duplicate_of: null
---
The D-473 exact large-coordinate family has true depth 2e21, while cutting.depths_above returns no violations and maximum zero. run_cutting uses separation.max_depth to retain best_scaled_total before final ceiling verification, so intermediate exact lower-bound claims remain exposed. Apply justified screening or exact fallback to cutting separation and add the reproducer. This is part of the published-core adversarial review remediation.
