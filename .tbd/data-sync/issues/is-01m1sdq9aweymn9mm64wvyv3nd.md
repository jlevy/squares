---
type: is
id: is-01m1sdq9aweymn9mm64wvyv3nd
title: Promote the not-ours path predicate, deriving the vendored set from .gitmodules
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T18:36:32.475Z
updated_at: 2026-09-05T21:38:53.492Z
closed_at: 2026-09-05T21:38:53.492Z
close_reason: "Done with D-459: the not-ours predicate is devtools/repo_scope.py, deriving the vendored set from .gitmodules, and check_svg_rendering no longer types 'vendor' in its own frozenset."
resolution: null
duplicate_of: null
---
Six repo-wide sweeps hand-maintain near-identical literal exclusion sets; D-455 records the cost of that shape within one file and the same argument holds across files. Two layers: a shared 'not this repository at all' predicate (vendored submodules, node_modules, dot-directories) and per-check domain exclusions argued in place. Home: packing/src/sqpack/project.py, which already owns repository-state questions. Derive the vendored set from .gitmodules rather than the literal 'vendor', so a submodule added elsewhere is excluded automatically.
