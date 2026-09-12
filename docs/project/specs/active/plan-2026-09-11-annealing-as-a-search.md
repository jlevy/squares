---
title: The Annealing as a Search
description: Benchmarking whether the workbench's blind physics can rediscover a known-best packing, and finding parameters that make it more likely
author: Claude (agent), for the repository maintainer
---
# Feature: The Annealing as a Search

**Date:** 2026-09-11

**Author:** Claude (agent), for the repository maintainer

**Status:** Planned; the harness is the first chunk

**Workflow:** W4 research programme

**Tracking:** `think-7umw` (epic)

## Overview

The workbench’s physics is a search, and nobody has measured it as one.

In blind mode it is told nothing about where the squares are meant to end up: it starts
from the packing of n in an inflated container, drops the new square into the emptiest
place a coarse grid finds, and closes the walls in with contacts, walls and a decaying
jiggle. Whether it can rediscover a known-best packing on its own — and how often, and
under what parameters — is a question with a number for an answer.

The number matters for two separate reasons, and confusing them would spoil both:

- **As an animation**, a blind run that lands near the record is a more honest picture
  than one snapped onto it.
- **As a search**, an annealer that reliably finds `s(11)` from nothing is evidence
  about the method — and the method is what the atlas campaign uses at scale.

## Why the Small n

`n = 11` and `n = 17` are the classic hard small cases: tilted squares, irrational
sides, a record no grid reaches.
They are also small enough to run thousands of trials on a laptop.

That combination is what makes them the right benchmark.
If the annealing cannot find them, no amount of tuning at `n = 100` means anything; if
it can, the success rate per parameter set is a number that can be optimised against.

## The Order of Work, and the First Is Not Optional

**A harness that reports a defensible number comes first** (`think-k2fr`). Then the
hypotheses, written down *before* the sweeps so that the sweep tests them rather than
generating them (`think-a87q`). Then the sweep (`think-fj07`), then whatever it says.

A hypothesis found in the data after the fact is a description of the data.

### What the harness has to report

Per (n, parameter set):

- **Success rate** — the fraction of trials whose final side is within a stated
  tolerance of the record.
  The tolerance has to be argued for, not picked: the record’s own poses score 0 to
  1.3e-5 of summed overlap, so anything looser than that is not “found it”.
- **Distance when it fails** — the distribution of the final side, not just a pass
  count. A method that lands 0.1% above the record every time is a different thing from
  one that scatters.
- **Cost** — wall time and step count per trial, so a parameter set that wins by running
  ten times longer is visible as such.
- **Reproducibility** — every trial keyed by its seed, so a claimed improvement can be
  re-run.

### Two constraints, both learnt here

1. **It must finish.** `check_revision6.py` runs a blind sweep over 323 pairs and has
   never completed — 57 minutes without finishing, measured, and still going at 30 on an
   idle machine (`think-i15w`). This harness samples a named set of n, reports
   incrementally, and has a declared budget.
2. **It is a program in `devtools`, not a script in the spike tree.** `OR-1`: never
   leave a measurement in one-off code.
   It comes under the lint and type floors like everything else.

## What Exists Already

Reused rather than replaced:

- `grade_motion.py` grades a run on two axes — outcome (residual, mean, turn at lock-in)
  and motion (wander, jerk, overlap).
  That is the scoring half.
- Blind mode (`setBlind`, `BLIND.inflate`) is the search half: a run with no knowledge
  of the target.
- The page’s API drives both headlessly, and the four-phase beat now lets the search and
  the landing be priced separately.

## Testing Strategy

The harness is itself the test, which is the trap to avoid: a benchmark that cannot be
wrong measures nothing.
So two things are checked independently of it — **H7, that replay is deterministic**,
before any other number is believed; and a **held-out set of n** that no sweep tuned
against, which is what a claimed improvement has to reproduce on.

## Open Questions

- **Is the blind run a search at all, or a quench?** H4 is the measurement: a search
  improves with steps, a quench plateaus early.
- **Is the answer decided by the initial drop rather than by the annealing?** H2. If so
  the schedule is decoration and the effort belongs in the proposal.
