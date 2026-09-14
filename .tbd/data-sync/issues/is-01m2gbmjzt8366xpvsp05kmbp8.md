---
type: is
id: is-01m2gbmjzt8366xpvsp05kmbp8
title: "PR #167: publish exp-160 output atomically and refuse input/output alias"
kind: bug
status: closed
priority: 2
version: 4
labels: []
dependencies: []
parent_id: is-01m2gce39ed9awfhdpaq8ed3rt
created_at: 2026-09-14T16:22:38.821Z
updated_at: 2026-09-14T19:20:07.594Z
closed_at: 2026-09-14T19:20:07.594Z
close_reason: Fixed in ed68f644; 14 focused tests pass, Ruff/BasedPyright are clean, pre-push functional validation passes, and fresh hosted required CI is green on the exact head.
resolution: null
duplicate_of: null
---
In packing/devtools/analyze_bc303_h162_receipt.py:199-202, direct Path.write_text truncates durable experiment output in place; interruption can leave partial JSON, and the CLI permits --input and --output to resolve to the same file, destroying the admitted exp-158 receipt. Use atomic same-directory publication and explicitly reject input/output alias; decide and enforce overwrite policy.

## Notes

Fixed in ed68f644; focused tests and static checks pass. Awaiting clean checkpoint and hosted CI before closure.
