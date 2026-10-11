---
type: is
id: is-01m3n5xkjsb1sa10wkmheddscx
title: "Intake evand's s(21) = 5 and s(45) = 7: pin evand/square-packing past 167d842c, retain the new covers, replay, review, register"
kind: task
status: in_progress
priority: 1
version: 6
labels:
  - packing
  - wand125-update
  - low-n
  - review
dependencies:
  - type: blocks
    target: is-01m3n5y05cdnsnkspf7e4vg5jp
parent_id: is-01m3n5wh72rsqd2z97m8v1vv4q
created_at: 2026-09-28T23:34:36.888Z
updated_at: 2026-09-30T20:18:25.129Z
---
wand125 reports (see packing/resources/web/wand125-x-update-2026-09-28/) that evand/square-packing now proves s(21) = 5 and s(45) = 7; the register holds s(21) >= 5000/1001 (verified, [evand square-packing 2026] at 167d842c) and s(45) >= 1391/200 reported (wand125 rectangles) with Nagamochi's 6.830951 verified. Acquire the new revision, retain the changed files byte-identical in a new packet beside evand-square-packing-2026-09-26/, replay the source's zero-margin sweeps in full as was done for s(32) = 6 (2.8 CPU-h there; about 4 CPU-h per cover at k = 7 per BC-396's estimate), note what the Lean build and second checker cover, write the mathematical review, and register at the honest V/C rung. Both upper bounds are the trivial grid (5 and 7), so each case moves to proved. Disposition for think-0g4t (BC-396, this project's own planned k = 7 transfer): superseded, or kept as a method-distinct second route toward C4.

## Notes

2026-09-30: the two cloud sessions named earlier (session_011CfRigVmuCke9r31UzDPhM, session_01Xt9EM5JEiNoK5aSsWz6E6x) no longer exist and pushed no branch. Both full re-sweeps were restarted at 05:24Z in session 01BwdQAcVk5jwFycxVkLGNaK on branch claude/determined-goldberg-ura2ed. Each runs 2 workers from an overlay of the two evand packets, with resumable records under that session's scratchpad (resweep/s21, resweep/s45). At 05:34Z they were at 1.8% and 1.6% of the source's per-root CPU, with every completed root's census equal to the shipped record and 0 uncertified. Expected finish about 15:00 to 16:00Z. Whether a re-run of identical code is worth its CPU, and the faster options, are in think-mx3k.

2026-09-30 20:18Z (session_01VfxwoTFTTtYPSdNYENYKZ1): no re-sweep results reached git. #249's branch is still at c6f51ce6b, and session 01BwdQAcVk5jwFycxVkLGNaK, whose scratchpad held the resumable records (resweep/s21, resweep/s45), is not reachable from this session. The #249/main integration (think-d15x) went ahead without them. Recording T-052/T-053's second entries needs those records recovered, or the re-sweeps re-run, or one of think-mx3k's faster options.
