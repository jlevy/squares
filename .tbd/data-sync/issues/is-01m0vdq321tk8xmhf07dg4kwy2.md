---
type: is
id: is-01m0vdq321tk8xmhf07dg4kwy2
title: Make multi-command test.sh steps fail on the first failed command
kind: bug
status: closed
priority: 1
version: 4
spec_path: explorations/packing/campaign/agendas/agenda-003-balanced-ten-hour-research-program.md
labels: []
dependencies: []
created_at: 2026-08-25T02:59:13.088Z
updated_at: 2026-08-27T05:39:27.360Z
closed_at: 2026-08-27T05:39:27.360Z
close_reason: PR 41's Python validator already removed the defective Bash execution path; session 026 added an end-to-end two-command CLI regression, a mutation that proves swallowed first failures are caught, and D-340. All 68 negative controls and the four-step integration surface pass.
resolution: null
duplicate_of: null
---
Discovered while migrating the n=3 SVG golden: step_small_n_moduli printed a nonzero terminal-component replay failure, continued to later commands, and the full gate reported ALL CHECKS PASSED. The current run_step conditional suppresses errexit inside invoked functions. Add a mutation control and make every step preserve the first failing command status.

## Notes

Claimed in session 026 phase 1. Reproduce the real multi-command run_step failure, add a failing mutation regression before production changes, repair the narrowest shared first-failure boundary, and require nonzero gate status without ALL CHECKS PASSED.
