---
type: is
id: is-01m2mh0gs7dt8125xkejfm4r7n
title: "PR #181 final type gate: narrow node stderr before diagnostic assertions"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2m6xx00sabcq5zqkrneavd0
created_at: 2026-09-16T07:13:30.406Z
updated_at: 2026-09-16T07:14:16.457Z
closed_at: 2026-09-16T07:14:16.455Z
close_reason: "Completed at PR #181 head f0a2c7b3: stderr is narrowed to str before exact TypeScript diagnostic containment checks; targeted BasedPyright is 0/0/0 and 28 browser-floor contract tests pass."
resolution: null
duplicate_of: null
---
The final full edit tier at head 529a9512 found BasedPyright errors in test_browser_floor_contract.py: nodejs_wheel's completed stderr remains str | bytes even with text=True, so two string containment assertions are not type-safe. Narrow stderr explicitly, retain the exact negative diagnostic assertions, and re-run the type floor.
