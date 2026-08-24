---
type: is
id: is-01m0tt28c28cfmj5j651zg4mzp
title: Enforce and review the packing workflow documentation contract
kind: task
status: open
priority: 1
version: 1
spec_path: explorations/packing/tools/check_synopsis.py
labels:
  - packing
  - documentation
  - focus-process
  - workflow-entry-points
dependencies: []
parent_id: is-01m0r7tkdt35ged6b10gaf9wa0
created_at: 2026-08-24T21:15:47.457Z
updated_at: 2026-08-24T21:15:47.457Z
---
Add the smallest checks that prevent taxonomy and status drift: schema validation for workflow values and phase structure, reconciliation of the W1-W6 names across their canonical and summary surfaces, and a freshness rule for any latest-round statement retained in the synopsis. Run link checks, generated-view checks, Flowmark, focused packing checks, and the normal gate. Then run separate lint, claim, reasoning, and purpose audits under the common documentation guidelines and leave any judgment-bearing findings as beads. Acceptance: all checks pass, the source documents retain their required footer, the final review names residual risks, and think-m79h can close only when its original lane-handoff example and this workflow work are both complete.
