---
type: is
id: is-01m5fwdhgyd3ar79bqwyy46jt8
title: Keep authored Results and derive current Records across result families
kind: task
status: closed
priority: 2
version: 5
delegate: profiles-data-integration
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T18:43:44.797Z
updated_at: 2026-10-21T21:45:33.744Z
started_at: 2026-10-21T18:43:52.643Z
closed_at: 2026-10-21T21:45:33.744Z
close_reason: Completed bounded implementation, reviewed evidence and local/hosted feature acceptance. Final-head CI and separate runtime/evidence followups remain open.
resolution: null
duplicate_of: null
---
User-confirmed scope: Results retains every reviewed primary-authored result ID, unchanged by historical record eligibility. Records is the current subset across all result families, including optimality proofs and formalizations, counted once per T ID and blank at zero. Comparable numeric bound claims require strict improvements; second proofs and formalizations have their own contribution lifecycle rather than being discarded as tied numeric values. Reuse canonical case-bound standing and explicit whole/partial supersession for non-bound families. Preserve original authorship, first_certified_in attribution, assurance lanes and multi-case partial currentness; never infer historical novelty from absent supersession. Implement shared classifier/tests in a dedicated module, with only minimal evidence-backed structured qualifications where canonical sources leave a genuine gap. No new mathematical result registrations; frontend integration and tally formatting remain separately owned.

## Notes

Completed the shared all-family Records classifier and frontend projection without filtering authored Results. One T ID counts once; non-bound families follow explicit whole/partial lifecycle; bound facets require positive current support or stronger pending claims, strict numeric comparison, correct assurance lanes and first_certified_in attribution. Exact-value proofs require their own lower-lane support and the correct proved status. Rounded/overlapping or unordered priority remains explicit, not an inferred winner. The typed family-scope link exposes T-163 currentness as unassessed and tracked by think-kqi1/think-e953 rather than a false positive. These are separate canonical-evidence followups, not unfinished implementation or hidden child work. The current index remains 116 known-current IDs and 5 unassessed IDs; primary Results stay 213. After T-196 adoption, 20 classifier/packet tests passed in 1.39 seconds, and the 54 identity/tally/coverage tests passed in 8.47 seconds. Astra reviewed the strict-point tie, proof-negative and family-unknown boundaries without remaining Blocker/High findings.

Final integration evidence: the scoped work is committed and published in https://github.com/jlevy/squares/pull/578, currently at db3cb6d4fe5f00a44d04a8ef91018aa2b365bad8. Hosted validation at e162a870a899a61cc77cd47fa2f56c0ff388c8ea passed Pages, Packing Validate and suites B/C; suite A passed all 4,364 assertion tests, then failed only the separate project-tally CALL wall guard. That independent runtime defect is fixed in e3e33171bf1d687190cc957a40e25fbbc9dbb23c and remains tracked by think-rolz while final-head CI runs. The exact final db3 CI verdict is not claimed here. This closure is for completed bounded acceptance; the overall think-zpfo handoff, think-uwd6 coverage parent, historical registrations, pending PDF census and real evidence gaps remain open.
