---
type: is
id: is-01m5gh8r272jj3mnamermgjyst
title: Reconcile profile attribution after T-223 adoption and T-225 integration
kind: task
status: in_progress
priority: 1
version: 5
delegate: ci_watch
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-22T00:48:07.750Z
updated_at: 2026-10-22T06:45:40.449Z
started_at: 2026-10-22T00:49:15.962Z
---
Reconcile exact profile attribution after upstream d7923b8d8: T-223 adoption at n204/n260 and T-225 Daniel regularized views. Resolve the assigned additive adopt_houses, resource-index and generated RESULTS/SYNOPSIS conflicts, retaining both branch behaviors and canonical output. Reconcile source-reviewed existing-profile spans and source-specific evidence without fuzzy identities or new historical results. Preserve original authorship, prerequisite roles, assurance lanes and raw source text. Validate census/schema/model/source/citation behavior; coordinator owns release, URL, merge, build and final CI work.

## Notes

Merged origin/main7359fa8b6 reconciliation completed by ci_watch: all1534prior occurrence rows and inspectionreceipts preserved;26newreviewedspans (25person,1company) produce1465resolved/78nonperson/7unresolved plus10manual.75profiles/217authoredResults/714Credits/112authoredcurrentRecords. HistoricalT226–228 increase Results only; T225 verifiedfacets replaceT196/T199/T223.73focusedtests passed9.34s,canonical228-result/verifier/citation/headline/sourcecoveragechecks pass. Committed with b6e062d61; finalcombinedUIgates/CI pending underthink-gbwb.
