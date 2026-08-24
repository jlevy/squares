---
type: is
id: is-01m0rrwmf90rynrj697ge7nk1k
title: quench_bracket's budget is wall-clock, so results depend on machine load
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T02:16:45.800Z
updated_at: 2026-08-24T02:16:45.800Z
---
quench_bracket and _free_sweep take time_budget in seconds and stop on a wall-clock deadline. Anything that changes how fast the machine runs -- a parallel pool, a busy laptop, a slower CI box, a colder cache -- changes how much work the quench does, and therefore whether it certifies convergence.

D-036 is already the defect where an incomplete free sweep returned as if every angle had been checked. A wall-clock budget is the same hazard one level up: it makes 'converged' a property of the machine as well as the mathematics.

Currently benign: a quench is ~2.5s against a 90s budget, ~35x of margin, and the parallel --deep regeneration still reproduces the committed map byte-for-byte. It stops being benign the moment the budget is tightened, the problem size grows, or a census runs many-wide on a shared box -- all three of which the planned campaign does.

Suggested work: express the budget as work (LP solves, or bracket iterations) rather than seconds, and keep a wall-clock deadline only as an outer backstop that is recorded when it fires. A run whose numbers depend on how loaded the machine was is not reproducible from its artifact, which is the property the engine's (seed, chain) keying exists to guarantee.
