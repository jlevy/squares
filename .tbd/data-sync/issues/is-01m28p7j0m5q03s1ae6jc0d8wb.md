---
type: is
id: is-01m28p7j0m5q03s1ae6jc0d8wb
title: "Phase 6B: the workbench's code comes under the floors"
kind: task
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
created_at: 2026-09-11T16:53:50.739Z
updated_at: 2026-09-11T20:33:21.833Z
---
build_candidate.py, check_workbench.py, check_revision6.py, check_revision7.py, test_candidate.py and the measurement tools are outside ruff and BasedPyright; the page's five thousand lines of JavaScript have no checker at all.

The Python half is mechanical: drop the spike's exclusion and fix what falls out.

The JavaScript half needs a decision, and the two honest options are a linter in the build (biome or eslint, pinned, run by build_candidate.py) or extracting the logic into modules the build inlines -- which is the same work Phase 6E wants for other reasons, so doing them together may be cheaper than doing either alone.

Done when: packing-validate --edit covers the workbench's Python, and a syntax or type error in the page's script fails a build rather than a viewer's console.

## Notes

Revision: the JavaScript half of this bead is now its own chunk, think-7f3p (Phase 6D: no JavaScript or HTML inside Python), because the owner named it as a rule rather than as an option. What stays here is the Python half: drop the spike's exclusion and fix what falls out.

Measured 2026-09-11: dropping the exclusion reports 1,691 findings, of which 1,426 are E501 line-too-long and 168 are T201 print. Both are settings rather than work -- print is already allowed in devtools, cases, tests and the console scripts, and line length is the formatter's. That leaves about 97 real findings, top categories zip-without-strict (15), non-lowercase locals (9), manual list comprehensions (8), boolean positional arguments (7). Ruff fixes 12 directly and 209 more under --unsafe-fixes.
