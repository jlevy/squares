---
type: is
id: is-01m50y8gbv8rbst9heyhwqgvra
title: "PR #631 C1 (suggestion): keep stack #632 merge-shaped when propagating fixes or landing"
kind: bug
status: closed
priority: 4
version: 3
delegate: addressing-632-af04656
labels: []
dependencies: []
parent_id: is-01m50y7s34ay3eywkrfp10p3xv
hold: null
hold_until: null
created_at: 2026-10-15T23:27:20.443Z
updated_at: 2026-10-15T23:44:09.108Z
started_at: 2026-10-15T23:27:24.711Z
closed_at: 2026-10-15T23:44:09.108Z
close_reason: "fixed (option 1): review-A fixes carried up by merge d533a91f1, release_pin --check 4cb98fc87def at f04a38eb7 and 425b5deed, landing command in #631's description; reply https://github.com/jlevy/squares/pull/631#issuecomment-6204616534"
resolution: null
duplicate_of: null
---
Low, suggestion, stack-level. DATA_REVISION in #627 (a6756dc5) and #628 (4cb98fc8) names merge commits; gh stack rebase --upstack / gh stack sync would linearize and break test_release.py. Carry fixes upward by merging and land with gh stack merge 631 --yes --merge. Review C: https://github.com/jlevy/squares/pull/631#pullrequestreview-5541107123
