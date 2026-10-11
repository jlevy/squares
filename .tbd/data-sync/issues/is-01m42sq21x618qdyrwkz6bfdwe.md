---
type: is
id: is-01m42sq21x618qdyrwkz6bfdwe
title: "#323: retarget to main, catch up, re-pin, regenerate, green CI"
kind: task
status: closed
priority: 1
version: 3
labels: []
dependencies:
  - type: blocks
    target: is-01m42sq2jz809z5ccym3jj0qwy
parent_id: is-01m42sq026mszrdm4fwf5r8g8y
created_at: 2026-10-04T06:30:41.469Z
updated_at: 2026-10-06T08:32:56.898Z
closed_at: 2026-10-06T08:32:56.898Z
close_reason: "Done: #323 landed on main with #305 in e19be6bb0 (both MERGED 2026-10-04 23:00Z); the retained-JSON layout and its check (b4f0638b5, check_retained_json) are on origin/main."
resolution: null
duplicate_of: null
---
After #305 merges: retarget base to main, merge main, resolve the DATA_REVISION conflict in packing/src/sqpack/release.py by re-pinning, regenerate composite-figure.json and bound-citations.json with their writers, run check_retained_json and --records, hosted CI green. Review pass per pr-review-requirements.
