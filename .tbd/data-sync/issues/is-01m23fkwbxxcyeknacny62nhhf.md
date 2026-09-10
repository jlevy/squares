---
type: is
id: is-01m23fkwbxxcyeknacny62nhhf
title: "Certificate format cannot express two atom classes: K5 clique and K6 floor"
kind: task
status: in_progress
priority: 1
version: 10
spec_path: docs/project/specs/active/plan-2026-09-10-n11-overnight-three-blocks.md
labels: []
dependencies: []
child_order_hints:
  - is-01m252542q6zq6hsb4jvj9y2rs
  - is-01m25255yg6wqveyja558g7sys
created_at: 2026-09-09T16:22:02.365Z
updated_at: 2026-09-10T07:09:14.368Z
---
Extend the certificate format and both covering routes to retain the weighted and floor charges already returned by the separator. Source: agenda034 lane A4 finding P10 and lane A5 F6. This is a representation and verification prerequisite, not evidence that the unconditional language or conditional route is exhausted.

Preserve distinct charge semantics. A ThresholdAtom(S,k,w) charges w*1[count>=k]. A floor atom with nonnegative integer multiplicities a, positive integer t and nonnegative w charges w*floor(a(P)/t), with budget w*floor(a(S)/t). These are not equivalent when a=1 and |S|>=2k. Use separate tagged records or an explicit charge mode; retain backward compatibility for existing frozen threshold records without reinterpreting their bytes.

Admission controls must include a 2-of-5 atom with a core containing four sites: threshold charge1 versus floor charge2. A T025 2-of-3 replay alone cannot catch the semantic mismatch. Also test zero weights/multiplicities where admitted, invalid signs and denominators, declared-budget mismatch, shared sites, closed-boundary membership, and D4 orbit accounting. The counting proof is sum_i floor(a(P_i)/t)<=floor(a(S)/t) for disjoint cores because their site traces are disjoint.

Implement exact event-cell coverage and the separately structured interval route with appropriate sound bounds. Re-decide unchanged T025/T026 through the preserved threshold mode and verify the same exact charges and budgets. Freeze a richer certificate only if its entire admissible domain passes both routes and its budget meets the declared physical counting threshold. Valid separated cuts alone do not constitute such a certificate.

The retained A5 value10 is exact for its finite final row set and an upper bound for the full rank-one closure on that fixed support. The corrected H155 conditional route remains live; this format may be useful to either strand. Primary paths use packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/.

## Notes

Astra xhigh independent review is complete: the floor budget proof is sound under strict core shrink and all 19 supplied controls pass. Two confirmed prototype defects are tracked separately: serialization/loader round-trip in think-h1ju and valid zero-charge NumPy overflow in think-k1pe. Sol xhigh repairs only those private source boundaries, then Astra will independently review the correction. The prototype remains unadopted; production dispatch, legacy migration, low-memory support and K5 remain open. No scientific target or retained certificate was run. Review: /private/tmp/n11-floor-atom-independent-review.md.
