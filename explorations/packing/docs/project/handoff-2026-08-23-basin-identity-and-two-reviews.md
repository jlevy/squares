# Handoff: Basin Identity, Two Open Reviews, and Why the Census Still Cannot Run

**Date:** 2026-08-23 (evening)

**Author:** Claude (agent)

**Status:** Current

Supersedes nothing —
[`handoff-2026-08-23-quench-spine.md`](handoff-2026-08-23-quench-spine.md) is still
accurate about the quench and is the better starting point for the *engine*. This one
covers what happened after it: the atlas, the basin-identity work, and two reviews that
are open at the same time.

Same rule as the other handoff: this states positions,
[`SYNOPSIS.md`](../../SYNOPSIS.md) states results, and where they disagree the synopsis
is right because the gate reconciles it and nothing reconciles this.

## The one-paragraph state

Basin identity, the atlas, and a mathematics-grounded golden all exist and work.
Four defects were found and fixed on the way (D-030 through D-033), and the gate went
480s → 152s. **But the census still cannot run, and the reason is not a missing
feature.** It is [D-034](../../defects.md): a local optimum is not always a *point*.
Where the contacts do not pin every degree of freedom the optimum is a **flat basin** —
a positive-dimensional set — and `distinct_basins` then counts members of one optimum
rather than distinct optima.
`n = 3` is a proved witness.
Until basin identity is defined for that case, every basin count in this repository is
an upper bound, and H-011’s saturation criterion is unreachable by construction.

## The unusual part of the current situation: two reviews, both open

|  | What it is | State |
| --- | --- | --- |
| **PR #14** | The atlas, canonical identity, the golden, D-030…D-035 | **merged** as `8926a7c` |
| **PR #15** | A 1,659-line standing review of #14 and the whole program: 21 findings, 4 omissions, 4 alternatives, 4 open questions, plus fixes | open, draft |
| **PR #16** | A response to #15 by the author of the reviewed code: 8 findings confirmed, 1 refuted with evidence | open, draft |

Read them in that order.
#15 is the more important document — it is the best thing this campaign has produced —
and #16 exists only because a review is worth more after someone has tried to break it.

**Do not treat #16 as a defence.** It concedes eight findings including the worst defect
in the reviewed work.
It disputes exactly one claim, and that one matters because its prescribed repair would
be implemented, would appear to work, and would not fix anything.

## Stacked on #15, and what that changed

PR #16 is now stacked on `codex/pr14-square-packing-review`, not on `main`. Re-verifying
every finding against that branch: **four of five were already fixed there**, several
exactly as specified — the vacuous convergence assertion, `--strict` implying `--deep`,
the pose/side pairing, and the write-before-check.
Independent convergence on the same fixes from two directions is the useful result, and
those beads are closed.

So the list of things that will actually cost you is now short.

### 1. Do not implement F-16’s build repair as written — it has been tested and it fails (`think-osyp`)

#15 marks the source-build repair done and selects control seeds to stabilise the
ladder.
That is a falsifiable prediction: the golden should then reproduce anywhere after
a source build. Checking out that branch, building its engine, and running **its own**
`tools/golden_basins.py --deep` on a different machine gives:

```
ORACLE FAILURES:
  the rebuilt map differs from the committed golden
GOLDEN BASIN CHECKS FAILED
```

The two environments disagree at both control seeds, in opposite directions: at `n = 10`
seed 7 the quench reaches the proved optimum here and (per their own `LADDER` comment)
does not there; at seed 14 they record `+0.000493446` and this machine gives
`+0.032867764695`. Same seed, same `n`, same engine source, both built from source.

A simulated annealer is chaotic — one ULP in an accept/reject diverges the trajectory,
and `lto = "fat"` with `codegen-units = 1` under a different toolchain or
microarchitecture changes float contraction.
**The fixture is non-portable, and selecting control seeds makes it worse**, because it
tunes the fixture to the machine that chose the seeds.

The ladder’s *oracle* is robust in every environment tested.
Assert the oracle; drop `annealer_gap` from the byte-compared surface, or store it with
a tolerance plus a toolchain and CPU fingerprint.

### 2. `git status` before `git add -A`, every time, until D-035 is fixed (`think-97pp`)

`tools/negctl.py` corrupts a tracked source file in place and restores it in a
`finally:` block, which a `SIGKILL` does not run.
An interrupted gate leaves a *deliberately subtle, deliberately flattering* mutation in
the tree — it has already happened once, and what it left behind was the D-031
basin-splitting bug.
A cadence-committing session would commit it behind green history.

## The queue, in the order it should be worked

Everything below is a bead; `tbd ready` is authoritative if this drifts.

| Order | Bead | Why here |
| ---: | --- | --- |
| 1 | `think-ivr1` | A guard that cannot fail is worse than no guard, and it is cheap |
| 2 | `think-lqp6` | `--strict` does not imply `--deep`, so the handover gate does not run the check its own comment promises |
| 3 | `think-o48b` | Reconcile #15 and #16 into `main`; **regenerate the golden and diff it**, because #15’s convergence fix changes what `converged` means |
| 4 | `think-1s0h` | Measure terminal flatness — the LP degeneracy route. This is what unblocks the census |
| 5 | `think-97pp` | D-035, before anything unattended |
| 6 | `think-yebk`, `think-lcfd` | Write-before-check, pose/side mismatch, two overstated docstrings |
| 7 | `think-jxx8` | The uniform multistart null — blocked on 4, not before it |
| 8 | `think-ouf0`, `think-5zwm`, `think-l3ds`, `think-7z7y` | Engine anchors, recovery rehearsal, the gate’s unexamined 101s, deferred atlas fields |

## Six things that will save you a day

1. **Convergence and discovery are different questions.** *Given a start in the
   optimum’s basin, does the pipeline land on it* is a property of the tools,
   deterministic, and must hold.
   *Does multistart find it in N draws* is a property of the landscape, probabilistic,
   and is what H-012 measures.
   Asserting the second is how a gate starts failing for reasons nobody can act on.
   This was conflated three times before it stuck.
2. **The trivial cases are where bugs are legible.** D-031 was found at `n = 3` and
   D-034 at `n = 5`. A wrong answer at `n = 4` is obviously wrong; a wrong answer at
   `n = 11` looks like research.
3. **Structural invariants do not catch mathematics.** All six of the atlas’s invariants
   passed green while twelve interrupted descents were recorded as twelve basins.
   What caught it was a proved `s(n)`.
4. **A check must be watched failing, and its inputs must be able to produce the
   failure.** Three separate vacuous checks shipped or nearly shipped here: two tampers
   that replaced nothing, and one assertion whose fixture excluded the failing case.
   `negctl` catches the first kind and not the third.
5. **Read the docs before deriving anything.** D-034 was derivable on day one from three
   documents that each held a third of it: rigidity was defined but only attributed to
   Trump’s packing; “basin” was defined as the preimage of an *endpoint* without saying
   that presumes a point; and the strategy premise is *“records are rigid; rigid optima
   live in rare basins”*, whose own construction presupposes that non-records may not
   be.
6. **The defect log’s detector column is the deliverable.** Thirty-five defects in, the
   automated gate has caught exactly one, and none of the soundness class.
   Build detectors that can be surprised — control cells, proved values, trivial
   instances — not more assertions about internal consistency.

## Open questions a fresh pair of eyes should weigh

- **Is `n = 5` actually flat?** The claim that it is a five-dimensional family was
  *rank-free* — counting 11 constraints against 16 coordinates bounds the dimension only
  if the constraint gradients are independent, which was never shown.
  `n = 3` is proved; `n = 5` is an unresolved observation of two endpoints sharing a
  side and a contact certificate.
  #15 is right about this and #16 concedes it.
- **What should the census count, once flatness is measurable?** Three candidates on
  `think-1s0h`: dedup on (contact certificate, side within the tier floor); canonicalize
  within the family; or report families with their dimension and stop publishing a
  single number. This is a decision about the deliverable’s shape, not an implementation
  detail.
- **Is uniform multistart the right null?** It is *a* baseline, not a canonical one, and
  every frequency statement is conditional on a proposer regime that is not fully
  recorded.
- **Nothing yet would notice a non-portable fixture.** Both branches ship one and both
  gates pass.
