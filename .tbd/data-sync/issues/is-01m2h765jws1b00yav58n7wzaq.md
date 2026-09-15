---
type: is
id: is-01m2h765jws1b00yav58n7wzaq
title: Extract JavaScript from the workbench package checkers
kind: task
status: open
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2h76347zn3abcahzd3642ac
created_at: 2026-09-15T00:24:06.491Z
updated_at: 2026-09-15T00:24:20.814Z
---
Extract the remaining JavaScript strings in `packages/workbench/tools/workbench_tools/` (about 50 lines over 8 files) into the package's `probes/`.

The files include `check_pack_panel.py` (8 calls), `check_probes.py`, `check_workbench.py` and others the guard lists. The two `check_workbench.py` strings added on 2026-09-14 are among them: the stage-rect read in `headline_gaps` and the `getSelection().removeAllRanges()` call.

Do this after PRs #160 and #171 have had their reviews addressed, because the same files are likely to change there. Acceptance: the allowlist is empty and `check_probes` covers the new probes.
