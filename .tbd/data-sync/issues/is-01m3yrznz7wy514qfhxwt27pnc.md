---
type: is
id: is-01m3yrznz7wy514qfhxwt27pnc
title: "T-007: record the Nagamochi Lemma 1 defect, re-derive the values it supplies (#295)"
kind: task
status: closed
priority: 1
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m3yrzkz80qd1wv5sjr0kkkv0
hold: null
hold_until: null
created_at: 2026-10-02T17:00:57.703Z
updated_at: 2026-10-06T10:22:37.641Z
started_at: 2026-10-06T07:56:25.542Z
closed_at: 2026-10-06T10:22:37.641Z
close_reason: "Complete on main since #305: E-nagamochi-lower is defect-found and T-007 incomplete at V0/C1; audit_t007_consumers shows the operative bound cites E-nagamochi-lower at 0 of 324 cases; check_nagamochi_bounds re-derives the 203 floors from Karakuş (6.1). Verified by lane R6 on 2026-10-06."
resolution: null
duplicate_of: null
---
T-007 registers Nagamochi 2005, Theorem 2 (V3/C1; the 2026-08-30 read left four items unverified). #295 (wand125) and PR #305's review (session-168) find Lemma 1 false for every a > 3, b > 2 (Karakuş's family, exact; chelokot's Lean counterexample, a square of side 1.0001 in the 4 x 4 container scoring 0.977543 < 1), so the published proofs of Theorem 1 and Theorem 2 are incomplete. Nobody has shown the bound false.

How to finish:
1. The owner decides on PR #305's review (think-bmze answers #295 meanwhile).
2. Record the defect: a mapped review document listed in T-007's `reviews` with verdict defect-open, or `external_review.state: defect-found` on E-nagamochi-lower. Either makes T-007 `incomplete` (`python -m devtools.result_status --list`); run `uv run --frozen --all-extras --group dev python -m devtools.check_results`.
3. Re-derive every value T-007 supplies (46 operative verified-field values, 63 cited by #295) from what is proved: replayed certificates already above it, chelokot's kernel-checked s(n^2 - 2) = n and Karakuş's s(k^2 - 1) = k and 1/2 + sqrt(N - floor(sqrt N) + 1/4), each imported as its own entry first (result-import.md). `packing-validate --only "the borrowed lower bounds re-derive"` holds the case records to the closed form (devtools.check_nagamochi_bounds).
Expected CPU: none beyond the gate; the work is a review decision and record edits.
What refutes: a counterexample to the bound itself (no one has one). The Lemma 1 defect makes the result incomplete, not refuted.
What moves the rung: C3 needs a machine check of a corrected capacity argument for Theorem 1 (think-8y1g's lambda = 1 spike is one input). Without it T-007 stays C1, recorded incomplete, and the case records cite the replacements.

## Notes

2026-10-06 (lane R6): every "how to finish" step is done on main since #305 (4 October), checked again on ebf232767.
1. The owner decided #305's review; it merged.
2. The defect is recorded. E-nagamochi-lower has external_review.state defect-found (2026-10-02), and result_status --list gives T-007 as incomplete, V0/C1.
3. The values are re-derived. audit_t007_consumers --report: the operative verified lower bound cites E-nagamochi-lower at 0 of 324 cases, all 324 unaffected with or without Karakuş. check_nagamochi_bounds: 203 floors re-derived from Karakuş's (6.1) and 175 reported values from Theorem 2, all agreeing; operative citations 0.
Both replacement sources are registered: Karakuş as T-083 and T-084, and chelokot as T-086 (C3).
What remains is T-007's own next rung, a machine check of a corrected Theorem 1 at full strength. That is research, not this bead's close condition.
Recommend closing at R6's merge.
