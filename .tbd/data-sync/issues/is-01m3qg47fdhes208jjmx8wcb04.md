---
type: is
id: is-01m3qg47fdhes208jjmx8wcb04
title: Replace false-positive repository-walker test selection with context-aware evidence
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies: []
parent_id: is-01m3p5wj25knm7rbx0g4a4tpvg
created_at: 2026-09-29T21:11:28.492Z
updated_at: 2026-09-29T22:06:21.462Z
closed_at: 2026-09-29T22:06:21.460Z
close_reason: Published in 9174140a8; 54 focused selector controls, the 7714-test broad run, documentation repair gate, and required Packing validation36636555656 passed. Conservative marker-bearing code/string coverage retained; only comments and the exact benign metadata import lose walker status.
resolution: null
duplicate_of: null
---
The original documentation-selection audit found WALKER_MARKERS substring matches for attack strings, importlib.metadata.version, temporary-directory-only globs and comments. Preserve actual repository walkers and dynamic imports, add positive and refusal controls, and measure selected files before narrowing. This is separate from worker scheduling and hosted fanout; do not claim it fixed by parallel execution.

## Notes

Session164 Sol bounded implementation: AST walker evidence now excludes comments and the exact benign from-importlib.metadata version import; real glob/listdir and dynamic import uses remain selected, and all old marker-bearing string literals remain conservative (including attack/alias/helper execution). Same retained frontier-path probe changed 82/387 to 81/388 selected after adding one dedicated regression test file; independent scan found only two existing walker-selection removals: test_change_scoped_selection.py (comment), test_command_help.py (metadata). Focused 43 tests pass; Ruff and BasedPyright clean. Broader gate and speed effect unmeasured; root owns integration.
