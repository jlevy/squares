---
type: is
id: is-01m5249k5jzwfh92yjb8qe5mbp
title: "PR #651 A1: link #642 and #651 as a formal GitHub stack"
kind: task
status: closed
priority: 2
version: 4
delegate: user-eb-addr-642-651
labels:
  - result-import
dependencies: []
parent_id: is-01m51e5rvjrd61yaww8djj1nzz
hold: null
hold_until: null
created_at: 2026-10-16T10:32:01.969Z
updated_at: 2026-10-23T05:32:38.573Z
started_at: 2026-10-16T10:32:11.518Z
closed_at: 2026-10-23T05:32:38.573Z
close_reason: "Tracker audit 2026-10-23 (c-audit-c-1023, think-lrg9), checked by coord-intake-1023: DONE. Its own moot condition met: #642 merged 17:48Z and #651 17:50Z on 2026-10-16; #655 and #658 merged too"
resolution: null
duplicate_of: null
---
Found by PR #651 review A (https://github.com/jlevy/squares/pull/651#pullrequestreview-5546386141), A1 (High): #651's base is #642's branch (claude/ecstatic-edison-8en33t-intake-1016), and GET repos/jlevy/squares/stacks?pull_request=651 (and 642) returns [], so the chain is informal (tbd shortcut stacked-prs). Deferred: the gh-stack extension cannot be installed in this session (its download is refused by the session proxy, verified about 08:00Z on 16 October), so gh stack link cannot run here. Meanwhile both PR descriptions declare the chain and the merge order: #642 first, then retarget #651 to main. Done when the two PRs are a formal stack verified through the stacks API, or when #642 merges and #651 is retargeted to main (then close as moot).

## Notes

Extended (coordinator, 18:00Z) to the rest of the informal chain: #642 and #651 merged 17:48Z/17:50Z (merge commits abd65fba3, 26d8bb335), #655 retargeted to main, #658 stacks on #655's branch. #655 review B's B1 (High) defers here. A formal stack stays impossible while the session proxy refuses the gh-stack download; the merge order is stated in each description instead.
