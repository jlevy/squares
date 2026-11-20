---
type: is
id: is-01m7x4914zvkckwd7k2jn37x5a
title: "Validation: census of the measures issue 1039 inherits at 38, 40, 41, 43, 51, 90, 92 (T-200..T-204, T-212, T-213), ~34 CPU-h, after think-f40c"
kind: task
status: open
priority: 2
version: 1
labels:
  - validation
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
created_at: 2026-11-20T18:42:36.831Z
updated_at: 2026-11-20T18:42:36.831Z
---
Found in think-fv42 (20 November 2026): issue 1039's certificates inherit, for some directions, coverage rows of Hosono's measures in this repository's sqverify-fast census format. devtools.compare_inherited_coverage matched 19 of the 36 evidence sets with such rows to census files row for row (n19, 20, 26-31, 37, 39 at 2,073 directions; 68, 84, 85 at 201). 17 match no census file: published/refined n38, 40, 41, 43, 51 (2,073 directions; T-200 to T-204's measures), n86, 88, 89, 90, 91, 92, 106, 107, 110 (201; T-208 to T-213, T-215, T-217's). The current T-337 claims at 38, 40, 41, 43, 51, 90 and 92 rest on them and stay below C3 until this runs.

## Validation
- Claim: the inherited coverage of T-337 at 38, 40, 41, 43, 51, 90, 92 (and of its superseded counts at 86, 88, 89, 91, 106, 107, 110): the measures of T-200 to T-204, T-212, T-213 (and T-208 to T-211, T-215, T-217) as Hosono published them, decided by sqverify-fast.
- Run: the sqverify-fast census of those measures, which think-f40c already holds for T-200 to T-217 with whole-net controls; then devtools.compare_inherited_coverage on the 17 sets, expecting every inherited row equal to a census row.
- Cost: 5.95G nodes for the seven current counts and 1.00G for the rest in the inherited rows, about 34 CPU-hours for the captures at T-327's census rate (4,624 CPU-s for 266M nodes); think-f40c prices the census with controls at 68.8 CPU-hours for T-200 to T-204, T-212 and T-213.
- Budget status: gated on think-f40c; the comparison itself costs minutes.
- Possible subset under the cap: the seven current counts first (about 29 CPU-hours of capture).
- Depends on: think-f40c's census runs; PR #1051 merged.
- Done when: every inherited row of the 17 sets equals a census row, and T-337's replay evidence covers 38, 40, 41, 43, 51, 90 and 92.
- Machine note: sqverify-fast census, CPU only.
