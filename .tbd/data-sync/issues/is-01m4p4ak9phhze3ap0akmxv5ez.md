---
type: is
id: is-01m4p4ak9phhze3ap0akmxv5ez
title: "Take exact verification out of the renderer hub: read the n=84 Ryxu history from a leaf module (PR #507 review A4)"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-10-10-website-development-loop.md
labels:
  - packing
dependencies: []
parent_id: is-01m4ke1dkg5m43rszjm49ar77r
created_at: 2026-10-11T18:41:41.669Z
updated_at: 2026-10-11T18:41:41.669Z
---
From PR #507 review A (https://github.com/jlevy/squares/pull/507#pullrequestreview-5484457606), finding A4 (Medium), deferred.
PR #507 made every attributed edit-tier step claim the static import closure of what it runs (fixing #496 review G1). `exact verification` reaches the site-renderer import cycle through one function-local import: packing/cases/gobel_strip/verify_exact.py (n == 84 branch) imports `devtools.register_ryxu_reports.read_history`, and register_ryxu_reports imports `render_case_verifiers`, a hub member. So the step now claims `packing/devtools/*` and runs for every devtools edit.
Measured by review A: one-file devtools edit selects 21 of 65 prerequisites instead of 10; `exact verification` alone costs 118.2 s at --jobs 2 and the other ten added steps 59.5 s; over a 40-merge replay the mean selection rose 44.9 -> 48.1 of 65 and pushes selecting <=25 steps fell 14 -> 11.
Fix: move `read_history` (and whatever it needs) into a leaf module with no renderer imports, point verify_exact.py and register_ryxu_reports.py at it, drop `_RENDERER_HUB` from the `exact verification` touches, and let test_every_attributed_step_claims_the_modules_it_runs confirm the narrower closure. verify_exact.py is scientific verification code: keep its behaviour byte-identical (same witness read for n = 84) and check whether any receipt or audit binds its bytes before editing.
