---
type: is
id: is-01m1w4ky0appzkx55hce6cwm6d
title: "PR #100 review R3: sweep oracle discards verify_claim's witness centre"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1w4krded865yyd393yn5my5
created_at: 2026-09-06T19:55:08.682Z
updated_at: 2026-09-06T19:55:30.689Z
closed_at: 2026-09-06T19:55:30.689Z
close_reason: Fixed in d663da6d on the PR branch.
resolution: null
duplicate_of: null
---
packing/devtools/check_fractional_sweep.py compare_case ignored the returned centre, so the only guard on the witness was verify_claim's own self-check. Now checks admissibility and direct mass. Fixed in d663da6d.
