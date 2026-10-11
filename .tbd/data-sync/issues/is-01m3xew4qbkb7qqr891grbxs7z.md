---
type: is
id: is-01m3xew4qbkb7qqr891grbxs7z
title: "Import wand125: mixed rectangle-measure certificates at n = 84, 85 (#282 comment of 2026-10-02)"
kind: task
status: closed
priority: 2
version: 4
labels:
  - result-import
  - packing
dependencies: []
parent_id: is-01m3yrzkz80qd1wv5sjr0kkkv0
created_at: 2026-10-02T04:45:01.547Z
updated_at: 2026-10-03T22:47:15.035Z
closed_at: 2026-10-03T22:47:15.034Z
close_reason: T-071 V3/C3 on main.
resolution: null
duplicate_of: null
---
Result import process. Stage 2 done: packet packing/resources/web/wand125-mixed-bounds-2026-10-02/ at 52af997 (PR #298). Stage 3: new register entry at V0/C0 (a later release adding counts). Stage 4: replays on cloud runners m2 (n84) and m3 (n85); review docs/project/reviews/review-2026-10-02-wand125-mixed-rectangle-bounds.md. Note wand125 has since pushed af1db07 (mixed_n101_L1028, another verifier) with no request yet.

## To finish (validation backlog, 2026-10-02)

T-071 (s(84) >= 47/5, s(85) >= 471/50, V0/C1). From packing/: `.venv/bin/python3 -m devtools.audit_wand125_point_and_mixed mixed-replay n84 --range A-B --work W --workers 4` over all 201 angles (split with `mixed-plan n84 --parts 3`), likewise n85, then `mixed-merge n84` and `mixed-merge n85`, and `mixed-control n84 --work W`. Packet resources/web/wand125-mixed-bounds-2026-10-02/. Expected CPU: 11.7 and 10.2 CPU-hours by `mixed-price` (budget twice the wall on a busy guest). Refutes: an angle the checker refuses (exit 1), or a replay not matching the shipped record. Moves the rung: each merged receipt recorded as a replayed-here source-replay entry derives V3/C3. mixed_n85_L946 (think-r7yt) raises the reported value at n = 85; T-071 stays true as stated and still needs its own replay. Run `uv run --frozen --all-extras --group dev python -m devtools.check_results`.
