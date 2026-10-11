---
type: is
id: is-01m478czzp4p015zm4dsxdt89c
title: "T-097 exit: s(66) >= 843/100 by sqverify-fast at the reviewed source (census rerun 2026-10-06), controls, evidence, rungs"
kind: task
status: closed
priority: 1
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m46g4yac7ewc22drc7twjhy5
hold: null
hold_until: null
created_at: 2026-10-06T00:04:18.038Z
updated_at: 2026-10-06T02:41:34.463Z
started_at: 2026-10-06T00:05:35.114Z
closed_at: 2026-10-06T02:41:34.462Z
close_reason: Done in jlevy/squares#369 (merged 34e87a86b); verdict replies posted 2026-10-06
resolution: null
duplicate_of: null
---

## Notes

2026-10-06, lane T-097 (claude/ecstatic-pascal-pothtx-t097, base 98c748e25):
- bce4134d1 census row of mixed_n66_L843 at the reviewed crate source (binary af0871c0..., source_sha256 7c49cf79...), VERIFIED 201/201, least bound 1.0000000006737138 at r=122, 2,104.9 CPU-s; control receipt CONTROLS_REFUSED at r=122; census test holds the route's remaining per-certificate conditions (no points, scaling 1, no declared net, densities far below F3's cap, audit_record a listed accepting review).
- 9b5f15259 records: E-n066-wand125-mixed-843-sqverify-fast-replay; T-097 V0/C1 -> V3/C3 (derived by check_results), S3; n = 66 verified 421/50 -> 843/100; views, atlas, piercing, T-007 audit, synopsis re-rendered; test_check_standing example updated (T-069 now beaten at 66 and 92).
- d4be73b91 DATA_REVISION re-pin.
- Open for others: think-0fkt (source-checker replay) no longer gates the move; T-094's replay entries and the census --evidence template still say "cargo build in sqverify_fast/", but the crate there now carries the unreviewed declared-net change (see report).
