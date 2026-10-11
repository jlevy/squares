---
type: is
id: is-01m3xrx6p081zyj7efn8tjkqw0
title: "Import wand125: linear point/segment certificates s(101) >= 257/25 and s(83) >= 187/20 (#294)"
kind: task
status: closed
priority: 2
version: 7
labels:
  - result-import
  - packing
dependencies:
  - type: blocks
    target: is-01m3yrzkz80qd1wv5sjr0kkkv0
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-02T07:40:22.080Z
updated_at: 2026-10-03T22:39:34.811Z
closed_at: 2026-10-03T22:39:34.810Z
close_reason: "T-073 n83 V3/C3 (e79ca3ac7) and T-080 n101-105 V3/C3 on main via #327 (9927035b6)."
resolution: null
duplicate_of: null
---
Result import process, I. New certificate kind: point masses + uniform segments + rectangles, D4, mass n - 1/100000, checked by code/unified_linear_verify.cpp (the verifier of mixed_n50_L735), 201 net angles. n101 at af1db07, n83 at 0c35d90; n82 (9.32) announced. Stage 2 packet, stage 3 entry V0/C0, stage 4 replay + review (new checker: review needed). Compared with Green G_10 = 10.2467.

## To finish (validation backlog, 2026-10-02)

T-073 (linear certificates at n = 83 and 101..105, V0/C1). From packing/: `.venv/bin/python3 -m devtools.audit_wand125_linear linear-replay n101 --range A-B --work W --workers 4` over all 201 angles (`linear-plan n101 --parts 4`), likewise n83, then `linear-merge n101`, `linear-merge n83`, and `linear-control n101 --work W`, each merged receipt keeping each direction's least lower bound (finding LC-4). Packet resources/web/wand125-linear-certificates-2026-10-02/. Expected CPU: 8.1 (n101) and 23.0 (n83) CPU-hours by `linear-price`. Refutes: an angle unified_linear_verify.cpp refuses, or a replay not matching the shipped record. Moves the rung: both merged receipts recorded as replayed-here entries derive V3/C3. mixed_n83_L937 (think-r7yt) raises n = 83's reported value; T-073 stays true as stated. Run `uv run --frozen --all-extras --group dev python -m devtools.check_results`.

## Notes

2026-10-03 06:05 l83 (session_01PADmST5bjm6g2wbCbc2gbK): first launch failed from the wrong directory; 0-90 relaunched 04:52Z and running; then 91-152, 153-200, linear-merge, linear-control. Branch claude/replay-wand125-linear-n83 has no receipts yet.
2026-10-03 21:05 Follow-up PR #327 (182776349): T-076 n82 linear V3/C3 (six ranges, 30.74 CPU-h; n82 verified 233/25) and T-073 n83 linear V3/C3 (26.15 CPU-h; no case moves, T-075 higher), plus think-sfbj reply records. After merge: final note on #294 to @wand125 (n82, n83 confirmed) and close #294.
