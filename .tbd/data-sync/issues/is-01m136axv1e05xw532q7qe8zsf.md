---
type: is
id: is-01m136axv1e05xw532q7qe8zsf
title: quench_bracket drops LP work from lp_solves when a free sweep aborts
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-08-28T03:24:09.938Z
updated_at: 2026-08-28T03:24:09.938Z
---
D-349. _free_sweep accumulates its own LP count and returns it; quench_bracket adds it only on the normal return. On _OutOfTimeError or _FixedCellUnsettledError the partial count is lost, so budget-cut runs understate lp_solves. Found via the Motion Lab timeline, which retains one event per solve. Fixing this changes reported engine numbers, so it needs its own research round rather than riding along with a tooling PR. See explorations/packing/src/sqpack/research/quench.py _free_sweep and its callers.
