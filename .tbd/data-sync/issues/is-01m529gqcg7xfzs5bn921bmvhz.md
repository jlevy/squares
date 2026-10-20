---
type: is
id: is-01m529gqcg7xfzs5bn921bmvhz
title: Grid-slack run blocks record summed wall time as cpu_seconds; fix the tool and the 16 October README figures
kind: task
status: in_progress
priority: 3
version: 2
delegate: user-eb-reg-3b3c
labels:
  - regularization
dependencies: []
parent_id: is-01m50wdrbfnwsq05w150az5z88
hold: null
hold_until: null
created_at: 2026-10-16T12:03:18.543Z
updated_at: 2026-10-16T12:03:24.936Z
started_at: 2026-10-16T12:03:24.936Z
---
Grid-slack run blocks record summed wall time under `cpu_seconds`.

`regularize_grid_slack.run_block` (packing/devtools/regularize_grid_slack.py, the cost block near line 1874) sums each report's `seconds`, which `run_one` measures with `perf_counter`. On a loaded host that is wall time, yet it is recorded as `cpu_seconds` (with `wall_seconds` the same number). All ten grid-slack run blocks in packing/atlas/known-best/regularized/index.json follow this convention, as do the retained `run.json` files under packing/cases/regularized_drawings/think-kpm3-2026-10-16/ and think-3zi3-2026-10-16/.

Two places say otherwise. #654 review A3: grid-slack-3c-deg05-1016 records 1,461.31 s, while the run's bash `time` logs give about 535 CPU-s. #653 review B1: the atlas README's think-kpm3 paragraph (packing/atlas/known-best/README.md, about line 273) says "3,916 CPU-seconds in all", using 1,843 CPU-s of grid-slack process time. No retained file holds that figure; the run.json blocks record 3,363 s of summed wall time under `cpu_seconds`. The think-3zi3 paragraph's "2,050 CPU-seconds in all" uses process time the same way.

To do:
1. Have `regularize_grid_slack` record process time per count (resource.getrusage, as the driver's receipt does) and sum that into `cpu_seconds`. Or, where no process time was measured, drop `cpu_seconds` and keep `wall_seconds` with the note.
2. Then correct the README's 16 October figures (think-kpm3 and think-3zi3 paragraphs) so they agree with what the record retains. Leave the existing blocks alone until the tool changes: the index check holds them to `run_block`.

Found by Review A of #654 (A3) and Review B of #653 (B1), 16 October 2026; deferred from both PRs.
