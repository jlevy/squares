---
type: is
id: is-01m4my11svdqyac7jkn0s46n0e
title: "PR #497 S3: section 4.4 re-decision cost is at the 450 s ceiling, to be measured"
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-code@spud10
labels:
  - regularization
dependencies: []
parent_id: is-01m4my092ypz9gkxjqdy3nr3tp
hold: null
hold_until: null
created_at: 2026-10-11T07:32:22.971Z
updated_at: 2026-10-11T18:54:16.272Z
started_at: 2026-10-11T07:32:36.455Z
closed_at: 2026-10-11T18:54:16.270Z
close_reason: "fixed in 5c9f4f227: re-decision step at the 450 s ceiling, measured before arming (OR-17); reply https://github.com/jlevy/squares/pull/497#issuecomment-6112491605"
resolution: null
duplicate_of: null
---
Suggestion. 1800 s / 4 = 450 s, the ceiling itself (OR-17); development.md derives 450 s from an 800 CPU-s step at four workers. PR #497, review A: https://github.com/jlevy/squares/pull/497#pullrequestreview-5482306635
