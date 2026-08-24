---
type: is
id: is-01m0tkxd8xsmw435t9f8srm6sz
title: Certify the n=5 equal-side pair shares one exact LP face
kind: task
status: closed
priority: 0
version: 3
spec_path: explorations/packing/campaign/agendas/agenda-001-basin-confidence-ladder.md
delegate: unknown@spud10.local
labels:
  - packing
  - basin-cartography
  - research
dependencies: []
parent_id: is-01m0r3zv2hh2jj64rb8mhqbtre
hold: null
hold_until: null
created_at: 2026-08-24T19:28:17.180Z
updated_at: 2026-08-24T19:46:35.003Z
started_at: 2026-08-24T19:28:23.171Z
closed_at: 2026-08-24T19:46:34.990Z
close_reason: Completed by 26360f1, 07a7f96, and ccec7e2. Exp-033 binds golden seeds 2 and 5 to exact Q(sqrt(2)) endpoints after a declared D4 action and relabelling; exact validity, a common 30-row fixed-angle cell, an exact LP dual, and active nullities 0/1/0 certify one connected optimal face. Generation plus independent replay costs 0.24s; the full 30-step gate passes in 30s. Scope remains fixed-angle only.
resolution: null
duplicate_of: null
---
Bounded BC-010 first pair. Reconstruct golden seeds 2 and 5, bind them to exact Q(sqrt(2)) poses after an explicit D4 transform and relabelling, and test whether one common fixed-angle cell contains an exact side-constant path. Acceptance: exact endpoint validity, exact common-cell feasibility for the full parameter interval, an exact LP dual proving the shared side is optimal in that cell, exact interior rank/nullity, independent replay, and a mutation that breaks the path. Scope the result to the fixed-angle optimal face; do not infer full nonlinear stationarity, basin mass, or census completeness.
