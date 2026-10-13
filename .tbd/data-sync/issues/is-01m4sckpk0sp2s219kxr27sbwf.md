---
type: is
id: is-01m4sckpk0sp2s219kxr27sbwf
title: Retain each regularization run's per-count decision in the regularized layer's index
kind: task
status: open
priority: 2
version: 2
labels:
  - regularization
dependencies:
  - type: blocks
    target: is-01m4t5y8cd4b8kfymqjt7g3bwa
created_at: 2026-10-13T01:04:11.867Z
updated_at: 2026-10-13T08:55:08.047Z
---
The layer index (packing/atlas/known-best/regularized/index.json) gives every count 1..324 a status (90 regularized, 181 unchanged, 53 refused at #559), but the generator runs' per-count decisions (no change, held, review, refused, no view, and why) survive only as per-run totals; the run reports stayed in a session scratch. T-154's selection.json explains 40 of the 53 counts drawn as the witness; 5, 10, 11, 17, 19, 27, 38, 51, 52, 67, 89, 150 and 290 have no committed per-count reason. Add a compact per-count decision list to each run block (or a retained receipt beside the index), checked by --check-atlas, so the repository alone answers whether every count was regularized and why one was not.
