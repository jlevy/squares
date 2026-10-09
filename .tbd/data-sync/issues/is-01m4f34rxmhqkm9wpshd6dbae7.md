---
type: is
id: is-01m4f34rxmhqkm9wpshd6dbae7
title: Admit the verified suite-D baseline for atlas publication checks
kind: chore
status: closed
priority: 2
version: 5
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-09T01:06:21.235Z
updated_at: 2026-10-09T13:44:10.860Z
started_at: 2026-10-09T01:06:39.583Z
closed_at: 2026-10-09T13:44:10.860Z
close_reason: Implemented, independently reviewed and qualified for PR474 source 6ccbbf000f0c9b48f2985c07c9893f98fe73ba92 against main 6a0499ba4; combined tree c65da41410e89a8dedffe93d3c1e153adb05096d. Local named push 65/65 and hosted 93 fast + 13 actual deferred (106) plus Pages passed; final readiness receipts recorded.
resolution: null
duplicate_of: null
---
Resolve the independent expired suite_d pending measurement that blocks current atlas records validation. Admit only the verified historical 101.34-second observation from complete green run 37613399745, attempt 1, job 112765857172 (October 7, 2026, actual checkout 33e96ced9ddf5025e47ecad8420865cf519102b8/tree 23782412f1a268956cd2bb4e323fba72cc9311b1, reference four CPUs/jobs1/inner1, one of101 steps). Keep the143-second ceiling, reference shape and policy unchanged. Both later190.63s and168.55s readings breached that ceiling despite green tests; preserve them as current performance debt under the existing owning tracker think-t7k5, and do not claim this declaration repair qualifies current performance. Strong independent evidence review accepted the narrow substitution. No unrelated n17 code, shard costs or other budget fields are imported. Run the maintained budget contract checks and include exact provenance and limits in the PR.

## Notes

The earlier reviewed 7900aafad declaration admitted the separately verified 101.34s October7 observation. During the approved main24 integration, retain the published canonical first-hosted 104.95s October1 baseline with exact run36939743802/job110628224361/merge75636e83f provenance; preserve the 101.34s run37613399745/job112765857172 as additional history in the argument, not a pooled sample or replacement baseline. Only this added historical argument differs semantically from the incoming budget registry. The 143s ceiling and four-CPU/jobs1/inner1 reference remain unchanged. Later163.63s,190.63s and168.55s breaches remain visible and performance qualification stays open under think-t7k5. The merged CLI/budget/snapshot contracts pass191+19 tests with no skips; prior91 budget tests are historical source-check evidence. Full publication/hosted gates remain pending; no current performance qualification is claimed.
