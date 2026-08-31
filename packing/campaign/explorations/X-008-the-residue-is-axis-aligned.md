---
title: X-008 — the shapes the grammar cannot express are the ones that are not tilted
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-008
  title: The shapes the grammar cannot express are the ones that are not tilted
  date: '2026-08-30'
  author: Claude (agent), under BC-024 in agenda-002, run as phase 9 of session-045
  campaign: packing.squares
  brief: >-
    BC-024 asked which chunk shapes, sizes, tilted-chunk counts and wall seatings recur
    across the imported n <= 100 corpus, and what the non-expressible residue has in
    common. Stratifying the retained component census by the source each record's geometry
    came from, and adding wall seating computed from the witness corners, answers it. The
    residue is 109 components and not one of them is tilted -- every other-polyomino in the
    corpus has angle exactly zero, so every tilted component the repository holds is a
    singleton, bar, L or rectangle and already expressible. The residue splits by seating
    into exactly two populations with nothing between them: 44 whole-record grid subsets
    touching all four walls, and 65 corner-seated blocks touching exactly two. Descriptive
    throughout; no H-044 verdict is emitted and none is available.
  sources:
  - packing/campaign/series/series-000-smoke-and-calibration/results/bc-024-chunk-taxonomy.json
  - packing/atlas/known-best/chunk-components.json
  - packing/atlas/known-best/manifest.json
  - packing/atlas/known-best/contact-assembly-grammar.yaml
  - packing/campaign/explorations/X-007-the-n5-optimum-flexes-once-and-that-once-is-shut.md
  proposes: []
---
# X-008 — The Shapes the Grammar Cannot Express Are the Ones That Are Not Tilted

**Date:** 2026-08-30

**Status:** Tier-S descriptive slice under `BC-024`, run as phase 9 of `session-045`. A
pass over imported geometry with no search and no adjudication.

**Owns:** The argument.
`devtools/census_chunk_taxonomy.py` owns the taxonomy, `tests/test_chunk_taxonomy.py`
pins it, and the gate step `chunk taxonomy agrees with the corpus` replays it.

## What Stratifying Buys

The broad component census already answers *what components are there*. It does not
answer *whose geometry they came from*, and the corpus turns out not to be one
population at all.

| Stratum | Records | Components | Tilted | Shapes |
| --- | ---: | ---: | ---: | --- |
| `exact-grid` | 64 | 64 | 0 | 44 other-polyomino, 17 rectangle, 1 each bar/L/singleton |
| `kingbird-derived-facts` | 34 | 387 | 237 | 197 singleton, 82 bar, 65 other-polyomino, 31 L, 12 rectangle |
| `unitsquare-rendering` | 2 | 137 | 58 | 137 singleton |

Two thirds of the corpus is a row-major subset of an integer grid with no tilt anywhere
in it.
It contributes exactly one component per record — a grid subset is connected — and
that component is a rectangle only when `n` factors conveniently.
For the other 44 it is the `other-polyomino` shape the grammar does not express.

**So the largest single part of the residue is trivial geometry.** That is worth saying
plainly because the shape of the word “residue” invites the opposite reading: something
exotic left over after the easy cases are handled.
Here it is `n = 7`, an integer grid with two squares missing.

The third stratum is `n = 68` and `n = 69`, whose witness geometry the
translation-escape screen also excludes.
Every one of their 137 squares is a singleton, and 58 of those singletons are tilted —
so this stratum is not unstructured *because* it is a grid, it is unstructured because
nothing in it lines up with anything else.

## The Residue Is Axis-Aligned, Entirely

This is the finding, and it is the reverse of what the categories suggest.

**Every `other-polyomino` component in the corpus has angle exactly `0`.** One distinct
angle value across all 109 of them.
So every tilted component the repository holds — 295 of them, across 36 records — is a
singleton, a bar, an L or a rectangle, and all four of those the grammar expresses.

The consequence for the partition-instrument design is direct.
Extending the grammar to cover what it currently misses is a question about
**axis-aligned polyominoes**. It is not a question about tilted assemblies, because the
tilted structure in this corpus is already covered.

## Wall Seating Separates the Residue Cleanly

Wall seating is the one axis the census could not supply.
Its `lattice_coordinates` are relative to a component, so a bar in a corner and the same
bar in the middle of the container are indistinguishable there.
Computing it from the retained witness corners gives the residue a structure with
nothing in between:

| Walls touched | Residue components | Which |
| ---: | ---: | --- |
| 4 | 44 | every `exact-grid` record; each is the whole record |
| 2 | 65 | every `kingbird-derived-facts` residue component |

No residue component touches one wall, or three, or none.
Both halves have an explanation that is obvious once seen and was not obvious in
advance: a grid subset spans the container, so it meets all four walls; and a block of
axis-aligned squares inside an otherwise tilted packing sits in a corner, so it meets
two.

The seating computation is checked against the one packing whose contacts are known
exactly. [`X-007`](X-007-the-n5-optimum-flexes-once-and-that-once-is-shut.md) enumerates
`n = 5` in `Q(sqrt 2)`: sixteen corner-on-wall contacts across four corner squares, two
walls each, and a middle square touching no wall.
The seating here, computed from decimal witness corners at a `1e-9` tolerance, reports
exactly that — `[0, 2, 2, 2, 2]`. Had it disagreed, the taxonomy would have been
measuring the witnesses’ precision rather than the packings’ geometry.

## What This Is Not

**No `H-044` verdict is emitted and none is available.** The census’s own `known_gap` is
explicit: a component the current detector did not express is not a refutation of chunk
expressibility until the minimal-partition solver exists.
A table of counts reads like a conclusion, so the record carries that sentence in its
own `subject` block and a test asserts it is there.

**The tolerance is deliberate and is not a feasibility claim.** Wall seating uses
`1e-9`. Thirty-six of the hundred records carry numerically-checked decimal witnesses,
so an exact-sign test would answer “touches no wall” for every one of them and the
taxonomy would be a description of the corpus’s precision.
Nothing here bears on feasibility, where the standard is exactness and stays exactness.

**One band, on purpose.** The exact-adjacency band is read and the near band is not.
They differ by nine components across the whole corpus, and a claim that changed with
the choice would be a claim about the tolerance rather than about the packings.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
