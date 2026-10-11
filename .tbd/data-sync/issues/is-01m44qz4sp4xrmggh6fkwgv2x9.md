---
type: is
id: is-01m44qz4sp4xrmggh6fkwgv2x9
title: Replay wand125's 14 mixed certificates of 4 October (T-090 stage 4)
kind: task
status: closed
priority: 2
version: 5
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
hold: null
hold_until: null
created_at: 2026-10-05T00:38:38.133Z
updated_at: 2026-10-06T17:02:10.512Z
started_at: 2026-10-06T07:50:57.852Z
closed_at: 2026-10-06T17:02:10.512Z
close_reason: "Done and on main via #382 (d087422ed); reply posted 2026-10-06 and recorded"
resolution: null
duplicate_of: null
---
Full 201-angle replays, as for T-082; held for compute budget like think-wpuu's runners.

## Notes

2026-10-05: covers T-091 only (the 12 at 797bdf6, packet wand125-mixed-bounds-evening-2026-10-04): 130.8 CPU-h planned, mixed-shard --runners 6. T-090's 16 at 8aa6a10 (incl. n69-L862, n86-L9503; 146.5 CPU-h, --runners 8) stay with think-wpuu.

2026-10-05 (intake pass think-i5qd): the blocks dependency on think-07s1 is removed. think-07s1 closed when the wand125 lane merged (105d38044), so T-091 is on main, and nothing this bead names is open. The replay of T-091's 12 waits only on a compute budget the owner sets (130.9 CPU-hours planned, mixed-shard wand125-mixed-bounds-evening-2026-10-04 --runners 6), as think-wpuu's does for T-090.

blocked_on: none
