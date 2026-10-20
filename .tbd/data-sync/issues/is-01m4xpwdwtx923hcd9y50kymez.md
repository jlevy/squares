---
type: is
id: is-01m4xpwdwtx923hcd9y50kymez
title: "Validate: decide the ledger's 21 undecided PR #574 comparisons exactly (17 computable, 4 lack an exact side; <0.1 CPU-h)"
kind: task
status: closed
priority: 2
version: 4
delegate: serene-hopper-vcheap
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4wsqt2sjrksybyz375sarb3
hold: null
hold_until: null
created_at: 2026-10-14T17:20:41.370Z
updated_at: 2026-10-14T20:27:02.577Z
started_at: 2026-10-14T17:41:54.453Z
closed_at: 2026-10-14T20:27:02.575Z
close_reason: "17 of 21 comparisons decided exactly and fed into the ledger, on main with #605 (77fa15c7e). The #574 and #593 comments are edited. T-174's text is in the post-#602 records bead. 29, 55, 71 and 83 stay gated."
resolution: null
duplicate_of: null
---
Exact comparisons left undecided by the 2026-10-14 ledger (packing/campaign/issue-intake/upper-bounds-20261014/README.md, Undecided Comparisons): 21 rows, all PR #574 (PingYou Ltd) against the reported lane or a pending register entry. Cheap exact checks; each could change a verdict from undecided to recorded or not recorded.

## Validation
- Claim: at each row, whether PR #574's side (the pr574 lane's claims.json or algebraic-claims.json at claude/wizardly-meitner-wqn4x3-intake-1014-pr574 56cf868c6, or the PR's own v2 certificate at 17 and 29) is below, equal to or above the standing member.
  - Reported lane given by a minimal polynomial in the case record, root at its print (11 rows): 17 (degree 18), 28 (6), 37 (8), 39 (5), 41 (42), 69 (38), 87 (41), 128 (40), 205 (40), 235 (83), 300 (40).
  - Reported lane the closed form k - (1/2)sqrt(2) + sqrt(1 + sqrt(2)) (k = 7, 10, 13), against PR #574's quartic side (3 rows): 54, 107, 178.
  - Pending register entries' exact sides (3 rows): 106 (T-121, degree 32), 152 (T-122, degree 40), 177 (T-123, degree 32), each with its retained rational root interval.
  - No exact form of the reported lane in the record (4 rows): 29, 55, 71, 83. The case records hold only the Kingbird print (reported_upper_bound exact_form and minimal_polynomial null).
- Run: isolate each root by exact sign change at the case record's minimal polynomial (or the register entry's), compare exactly with PR #574's side (rational, or algebraic by its minimal polynomial and isolating interval), and feed the result to devtools.intake_ledger (ledger.yaml's exact sides) so `render` and `render --check` carry the verdicts; keep the program and output in the ledger's review/ directory.
- Cost: not measured; expected well under 0.1 CPU-h (root isolation of polynomials of degree at most 83, and comparisons at a few hundred digits).
- Budget status (owner, 2026-10-14): runnable (<= 40 CPU-h) for 17 rows; the 4 rows at 29, 55, 71, 83 are gated on a missing input.
- Possible <= 40 CPU-h subset: n/a.
- Depends on: for 29, 55, 71, 83, an exact side for the reported lane's packing, which the record lacks (at 29, Evan Daniel's degree-7213 minimal polynomial of #545 is unpublished, think-6gti); for 106, 152, 177, T-121 to T-123's retained root intervals. No owner decision.
- Done when: the 17 rows are decided and the ledger re-rendered with them, the 4 rows are listed with the input each needs, and the verdicts are handed to the records lane (think-a30g); noted on think-9v2k's lane by message, not by editing it.
- Machine note: 4 CPUs shared with gates; a run > 2 wall-h should be scheduled outside a validation gate. Seconds to minutes.

## Notes

2026-10-14 validation lane vcheap (serene-hopper-vcheap), branch lane/validation-cheap, commit 5aae19033 (not pushed). Ledger and intake directory not edited (another lane owns them).

Tool: new devtools.decide_undecided_comparisons (tests/test_decide_undecided_comparisons.py, 18 tests incl. one slow full re-derivation and an mpmath second route at 28, 37, 39). Exact only: record root = Sturm-isolated root of the case record's minimal_polynomial in [print - 1 ulp, print + 1 ulp] (one root certified in each window), or T-121..T-123's polynomial_ascending in its retained reported_root_interval (reported-catalogue.json, one root each); PR #574 rational vs root by one sign; PR #574 quartic witness vs closed form k - (1/2)sqrt(2) + sqrt(1 + sqrt(2)) in sqpack.field.NumberField (equal iff the closed form minus 7/10/13 is a root of 4x^4 - 12x^2 + 16x - 7 inside the witness's isolating interval: it is). Cost 5.2 CPU-s.

Inputs: PR #574 sides from the pr574 lane at 56cf868c6 (acquisition/claims.json exact_side; facts/alg-n-054/107/178) and, at 17, PR #574's own claims.json at 4c319c2 rows[17].side_exact, checked equal to s_exact of numerical-refinements/certificates/n017.cert.json (sha256 c2742c91, as the row names) in the v2 archive (ced04297...). Kept in packing/campaign/issue-intake/upper-bounds-20261014-undecided-sides.json because that lane's packet is not on main.

Receipt: packing/campaign/issue-intake/upper-bounds-20261014-undecided-resolved.json (relation = PR #574 vs standing; margin = PR - standing, rigorous bounds):
17 above 1.28e-93 | 28 above 4.49e-95 | 37 above 2.19e-90 | 39 above 1.03e-90 | 41 above 1.19e-89 | 54 equal 0 | 69 above 2.19e-89 | 87 above 1.99e-89 | 106 (T-121) above 1.01e-94 | 107 equal 0 | 128 above 2.60e-89 | 152 (T-122) above 1.01e-94 | 177 (T-123) above 1.39e-64 | 178 equal 0 | 205 above 1.13e-94 | 235 above 1.30e-94 | 300 above 1.21e-94.
Counts: 14 above, 3 equal, 0 below: no row makes PR #574 stronger than the standing member. Gated, listed in the receipt with the input each needs: 29 (Daniel's degree-7213 polynomial, #545, think-6gti), 55, 71, 83 (case records hold only the Kingbird print).

Remaining (not this lane's): feed the receipt to devtools.intake_ledger and re-render (the ledger lane); hand verdicts to the records lane (think-a30g); message think-9v2k's lane. Bead left open for those. The bead's Run said to keep program and output in the ledger's review/ directory; per the coordinator's brief they are in devtools/ and beside the intake directory instead.
