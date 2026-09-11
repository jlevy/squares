---
type: is
id: is-01m28p7j0m5q03s1ae6jc0d8wb
title: "Phase 6B: the workbench's code comes under the floors"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-11T16:53:50.739Z
updated_at: 2026-09-11T16:53:50.739Z
---
build_candidate.py, check_workbench.py, check_revision6.py, check_revision7.py, test_candidate.py and the measurement tools are outside ruff and BasedPyright; the page's five thousand lines of JavaScript have no checker at all.

The Python half is mechanical: drop the spike's exclusion and fix what falls out.

The JavaScript half needs a decision, and the two honest options are a linter in the build (biome or eslint, pinned, run by build_candidate.py) or extracting the logic into modules the build inlines -- which is the same work Phase 6E wants for other reasons, so doing them together may be cheaper than doing either alone.

Done when: packing-validate --edit covers the workbench's Python, and a syntax or type error in the page's script fails a build rather than a viewer's console.
