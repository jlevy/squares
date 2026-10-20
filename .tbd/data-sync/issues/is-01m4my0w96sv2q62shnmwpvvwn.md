---
type: is
id: is-01m4my0w96sv2q62shnmwpvvwn
title: "PR #497 A6: mathematics written as code, not math spans (conventions.md section 10)"
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
created_at: 2026-10-11T07:32:17.316Z
updated_at: 2026-10-11T18:54:12.487Z
started_at: 2026-10-11T07:32:33.030Z
closed_at: 2026-10-11T18:54:12.484Z
close_reason: "fixed in 5c9f4f227: math spans, file in math-markup.yaml; check_math_markup, check_katex, check_math_spans pass; reply https://github.com/jlevy/squares/pull/497#issuecomment-6112491605"
resolution: null
duplicate_of: null
---
Low. No $...$ span in the report; run migrate_math --apply and check_math_markup. PR #497, review A: https://github.com/jlevy/squares/pull/497#pullrequestreview-5482306635
