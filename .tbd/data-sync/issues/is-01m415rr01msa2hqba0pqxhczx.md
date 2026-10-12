---
type: is
id: is-01m415rr01msa2hqba0pqxhczx
title: "CI: record the measure-verifier tier's first hosted measurement"
kind: chore
status: in_progress
priority: 2
version: 2
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m3yrezbcgcr728c37fq49bvf
hold: null
hold_until: null
created_at: 2026-10-03T15:22:50.752Z
updated_at: 2026-10-09T22:15:56.293Z
started_at: 2026-10-09T22:15:56.293Z
---
The measure verifier's gate moved out of the checks tier into its own pull-request tier and job (measure_verifier, PR #311) after the checks tier read 168.3 s against 140 s (run 37098372802) and 137.93 s (run 37131940076). The tier is declared in packing/devtools/gate-budgets.yaml with a ceiling and a pending measurement under this bead. Close it by replacing the pending fields with the geometric mean of the first hosted cohort (python -m devtools.read_tier_walls --tier measure_verifier --run-id ...), checking the ceiling against the 2x headroom rule.
