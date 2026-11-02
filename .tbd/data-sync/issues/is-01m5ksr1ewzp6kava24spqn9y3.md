---
type: is
id: is-01m5ksr1ewzp6kava24spqn9y3
title: "Validate: chelokot's and Daniel's Lean proofs of s(2) to s(5) (think-7l2j), receipt-bound builds (<1 CPU-h)"
kind: task
status: in_progress
priority: 3
version: 6
delegate: bold-ritchie-l29
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T07:14:00.796Z
updated_at: 2026-11-02T11:10:50.073Z
started_at: 2026-10-26T11:21:28.603Z
---
Validation part of think-7l2j (chelokot's and Evan Daniel's Lean proofs that s(2) = s(3) = s(4) = 2 and s(5) = 2 + 1/sqrt 2; no issue). Created by c-lean-1023 under the 23 October intake epic, as the lane rules allow; it serves think-7l2j.

## Validation
- Claim: chelokot/square-packing-archive at 753079eb37d8d16225a5dc1f56e493a3c3b243f4: Records.Square5.s5_eq_goebel, NearSquare.s2_eq_two, s3_eq_two, SquareNumbers.s4_eq_two (Lean v4.33.0, Mathlib db584cd6); evand/square-packing at 7051f4eabf7f9b2509ad1e7cc296f57d19482027: rect2_iff, rect3_iff, rect4_iff, rect5_pts_lower, rect5_upper (Lean v4.33.1, Mathlib 0df444a3). Packets: packing/resources/web/chelokot-small-n-lean-2026-09-05/ and evand-rect-small-n-lean-2026-10-22/.
- Run: (a) from the chelokot packet's retained bytes, `lake exe cache get`, `lake build` of the three Records modules and a probe printing the seven theorems' axioms, under a receipt that names them (devtools.replay_chelokot_lean's pattern; the 2 October build of the whole archive already logged these axioms, build.log lines 330 and 338 to 343, but its receipt names only T-086's theorem); (b) from the rectangle packet, `lake build` of Rect, Rect3, Rect4, Rect5Pts and Rect5Pack and a probe of their axioms. Accept only the three standard axioms.
- Cost: under 1 CPU-hour in all (eight modules each, no certificates; an estimate from size).
- Budget status: runnable within a lane's 2 CPU-hour single run; needs two toolchains and two Mathlib caches, about 20 GB of disk, which the lane's host lacked on 23 October (5.2 GB free).
- Possible subset: either route alone.
- Depends on: the packets; the stage 4 review, which also reads the square-case step from the rectangle theorems (Fried4 at w = h < 2, and five squares in a side below 2).
- Done when: receipts are committed on a branch this bead names and registered as `replayed-here` entries on the register entry that think-4o9c's decision makes (T-237 is allocated and held), or the owner dispositions them.
- Machine note: small; not alongside a validation gate.

blocked_on: none

## Notes

2026-10-26 ~11:25Z w-val-1026 (moderate-tier sub-agent of coord-n12-1025, the 26 October intake review's validation lane): NOT STARTED, disk. The run needs two Lean toolchains (v4.33.0 for chelokot's 753079eb, v4.33.1 for Daniel's 7051f4e) and two Mathlib caches (db584cd6 and 0df444a3), about 10 GB each by the two packets' READMEs (chelokot-small-n-lean-2026-09-05/README.md lines 155-159, evand-rect-small-n-lean-2026-10-22/README.md lines 137-139): about 20 GB for both routes, about 10 GB for either alone. This host (four cores, shared) had 5.1 GB free on / at 11:21Z on 26 October (`df -h /`: 252G size, 34G used, 5.1G avail), so neither route fits; no toolchain (~/.elan absent) or Mathlib cache is present to reuse. CPU price unchanged: under 1 CPU-hour for both (an estimate from size). Runnable on a host with at least 12 GB free for one route or 22 GB for both; nothing else blocks it. #786 stays open on it (review track: it closes only when T-238 is confirmed or refuted).
