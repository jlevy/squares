---
type: is
id: is-01m1w4m3n2c2ab15q65nczknwe
title: "PR #100 review R6: devtool docstrings invoke a bare python interpreter"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m1w4krded865yyd393yn5my5
created_at: 2026-09-06T19:55:14.466Z
updated_at: 2026-09-06T19:55:30.695Z
closed_at: 2026-09-06T19:55:30.695Z
close_reason: Fixed in d663da6d on the PR branch.
resolution: null
duplicate_of: null
---
check_fractional_sweep.py and its test docstring said python -m ..., against AGENTS.md's interpreter rule; now the uv run form. Fixed in d663da6d.
