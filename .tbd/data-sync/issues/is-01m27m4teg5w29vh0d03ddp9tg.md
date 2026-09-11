---
type: is
id: is-01m27m4teg5w29vh0d03ddp9tg
title: Align the explainer release-history test with seven-place public decimals
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m26sv4284ry42pyavjhmmzqs
created_at: 2026-09-11T06:58:09.487Z
updated_at: 2026-09-11T06:58:59.463Z
closed_at: 2026-09-11T06:58:59.462Z
close_reason: Updated test_release to enforce the published seven-place form 3.8264474 with an ellipsis. All five release tests pass; exact-value validation remains in the theorem and claim records.
resolution: null
duplicate_of: null
---
The v0.4.0 release record correctly presents the lower bound as 3.8264474 with an ellipsis, but test_release still requires the superseded 18-place string. Update the assertion to enforce the seven-decimal public style without weakening the exact-value checks in research and claim records.
