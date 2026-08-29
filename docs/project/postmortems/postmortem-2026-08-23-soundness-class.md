# Postmortem: The Soundness Class, and the Perimeter That Let D-014 Through

**Date:** 2026-08-23

**Author:** Claude (agent), for samanthadrakova@gmail.com

**Status:** Complete

**Scope:** the six soundness defects in [`defects.yaml`](../../../packing/defects.yaml)
— D-009, D-011, D-013, D-014, D-020, D-021 — with **D-014** as the primary case, since
it is the only one that produced a false claim about the mathematics.

## What happened

A quench built to refine packings reported, for `n = 11`, a side of

```
3.877083568103152   against Walter Trump's   3.877083590022814
```

— a packing 2.2×10⁻⁸ better than a construction that has stood unbeaten since 1979.

It was not a packing.
Squares 4 and 8 overlapped by 9.876×10⁻⁸. The linear program had returned a solution
violating **its own separating-axis constraint**, and reported it as optimal, because
HiGHS defaults to a primal feasibility tolerance of 10⁻⁷ — larger than the quantity
being measured.

The error had a direction, and the direction is the point.
Overlapping squares occupy a smaller box, so this class of failure always *flatters*: it
does not produce noise, it produces apparent discoveries.

## How it was actually caught

The investigation was triggered by a sentence written before any of this code existed,
in the campaign runbook:

> The `n = 12` negative control.
> The 4×4 grid is almost certainly optimal, so a run reporting anything below `4` has
> found a bug in the geometry, not a packing.

That sentence was a useful alarm but an invalid oracle: `s(12) = 4` is not proved, so a
valid value below `4` could be a discovery ([D-042](../../../defects.md)). The sound
rule is the one generalized in the same document: *do not record `beat_record: true` at
any precision below `exact`*. The independent geometry check established the actual
defect; the open-case incumbent did not.

**The existing perimeter did not catch it.** The test suite passed, and the differential
test compared `sqsearch` against `sqpack` without seeing the quench.
The quench’s own consistency was intact — the solver’s answer was self-consistent with
the solver’s own idea of feasible.
The only tripwire was a pre-registered expectation about the *world*.

## Why it could not have been caught sooner

Three reasons, in increasing order of how much they should worry us.

**1. There was no detector, only a rule.** A rule requires someone to look.
It fired here because a human-shaped agent read a number and recognised it as
impossible. Had the same solve happened inside an overnight sweep of 3,000 rounds, it
would have been a row in a JSONL file, and the first person to notice would have been
whoever tried to publish it.

**2. The perimeter had a hole exactly where the new code was.** The repository already
owned a validity oracle (`sqpack`, exact over the packing’s own number field) and
already understood that independent checking matters — `differential_test.py` exists
precisely to stop `sqsearch` and `sqpack` drifting apart.
But the quench was new, and nothing extended the perimeter to cover it.
It was checked against its own constraint rows, which is no check at all when the
constraint rows are what the solver got wrong.

**3. The founding argument had already been made, about a different layer, and nobody
transposed it.** Six research documents argue that a floating-point validity check needs
a tolerance to accept true contacts, and that this tolerance is a blind spot which also
accepts small overlaps.
That argument is the reason `sqpack` exists.
It applies word for word to an *optimiser*, and no document said so.
The idea was present, correct, and scoped one layer too narrowly.

## The generalisable cause

D-014 and D-019 — a critical soundness failure and a non-termination bug that look
nothing alike — have the same root:

> **A tolerance was chosen without reference to the scale of the quantity it governs.**

- D-014: the solver’s feasibility tolerance (10⁻⁷) was *looser* than the improvement
  being claimed (2×10⁻⁸), so the claim lived entirely inside the solver’s slack.
- D-019: the line search’s convergence tolerance (10⁻¹⁵, absolute) was *tighter* than
  one ULP of the angles it was applied to (1.78×10⁻¹⁵ at 14.14 rad), so the interval
  could never satisfy it and the loop could not terminate.

Same mistake, opposite ends.
This is now a rule (below).

## What has changed

Five things, all in this branch, all with checks:

| Change | Guards |
| --- | --- |
| [`devtools.check_soundness_perimeter`](../../../packing/devtools/check_soundness_perimeter.py) — every component that can emit a packing, checked by `sqpack` through code it does not share | D-014’s whole class |
| Post-check inside the quench: a solution violating its own constraints is rejected, not returned | D-014 |
| Solver tolerance pinned at its floor (10⁻¹⁰), and the perimeter held to the same bound so they cannot drift | D-014, D-021 |
| Tolerances scaled to the quantity they govern; the line search capped in iterations | D-019 |
| [`devtools.run_negative_controls`](../../../packing/devtools/run_negative_controls.py) + [`devtools/controls.yaml`](../../../packing/devtools/controls.yaml) — the negative controls checked in and run, rather than performed once and described | the checking apparatus itself |

The perimeter was replayed against the original defect: handed the configuration that
“beat” the record, it rejects it and names the overlapping pair.
That replay is now a permanent test.

## The rules this yields

Four, stated so they can be applied to code that does not exist yet.

**R1 — Every component that can emit or accept a configuration is checked by the oracle,
through code it does not share.** Self-consistency is not validity.
A component checked against its own model of correctness is checked against the thing
most likely to be wrong.
The perimeter is a list, and adding a component means adding it to the list.

**R2 — Every tolerance is stated relative to the quantity it governs, and compared to it
out loud.** Before a tolerance is chosen, write down the scale of what it must resolve.
A feasibility tolerance must be *tighter* than the smallest claim built on it; a
convergence tolerance must be *reachable* at the scale of its argument.
Both failures this session were this rule, unwritten.

**R3 — A claim that would be a discovery is treated as a defect until an independent
layer agrees.** This already existed as the assurance discipline and it is what saved
us. Strengthen it from a convention someone reads into a check something runs: the
perimeter now refuses the configuration, so the flattering number never reaches the
record.

**R4 — A new component inherits the perimeter, not just the conventions.** The gap was
not that the quench was written carelessly; it was that it was written *outside* the
coverage that already existed.
Adding a component to the pipeline means adding it to `perimeter_test.py` in the same
change.

## What remains true and unfixable

Floating-point LP refinement has a floor.
With the configured feasibility tolerance, a returned side can be wrong at about 10⁻¹¹,
and eight recorded rounds sit at exactly that scale with small negative gaps to the
analytic value. That is contained by the assurance contract: numerical results may not
claim a record. The limitation is [D-021](../../../defects.md), left open deliberately
rather than papered over.
Removing it needs exact rational arithmetic in the LP, which is a real project and is
tracked (`think-hg3u`).

## The uncomfortable observation

Of 23 defects now logged, **the automated gate caught none of them.** They were caught
by control cells whose answers were known in advance, by pre-registered rules, by a
generated view contradicting its source, by chased anomalies, and by reading.

> **Correction, 2026-08-23.** True as written, at 23. At 26 the gate has caught one —
> [D-024](../../../defects.md), a bookkeeping defect found by a contiguity check — and
> still no soundness defect, which is the claim this section rests on and is unchanged.
> Repeating the wider sentence verbatim in three living documents is itself logged, as
> [D-028](../../../defects.md); the generated view now computes it instead.

That is not an argument against the gate — a gate stops regressions, and this session
added several.
It is an argument about what a gate *is*: it confirms what someone already
thought to check. Every defect here was, by definition, something nobody had thought to
check.
The devices that found them were the ones built to be **surprised** — a cell whose
answer is known, a rule about what cannot happen, a view that must agree with its
source.

Build more of those.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
