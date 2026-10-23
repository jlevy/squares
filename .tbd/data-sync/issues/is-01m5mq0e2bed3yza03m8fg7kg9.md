---
type: is
id: is-01m5mq0e2bed3yza03m8fg7kg9
title: "PR #752 A1: T-157's next_rung counts the 23 October review toward rung 4"
kind: bug
status: closed
priority: 1
version: 3
delegate: c-review-sqvc-1023
labels: []
dependencies: []
parent_id: is-01m5mpzs25g0r8zzepe0c8fmka
hold: null
hold_until: null
created_at: 2026-10-23T15:45:24.555Z
updated_at: 2026-10-23T16:25:50.433Z
started_at: 2026-10-23T15:45:43.090Z
closed_at: 2026-10-23T16:25:50.432Z
close_reason: "fixed in 6dccc9d7e (fix a): the review's item on T-192 only, T-157's next_rung restored; with one synthetic oversight record T-157 stays V3/C3. Reply: https://github.com/jlevy/squares/pull/752#issuecomment-6369600734"
resolution: null
duplicate_of: null
---
Severity High. packing/frontier/results.yaml:19709-19715 (T-157 next_rung) and the reviews items on T-145 (results.yaml ~16026) and T-157 (~19629); docs/project/reviews/review-2026-10-23-wand125-sqverify-continuous-soundness.md:699-702 (section 9). One synthetic human oversight record lifts T-157 to V4/C4 on the strength of a review that decided no part of its cover. Coordinator's call: fix (a), the accepted reviews item on T-192 only, cite the review from T-145 and T-157 without a reviews item, restore T-157's next_rung; add the item to T-145 and T-157 after think-flxm replays the mode. Review: https://github.com/jlevy/squares/pull/752#issuecomment-6368625335 (PR #752, review A, head ad0d4ea1f).
