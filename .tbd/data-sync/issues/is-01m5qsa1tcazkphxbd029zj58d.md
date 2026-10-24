---
type: is
id: is-01m5qsa1tcazkphxbd029zj58d
title: "Import #798: Amund Kristiansen's 14 upper bounds at 334–504 (gist e4df936 at c9be7b7)"
kind: task
status: in_progress
priority: 2
version: 5
assignee: null
delegate: c-import-798-1024
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T20:23:20.140Z
updated_at: 2026-10-24T20:51:52.110Z
started_at: 2026-10-24T20:24:12.673Z
---
New 2026-10-24 issue https://github.com/jlevy/squares/issues/798 (amundsk, 19:03:14Z): fourteen upper bounds at 334, 338, 343, 372, 376, 377, 379, 382, 412, 416, 457, 458, 502, 504, each below #763's 964ee2b side; 12 called new packings found from #763's, 2 refinements (372, 412). Gist amundsk/e4df936fb09c68446598d4c8309d0166 at c9be7b70e2220c2eccb2c5ea746094bc85dda405: s<N>_amund.cert (dilation certificates via Evan Daniel's dilate_cert.py) and s<N>_amund.input.txt. CC0 1.0 per the author's #755 comment of 2026-10-24T19:13:49Z. Report order: after 43f666c (pushed 2026-10-24T06:10:44Z, think-gn29: 108 own-count certificates at 330-997) and the 964ee2b notebook sides (think-lyf9, #795): compare at each count before recording. Stage 0 owner; stage 1 triage read-only first.

## Notes

2026-10-24 c-triage-798-1024 (stage 1 triage, read-only; drafts in /tmp/claude-0/-home-user-squares/d57983cc-21aa-53cd-a24f-c90463a5a3c0/scratchpad/triage-798/). Pin: gist e4df936 at c9be7b70e2220c2eccb2c5ea746094bc85dda405 (tree dd45a26, committed 19:01:54Z, only revision), 29 files 1,104,636 bytes; all 28 issue digests match; CC0 1.0 by issuecomment-6388401978 on #755, so retain all. Sides admitted at 12 places; dilate_cert formulas reproduce every side and centre (tangents differ 1-5 ulp, Apple libm); lineage table vs 964ee2b reproduced exactly by measure_identity. Report order: 43f666c (pushed 06:10:44Z, think-gn29) is below #798 at 372 (+1.91e-11) and 412 (+1.25e-9): not recorded. 12 rows (334 338 343 376 377 379 382 416 457 458 502 504) below every earlier report by 1.24e-5 (457) to 8.75e-3 (334); vs 43f666c at 376/377/416/458/502/504. 382's earlier report is #670's file (same bytes at 964ee2b). Price: certify ~0.25 CPU-h + sharp-controls ~0.8 CPU-h (measured: 504 positive 30.2 s both routes; 334 sharp 160.9 s, 11 controls as expected); checks double it; under the 40 CPU-h item rule. No stage 4 review (beyond-horizon rows); draft S2. Author question (informational): did the 376 search start from 964ee2b's file (packing nearer 43f666c's). Coordinator: walk reads 43f666c as a publication, no need to wait on gn29.
