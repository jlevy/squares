---
type: is
id: is-01m2gbmjzt8366xpvsp05kmbp8
title: "PR #167: publish exp-160 output atomically and refuse input/output alias"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2gbcm4afdzz4r8x790g898q
created_at: 2026-09-14T16:22:38.821Z
updated_at: 2026-09-14T16:22:38.821Z
---
In packing/devtools/analyze_bc303_h162_receipt.py:199-202, direct Path.write_text truncates durable experiment output in place; interruption can leave partial JSON, and the CLI permits --input and --output to resolve to the same file, destroying the admitted exp-158 receipt. Use atomic same-directory publication and explicitly reject input/output alias; decide and enforce overwrite policy.
