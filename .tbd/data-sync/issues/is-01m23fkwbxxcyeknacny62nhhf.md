---
type: is
id: is-01m23fkwbxxcyeknacny62nhhf
title: "Certificate format cannot express two atom classes: K5 clique and K6 floor"
kind: task
status: in_progress
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-10-n11-overnight-three-blocks.md
labels: []
dependencies: []
created_at: 2026-09-09T16:22:02.365Z
updated_at: 2026-09-10T06:16:07.009Z
---
Extend the certificate format and both covering routes to retain the weighted and floor charges already returned by the separator. Source: agenda034 lane A4 finding P10 and lane A5 F6. This is a representation and verification prerequisite, not evidence that the unconditional language or conditional route is exhausted.

Preserve distinct charge semantics. A ThresholdAtom(S,k,w) charges w*1[count>=k]. A floor atom with nonnegative integer multiplicities a, positive integer t and nonnegative w charges w*floor(a(P)/t), with budget w*floor(a(S)/t). These are not equivalent when a=1 and |S|>=2k. Use separate tagged records or an explicit charge mode; retain backward compatibility for existing frozen threshold records without reinterpreting their bytes.

Admission controls must include a 2-of-5 atom with a core containing four sites: threshold charge1 versus floor charge2. A T025 2-of-3 replay alone cannot catch the semantic mismatch. Also test zero weights/multiplicities where admitted, invalid signs and denominators, declared-budget mismatch, shared sites, closed-boundary membership, and D4 orbit accounting. The counting proof is sum_i floor(a(P_i)/t)<=floor(a(S)/t) for disjoint cores because their site traces are disjoint.

Implement exact event-cell coverage and the separately structured interval route with appropriate sound bounds. Re-decide unchanged T025/T026 through the preserved threshold mode and verify the same exact charges and budgets. Freeze a richer certificate only if its entire admissible domain passes both routes and its budget meets the declared physical counting threshold. Valid separated cuts alone do not constitute such a certificate.

The retained A5 value10 is exact for its finite final row set and an upper bound for the full rank-one closure on that fixed support. The corrected H155 conditional route remains live; this format may be useful to either strand. Primary paths use packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/.

## Notes

Sol high completed a private K6 checkpoint under /private/tmp/n11-floor-atom-prep/:
floor.py, floor_interval.py, decide_floor_certificate.py, synthetic tests and a contract.
Nineteen synthetic tests, Ruff and BasedPyright passed on project Python3.14.
No retained certificate or scientific target ran, and no shared source or registry changed.

Remaining: independent source review, production CLI/source/parallel adapter, legacy
dispatch integration, low-memory slab route and affected gates. K5 source mapping and
admission remain open; the general floor representation may express its budget-one
subclass under the reviewed total-weight premises. This does not close think-g3j7.
The six A6 cuts use existing threshold semantics and do not depend on this extension.
Model identity comes from dispatch: gpt-5.6-sol at high, not the worker's generic footer.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
