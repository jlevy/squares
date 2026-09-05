---
type: is
id: is-01m1sbmxxmmkweq9baxde2xs0e
title: "Fix D-455: the inline-SVG ownership check swept the vendored kpress submodule"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T18:00:18.099Z
updated_at: 2026-09-05T18:14:55.412Z
closed_at: 2026-09-05T18:14:55.412Z
close_reason: "Fixed as D-455: FOREIGN_DIRECTORY_NAMES states the exclusion once and both sweeps draw from repository_documents(). Regression in packing/tests/test_check_svg_rendering.py, in the fast tier because the gate that caught it runs only on main."
resolution: null
duplicate_of: null
---
check_svg_rendering's document sweep excluded resources, node_modules and dot-prefixed directories but not vendor/, so the kpress submodule's own fixtures failed the all_inline_svg_targets_are_owned_artifacts control. Red on main across three merges. Fixed by stating the exclusion once as FOREIGN_DIRECTORY_NAMES and drawing both sweeps from one repository_documents() generator.
