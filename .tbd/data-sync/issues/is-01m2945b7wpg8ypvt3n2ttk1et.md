---
type: is
id: is-01m2945b7wpg8ypvt3n2ttk1et
title: measure_law.py points at a page that does not exist
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-11T20:57:18.330Z
updated_at: 2026-09-11T20:57:18.330Z
---
`measure_law.py` hard-codes `PAGE = HERE / "workbench.html"` and takes no argument to override it. That file is not what the generator writes beside it -- the built page there is `index.html` -- so the instrument cannot run as shipped. It was only measured during Phase 6B by patching `PAGE` from a wrapper.

`measure_greens.py` has the same stale default but accepts a positional path, so it runs when given one. Give `measure_law.py` the same positional argument, and while there, check every instrument in the tree for the same hard-coded default -- the page's name changed and the instruments were not all told.

A behaviour defect rather than a lint one, which is why Phase 6B left it alone.
