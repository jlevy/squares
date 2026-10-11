---
type: is
id: is-01m45f7t70krz1wq7gsthsngrd
title: "Import wand125: mixed_n67_L848 (6c0842e) and mixed_n84_L9411 (a541afb) posted on #282 on 5 October"
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
created_at: 2026-10-05T07:25:19.455Z
updated_at: 2026-10-05T08:45:46.957Z
started_at: 2026-10-05T07:44:28.460Z
closed_at: 2026-10-05T08:45:46.957Z
close_reason: Stages 1-3 merged in jlevy/squares#362 as T-094 (V0/C0); stage 4 review and replay is think-flv5
resolution: null
duplicate_of: null
---
Two certificates posted on jlevy/squares#282 after T-090 (8aa6a10) and T-091 (797bdf6) were packeted, with no owning bead until now (found by the stack-357 bead bookkeeper on 2026-10-05): s(67) >= 212/25 = 8.48 (mixed_n67_L848, wand125/square-packing-bounds 6c0842e, comment 2026-10-05T06:06:49Z; supersedes their mixed_n67_L8475 = 8.475 of 2475d08) and s(84) >= 9411/1000 = 9.411 (mixed_n84_L9411, a541afb, 2026-10-05T06:07:23Z; supersedes mixed_n84_L94075 = 9.4075 of c9c6be0). Same kind and verifier as mixed_n84_L940; the source reports a full 201-angle replay from the bundle on a fresh Ubuntu 24.04 machine. Run the import runbook stages 1-3 (claim map against the record, packet at the later pin, register or extend a T-NNN at V0), queue the stage-4 replay with the others, and fold the acknowledgement into think-7gop / think-aygi. The superseded mixed_n67_L8475 (2475d08) and mixed_n84_L94075 (c9c6be0) fall in the 14 posts from b321ac9 to 3554616 that T-090 covers (think-e6ss), so these two raise T-090 entries at n = 67 and 84 rather than open new counts.

## Notes

2026-10-05 08:00Z (intake pass think-i5qd, branch claude/ecstatic-pascal-pothtx-intake3): stages 1 to 3 done on the branch, not yet merged.

Stage 1, claim map. The pin is a541afbe7826ff75f6d3848e10279fd524d55af3 (head; 6c0842e adds mixed_n67_L848, a541afb adds mixed_n84_L9411; nothing else changed after 797bdf6). Two claims, both in scope, both requested (#282 comments 5989043109 and 5989049022): s(67) >= 212/25 = 8.48 (536 rectangles) and s(84) >= 9411/1000 = 9.411 (686 rectangles), mass n - 1/100000, the n = 50 checker byte for byte. Register action: a later release raising an earlier entry's values -> a new entry, T-094; T-090 (339/40, 3763/400) keeps its claim and the case records report T-094. Verified lower bounds stay 1691/200 (n = 67, T-070) and 47/5 (n = 84, T-071). Monotonicity carries nothing: the record reports 851/100 at n = 68 and 473/50 at n = 85.

Validation plan, priced: no missing tool (no W7). The complete replays with devtools.audit_wand125_point_and_mixed, 26.5 CPU-hours planned (mixed-price 23.7 x observed 1.119; the source's own oblique seconds give 21.2), mixed-shard wand125-mixed-bounds-2026-10-05 --runners 2, about 3.3 wall hours on each of two 4-worker hosts; plus a review of the two certificates for C1. Not started: over the session's 15 CPU-minute ceiling. Owned by think-flv5, held for the owner's budget.

Stage 2: packet packing/resources/web/wand125-mixed-bounds-2026-10-05 (c04d61bbe), key [wand125 mixed bounds 2026-10-05]; acquire_source --check PACKET_MATCHES_ITS_CONTRACT; mixed-audit passes on both; mixed-fetch on both pinned tarballs BUNDLE_READY (621 files, preconditions, all 200 inputs enclose the candidate) in 37 s.

Stage 3: T-094 at V0/C0 with E-n067-wand125-mixed-848-report, E-n084-wand125-mixed-9411-report, the coverage entry, n-067/n-084 reported lanes, renders (067c7d9e3), re-pin (4b5b0ed25). result-requests #282: oct5-n67-n84 -> T-094, read_through 2026-10-05T06:07:23Z. The acknowledgement draft is in think-7gop's notes.
