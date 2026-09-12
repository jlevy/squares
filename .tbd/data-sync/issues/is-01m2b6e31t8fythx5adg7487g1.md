---
type: is
id: is-01m2b6e31t8fythx5adg7487g1
title: Replace the private selection-review script with a maintained exact checker
kind: task
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Sol implementation; root review
labels:
  - n11
  - tooling
  - review
dependencies:
  - type: blocks
    target: is-01m2b4yg9c8wm02dr21yhzn6vt
parent_id: is-01m2b4yg9c8wm02dr21yhzn6vt
created_at: 2026-09-12T16:15:30.873Z
updated_at: 2026-09-12T16:41:50.596Z
closed_at: 2026-09-12T16:41:50.593Z
close_reason: "Maintained exact checker and regression committed and pushed at 39714308; focused replay and test passed, the 45-step edit tier passed, and all hosted PR #156 checks passed."
resolution: null
duplicate_of: null
---
Move the exact arithmetic and finite-enumeration checks from /private/tmp/n11-selection-theorem-review-checks.py into a maintained repository entry point with focused regression coverage. Preserve the 256 availability profiles, 16 maximal products, D4 and fixed-wall orbit counts, 80 incidence count, 81 four-parent configurations, label sets, containment and separation margins, distant-wall comparison, and rational controls. Make the durable source-distinct review cite the maintained checker and a reproducible target-free command. Do not turn these finite controls into a global selection theorem or run a scientific target.

## Notes

Maintained checker and unmarked regression are now committed on PR #156 at `39714308`. The checker replays 256 profiles, 16 maximal products, the 3/10 orbit split, 80 incidences, all 81 four-parent controls, and exact rational margins. Focused checker and test pass; delegated edit tier passed all 45 selected steps. Awaiting hosted CI on the published head before closure.
