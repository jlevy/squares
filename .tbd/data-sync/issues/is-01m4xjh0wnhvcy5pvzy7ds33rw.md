---
type: is
id: is-01m4xjh0wnhvcy5pvzy7ds33rw
title: "#514 review B7: the stamp tool's id pattern T-\\d{3} failed open on four-digit or quoted ids"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
created_at: 2026-10-14T16:04:33.301Z
updated_at: 2026-10-14T16:05:25.393Z
closed_at: 2026-10-14T16:05:25.393Z
close_reason: "fixed in 662da8162: register_ids takes the ids from safe_load and raises when the - id: line scan, which accepts any bare or quoted id, does not find the same ids in order; test_the_ids_are_the_parsed_registers_and_a_line_the_scan_misses_fails"
resolution: null
duplicate_of: null
---
Review B of #514 (review 5520287797), finding B7: the stamp tool's id pattern T-\d{3} failed open on four-digit or quoted ids
