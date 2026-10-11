---
type: is
id: is-01m45jysnrq0d9avv3p3xaqfvg
title: "Import wand125: mixed_n66_L843 (d73ce20) posted on #282 on 5 October"
kind: task
status: closed
priority: 2
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
hold: null
hold_until: null
created_at: 2026-10-05T08:30:18.296Z
updated_at: 2026-10-06T02:41:35.399Z
started_at: 2026-10-05T17:07:20.778Z
closed_at: 2026-10-06T02:41:35.399Z
close_reason: Done in jlevy/squares#369 (merged 34e87a86b); verdict replies posted 2026-10-06
resolution: null
duplicate_of: null
---
wand125 posted s(66) >= 843/100 = 8.43 (certificates/mixed_n66_L843, wand125/square-packing-bounds d73ce20d6650, comment https://github.com/jlevy/squares/issues/282#issuecomment-5990620723 at 2026-10-05T08:11:44Z) after the intake pass think-i5qd had pinned a541afb for T-094, so it is outside that packet. Same kind and checker as T-094 (rectangle density of mass n - 1/100000, code/mixed_rotated_verify.cpp, the n = 50 checker); it supersedes the source's mixed_n66_L842 = 421/50 = 8.42, which T-069 holds at V3/C3, so it would raise the reported lower bound at n = 66 by 0.01 and leave the verified one at 421/50 until its replay. Stages 1 to 3 at d73ce20 or a later head: a packet by acquire_source (precedent wand125-mixed-bounds-2026-10-05), an audit_wand125_point_and_mixed row (named n66-L843), mixed-audit and mixed-fetch, a reported evidence entry, coverage, a register entry at V0, the n-066 reported lane, result-requests #282 key oct5-n66-843 moved from queued to registered, and the replay priced (about 10 to 13 CPU-hours by T-069's n = 66 replay of 11.7 measured CPU-hours) and queued. Held in packing/campaign/intake-watch.yaml as a read of d73ce20 naming this bead.

## Notes

2026-10-05 22:00 subsumed by think-8qo9 (lane B): mixed_n66_L843 retained at 43050ed (packet wand125-mixed-bounds-finer-net-2026-10-05), n66-L843 audit row, mixed-audit and mixed-fetch pass, registered as T-097 (provisional) at V0/C1 after the 5 October review, 12-direction sample replay matching, sqverify-fast all 201; complete replay moved to think-0fkt. The intake-watch read of d73ce20 is removed. For the coordinator to close.
