---
title: H-107 — the retained scalar sites admit a complete cover
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-107
  kind: hypothesis
  claim: >-
    The terminal exp-116 site set supports a D4-invariant nonnegative rational
    atomic measure of total mass below eleven covering every contained closed
    B-square at all 181 retained net directions, at L=61/16 and B=9977/10000.
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:21', 'proof:22']
  criterion:
    shape: determination
    metric: independently verified mass-below-eleven cover on the frozen sites
    direction: >-
      Accept only after declaration, complete production sweep and interval
      decisions, and standalone unpinned verification accept the same candidate.
      Reject only an independently verified exact finite-site dual of mass at
      least eleven; this experiment implements no such rejection path.
    threshold: total mass strictly below eleven and minimum covered mass at least one
  instrument: packing/devtools/run_fixed_site_completion.py followed by the existing exact certificate decisions
  instrument_ready: true
  regime: Frozen exp-116 terminal sites and initial rows; one row-only completion, no site or dual-support adaptation.
  instance: {axis: side, point: '61/16'}
  priority: 1
  cost_estimate: One 2100-second total process cap and one 1200-second shared conditional verification cap; no retry.
  prereqs: [committed prospective protocol and passing record checks, completed independent adapter review, unchanged proof-chain source controls, fresh sufficient allocation and renewed operational lease]
  replication: false
  registered: '2026-09-07'
---
# H-107 — Complete Rows on the Retained Sites

This is the first narrow discriminator under
[H-094](H-094-n11-weight-and-site-redesign.md), selected by the
[BC-252 assessment](../series/series-000-smoke-and-calibration/results/agenda-025/bc-252-exp116-next-discriminator.md).
Exp-116 stopped adding sites while its two-round row solves remained incomplete.
That result does not establish that these sites fail to support a covering measure.

The proposed test,
[exp-118](../series/series-000-smoke-and-calibration/experiments/exp-118-h-107-fixed-site-completion.md),
was not launched: its record gate was incomplete at the 03:16 UTC cutoff.
Both the 2100-second target allowance and the 1200-second verification allowance remain
unspent. A future launch requires a fresh sufficient allocation, passing record checks
and a renewed operational lease.
H-107 remains unresolved.

The September 7 priority review under `think-m9a9` holds this test out of the next
two-hour block; `think-7fec` retains the later-session reconsideration.
Success would establish fixed-site sufficiency at 3.8125 and provide a scalar control,
but none of the currently selected density or geometry-based compatibility steps depends
on this success. Readiness alone does not allocate another run.
The
[current agenda](../agendas/agenda-024-post-381-24h-portfolio.md#selected-continuation-after-session-090)
owns the reopening conditions; this scheduling decision changes no mathematical claim or
scientific cap.

Freeze the terminal state from exp-116: 24,653 exact sites in 3,180 D4 orbits, 11,885
initial exact placement rows, and the net `t_k=(207107/500000)k/180`, for `k=0,...,180`.
Here `L=61/16` is the containing square’s side and `B=9977/10000` is the core square’s
side.
D4 invariance means invariance under the containing square’s quarter-turn rotations
and reflections; a cover assigns mass at least one to every contained closed core square
at each retained direction.
The legacy state does not embed that net; its identity comes from exp-116’s committed
protocol and producer, not from an invented state field.
Each LP variable is a per-atom weight within one orbit; the objective uses orbit sizes.
Rows count orbit atoms inside a contained core square.

One invocation adds rows on these fixed sites.
It does not run the cutting loop, arrangement-depth separation, support truncation or
site adaptation again.
The existing bridge’s snapping and rationalization can produce only an unverified
candidate. Its numerical convergence is not the acceptance criterion.
Full exact coverage, mass, net/shrink conditions and independent file replay are
required.

A numerical objective at least eleven, an incomplete row solve, failed rationalization,
verification refusal or any process timeout leaves this claim unresolved.
The present adapter has no exact finite-site dual decision and no rejection branch.
Even a future exact rejection would exclude these sites, not every scalar measure in
H-093. No result changes exp-116’s original unresolved outcome.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
