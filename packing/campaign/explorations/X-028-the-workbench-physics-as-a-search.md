---
title: X-028 — the workbench's blind physics, measured as a search
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-028
  title: The Workbench's Blind Physics, Measured as a Search
  date: '2026-09-12'
  author: Claude Opus 5, unattended
  campaign: packing.squares
  brief: >-
    The workbench's animation runs a contact-and-jiggle simulation that, in blind mode, is
    told nothing about where the squares are meant to end up. Nobody had measured whether
    it can rediscover a known-best packing. This exploration builds the instrument, takes
    the baseline, and reports what the first 80,000 trials say about what the method is.
  sources:
  - packing/atlas/known-best/video/spikes/v2-transitions/assets/workbench.js
  - packing/devtools/bench_annealing.py
  - docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
  proposes: []
---
# X-028: The Workbench’s Blind Physics, Measured as a Search

The workbench draws each step of the atlas by simulating it.
In its **blind** mode the simulation is told nothing about the target: it starts from
the packing of `n` in a container inflated past the record, drops the new square into
the emptiest cell of a coarse grid, and closes the walls in with contacts, walls and a
decaying jiggle.

That is a search. It had never been measured as one, and this exploration is what
measuring it found.

## 1. There Was No Seed, So There Was No Rate

The first finding came before any measurement and reshaped what could be measured.

Every generator on the page was seeded from `n` alone — the cached simulator’s shake
from `p.n`, the live optimiser’s from `N + INITIALS.indexOf(kind) * 7919`, the random
start’s poses from `N`. So a given `n` and parameter set had **exactly one blind
trial**, and it was the same trial every time.

That is the right property for an animation: it is what makes a capture reproducible
across builds. It also makes a success *rate* impossible, because a rate over one sample
is 0 or 1.

`setSeed` now folds a run seed into all three generators, defaulting to zero, which
mixes to nothing — the page’s whole checker suite passes unchanged, including the one
that compares free-run misses against values recorded before seeds existed.

## 2. The Method Closes About Half the Gap, Wherever It Is Pointed

The baseline: 1,200 trials, six `n`, four seconds.

**No trial at any `n` came within 0.1% of the record.**

The apparent structure in the raw numbers — `n = 11` landing 0.95% out while `n = 17`
landed 4.6% out — is an artefact of the metric.
Raw excess cannot be compared across `n`, because the room between the record and the
trivial grid `ceil(sqrt(n))` differs at every one: at `n = 29` the grid is 1.1% above
the record, at `n = 5` it is 10.8%. The same excess means opposite things.

Normalised — the fraction of the record-to-grid gap a run closes, 1 for the record and 0
for the grid — the picture is flat:

| n | gap % | excess % | closed |
| ---: | ---: | ---: | ---: |
| 5 | 10.82 | 5.686 | 0.474 |
| 10 | 7.90 | 4.230 | 0.465 |
| 11 | 3.17 | 0.947 | 0.701 |
| 17 | 6.94 | 4.617 | 0.335 |
| 26 | 6.74 | 4.528 | 0.328 |
| 29 | 1.12 | 0.475 | 0.574 |

Median 0.469 over all 1,200 trials.
**The method closes about half the gap wherever it is pointed**; `n = 11` and `n = 29`
only looked easy because their gaps are small.

This retires the framing the campaign started with.
There is no difficulty gradient across these `n` to explain, so a hypothesis about which
arrangements are hard for the annealing is answering a question the data does not pose.

## 3. The Value Is in the Tail, and the Shake Is What Buys It

A trial costs half a millisecond.
So the operational question is never what one run gives but what the best of a budget
gives — and nothing was reporting that.

80,000 trials at shake level 6:

| n | k=1 | k=10 | k=100 | k=1000 | k=10000 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 0.500 | 0.520 | 0.538 | **0.987** | 0.989 |
| 11 | 0.695 | 0.719 | 0.747 | 0.747 | 0.845 |
| 17 | 0.337 | 0.461 | 0.507 | 0.538 | 0.553 |
| 29 | 0.364 | 0.596 | 0.653 | 0.692 | 0.708 |

The median says the method closes half the gap.
The best of a thousand at `n = 5` closes **98.7%** of it.
Both are true, and only the second says what the search can reach.

**The shake trades the median for the tail, which is what a search does.** Median
`closed` falls monotonically with the dial — 0.712, 0.707, 0.696, 0.689, 0.539 at
`n = 11` for levels 0, 1, 3, 6, 10 — while best-of-k rises.
At level 0 the variance is exactly zero: best equals median equals worst at every `n`,
because the shake is the only randomness there is, so without it the seed does nothing.
At level 10 it overshoots — `n = 29`’s median `closed` is **−3.6**, a run ending worse
than the grid it started from.

### The shape of the `n = 5` tail is the interesting part

At level 6, two trials in a thousand land at 0.139% and 0.230% excess, and the next best
is 4.854%.

That is not a gradient.
It is a **second basin**, reached about twice in a thousand tries, and it is why
best-of-k has a step in it between k=100 and k=1000 rather than a slope.
A landscape with a rare good basin is a landscape where restarts are worth more than
schedule tuning — which is a claim the sweep can test rather than a conclusion this
exploration is entitled to.

## 4. What This Changes

- **The outcome metric is `closed`, not excess.** Excess stays in the record because it
  is what the page shows, but nothing may be compared across `n` with it.
- **Best-of-k is the report.** A median is a statement about one run and nobody runs
  one.
- **The shake dial is a search parameter, not a presentation one.** Its effect on the
  median is the opposite of its effect on the tail, and the workbench’s own default (3)
  is chosen for how the animation looks.

## 5. What Is Not Established

- **Nothing has reached a record.** The best result anywhere is 98.7% of the way at
  `n = 5`, which is 0.139% above `s(5)`. Whether the remaining 1.3% is reachable at all
  by this method is open.
- **Only one instrument.** These numbers are the workbench’s simulation, at its own step
  count and force law.
  They say nothing about the campaign’s Rust engine.
- **The regime is one machine, one build.** Every number here is from a single headless
  Chromium on one laptop, at the shipped beat.

## 6. What Follows

The hypotheses this compresses into are registered separately; the ones worth naming
here are whether the initial drop or the schedule decides the answer, whether the rare
basin at `n = 5` is reachable more often by restarting rather than shaking, and whether
the half-the-gap regularity survives `n` outside the six sampled.
