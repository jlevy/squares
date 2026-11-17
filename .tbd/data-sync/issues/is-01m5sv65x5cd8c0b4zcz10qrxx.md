---
type: is
id: is-01m5sv65x5cd8c0b4zcz10qrxx
title: "Exact-side register slice 4: n = 83 completed (irreducibility patterns, roots below the side, coefficients)"
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/specs/active/plan-2026-10-25-exact-side-register.md
labels:
  - project
dependencies: []
parent_id: is-01m5sv3xcxr02a4019fz9bbmn9
created_at: 2026-10-25T15:34:39.268Z
updated_at: 2026-10-25T15:34:39.268Z
---
Slice 4 of the exact-side register (spec docs/project/specs/active/plan-2026-10-25-exact-side-register.md; epic think-gbr2; tracker #811). Complete n = 83's degree-672 entry, measured on 25 October 2026 by devtools.kingbird_root_polynomial from the pinned square-83.svg (receipt packing/resources/web/known-best-packings/receipts/kingbird-n083-root-polynomial.json: 673 coefficients, primitive, height 724 digits, exactly one root within 1e-99 of the printed side, about 80 s):

- irreducibility over Q by factor-degree patterns modulo several primes (distinct-degree factorization over F_p; the #435 stack recorded patterns at 100003, 100019 and 100043), so `irreducible` becomes `measured`;
- the count of real roots below the side, which the source's Root index 27 states: think-chsu's question, owned under the stack's epic and not taken over here; coordinate with its owner or ask the coordinator to re-home it;
- the 673 coefficients retained as a derived fact (about 343 KB of text) if the owner approves, under the Kingbird retention policy, so the catalogue view can print them.

Price: about 3 agent-hours and a few CPU-minutes (the Descartes isolation alone was about a minute with GMP integers).
