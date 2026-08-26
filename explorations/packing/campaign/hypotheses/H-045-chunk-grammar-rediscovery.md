---
title: H-045 — does a frozen chunk grammar rediscover known optima from no hints?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-045
  kind: hypothesis
  claim: >-
    A chunk grammar and enumeration order frozen against the proved cells n = 5 and
    n = 10, run with no target geometry supplied, ranks a pose within 1e-9 of the
    standing best first among all enumerated strata at n = 11, and returns exactly 4 at
    n = 16.
  lane: search
  derived_from: [X-003]
  strategy_refs: ['search:15', 'search:17', 'search:18', 'search:20']
  criterion:
    shape: determination
    metric: >-
      rank of the standing-best side among enumerated stratum optima, and the n = 16
      guard value
    direction: >-
      rank 1 within 1e-9 at n = 11 and exactly 4 at n = 16, both from a grammar frozen
      before the run
    threshold: 1
  instrument: >-
    Stage-1 stratum enumerator (think-sfzh) emitting initial placements, glued-chunk
    equality rows (think-vnm5), the existing cell-read LP quench to a cell fixed point,
    and the coarse class-angle sweep and bracketing driver (think-dh4b), with every
    stratum priced in counted LP solves.
  instrument_ready: false
  regime: >-
    numerical f64 LP under the measured 1e-11 solver floor; grammar, chunk-size caps,
    sweep resolution, and enumeration order frozen and committed before the n = 11 and
    n = 17 runs
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [5, 10, 11, 16, 17]}
  priority: 2
  cost_estimate: >-
    tier S at n = 5, 10, 16; tier M at n = 11 and n = 17, priced in LP solves rather
    than wall time
  prereqs: [H-044, stage-1 enumerator, glued-chunk LP rows, class-angle sweep driver]
  replication: true
  registered: '2026-08-26'
  notes: >-
    Rediscovery of Trump's packing is not itself novel: Gensane-Ryckelynck 2005 obtained
    it several times from random billiard starts, and the 2026 SCIP and FICO Xpress
    study reports 3.87709 from scratch. The registered value here is deterministic
    coverage rather than rediscovery, so the criterion is a rank over an enumerated
    population, not a best-found side. n = 16 is the guard: a value below 4 means a bug,
    and the same published study returned 4.00001 there, so this boundary is known to be
    easy to get wrong. n = 17 carries the differentiator separately because no archived
    method demonstrably rediscovers Bidwell's record cold; it is declared in the sweep
    and reported as its own cell, never folded into the n = 11 verdict. A grammar frozen
    after seeing n = 11 would make the criterion vacuous, which is why the freeze
    commit precedes the target run and is named in the round record.
---
# H-045 — the rediscovery ladder

The registered claim is about **coverage semantics**, not about finding a packing nobody
has. Both existing from-scratch successes at `n = 11` are stochastic or opaque:
Gensane-Ryckelynck report obtaining the packing “several times” after thousands of
random-start billiard runs, and the general-purpose solver study reports an incumbent
after a fixed compute budget.
Neither can say what was searched.

An enumerator can. If a frozen grammar enumerates `N` strata and the standing best ranks
first among their optima, the round establishes a statement of a different kind: the
record is stratum `k` of `N`, visited deterministically, and no other enumerated stratum
beats it. The near-miss corpus is the by-product, with identity given by the stratum
label rather than a floating-point endpoint key.

## The freeze, and why it is the whole design

The failure mode of any grammar-based rediscovery is leaking the answer into the
grammar. The ladder is therefore ordered so that all design freedom is spent before the
target is approached:

1. **Calibrate on proved cells.** `n = 5` and `n = 10` are each an aligned frame plus
   one `45°` group, and the built quench already takes both to `1e-15`. Grammar
   iteration stops here.
2. **Freeze and commit** the grammar, chunk-size caps, sweep resolution, and enumeration
   order. The round record names the freeze commit.
3. **Run the guard.** `n = 16` must return exactly 4.
4. **Run the target once.** `n = 11`, unrestricted, no target geometry supplied.
5. **Run the differentiator.** `n = 17`, reported as its own cell.

## What this round may not claim

A rank-1 result is a numerical statement under the `1e-11` solver floor
([D-021](../../defects.md)) about the enumerated population only.
It is not a bound, not an optimality proof, and not a coverage claim about strata the
frozen grammar cannot express, which is what
[H-044](H-044-chunk-expressibility-of-records.md) measures separately.
A stopped quench is not a certified local optimum ([D-052](../../defects.md)), and
aligned strata are maximally degenerate cells, so endpoint reproducibility across
toolchains ([D-059](../../defects.md)) is a declared risk for this instrument rather
than an assumed property.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
