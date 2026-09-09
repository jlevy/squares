---
title: X-025 — hunting by hand, and the threads the move-set round opened
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-025
  title: Hunting by Hand, and the Threads the Move-Set Round Opened
  date: '2026-09-08'
  author: Claude Opus 5, for the repository owner
  campaign: packing.squares
  brief: >-
    Frame the research ideas this branch turned up before any of them is broken into
    hypotheses, because the research goals are not yet clarified. Start from the
    through-line: a question about making an animation look natural became a question
    about why squares settle where they do, and then a measured explanation of a
    years-old failure in the search engine. Give the most room to the direction the
    owner named, a workbench for hunting better configurations by hand with manual
    perturbation in chosen settings, and develop it as a research idea rather than as a
    user interface. Frame the relaxed intermediate, the tween model, directional
    pressure, off-grid seeding and replica exchange without committing to any of them.
    Carry an explicit catalogue of candidate hypotheses, sorted by whether they are
    ready to formalise, and say what the new material does to three standing but unbuilt
    ones. Nothing here is registered; no hypothesis is proposed and no experiment is
    launched.
  sources:
  - docs/project/research/research-2026-09-08-annealing-for-square-packing.md
  - packing/campaign/hypotheses/H-135-simultaneous-perturbation-move.md
  - packing/campaign/hypotheses/H-136-wall-pressure-dense-objective.md
  - packing/campaign/hypotheses/H-137-basin-hopping-over-the-lp-quench.md
  - packing/campaign/hypotheses/H-138-cooling-schedule-length.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-134-arm-calibration.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-135-round-1-perturbation.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-136-round-1-pressure.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-137-basin-hopping.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-138-round-1-schedule.md
  - packing/campaign/hypotheses/H-004-neighbor-transfer-seeding.md
  - packing/campaign/hypotheses/H-012-record-basins-are-rare.md
  - packing/campaign/hypotheses/H-013-delta-continuation.md
  - packing/campaign/hypotheses/H-018-basin-entry.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-005-basin-entry-n11.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-006-lp-quench-n5-n10-n11.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-011-h-020-n17.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-012-h-024-n29-angle-classes.md
  - packing/campaign/explorations/X-001-standing-review-and-search-philosophy.md
  - packing/campaign/explorations/X-009-where-a-new-packing-is-reachable.md
  - packing/campaign/ideas.md
  - packing/atlas/known-best/video/spikes/README.md
  - packing/atlas/known-best/video/spikes/v1-slideshow/NOTES.md
  - packing/atlas/known-best/video/spikes/v2-transitions/NOTES.md
  - packing/atlas/known-best/translation-escape-screen.json
  - packing/src/sqpack/verify.py
  - packing/src/sqpack/research/quench.py
  - packing/src/sqpack/motion_lab/contracts.py
  - packing/frontier/README.md
  - packing/frontier/square-packing-case.schema.yaml
  - packing/devtools/gap_ranking.py
  - packing/devtools/measure_objective_sparsity.py
  - docs/project/specs/active/plan-2026-08-25-generalized-motion-lab.md
  - docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
---
# X-025 — Hunting by Hand, and the Threads the Move-Set Round Opened

**Put a person back in the loop, and build the instrument that would make a hand-made
attempt mean something.** The provenance census is the argument: of the 36 cases at
`n ≤ 100` whose best known packing beats the trivial grid, 21 are human geometry and 10
are simulated annealing, so for exactly the cases that are still open the historically
dominant method is a person with a pencil.
This document does not propose that as a plan.
It says why the direction is interesting, what would have to exist before an attempt
could be judged, and what else the last two days opened that is worth thinking about
before anything is registered.

## Why This Is an Exploration and Not a Plan

The owner’s instruction was explicit twice over: cover the ideas before they are broken
down into hypotheses, because the research goals are not clarified; and keep it free and
open-ended, with lists of the hypotheses that look relevant.

So two things are true of what follows.
It is allowed to hold a direction as interesting for reasons that are not yet
measurable, to keep two incompatible readings of the same evidence side by side, and to
record a hunch as a hunch.
And it carries an explicit catalogue of candidate hypotheses anyway, because a framing
document that leaves no trace of what could be tested is a mood.
Those candidates are candidates: no `H-` numbers, no schema envelope, nothing written to
the campaign register.
Where the reasoning is speculation it says so in the sentence rather than in a caveats
section at the end.

### On the number

The next free identifier above the highest either the working tree or `origin/main`
holds is `X-023`. This document takes `X-025` instead, leaving two.
The `n = 11` proof line is producing explorations in a run (`X-017`, `X-018`, `X-019`,
`X-021`, `X-022`, the last of those on an unmerged branch) and `X-020` is already a
burned name from a rename.
This document belongs to a different lane, and taking the next number would sit directly
in that line’s path.
Identifier collisions have bitten this branch twice today, once for four hypotheses and
once for five experiments, and the gap costs nothing.

## The Through-Line

It is worth stating plainly, because it is unusual and because it is easy to overclaim.

A question about making an animation look natural became a question about why squares
settle where they do, and then a measured explanation of a years-old failure in the
search engine.

The animation is the atlas video: 324 known-best packings, one per `n`, and a transition
between each consecutive pair.
Building the transitions raised the question of whether the motion could be physical
rather than interpolated, and the physics spike answered it in the negative in a way
nobody had asked for.
Aimed straight at a known answer with the final snap disabled, the settle still rests
one to 1.7 units away per square and 0.1 to 1.1 per cent wide.
Run blind, with no target poses at all, every genuinely packed case loses, by up to 6.8
per cent at `307 → 308`. Then the annealing dial: raising it from level 0 to level 10
more than halves the worst angle error twice over, `42.9°` to `19.9°` at `100 → 101` and
`17.3°` to `7.6°` at `110 → 111`, while the container side stays flat to within a few
tenths of a per cent
([the spike notes](../../atlas/known-best/video/spikes/v2-transitions/NOTES.md),
revision 7).

Shaking harder fixes orientations and does nothing to the side.
That is a statement about the objective, not about the animation, and it is the same
defect the
[annealing survey](../../../docs/project/research/research-2026-09-08-annealing-for-square-packing.md)
derives analytically from `required_side(c) = max(hix - lox, hiy - loy)`: only the
squares attaining the extremes of the binding span can reduce it, so a single-square
move is a no-op on the objective for almost every square.

The search campaign then measured it directly, and the measurement is sharper than the
argument. From `devtools/measure_objective_sparsity.py`, 8,000 proposals per kind per
cell at scales `0.01`, `0.05` and `0.2`, recorded in
[exp-134](../series/series-000-smoke-and-calibration/experiments/exp-134-arm-calibration.md):

| cell | single-square proposals that lower the side | that change it at all | collective proposals that lower it |
| ---: | ---: | ---: | ---: |
| 5 | `0.0646` | `0.4716` | `0.054`–`0.071` |
| 10 | `0.0000` | `0.3488` | `0.0041`–`0.0068` |
| 11 | `0.0000` | `0.3038` | `0.0034`–`0.0051` |
| 17 | `0.0000` | `0.2801` | `0.0006`–`0.0009` |
| 19 | `0.0000` | `0.2465` | `0.0000`–`0.0005` |
| 26, 27, 29, 37, 50, 52 | `0.0000` | `0.24` down to `0.17` | `0.0000` |

At the trivial grid, no single-square proposal lowers the required side at all, for
every tested cell but `n = 5`, at every scale tried.
The reason is not that the moves are too small.
It is that the grid’s binding span is attained by a whole row or column of `m` squares
at once, so no one square is the unique extremum whose retreat could shrink it.
A quarter to a third of proposals still change the objective, and outside `n = 5` every
one of those raises it.

The consequence, from
[exp-135](../series/series-000-smoke-and-calibration/experiments/exp-135-round-1-perturbation.md):
adding a whole-configuration move takes `n = 17` from exactly `5.0` on every control
seed to a best of `4.682227`, which is `+6.70e-03` from Bidwell, a gap forty-eight times
smaller than the control’s. It takes `n = 11` from `3.922761` to `3.886755` and `n = 26`
from exactly `6.0` to `5.746574`. Above `n = 26` it stops, and it stops abruptly: at
`n = 29, 37, 50, 52` every seed of both arms returns the grid bit for bit.

**One correction to how this has been told.** The `n = 17` figure often quoted as
“within `0.002` of Bidwell cold” is `4.677676`, `+2.15e-03`, and it is not the
collective move alone: it is the both-factors arm of
[exp-138](../series/series-000-smoke-and-calibration/experiments/exp-138-round-1-schedule.md),
collective move plus a tenfold longer anneal, and that arm’s delivered budget at
`n = 17` overshot the control’s by `×1.31`. The collective move on its own reaches
`+6.70e-03`. Both are cold and both are against a control sitting at exactly `5.0`,
which is the point either way; the smaller number just is not the move’s.

### What the through-line does and does not license

It licenses saying that a visualisation built for exposition produced a real diagnostic,
and that the diagnostic was independently confirmed by an instrumented measurement and
by a literature survey that found the record-holders saying the same thing in their own
words. That is a good day.

It does not license saying that animations are a research method.
One spike found one thing, and it found it because the objective’s defect is unusually
visible: an error that lives in orientation while the number stays flat is exactly the
kind of error a picture shows and a scalar hides.
Nothing here predicts that the next animation finds anything.
It also does not license treating the physics simulator’s failures as measurements of
the problem: the spike’s own notes say plainly that nothing checks the blind run against
a real compaction, so “6.8 per cent worse” is against that simulator with those
constants.

## The Direction With the Most Room: A Workbench for Hunting by Hand

The owner named this one, and it deserves the most space.
A workbench for hunting better configurations by hand, with manual perturbation, in
chosen settings. Treated as a research idea rather than as a user interface.

### The provenance argument, verified here

Read first-hand from `packing/frontier/n-001.md` through `n-100.md`, comparing
`packing.reported_upper_bound.value` against `ceil(sqrt(n))` and reading
`construction_method` off the same field:

| how the best-known non-grid packing at `n ≤ 100` was found | count | `n` |
| --- | ---: | --- |
| `hand-construction` | 15 | 5, 11, 17, 18, 19, 37, 40, 54, 65, 66, 70, 82, 85, 88, 89 |
| `simulated-annealing` | 10 | 28, 29, 39, 41, 50, 51, 53, 55, 71, 87 |
| `diagonal-strip` | 6 | 10, 27, 38, 52, 67, 84 |
| `extension` | 3 | 26, 83, 86 |
| `unknown` | 2 | 68, 69 |
| **total** | **36** |  |

**Twenty-one is `15 + 6`, and the two should not be silently folded.** The schema keeps
`hand-construction` and `diagonal-strip` apart, and
[`search-strategies.yaml`](../../frontier/search-strategies.yaml) lists them as separate
constructive strategies.
A diagonal strip is a closed-form family, not a bespoke arrangement.
“Twenty-one found by hand” is loose; “twenty-one are human geometry rather than search”
is what the records support, and the annealing survey’s own table says exactly that.
Two further cautions on the same count.
The two `unknown` cases have a recorded finder and an unrecorded method, so the search
credit is a lower bound.
And reading `construction_method != trivial-grid` instead of comparing values gives 48,
not 36, because twelve cases carry a non-grid method label while their best known side
equals the grid (`n = 1, 4, 6, 9, 13, 22, 23, 24, 33, 34, 35, 46`); `36 / 15 / 10` and
`48 / 25 / 10` are the two coherent censuses and a mixture of them is neither.

With that said, the argument survives intact.
For the cases that are actually open, a human construction is the modal provenance, and
the machine’s ten are recent and concentrated: nine of the ten are dated 2024 to 2026,
all sit between `n = 28` and `n = 87`, and they come from a closed GPU engine whose
author records that without special modifications it almost always gets stuck just above
the trivial size.
The catalogue’s own provenance comments record that engine being seeded
from a cherry-picked state, from a neighbouring record with squares removed and
straightened, from an analytically constructed state, and at `n = 103` from manually
moving squares in one corner of the picture and feeding the result back in.

**The record-holders are already doing this, without an instrument for it.** The
`n = 103` provenance is a person moving squares in one corner of a picture and feeding
the result back into a search.
That is an observation about practice, not a measurement, and it is the strongest
non-numerical part of the argument.

### What a person contributes that the annealer cannot

Three candidates. Each is stated with an honest note on whether it can be made sharp,
because two of the three currently cannot.

**Recognising symmetry and family structure.** The evidence that this is worth something
is strong and indirect.
[exp-006](../series/series-000-smoke-and-calibration/experiments/exp-006-lp-quench-n5-n10-n11.md)
reached the analytic `n = 11` optimum in 70 LP solves by constraining eleven angles to
two classes and golden-sectioning the shared tilt, against 1,024 for free descent.
The `n = 55` record closes its exact system in seven unknowns for 55 squares.
[exp-012](../series/series-000-smoke-and-calibration/experiments/exp-012-h-024-n29-angle-classes.md)
measured exactly six angle classes at `n = 29` at tolerance `1e-80`. But the same survey
records hard symmetry-breaking measuring strictly worse on 539 instances against better
on 2, and this problem supplies its own counterexamples, since `n = 17` needs three
angles and `n = 29` at least six.
So the human contribution is not the restriction.
It is *choosing which restriction to try*, and making that testable needs a null of
restrictions chosen at random from the same family, which nobody has built.

**Seeing that a configuration is the wrong shape rather than a worse number.** This is
the one that feels most true and is hardest to measure.
The engine’s entire state, as far as its decisions are concerned, is a scalar.
A person looking at the `n = 26` result at `5.823450` against a record of `5.621320` can
see whether the tilted band is in the wrong place or merely loose; nothing in this
repository reports that distinction.
Speculating, and flagged as such: a shape distance built from the angle-class census and
the contact graph might track the remaining gap better than the gap tracks itself across
restarts, and that correlation becomes measurable the moment an archive of refined
optima exists. Until then this is an intuition with no instrument.

**Choosing which basin to enter rather than polishing the one you are in.** This one is
already half measured, and the measurement is in the campaign’s own words: exp-006’s
verdict on the LP quench is that it is a polisher, not a rescue, because it optimises
whichever basin it is handed.
Basin choice is the whole of the problem the engine cannot do, and its only mechanism
for it is a random proposal.
A person choosing where to start is choosing a basin, directly and deliberately.

**And what a person contributes nothing to.** The number.
Given the arrangement, the fixed-angle LP reproduces Trump’s side to `4.4e-16`. Any
contribution a hand makes is entirely upstream of the arithmetic, which is a useful
constraint on what the workbench should be for: it is a tool for choosing arrangements,
not for improving values.

### What the instrument has to provide before an attempt means anything

Four requirements, in the order that matters.

**1. Exact feasibility on demand, and honesty about the difference.**
[`verify_packing`](../../src/sqpack/verify.py) with `exact_sign` over a number field is
a proof.
With `float_sign` it is not, and the docstring says why it cannot be made one by
raising precision: a valid tight packing has pairs whose separation is exactly zero, so
any tolerance large enough to accept those contacts also accepts overlaps smaller than
the tolerance, and a tolerance of zero rejects the valid packing outright.
A workbench’s live feedback is necessarily a float screen.
It must say so on its own face, and exact verification must be a separate deliberate
act, not a background reassurance.

**2. A polish step, so a rough placement is judged at its own local optimum.** Without
it the workbench measures the user’s mouse.
[`quench_bracket`](../../src/sqpack/research/quench.py) is the polisher that fits, and
it fits for a measured reason: it brackets rather than descends over angle classes by
golden section, because the objective has a corner at the optimum, with one-sided slopes
`0.175` and `0.384` measured in exp-006 and both Powell and Nelder-Mead doing worse than
plain descent there.
It converges from cold uniform random starts on 12 of 12 at `n = 5` to the proved
`2.707106781187`, and polishes annealer output at `n = 10` to a median gap of `8.9e-16`.
It also has two known defects that an interactive tool would feel immediately:
[exp-137](../series/series-000-smoke-and-calibration/experiments/exp-137-basin-hopping.md)
found `time_budget=4.0` producing calls of up to about 30 seconds, and LP output
penetrating by about `1e-16` and needing a monotone centroid-scaling repair before
emission. Both are prerequisites, not details.

**3. A record of attempts, including the failures.** This is the requirement that
separates a research instrument from an interesting afternoon, and it is the one most
likely to be skipped.
What it has to store: the starting configuration, the sequence of edits, the polished
result, the verification status, and who made it.
Ellsworth’s published run statistics are the model to copy, and the unit they use is the
right one: a refined local optimum, with the currency being basins per record rather
than moves per second.

**4. A path from candidate to real verification, not a screen.** The repository already
has the promotion pipeline and the interval certification lane.
The workbench’s output enters that pipeline; it does not write to
[`packing/frontier/`](../../frontier/README.md), and its green tick is a candidate, not
a record.

**Most of this is already half built, in two places that share a name.**
`sqpack/motion_lab` is a shared shell whose Phase 1 is a setup-only snap-and-quench
playground: set the count and the side, randomise a seeded start, drag or rotate
individual squares, snap touching squares into temporary chunks that move together, then
discard the snaps and send poses to the existing optimiser.
It has a typed `PoseFrame` whose `frame_kind` distinguishes an editor preview from an
exact path, a numerical state, a probe and an illustrative tween, and a `QuenchTrace/v1`
that types the solver’s phases.
Its Phase 2, which would preserve a contact or a rigid group *during* optimisation, is
[paused pending explicit constraint semantics](../../../docs/project/specs/active/plan-2026-08-25-generalized-motion-lab.md).
Separately, the video spike’s `workbench.html` has a gap bar that reads the record and
the proved lower bound off the frontier, computes the side the current arrangement would
need every frame, and turns green only when every square is on its target.
Two instruments, one name, and a research workbench wants the motion lab’s editor and
the video workbench’s gap bar.

One trap in that borrowing.
The video workbench’s “is the record” test needs a correspondence to the record, and its
blind mode makes the box the whole test precisely because no correspondence exists.
A hand-made hunt for something new has no correspondence by construction, so the box is
always the whole test, and the gap bar’s shaded open span between the two bounds is the
right display for it.

### Which cases to hunt, and why

- **`n = 17`, `19`, `26`.** These are where the engine now gets close and stalls:
  `4.677676` against a record of `4.675530` at 17, `4.958948` against `4.885618` at 19
  with the seed ranges still overlapping the control’s, and `5.710314` against
  `5.621320` at 26. A near miss is the configuration a person has most to work with,
  because the shape is visible and the remaining error is small enough to attribute to a
  part of it.
- **`n = 27` through `52`.** Above `n = 26` the collective move stops working, and the
  failure is not gradual.
  At `n = 29, 37, 50, 52` every seed of both arms returns the grid bit for bit; at
  `n = 27` the median is the grid for both arms, with one candidate seed reaching
  `5.878417`. There is no cell where the arm gets partway.
  These are the cells where the engine has no reliable route off the grid, so the only
  candidates are a seed transferred from a neighbour or a hand-made start.
- **The grid cases where a better packing plausibly exists.**
  [X-009](X-009-where-a-new-packing-is-reachable.md) re-indexes by `k = m² - n` and
  finds that nobody has ever beaten a grid at `k ≤ m - 2` anywhere to `n = 324`. Of the
  31 open grid cases at `n ≤ 100`, 18 sit in that never-beaten band and should not be
  hunted at all; the honest task there is a proof.
  The 13 at `k = m - 1` and `k = m` are the candidates, and `n = 90` is the one X-009
  treats as defensible after Cantrell falsified `s(m² - m) = m` at `m = 11` in February
  2025\.
- **Not the narrowest gaps.** The five smallest open gaps at `n ≤ 100` are `n = 12` at
  `0.0400`, `97` at `0.0557`, `78` at `0.0627`, `11` at `0.0671` and `61` at `0.0718`,
  and three of the five are unproved members of `s(m² - 3) = m`. Their gaps are small
  because Nagamochi’s bound is nearly tight there, and their conjectured optima are
  integers. Those are proof targets.
  `gap_ranking.py`’s own docstring makes the point that a narrow gap is not a difficulty
  estimate.
- **The wide margins are where a search has room to show an effect**, and at `n ≤ 100`
  they run to `0.5364` at `n = 51`, `0.5233` at `68`, `0.5218` at `84`. Those are also
  the cells where a hand attempt has the most to beat and the least chance of beating
  it, so they are calibration rather than hunting ground.

### What would count as success

A new record is a rare event.
Ellsworth’s `4 / 3004` at `n = 51` is a rediscovery rate for a case his own engine’s
record already set, which makes it an optimistic bound on discovery, and it is the only
published number of its kind.
So “did it find a record” cannot be the criterion for a research instrument, and three
things could be.

- **Time to a known answer, denominated in refined optima.** Treat a solved case as
  unknown, put a person on it, and count the refined and verified local optima before
  they reach within a stated distance of the record.
  Run the engine at the same count.
  This is clean, it is a rediscovery measurement with all that implies, and it is the
  one measurement that would settle whether a hand is worth its cost at all.
- **Reaching components the engine’s cold multistart never reaches.** More interesting
  and not currently available, because it needs the terminal-component identity that
  [H-012](../hypotheses/H-012-record-basins-are-rare.md) needs and does not have.
- **Whether the record accumulates.** Whether the tenth session is better than the first
  on the same measure.
  This is the only one of the three that requires nothing but the attempt log, and it is
  the one that distinguishes an instrument from an afternoon.

The failure mode worth naming in advance: a tool that is pleasant to use, produces a
picture, and whose attempts are never counted.
The test for that is simple and it is behavioural rather than technical.
Is a session that found nothing written down as carefully as one that found something?

### The honesty constraints, which the house already holds

- **A float feasibility check means something only with positive gaps.** A hand-edited
  configuration must be polished and exactly verified before any claim leaves the
  workbench. This is not a stylistic preference; `verify_packing`’s own docstring is the
  authority for it, and the defect that produced the function
  ([`corners_from_poses`](../../src/sqpack/verify.py), D-014) was a quench emitting a
  packing that violated its own constraints.
- **A hand-edited run is not reproducible from a seed**, so its provenance must be
  recorded as hand-made rather than dressed as a run.
  The frontier’s `construction_method` field already carries `hand-construction` for
  fifteen cases, so the register has the slot; what it does not have is a convention for
  recording *this* repository’s hand-made attempts, which is a small design question and
  a real one.
- **A near-record candidate is a candidate.** The atlas already holds an exact statement
  of how tight these things are.
  Over the 318 screened records and 52,064 squares in
  [`translation-escape-screen.json`](../../atlas/known-best/translation-escape-screen.json),
  the largest absolute container slack anywhere is `3.7e-33`: no packing in the corpus
  has slack. 296 of the 318 records still have at least one square that can be
  translated, 5,323 squares in all, and the screen’s own note is the sentence to keep: a
  strict-separating count is not a clearance count, because every square in every
  retained record touches something and the loose ones slide tangentially rather than
  float. 2,609 of the movable squares move with at least one contact staying exactly
  closed, at a median slide of `0.536`. A hand-made configuration that looks tight is
  almost certainly loose somewhere, and the escape screen is the existing tool for
  saying where.

## Threads Worth Framing, Without Committing to Any

### The relaxed intermediate, and what it does to H-013

Inflate the container, perturb, contract.
This is Gensane’s layer 3 with a container that breathes, and it is
[H-013](../hypotheses/H-013-delta-continuation.md)’s delta continuation with an explicit
schedule instead of a projection family.

The animation’s blind mode is already a crude instance of it, which is worth noticing
because it means the loop’s shape has been built and watched.
The container opens to `1.12` times the record’s side, holds for the first `0.2` of the
move while the new square inflates, then contracts toward the record’s side, pausing
whenever two full-size squares overlap by more than `0.08`, and reaching the record at
`0.9` if nothing jams.
It never wins: every matched pair loses, up to `6.8` per cent.

Two readings, and both matter.
It is a negative result about a badly built version, since the notes themselves record
that nothing checks the blind run against a real compaction and that the constants were
never swept. And it is a cheap positive: the loop runs, it is deterministic under a
seeded generator, and its failure mode is legible, since the contraction stalls on
overlap rather than on the objective.
H-013’s own kill condition is untouched by any of this, because it requires beating
direct multistart on the `n = 10` gate before it may consume an `n = 11` budget, and the
blind mode does not attempt that.
What has changed is that H-013 now has a demonstration of its own mechanism running
badly, which is a better starting point than a description.

### Does the tween model have research content, or is it purely exposition?

Two readings, held side by side on purpose, because the evidence supports both.

**It is exposition.** The correspondence between consecutive records exists so a video
is legible, and its cost function was tuned for that: at angle weights below 1 the
matching sends a corner square of the `2×2` to the centre of `n = 5` and lets the new
square appear in a corner, which contradicts the story every viewer knows, so the weight
was set to 1. A quantity chosen to look right is not a measurement.

**It is about the catalogue, not the animation.** Over the 158 genuinely matched pairs,
no square travels more than `1.66` units, 249 of 323 pairs move nothing more than one
unit, and 90.4 per cent of moving squares travel inside rigid blocks.
The one number that is invariant to the cost is the interesting one: total rotation is
forced by the change in tilt census between frames rather than chosen by the weight, and
dropping the weight from 8 to 0 changes it by only 13 per cent.
That is a statement about how the records themselves evolve in `n`, not about the
matcher.

**What would separate the readings is a null, and nobody has run it.** Match records at
distance 2, 3 and 5 in `n` under the same cost, and match records at similar `n` from
different construction families.
If consecutive records are closer than the null predicts, the catalogue has local
structure worth naming and possibly worth searching along.
If they are not, small displacements are a generic property of dense packings and the
Hungarian assignment, and the animation is exposition after all.
It needs no machinery beyond the matcher that already exists, it runs over records the
repository already holds, and no version of it has been run.

### Directional rather than isotropic pressure

[exp-136](../series/series-000-smoke-and-calibration/experiments/exp-136-round-1-pressure.md)
refuted the wall-pressure surrogate, and the refutation is a design error rather than a
null result, which makes it more useful than a clean negative.
`required_side` is minimised by a tight square; the aggregate `spread` term is minimised
by a disc. So the term optimises a disc: at `n = 5` every seed returns exactly
`2.828427126`, which is `2√2`, the side five axis-aligned unit squares need, and `0.121`
above the proved optimum the control reaches on every seed to `1.2e-08`. At `n = 11`
every seed returns exactly `4.0`. One cell of eleven improved and three regressed,
including both proved controls.

Squarl’s wall pressure is not this term.
It pushes each square inward from the container, so the force carries the wall’s normal
and therefore the container’s shape.
The open question is whether a per-wall directional term recovers what the aggregate one
destroyed, and it has a trap worth naming before anyone runs it: the tempting comparator
is the isotropic term, which is worse than doing nothing, and beating it would mean
nothing at all.
The comparator has to be the control, and the honest framing is that this
is a cheap partial substitute for the inflation rewrite rather than a competitor to it.

### Seeding off the grid above `n = 27`

Above `n = 26` nothing in the engine reliably leaves the grid.
At `1e10` pair tests per seed the collective arm returned exactly the grid at
`n = 29, 37, 50, 52` on every seed of both arms, and the grid median at `n = 27` with a
single seed at `5.878417`.

Two things complicate the obvious reading, and both point the same way.

**“Zero” is a resolution, not a proof.** The escape rate measured `0.0000` at `n = 26`
on an 8,000-proposal screen, and the arm left the grid at `n = 26` anyway, with the two
seed ranges disjoint and a median of `5.823450`. A measured zero at 8,000 proposals
bounds the rate at roughly `1e-4`; a round makes many orders of magnitude more proposals
than that. So the honest statement is that the escape rate falls below the screen’s
resolution somewhere around `n = 19`, and where it actually reaches zero, if it does, is
not known.

**The engine is not weak, it is disabled by its starting point.** Probing arm B’s own
emitted `n = 18` poses at side `4.84`, `3.5` per cent of single-square proposals lower
the side, against `0.0000` at the grid.
The sparsity is a property of the grid, not of the objective.
Anything that gets the configuration off the grid restores the ordinary move set to
usefulness, which is a strong argument for seeding and a strong argument for the
workbench, since they are the same argument.

That is where [H-004](../hypotheses/H-004-neighbor-transfer-seeding.md) sits, still
unbuilt, and it is now the highest-value unbuilt instrument on the search lane.

### Replica exchange over a pressure ladder

The one annealing-family scheme currently producing packing records, and the archive
cannot follow it.

The insight is that hard particles are athermal, so raising the temperature has nothing
to exchange and the parameter worth exchanging between replicas is the pressure.
The line built on it identified 108 novel maximal disk packings at `N = 300` to `720` in
2024, with the maintainer of the Packomania record tables as a coauthor, so the beaten
configurations were the recognised records.
Ellsworth’s 65,536 GPU threads are already 65,536 independent replicas; the missing
piece is the exchange.

The obstacle is documented and it is not laziness.
The 2024 paper and its 2026 successor both failed retrieval on 2026-09-08 and the audit
packet records the attempts and the open-access verdicts, so the replica count, the
ladder’s spacing and the cost per record are not in hand.
Only Odriozola’s 2009 predecessor is retained.
Building this here means reconstructing a design from an abstract, and it presupposes
the inflation formulation, because without a pressure there is nothing to ladder.
Both of those are real costs and neither is a reason to drop the direction.

### Search by projection, which turned out to be available immediately

Written into this thread list on 2026-09-09 and answered the same day, which is why it
reads differently from the rest.

The
[simulation survey](../../../docs/project/research/research-2026-09-09-simulation-mechanisms-for-packing.md)
ranks divide and concur first, and
[exp-139](../series/series-000-smoke-and-calibration/experiments/exp-139-projection-search.md)
ran it. The thing worth carrying into the rest of this document is not the sides it
reached but what its failure mode says about everything else here.

**A projection search has no tolerance dial, and that changes what a measurement
means.** Twenty-eight runs, every one ending on an arrangement whose deepest overlap is
the float `0.0`, re-checked by an oracle the search does not share.
Set against a penalty physics that produced zero feasible arrangements in 48 runs and
reported container sides *below* what geometry allows, this is the difference between an
instrument and a plausible picture.
Any thread above that ends in “and then we measure how close it gets” should be read as
presupposing this property, and most of them currently do not have it.

**It fails at the grid, like everything else here.** Every failed run failed at the
first tightening.
A grid of `k` squares in a row needs a container of exactly `k`, so the
moment the schedule asks for less the whole topology is infeasible at once — no partial
repair exists to find.
That is [the seeding thread](#seeding-off-the-grid-above-n--27) arriving from a
completely different direction, and it is now the third independent mechanism to hit the
same wall. The wall is a property of the *starting configuration*, not of any move set,
and this document should stop treating “escape the grid” as an annealing problem.

**The dial that decides everything is the start policy, and it trades.** Fresh random
starts buy escape; continuing the packing in hand buys refinement.
At `n = 5` every mixed or fully cold run left the grid and none of them matched the
single pure-continuation run that did.
That shape — reliability and quality pulling opposite ways, with the mixture beating
both endpoints at `n = 11` — is the same shape the hand-hunting argument above depends
on, and it is the first quantitative evidence for it on this problem.

**What it does not do is beat the engine.** `sqsearch` with a long schedule and the
collective move reaches `4.7071` at `n = 17` where this reaches `4.8047`, at a budget
orders of magnitude larger and with no feasibility guarantee.
The interesting reading is that the two are good at different things, and that a hybrid
— project to feasibility, then anneal, then project again — is not yet on any list here.

### A ladder of configuration constraints, and where memory sits on it

The frame this thread list was missing.
Structure is not on or off; it is a quantity, and the experiment worth running is which
is the *lowest* rung that suffices — because the top of the ladder is the answer itself,
and realising a full contact structure is a linear program rather than a search.

| rung | what is declared | for `n = 11` |
| ---: | --- | --- |
| 0 | nothing | a cold random start |
| 1 | a partition: which squares share an orientation, sizes only | two numbers, 6 and 5 |
| 2 | the contact graph: which pairs touch | 14 edges |
| 3 | the contact graph with types: which of those are face to face | 8 of the 14 |
| 4 | additional geometric constraints: which squares lie on the container | the other 20 of 34 incidences |
| 5 | additional memory constraints: repulsion from optima already visited | not built |

Rung 3 is the one that buys the most per bit, and the reason is worth stating.
An edge-edge contact pins the pair’s relative orientation to a quarter turn *without
naming an angle*, so the orientation classes are derived from the structure rather than
read off the record; a corner contact joins nothing, which leaves the hint loose exactly
where the record is loose.
That is the balance this exploration has been circling since the workbench sections:
constrained enough to cut the search space, flexible enough to move near optimality.

Every rung is declared as a **band, not an equality**, and that is not a detail.
Declared exactly, the record becomes a *repelling* fixed point: started from Trump’s own
`n = 11` packing with its fourteen contacts declared, the iteration drifts 0.0000 at 200
steps, 0.0012 at 1,000 and 0.2839 at 4,000, deterministically, at every relaxation above
`0.1`. Exact tangency makes the constraint sets meet non-transversally, the degenerate
case the 2025 flow-limit paper excludes from its convergence results.
The instrument is `devtools/sweep_structure_hints.py`; the controls beside each rung are
a *rewired* graph of the same size whose edges do not touch at the record, and a
*thinned* random subset, without which a result says only that constraints help and not
that the structure did.

**Rung 5 is metadynamics, and naming it connects a literature neither survey covered.**
The idea: map the local optima a search keeps falling into, then repel from those
specific configurations, so a run approaching an explored basin is pushed out of it —
physics with memory.
That is Laio and Parrinello’s history-dependent bias, deposited at visited points in a
collective-variable space to fill basins.
The closest thing either survey records is basin hopping
([H-137](../hypotheses/H-137-basin-hopping-over-the-lp-quench.md)), which perturbs an
incumbent rather than remembering where it has been.

Its hard part is not the bias, it is the coordinate.
Repelling in the raw `3n`-dimensional pose space is useless because the squares are
interchangeable, so a relabelled copy of a visited optimum is a different point there
and escapes the repulsion entirely.
The variable has to be permutation-invariant, and the candidates are already in this
repository and already listed in this document as the missing configuration distance:
the contact-graph signature, the angle-class census, the chunk taxonomy.
Tracked as `think-dh4k`.

## A Catalogue of Candidate Hypotheses

These are candidates.
None has an identifier, none is registered, and several should never be.
They are sorted by whether the instrument exists, because that is the distinction that
decides what could run next rather than what sounds best.

### Ready to formalise: the instrument exists or is a small extension

**C0a. The contact structures of best-known packings are a harvestable dataset, and they
are not arbitrary.** *Claim.* Extracting the full-side contact graph of all 324 retained
packings yields a population of structures with shared features, and a structure that
appears at one `n` recurs at others more often than a null model of random graphs at the
same edge density would predict.
*Evidence already in hand.* None directly, which is the point: nobody has looked.
Adjacent evidence is that the contact atlas already enumerates structures for small `n`
(`packing/atlas/known-best/contact-structures.json`, `contact-assembly-grammar.yaml`),
so a harvested population has something to be compared against rather than described in
isolation. *Instrument.* Exists and is a loop.
The full-side contact test is already computed over every retained packing for the atlas
shade rule, so the extraction is a pass over `witnesses/known-best/`, not a new
capability. *Criterion.* Would have to name the recurrence measure and the null before
looking, because a population of 324 graphs will show patterns whether or not any are
real.

**C0b. Which physics settings most reliably reach the optimum is itself measurable, by
sweeping the settings rather than the cases.** *Claim.* Over a fixed set of cases whose
records are known, the fraction of runs landing within tolerance of the record varies
systematically with the force law and the relationship setting, and some region of that
parameter space is reliably better than the rest.
*Evidence already in hand.* Two measurements, and together they say the space is real
and has no single best point.
Over 2,400 steps from a grid start, blind, the presets separate and they separate in
opposite directions at two cells (`measure_law.py --laws`): at `n = 17` the rigid law is
the only setting that leaves the trivial grid at all, reaching `4.756` against sticky’s
`4.988` and the record’s `4.676`; at `n = 29` the same law jams at `6.402` where sticky
sits at `5.986` against a record of `5.934`. A hard contact is a better search operator
at one size and a worse one at another, on the same physics with nothing else changed,
which is exactly the claim that some region of the space is better than the rest — and
exactly the warning that the region is not a single setting.
Against that, growth pays nothing yet (`measure_law.py --grow`): growing from a starting
size of `0.3` to unit squares over 7,200 steps lands `n = 17` at `4.988` under both the
`constant` and the `clean` rule, the same place the plain settle reaches and 6.7 per
cent above the record.
So one axis of the space is live and one is inert at these sizes and from this start,
which is the kind of thing a sweep is for and a single run cannot say.
The observation prompting the candidate stands: the workbench now has enough parameters
(rigidity, repulsion, attraction strength and range, the relationship mask, growth rule
and rate, annealing level) that they form a space rather than a handful of switches.
*Instrument.* Partly.
The workbench can run one setting at a time and report the gap; what is missing is a
driver that sweeps settings across cases headlessly and tabulates hit rates, which is
the same shape as `devtools/run_arm_sweep.py` and could reuse it.
*Criterion.* The honest one is a hit rate against the record over seeds and cases, at a
declared budget, with the caveat that tuning on cases whose answers are known is fitting
to a test set: any region found this way is a hypothesis about unseen `n`, not a result,
and would have to be confirmed on cases held out from the tuning.
That caveat is what makes this worth doing properly rather than casually, and it is why
the observation belongs here rather than in a hypothesis today.

*The larger form, which the owner named and which is not for today.* The sweep above
treats the settings as a list to try.
The ambition beyond it is a framework that models the strategies rather than enumerating
them: represent a physics strategy as a point in a parameter space, score it by how
reliably it reaches known optima, and then improve the strategy itself by iterating on
that score. Three things are worth saying plainly before anyone builds it.

First, this is hyperparameter search over a solver, and the repository already owns the
machinery for running it honestly: the campaign’s hypothesis records, pre-declared
accept rules and `devtools/run_arm_sweep.py` are the same shape, and a new framework
should extend them rather than start a parallel one.

Second, the failure mode is not subtle.
Tuning on cases whose answers are known is fitting to a test set, and a setting that
wins on the tuning cases has established nothing about unseen `n`. Any framework here
needs a held-out split declared before the first run, and the honest headline is the
score on the held-out cases, not the best score found.

Third, on gradients.
The simulator is a fixed-timestep program, so in principle the final container side is a
differentiable function of the force law’s parameters and a gradient could be taken
through the rollout rather than estimated by sampling.
In practice contact events are discontinuities: a pair that touches in one rollout and
misses in another gives a gradient that describes neither, and the objective is a max
over a few extreme squares, which is exactly the flatness the move-set finding is about.
Differentiable-physics work handles this with smoothed contacts, which changes the thing
being optimised into a softened relative of it.
That is a real technique and it is also a real hazard, so it belongs here as a direction
with a named difficulty rather than as a plan.

*Where it would live, and why the name matters.* The workbench today has two modes, Pack
for a single `n` and Animate for a range.
The form this takes is a third, **Calibrate**: choose the cases whose records you are
optimising against, choose which parameters vary and over what ranges, run seeds per
configuration, and rank by the fraction of runs landing within tolerance of the record
at a declared budget.

The three modes divide by who is doing the work, which is worth stating because it is
also what each is for.
**Pack** is the mode a person participates in: one `n`, the speed turned down as far as
wanted, squares grabbed and moved by hand, the settle watched rather than scored.
It is where the hand-hunting argument above actually cashes out, and its value is that a
person can intervene mid-run.
**Animate** is the machine rendering what is already known across a range, at speed and
without interaction, which is the video.
**Calibrate** is the machine searching over its own settings, with nobody watching any
single run.

*On the second name.* Animate was called Sweep until 2026-09-08, and the rename is not
cosmetic. Calibrate is the mode that sweeps — over parameters, not over `n` — and an
instrument with two modes called sweep would be permanently ambiguous about which axis
was moving.
Animate says what that mode does, and leaves the word for the thing that does
it.

*The three axes, and why Calibrate is cheap when it comes.* A mode is not a feature.
It is a choice on each of three axes, and every mode makes all three choices whether or
not it exposes them.

- **Scope** — what set of cases is in front of the instrument.
  Pack takes one `n`. Animate takes a range.
  Calibrate takes a set split into the cases it tunes on and the cases it holds back.
- **Strategy** — how the physics runs: the force law’s four parameters, the relationship
  graph, growth and its rule and rate, the annealing level, and which solver runs.
- **Presentation** — what a viewer sees: the colour scheme, the timing, the motion
  phasing, the desaturation while moving.

Read down the axes and the modes fall out of them.
Pack is one case, a strategy chosen by hand and changed mid-run, and presentation tuned
for watching. Animate is a range, a strategy that has to be the same at every `n` or the
frames are not comparable, and presentation tuned for a video.
Calibrate is a split set, a strategy that varies by construction, and no presentation at
all, because nobody is watching any single run.

The decomposition also prices the third mode, which is the practical reason to write it
down. **Calibrate is Pack’s strategy panel with a loop and a results table around it**:
the same single-`n` settle, the same parameters behind the same setters, the same gap
read at the end. Nothing new has to be modelled.
That is why it is cheap once Pack is right, and it is also why Pack should be got right
first: every part of Calibrate that turns out to be hard will be a part of Pack that was
left approximate, and it will be discovered a thousand runs at a time.

Mechanically it is Pack with a loop around it: the same single-`n` settle, repeated
while the parameters sweep, keeping what performed best.
Two kinds of best, and the difference matters.
Per run, the single configuration that reached the lowest container side, which is the
one to look at and the one most likely to be luck.
Statistically, the configuration whose distribution over seeds is best, by median or by
hit rate within tolerance, which is the one to believe.
A mode that reports only the first is a slot machine; a mode that reports both, and
shows how far apart they are, is an instrument.

The name was chosen over “backtest” deliberately.
Backtesting is a finance term where running a strategy against history is routine and
the overfitting risk is a footnote; here that risk is the main event.
Calibration is both the accurate description, since the instrument is being set against
known answers, and this repository’s existing word for it: the campaign’s series is
`series-000-smoke-and-calibration`, and the atlas pins its calibration-only annotation
layers to `n = 1..100` precisely so the rest stays an unseen corpus.

The naming does real work.
A mode called Calibrate that shows a calibration set and a held-out set side by side
makes the hazard structural rather than a caution in prose: the question “which set did
that number come from” is forced by the interface.
A mode called Backtest invites the best number on the screen to be read as the result.
The headline that mode reports should be the held-out score, and a winner whose held-out
score collapses is the most useful thing it could show.

*One question the mode cannot answer for itself: how often the split is declared.* Per
run, the split is a parameter of the configuration and a session may carry several; per
session, it is fixed once before the first run and every configuration that session
tries is scored against the same held-out cases.
Per session is the one to argue for, and the argument is one sentence: a split chosen
after seeing results is not a split.
Per-run declaration is a declaration in form and a search in practice — with 324 cases
and a mode built to make re-running cheap, a person who dislikes a held-out score can
redraw the line and go again, and nothing in the record would show that they had.
The cost of per session is real and worth naming: it forfeits the ability to re-scope
mid-afternoon, which matters most when the interesting cases are exactly the ones not
known in advance. This is a question about how the instrument is used rather than about
what it computes, so it is the owner’s, and it should be settled before Calibrate is
built rather than after: the answer decides whether the split lives in the run record or
in the session record, and retrofitting it the other way means every earlier number is
unscored.

**C0c. Enumerate the contact structures, then let the physics triage which are worth
exact treatment.** *Claim.* Running the settle under each enumerated contact structure
as its attraction mask separates the structures that realise from those that do not,
cheaply enough to order the exact realizer’s queue, and the ordering it produces is
better than enumeration order.
*Evidence already in hand.* The enumeration exists and is complete where it exists:
`packing/atlas/enumerated/` holds 11,013 orbits over all 21 connected unlabeled
five-vertex topologies, and `src/sqpack/contact_realization.py` already turns a scaffold
into a realization with exact arithmetic.
What is missing is a cheap filter in front of the exact step, which is what the
workbench’s contact relationship would be.

*Evidence measured since, and it is against the filter as built.* The contact
relationship exists now, and it has been measured twice, negatively both times.
Settled for 2,400 steps from a grid start under the sticky law
(`measure_law.py --graphs`), the fraction of the target graph’s edges that are full-side
contacts at the end is **1 of 4 at `n = 17` and 1 of 17 at `n = 29`** under the contact
mask, against **2 of 4 and 7 of 17** for attracting every pair indiscriminately.
Biasing toward the graph does worse than not biasing at all.
The second measurement is the sharper one, because it starts from a configuration that
already has the structure: under a hand-drawn ring joining each square to the next, from
an ordered fill (`measure_law.py --drawn`), the run ends at **1 of 5 at `n = 5` and 0 of
11 at `n = 11`** — and the ordered fill *starts* with 3 of 5 and 8 of 11 already
realised, consecutive indices in a row-by-row fill being adjacent squares.
The bias did not build a contact graph.
It pulled one apart.

Two measured reasons, and neither is a tuning problem.
**The pull cannot reach**: target pairs end one to four units apart — `n = 29`’s pair
`(0, 3)` at a gap of 3.91 — while the attraction acts over a quarter of a side, and
raising the range to 2.0, past the shipped bound, moves the fraction 0/4 to 0/4 at
`n = 17` and 0/17 to 3/17 at `n = 29`, inside the run-to-run spread.
**And where a pair does meet, it meets corner-to-side**: `n = 17`’s target pair `(0, 4)`
ends in contact at a gap of `−0.001` with its orientations 1.93° apart, where a
full-side contact needs them inside 0.5°. The law has no torque term, so nothing rotates
a pair into face-to-face registry.
Two cautions on reading those fractions.
`n = 100` reads 180 of 180 under every relationship, which is not the bias working — the
grid start of 100 *is* the record, so its contact graph is realised before the run
begins. And the full-side test is not symmetric in the pair: it reads the centre offset
in the lower-indexed square’s frame, which leaves two of 322 retained frames one edge
short of their own contact graph, a defect tracked separately and too small to move the
numbers above.

*Instrument.* Half exists, and the half that exists is now measured not to work.
The enumeration, the exact realizer and the contact-graph attraction mask are all there;
the driver that walks the enumeration, runs a settle per structure and tabulates which
realised is not. *Criterion.* Precision and recall against the exact realizer on the
size-five set, where the answer is already known for every orbit, before it is pointed
at anything larger.
*What the negative does to the candidate.* It does not kill it and it
does reorder it. C0c rests on the settle-under-a-mask being a usable filter, and on the
two cells where the answer is known the filter’s false-negative rate is near total: the
retained record’s own contact graph, handed to the settle as its target, comes back
essentially unrealised.
Precision and recall measured today would be measuring a torque-free law rather than the
idea. A pairwise torque term that turns two squares toward a shared edge is the missing
half, and it is the prerequisite this candidate did not know it had.

*The binding constraint is enumeration growth, and it is already priced.* The atlas is
complete at size five, not at `n <= 30`; `contact-enumeration-pricing.json` records caps
of 100,000 canonical proposals, 100,000 LP solves and 10,000,000 raw orbit images, with
a decision rule that refuses the legacy path when its exact orbit work exceeds the
declared budget. So “enumerate all plausible contact groupings” is a small-`n` method
whose ceiling has been measured rather than guessed, and the honest form of this
candidate is not “enumerate and optimise” but “use the settle to decide what the exact
realizer looks at next”.
The physics never certifies anything: only the exact realizer does, and a structure the
settle likes is a candidate, not a result.

*Note on where snapping belongs.* Ending a run on the retained packing is production
machinery, not evidence: it is how an Animate run across all 324 records lands each
frame on what is actually known.
It says nothing about the physics, because the physics did not find the endpoint.
Its research use is the reverse direction above, harvesting what the records’ structures
are, rather than the forward one.
The atlas video plan now carries the same statement as its own decision `D16`, so the
production side and the research side cannot drift on what a snapped frame means.

**C0d. A force law must hold a known optimum still.** *Claim.* Loaded with a retained
best-known packing and run under the law with no target and no snap, the configuration
does not drift: on a record with no movable square every square holds its pose exactly,
and on a record with rattlers only the squares the translation-escape screen already
identifies as free may move, with the container side never growing.

*Why it goes before C0b rather than after.* It is a necessary condition, so it needs no
discovery, no seeds and no budget argument.
A law that cannot hold a known optimum still cannot find one, and every hit rate C0b’s
sweep would report is uninterpretable until this passes.
It is also the cheapest test in the catalogue — 318 loads and 318 settles, no search —
and it is the only one for which the repository already holds the answer key.
It is two-sided, which is what makes it a test rather than an assertion: on some records
the law must hold everything, and on others it is allowed to move exactly the squares
the corpus says are loose.

*Evidence already in hand.* None on the claim; nobody has loaded a record into the
solver and watched it sit.
What is in hand is the answer key, verified here against
[`translation-escape-screen.json`](../../atlas/known-best/translation-escape-screen.json)
rather than taken on trust.
Of 318 screened records — six are excluded for a witness shape residual above the limit,
`n = 68, 69, 103, 105, 110, 131` — **296 have at least one square that can be
translated**, 5,323 squares in all, of which **2,714 can be pushed clear of everything
they touch**. So drift is not automatically a failure.
The **22 records with no movable square** are the 18 perfect squares from `n = 1` to
`n = 324` together with `n = 5, 11, 28, 40`, and those are the records on which any
drift at all is a defect in the law.
The largest absolute container slack anywhere is `3.7e-33`, so the container side is a
hard ceiling on every record and a settle that grows it has overlapped something.

*Instrument.* A small extension, and every part of it exists.
The workbench already loads a retained packing as a starting arrangement, already runs a
settle with the snap and the target off, and already reports the deepest overlap and the
side the arrangement would need.
What is missing is the driver: load each record, settle, report per-square displacement
and turn against the loaded pose, and join the result against the screen’s own
`movable_squares` list.
That is the shape of the headless `measure_law.py` harness the prototype already
carries.

*Criterion.* Declared per record before the run.
On a record with no movable square: maximum per-square displacement and turn below a
stated tolerance, and the container side non-increasing.
On a record with movable squares: every square that moved past tolerance appears in that
`n`’s `movable_squares` list, and the container side is non-increasing.
The headline is three counts — records held exactly, records where only listed squares
moved, records that failed — rather than a mean, because the failure being looked for is
categorical and a mean would hide a total failure at one `n` behind 300 successes.

*Two confounds to handle before it runs.* The screen states its own one-sidedness: a
miss proves only that one square cannot be **translated** at that tolerance, and
rotation and coordinated multi-square motion are outside the test, so a square that
turns in place is not a screen hit and needs its own tolerance rather than a pass.
And 23 of the 318 records are recorded as not stable across the screen’s tolerances
(`n = 132`, 154 to 156, 179 to 182, 206 to 210, 238 to 241, 270, 273, 297, 301, 305,
307); those should be reported separately rather than scored, because on them the answer
key is itself tolerance-dependent.

**C1. Anneal length and move family interact, and the interaction is the finding.**
*Claim.* At equal delivered budget, the improvement from the collective move and the
improvement from a tenfold longer anneal are not additive, and the both-factors arm
beats the sum of the two main effects.
*Evidence already in hand.* exp-138’s `2×2`: cells improving the control’s median by at
least `0.01` are 0 for the control, 4 for the collective move alone, 3 for the long
schedule alone, and 5 for both.
The both-factors arm’s best at `n = 17` is `4.677676`, against `4.682227` for the move
alone and `4.700170` for the schedule alone; its `n = 26` median is `5.710314`, against
`5.823450` and `5.887456`. *Instrument.* Exists: `--steps` and `--p-perturb` are both
already flags, and exp-138 reports `lines_changed: 0`. The extension needed is budget
accounting, because the both-factors arm overshot by `×1.31` at `n = 17`, `×2.13` at
`n = 37` and `×3.92` at `n = 50`, and the record says so itself.
*Criterion shape.* A factorial with delivered pair tests equal across arms to within a
declared tolerance, scoring the interaction term rather than either main effect, on the
cells where both factors are individually active.
*Why it is first.* Because the branch’s own record says the design input is contradicted
by it, and a contradicted design input is the most valuable thing a round can produce.

**C2. The collective escape rate predicts where the collective move works, once it is
measured to the right resolution.** *Claim.* The per-proposal probability that a
collective move lowers the side at the grid predicts, cell by cell, whether the
collective arm leaves the grid at a fixed budget.
*Evidence.* Currently against, at face value: `n = 26` measures `0.0000` and escapes, so
the screen’s zero is an upper bound rather than a rate.
The ordering `0.0051`, `0.0009`, `0.0000` across `n = 11, 17, 26` is otherwise
consistent with the outcomes.
*Instrument.* `devtools/measure_objective_sparsity.py` exists and needs only more
proposals; resolving `1e-6` needs on the order of `1e7` proposals per cell, which is
cheap because a proposal is a screen and not a run.
*Criterion shape.* A determination with an interval: the measured rate at the cells that
escaped is above the rate at the cells that did not, with non-overlapping intervals, at
a resolution that separates them.
*Note.* Cheap, and decisive about a claim three records now state as a flat zero.
It would tell the search lane whether `n = 26` is a boundary in the landscape or a
boundary in the budget.

**C3. The sparsity is a property of the grid, not of the objective.** *Claim.* The
fraction of single-square proposals that lower the side is near zero at the grid and
materially positive at every non-grid configuration of the same `n`, at the same scales.
*Evidence.* One measurement, in exp-134: `3.5` per cent at arm B’s emitted `n = 18`
poses at side `4.84`, against `0.0000` at the grid.
That is one configuration at one cell.
*Instrument.* The same sparsity tool, pointed at a sample of off-grid configurations
drawn from the arm’s own output at several sides.
*Criterion shape.* A determination over a stratified sample, reporting the lowering
fraction as a function of the configuration’s excess over the record.
*Why it matters more than it looks.* It converts a diagnosis into a design rule: the
right engine is two-stage, with a collective move to leave the grid and the ordinary
move set to work once it has, and nobody has tested the staging.

**C4. Neighbour-transfer seeding reaches cells nothing else reaches.** *Claim.* Seeds
built by adding a square to the `n - 1` record or removing one from the `n + 1` record,
with some straightened, beat cold starts at equal budget on cells above `n = 26`.
*Evidence and standing.* Registered as H-004, instrument marked not built, priority 2,
and framed at `n = 11`. The new material changes both its target and its priority: at
`n = 11` there is now a cold route that works, so the cell is a poor discriminator;
above `n = 26` there is no reliable route, and that is where transfer is the only
candidate other than a hand.
*Instrument.* Not built.
Add-one-in-largest-gap and remove-one-and-straighten proposers over versioned source
packings, with the common quench and verifier.
*Criterion shape.* H-004’s paired form carries over unchanged; the sweep should move to
the cells where the collective arm returns the grid.

**C5. A hand-made start, polished, beats a cold engine start at equal refined optima.**
*Claim.* On a case treated as unknown, a person using the workbench reaches within a
stated distance of the record in fewer refined and verified local optima than the engine
does. *Evidence.* None here at all.
The provenance census is historical and says people found these packings; it does not
say a person would beat a 2026 engine on the same case today, and the ten annealing
cases are recent, so the method mix is moving.
*Instrument.* The workbench, which does not exist, plus the attempt record, which does
not exist. *Criterion shape.* Paired on a rediscovery task, counting refined optima
rather than wall time, on solved cases held out from the person’s knowledge as far as
that is possible. *The honest problem with it.* Blinding a person to a published record
is close to impossible, and the workbench’s own gap bar shows the record by design.
Anyone who formalises this has to solve the blinding problem first, or accept that it
measures rediscovery under full information, which is a weaker claim than it sounds.

### Needs an instrument first

**C6. The relaxed intermediate reaches record components more often than direct
multistart.** *Claim.* H-013’s delta continuation, in the concrete form of inflate,
perturb, contract with a declared schedule.
*Evidence and standing.* H-013 is registered with its instrument marked not built and a
kill condition at the `n = 10` gate.
The new material does not move the verdict and does move the picture: the animation’s
blind mode is a running instance of the same loop, at `1.12` inflation with a
contraction that pauses on overlap, and it loses every matched pair by up to `6.8` per
cent. That is a demonstration of the mechanism failing under constants chosen for a
video, not a result about the mechanism, and the spike’s notes say as much themselves.
So H-013’s standing is unchanged as a hypothesis and improved as a build: its loop shape
has now been watched running.
*Instrument.* Not built.
A fixed-side feasibility and projection operator with a declared delta schedule,
predictor and corrector residuals, and a common terminal classifier, which the existing
side-minimising quench is not, because that quench erases delta.
*Criterion shape.* H-013’s paired form, unchanged, with the `n = 10` gate kept as the
gate.
*Note.* The overlap-driven stall is the interesting observable and nothing measures
it. If the contraction always jams on overlap rather than on the objective, the
schedule’s right variable is the overlap tolerance, not the delta.

**C7. A directional wall-pressure term does not have the disc pathology.** *Claim.* A
per-wall inward term, carrying the container’s normals, lowers the median best side
against the control on cells where the isotropic aggregate raised it.
*Evidence.* exp-136’s mechanism is exact and explains its own failure completely;
nothing bears on the directional variant.
*Instrument.* Not built; it is a change in `geom.rs` and it is a smaller change than the
inflation rewrite. *Criterion shape.* Paired against the control, never against the
isotropic term, on the proved cells first, since those are where the isotropic term’s
failure was unmistakable.

**C8. The inflation formulation makes every square carry objective gradient.** *Claim.*
Under a fixed container with a common square side maximised, the fraction of
single-square proposals that improve the objective at a jammed configuration is on the
order of the active contact set rather than of the two to four extremes.
*Evidence.* Analytic, and unanimous across three independent implementations that reach
records or near-records; nothing measured here.
*Instrument.* The rewrite.
This is the expensive one and it is the one everything else keeps pointing at.
*Criterion shape.* The sparsity measurement, run under both formulations at the same
configurations, which makes it a direct comparison rather than an outcome race.

**C9. Replica exchange over a pressure ladder beats independent replicas at equal
cycles.** *Claim.* As stated in the disk literature, transferred to squares.
*Evidence.* Strong and unreachable: 108 novel maximal disk packings, with the record
table’s maintainer as coauthor, and the two papers that would say how are not
retrievable. *Instrument.* Presupposes C8. Not costable from here.
*Criterion shape.* Records per cycle against an independent-replica control at matched
cycles, which is the comparison the source claims and the one the archive cannot read.

**C10. Record basins are rare in quench measure.** *Claim.* H-012 unchanged.
*What the new material does to its standing.* It supplies the first in-repo numbers of
the right shape without touching the estimand.
Over 55 runs per arm, exp-135 recorded 10 landing inside a `1e-4` basin proxy of a
record against 5 for the control, and 8 inside `1e-6` against 5, with `n = 10`
accounting for the cleanest part of it at 5 seeds of 5 inside `1e-4` against 0 of 5;
exp-137 recorded `0 / 25` record hits under both of its conditions across five cells.
None of that is H-012, because H-012 is stated over a named proposal, quench and
terminal equivalence at `n = 11`, and the terminal-component identity at `n = 11` still
does not exist. So the standing moves from “no in-repo data at all” to “hit counts at
`n = 10` under two named proposers, and the missing piece is the equivalence relation,
not the sampling”.

### Not yet sharp enough to test

**C11. Consecutive records are structurally close in a way that is not an artefact of
the matcher.** The tween statistics are suggestive and confounded, and the null
described above has to run before the question can even be stated as a claim.
Until then this is a research question, not a hypothesis.

**C12. A person sees shape where the engine sees a number.** No measure of shape
distance exists here, and the candidates (angle-class census, contact-graph signature,
tilt census) have never been correlated with anything.
Sharpening this needs an archive of refined optima first, which is C3’s and C10’s
prerequisite too, and that recurrence is itself informative.

**C13. The animation’s physics has research content.** Almost certainly not, in its
current form. Its constants were tuned to look right, its blind mode has never been
compared against a real compaction, and its own notes say so.
It is listed here only so that nobody has to rediscover the reasoning: this one should
be killed rather than sharpened, and the atlas video plan should keep it as exposition.

**C14. H-018’s negative is about the refiner, not about the basin.** Perturbing Trump’s
`n = 11` by `1e-3` returned within `1e-6` in zero of forty trials, in every arm, with
the residual scaling approximately linearly with the perturbation and shrinking with
effort.
The artifact’s own reading is incomplete convergence of the tested refiner rather
than evidence about basin width, and it explicitly declines to conclude anything about
an attracting basin, a basin radius, isolation or terminal-component membership.
Re-running it against `quench_bracket` in its current form, which converges cold at
`n = 5` on 12 of 12 and reached the solver floor on the proved controls, would separate
the two explanations.
That is a re-measurement rather than a hypothesis, and it is a prerequisite for anything
that wants to talk about basins at `n = 11`, C10 included.

## On Granularity, and What This Branch Got Wrong About It

This branch created four hypotheses and five experiment records in a single afternoon.
Two of them are closer to parameter sweeps than to standing scientific claims, and the
records say so themselves.

`H-138`, on cooling schedule length, is a claim about one flag.
Its experiment reports `lines_changed: 0` and states outright that no code change was
needed because `--steps` already existed, so the round is a parameter and not a feature.
`H-136`, on wall pressure, declared its own limit before running (the term is isotropic)
and was then refuted by a mechanism derivable from the term’s algebra: a `spread`
penalty is minimised by a disc.
Both produced real information.
Neither is the kind of claim that should hold a permanent identifier in a register whose
other entries are questions like whether some global minimiser has an
axis-plus-one-angle representative.

**The right shape was one hypothesis with arms underneath.** A single claim that the
proposer, not the acceptance rule, sets what this engine can reach, with four arms: the
collective proposal, the pressure surrogate, the schedule length, and the outer
basin-hopping loop. That carries exactly the same information.
It keeps the factorial visible, which matters, because the interaction between move
family and schedule length is the round’s most interesting result and it is currently
split across two records that each report it as a complication of their own verdict.
And it consumes one identifier instead of four.

The cost of not doing that was paid the same day and is concrete.
The four were registered as `H-127` through `H-130` and had to be renumbered to `H-135`
through `H-138` when this branch merged `main`, because the `n = 11` proof line had used
those same four identifiers for unrelated corner-class work.
The five experiment records were renumbered the same way and for the same reason, ending
at `exp-134` through `exp-138`. That is a whole afternoon’s identifiers consumed inside
a range another line was actively claiming, and it is why this document leaves a gap.

**Nothing above is a request to edit those records.** They are written, they are
renumbered, their verdicts stand, and rewriting a registered artifact to look tidier is
worse than leaving an ugly one in place.
The point is what the next round should look like.

## What Is Tracked as Work, and Where

Nothing above is registered, and none of it has an `H-` number.
What does exist, from 2026-09-08, is a bead epic for the instrument, so that the
workbench’s engineering does not live inside the atlas video plan that accidentally
produced it.

**Epic `think-qn6l`**, under the move-set campaign `think-5dt2`, with this document as
its spec. Under it:

- *In flight in the prototype:* `think-wklm` (Pack draws all `n` squares at rest,
  restart beside play), `think-9j4w` (the Sweep-to-Animate rename, internals included),
  `think-ic0g` (the solver choice joins the strategy group, the tween goes unavailable
  in Pack, timing and phasing become Animate-only), `think-j30w` (a best-known start and
  a re-randomising random start with a visible seed), `think-tswc` (steps per second
  under Node, with no browser).
- *Known defects, deferred deliberately:* `think-i52z` (the standing
  `mark stroke is none` failure, stale needle or real regression), `think-9nil` (the
  asymmetric full-side contact test), `think-yfhr` (the collision routine written
  twice), `think-ng1e` (no undo on the drawn graph), `think-zt6u` (42 greens do not hold
  324 identities), `think-7v26` (the rigidity slider reaches settings the fixed timestep
  cannot hold).
- *Not built:* `think-wffa` (Calibrate, candidate C0b) and `think-eq0n` (the
  stationarity test, candidate C0d), the second blocking the first.

The video artefacts stay with their own plan and are not repeated here: the frame record
and player, the capture pipeline that turns Animate into a video file, the transition
record and tween, and publication remain `think-hsdj`’s.

## What This Document Could Not Settle

- **Whether the collective move is genuinely inert above `n = 26`.** The screen measures
  zero and `n = 26` escaped anyway, so the direction of the error is known and its size
  is not. C2 is the cheap fix.
- **Whether the both-factors `n = 17` result is at equal budget.** It is not: `×1.31` at
  `n = 17`, and the same arm’s `n = 37` and `n = 50` results are explicitly recorded as
  not at equal budget at `×2.13` and `×3.92`.
- **Anything about what a person actually contributes.** The census is historical.
  Historical dominance is not a prediction, the machine’s ten cases are recent and
  clustered in the last two years, and no measurement anywhere in this repository or in
  the retained literature compares a human to an engine on this problem at matched
  effort. The workbench argument rests on provenance and on the record-holders' own
  recorded practice, and that is weaker evidence than a measurement, which is why this
  is an exploration.
- **The replica-exchange design.** Two papers, both unretrievable, and the audit packet
  records the attempts so the next reader inherits a checked obstacle rather than a
  guess.
- **How this repository should record a hand-made attempt.** The frontier has
  `construction_method: hand-construction` for other people’s constructions.
  It has no convention for its own, and inventing one is a prerequisite for the
  workbench rather than a consequence of it.
- **Whether Calibrate’s held-out split is declared per session or per run.** Argued for
  per session under C0b, on the ground that a split chosen after seeing results is not a
  split, but it is a question about how the instrument is used and it is the owner’s. It
  has to be answered before Calibrate is built, because it decides whether the split
  lives in the run record or the session record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
