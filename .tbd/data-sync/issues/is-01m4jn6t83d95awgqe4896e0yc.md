---
type: is
id: is-01m4jn6t83d95awgqe4896e0yc
title: Align web atlas layout goldens with approved asymmetric compact gaps
kind: bug
status: closed
priority: 1
version: 7
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4h9s465x7mphy1xxkmdyqc9
hold: null
hold_until: null
created_at: 2026-10-10T10:19:45.766Z
updated_at: 2026-10-10T11:24:56.801Z
started_at: 2026-10-10T10:20:31.804Z
closed_at: 2026-10-10T11:24:56.801Z
close_reason: Final accepted atlas behavior implemented and published in PR474 at d83b7c03d, containing main657cc4861. Local repair-delta66PASS; hosted Fast94+actualDeferred13=107PASS on immutable mergec78974427 with identical headtree; Pages17 dependencies+required aggregatePASS; formal seniorI/correctnessJ no findings in declared scopes. Required CI PASS, no unresolvedthreads, CLEAN/MERGEABLE finalreadback. Canonical exports qualified; prior failures retained without acceptance relaxation. Later user refinements supersede earlier styling/layout requirements. Completed ready-to-merge scope; no GitHub merge performed. Browser hold, future intake and performance follow-ups remain open. Final evidence full107-final-proof.json and final-freshness.json under external final/ci-final-head-d83b7c03d.
resolution: null
duplicate_of: null
---
Ha739 delta gate exposed 18 site_atlas_views assertions: initial Small capacity remains expected15 but new20percent horizontal gap yields16; uniform-height check incorrectly equates vertical and horizontal gap after independent25percent vertical tightening. Inspect actual renderer contracts and fix exact stale expectations without weakening reserved size, common heights, complete rows, right alignment, segment gaps or measured ratio acceptance. Root owns source publication and tracking.

## Notes

Exact stale expectations identified: initial Small placement capacity15 should be16 after approved tighter horizontal spacing; settled capacity remains15. Uniform row geometry should compare measured vertical distance with computed row_gap_px, not independently sized horizontal gap_px. Only two test assertions changed; same tolerances, uniform height/pitch, full row bounds/right edges, drawing scale, segment separation and0.8/0.75 measured ratios retained. Focused/full-file serial qualification pending.

Committed exact reviewed fixes at d83b7c03d92a3f1853c479f45fabb07cb289aa97. Focused serial selection passed116 tests in224.38s, zero failures/errors/skips, including all web atlas cases and four timeout/custody controls. Ruff, formatting and targeted BasedPyright pass with zero findings. Independent senior I and correctness J supplementary inspections report no findings; formal reviews held for publication. Current repair-delta pre-push selects113 files from basea739, explicit jobs8/inner1 gives three pytest workers without deadline or acceptance changes. Final actual hosted qualification still pending; do not close prematurely.

First d83 repair-delta allocation retained as exit1: all65 edit checks passed; normal4498 passed/35 skipped/4 warnings in700.92s, then unchanged900s step deadline terminated incomplete pool lane during full324 corpus build. No source assertion failed. Root allocation jobs8/inner1 left the corpus serial. Identical-head retry changes only resource shape to jobs6/inner4 (five pytest workers, four corpus workers), same113file selection and deadlines. No published or complete-gate claim; final qualification remains pending.

Final qualification completed at published H d83b7c03d92a3f1853c479f45fabb07cb289aa97 and base T657cc486130e9020608ff244d8a86d1d04153634. Immutable merge Mc78974427a2a5d6ca144f7333f95c82c6d2bc08f has the same tree88e808eb1b9b12a094808853a5915e7ee28d6baf as H. Local repair-delta pre-push:66 selectedPASS in791.61s; normal4498PASS/35SKIP, pool3PASS; combined718.02s within unchanged900s. Hosted Fast38046943798:94 canonicalPASS; actual branch-definition Deferred38047004997:13 disjoint canonicalPASS, all10workers/resolver/aggregatePASS. Union107exact;234 command receipts cleanM provenance; exhaustive shards2/30/29=61 distinctPASS/zero failures/errors/skips. Pages38046943822:17 applicable dependencies plus required aggregatePASS, actual production PDF math/font/layout/stored-fresh guardsPASS. Maintained verified_merge_tree explicitly accepts current Fastrun38046943798. Independent formal seniorI5478716184 and correctnessJ5478716232 published atH/T with no findings in declared scopes. Focused116PASS retained. Previous failed/interrupted/timeout attempts remain failed evidence, without deadline/assertion relaxation or retroactive qualification. Deep891s/1900s; Fast370s/180s and Pages284s/180s reporting-only advisories remain owned by think-g4n9, without a new reference-cost claim. Proof: final/ci-final-head-d83b7c03d/full107-final-proof.json and push-d83b7c03d-retry2.json. No GitHub merge authorized or performed.
