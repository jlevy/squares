# Feature: The Overnight Cartography Run

**Date:** 2026-08-23

**Author:** Claude (agent)

**Status:** Draft — the plan for the first long unattended session.

## Overview

The harness exists and the record is clean; what is missing is **work the harness can
do**. This spec plans one night: what gets built in the first hours, what runs in the
remaining ones, and what has to be true at each handover for the night to be worth
having.

It is deliberately narrow.
It does not re-plan the toolkit — that is
[the minimal-packing-toolkit spec](plan-2026-08-22-minimal-packing-toolkit.md), whose
Phases 1–4 already enumerate every remaining piece and already carry a bead each.
This spec is the *scheduling* layer over that one: which of those pieces this night
takes, in what order, and where the unattended half begins.

### The fact that shapes the whole plan

**Almost nothing that remains is overnight-shaped work.** `canonicalize`, `atlas`,
`descriptors`, `meter`, the multistart proposer — all of it is code an agent writes, not
compute a runner drains.
The campaign’s own effort record says the same thing from the other side: **275
agent-minutes against 16.4 wall-minutes** over its first ten rounds.

So a night that is purely unattended is a night that runs `H-017` and stops.
The plan below instead treats the night as **build, then run**, with a single explicit
handover — and it names what must hold at that handover, because that is the point where
nobody is watching any more.

## Goals

- **A queue with more work in it than the night can consume**, so the session ends on a
  budget rather than on `queue empty`.
- **One strategy carried to completion**, not five started.
- **A morning artifact that leads with what needs a human**, and a record that is
  gate-clean at every point in between.
- **Every step of the plan is a bead**, so the night is resumable by a different agent
  and the plan cannot drift from the work.

## Non-Goals

- **Beating a record.** Unchanged from the toolkit spec: this is calibration and
  measurement.
- **Finishing Phase 1.** The night takes the minimum of it that unblocks a census, and
  leaves `descriptors`, `meter` and the exact re-verification pass for later.
- **A fleet.** One runner, per the harness’s own refusal.
  Parallelism is not this night’s constraint; queue depth is.
- **Retiring `H-017`.** It stays registered and runnable, as the fallback if the build
  half overruns — see [Fallbacks](#fallbacks).

## The queue, and why it is one deep

`runner.py status` today:

```
queue: 1 runnable, 8 not
  -  H-001, H-011, H-012: instrument_ready is false
  -  H-002, H-016, H-018, H-020: already resolved
  -  H-019: already confirmed
  +  H-017 (priority 4) cells [11], 5 seeds, timebox 8h
```

Those three `instrument_ready: false` entries are the whole problem, and they are honest
rather than stale — each names an instrument that genuinely does not exist:

| Hypothesis | What it waits on | Bead |
| --- | --- | --- |
| [H-011](../../../../campaign/hypotheses/H-011-small-n-census.md) — a declared small-`n` landscape view is censusable | terminal-component identity, event archive, uncertainty estimator | `think-ogv7`, `think-0yo9`, `think-3szr` |
| [H-012](../../../../campaign/hypotheses/H-012-record-basins-are-rare.md) — record components are rare under a named regime | H-011’s machinery plus an explicit `n=11` cell and proposer comparison | `think-axbi`, `think-apwt` |
| [H-001](../../../../campaign/hypotheses/H-001-angle-class-reduction.md) — angle-class reduction beats free annealing | an angle-class proposer | `think-opzu` |

The dependency graph already encodes this, and `canonicalize` is the single unblocked
root:

```
think-zcx4  quench contract ─▶ think-0yo9  terminal components ─┐
think-3szr  identity calibration ───────────────────────────────┼─▶ think-ogv7  H-011
think-jxx8  named multistart baseline ──────────────────────────┘
think-apwt  proposer-conditioned measures ─────────────────────────▶ think-axbi  H-012
```

The queue is no longer one implementation bead deep.
The PR-description ambiguities are handover blockers because they determine what H-011
counts and what probability H-012 estimates.

## Revision, 2026-08-23: what building Half A found

Two of Half A’s three pieces landed — [`canonicalize`](../../../../sqpack/canonical.py)
and [`atlas`](../../../../sqpack/atlas.py) — and building them turned up a defect that
would have made the whole night worthless.

**[D-030](../../../../defects.md).** `quench_bracket` narrowed its angle search window
on a fixed schedule rather than on evidence, so a quench starting from a uniform random
configuration could never arrive: it descended until the window ran out, then crawled.
At `n = 5`, 11 of 12 cold starts stopped on the sweep limit at `≈ 3.078` against the
proved `2.707107`, and **the atlas recorded all twelve interrupted descents as twelve
distinct basins while every one of its structural invariants passed green.**

That is the shape this plan is most exposed to, so it is worth naming precisely: the
store was correct, the keys were correct, the schema was correct, and the census was
nonsense — because none of those check *what the store is fed*. A discovery curve built
on it would never plateau, which presents as “the landscape is enormous” rather than
“the instrument stopped early”, and `H-011`’s saturation criterion and `H-012`’s basin
ranking would both have inherited it silently.

Fixed, measured and regression-guarded.
The census now converges 12 of 12 from cold and finds `s(5) = 2.707106781187` exactly.

### What that changes about the plan

**Half A gains a validation step, and it comes before the multistart proposer rather
than after.** The night’s whole premise is that the harness can be left alone with these
tools, and D-030 is direct evidence that the tools can be confidently wrong in the
flattering direction while every check around them passes.
One defect found by luck at `n = 5` is not a basis for running `n ≤ 10` unattended.

So the sequence is now:

1. ~~`canonicalize`~~ — done
2. ~~`atlas`~~ — done
3. ~~D-030~~ — found and fixed
4. **The validation suite** — implemented and already useful: it found
   [D-031](../../../../defects.md) at `n = 3` on its first run.
   F-16 in the stacked review keeps this step open until oracle and characterization
   policies are separated.
   See [Validating the tools](#validating-the-tools-before-trusting-them)
5. **Resolve [D-034](../../../../defects.md): define terminal components and identity
   uncertainty** (`think-1s0h`, `think-0yo9`, `think-3szr`). The exact `n=3` family is
   the control; the `n=5` duplicate is unresolved until rank and continuation establish
   its relation
6. **Classify unrecognised endpoints from retained poses** (`think-aans`)
7. **Fix [D-035](../../../../defects.md)** — an interrupted negative control can leave
   deliberate sabotage in the tree and must not coexist with cadence commits
   (`think-97pp`)
8. **`multistart`, one named baseline proposer** — supervised development only until its
   full `P/Q/E` regime and comparison arms exist (`think-apwt`)
9. The recipe, the handover gate, the night

## Validating the tools before trusting them

The goal is not test coverage.
It is **being able to point a research loop at these tools in ways nobody anticipated
and still believe the output** — which is a stronger requirement than “the tests pass”,
and D-030 is why.

### Why an ordinary golden test is not enough here

A golden test whose expected values are *whatever the code produced last time* is a
characterization test.
It catches regressions, and it cannot tell you the code was ever right.
Against this project’s actual failure history — where four of six soundness defects
pointed in the flattering direction — a golden captured from a wrong run is a wrong
answer with a checksum on it.

So the goldens here are **grounded in mathematics rather than in a previous run**, at
three levels of strength:

| Level | Oracle | Where it bites |
| --- | --- | --- |
| **Proved** | `s(n)` is known exactly for `n = 1…4, 5, 9, 10, 16` | The best basin must equal it. A basin *below* it is a bug, unconditionally |
| **Closed form** | A real optimum lands on a recognisable algebraic number | An arbitrary stopping point does not land on `2 + 2√2⁄3`. Matching a closed form to `1e-12` is evidence the point is real, not merely stable |
| **Independent** | `sqpack.verify` decides validity through code the quench does not share | Every basin in the map is a *valid packing*, checked by the soundness perimeter’s oracle rather than by the thing that produced it |

The first two are what a characterization golden cannot do.
The third is the perimeter rule (**R1**) applied to the map rather than to a component.

### The trivial cases are the ones worth testing

`n = 1, 2, 3, 4` have answers anyone can check by drawing them, and `n = 9, 16` are
grids. They are cheap, they are exact, and an engine that cannot recover `s(4) = 2` has
no business being pointed at `n = 11`. They are also where a bug is *legible*: a wrong
answer at `n = 4` is obviously wrong, where a wrong answer at `n = 11` looks like
research.

This is the calibration ladder (**R-3**) taken one rung lower than the campaign has been
using it.

#### It paid on the first run: [D-031](../../../../defects.md)

`n = 3` — three unit squares in a `2 x 2` box, the most trivial case in the suite —
reported **four** basins from four proposals.
Two of them had identical side, identical closed form, identical contact count and
identical angle classes.
They were the same packing: the same squares in the same places, one set at `0` and one
at `90` degrees.

The geometric key quantized an angle with `round(theta / quantum)`, which treats it as a
point on a line. It is a point on a *circle*: a unit square is invariant under a quarter
turn, so `theta` is periodic with period `pi/2`, and the quantizer had a seam at the
wrap-around. An angle one ULP below `pi/2` keyed as step `1570796`; its twin at `0.0`
keyed as `0`.

Three things about this are worth carrying forward.

1. **It was flattering in both directions that matter.** A split landscape reads as
   richer than it is, and splitting the basin a record lives in makes that basin look
   *rarer* — which is the direction that confirms this campaign’s own rarity premise.
2. **The other key could not have caught it.** Two images of one packing have identical
   contact graphs, so the contact certificate agrees with itself while the geometric key
   is wrong. Two keys that fail in opposite directions is the design; this is a case
   where only one of them was load-bearing.
3. **It needed a case small enough to read by hand.** Nothing was inconsistent — the
   store was internally coherent, every structural invariant passed, and at `n = 5` or
   above “four basins” would have looked like a finding.
   At `n = 3` it looked like an arithmetic mistake, because the right answer was already
   on the page.

The fix quantizes on the circle; the witness — `nextafter(pi/2, 0)` against `0.0` — is
now a check in `tools/canonical_check.py`, and the `n = 3` row of the golden map is the
second guard.

## Design

### The night in two halves

|  | Hours | Who | Output |
| --- | ---: | --- | --- |
| **A. Build** | ~0–3 | agent, watched | `canonicalize`, a minimal `atlas`, the multistart proposer, each with a gate check |
| **Handover** | — | — | the [handover gate](#the-handover-gate) below |
| **B. Run** | ~3–9 | harness, unattended | the `n ≤ 10` census sweep drains; `H-011` and then `H-012` get verdicts |

The handover is the only interesting moment in the plan, because it is where the
project’s dominant defect detector switches off.
The defect log is explicit about this: **24 of 29 defects were caught by a person or
agent reading with intent, and 1 by the automated gate.** Half B has no reader.
So the handover gate below is not ceremony — it is the substitute.

### Half A: the minimum spine that unblocks a census

Three beads, taken in this order, each landing with its own check in `test.sh`.

1. **`canonicalize` (`think-t1s9`)** — two-level basin identity: a quantized geometric
   key under `D₄` and square relabelling as the fast path, contact graph up to
   isomorphism as ground truth.
   This is the piece that makes “basin” mean something.
   Until it exists, basin counts are artifacts of a tolerance
   ([D-020](../../../../defects.md)).

   *Check:* Trump’s packing and a perturbed-then-quenched copy of it produce the same
   canonical key; two genuinely distinct `n = 5` optima do not; the key is invariant
   under all eight `D₄` images and under relabelling.

2. **`atlas` (`think-eq6l`)** — append-only, deduplicated by canonical identity, one
   soft-schema artifact.
   Minimum viable fields only: canonical key, exact-or-polished side, quench frequency,
   angle signature. `descriptors` and neighbour links are explicitly *not* in scope
   tonight (`think-hhon` stays open).

   *Check:* the atlas validates against its schema; re-running the same seeds adds no
   new entries; the whole-set checker sees no duplicate keys.

3. **`multistart` (`think-jxx8`)** — the uniform-sampling null proposer, which is what
   the census is actually made of and what every later proposer is measured against.
   It must obey the harness’s experiment contract: JSON Lines carrying `best_side`, `n`,
   `seed` and a zero `overlap`, exit 0.

   *Check:* `runner.py preflight` passes with it in the queue, and one supervised round
   completes end to end at `n = 5`.

**Deliberately deferred:** `meter` (`think-b4jc`). Pair-tests are the campaign’s
declared budget currency and `sqsearch` still does not emit them, so tonight’s budgets
are in **wall-clock and restarts**, declared as such in the recipe.
That is a known, recorded compromise, not an oversight — and it is why tonight’s rounds
must not be used for cross-proposer budget comparisons.
`think-owm0` tracks retiring the move-based budget.

### The handover gate

Half B does not start until every one of these holds.
Each is mechanical; none is a judgment call.

```
[ ] ./test.sh --strict                     exits 0, zero skips
[ ] runner.py preflight                    all checks pass, including a non-empty queue
[ ] runner.py status                       shows >= 6 runnable cells, i.e. more than the night can drain
[ ] one supervised round, end to end       claim -> execute -> record, gate-clean after
[ ] git status                             clean; everything committed
[ ] the recipe's timebox is sized          against THIS machine's measured throughput
```

The third line is the one that would have caught tonight’s actual problem a day ago, and
it is now
[step 7 of the skill’s pre-flight](../../../../../../.agents/skills/experiment-loop/references/unattended.md).
A working runner in front of an empty queue is an idle night.

### Half B: the initial strategy, and running it to completion

**The strategy: a versioned raw-coordinate multistart baseline + LP quench + certified
terminal-component classification, swept over `n = 5…10`, with event-level coverage
estimation.** That is the corrected H-011.

Why this and not the alternatives:

- **Not `H-017` (100× budget at `n = 11`).**
  [exp-011](../../../../campaign/series/series-000-smoke-and-calibration/experiments/exp-011-h-020-n17.md)
  showed the annealer returns the trivial grid at `n = 17` on all five tested seeds.
  That scopes a failure of this method and budget at `n=17`; it does not establish
  blindness to oblique records at every `n`.
- **Not `H-001` (angle-class).** Its proposer does not exist, and building it is a
  bigger job than the three beads above.
- **`H-011` is load-bearing.** Its event, component, and uncertainty machinery is reused
  by H-012. H-012 is not merely a query over the declared H-011 sweep, because it also
  requires an explicitly budgeted `n=11` cell and a named proposer regime.

Its declared sweep is `n = 5, 6, 7, 8, 9, 10`, and `n = 8` is the **kill line**: the
corrected registered criterion requires the 95% upper confidence bound on unseen
terminal-component mass to fall below `0.05` within tier S. A visual plateau is
diagnostic only.

**Running to completion** means, concretely: the harness claims one round per cell,
drains the sweep in `n` order, and stops on whichever comes first — the sweep
completing, the session budget expiring, the saturation criterion firing, or three
consecutive guard refusals.
Every one of those writes the session report; only the last exits non-zero.

### What the morning gets

`campaign/session-report.md`, the current generated handoff, leading with **Needs
review** — which will hold any cell that met its criterion, because
[the harness cannot write the accepting verdict](../../../../campaign/runner.py).
It is not append-only until D-071 closes.
Then the ledger, regenerated after every round, and one commit per round.

The first things to read are censoring, identity ambiguities, and the unseen-mass
interval per `n`; the `n=8` question is whether the preregistered bound passed, not
whether a plot looked flat.

## Fallbacks

Named in advance, because a decision made at 2am is a decision made badly.

| If | Then |
| --- | --- |
| Half A overruns past ~4h | Do **not** start a half-built census. Fall back to `H-017`, which is registered, recipe’d and needs nothing new — a predicted-negative night is still a recorded night |
| `canonicalize` lands but `atlas` does not | Same fallback. A census without dedup is not a census |
| The multistart proposer fails `preflight` | Fall back to `H-017`; file what failed as a bead |
| Half B hits three guard refusals | The harness stops itself and exits non-zero. Do not restart it — the instrument is suspect, and that is the morning’s first item |
| A round dies mid-flight | `runner.py release <exp-id>` records it `unresolved` and returns its hypothesis to the queue. Recovery is one step, not a restart |

## Implementation Plan

Every item is a bead against this spec:

```bash
tbd list --spec explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
```

### Half A — build (watched)

- [x] `canonicalize`: two-level basin identity (`think-t1s9`)
- [x] `atlas`: minimum viable deduplicated store (`think-eq6l`)
- [x] **D-030**, found while building the above: the quench could not converge from a
  cold start, and the atlas recorded the interrupted descents as basins
- [x] **Golden basin maps for the small proved cases** (`think-u0i6`) — built as
  `tools/golden_basins.py` over `n = 1…5, 9, 10`, wider than this spec asked for, each
  with its proved optimum, closed-form recognition, and independent validity
- [x] **D-031**, found by the above on its first run at `n = 3`: basin identity split an
  angle at the `pi/2` seam, so identical packings a quarter turn apart were two basins
- [ ] **Engine anchors at the trivial cases** (`think-ouf0`) — `sqsearch` must recover
  `s(n)` at `n = 1…4, 9, 16`, and more budget must never return a worse best.
  *Partly standing already:* the engine selftest’s check 7 is a positive control on
  `s(5)`, both that it is reached and that it is never beaten.
  The gaps are the rest of the ladder and the budget-monotonicity half, which nothing
  checks today. **No longer blocks `multistart`** — it blocks the handover gate instead.
  The census runs the quench, which the golden suite now validates; `sqsearch` is not in
  that loop, so gating the proposer on an engine anchor idles the queue for a reason
  that does not bear on it.
  It still has to be true before the night starts, which is what the handover gate is
  for
- [ ] **`multistart`: the uniform null proposer**, obeying the experiment contract
  (`think-jxx8`) — retain it as a named raw-coordinate baseline, not a canonical null
- [ ] **Terminal-component identity** (`think-0yo9`) — the exact `n=3` sliding family
  must remain one connected component at every tested geometric quantum
- [ ] **Identity calibration** (`think-3szr`) — D-021’s side floor must not decide pose
  equality; unresolved pairs produce count bounds
- [ ] **Unrecognised endpoint classification** (`think-aans`) — retain poses and emit
  evidence-based terminal/promotion classes
- [ ] **Proposer-conditioned comparison** (`think-apwt`) — version `P/Q/E` and compare
  proposal measures at equal pair tests
- [ ] Give `H-011` a `runner.command` recipe, sized against measured throughput
- [ ] Flip `H-011.instrument_ready` to true in the same change that makes it true

### Found while building Half A, tracked but not blocking the night

- `think-5zwm` — rehearse the recovery path (`claim → ledger → release → ledger`)
  against a scratch record.
  [D-032](../../../../defects.md) and [D-033](../../../../defects.md) both shipped in a
  merged PR because nothing had ever run `release`, and neither fix left an
  unconditional check behind
- `think-l3ds` — the gate is 152s, down from 480s. The perimeter (59s) and the negative
  controls (42s) are 101s of what remains and nobody has looked at either
- `think-7z7y` — the atlas fields deferred from the minimum viable store: algebraic
  degree, symmetry group, neighbour links with merge-delta.
  Degree bears on reconstruction, but it cannot by itself separate a legitimate optimum
  from an unconverged or non-isolated endpoint
- `think-97pp` — [D-035](../../../../defects.md), the `negctl` residue.
  Blocking for the night, listed here as well because it is infrastructure rather than
  cartography

### Why the flat-basin problem surfaced this late

Worth recording, because the answer is about documents rather than about code.
Every piece of it was already written down, in three places that never met:

- the **glossary** defined rigidity, but only ever attributed it to Trump’s packing — a
  property records happen to have, rather than one an arbitrary optimum may lack;
- the **basin** definition said “the preimage of one quench *endpoint*”, which silently
  presumes the endpoint is a point, and never stated that as a precondition;
- the **strategy premise** is literally *“records are rigid; rigid optima live in rare
  basins”* — a sentence whose own construction presupposes that non-records may be
  non-rigid, and which never asked what those do to a census that counts basins.

Joining those statements exposes the missing precondition, but does not choose the
component definition.
The research doc now preserves the correction and distinguishes the exact `n=3` family
from the still-unresolved `n=5` pair.
See the [terminology section](../../../../SYNOPSIS.md#terminology).

### The handover

- [ ] **[D-034](../../../../defects.md) resolved** — the census cannot start before
  basin identity means something.
  This is not a checklist item that can be waived on the night: a census run against the
  current definition produces a number that is wrong in the flattering direction and
  looks fine
- [ ] **[D-035](../../../../defects.md) fixed** — an interrupted gate currently leaves a
  deliberately-subtle sabotage in the working tree.
  A session that commits on a cadence will commit it.
  This is the one item on this list that can corrupt the *repository* rather than a
  measurement
- [ ] Run the handover gate above; do not proceed on a partial pass

### Half B — run (unattended)

- [ ] `runner.py run --session-hours 8`
- [ ] Morning: read the session report, resolve the review queue, re-screen the registry

## Testing Strategy

Each Half A bead lands with its check wired into `test.sh` in the **same change**, not
after. That is rule **R1** from the
[soundness postmortem](../../postmortems/postmortem-2026-08-23-soundness-class.md), and
the reason it is not optional here is that Half B has no reader: a check that lands
tomorrow protects nothing tonight.

Each check must also be watched failing, via `tools/negctl.py`, before it is trusted —
the same standard the existing fifteen negative controls meet.
A guard nobody has seen fire is not yet evidence.

## Open Questions

- **What is the counted object?** A terminal component under declared `P/Q/E`, not a
  hash. At `n=3`, the exact side-2 sliding family proves endpoint equality is
  positive-dimensional; `think-0yo9` owns the component contract.
- **What are the unrecognised singletons?** The current artifacts cannot decide.
  They remain unresolved endpoints until `think-aans` replays retained poses through
  stationarity, isolation, and promotion checks.
- **What does D-021 resolve?** Only scalar side differences at the polished tier.
  `closest_pair` is a side-gap diagnostic, not an identity test; `think-3szr` owns the
  tolerance sweep and ambiguity bounds.
- **Is uniform multistart the right null?** There is no distribution-free null.
  Raw coordinate-uniform sampling is one interpretable baseline once its box,
  feasibility rule, quench, and identity relation are versioned; `think-apwt` compares
  it with other named measures.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
