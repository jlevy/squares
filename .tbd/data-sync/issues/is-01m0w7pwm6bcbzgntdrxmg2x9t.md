---
type: is
id: is-01m0w7pwm6bcbzgntdrxmg2x9t
title: Basin-entry summary omitted emitted pair-test work
kind: bug
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
delegate: codex-root
labels: []
dependencies: []
parent_id: is-01m0pqg2mnmsmv8250d0rw25kb
created_at: 2026-08-25T10:33:29.478Z
updated_at: 2026-08-25T10:33:29.478Z
---
The first sqsearch pair-test meter draft emitted pair_tests on each basin-entry trial but did not aggregate the trials into the basin-entry summary. A summary-only consumer would undercount all producer work as unknown/absent even though the trial rows carried it. Add checked summary aggregation and a regression check before integration.
