# Research: Annealing for Square Packing, and How Far It Actually Reaches

**Date:** 2026-09-08

**Author:** Joshua Levy, with Claude Opus 5 assistance

**Status:** Complete for the question asked.

## Overview

The question this document answers, as the repository owner put it: *what are the best
simulated annealing algorithms we could use, and if we did just the right ones,
shouldn’t that solve square packing to `n = 100` at least?*

The short answer is that the premise is half right and the framing hides four different
problems.

The half that is right: the repository’s current annealer is far from the state of the
art, and the distance is not a matter of budget or cooling schedule.
It is a matter of formulation and move set.
Every engine that has actually set a record on this problem does something the
repository’s annealer does not do, and the missing pieces are nameable.
The people who hold the records say so themselves.
The provenance comment on the `n = 55` record, read first-hand for this document, states
that without special modifications the annealer “almost always gets stuck just above the
trivial size”, which is precisely what this repository measured at `n = 17` in exp-011.

The half that is wrong: “solve to `n = 100`” is not one task.
Of the 100 cases at `n <= 100`, 64 have a best-known packing equal to the trivial
`ceil(sqrt(n))` grid, which the repository’s annealer already returns by construction.
The real target is the other 36, and 21 of those 36 were found by hand rather than by
any search program. The best public annealer, run by the person who runs it best, needed
roughly a thousand classified local optima per record hit at `n` near 50, and a 2026
machine-learning system with a well-built pipeline spent a nine-hour production search
at `n = 17` without beating a packing found by an undergraduate in 1998. “The right
annealer solves everything to 100” is not supported by any evidence found here.

On the question as literally asked, there is a good answer and it is not a cooling
schedule. The annealing-family method currently setting packing records in the sibling
literature is **replica exchange over a pressure ladder**: many parallel chains that
swap configurations across levels of an inflation pressure, because hard particles are
athermal and temperature has nothing to exchange.
That scheme produced 108 new maximal disk packings in 2024. It is also a short step from
what the record-holders already run, since their 65,536 GPU threads are already
independent replicas without the exchange.

What *is* supported: a well-built engine should recover most of the 36 non-grid
best-knowns cold, and the repository’s current one recovers essentially none of them.
Closing that gap is a real and worthwhile program.
Proving optimality is a different problem that annealing does not address at all.

## Questions to Answer

1. What does “solve square packing to `n = 100`” actually require, case by case?
2. What algorithms produced the published records, in enough detail to reimplement?
3. What has the wider continuous-packing literature established about annealing against
   its competitors?
4. Does the move set matter more than the cooling schedule, and what is the evidence?
5. Given this repository’s own refutations at `n = 11` and `n = 17`, is the owner’s
   expectation plausible?
6. What engine would give the best shot at recovering known-best packings cold, and what
   is the cheapest first change to `sqsearch` that would move the number?

## Scope

Included: search algorithms for packing congruent squares under free rotation, the
transferable parts of the circle-packing and irregular-packing literature, the move sets
and local-refinement steps those methods use, and a concrete engine recommendation
scoped to this repository’s existing machinery.

Excluded: lower bounds and optimality proofs, except where needed to say what annealing
cannot do; exact algebraic promotion of a numerical packing, which
[the algorithms and tooling report](research-2026-08-22-square-packing-algorithms-and-tooling.md)
already covers; and the asymptotic regime.

Claims below are separated three ways.
**Published** means it is in a source with a URL and a date, quoted or paraphrased from
that source. **Measured here** means this repository ran it and recorded it in the
campaign. **Inference** means it is the author’s reasoning over the other two, and is
marked as such.

## 1. What “Solve to `n = 100`” Actually Asks For

**Measured here, 2026-09-08**, over the 100 case files `packing/frontier/n-001.md`
through `n-100.md`:

| Partition of `n <= 100` | count |
| --- | ---: |
| Best known equals the `ceil(sqrt(n))` grid | 64 |
| … of those, proved optimal | 33 |
| … of those, open | 31 |
| Best known beats the grid | 36 |
| … of those, proved optimal | 2 (`n = 5`, `n = 10`) |
| … of those, open | 34 |

The 64 grid cases are not a search problem.
`sqsearch` initialises its incumbent to the grid and reports it unless something beats
it (`packing/sqsearch/src/search.rs`, `run_chain`), so it “matches the known best” on
all 64 without doing anything.
For 31 of them nobody has ever found anything better, and
[X-009](../../../packing/campaign/explorations/X-009-where-a-new-packing-is-reachable.md)
records the relevant regularity: across the whole retained catalogue to `n = 324`,
re-indexed by `k = m^2 - n` with `m = ceil(sqrt(n))`, **nobody has ever beaten a grid at
`k <= m - 2`**. Re-deriving that index over the 31 open grid cases here gives `k` from 3
to 10, of which 18 sit in the never-beaten band, 6 at `k = m - 1`, and 7 at `k = m`
(`n = 12, 20, 30, 42, 56, 72, 90`).

**Inference.** For the 18 the honest task is a proof, not a search, and an annealer that
fails to beat the grid there is probably failing to beat an optimum.
The 13 at `k = m - 1` and `k = m` are the ones where a better-than-grid packing
plausibly exists, because the `s(m^2 - m) = m` conjecture has been falsified at
successively smaller `m`, most recently by Cantrell in February 2025 at `m = 11`, which
makes `n = 90` the one grid case at `n <= 100` that X-009 treats as a defensible search
target.

The 36 non-grid cases are the whole of the search problem, and their provenance is the
most informative number in this section.
**Measured here**, from the `construction_method` field of the same 36 case files:

| How the best-known non-grid packing at `n <= 100` was found | count |
| --- | ---: |
| Hand construction | 15 |
| Diagonal strip (Göbel and Stenlund families, closed form) | 6 |
| Simulated annealing | 10 |
| Extension of a neighbouring record | 3 |
| Unknown | 2 |

Twenty-one of the thirty-six are human geometry.
Ten are annealing, all between `n = 28` and `n = 87`, and all but one dated 2024 or
later. Over the full register to `n = 324` the annealing count is 40 cases, spanning
`n = 28` to `n = 307`; the
[2026-08-22 report](research-2026-08-22-square-packing-algorithms-and-tooling.md) gives
the compatible figure of 47 of 184 catalogue *pictures* crediting annealing, counted
against a different denominator.

The margin a search has to find also varies by an order of magnitude.
`n = 65` beats the grid by `0.4645`; `n = 89` beats it by `0.0503`. **Inference:** a hit
rate quoted without naming the case is close to meaningless, and any experiment on this
should stratify by margin.

## 2. What the Published Record Engines Actually Do

### 2.1 Gensane and Ryckelynck, 2005: inflation with simultaneous perturbation

**Published.** Thierry Gensane and Philippe Ryckelynck, *Improved Dense Packings of
Congruent Squares in a Square*, Discrete and Computational Geometry 34(1), 97-109, 2005,
[doi:10.1007/s00454-004-1129-z](https://doi.org/10.1007/s00454-004-1129-z). This is the
first algorithm that worked on this problem.
Friedman’s survey says so in as many words: the methods that worked for circles did not
generalise to squares
“[until recently when an effective algorithm was found](https://www.combinatorics.org/files/Surveys/ds7/ds7v5-2009/ds7-2009.html)”
(Electronic Journal of Combinatorics Dynamic Survey DS7,
[doi:10.37236/28](https://doi.org/10.37236/28), first published 6 March 1998, version 5
last updated 14 August 2009, with a corrigendum dated 1 March 2023; retained at
`packing/resources/web/friedman-ds7-survey-2009-html.md`).

The formulation is the first thing to take from it.
Instead of minimising the enclosing side, they fix the container and maximise the
**inflation** `omega(C)`: how far the squares can be grown from a given configuration
before an overlap appears.
`s(n)` is then tied to the supremum of `omega` over admissible configurations.
The abstract states the link directly and the paper builds a billiard-style algorithm on
it.

The square paper is paywalled and the author’s university page is gone, but the
companion method paper is fully open and states the same algorithm family verbatim:
Gensane, *Dense Packings of Equal Spheres in a Cube*, Electronic Journal of
Combinatorics 11 (2004) #R33,
[open access](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v11i1r33),
retained at
`packing/resources/papers/gensane-2004-dense-packings-equal-spheres-cube.pdf` with its
faithful extraction beside it.
Four numbered procedures, its Algorithms 1 to 4:

1. **Random walking.** Pick one object, draw a displacement uniform in a ball of radius
   `eps`, project it back into the container if it leaves, and **accept only if the
   minimum separation to every other object stays at least `alpha`**. Overlap is
   *forbidden*, not penalised, and there is no repair step.
2. **Stochastic billiard.** Run random walking; on improvement set `eps := 2 eps` and
   raise `alpha` to the new separation, otherwise `eps := eps / 2`; stop when `eps`
   falls below a floor.
   Collision directions are never computed.
3. **Perturbation.** Displace *every* object simultaneously by uniform draws of
   magnitude `eps`, projecting back into the container.
   This move deliberately permits overlap.
4. **With perturbations.** Alternate 3 and 2; if the result beats the incumbent keep it
   and double `eps`, otherwise restore the saved configuration and halve `eps`. Gensane
   reports a ratio `eps / factor` of `1e-12`, with `factor = 1e5`.

Two things in that specification deserve emphasis, because they contradict the shape of
the question this document answers.

**It is not simulated annealing.** The acceptance rule in layer 2 is strictly greedy.
There is no temperature, no Metropolis exponential, and no uphill acceptance.
The escape mechanism is layer 3’s simultaneous perturbation with a restore-on-failure
outer loop, not a hot phase.
The first algorithm that worked on squares in a square was an adaptive-step greedy
billiard, and it stood as the `n = 29` record from 2004 until December 2025.

**Layer 3 is the load-bearing one and the paper says why.** Layer 2 converges to
configurations that are *solid*, meaning no single object can be moved to improve the
packing, but solid is not locally optimal.
Simultaneous perturbation lets the search walk along a connected path of solid
configurations to a genuine local optimum.
Gensane found this necessary in three dimensions and expected it to matter generally.

The sphere paper also publishes per-`n` hit frequencies on an 800 MHz CPU, which are the
direct ancestor of Ellsworth’s 2026 basin statistics: at `n = 11` the best packing was
found about once in 140 runs, at `n = 24` about once in 50. Pairing a small sample of
billiard runs with one perturbation run found the best `n = 24` packing at roughly a
tenth of the cost of billiard alone.

Results for squares: improved `n = 11, 29, 37`, and an alternative optimum at `n = 18`;
`s(11) <= 3.8772`, `s(29) < 5.9648`, `s(37) <= 6.603236`. It *recovered* Trump’s 1979
`n = 11` packing rather than beating it, which made it the first computer packing
plausibly optimal, and its `n = 11` closed form is still the record.
DS7 also records that the `n = 29` packing it found carries squares at “no less than 6
different angles”, which this repository independently reproduced: exp-012 measured six
numerical angle classes in the current `n = 29` record at tolerance `1e-80`.

### 2.2 Schadt’s annealer and Ellsworth’s modification, 2024 to 2026

**Published.** The record engine for the low hundreds is a GPU simulated annealer
written by Thomas Schadt and run in modified form by David Ellsworth
([the Kingbird catalogue](https://kingbird.myphotos.cc/packing/squares_in_squares.html),
retained at `packing/resources/web/kingbird-squares-in-squares.md`, archived
2026-08-22). The search code is not public.
Two artifacts do exist and are worth more than the absence.

**Schadt’s own methodology note.** His single public repository,
[BalthasarStrauss/Squares-packing_S-29-_New-Record](https://github.com/BalthasarStrauss/Squares-packing_S-29-_New-Record)
(MIT, created 2025-12-08; the account’s `name` field is “Thomas Schadt”), publishes the
`n = 29` record he set in December 2025 along with a verifier, and states the method in
four sentences. The relevant one: the solution was found using C++ with data type
`float`, then relaxed to at least `1e-100` in C++ with Boost, then checked in Python at
the same precision. He also says the packing is “most certainly not fully optimized”.
The repository already retains this at `packing/resources/web/schadt-s29-2025/`.

**The single most useful sentence anyone has written about this problem.** The
provenance comment in
[`square-55.svg`](https://kingbird.myphotos.cc/packing/square-55.svg), fetched and read
first-hand on 2026-09-08, records that Schadt found the `n = 55` record on 3 January
2026 with a GPU annealer **started from a cherry-picked state produced by an earlier
program of his that reimplements the Gensane and Ryckelynck algorithm**. The comment
then says why the cherry-picking was necessary: without special modifications the
annealer “almost always gets stuck just above the trivial size”, which it attributes to
stacked rows and columns.
The same comment adds that the Gensane reimplementation, left to keep optimising that
state on its own, went a different way and stuck at `7.9577055242`, and that Ellsworth
*refound* the same record from randomness a month later with modified version 3 of
Schadt’s program.

**Inference, and it is the direct answer to the owner’s question.** That sentence is the
record-holders' own diagnosis of exactly the failure this repository measured in
exp-011, where `sqsearch` returned the trivial `5.0` at `n = 17` on five seeds of five.
Getting stuck just above the trivial size is not a bug in this repository’s
implementation, and it is not fixed by budget.
It is the default behaviour of a plain annealer on this problem, stated by the person
who holds most of the records, and the working fix in his pipeline is a *different
algorithm* upstream, a hand-picked starting state, or a modified annealer.
Note also the direction of the hybrid: the greedy billiard finds the state and the
annealer improves it, not the other way round.

**Inference, and it corrects something in this repository’s own notes.** The search
phase runs in *single precision*, and the multiprecision work is a separate downstream
relaxation.
`packing/campaign/ideas.md` parks GPU population search partly on the grounds
that MPS “forces `float32`, the wrong precision for a geometry whose true contacts are
exactly zero”. Schadt’s note says the record engine searches in float32 and relaxes
afterwards, so float32 is the right precision for the *search* stage and the wrong one
only for the stage that is not the search.
That objection should not block a GPU search lane.

**Ellsworth’s published run statistics.** These are the only hard performance data of
their kind for this problem, and the repository retains them at
`packing/resources/web/kingbird-run-statistics-2026/` (retrieved 2026-08-31; sources
[square-51.stats.txt](https://kingbird.myphotos.cc/packing/square-51.stats.txt) and
[square-55.stats.txt](https://kingbird.myphotos.cc/packing/square-55.stats.txt)). Both
runs used an NVIDIA RTX 3080 Ti with the annealer set to 65,536 threads.

At `n = 51`, over nine sessions on 31 January and 1 February 2026, the classified basins
fell out as:

| refines to | instances |
| --- | ---: |
| `s = 7.70435372947124...` (Hajba, July 2009) | 2,816 |
| `s <= 7.70374810693708...` | 184 |
| `s = 7.70079923541701...` (the record) | 4 |

The record basin’s share is `4 / 3004`, about `1.3e-3`, roughly 700 times less likely
than the modal basin.
Ellsworth’s own phrase for it is “an exceedingly rare find”.
At 23.571 seconds per classified basin he computes 4.917 hours of GPU time to hit the
record basin once. At `n = 55`, five sessions produced 1,893 instances below `s = 8.0`,
of which five sit in the record family, at 2.614 seconds per instance and a computed
40.604 minutes per qualifying hit.

Three workflow facts in those files matter as much as the rates.

- The schedule is **tuned from the statistics of past successes**: the `n = 51` file
  says the last three sessions were the most optimised, “with the median average
  temperature and cooldown period taken from the previous sessions’ finds”.
  The annealer’s parameters are fitted to the empirical distribution of hits, not chosen
  a priori.
- The annealer’s output is a **basin**, not a packing.
  A separate refinement drives it to the local optimum, and a further analytic step
  produces the exact value.
  The `n = 55` file distinguishes basins that “directly”, “readily” and “with more
  delicate refinement” reach a target.
- Seeding is usually not cold, and is often not even automatic.
  The catalogue’s provenance comments record runs started from randomness, from a
  neighbouring record with squares removed and some straightened, from a larger packing
  with dozens of squares deleted, from redistributing squares along a diagonal, from an
  analytically constructed state, and, at `n = 103`, from manually moving squares in one
  corner of the picture and feeding the result back in to coax out a particular
  improvement. Large cases run for weeks of wall clock: `n = 303` ran from 23 February to
  13 March 2026, and `n = 304` from 30 April to 16 May 2026.

**Inference.** The unit of work in a serious record search is one *refined local
optimum*, and the currency is basins per record, not moves per second.
At `n` near 50 that currency reads roughly `10^3` classified basins per record hit.
Any budget this repository quotes for a search experiment should be denominated the same
way.

### 2.3 Squarl, 2026: an open implementation with the whole pipeline visible

**Published.** [sam-bee/squarl](https://github.com/sam-bee/squarl), a Go, CUDA and GoMLX
project by Sam Burns, most recently pushed 2026-08-05, with an accompanying three-part
write-up at
[sam-burns.com](https://sam-burns.com/posts/n17-square-packing-near-record-arrangement/)
(part 2 dated 5 August 2026; figures and data retained at
`packing/resources/web/burns-n17-series-addendum-2026-09-07/`, and the repository’s own
documentation retained at `packing/resources/web/squarl-n17-2026/`, pinned at commit
`016dff98`, from which every figure in this section is read).
It targets `n = 17` only.
It did not beat the record.
It is nonetheless the most useful single source found for this question, because every
component the closed engines hide is written down.

Its formulation is the inflation formulation: a unit container, seventeen squares of
side `s`, initial states built without overlap at `s = 1/7`, and the reported container
width is `1/s`.

Its move set, in the README’s own terms, is “CUDA-native individual and contact-group
actions”, and **“every action contracts, acts, and re-expands to a legal measured
packing”**. A move shrinks the squares to create room, applies a translation or rotation
to one square or to a contact group, then re-expands maximally.
The score of a move is the room it created globally.

Its local refinement has two tiers.
The fast tier is a batched CUDA **wall-pressure** solver that translates and rotates
copies of the state; it runs on every rollout and, in the docs’ words, “discovers useful
contact basins at high throughput”.
The deep tier, described in `docs/deep-polishing.md` and retained at
`packing/resources/web/squarl-n17-2026/squarl-docs-deep-polishing.md`, is the part worth
copying:

- One **directed separating-axis branch is inferred per pair**, choosing the branch with
  the largest current margin.
  A pair is *ambiguous* when the two best margins differ by at most `5e-5`, and only
  ambiguous pairs enter a bounded alternative-branch beam (at most two pairs, four
  states, one full alternative refinement).
- **For fixed angles, a float64 simplex LP solves all 34 centre coordinates and the
  container width together**, under 68 wall constraints and 136 directed pair
  constraints. A verified feasible basis is reused between nearby angle proposals.
- **Angles are tied into classes and then released.** Angles within `0.002` radians of
  an axis are snapped to an exact multiple of `pi/2`; other angles within `0.01` radians
  of each other are tied, optimised by a bounded Nelder-Mead search over the tied
  parameters, then released as independent variables.
  The default budget is 96 clustered and 32 released evaluations.
- Acceptance is guarded: an improvement is taken only when two deterministic replays
  agree within `5e-7` and pass independent wall and separating-axis verification within
  `2e-7`.

What it achieved, from `docs/final-search-closeout.md`
(`packing/resources/web/squarl-n17-2026/squarl-docs-final-search-closeout.md`): a final
non-learning production search ran 32,390 seconds, completed 36 blocks of 40 proposals
(576 archive mutations, 720 separator-boundary mutations, 144 parent-conditioned
topology kicks, and explicitly “no frozen-source or ML proposals”), evaluated 1,162
centre-LP candidates and made 143 deep attempts.
Its best strict float64 width was `4.675530095599908`, which is `1.995e-9` **above**
Bidwell’s `4.67553009360455`. The conclusion in the repository’s own words is that the
published reference was not beaten under the strict validation rule.

**Inference, with a caveat.** Reaching `4.6755300956` means the search was inside
Bidwell’s arrangement, not merely near its value; the remaining `2e-9` is a numerical
resolution question, not a topology question.
The caveat is that the proposals came from an archive built by the project’s own earlier
searches, and a companion document (`docs/hard-topology-drain.md`, retained at
`packing/resources/web/squarl-n17-2026/squarl-docs-hard-topology-drain.md`) says of an
earlier four-hour drain that “no retained state exactly matched the published-record
material basin”. So this is a warm search over a self-built archive, not a cold
discovery, and the sources do not settle which run first entered that basin.

Separately, the blog series reports that four independent searches converged on a
*different* topology at width `4.677648294965133`, eleven axis-aligned squares and six
at one common tilt, and the author’s summary of the whole effort is that the world
record was not broken.

### 2.4 General-purpose global optimisation, as the control

**Published.** Berthold, Kamp, Mexi, Pokutta and Pólik, *Global Optimization for
Combinatorial Geometry Problems Revisited in the Era of LLMs*
([arXiv:2601.05943](https://arxiv.org/abs/2601.05943), submitted 9 January 2026,
retained at
`packing/resources/papers/berthold-kamp-mexi-pokutta-polik-2026-global-optimization-combinatorial-geometry.pdf`),
ran FICO Xpress 9.8 and SCIP 10.0 on packing benchmarks with a 10,000 second limit
preceded by a 5,000 second multistart, on a 48-core Xeon Gold.
Restricted to squares in a square, the
[2026-08-22 report](research-2026-08-22-square-packing-algorithms-and-tooling.md#general-purpose-global-optimization)
tabulates the outcome: they match the record at `n = 5, 10, 11`, miss the *trivial* grid
at `n = 16` by returning `4.00001`, and fall behind from `n = 17` onward, returning
`6.00000` at `n = 29` where the record is `5.9338`.

Their May 2026 follow-up, *Out-of-the-Box Global Optimization for Packing Problems*
([arXiv:2605.04850](https://arxiv.org/abs/2605.04850), retained at
`packing/resources/papers/berthold-kamp-mexi-pokutta-polik-2026-out-of-the-box-packing-problems.pdf`),
packs `n` regular `m`-gons into a regular `l`-gon under free rotation with a
Farkas-lemma non-overlap formulation, and does set new incumbents at several `(l, m)`
pairs, beating records held by Cantrell, Friedman and Morandi.
**Squares in a square, the case `(4, 4)`, is not among them**, and their median
optimality gaps run from `9.9%` to `15.2%`, so the dual bounds are far from closing
anything.

**Inference.** This is the calibration point for the whole question.
State-of-the-art general-purpose global optimisation, given hours per instance on 48
cores, reproduces the records to about `n = 16` and then degrades, and when the same
team went looking for new incumbents under free rotation a year later, this particular
family was one they did not move.
Any claim that a general method “should” reach `n = 100` has to explain why it beats
this result by a factor it has never been shown to beat.

## 3. The Wider Family, and a Correction

Circle packing is the better-studied sibling and its solvers transfer, because the hard
structure is the same: a continuous, nonconvex, highly multimodal objective with an
enormous number of nearly-equal local optima.

**The correction comes first, because the obvious story is wrong.** It would be tidy to
report that basin hopping beats annealing on packing.
It is not what the literature says.
No matched-budget head-to-head of basin hopping against simulated annealing on a
continuous packing problem was found at all.
The basin-hopping papers compare against the *record table*, not against an annealer run
under an equal budget.
And in the one place where both families were later measured on shared instances, the
annealer did better.

Ye, Huang and Lü, *Iterated Tabu Search Algorithm for Packing Unequal Circles in a
Circle* ([arXiv:1306.0694](https://arxiv.org/abs/1306.0694), 2013), Table 3, read from
the PDF for this document and retained at
`packing/resources/papers/ye-huang-lu-2013-iterated-tabu-search-unequal-circles.pdf`,
compares their method against several references on the 30 circle-packing-contest
instances at `n = 21` to `50`:

| their method against | better | equal | worse |
| --- | ---: | ---: | ---: |
| Population basin hopping (Addis, Locatelli and Schoen, the contest winners) | 27 | 3 | 0 |
| The contest record over all 155 teams | 25 | 4 | 1 |
| **Simulated annealing (Müller, Schneider and Schömer, 2009)** | **20** | **7** | **3** |
| Best known at the time | 14 | 13 | 3 |

Population basin hopping was beaten on every instance where the two differed.
The annealer was not: it tied on 7 and won on 3. The annealing paper in question is
André Müller, Johannes J. Schneider and Elmar Schömer, *Packing a multidisperse system
of hard disks in a circular environment*, Physical Review E 79:021102 (2 February 2009,
[abstract](https://link.aps.org/doi/10.1103/PhysRevE.79.021102)), whose own summary is
that it found denser packings than the literature held for various instances, on the
same family the basin-hopping team had won the contest with.
That paper is closed access with no preprint and is **not** in the archive; the failed
retrieval and its open-access verdict are recorded in
`packing/resources/web/annealing-methods-audit-2026-09-08/`, so what is claimed about it
here is only what Ye, Huang and Lü’s retained table reports.

So the honest generalisation is **not** that annealing loses.
It is that the acceptance rule is not what separates these methods, which is the same
conclusion section 4 reaches from the other direction.
The methods that do well are two-level: a cheap global proposal on top of a strong local
solver, with the *perturbation* rather than the acceptance rule doing the steering.
Annealing, basin hopping and thresholding search are three ways of deciding what to
keep; they differ far more in what they propose and what they refine with.

With that correction on record, five published results carry the substantive argument,
and all four have numbers.

**Multistart does not work, and the reason is counted.** Grosso, Jamali, Locatelli and
Schoen, *Solving the problem of packing equal and unequal circles in a circular
container*, Journal of Global Optimization 47:63-81, 2010
([preprint](https://optimization-online.org/wp-content/uploads/2008/06/1999.pdf),
retained at
`packing/resources/papers/grosso-jamali-locatelli-schoen-2010-packing-equal-unequal-circles.pdf`),
ran 50,000 local searches from random starts and found roughly **16,000 distinct local
minimisers by `n = 40`**, with the count rising rapidly and irregularly in `n`. Their
conclusion is that multistart is most likely not an appropriate method for this problem.
Against monotonic basin hopping, plain multistart with twice the local searches reached
the best known solution in only a few cases and in a single case cleanly.

**The perturbation magnitude has a sharp optimum, and it is the parameter that
matters.** The same paper swept the displacement magnitude over `{0.6, 0.8, 1.0, 1.2}`
on `n` from 60 to 80 and counted failures: 14 at `1.2`, 8 at `1.0`, 8 at `0.6`, and **3
at `0.8`**. Their explanation is the cleanest statement of the tradeoff anywhere: too
small and the new start lies in the basin of the current minimiser; too large and the
method degenerates to multistart, which disrupts the structure.
A good perturbation preserves structure.

**The landscape is mostly single-funnel, with a minority that is not.** Addis, Locatelli
and Schoen, *Disk Packing in a Square: A New Global Optimization Approach*, INFORMS
Journal on Computing 20(4):516-524, 2008
([preprint](http://www.optimization-online.org/DB_FILE/2005/10/1229.pdf), retained at
`packing/resources/papers/addis-locatelli-schoen-2008-disk-packing-square.pdf`),
conjecture that the problem has a **funnelling landscape**, the feature familiar from
molecular conformation, and build basin hopping on that conjecture: 32 improved
instances for `n <= 130`, the smallest at `n = 53`, plus one sphere improvement at
`n = 28`. Grosso et al.
then measure where the conjecture fails: population basin hopping is usually not worth
its cost, because single-path search is already efficient, **but at `n = 31` monotonic
basin hopping found the best known solution in 1 run of 50 while population basin
hopping with 10 members found it in 9 of 10**. That is the signature of a multi-funnel
instance inside an otherwise funnel-like family, and which `n` behave that way cannot be
predicted in advance.

**The single most decisive move-versus-schedule measurement on a packing problem.** Lai,
Hao, Xiao and Glover, *Perturbation-based thresholding search for packing equal circles
and spheres*, INFORMS Journal on Computing, accepted 31 January 2023
([PDF](https://leria-info.univ-angers.fr/~jinkao.hao/papers/LaietalJOC2023.pdf),
retained at
`packing/resources/papers/lai-hao-xiao-glover-2023-perturbation-thresholding-search.pdf`).
The framework is thresholding search, so there is **no cooling schedule at all**. They
compare two perturbation operators: a one-shot uniformly random perturbation at strength
`0.8` (Grosso’s value), and a *sequential* random perturbation, a series of small
perturbations each followed by a very short local optimisation with the strength
decayed, which they explain as smoothing the landscape by eliminating small barriers
without moving the global optimum.
Over 100 runs per instance: on one sphere instance the sequential operator’s success
rate rises to **100%** while the one-shot operator stays at **0%**; on one circle
instance the result is exactly reversed.
An adaptive hybrid does well on everything.
Their own summary is that performance is strongly related to the perturbation operator.
The method improved 156 best-known circle results for `2 <= n <= 400` and 66 best-known
sphere results.

Threshold accepting also has a direct track record on the sibling problem: the
TAMSASS-PECS algorithm (*Packing Equal Circles in a Square II: New Results for up to 100
Circles Using the TAMSASS-PECS Algorithm*,
[doi:10.1007/978-1-4613-0295-7_15](https://doi.org/10.1007/978-1-4613-0295-7_15))
reported better solutions than the then-published literature at `n = 32, 37, 47, 62, 72`
and forty new results, using a worsening threshold in place of the Metropolis rule.
That chapter is closed access and is not retained; the check is recorded in
`packing/resources/web/annealing-methods-audit-2026-09-08/`.

**The one place where an annealing-family method is provably producing packing records
right now is replica exchange over a pressure ladder.** This is the most directly usable
answer to the owner’s question that this survey found, and it is not in the
square-packing literature at all.

The insight is Odriozola’s, and it is one sentence: hard particles are *athermal*, so
raising the temperature does nothing useful; the parameter to exchange between replicas
is the **pressure**, expanding the volume to let a crowded system unblock
([arXiv:1010.2923](https://arxiv.org/abs/1010.2923), Journal of Chemical Physics 131,
144107, 2009; retained at
`packing/resources/papers/odriozola-2009-replica-exchange-hard-spheres.pdf`, and the
OpenAlex response confirming the preprint and the article are the same work is in the
audit packet). The line built on it:

- A 2018 study ran one replica per GPU core, thousands of replicas, for disks in a
  circular cavity at `N <= 125`, and matched every conjectured-optimal packing.
- Basurto, Gurin, Specht and Odriozola, *Searching for the maximal packing fraction of
  hard disks confined by a circular cavity through replica exchange / event-chain Monte
  Carlo*, Journal of Chemical Physics 161(4):044110, 28 July 2024
  ([doi:10.1063/5.0219006](https://doi.org/10.1063/5.0219006)), ran `N = 300` to `720`
  and **identified 108 novel maximal packings, some beating the existing configuration
  by more than `0.001` in packing fraction**. Eckard Specht, who maintains the
  Packomania record tables, is a coauthor, so the beaten configurations are the
  recognised records. Both the article and its 2026 successor were attempted on
  2026-09-08 and neither could be retrieved; the attempts, HTTP results and open-access
  verdicts are in `packing/resources/web/annealing-methods-audit-2026-09-08/`, which
  retains the OpenAlex record for the 2024 paper.
- A 2026 successor, Basurto, Gurin, Varga and Odriozola, *Densest packings and
  accelerated equilibration of hard body systems via out-of-equilibrium replica exchange
  Monte Carlo method*, Computer Physics Communications 320:109990
  ([doi:10.1016/j.cpc.2025.109990](https://doi.org/10.1016/j.cpc.2025.109990), located
  through the Crossref response retained in the audit packet), makes the replica
  exchange deliberately *out of equilibrium*, violating balance to force replicas across
  the whole pressure range, reports beating standard replica exchange at equal cycles,
  and sets new records to `N <= 1000`.

**Inference.** This is what “the right annealing algorithm” looks like in 2026 for a
packing problem, and it is closer to what Ellsworth already runs than it first appears:
his 65,536 GPU threads are 65,536 independent replicas, not a domain decomposition.
The step he is missing, and that this line has, is *exchange* between them.

The structural claim underneath all of this is that **the acceptance rule is the least
important part of a stochastic packing search**. What matters is the formulation, the
perturbation, the schedule *parameter* being the right physical one, and the strength of
the local solver.
Annealing is a way of accepting moves; it says nothing about any of the
four.

**Why the billiard half of this does not port to squares, and what that costs.** The
event-driven Lubachevsky and Stillinger algorithm grows particles until jamming by
predicting collision times analytically.
That line was extended to smooth convex bodies, ellipsoids and superquadrics, and stops
there: a polygon has no analytic overlap potential, so there is no collision-time
predictor for a growing, rotating square.
Torquato and Jiao abandoned dynamics for Metropolis moves plus separating-axis tests for
exactly this reason.
It also explains a design choice in Gensane’s method that otherwise looks odd: his
billiard is *stochastic* and never computes a collision direction, which is precisely
how he avoids needing the predictor.
One further caveat on borrowing from that literature: the adaptive shrinking cell
optimises a periodic fundamental cell rather than a bounded container, and unit squares
tile the plane, so the periodic formulation is vacuous here.

**The dimension argument, which is the best reason to expect the transfer to hold.**
Gensane’s own summary of his sphere results is that plain billiards suffices for disks
in a square, but simultaneous perturbation is indispensable in three dimensions.
A disk in the plane has two degrees of freedom; a sphere in space has three; **a freely
rotating square in the plane also has three**. The regime where he found perturbation
indispensable is the regime this problem sits in.
That is an inference, not his claim, but it is the sharpest one available.

**What is still inference.** None of the measured results in this section is on squares
in a square. The transfer rests on the shared structure, on the degree-of-freedom count
above, on Gensane and Ryckelynck having built the square method by porting the disk
billiard, and on Ellsworth and Squarl independently arriving at the same two-level
shape.

## 4. The Move Set, Not the Cooling Schedule

The canonical experimental study of annealing settled the schedule half of this question
and it has not been overturned.
Johnson, Aragon, McGeoch and Schevon, *Optimization by Simulated Annealing: An
Experimental Evaluation*, Operations Research 37(6):865-892 (1989,
[full text](https://faculty.washington.edu/aragon/pubs/annealing-pt1.pdf)) and
39(3):378-406 (1991,
[full text](https://faculty.washington.edu/aragon/pubs/annealing-pt2.pdf)); both parts
retained at
`packing/resources/papers/johnson-aragon-mcgeoch-schevon-1989-annealing-part-i.pdf` and
`...-1991-annealing-part-ii.pdf`. Their numbered conclusions, read from the Part I PDF
for this document:

- **Observation 5**: there seems no reason to replace standard geometric cooling by any
  of the non-adaptive alternatives they examined, which included logarithmic and linear
  temperature cooling.
- **Observation 4**: simple-minded adaptive scheduling appears to yield no improvement
  beyond what the extra running time it consumes would have bought anyway.
- **Observation 6**, by contrast, is about move generation, and it is positive: better
  solutions are found at a given running-time bound by generating moves from random
  permutations rather than independently, an effect they size at almost what doubling
  the running time would buy.

Part II is the sharper result, because it changes only the neighbourhood.
On the same graph-colouring instance with the same schedule machinery, the penalty-
function neighbourhood needed 182 hours to find a 91-colouring, while in that same 182
hours the Kempe-chain neighbourhood found one using **89** colours.

Nothing in the packing literature contradicts this and much of it amplifies the point:
Lai and colleagues’ `0%` against `100%` success swing from changing only the
perturbation operator (section 3); and, in the statistical physics of dense particle
systems, Ninarello, Berthier and Coslovich’s finding that alternating ordinary
displacement moves with particle swaps accelerates the dynamics by up to **ten orders of
magnitude** (*Models and algorithms for the next generation of glass transition
studies*, Physical Review X 7, 021039, 2017,
[doi:10.1103/PhysRevX.7.021039](https://doi.org/10.1103/PhysRevX.7.021039); retained at
`packing/resources/papers/ninarello-berthier-coslovich-2017-next-generation-glass-transition.pdf`).
No schedule change buys `1e10`.

Three independent implementations of *this exact problem*, built by people who did not
coordinate, all use enriched move families, and none of them differs from `sqsearch`
mainly in its schedule.
One of them holds most of the records and says in writing that the schedule is tuned
after the fact from the statistics of successful runs.
Another does not anneal at all.

The move sets actually used by systems that get close on this problem, collected from
section 2:

| Move | Used by | What it does |
| --- | --- | --- |
| Single-square translate | all | the baseline |
| Single-square rotate | all | the baseline under free rotation |
| Simultaneous perturbation of every object | Gensane and Ryckelynck layer 3 | walks along a path of solid configurations to a true local optimum |
| Contact-group (block) move | Squarl | moves a rigidly-touching cluster as one body |
| Contract, act, re-expand | Squarl | makes room before moving, then rescores by how much room the move created |
| Wall pressure | Squarl fast polish | pushes every square inward from the container, so the objective is felt everywhere |
| Fixed-angle LP over all centres and the side | Squarl deep polish; this repository’s H-002 | solves the entire translation subproblem exactly |
| Angle tying and release | Squarl deep polish; this repository’s exp-006 | collapses `n` angles to a handful of classes, then frees them |
| Remove-and-straighten from a neighbouring record | Ellsworth’s seeding | transfers structure across `n` |
| Separator-boundary mutation | Squarl | changes which separating axis a pair uses, i.e. changes the combinatorial cell |
| Rotational compaction and separation | Milenkovic 1998; Gomes and Oliveira 2006 | translates *and rotates* every piece at once to a local overlap minimum, by LP |
| Swap two objects | Grosso et al.; Imamichi et al. ILSQN | attacks combinatorial difficulty that continuous moves cannot reach |
| Sequential perturbation with decaying strength | Lai et al. 2023 | smooths the landscape by erasing small barriers |

`sqsearch` implements exactly the first two.

**The collective move is the one every serious implementation has and `sqsearch` does
not.** Li and Milenkovic’s compaction and separation algorithms (*Compaction and
separation algorithms for non-convex polygons and their applications*, European Journal
of Operational Research 84:539-561, 1995) translate *all* pieces at once by linear
programming, either to shrink the container or to remove overlap.
Milenkovic’s *Rotational polygon overlap minimization and compaction* (Computational
Geometry 10(4):305-318, 1998) extends this to translate and rotate all pieces at once,
which is the operator this problem actually needs.
Gomes and Oliveira, *Solving irregular strip packing problems by hybridising simulated
annealing and linear programming* (European Journal of Operational Research
171(3):811-829, 2006), use exactly that pairing, with annealing guiding the search and
the LP compaction and separation models *generating the neighbourhoods*, and report an
average improvement of `8.84%` over previously published results.
The Torquato and Jiao adaptive shrinking cell scheme is worth noting for the contrast:
it moves only one particle at a time, and its single collective move is the strain of
the simulation cell itself.

**The one fully specified Metropolis annealer for tilted unit squares** is Blair,
Santangelo and Machta, *Packing Squares in a Torus*,
[arXiv:1110.5348](https://arxiv.org/abs/1110.5348), 2012, retained at
`packing/resources/papers/blair-santangelo-machta-2012-packing-squares-in-a-torus.pdf`.
The container is a torus rather than a square, so it sets no record for `s(n)`, but its
design is instructive because every choice is stated: translation, rotation and
system-volume moves at probabilities `0.495`, `0.495` and `0.01`; a move producing any
overlap is rejected outright, and translations and rotations are otherwise accepted
unconditionally; the box is held fixed and the *squares are rescaled* to change density,
so the annealed parameter is **pressure, not temperature**, run from `beta P = 0.01` to
`3000` in constant steps of inverse pressure; step sizes auto-tuned to a `0.4`
acceptance ratio. It reached `n <= 27` with 1,000 repeats per `n`. Note what it shares
with Gensane and with Squarl and not with `sqsearch`: hard rejection instead of a
penalty, and an inflation-style density parameter instead of an enclosing side.

**Inference, and it is the sharpest technical point in this document.** There is a
structural reason the first two are not enough, and it is visible in the objective.
`required_side(c) = max(hix - lox, hiy - loy)` (`packing/sqsearch/src/geom.rs`). Only
the squares attaining the extremes of the binding span can *reduce* it: generically two
squares, four when both spans are tight, which is the situation at any good packing.
Every other single-square translation leaves the side term **exactly** unchanged, so its
energy change comes only from the overlap term, and once `lambda` has ramped, any move
that creates overlap is rejected outright.
So at `n = 17` roughly four proposals in seventeen can improve the objective at all; at
`n = 51` roughly four in fifty-one; at `n = 100` roughly four in a hundred.
The remainder are a random walk on a plateau, bounded by rejection.

That is a precise account of the failure recorded in exp-011, where the annealer
returned exactly `5.0` at `n = 17` on five seeds of five.
The grid is jammed, only the corner squares carry any side gradient, and moving one
outward raises the objective while moving one inward is refused.

Both of the formulations that work fix this in the same way.
Inflation replaces a max over two to four extremes with a min over the *active contact
set*, which at a jammed configuration has size on the order of `2n`, so every square
participates in the objective.
Wall pressure adds the same information as a force term.
Contract-act-re-expand makes the reward of a move equal to the space it opened anywhere
in the packing.

**Symmetry and angle classes.** Several independent lines of evidence say the angle
vector is low-dimensional at a record.
DS7 describes `n = 17` as the smallest case whose best packing uses three different
angles, and the `n = 29` packing as using at least six; exp-012 measured exactly six
numerical classes at `n = 29` at tolerance `1e-80`, with the closest pair separated by
`0.296` degrees, insensitive to the clustering radius by about 89 orders of magnitude.
The `n = 55` record’s own SVG, read for this document, closes its exact system with a
Mathematica `FindRoot` in **seven unknowns for 55 squares**: the side, plus six free
angles named `a` through `f` alongside an axis-aligned class.
Squarl ties angles within `0.01` radians and optimises the tied parameters before
releasing them. The repository’s exp-006 found the same thing from the other direction:
constraining the eleven `n = 11` angles to two classes and golden-sectioning the shared
tilt reached the analytic optimum in **70 LP solves**, against 1,024 for free descent
over all eleven angles.
**Inference:** angle-class structure is the strongest available prior for this problem
and no part of `sqsearch` uses it.

**But symmetry must be a seed, never a constraint, and there is a measurement on both
sides.** For it: Oakley, Johnston and Wales, *Symmetrisation schemes for global
optimisation of atomic clusters* (Physical Chemistry Chemical Physics 15(11):3965-3976,
2013), report that allowing approximate point-group symmetry reduces the mean time to
locate the global minimum by **up to two orders of magnitude** on multi-funnel Lennard-
Jones clusters, with smaller gains on single-funnel ones.
That article is nominally hybrid open access but the publisher’s PDF returned HTTP 403
on 2026-09-08 and it is not retained; the attempt is in
`packing/resources/web/annealing-methods-audit-2026-09-08/`. Against it: Berthold, Kamp,
Mexi, Pokutta and Pólik’s May 2026 follow-up
([arXiv:2605.04850](https://arxiv.org/abs/2605.04850)) measured elementary
symmetry-breaking constraints on polygon and solid packing and found them **the worst
variant overall**, a median `2.178%` worse, strictly worse on 539 instances against
better on 2. And this problem supplies its own counterexamples: `n = 17` needs three
distinct angles and `n = 29` at least six.

The same paper supplies the verification protocol, and it is the right one to adopt:
they cleaned circle instances by enforcing the *conjectured* structure, symmetry,
axis-aligned roundings and touching constraints as equalities, re-solved the restricted
problem, and confirmed the same solution came back.
The pattern is to use the restriction to reach a candidate cheaply, then re-solve
unrestricted from that candidate and confirm it is not improved.
That converts a possibly lossy restriction into a seeding heuristic with a check.

**Step size should be adapted to an acceptance target, not left to the schedule.** Every
implementation that reports it does the same thing: the torus annealer tunes
translation, rotation and volume step sizes independently to an acceptance ratio of
`0.4`; the adaptive shrinking cell reduces the trial-move magnitude when acceptance
falls significantly below `50%`; Xu, Xiao and Amos’s annealer for weighted polygon
packing ([arXiv:0809.5005](https://arxiv.org/abs/0809.5005), retained at
`packing/resources/papers/xu-xiao-amos-2008-simulated-annealing-weighted-polygon-packing.pdf`)
shrinks the neighbourhood from `±0.55 R0` in position and `±0.55 pi` in orientation to
`0.05` of that range over the run.
**Inference:** in `sqsearch` the move scale and the Metropolis temperature are the same
variable, so the acceptance ratio cannot be targeted independently of the schedule.
Separating them is a small change with a well-attested payoff.

**What this document could not establish.** Two gaps, and they are different sizes.

The smaller one: no study was found that crosses several cooling schedules with several
move sets factorially and reports the interaction, on any problem.
All the evidence above, on both sides, is one factor at a time.
It is consistent and lopsided, but it is not a designed experiment.

The larger one: **no source was found that ablates move families against each other on
squares in a square with matched budgets.** Move-set ablations exist for circles and
spheres (Lai et al., Grosso et al.)
and for graph problems (Johnson et al.), but not for this problem.
The most modern nesting heuristic, `sparrow`
([arXiv:2509.13329](https://arxiv.org/abs/2509.13329), September 2025, retained at
`packing/resources/papers/gardeyn-vandenberghe-wauters-2025-sparrow-2d-nesting.pdf`),
which matched or beat every previous best across 13 benchmarks and abandons cooling
schedules entirely in favour of guided local search with adaptive weights, explicitly
declines to publish a per-component ablation.
So the claim that the move set dominates the schedule *on square packing specifically*
rests on the structural argument above and on three independent implementations adding
the same move families.
Nobody has measured it here, this repository included.
That is exactly the gap section 8 proposes to close.

## 5. What This Repository Has Already Measured

These are the constraints any answer has to respect.
All are recorded in `packing/campaign/`.

- **exp-001** (2026-08-22, `sqsearch` defaults, 12 billion moves in 302 seconds on an M1
  Pro): at `n = 10` the best of five seeds was `3.7075262001`, a gap of `4.19e-04`; at
  `n = 11`, `3.9144165418`, a gap of `3.73e-02`; at `n = 12`, exactly `4.0`. The five
  `n = 11` seeds spanned `[3.9144, 3.9361]`, a band five times narrower than the
  remaining distance to Trump.
  H-016 refuted. The report’s own reading is that `n = 10` is a polish failure and
  `n = 11` an exploration failure, and that one criterion could not tell them apart.
- **exp-011** (2026-08-23, `n = 17`, five seeds, `1e8` moves per chain, eight chains):
  best `5.000000000000`, gap `+3.2447e-01`. The annealer returned the trivial grid on
  every seed. H-020 refuted.
- **exp-005 / H-018** (basin entry at `n = 11`): started from Trump’s exact
  configuration perturbed by uniform noise, zero of forty trials at `eps = 1e-3`
  returned within `1e-6`. The residual scaled approximately linearly with the
  perturbation and shrank with effort, which the artifact reads as incomplete
  convergence of the refiner rather than as evidence about basin width.
- **exp-006 / H-002** (LP-in-cell quench): the fixed-cell LP is exact, reproducing
  Trump’s side to `4.4e-16` when solved at his angles.
  As a quench on annealer output it gave 1.1x, 1.2x and 1.3x improvements at
  `n = 5, 10, 11` with overlapping control and candidate ranges, so no detectable
  effect. Its verdict: “the quench is a polisher, not a rescue.”
- **exp-006 / H-019** (the kink): walking the shared `n = 11` tilt off its optimum gives
  a response that is *linear on both sides*, with slopes `0.175` and `0.384`. The
  objective has a corner at the optimum where the active contact set changes.
  Finite-difference descent stalls five orders short, and Powell and Nelder-Mead both
  did worse than plain descent.
- **H-012** (record basins are rare) is registered, load-bearing for the whole
  cartography programme, and **not yet measured**. Ellsworth’s `4 / 3004` is the nearest
  external analogue, under a different proposer, quench and equivalence relation.
- **Parked in `ideas.md`:** the fixed-side shrink-and-re-anneal outer loop was built
  twice and abandoned, because the grid is exactly jammed and no local move escapes it;
  the squared overlap penalty was replaced by a linear one because its gradient dies as
  the overlap closes.

**Inference.** The two refutations are not the same failure and should never be quoted
together as “annealing does not work”.
`n = 10` says the refiner is weak.
`n = 17` says the proposer never leaves the starting basin.
Sections 7 and 8 address them separately.

## 6. The Owner’s Question, Split Four Ways

**Reproducing a known-best packing from a good starting point.** Solved, and not by
annealing. The fixed-cell LP already reproduces Trump’s side to `4.4e-16` (exp-006), and
Squarl’s deep polish reproduces Bidwell’s to `2e-9` from an archive state.
Given the arrangement, recovering the number is an LP plus an angle search over a
handful of classes. Nothing here is hard.

**Finding it cold at `n < 20`.** Partly reachable, and the honest boundary is around
`n = 16`. General-purpose global solvers match the record to `n = 16` and fail from
`n = 17` (Berthold et al.). A purpose-built 2026 system with contact-group moves, an
inflation formulation, an LP polish and a learned proposer spent a nine-hour production
search at `n = 17` and landed `2e-9` above the record.
Gensane and Ryckelynck recovered `n = 11` in 2005. **Inference:** `n = 11` and `n = 18`
and `n = 19` should be reachable cold by a good engine; `n = 17` is reachable but at the
edge of what anyone has demonstrated.

**Finding it cold at `20 <= n <= 100`.** This is where the owner’s expectation breaks,
and three independent lines of evidence break it.

The first is the record-holders' own statement that a plain annealer gets stuck just
above the trivial size, and that their working pipeline routes around it with a
different upstream algorithm, hand-picked states, and manual intervention at `n = 103`.

The second is Ellsworth’s basin statistics: `4 / 3004` at `n = 51` and roughly
`5 / 1893` at `n = 55`, on a tuned closed-source GPU annealer with 65,536 threads.
Those are record *rediscovery* rates for cases whose records that same engine set, so
they are an optimistic bound on rediscovering a record the engine has never seen.

The third is the clock.
Gensane and Ryckelynck’s `n = 29` packing stood as the record from 2004 to December
2025, through 21 years in which anyone could have pointed an annealer at it.
The 21 non-grid cases at `n <= 100` credited to hand construction have, so far as any
public source shows, never been rediscovered cold by any search program.

**Inference:** a well-built engine should recover a substantial fraction of the 36
non-grid cases, probably most of the larger-margin ones, at a cost measured in thousands
of refined local optima per case.
“All 36” is not supported by anything.
“All 100” is a category error, since 64 of them are the grid.

**Proving optimality.** Annealing cannot do this and no amount of budget changes that.
A search returns a feasible packing, which is an upper bound.
The repository’s own frontier makes the distinction load-bearing: `n <= 100` has 65 open
cases, and closing one needs a matching lower bound, which is the proof lane’s problem
and unrelated to the search engine.
Even the exact algebraic value of a found packing is a separate step: the catalogue
flags 32 of 184 pictured packings as not yet analytically optimised.

## 7. What the Engine Should Look Like

A specification concrete enough to build.
Every choice names its evidence, and the guesses are marked.

**Formulation: inflation, not enclosing side.** Fix the container to the unit square,
carry a common square side `s`, and maximise `s`. Report `1/s` as the packing side.
*Evidence:* Gensane and Ryckelynck’s paper is built on this and it is what made squares
tractable; Squarl uses it; the structural argument in section 4 says why the enclosing-
side objective is sparse under single-square moves and the inflation objective is not.
This is the single highest-value change and it is a rewrite of `geom.rs`, not a tweak.

**Outer loop: monotonic basin hopping with an adaptive step, not a cooling schedule.**
From the incumbent local optimum, perturb every square at once, run the local solver to
convergence, accept only on improvement, and restart from a fresh scatter after a fixed
count of consecutive non-improving steps.
Adapt the perturbation size the way Gensane does: double it on success, halve it on
failure, and restore the saved configuration when a perturbation fails.
*Evidence:* this is Gensane’s algorithm 4 with a stronger local solver substituted for
his layer 2, and the same two-level shape is what Ellsworth, Squarl and the disk-packing
literature all converge on; the acceptance rule is the part every source treats as
incidental.

**Start the perturbation magnitude near Grosso’s value and expect a sharp optimum.**
Their sweep on circles put the best value at `0.8` in units of the object’s own scale,
with roughly a threefold difference in failure count between that and the neighbouring
values they tried. *Evidence:* published, on circles.
*Guess:* that the optimum for squares is near the same relative magnitude, since the
argument for it, preserve structure while leaving the basin, is geometric rather than
shape-specific.

**Carry two perturbation operators and switch between them adaptively.** One-shot
uniform perturbation, and Lai et al.'s sequential variant, a series of small
perturbations each followed by a very short local optimisation with decaying strength.
*Evidence:* on their benchmarks each operator was the sole winner on some instances and
had a zero success rate on others, and the adaptive hybrid did well on all of them.
This is the highest-value cheap idea found in the whole survey and it is
problem-agnostic.

**Keep a population in reserve, not as the default.** Single-path basin hopping is
usually enough and a population usually costs more than it returns, but a minority of
instances invert that completely: Grosso et al.'s `n = 31` went from 1 success in 50 to
9 in 10 when a population of 10 replaced a single path.
*Guess:* which `n` behave that way is not predictable in advance here either, so the
practical rule is to escalate to a population on any case the single path fails
repeatedly, rather than to run populations everywhere.

**Adapt every step size to an acceptance target rather than to the clock**, at roughly
`0.4` to `0.5`, and shrink the neighbourhood over the run.
*Evidence:* the torus annealer, the adaptive shrinking cell and the weighted-polygon
annealer all do this and all report the target.
This requires decoupling the move scale from the Metropolis temperature, which in
`sqsearch` are currently the same variable.

**Use symmetry and angle classes as seed generators with an unrestricted check, never as
hard constraints.** Run the class-restricted search to get a candidate cheaply, then
re-solve unrestricted from that candidate and confirm it is not improved.
*Evidence:* symmetrisation buys up to two orders of magnitude on multi-funnel landscapes
(Oakley et al.), hard symmetry-breaking measurably degrades packing solutions on 539
instances against 2 (Berthold et al.
2026), the seed-then-verify protocol is theirs, and this problem’s own records at
`n = 17` and `n = 29` are not symmetric enough to survive a hard restriction.

**A second stage is not optional, and the order matters.** Schadt’s `n = 55` record came
from a GPU annealer started on a cherry-picked state produced by his Gensane
reimplementation, because the annealer alone sticks just above the trivial size.
If this repository keeps an annealer at all, it belongs *after* a greedy inflation
stage, not before it, and the annealer’s job is to improve a state that is already off
the grid.

**Move set, in proposal-probability order.**

1. Simultaneous perturbation of all squares at scale `eps` (Gensane layer 3).
2. Single-square translate and rotate, with the contract-act-re-expand wrapper so the
   move is scored by the room it creates.
3. Contact-group move: identify a set of squares in mutual contact, move it rigidly.
4. Separator-boundary move: flip which separating axis an ambiguous pair uses, which
   changes the combinatorial cell without changing the geometry much.
5. Swap: exchange the poses of two squares.
   Cheap, and it is the operator that attacks combinatorial difficulty, which continuous
   moves cannot reach. Grosso et al.
   found swap beat a continuous displacement on four of five unequal-circle instances,
   losing only on the one instance whose circles were mostly identical, and under free
   rotation squares of equal size still differ in orientation, so a swap is not a no-op
   here.
6. Remove-and-reinsert: drop the square with the largest local slack and reinsert it in
   the largest hole.
7. Neighbour transfer: seed from `n-1` or `n+1` records with a square added or removed
   and some straightened.
   *Evidence:* this is exactly the catalogue’s recorded seeding practice, and it is
   already registered here as H-004, unbuilt.

**Local solver: fixed-angle LP with a bounded cell beam, plus an angle-class search.**
At fixed angles and a fixed directed separating axis per pair, the problem in the `2n`
centres and `s` is a linear program.
Choose each pair’s branch by largest current margin; call a pair ambiguous when its two
best margins are within a declared tolerance and beam over a bounded number of ambiguous
pairs. Above that, tie angles into classes by a declared radius, snap near-axis angles
exactly, optimise the class parameters, then release.
*Evidence:* Squarl’s `deep-polishing.md`
(`packing/resources/web/squarl-n17-2026/squarl-docs-deep-polishing.md`) specifies
precisely this and gives working tolerances (`5e-5` ambiguity, `0.002` snap, `0.01` tie,
96 clustered and 32 released evaluations); this repository’s exp-006 independently
validated the LP half to `4.4e-16` and measured the class-constrained angle search at 70
LP solves against 1,024. Two independent implementations arriving at the same
architecture is the strongest single piece of evidence in this document.

**Angle search must be kink-aware.** exp-006 measured a corner at the `n = 11` optimum
with slopes `0.175` and `0.384`, and found Powell and Nelder-Mead both worse than plain
descent there. Use golden section or a bracketing method on the class parameters, or a
subgradient method, and do not use a smooth local model.
*Evidence:* measured here, exp-006 and H-019.

**Penalty and repair.** Inside the inflation formulation overlap is *forbidden* rather
than penalised, because the contract step guarantees legality by construction.
Keep the linear penalty only if a penalised variant is retained for comparison; the
reason for linear over squared is already recorded here and stands.
*Evidence:* Gensane’s random walking rejects any overlapping move; Squarl’s every action
“re-expands to a legal measured packing”.

**Precision.** Search in `float32`, refine in `float64`, promote in exact arithmetic.
*Evidence:* Schadt’s own note says the `n = 29` record was found in C++ `float` and
relaxed afterward with Boost; Squarl keeps a float32 rollout path and a float64 deep
polish, and requires two agreeing replays before accepting an improvement.

**Parallelism: replicas with exchange, not a domain decomposition, and the exchanged
parameter is pressure.** Run many independent chains, each cheap, and exchange
configurations between neighbouring levels of an inflation-pressure ladder.
*Evidence:* this is the only parallel scheme found that is *currently producing* packing
records, at 108 new maximal disk packings for `N = 300` to `720`, with the Packomania
maintainer as a coauthor; and hard particles are athermal, so pressure rather than
temperature is the parameter with anything to exchange.
It is also a small step from what Ellsworth already runs, since his 65,536 GPU threads
are already independent replicas.

**Do not expect the physics engines’ GPU speedups to apply.** HOOMD-blue’s hard-particle
Monte Carlo (Anderson, Irrgang and Glotzer, retained at
`packing/resources/papers/anderson-irrgang-glotzer-2016-scalable-metropolis-hard-shapes.pdf`)
is the obvious library to borrow from, and its polygon overlap kernels and rotation
moves are worth borrowing, but its parallelism is domain decomposition and its own
socket-to-socket figures are modest, around `1.8x` to `3.1x` on polygons and polyhedra,
with a stated minimum practical system size in the tens of thousands of particles.
At `n = 20` to `500` squares there is nothing to decompose.
*Inference:* this reframes the repository’s own parked GPU result.
`ideas.md` measured 2.5M evaluations per second on MPS against 18 to 20M on CPU cores
and concluded the kernel was launch-bound and bandwidth-bound.
That is the right measurement of the wrong thing: the parallelism worth having here is
over *replicas*, which is embarrassingly parallel and needs no arithmetic intensity per
configuration.

**Keep an archive, because that is what turns a search into a campaign.** Store refined
local optima classified by contact structure.
Ellsworth’s statistics files are an archive report, and Squarl’s production runs draw
most of their proposals from an archive of its own previous optima.
*Evidence:* published in both cases.

**Budget, denominated correctly.** Per case, expect to need on the order of `10^3`
refined and classified local optima before a record-quality one appears at `n` near 50,
by direct analogy with `4 / 3004` and `5 / 1893`. Budget in refined optima, not in
moves. A budget in moves is uninformative because the move cost changes by orders of
magnitude between the raw proposer and the LP polish.

**What this specification does not claim.** It does not claim to reach `n = 100`. It
claims to close the distance between `sqsearch` and the engines that have actually set
records, and the honest prediction is that it recovers many of the 36 non-grid cases and
not all of them.

## 8. What Is Cheap to Try Here First

The specification in section 7 is a rewrite.
The question is what single change to the existing `sqsearch` has the best expected
return, and section 4 answers it: the objective is sparse under the current move set,
and the cheapest repair for that is Gensane’s layer 3.

**A simultaneous perturbation move costs about twenty lines.** `search.rs` already has
`perturb`, written for the basin-entry mode, which displaces every pose by uniform noise
of size `eps`. It is not on the move menu for ordinary search.
Adding it as a proposal with probability `p_perturb`, scored against the same energy and
accepted by the same rule, changes no data structure and no interface.
It is strictly the cheapest structural change available.

**The published payoff for exactly this move is large.** Gensane measured it on spheres
in a cube, where a particle has three degrees of freedom, as a freely rotating square in
the plane does. At `n = 12`, ten thousand plain billiard runs gave six digits; adding
perturbation gave six *more* digits at a small fraction of the effort.
At `n = 21`, plain runs gave two digits and perturbation gave twelve.
At `n = 24` the best packing arrived at roughly a tenth of the cost.
His stated conclusion is that plain billiards suffices for disks in a square but
perturbation is indispensable in three dimensions.
No comparable measurement exists for squares, which is why this is a hypothesis and not
a plan.

Stated as a hypothesis in this campaign’s form:

> **H-XXX. A simultaneous all-square perturbation move rescues the cases where
> single-square moves cannot leave the grid.**
> 
> *Claim.* With a simultaneous perturbation proposal added at probability
> `p_perturb = 0.05`, and every other parameter at its `sqsearch` default, the median
> best side over five seeds is at least `0.01` lower than the paired single-square-only
> control at equal move budget, on at least three of the five cells
> `n in {11, 17, 19, 26, 27}`.
> 
> *Regime.* `sqsearch` at the commit under test, `f64` screening, eight chains, `1e8`
> moves per chain, seeds 1 to 5, the same host, control and candidate interleaved.
> 
> *Criterion.* Paired, metric = paired difference in median best side, threshold `0.01`,
> direction = candidate lower.
> 
> *Kill.* Fewer than three of five cells improve by `0.01`. That result would say the
> plateau diagnosis is wrong or that the perturbation is not the binding constraint, and
> it would move the next attempt to the inflation rewrite rather than to more moves.

The cell set is chosen for stratification rather than for difficulty.
`n = 11` and `n = 17` are the two cells this repository has already refuted, so they are
the calibration points.
`n = 26` and `n = 27` beat the grid by `0.379` and `0.293`, the large-margin end where a
search has the most room to show an effect.
`n = 19` beats it by `0.114`, the small-margin end.
All five are non-grid, so none of them can be passed by returning the incumbent.

**One change at a time, which is this campaign’s own discipline.** H-031 already states
the rule: do not combine several move families and a new schedule into a proposer bundle
nobody can interpret afterwards.
Three further changes are each about as cheap as the first, and each deserves its own
paired round rather than being folded in.

- **Decouple the move scale from the Metropolis temperature and target an acceptance
  ratio.** In `search.rs` the single variable `temperature` is both the proposal scale
  in length units and the denominator of the Metropolis exponential, so acceptance
  cannot be targeted independently of the schedule.
  Every implementation surveyed that reports a step-size rule tunes it to an acceptance
  ratio near `0.4` to `0.5`. This is a few lines and its own experiment.
- **A wall-pressure term**: a small penalty proportional to each square’s distance from
  the container boundary, which gives every square a nonzero derivative of the objective
  without requiring the inflation rewrite.
  A partial substitute for section 7’s formulation change, and ablatable against it.
- **Neighbour-transfer seeding**, already registered as H-004 with an instrument marked
  not built, and the one seeding practice the catalogue explicitly records the
  record-holders using.

Beyond those, the next thing worth building is not another move.
It is the **replica exchange over a pressure ladder** of section 3, because it is the
one scheme in this survey that is currently producing packing records, and because the
repository’s parked GPU measurement was of the wrong axis of parallelism.

## Key Insights

- **“Solve to `n = 100`” is 36 cases, not 100.** Sixty-four have the grid as their best
  known packing and `sqsearch` returns it by construction.
  Thirty-one of those 64 are open, and 18 of the 31 sit in a band where no grid has ever
  been beaten at any `n` to 324, so failing to beat them is probably correct behaviour.
- **Twenty-one of the 36 were found by hand.** Annealing is credited with 10. The claim
  that a search program “should” find all of them is not supported by the record of
  which program found which.
- **The record-holders say a plain annealer gets stuck just above the trivial size.**
  That is the exp-011 failure exactly, diagnosed by the people who set the records, and
  their fix is a different upstream algorithm and a hand-picked starting state rather
  than a better schedule.
- **The first algorithm that worked here was not an annealer.** Gensane and Ryckelynck’s
  method accepts strictly greedily, has no temperature, and escapes by perturbing every
  square at once. Its `n = 29` record stood for 21 years.
- **The formulation is the bug, not the schedule.** `required_side` is a max over two to
  four extreme squares, so a single-square move is a no-op on the objective for most
  squares. Inflation, wall pressure and contract-act-re-expand all fix the same defect,
  and all three are used by systems that get close.
- **Two independent implementations converged on the same architecture:** fixed-angle LP
  over all centres and the side, with a per-pair directed separating axis, wrapped in an
  angle-class tie-and-release search.
  Squarl built it; this repository’s exp-006 validated both halves without knowing about
  it.
- **Annealing is not the weak link, and the tidy story is wrong.** No matched-budget
  head-to-head of basin hopping against annealing on a continuous packing problem was
  found; where both were later measured on the same 30 contest instances, population
  basin hopping lost every non-tie while the annealer tied 7 and won 3. The acceptance
  rule is not what separates these methods.
- **The annealing-family method currently setting packing records is replica exchange
  over a pressure ladder**, not a cooling schedule: 108 new maximal disk packings at
  `N = 300` to `720` in 2024, with Packomania’s maintainer as a coauthor.
  Hard particles are athermal, so pressure is the parameter worth exchanging, and
  Ellsworth’s 65,536 GPU threads are already replicas without the exchange.
- **The perturbation operator is what swings the result, and it is measurable.** On
  circles and spheres, changing only the perturbation moved success rate between `0%`
  and `100%` on the same instances (Lai et al.
  2023); on graph colouring, changing only the neighbourhood bought two whole colours at
  equal time (Johnson et al.
  part II); on cooling schedules, the same authors’ Observations 4 and 5 found nothing
  worth having.
- **Multistart is the wrong shape and the count says why.** Fifty thousand random-start
  local searches on circles produced about sixteen thousand *distinct* local minima by
  `n = 40`. Restarting harder is not a plan.
- **The right unit of work is a refined local optimum, and the right rate is basins per
  record.** Ellsworth’s `4 / 3004` at `n = 51` is the only published measurement of this
  quantity for this problem, and it is the number any budget argument has to survive.
- **Search precision and certification precision are different questions.** The record
  engine searches in `float32` and relaxes afterwards, by its author’s own statement, so
  the `float32` objection parked against a GPU lane in `ideas.md` does not apply to the
  search stage.
- **Annealing cannot prove anything.** Sixty-five of the hundred cases at `n <= 100` are
  open, and closing one needs a lower bound.

## Limits

- No head-to-head comparison of annealing against anything on squares in a square was
  found, published or in the retained archive.
  Section 3 is measured on circles, disks and spheres and transfers to squares by
  inference. The one head-to-head it does report is on *unequal* circles in a circle, is
  a by-product of a third method’s comparison table rather than a controlled experiment,
  and equalises budget only loosely.
- The replica-exchange results are read from abstracts and search results.
  The 2024 Journal of Chemical Physics paper and its 2026 successor are paywalled, so
  the replica count, the pressure ladder and the cost per record are not in hand.
  That matters, because those are exactly the numbers a plan would need.
  Both were attempted again on 2026-09-08 and both failed;
  `packing/resources/web/annealing-methods-audit-2026-09-08/` records the attempts, so
  the next agent inherits a checked obstacle rather than a guess.
  The one predecessor in that line that *is* open, Odriozola’s pressure-exchange paper,
  is now retained.
- No factorial study crossing cooling schedules with move sets was found on any problem.
  Every result cited in sections 3 and 4, on both sides of the question, varies one
  factor at a time.
- Two primary sources could not be read directly and are reported from their abstracts
  and from citing work: Gensane and Ryckelynck 2005, which is paywalled and whose
  author’s page is gone, and Gomes and Oliveira 2006. The Gensane algorithm is
  reconstructed from his open companion paper on spheres, which states the same four
  procedures, so the algorithm family is safe even though the square-specific inflation
  computation is not in hand.
- The Squarl figures are read from that project’s own documentation, now retained at
  `packing/resources/web/squarl-n17-2026/` at a pinned commit.
  Nothing in them has been replayed here, and the question of whether its `n = 17`
  archive reached Bidwell’s arrangement cold is not settled by its documents.
- Ellsworth’s basin statistics are two cases on one GPU with one tuned engine.
  They are the best data of their kind and they are not a portable prediction.
- The census in section 1 reads the repository’s own frontier register, which is derived
  from the catalogue. Its `construction_method` field carries `unknown` for 2 of the 36
  non-grid cases at `n <= 100` and for 37 cases overall to `n = 324`, so the method
  counts are lower bounds.
- The structural argument about `required_side` in section 4 is an analytic property of
  the objective, not a measurement.
  It predicts a specific plateau statistic that no experiment here has yet measured, and
  section 8’s hypothesis is the cheapest way to test the prediction rather than the
  argument.
- Joost de Winter’s August 2026 report claiming improvements at `n = 68, 126, 206` could
  not be retrieved (see `packing/resources/web/de-winter-improved-packings-2026/`), so
  its method is unknown and it is not counted anywhere above.

## References

Every source below that this repository holds names its local path.
The retrieval receipts for the fifteen papers and the one repository added on
2026-09-08, the readings checked against those bytes, and the open-access verdict on
every source that could not be retrieved, are in
[the annealing methods audit packet](../../../packing/resources/web/annealing-methods-audit-2026-09-08/README.md).
A source with no local path is one the archive does not hold, and the packet says why.

- [Erich Friedman, *Packing Unit Squares in Squares: A Survey and New Results*, Electronic Journal of Combinatorics DS7 version 5, 2009](https://www.combinatorics.org/files/Surveys/ds7/ds7v5-2009/ds7-2009.html)
  (retained at `packing/resources/web/friedman-ds7-survey-2009-html.md`)
- [Thierry Gensane and Philippe Ryckelynck, *Improved Dense Packings of Congruent Squares in a Square*, Discrete and Computational Geometry 34(1), 97-109, 2005](https://doi.org/10.1007/s00454-004-1129-z)
  (the landing page is paywalled; Springer serves the PDF openly and the archive has
  retained it since 2026-08-22 at
  `packing/resources/papers/gensane-ryckelynck-2005-improved-dense-packings.pdf`,
  raw-only. The algorithm is reconstructed from the companion paper below, which states
  the four procedures verbatim)
- [Thierry Gensane, *Dense Packings of Equal Spheres in a Cube*, Electronic Journal of Combinatorics 11 (2004) #R33](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v11i1r33)
  (open access; states the four procedures verbatim; retained at
  `packing/resources/papers/gensane-2004-dense-packings-equal-spheres-cube.pdf`)
- [E. Blair, C. Santangelo and J. Machta, *Packing Squares in a Torus*, arXiv:1110.5348, 2012](https://arxiv.org/abs/1110.5348)
  (retained at
  `packing/resources/papers/blair-santangelo-machta-2012-packing-squares-in-a-torus.pdf`)
- [The `n = 55` record SVG and its provenance comment](https://kingbird.myphotos.cc/packing/square-55.svg)
  (fetched 2026-09-08)
- [David Ellsworth, *Squares in Squares* catalogue](https://kingbird.myphotos.cc/packing/squares_in_squares.html)
  (retained, archived 2026-08-22)
- [Ellsworth’s `n = 51` run statistics](https://kingbird.myphotos.cc/packing/square-51.stats.txt)
  and
  [`n = 55` run statistics](https://kingbird.myphotos.cc/packing/square-55.stats.txt)
  (retained 2026-08-31)
- [Thomas Schadt, `Squares-packing_S-29-_New-Record`, MIT, December 2025](https://github.com/BalthasarStrauss/Squares-packing_S-29-_New-Record)
  (retained at `packing/resources/web/schadt-s29-2025/`)
- [Sam Burns, `squarl`, August 2026](https://github.com/sam-bee/squarl), and
  [the `n = 17` near-record write-up](https://sam-burns.com/posts/n17-square-packing-near-record-arrangement/)
  (figures retained 2026-09-07 at
  `packing/resources/web/burns-n17-series-addendum-2026-09-07/`; the repository’s own
  documentation retained 2026-09-08 at `packing/resources/web/squarl-n17-2026/`, pinned
  at commit `016dff98`)
- [Timo Berthold, Dominik Kamp, Gioni Mexi, Sebastian Pokutta and Imre Pólik, *Global Optimization for Combinatorial Geometry Problems Revisited in the Era of LLMs*, arXiv:2601.05943, 9 January 2026](https://arxiv.org/abs/2601.05943),
  and the May 2026 follow-up [arXiv:2605.04850](https://arxiv.org/abs/2605.04850) with
  the symmetry-breaking measurement (both retained at
  `packing/resources/papers/berthold-kamp-mexi-pokutta-polik-2026-global-optimization-combinatorial-geometry.pdf`
  and
  `packing/resources/papers/berthold-kamp-mexi-pokutta-polik-2026-out-of-the-box-packing-problems.pdf`)
- [David S. Johnson, Cecilia R. Aragon, Lyle A. McGeoch and Catherine Schevon, *Optimization by Simulated Annealing: An Experimental Evaluation*, Operations Research 37(6) 1989 (part I)](https://faculty.washington.edu/aragon/pubs/annealing-pt1.pdf)
  and
  [39(3) 1991 (part II)](https://faculty.washington.edu/aragon/pubs/annealing-pt2.pdf)
  (retained at
  `packing/resources/papers/johnson-aragon-mcgeoch-schevon-1989-annealing-part-i.pdf`
  and `...-1991-annealing-part-ii.pdf`)
- [Bernardetta Addis, Marco Locatelli and Fabio Schoen, *Disk Packing in a Square: A New Global Optimization Approach*, INFORMS Journal on Computing 20(4), 2008](http://www.optimization-online.org/DB_FILE/2005/10/1229.pdf)
  (retained at
  `packing/resources/papers/addis-locatelli-schoen-2008-disk-packing-square.pdf`)
- [Andrea Grosso, Abdulmajeed Jamali, Marco Locatelli and Fabio Schoen, *Solving the problem of packing equal and unequal circles in a circular container*, Journal of Global Optimization 47, 2010](https://optimization-online.org/wp-content/uploads/2008/06/1999.pdf)
  (retained at
  `packing/resources/papers/grosso-jamali-locatelli-schoen-2010-packing-equal-unequal-circles.pdf`)
- [Xiangjing Lai, Jin-Kao Hao, Renbin Xiao and Fred Glover, *Perturbation-based thresholding search for packing equal circles and spheres*, INFORMS Journal on Computing, 2023](https://leria-info.univ-angers.fr/~jinkao.hao/papers/LaietalJOC2023.pdf)
  (retained at
  `packing/resources/papers/lai-hao-xiao-glover-2023-perturbation-thresholding-search.pdf`)
- Zhengyu Li and Victor Milenkovic, *Compaction and separation algorithms for non-convex
  polygons and their applications*, European Journal of Operational Research 84, 1995;
  Victor Milenkovic, *Rotational polygon overlap minimization and compaction*,
  Computational Geometry 10(4), 1998 (both Elsevier, not retained)
- José F. Oliveira and A. Miguel Gomes, *Solving irregular strip packing problems by
  hybridising simulated annealing and linear programming*, European Journal of
  Operational Research 171(3), 2006 (closed access; the check is in the audit packet)
- [Jelle Gardeyn, Greet Vanden Berghe and Tony Wauters, *An open-source heuristic to reboot 2D nesting research* (`sparrow`), arXiv:2509.13329, September 2025](https://arxiv.org/abs/2509.13329)
  (retained at
  `packing/resources/papers/gardeyn-vandenberghe-wauters-2025-sparrow-2d-nesting.pdf`)
- [Fan Ye, Wenqi Huang and Zhipeng Lü, *Iterated Tabu Search Algorithm for Packing Unequal Circles in a Circle*, arXiv:1306.0694, 2013](https://arxiv.org/abs/1306.0694)
  (the annealing versus basin-hopping table; retained at
  `packing/resources/papers/ye-huang-lu-2013-iterated-tabu-search-unequal-circles.pdf`,
  and Table 3 was re-read against those bytes for the audit packet)
- André Müller, Johannes J. Schneider and Elmar Schömer, *Packing a multidisperse system
  of hard disks in a circular environment*, Physical Review E 79:021102, 2009 (closed
  access, no preprint; not retained, and everything claimed about it here comes from Ye,
  Huang and Lü’s retained table)
- Gerardo Odriozola, *Replica Exchange Monte Carlo applied to Hard Spheres*, Journal of
  Chemical Physics 131:144107, 2009,
  [preprint arXiv:1010.2923](https://arxiv.org/abs/1010.2923) (pressure rather than
  temperature as the exchanged parameter; retained at
  `packing/resources/papers/odriozola-2009-replica-exchange-hard-spheres.pdf`);
  [Eduardo Basurto, Péter Gurin, Eckard Specht and Gerardo Odriozola, *Searching for the maximal packing fraction of hard disks confined by a circular cavity through replica exchange / event-chain Monte Carlo*, Journal of Chemical Physics 161(4):044110, 2024](https://doi.org/10.1063/5.0219006)
  (nominally hybrid open access, HTTP 403 on 2026-09-08, not retained); and the
  out-of-equilibrium successor, Eduardo Basurto, Péter Gurin, Szabolcs Varga and Gerardo
  Odriozola, *Densest packings and accelerated equilibration of hard body systems via
  out-of-equilibrium replica exchange Monte Carlo method*, Computer Physics
  Communications 320:109990, 2026
  ([doi:10.1016/j.cpc.2025.109990](https://doi.org/10.1016/j.cpc.2025.109990); closed
  access, not retained)
- [Yi-Chun Xu, Ren-Bin Xiao and Martyn Amos, *Simulated Annealing for Weighted Polygon Packing*, arXiv:0809.5005, 2008](https://arxiv.org/abs/0809.5005)
  (retained at
  `packing/resources/papers/xu-xiao-amos-2008-simulated-annealing-weighted-polygon-packing.pdf`)
- Nicholas Oakley, Roy L. Johnston and David J. Wales, *Symmetrisation schemes for
  global optimisation of atomic clusters*, Physical Chemistry Chemical Physics 15(11),
  2013 ([doi:10.1039/c3cp44332a](https://doi.org/10.1039/c3cp44332a); nominally hybrid
  open access, HTTP 403 on 2026-09-08, not retained)
- [The annealing methods source audit, 2026-09-08](../../../packing/resources/web/annealing-methods-audit-2026-09-08/README.md):
  the query receipts, the fifteen-paper acquisition manifest, the readings checked
  against the retained bytes, the screened-out adjacent problems, and every attempted
  and failed retrieval above
- [Joshua A. Anderson, M. Eric Irrgang and Sharon C. Glotzer, HOOMD-blue hard-particle Monte Carlo, arXiv:1509.04692, 2016](https://arxiv.org/abs/1509.04692)
  (retained at
  `packing/resources/papers/anderson-irrgang-glotzer-2016-scalable-metropolis-hard-shapes.pdf`)
- Andrea Ninarello, Ludovic Berthier and Daniele Coslovich, *Models and algorithms for
  the next generation of glass transition studies*, Physical Review X 7:021039, 2017
  (retained at
  `packing/resources/papers/ninarello-berthier-coslovich-2017-next-generation-glass-transition.pdf`)
- [Algorithms and tooling for square packing](research-2026-08-22-square-packing-algorithms-and-tooling.md)
- [A search philosophy for square packing](research-2026-08-23-search-philosophy-and-landscape-cartography.md)
- Campaign artifacts: exp-001, exp-005, exp-006, exp-011, exp-012; hypotheses H-002,
  H-004, H-012, H-016, H-017, H-018, H-019, H-020, H-024, H-031; exploration X-009

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
