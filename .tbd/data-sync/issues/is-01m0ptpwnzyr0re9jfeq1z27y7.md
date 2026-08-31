---
type: is
id: is-01m0ptpwnzyr0re9jfeq1z27y7
title: Gate and runner must not run concurrently; negctl corrupts tracked files in place
kind: bug
status: closed
priority: 2
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0pqfp4rm5r4fy7ys6t03h0w
created_at: 2026-08-23T08:10:05.887Z
updated_at: 2026-08-23T08:10:22.459Z
closed_at: 2026-08-23T08:10:22.459Z
close_reason: "Fixed in the same change: test.sh touches .gate-running with an EXIT trap, and every runner step that reads the record refuses while it is present."
resolution: null
duplicate_of: null
---
