---
type: is
id: is-01m52ct0hx1ynh99j59jej4tze
title: "default_drawings --compare misses strong-view losses whose replacement is the axis tool's view (7 of 7 at #657's adoption)"
kind: bug
status: open
priority: 1
version: 1
labels:
  - regularization
dependencies: []
parent_id: is-01m50wdvvpwz9asfq2gvaxfz5w
created_at: 2026-10-16T13:00:48.573Z
updated_at: 2026-10-16T13:00:48.573Z
---
From PR #657 review B4 (https://github.com/jlevy/squares/pull/657#pullrequestreview-5548086952): #641's `default_drawings --compare` predicate (`falls_to_irregular_house` at 7aa4775ea) flags a strong view lost by a deferral or adoption only when the new drawing is the house drawing. After #657's adoption every new drawing at a lost strong view is the axis tool's view, so the predicate flags 0 of the 7 losses (176, 211, 232, 237, 264, 271, 302); the worst is 302: 0/0/0/14/14/978/978 -> 6/26/11/40/19/882/952. Fix in #641 (or a follow-up before the next adoption): flag any strong view whose replacement is worse on some goal of the improvement rule, whatever drew the replacement, with a test at a real-shaped count; then rerun --compare on #657 and list the losses for the owner.
