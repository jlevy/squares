---
type: is
id: is-01m7hewzayyc5nrepf8k7ygx0h
title: "Import #1001: JoeGun's five upper bounds on Kodaj's packings (s(127), s(204), s(232), s(264), s(305)) at bc10ce4"
kind: task
status: in_progress
priority: 1
version: 4
delegate: bold-ritchie-l187
labels: []
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-16T05:57:22.906Z
updated_at: 2026-11-16T06:34:48.395Z
started_at: 2026-11-16T05:58:26.297Z
---

## Notes

L187 (bold-ritchie-l187), 2026-11-16: claimed 05:58Z (claimed [think-0y9m], skipped []), synced. Worktree claude/bold-ritchie-xo28us-l187 off origin/main 31ddae6fe. Source JonathanGun/square-packing-upper-bounds: git ls-remote head bc10ce471c9d7841b9a53b383dae87d23dbe5a99 (06:01:23Z), the only commit (2026-11-16T05:31:52Z, before #1001 at 05:33:07Z); cloned into scratch l187-dl/src/repo; all five n-NNN-candidate.yaml match the issue's SHA-256 list (sha256sum -c OK). Kaggle (www.kaggle.com, Kodaj's notebook and the kernels API) refused by the session proxy, CONNECT 403 at 06:01:47Z: the notebook is not reachable from this container.
Controls plan stated before any program decided any certificate: scratch l187-notes/controls-plan-1001.md SHA-256 6c25dc71c13eb471a0d2d6118c9f1131bbf8aa9a87839dab1b9624991b6cad35, hashed 06:03:24Z; 15 gross jobs (3 per count) and 55 sharp rows (11 per count), with the touching-wall branch (expected at 232) and the touching-pair branch stated in advance.

Intake commit b3a0c1b01 (06:34:00Z): packet joegun-upper-bounds-2026-11-16 (whole tree, 16 retained + Evan Daniel's notice pinned; CC BY 4.0 / MIT; check.py, make-pose.py never run). Replay: 15 jobs on both routes, 819,474 pair decisions, 252 route CPU-s, check --replay re-decided all 15 (4.9 min); all 55 sharp controls as stated (plan 6c25dc71, 06:03:24Z), touching-wall branch at every count; least wall clearance 0, least pair gaps 1.1203e-11 (127: 50,54), 1.1203e-11 (204: 8,109), 9.97e-13 (232: 188,197), 1.2e-12 (264: 255,256), 1.1251e-11 (305: 130,137). Gains below houses: 127 T-174 9.1249e-3; 204 T-268 1.7145e-3; 232 T-275 1.8780e-3; 264 T-186 9.2753e-4; 305 T-174 4.7041e-3. Identity: not 1:1 with any house; 70/73/35/44/113 squares beyond 0.1 -> new arrangements relative to the record. House margins 0, 1.48e-19, 3.00e-12, 1.68e-99, 0 (RV-3 does not reach); own margins 1.21e-10, 1.55e-10, 1.47e-11, 1.89e-11, 1.91e-10. L-step scan = main's. Ledger upper-bounds-1001-20261116 records #1001 at all five; Kodaj's quoted 270 listed as other item, not claimed. Nothing of L186 read.
