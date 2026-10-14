---
type: is
id: is-01m4wv28mebp8r7ss9p8r6dgxy
title: "Import wand125: the closed-form lower bound s(N) >= a(N) for every non-square N >= 49 (closed-form-v1, eb0fd19), with its Rust replay checker (no issue)"
kind: task
status: in_progress
priority: 1
version: 2
delegate: serene-hopper
labels:
  - result-import
dependencies: []
parent_id: is-01m4wsqt2sjrksybyz375sarb3
hold: null
hold_until: null
created_at: 2026-10-14T09:14:32.462Z
updated_at: 2026-10-14T09:14:41.667Z
started_at: 2026-10-14T09:14:41.667Z
---
Found by the 2026-10-14 watch survey (think-fxs7): wand125/square-packing problems/closed-form (eb0fd19, 2026-10-13T09:36Z): s(N) >= a(N) for every non-square N >= 49, with a Rust replay checker; gives s(k^2-1), s(k^2-2), s(k^2-3) = k for k >= 8 without Nagamochi's lemma. The survey's own evaluation of a(N) from intervals.json (50-digit decimals, not the author's checker) beats the reported lower bound at 156 counts (104-116, 125-139, 148-164, 173-191, 201-220, 230-251, 261-284, 294-319) and the verified lower bound at 189. Stages 1-2, a priced replay of the author's checker, and a mathematical review of the theorem.
