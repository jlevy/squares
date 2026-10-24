---
type: is
id: is-01m5nq1pn7ja1gytv550typ670
title: "Efficiency: split the four fine-net sweeps into their own deep-gate job, or speed up exact_intersection_area (think-znx8 follow-up)"
kind: task
status: open
priority: 1
version: 3
labels: []
dependencies:
  - type: blocks
    target: is-01m5mg0a0fy7p6y69xxz9fbx2g
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T01:05:20.551Z
updated_at: 2026-10-24T03:07:56.430Z
---
Bring deep-gate `deferred-slow-lane` (and main's post-merge `slow-lane`, which runs the same Step on every push and on the daily cron, packing-validation.yml:821-861) back under a safe margin after #745 added the four whole 2,073-direction fine-net sweeps (n19, n20, n27, n31; 761 to 953 s in all).
Why (#745 review B1, https://github.com/jlevy/squares/pull/745#issuecomment-6379074892):
- xdist's default `load` mode handed all four sweeps to one worker on certifying run 40050481868 (gw2 at 1676 s, the other three idle for 548 to 575 s).
- The only limit that actually kills the run is the Step's 1800 s cap (`FAST_SUITE_BUDGET_SECONDS`, validate.py:263), and on the slower runner class (40033801674) the Step would end near 1850 s.
- think-tcsl's planned `mixed_n26_L5555.control.json` adds a fifth whole sweep automatically through `sweep_cases()`.
Smallest fix (the reviewer's): a separate cap for the slow step, `SLOW_SUITE_BUDGET_SECONDS = 2400.0`, next to validate.py:263, used in `Step("slow behavioral tests")` (~:5036-5040) and asserted in tests/test_validation_cli.py (~:3181-3186). It removes the kill without touching scheduling.
Better follow-ups: spread the sweeps across workers (`--dist` choice, or one sweep per node with a group), and/or speed up `exact_intersection_area` (3.20 of 5.03 s in a profile) about 3.4x.
Done when: the slow step has its own recorded cap with evidence, main's post-merge slow lane passes with margin on both runner classes, and gate-budgets.yaml records the measurement (OR-17).
