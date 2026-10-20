---
type: is
id: is-01m4s9p3cnbymsmkqby6jpsvc1
title: "regularize_evand: a --from-stage import re-run after a regularizer timeout needs regularize.json"
kind: bug
status: open
priority: 3
version: 1
labels:
  - regularization
dependencies: []
created_at: 2026-10-13T00:13:04.789Z
updated_at: 2026-10-13T00:13:04.789Z
---
Found in the stack review of #511 (12 October 2026): a regularizer timeout writes no regularize.json, so a later '--from-stage import' on that count raises FileNotFoundError and overwrites the count's decision with status: error, as a timed-out solve did before 94a87ecb5 (kept_solve). Keep the stored regularize block, or stop with a clear error naming --from-stage regularize, and test it. packing/devtools/regularize_evand.py, _run_stages.
