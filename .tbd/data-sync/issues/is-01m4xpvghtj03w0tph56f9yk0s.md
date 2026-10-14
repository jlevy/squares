---
type: is
id: is-01m4xpvghtj03w0tph56f9yk0s
title: "Validate: Fang's 11 direct certificates s(421)..s(814) at 078789a, both exact routes, certify + check --replay (~3.0 CPU-h; running)"
kind: task
status: closed
priority: 1
version: 3
delegate: serene-hopper
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4wt4ehr9401mzvgm1n3br4v
created_at: 2026-10-14T17:20:11.322Z
updated_at: 2026-10-14T20:27:01.531Z
closed_at: 2026-10-14T20:27:01.530Z
close_reason: "Replay of Fang's 11 other direct certificates (421-814) landed on main with #605 (merge 77fa15c7e): all 14 pass both routes, all 28 controls are refused, 1.54 CPU-h of routes; receipts are per count."
resolution: null
duplicate_of: null
---
Validation part of think-7bw3 (Kevin Fang's direct certificates at TheSnakeFang/squarepack-certs 078789a). Split out so the validation backlog reads on its own; RUNNING now.

## Validation
- Claim: the 11 beyond-horizon upper bounds s(n) <= the exact side of nNNNN/nNNNN.cert at TheSnakeFang/squarepack-certs 078789a4cfd36f915f1bfbe76d742413d79b2965, for n = 421, 422, 463, 464, 507, 508, 553, 601, 651, 758, 814 (published at e646c47 and c284cd0; printed sides in think-7bw3's notes). 380, 381 and 382 are already replayed (9 jobs, receipt in the packet).
- Run: from packing/, `uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports fang-direct-certificates-2026-10-13 certify --jobs-dir DIR --workers 1` over the 11 counts (positive, duplicate-square and outside-container jobs on both maintained exact routes: sqpack's exact witness verifier and the independent rational corner checker), then `certify --finished`, then `... fang-direct-certificates-2026-10-13 check --replay`. Packet packing/resources/web/fang-direct-certificates-2026-10-13/ (the certificates are retained there; digests in acquisition/sources.json).
- Cost: 3.02 CPU-h. 10,865,736 pair decisions in each of certify and check --replay (1.51 CPU-h each) at 5.0e-4 route CPU s per decision, measured on 380-382 on 2026-10-14 (652.11 s for 1,303,026 decisions; think-7bw3 notes). About 4.0 h of one-worker wall at load 6-10, up to 5.8 h.
- Budget status (owner, 2026-10-14): runnable (<= 40 CPU-h). RUNNING: coordinator serene-hopper, worktree /home/user/squares-wt/fang-certs (branch lane/fang-certs-replay). Do not start a second run.
- Possible <= 40 CPU-h subset: n/a (runnable as a whole).
- Depends on: nothing. The 14 beyond-horizon rows are registered in the 14 October records PR (#602), verified at 380-382 and reported at these 11.
- Done when: all 11 positives pass both routes, all 22 controls are refused by both, check --replay equals the retained rows, the receipt (receipts/exact-certification.json.xz of the packet) is committed, and the 11 rows' evidence moves to verified; the result is noted on think-7bw3.
- Machine note: 4 CPUs shared with gates; a run > 2 wall-h should be scheduled outside a validation gate. This run is about 4 wall-h on one worker. Each 814 job takes about 331 CPU s and up to 634 s of wall at the worst ratio seen (1.92), against the kernel's fixed 600 s JOB_TIMEOUT (each 758 job up to 550 s); decide-job per job, then certify --finished, is the recovery the couzo and PR #574 lanes used.
