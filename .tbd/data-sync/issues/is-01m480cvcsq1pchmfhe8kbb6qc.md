---
type: is
id: is-01m480cvcsq1pchmfhe8kbb6qc
title: "Replay wand125's ValidTilt9 run (records-tilt9-v1, c561dbb) in full: the independent route to T-081's finite premise"
kind: task
status: open
priority: 2
version: 5
labels:
  - result-import
  - packing
dependencies: []
created_at: 2026-10-06T07:03:39.160Z
updated_at: 2026-10-09T06:05:57.295Z
---
Held from think-dsz4 (lane R3, 6 October intake round), which retained wand125/valid7-independent-check at c561dbb3 in packing/resources/web/wand125-valid7-independent-check-2026-10-06/ and recorded the run as reported evidence E-k2m4-wand125-validtilt9-report on T-081. The full replay costs far more than the 6 CPU-hour ceiling of that lane, so it waits for a budget the owner sets. The price, from a stratified sample of roots re-run here, is in the packet's receipts/validtilt9_sample_compare.json and README (Price section). Two designs, per review-2026-10-06-wand125-validtilt9-independent-check.md section 5: (A) re-certify every CORE and TIERB2 leaf of the published records with check_record.py --partial --recheck/--recheck-b, sharded, against the retained release/records.sha256 (option-free, tests the published certificate; leaf re-certification cost about as much as the search for Valid7); or (B) re-run run_all.py over the 28,350 roots with each root's phase options from devtools.audit_validtilt9_independent PHASES (the sample's stage/run/compare subcommands), comparing leaf lists root for root. Controls: devtools.audit_validtilt9_independent control (two box-9 mutants refused). Then a replayed-here evidence entry, independent-implementation, and T-081's ValidTilt9 part can move; the Lean reduction needs its own replayed entry as well.

## Notes

2026-10-06 (later): the owner declined the full replay for now (#316 closed with T-081 at V0/C1). Waits on an owner compute budget (about 118-435 CPU-hours), not on think-dsz4.

blocked_on: think-3j6u
