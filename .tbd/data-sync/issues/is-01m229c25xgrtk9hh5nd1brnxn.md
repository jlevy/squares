---
type: is
id: is-01m229c25xgrtk9hh5nd1brnxn
title: Build Calibrate, the third workbench mode
kind: feature
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels:
  - packing
dependencies: []
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-09T05:13:40.284Z
updated_at: 2026-09-09T05:14:06.971Z
---
Calibrate is Pack's strategy panel with a loop and a results table around it, which is why it is cheap once Pack and Animate are clean. Scope: a set of cases, split into cases tuned on and cases held back. Mechanics: the same single-n settle repeated while parameters sweep, keeping what performed best. Report two kinds of best and the gap between them, because that gap is the point: per run, the configuration that reached the lowest container side, which is the one most likely to be luck; statistically, the configuration whose distribution over seeds is best by median or hit rate, which is the one to believe. Named Calibrate rather than Backtest deliberately: it is the accurate description, it is already this repository's word (series-000-smoke-and-calibration, and the atlas pinning its calibration-only layers to the first hundred so the rest stays unseen), and it makes the overfitting hazard structural rather than a caution in prose. The held-out split is declared once per session before the first run, because a split chosen after seeing results is not a split. Framed in packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md. Deferred until Pack and Animate settle.
