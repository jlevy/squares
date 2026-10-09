---
type: is
id: is-01m4f1dr9rjm9csyhx95q2pm7k
title: Collapse matching publication and revision dates in shared paper fronts
kind: task
status: closed
priority: 2
version: 8
delegate: claude-code@spud10.local
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-09T00:36:18.359Z
updated_at: 2026-10-09T02:07:50.850Z
started_at: 2026-10-09T00:36:38.536Z
closed_at: 2026-10-09T02:07:50.849Z
close_reason: Shared paper dates implemented, Astra reviewed, final source full CI green and PR458 mergeable.
resolution: null
duplicate_of: null
---
PR #458 follow-up: shared HTML/Markdown/PDF paper date display should show Published Month D, YYYY when first publication and revision dates match, while retaining distinct date labels, original-proof dates, and metadata. Add focused regression coverage, update native paper design guidance, refresh preview, Astra review, push and confirm CI.

## Notes

Completed at source 4505019f7e48a53d31f5a1dc2c91d2a0c3953f6b. Shared HTML/Markdown/PDF dates collapse matching publication/revision days to Published once; source event dates/metadata retained, native design/tests/preview updated. Astra D confirmed audit fix; F final integration review 5464775085 has no findings, with prior B/C/E scope explicit. Local focused groups122 passed12skips +104budget +70workflow +285postcommitoverview, full/focusedtype and lint pass; normalhooks and final source export/drift pass. Local broadpush exit1:11 sparse-input failures all independently passed hosted,900s reachable timeout, no localpush successcredit. Final current runs Packing37870564480 SUCCESSattempt1; Certificate37870564598 SUCCESSattempt2 after one bounded D509 PDF retry (guards unchanged,2 loads agree/storedfreshmatch,NOTJUDGED partial wall,no causefix); Mergeability37870562363 SUCCESS; explicitdeep37870591332 SUCCESSattempt1. 20 clean receipts/108passing executionrecords exactly106 nativeSteps=93fast13deferred,all3exhaustiveshards61tests/17disjointfiles. Actualvalidation baseb810432/mergea35e45671a288017b3230e183355b511020923d5/tree5ae72732379b481dd168f78e965d80806a922d9b; latermain24fe88bc clean separate threewaymerge/tree04ea4577 without executioncredit. Fresh PRcheckwatch97319 exited0 finalallpassed; GitHubMERGEABLE/CLEAN,remotehead450/localclean. Final cost-first PRbody checked/posted. No thresholds/deadlines/policies relaxed; no oldhead/skipped executioncredit; t7k5 performance debt remains open. Ready for maintainer review; no PRmerge authorization.
