---
type: is
id: is-01m474bg92xth3mw1fx75ad9eg
title: Return pull-request wall ceilings to enforcement once the gate measures run-to-run spread
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-10-05T22:53:34.881Z
updated_at: 2026-10-05T22:53:34.881Z
---
Owner decision 2026-10-05 (session 182: 'make all additional necessary fixes, if there are any walltime budget decisions'): on hosted pull-request runs the tier ceilings (rule 1) and the 12 s per-test call-wall rule are advisory, reported and not failed, up to a hang detector: a tier wall above 2x its ceiling, or a test call above 45 s, still fails. Evidence: CI stabilization evaluation 2026-10-05 -- 28 of 36 red stack pushes were budget-only with every test green; the +9% raise (3d89c6fa5) was breached again at 171.2 s vs 168 s on #356 (run 37380844925); hosted runner variance 1.6-1.8x (think-g4n9), 2.3x on identical code (think-53a2). Ceilings stay enforced on main, scheduled and deep runs. Close when the ceiling is judged against a median over hosted samples or a runner-normalised wall (see think-be1s) and enforcement returns.
