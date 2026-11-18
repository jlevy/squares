---
type: is
id: is-01m4mbkx4jfae22h9h4evzbsy9
title: "Import evand: n17 hard tail, wall-chain elimination of width 1 misses m851903's obstruction, a float negative (#494)"
kind: task
status: open
priority: 3
version: 6
labels:
  - result-import
dependencies: []
hold: paused
created_at: 2026-10-11T02:10:37.842Z
updated_at: 2026-11-17T21:51:36.545Z
---
Issue https://github.com/jlevy/squares/issues/494 (evand, 2026-10-11T00:58:50Z), opened after the 2026-10-10 intake pass's sweep, so it belongs to the next pass. A negative, float only: X-052 section 2.5's width-1 wall-chain path relaxation, run on m851903 and the endpoint state 3439615 at evand/square-packing cd55295 (search/wallchain/, search/WALLCHAIN.md), barely separates m851903 from the true state (62 and 73 percent of sampled interior poses leave the ring feasible, against 82 percent for the control). Nothing is a certificate and nothing is claimed for the register. Next pass: stage 1 triage (enter #494 in result-requests.yaml with triage pending; record it as a negative for the n17 hard-tail lane, not a result), acknowledge the author. Held with the n = 17 intake (think-x4v4).

## Notes

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): existing issue https://github.com/jlevy/squares/issues/494 states the remaining work (reply https://github.com/jlevy/squares/issues/494#issuecomment-6119249272: a note beside X-052 section 2.5, held with think-x4v4). Tracker https://github.com/jlevy/squares/issues/544.

2026-10-13 owner decision: suspended pending Overbeck's proof that s(17) = L (#557; registered as T-153 by #560, credited by #571), which likely subsumes new s(17) research. Resumes only if the owner lifts the suspension, for example if T-153's replays and reviews find a gap or the candidate is withdrawn. Intake of #494 (evand's n = 17 hard-tail negative), already held with think-x4v4; new s(17) work on this project's proof route. #494 may want a note that the n = 17 route is suspended.

2026-10-31 bold-ritchie-l6 (stalled-bead triage of the 31 October intake pass, think-ztcy): Waits on the owner's standing n = 17 hold of 13 October (pending T-153); #494's note beside X-052 section 2.5 is held with think-x4v4.

2026-11-17 w5-audit-1117r (think-uz0m, the stalled-bead audit of the 17 November intake pass, think-p02d; read against main f9ddfeeef): (c) waits on the owner. The owner's n = 17 intake hold of 13 October (pending T-153, Overbeck's s(17) = L) still stands, checked today: T-153 reads V0/C1 in packing/frontier/results.yaml, its ten trees (about 21 CPU-h, under the cap) and its capture recomputation (about 1,273 CPU-h) are unrun (think-lqtu), and none of the eight 17 November decisions (think-b0w5, -fibh, -gmoj, -k2lh, -l7j0, -x30l, -0mup, -k8vt) touches n = 17. The hold is 35 days old; whether to keep it, lift it for T-153's ten trees, or lift it goes to the owner through the coordinator (think-uz0m's report). Nothing here runs until then. #494's float negative stays queued beside X-052 section 2.5.
