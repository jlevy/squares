---
type: is
id: is-01m0vdq321tk8xmhf07dg4kwy2
title: Make multi-command test.sh steps fail on the first failed command
kind: bug
status: open
priority: 1
version: 2
spec_path: explorations/packing/campaign/agendas/agenda-003-balanced-ten-hour-research-program.md
labels: []
dependencies: []
created_at: 2026-08-25T02:59:13.088Z
updated_at: 2026-08-27T04:39:04.991Z
---
Discovered while migrating the n=3 SVG golden: step_small_n_moduli printed a nonzero terminal-component replay failure, continued to later commands, and the full gate reported ALL CHECKS PASSED. The current run_step conditional suppresses errexit inside invoked functions. Add a mutation control and make every step preserve the first failing command status.
