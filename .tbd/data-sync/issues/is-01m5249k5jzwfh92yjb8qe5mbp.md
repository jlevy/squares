---
type: is
id: is-01m5249k5jzwfh92yjb8qe5mbp
title: "PR #651 A1: link #642 and #651 as a formal GitHub stack"
kind: task
status: in_progress
priority: 2
version: 3
delegate: user-eb-addr-642-651
labels:
  - result-import
dependencies: []
parent_id: is-01m51e5rvjrd61yaww8djj1nzz
hold: null
hold_until: null
created_at: 2026-10-16T10:32:01.969Z
updated_at: 2026-10-16T17:51:13.120Z
started_at: 2026-10-16T10:32:11.518Z
---
Found by PR #651 review A (https://github.com/jlevy/squares/pull/651#pullrequestreview-5546386141), A1 (High): #651's base is #642's branch (claude/ecstatic-edison-8en33t-intake-1016), and GET repos/jlevy/squares/stacks?pull_request=651 (and 642) returns [], so the chain is informal (tbd shortcut stacked-prs). Deferred: the gh-stack extension cannot be installed in this session (its download is refused by the session proxy, verified about 08:00Z on 16 October), so gh stack link cannot run here. Meanwhile both PR descriptions declare the chain and the merge order: #642 first, then retarget #651 to main. Done when the two PRs are a formal stack verified through the stacks API, or when #642 merges and #651 is retargeted to main (then close as moot).

## Notes

Extended (coordinator, 18:00Z) to the rest of the informal chain: #642 and #651 merged 17:48Z/17:50Z (merge commits abd65fba3, 26d8bb335), #655 retargeted to main, #658 stacks on #655's branch. #655 review B's B1 (High) defers here. A formal stack stays impossible while the session proxy refuses the gh-stack download; the merge order is stated in each description instead.
