---
type: is
id: is-01m29n9q19bfnmxmyknc927dt1
title: The blind run has no seed, so there is one trial per n
kind: bug
status: open
priority: 0
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies: []
parent_id: is-01m29kqwefbzzpt7bngm68pq6p
created_at: 2026-09-12T01:56:47.260Z
updated_at: 2026-09-12T01:56:47.260Z
---
**Found before any sweeping, and it reshapes the programme.** The blind run has no seed. Every source of randomness in the page is seeded from `n` alone:

- The cached simulator's shake: `seed = Math.imul(p.n, 2654435761) + 0x9e3779b9` (workbench.js, the body-table builder).
- The live optimiser's shake: `seededRandom(N + INITIALS.indexOf(kind) * 7919)` -- n and the start kind.
- The random start's poses: `seededRandom(N)`.

So for a given n and parameter set there is exactly ONE blind trial, and it is the same trial every time. That is a deliberate and good property for an animation -- the same pair jiggles the same way in every build, which is what makes a capture reproducible -- and it makes a success RATE impossible: a rate over one sample is either 0 or 1.

H7 is therefore answered in a stronger form than it was asked: replay is deterministic because there is nothing to vary. And the answer changes what has to be built first.

**What this bead is.** Make the seed an input: `setSeed(k)` on the API, mixed into all three generators, defaulting to whatever reproduces today's runs exactly so no existing capture, checker or recorded measurement moves. Then a trial is (n, parameters, seed) and a rate is a rate.

Two things to be careful of:
- **The default must be bit-identical to today.** `check_revision7` compares free-run misses against recorded values and `check_workbench` keys trajectories by their parameters; a changed default breaks both, and rightly.
- **The seed belongs in the trajectory cache key**, or two seeds will share one cached run -- the same class of bug as the correction ratio, which took the gate from 90 seconds to 17 minutes when it was keyed wrongly.

Blocks think-k2fr: the harness cannot report a success rate until there is more than one trial to succeed at.
