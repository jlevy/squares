---
type: is
id: is-01m2qk7y4msb762704fz3hyytv
title: Retain or regenerate the sites-1 rows-complete checkpoint at 153/40
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - research
dependencies: []
parent_id: is-01m2exznj4k1zyz1rczby8ch2k
created_at: 2026-09-17T11:50:13.907Z
updated_at: 2026-09-17T11:50:13.907Z
---
The rows-complete covering LP at 153/40 (15,021 rows over 17,389 sites, the A6 sites-1 checkpoint) exists only as unretained scratch on another host, which blocked the decisive M1 test on 2026-09-17 (think-4woh). Regenerate it with the repository's own producer, retain it under a deterministic, source-bound receipt (size permitting, or a regeneration command plus digest), and record the command, cost and location, so relational-atom columns can be tested against the real rows-complete LP.
