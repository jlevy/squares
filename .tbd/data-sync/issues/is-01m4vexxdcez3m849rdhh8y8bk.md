---
type: is
id: is-01m4vexxdcez3m849rdhh8y8bk
title: "PR #588 B1: reported second certificate accepted where the verified lane beats its value"
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4vex5amc35y6f4zqamve8q6
hold: null
hold_until: null
created_at: 2026-10-13T20:23:12.556Z
updated_at: 2026-10-13T20:51:07.843Z
started_at: 2026-10-13T20:23:27.437Z
closed_at: 2026-10-13T20:51:07.843Z
close_reason: "fixed in d3cfe11: verified-not-beaten guard in restates and problems; red test added"
resolution: null
duplicate_of: null
---
Severity Medium. PR #588 review https://github.com/jlevy/squares/pull/588#pullrequestreview-5509418328, finding B1. Where: packing/devtools/check_standing.py:278-282,359-365.
