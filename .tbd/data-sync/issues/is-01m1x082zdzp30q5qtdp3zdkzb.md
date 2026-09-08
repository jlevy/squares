---
type: is
id: is-01m1x082zdzp30q5qtdp3zdkzb
title: "Decide the two strongest external n = 17 certificates here: anabologyco 4.5705 under Boost and Lean, Mira 4.468292 by the green17 interval audit"
kind: task
status: open
priority: 2
version: 1
labels:
  - n17
  - controls
dependencies: []
parent_id: is-01m1wwrjmnkeq6xgkwcz4ha3zs
created_at: 2026-09-07T03:58:00.685Z
updated_at: 2026-09-07T03:58:00.685Z
---
Follow-up to the 2026-09-07 GitHub-certificates review (think-7104). (1) anabologyco-maker's s(17) >= 9141/2000 = 4.5705 is source-backed only: its Sturm partition, endpoint audits and 148,937-cell coverage audit need g++ with Boost.Multiprecision and OpenMP (verify_core.sh, scripts/run_coverage_ranges.sh; about 400 s of checker time per the source's own summary), and its Lean layer needs Lean 4.33 (lake build FullTheorem, 8.5 h single-threaded per the source). Run them in an environment that has both and record an evidence entry at assurance verified if they pass. The repository's shrink-and-net verifier cannot decide this certificate (atoms on the wall-distance-one lines are dropped by the shrink), so a decision needs either the source's chain or a first-party exact-orientation verifier. (2) Mira's 16-point certificate at 4468292/1000000 and Fort's at 4456575/1000000 were replayed here only by the sources' own Python checkers; cases/green17/interval_audit.py takes an arbitrary side and point set (--side and the points argument) and would be a genuinely independent decision of the same claim (closed containment there versus strict interior in the sources; state the relation). Archive: packing/resources/web/n17-github-certificates-2026/.
