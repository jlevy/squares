---
type: is
id: is-01m51568exrdg1j7267aj1kvhh
title: "Regularization record: keep per-count run outcomes (decisions) on each atlas index entry, from the reports regularize_evand layer reads, so 'ran, nothing better' needs no hand-written SETTLED entry"
kind: task
status: open
priority: 2
version: 1
labels:
  - regularization
dependencies: []
parent_id: is-01m50wdrbfnwsq05w150az5z88
created_at: 2026-10-16T01:28:26.844Z
updated_at: 2026-10-16T01:28:26.844Z
---
Deferred from jlevy/squares#636 review A7 (https://github.com/jlevy/squares/pull/636#pullrequestreview-5541598868). The audit's minimal change item 2 (think-y1x3): record each strong generator run's outcome on the index entry it decided (generator, run id, outcome, on the witness's source key/path/revision and side), written by regularize_evand layer and the grid-slack admission from the per-count reports they already read, so default_drawings derives decided-no-better from the index instead of SETTLED's prose. Then retire the decided-no-better SETTLED entries whose runs it records. Waits on: #636 merging (the state record and gate it extends).
