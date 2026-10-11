---
type: is
id: is-01m169k75pahfaa159xa14jpz3
title: Derive the one stationarity condition n=5 still needs
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-08-29T08:18:50.677Z
updated_at: 2026-10-06T08:41:46.139Z
closed_at: 2026-10-06T08:41:46.138Z
close_reason: "Done: agenda-006 BC-069 (bead think-864y) is state complete; session-044 records n = 5 rank 15 -> 16 of 16 with the residual unmoved at 1.110e-16, in sqpack/promote/system.py and probe_contact_system --case gobel5."
resolution: null
duplicate_of: null
---
After BC-059's edge-edge repair, Gobel's n=5 is the only retained size with a genuine rank shortfall: 15 of 16, one condition short, with side_leak 1.0e-16 so the first-order condition already holds there. It has no edge-edge contact at all, so the repair does not touch it. That makes it the cleanest case to derive a real closure condition on — and the only one that still needs one. The condition is the Lagrange or Fritz-John statement that no admissible motion decreases the side, in determinant form. close() currently reports that one is needed and refuses to invent it. Exit: a condition in a form a solver accepts, whose addition takes the n=5 rank to 16/16 with the residual unmoved at the retained pose; or a typed statement of which formulation the contact graph resists.
