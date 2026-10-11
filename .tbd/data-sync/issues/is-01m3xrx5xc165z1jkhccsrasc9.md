---
type: is
id: is-01m3xrx5xc165z1jkhccsrasc9
title: "Import wand125: mixed rectangle-measure certificate at n = 76 (#282 comment of 2026-10-02, 7975030)"
kind: task
status: closed
priority: 2
version: 5
labels:
  - result-import
  - packing
dependencies:
  - type: blocks
    target: is-01m3yrzkz80qd1wv5sjr0kkkv0
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-02T07:40:21.292Z
updated_at: 2026-10-03T22:47:15.469Z
closed_at: 2026-10-03T22:47:15.468Z
close_reason: T-072 V3/C3 on main.
resolution: null
duplicate_of: null
---
Result import process, H. 447/50 = 8.94 by 317 rectangles, mass 7599999/100000, same checker as T-048/T-069 (mixed_rotated_verify.cpp). Stage 2: packet at 7975030; stage 3: new entry (a later release adding a count), V0/C0; stage 4: mixed-replay + review addendum. Above rect_n76 (8.925, T-068).

## To finish (validation backlog, 2026-10-02)

T-072 (s(76) >= 447/50) reached V3/C3 on 2 October on PR #298's branch: the complete replay matched the shipped run at all 201 directions (3.64 CPU-hours). To finish: the control on this certificate (`.venv/bin/python3 -m devtools.audit_wand125_point_and_mixed mixed-control n76 --work W`, a few minutes), merge PR #298, close this bead, and draft #282's reply from main.
