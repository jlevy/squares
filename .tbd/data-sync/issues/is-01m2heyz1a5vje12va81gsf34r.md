---
type: is
id: is-01m2heyz1a5vje12va81gsf34r
title: "PR #160 review D66: contract tests write fixtures into the source tree and race under xdist"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:39:59.017Z
updated_at: 2026-09-15T02:40:58.167Z
closed_at: 2026-09-15T02:40:58.166Z
close_reason: "Fixed on #160 at f7a640a2: ESLint and Ruff probes read stdin at an in-scope path, other fixtures use tmp_path; nothing is written into the source tree (floor and lint contract files pass under -n 4)."
resolution: null
duplicate_of: null
---
Review finding, PR #160 stack triage (2026-09-14), lane D-tools.

Two contract tests created fixtures inside the source tree, racing `test_every_first_party_script_is_in_a_type_program` (which lists untracked files) under xdist.

Source: #160 R18.

Files: `packing/tests/test_browser_floor_contract.py:274-289`; `packing/tests/test_lint_floor_contract.py:190-205`.
