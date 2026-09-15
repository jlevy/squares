---
type: is
id: is-01m2hf8dqrw7gqp7a2nwv4w2hz
title: "PR #155 review D05: H-207..H-209 declare instrument_ready for sweeps the harness cannot run"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2hb40g8vbnq8914rkt7p87c
created_at: 2026-09-15T02:45:08.983Z
updated_at: 2026-09-15T02:45:08.983Z
---
Review: attic/reviews/pr155/review-pr155-d46b86a5.md (PR #155 review at d46b86a5). Parent: think-xqc3.

Source: #155 R1 (record item). Code item (unknown --sweep keys dropped, clamped values recorded as requested) is fixed on #160 at f9099096 (workbench_tools/benchmark.py:369-378, trial_records.py:555-583).

Files: packing/campaign/hypotheses/H-207-restarts-beat-schedule.md:24, H-208-the-drop-decides.md:23 (against :46-48), H-209-no-parameters-reach-a-record.md:23.

Fix: instrument_ready false on all three, each naming the instrument its test needs. Instrument work itself stays with think-fj07.
