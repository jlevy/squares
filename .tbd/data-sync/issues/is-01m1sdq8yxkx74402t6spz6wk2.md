---
type: is
id: is-01m1sdq8yxkx74402t6spz6wk2
title: check_documentation fails on a clone without submodules
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T18:36:32.093Z
updated_at: 2026-09-05T21:38:53.181Z
closed_at: 2026-09-05T21:38:53.180Z
close_reason: "D-459. Reproduced on a submodule-less clone: 'document exclusion is empty: vendor/**/*.md'. devtools/repo_scope.py reads .gitmodules, both sweeps use it, the map pattern is deleted, and the guard matches patterns the way the loader does rather than by prefix."
resolution: null
duplicate_of: null
---
docs/project/document-map.yaml carries 'pattern: vendor/**/*.md' and the loader requires every exclusion to match something, so with vendor/ present but not checked out the check emits 'document exclusion is empty: vendor/**/*.md'. A plain git clone therefore fails the docs check; CI is safe only because both workflows pass submodules: true. Cleanest fix is for check_documentation to take the shared not-ours predicate in code, after which the map entry can be deleted.
