---
type: is
id: is-01m4vcsmrz2t2sf7p05tx04zac
title: Date grid-slack runs from a recorded time, not report mtimes
kind: bug
status: open
priority: 3
version: 1
labels:
  - regularization
dependencies: []
created_at: 2026-10-13T19:45:55.487Z
updated_at: 2026-10-13T19:45:55.487Z
---
Found while fixing #548 review B5 (which fixed regularize_evand.run_block). devtools/regularize_grid_slack.py run_block dates a run by the latest report.json modification time (finished = max(path.stat().st_mtime)); Git keeps no mtimes, so a copied or restored run directory is dated the day it was copied. Have run_one write the time into each report (or a run receipt) and read it there, keeping the index's own date for older runs as regularize_evand.dated_runs does.
