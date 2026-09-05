---
type: is
id: is-01m1qey47ncj6qjqvrqekhr5kz
title: "Interval route: a per-direction box budget and an atom cap, sized from measurement"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-05T00:19:16.341Z
updated_at: 2026-09-05T01:03:54.942Z
closed_at: 2026-09-05T01:03:54.942Z
close_reason: "Folded into think-nb9d's commit: BOX_BUDGET sized from the measured maximum with the margin written down, MAX_INTERVAL_ATOMS ported and read by the gate."
resolution: null
duplicate_of: null
---
PR 80 adds BOX_BUDGET = 100,000 boxes per direction (a search that reaches it returns undecided, or refuted if a sampled point already refutes) and MAX_INTERVAL_ATOMS = 4,096 (the boxes-by-atoms mask stays under 16 MiB). Both are refusal policies rather than arithmetic soundness, so they are not in the F7/F29 port. Decide them on their own: the review measured 31,103 boxes at the n = 17 top rung, so 100,000 is 3.2x headroom, and the stack's comment names 2,097 atoms as the largest retained certificate when it is 2,260. Size the budget from the net or from a measured maximum with the margin written down; port the atom cap with its arithmetic; add the budget-exhausted outcome and its regression.
