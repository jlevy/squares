---
type: is
id: is-01m4xpwdwtx923hcd9y50kymez
title: "Validate: decide the ledger's 21 undecided PR #574 comparisons exactly (17 computable, 4 lack an exact side; <0.1 CPU-h)"
kind: task
status: open
priority: 2
version: 1
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4wsqt2sjrksybyz375sarb3
created_at: 2026-10-14T17:20:41.370Z
updated_at: 2026-10-14T17:20:41.370Z
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
