---
type: is
id: is-01m23fkwbxxcyeknacny62nhhf
title: "Certificate format cannot express two atom classes: K5 clique and K6 floor"
kind: task
status: open
priority: 1
version: 3
labels: []
dependencies: []
created_at: 2026-09-09T16:22:02.365Z
updated_at: 2026-09-10T04:30:12.414Z
---
Extend the certificate format and both covering routes to retain the weighted and floor charges already returned by the separator. Source: agenda034 lane A4 finding P10 and lane A5 F6. This is a representation and verification prerequisite, not evidence that the unconditional language or conditional route is exhausted.

Preserve distinct charge semantics. A ThresholdAtom(S,k,w) charges w*1[count>=k]. A floor atom with nonnegative integer multiplicities a, positive integer t and nonnegative w charges w*floor(a(P)/t), with budget w*floor(a(S)/t). These are not equivalent when a=1 and |S|>=2k. Use separate tagged records or an explicit charge mode; retain backward compatibility for existing frozen threshold records without reinterpreting their bytes.

Admission controls must include a 2-of-5 atom with a core containing four sites: threshold charge1 versus floor charge2. A T025 2-of-3 replay alone cannot catch the semantic mismatch. Also test zero weights/multiplicities where admitted, invalid signs and denominators, declared-budget mismatch, shared sites, closed-boundary membership, and D4 orbit accounting. The counting proof is sum_i floor(a(P_i)/t)<=floor(a(S)/t) for disjoint cores because their site traces are disjoint.

Implement exact event-cell coverage and the separately structured interval route with appropriate sound bounds. Re-decide unchanged T025/T026 through the preserved threshold mode and verify the same exact charges and budgets. Freeze a richer certificate only if its entire admissible domain passes both routes and its budget meets the declared physical counting threshold. Valid separated cuts alone do not constitute such a certificate.

The retained A5 value10 is exact for its finite final row set and an upper bound for the full rank-one closure on that fixed support. The corrected H155 conditional route remains live; this format may be useful to either strand. Primary paths use packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/.

## Notes

NARROWED 2026-09-10 (agenda-034 lane A6, and PR 139 finding on the same point).

The title and the original framing read as if the certificate format blocked separation
work in general. It does not. It blocks exactly two named atom classes:

  K5 budget-one CLIQUE atoms, which carry integer multiplicities; and
  K6 Chvatal-Gomory FLOOR atoms, whose charge exceeds one on some cores.

Everything below about those two classes stands unchanged, and so does the build list.

What is NOT blocked, and this is the correction. The route that now matters at 153/40 runs
entirely inside the existing format. Lane A6 separates six atoms from the depth-one
certificate -- two two-of-three (|S| = 3, k = 2) and four three-of-five (|S| = 5, k = 3),
budget 1 each -- and they take the blocking support from exactly 11 to 10.4210526, bracketed
exactly. All six are (S, k) threshold atoms with uniform multiplicity, which ThresholdAtom
already expresses, so every one of them is FREEZABLE AND GATEABLE TODAY. The loop that found
them deliberately discards the reader's non-uniform budget-one atoms and its Chvatal-Gomory
giants precisely because P10 showed those cannot be frozen, and it reaches 10.42 without them.

So this bead is a widening of the format for two classes, not a blocker on the live route.
Wherever the record said the format blocks separation work generally, it now names the two
classes instead: X-024 section 5 carries the narrowed statement.

Priority unchanged: the two classes are still where the reader finds its largest violations,
and a future loop whose best cut lands outside two-of-three and three-of-five still hits this
wall.
