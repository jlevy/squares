---
type: is
id: is-01m4yx3avzeb0mx1esvgr6epcs
title: Record each control's mutated output before and after a worker-content change
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies: []
parent_id: is-01m1sx5m1p5868jhwcdzfkvada
created_at: 2026-10-15T04:28:33.534Z
updated_at: 2026-10-15T04:28:33.534Z
---
From review A7 of PR #611 (https://github.com/jlevy/squares/pull/611#issuecomment-6184210564). Unmutated equality (run_negative_controls --baseline) shows a checker reads the same before a mutation, and '174 fire' shows no control went green. Neither shows each control fires for the same reason: a dropped file read only on a mutated path, whose absence happens to print the expected message, passes both. Extend --baseline (or add a mode) to record each control's mutated stdout/stderr in a worker and diff main against a head that changes what workers hold. Done when: the mode exists with a test, and one prune or copy-back change is shown with mutated outputs equal apart from wall times.
