---
type: is
id: is-01m23xrtdbtja91gcsns0yc1g8
title: Decide whether lane A5's nu_S program becomes a devtool
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-09-09T20:29:24.265Z
updated_at: 2026-09-09T20:29:24.265Z
---
The fixed-support maximisation under the atom classes — lane A5's `nu_S` program — is
retained as a scratch receipt at
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/lane-a5-cap-lp.py.txt`.
It is the one retained script that looks like a tool rather than a probe, and this bead
is the decision on whether to promote it to `packing/devtools/`.

**What it is.** It extends the pattern of `packing/devtools/polish_ceiling_family.py` —
working-set polish with exact rows, exact rational rebuild, exact dual bound — from the
point program to the threshold program, by imposing two complete row families on the same
fixed-support maximisation: the depth rows (one per distinct membership set of the
arrangement) and the budget-one rank-one atom rows (one per non-Helly maximal clique with
exact `tau*`). It imports `placement_orbits` from the tracked tool and calls
`devtools.plateau_reader` for the arrangement, the intersection graph and the piercing
numbers, so the geometry is the repository's throughout. It produced the exact results
`nu_S(153/40) = nu_S(383/100) = 32/3`, their no-atom controls at exactly `11`, and the
priced duals that F7 reads.

**Why it was not promoted with the retention.** Promotion needs its own tests and review,
which the retention commit deliberately did not do. Specifically:

- No tests. The tracked surface runs at zero Ruff and BasedPyright findings and the
  devtools have tests; this file has neither, and its exact primal rebuild has a known
  failure mode already recorded in the lane document (§9: the first version accepted the
  zero vector, because it checked feasibility and not the objective).
- It hard-codes scratch paths (`RS`, `OUT`) and reads its families from a scratch run
  directory. A promoted tool takes paths as arguments.
- The rationalisation step is a denominator sweep that can return a valid but weak bound
  rather than the optimum; the lane document reports two loop rounds where it did. A tool
  should say which case it is in, and the receipt only reports the number.

**What done looks like.** Either a `packing/devtools/` module with a CLI, tests in
`packing/tests/`, no hard-coded paths, and the rationalisation outcome reported
explicitly — reproducing `32/3` at both sides and `11` on the no-atom controls as its
golden case — or a recorded decision not to promote, with the reason, leaving the receipt
as the record.

Context: `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/lane-a5-the-fixed-support-maximum-under-the-atom-classes.md`
(§8 Method, §9 Timings, and the Files section).
