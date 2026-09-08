---
type: is
id: is-01m1z100sap6w81x9xwre75mtj
title: render_explainer --output outside the repository renders everything and then exits non-zero
kind: bug
status: open
priority: 3
version: 1
labels:
  - explainer
dependencies: []
created_at: 2026-09-07T22:49:33.736Z
updated_at: 2026-09-07T22:49:33.736Z
---
Found by the PR #114 verification review (comment 5576356516): pre-existing since b9f85ed on main, packing/devtools/render_explainer.py near line 2249 lacks the is_relative_to guard its neighbouring paths have, so an --output outside the repository renders all outputs and then fails on the relative-path computation. Add the guard, a test with a temporary directory outside the repo, and decide whether outside-the-repo output is supported (then it must succeed) or refused (then it must refuse before rendering).
