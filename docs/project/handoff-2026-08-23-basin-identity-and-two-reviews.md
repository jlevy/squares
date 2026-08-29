# Handoff: Basin Identity and the Integrated PR Reviews

> **Lifecycle:** Superseded for current guidance by the [synopsis](../../SYNOPSIS.md).
> Retained as a dated handoff.

**Date:** 2026-08-23

**Author:** Claude and Codex agents

**Status:** Historical after PR #16 was reviewed and absorbed into PR #15

This handoff covers the atlas, basin identity, and the independent response to the
standing program review.
For the quench engine, start with
[`handoff-2026-08-23-quench-spine.md`](handoff-2026-08-23-quench-spine.md).
For claims and current evidence, [`SYNOPSIS.md`](../../SYNOPSIS.md) is authoritative.

## Current state

PR #14 is the merged prototype base.
PR #15 contains the standing technical review, the correction program, and the complete
five-commit history from PR #16. PR #16 is no longer a parallel line of work.

The census remains blocked by a mathematical identity problem, not by a missing batch
runner. The exact `n=3` sliding construction proves that a terminal set need not be an
isolated point. For any cell containing a connected terminal component, a point-key
cluster count can overcount components.
The corresponding claim at `n=5` remains unresolved: raw contact subtraction is not a
rank calculation, a first-order null direction need not continue to a finite motion, and
equality rank alone does not settle feasibility under unilateral contacts.

Use **terminal family** only after Jacobian nullity, feasible tangent directions, and
continuation evidence have been checked.
Do not call every numerically close group a flat basin.

## What PR #16 established

The response supplied three durable contributions:

- It independently confirmed five PR #15 corrections: the non-converged atlas fixture,
  strict-implies-deep wiring, pose/side pairing, oracle-before-write ordering, and
  narrowed closed-form prose.
- It corrected its own rank-free `n=5` dimension claim and its misuse of
  “contrapositive.”
- It retracted a seed comparison that used different seeds, then retained a
  like-for-like cross-environment discrepancy.

The cross-environment result is important but narrower than the first handoff claimed.
The emitted `ORACLE FAILURES` heading includes any rendered-byte mismatch, so it does
not prove which mathematical predicate failed.
No complete environment fingerprint or raw per-predicate output was retained.
A source build therefore does not yet establish portable byte identity, but the evidence
also does not establish that every post-quench oracle is portable or that floating-point
contraction is the cause.

Dropping only `annealer_gap` is not enough.
The rendered golden also contains stochastic endpoint identities, discovery counts,
frequencies, and `found_optimum`. D-059 and `think-osyp` now require two explicit
surfaces:

1. a cross-environment mathematical surface containing independently checkable
   convergence, pose validity, and proved-value predicates; and
2. a versioned characterization surface bound to the engine digest, toolchain, target,
   host, proposer, quench, equivalence policy, seeds, and retained endpoint poses.

On the PR #15 integration environment, a fresh
`uv run --frozen --quiet python tools/golden_basins.py --deep` run passed in about 91
seconds. PR #16 records a failure on another environment.
That pair motivates the portability experiment; it does not settle it.

## The `n=5` six-of-six observation

The current golden records six converged `n=5` terminators from six proposals and six
endpoint-key rows. Those rows contain five distinct side values and none reaches the
proved optimum. The only justified sampling conclusion is:

> This proposer/quench/key sample showed no saturation in six draws.

At least four explanations remain live:

- the endpoint identity is too fine for connected terminal components;
- the landscape contains several genuinely distinct terminal components;
- some terminators are insufficiently stationary or are quench-sensitive; or
- numerical clustering splits equivalent endpoints.

`think-1s0h` must measure these alternatives.
The observation is evidence for the experiment, not the result of the experiment.

## Work lanes and real dependencies

This is a dated priority map, not a serialized queue.
`tbd ready` and `tbd blocked` are authoritative when it drifts.

| Lane | Bead | Dependency or purpose |
| --- | --- | --- |
| Correctness | `think-1s0h` | Measure terminal flatness and define what the census can count |
| Correctness | `think-siui`, `think-jxx8` | Blocked by `think-1s0h`; identity invariance and the named multistart baseline need the terminal-family decision |
| Correctness | `think-osyp`, `think-zt29` | Independent portability and golden-policy work; separate mathematical predicates from stochastic characterization |
| Process | `think-97pp` | Independent narrow recovery work: visible mutation state, bounded children, signal-aware restoration, and focused crash rehearsal |
| Infrastructure | `think-lcfd` | Independent terminology and field migration from `closest_pair` to `closest_side_gap` |
| Infrastructure | `think-ouf0`, `think-5zwm`, `think-l3ds`, `think-7z7y` | Independent engine anchors, budget monotonicity, gate timing, and deferred atlas fields |

`think-ivr1`, `think-lqp6`, `think-yebk`, and `think-o48b` are closed because their
focused repairs were verified.
Golden portability continues under `think-osyp`; D-059’s broader separation and gate
policy remains under `think-zt29`. `think-97pp` is open.

## Operating rules for the next loop

1. Run the cheapest focused check that can falsify the current change.
   Run the normal gate once before pushing an integrated checkpoint.
2. Record elapsed wall time, the exact command, environment provenance when relevant,
   and the retained artifact.
   Do not infer a particular oracle failure from a generic aggregate label.
3. Until D-035 lands, inspect `git status` before broad staging after an interrupted
   negative-control run.
   The accepted repair is cooperative crash recovery, not hostile repository isolation.
4. Keep mathematical claims, exploratory measurements, and process state in their own
   records: the synopsis and research docs, campaign artifacts, defects, beads, and
   agent-session handoffs respectively.
5. Treat every causal interpretation of a stochastic census as a registered hypothesis
   with alternatives and a discriminating measurement.

## Questions that remain open

- Is the observed `n=5` terminal set positive-dimensional, a collection of isolated
  terminals, or a mixture?
- What equivalence relation should the census use once terminal nullity is measurable?
- Which post-quench predicates reproduce across toolchains and hosts when tested and
  reported individually?
- Which stochastic fields are scientifically useful enough to retain, and what complete
  provenance makes comparisons meaningful?
- Is uniform multistart the right null distribution for basin-volume claims?

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
