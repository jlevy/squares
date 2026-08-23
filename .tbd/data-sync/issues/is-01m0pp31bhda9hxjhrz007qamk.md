---
type: is
id: is-01m0pp31bhda9hxjhrz007qamk
title: README's layout tree omits seven files that exist
kind: bug
status: closed
priority: 3
version: 2
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0pp24qsn326dyxy9na7wc50
created_at: 2026-08-23T06:49:21.009Z
updated_at: 2026-08-23T07:01:15.143Z
closed_at: 2026-08-23T07:01:15.143Z
close_reason: "Layout tree gains conventions.md, defects.yaml, defects.schema.yaml, differential_test.py and run_baseline.sh. It is no longer hand-maintained on trust: check_readme.py compares it against the directory listing in both directions, and caught the last missing entry itself."
resolution: null
duplicate_of: null
---
Missing from the tree: conventions.md, defects.yaml, defects.schema.yaml, differential_test.py, run_baseline.sh, pyproject.toml, uv.lock. conventions.md is the worst omission -- README devotes a section to it but the tree does not show it. Refresh the tree, and consider a check that compares it against the directory listing, since this is the third generated-or-hand-maintained view in this directory to drift (D-010, D-017, D-022, D-028).
