---
type: is
id: is-01m15b67k65dz0mcqmdcwq1812
title: Repoint config, CI and the path constants
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m15219m6eh8fww5pm9sc2sqd
created_at: 2026-08-28T23:27:27.845Z
updated_at: 2026-08-28T23:27:30.458Z
closed_at: 2026-08-28T23:27:30.457Z
close_reason: Landed in the reorg branch
resolution: null
duplicate_of: null
---
Config: .flowmarkignore, .gitattributes, .gitignore lose the old prefix. .flowmarkignore matters most -- check_generated_markdown compares md.relative_to(REPO) against its lines.

CI: four working-directory settings become packing; drop the push path filter, since the project now spans the root and a filter naming one subtree would skip the gate on the documents it validates. tests/test_module_boundaries.py pins that shape and changes with it.

Constants, two groups: eight that climbed to the repository root lose one level; eight more in five modules gain a REPO = ROOT.parent, because README, SYNOPSIS, defects.md and the reports no longer live under ROOT.

Also: controls.yaml reaches ../ not ../../, and pyproject.toml drops readme = README.md, which is now outside the build root.
