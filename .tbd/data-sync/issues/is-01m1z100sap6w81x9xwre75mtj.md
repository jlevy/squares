---
type: is
id: is-01m1z100sap6w81x9xwre75mtj
title: render_explainer --output outside the repository renders everything and then exits non-zero
kind: bug
status: closed
priority: 3
version: 2
labels:
  - explainer
dependencies: []
created_at: 2026-09-07T22:49:33.736Z
updated_at: 2026-10-06T08:41:34.680Z
closed_at: 2026-10-06T08:41:34.680Z
close_reason: "Done in the renamed renderer: render_n11_lower_bounds_explainer.py on origin/main resolves --site once and prints every written path through 'relative_to(REPO) if is_relative_to(REPO) else str(path)' (lines 3291, 3308, 3326-3330), so output outside the repository no longer fails after rendering."
resolution: null
duplicate_of: null
---
Found by the PR #114 verification review (comment 5576356516): pre-existing since b9f85ed on main, packing/devtools/render_explainer.py near line 2249 lacks the is_relative_to guard its neighbouring paths have, so an --output outside the repository renders all outputs and then fails on the relative-path computation. Add the guard, a test with a temporary directory outside the repo, and decide whether outside-the-repo output is supported (then it must succeed) or refused (then it must refuse before rendering).
