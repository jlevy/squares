---
type: is
id: is-01m28p7j0m5q03s1ae6jc0d8wb
title: "Phase 6B: the workbench's code comes under the floors"
kind: task
status: open
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
created_at: 2026-09-11T16:53:50.739Z
updated_at: 2026-09-11T21:09:08.038Z
---
build_candidate.py, check_workbench.py, check_revision6.py, check_revision7.py, test_candidate.py and the measurement tools are outside ruff and BasedPyright; the page's five thousand lines of JavaScript have no checker at all.

The Python half is mechanical: drop the spike's exclusion and fix what falls out.

The JavaScript half needs a decision, and the two honest options are a linter in the build (biome or eslint, pinned, run by build_candidate.py) or extracting the logic into modules the build inlines -- which is the same work Phase 6E wants for other reasons, so doing them together may be cheaper than doing either alone.

Done when: packing-validate --edit covers the workbench's Python, and a syntax or type error in the page's script fails a build rather than a viewer's console.

## Notes

The instruments landed as 7dd0233d: ruff 62 -> 0, format 14-of-15 -> 0, basedpyright 11 -> 0, re-verified by the coordinator.

check_workbench.py and probes.py joined them in e52b50a6, once think-7f3p took the JavaScript out: basedpyright 121 -> 0 (120 of the 121 were one wrong annotation on the drive helper), and the formatter ran over the file for the first time.

MEASURED and left: check_workbench.py still reports 373 ruff findings, of which 348 are E501 and every one of those is English prose inside a string literal -- the long OK sentence and the check() failure messages. The formatter does not reflow string contents, so closing these means re-wrapping implicit concatenations while keeping the joined text byte-identical. That wants a tool rather than a hand: the joined value is what the gate prints, and the gate's output is compared byte for byte. The other 25 are ordinary (B905 zip-without-strict x15, FBT003 x5, one each of C901, ERA001, FBT001, PLR0911, RUF005).

Still outside: build_candidate.py and the four remaining checkers, which want think-7f3p first for the same reason. Then the exclusion at pyproject.toml:166 comes out.
