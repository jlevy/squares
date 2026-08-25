---
type: is
id: is-01m0w021rvnfpdzkgmzx0tbbr7
title: Remove exp-037 checker wrapper from forbidden legacy tools path
kind: bug
status: closed
priority: 2
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels: []
dependencies: []
parent_id: is-01m0vr7g27g67p699aepcdksxd
created_at: 2026-08-25T08:19:46.568Z
updated_at: 2026-08-25T08:20:51.413Z
closed_at: 2026-08-25T08:20:51.401Z
close_reason: "Completed: removed the forbidden tools wrapper, rebound exp-037 and its session to python -m cases.n5.tangent_inventory, reconciled the synopsis, README, defect log, and ledger, and passed direct record/replay, ten module-boundary tests, and the 15-step fast gate."
resolution: null
duplicate_of: null
---
The exp-037 implementation added a thin Python wrapper under explorations/packing/tools, which the module-boundary contract forbids. Remove it, bind the experiment and session to python -m cases.n5.tangent_inventory, reconcile generated and hand-maintained views, and verify the architecture and fast gates.
