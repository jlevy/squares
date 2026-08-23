---
type: is
id: is-01m0pd7heak20pe5sv132jmftx
title: quench_bracket output depends on class_tol, so basin identity would too
kind: bug
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0pdh5bj67ca8vk7ct53g5qt
created_at: 2026-08-23T04:14:31.370Z
updated_at: 2026-08-23T04:20:07.728Z
---
quench_bracket merges angles within class_tol (default 1e-2 rad = 0.57deg) and forces them equal, so what it returns is the optimum of a CONSTRAINED problem, not a true local optimum. Two consequences: a packing whose optimum needs two angles closer than the tolerance is unreachable; and the cartography plan defines a basin as where the quench lands, so basin identity inherits a tuning parameter and the atlas would be partly an artifact of it. Must be settled before the atlas is built. Fix direction: unconstrained polish after class bracketing to confirm a true local optimum, plus a class_tol sensitivity sweep.
