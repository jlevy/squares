---
type: is
id: is-01m4mbkx4jfae22h9h4evzbsy9
title: "Import evand: n17 hard tail, wall-chain elimination of width 1 misses m851903's obstruction, a float negative (#494)"
kind: task
status: open
priority: 3
version: 2
labels:
  - result-import
dependencies: []
created_at: 2026-10-11T02:10:37.842Z
updated_at: 2026-10-12T07:57:04.775Z
---
Issue https://github.com/jlevy/squares/issues/494 (evand, 2026-10-11T00:58:50Z), opened after the 2026-10-10 intake pass's sweep, so it belongs to the next pass. A negative, float only: X-052 section 2.5's width-1 wall-chain path relaxation, run on m851903 and the endpoint state 3439615 at evand/square-packing cd55295 (search/wallchain/, search/WALLCHAIN.md), barely separates m851903 from the true state (62 and 73 percent of sampled interior poses leave the ring feasible, against 82 percent for the control). Nothing is a certificate and nothing is claimed for the register. Next pass: stage 1 triage (enter #494 in result-requests.yaml with triage pending; record it as a negative for the n17 hard-tail lane, not a result), acknowledge the author. Held with the n = 17 intake (think-x4v4).

## Notes

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): existing issue https://github.com/jlevy/squares/issues/494 states the remaining work (reply https://github.com/jlevy/squares/issues/494#issuecomment-6119249272: a note beside X-052 section 2.5, held with think-x4v4). Tracker https://github.com/jlevy/squares/issues/544.
