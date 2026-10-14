---
type: is
id: is-01m4w0w8x81jgrxwd2dshv8f0v
title: "PR #592 (merge): formalization kind, n = 17 correctness reviews, documented independence of confirmations"
kind: task
status: in_progress
priority: 1
version: 13
delegate: codex@spud10.local
labels: []
dependencies: []
child_order_hints:
  - is-01m4w46vwppxrngcwfqaec682g
  - is-01m4w46wctqb23441kpe4ksg17
  - is-01m4w46wxs3d28feb8vm671ge8
  - is-01m4w46xdak0nd3kmxcp1zm4vq
  - is-01m4w46xw173rgshbzzkr2zzhy
  - is-01m4w46ybr3v07r4statsr8eme
  - is-01m4w46yvdzemx6xfb596cnz55
  - is-01m4w46zc6xmqckenrsfk9gf5s
hold: null
hold_until: null
created_at: 2026-10-14T01:36:53.160Z
updated_at: 2026-10-14T04:45:31.493Z
started_at: 2026-10-14T01:36:54.191Z
---

## Notes

Owner's authorization in this session (14 October): 'continue and PR and review and merge'.
Round 1: review A (senior) at 7a1aadceb, https://github.com/jlevy/squares/pull/592#issuecomment-6159185393 — approve with changes; no Blocker/High; A1 M (proof-assistant test reads target's evidence), A2 M (precedence refusal not stated by owner; record 'simplification should be allowed too but that is different'), A3 L, A4 L, A5 L, A6-A8 Nit.
Coordinator decision on A2: drop the hard refusal of a simplification citing proof-assistant evidence; record the third remark verbatim; formalization requires its own proof-assistant-checked evidence; where both fit the owner decides. Put the question to the owner in the report.
Plan: the writer finishes -> push -> one moderate addresser for A1-A8 -> round 2: B senior follow-up of everything after 7a1aadceb, C correctness of the independence record -> address -> gate -> merge -> site audit.
