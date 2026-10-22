---
type: is
id: is-01m5ghbpszw0r22b4wm95vgkfr
title: "Decide #715's 30 sub-print re-certifications of Couzo's 4e4c8ce certificates (2.4e-23 to 3.2e-23 below, same print)"
kind: task
status: in_progress
priority: 1
version: 3
delegate: c-lane-715-import
labels:
  - result-import
  - decision
dependencies: []
parent_id: is-01m5g8xj3hqca5wcen9f71dtnd
hold: null
hold_until: null
created_at: 2026-10-22T00:49:44.766Z
updated_at: 2026-10-22T00:49:56.222Z
started_at: 2026-10-22T00:49:56.222Z
---
Issue #715 (franciscouzo/square-packing 6b7391de) restates 64 counts at or below 1024 that the triage read as certificates first published at 02f9690, f311f08, a7067d7 and 4e4c8ce (9 to 15 October). At the pin, 30 of them are not byte-identical: the explicit certificates certificates/nN.cert, first committed at 5a299b4 (2026-10-20) and pushed with the pin at 2026-10-21T22:56:37Z after the issue, are exact L-border re-materializations of the same packings whose sides are below the 4e4c8ce certificates' by 2.37e-23 to 3.18e-23. Both round up to the same 12-place print. Counts: 535, 582, 591, 631, 633, 640, 682, 684, 691, 695, 735, 737, 742, 745, 790, 791, 797, 798, 799, 854, 855, 856, 857, 909, 913, 915, 916, 970, 975, 977.

By the ledger rule with exact sides, each would be recorded after the 4e4c8ce publication as a refinement of Couzo's own packing; by the issue's prints it is undecided. The lane's brief says to stop on a row whose newness depends on rounding, so nothing is recorded for these counts. The certificates are retained and replayed in packing/resources/web/couzo-issue715-2026-10-21 (receipts/filtered-exact-replay.json; receipts/earlier-publications.json gives each margin), and the 22 October ledger (packing/campaign/issue-intake/upper-bounds-20261022) leaves them undecided against the 4e4c8ce publication.

Decision wanted (coordinator or owner): record these 30 as #715's rows (a 30-row addition to the packet's claims record and source-coverage.yaml, superseding 487b058's rows now and 4e4c8ce's when think-yfoo lands), or leave them to think-yfoo's 4e4c8ce import as restatements.
blocked_on: none
