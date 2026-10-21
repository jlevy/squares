---
type: is
id: is-01m5fremhm4c78ag7ht2ethyte
title: "PR #704 B4: the snapshot note in run_negative_controls.py records a stale figure"
kind: bug
status: open
priority: 3
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m5fre23qy5rq285h9tsarhz0
created_at: 2026-10-21T17:34:26.355Z
updated_at: 2026-10-21T17:34:26.355Z
---
Low. packing/devtools/run_negative_controls.py:236-242 at d2eca7108: the note records 232,767,018 bytes; --source-bytes read 232,768,595 at the head. Review B: https://github.com/jlevy/squares/pull/704#issuecomment-6306759614
