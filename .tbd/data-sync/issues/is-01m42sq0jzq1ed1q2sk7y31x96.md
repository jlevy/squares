---
type: is
id: is-01m42sq0jzq1ed1q2sk7y31x96
title: "#305: merge main (#334), re-pin DATA_REVISION if needed, hosted CI green"
kind: task
status: closed
priority: 1
version: 4
delegate: claude-code@vm
labels: []
dependencies:
  - type: blocks
    target: is-01m42sq1hwn811q3t0jfz4dcsj
parent_id: is-01m42sq026mszrdm4fwf5r8g8y
hold: null
hold_until: null
created_at: 2026-10-04T06:30:39.967Z
updated_at: 2026-10-04T06:52:45.778Z
started_at: 2026-10-04T06:31:03.851Z
closed_at: 2026-10-04T06:52:45.778Z
close_reason: "Merged main (#334) into #305 as f60987ea8 (clean, no re-pin needed: release_pin --check passes). Local --records 43/43 steps; --push: 10,645 passed, only the two host-only process-group reaping tests fail (also fail on main ebe5415a7 here). Pushed; hosted CI pending on f60987ea8 and the review-fix push that follows."
resolution: null
duplicate_of: null
---
main moved past #305's last green head 498258a9f with #334 (pages/site-head contract, render_case_pages, render_overview, test_overview, test_case_pages). Textual merge is clean; prove the semantic merge: local --records/--edit plus the touched tests, then hosted CI green on the merge head.
