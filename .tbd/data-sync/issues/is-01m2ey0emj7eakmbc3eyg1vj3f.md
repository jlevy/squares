---
type: is
id: is-01m2ey0emj7eakmbc3eyg1vj3f
title: Reconcile SYNOPSIS and the active plan after the stack lands and the strategy reset
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - docs
dependencies: []
parent_id: is-01m2etr75jfh3t3ry7kj1ccqrb
created_at: 2026-09-14T03:05:13.091Z
updated_at: 2026-09-14T03:43:16.183Z
---
After #156, #161–#166 and #157 land, the reader-facing 'selected next entry' lines are stale: #157 names think-8c9e (weighted stage 3, now paused) and the chain names BC329 admission (paused). Run a W8 documentation pass over README, SYNOPSIS and the active daytime plan so they state the paused lanes, the unchanged T-026 bound, and the strategy reset (think-gtax) as the next entry. #167 (H-162 preregistration, draft) stays open on main as a paused BC303 layer.

## Notes

2026-09-14 review nit: on the landing tree SYNOPSIS.md:150 says 'No hypothesis is running' while H-160 is running at SYNOPSIS.md:3649 and in the ledger; check_synopsis does not test that sentence. Fix in this pass.
