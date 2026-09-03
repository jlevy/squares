---
title: H-052 — the fixed n = 17 certificate agrees under independent accumulation
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-052
  kind: hypothesis
  claim: >-
    The fixed retained Massaccesi n = 17, L = 4.5058 certificate agrees on every
    preregistered exact invariant when evaluated by an independently written exact
    accumulation implementation that does not copy the published two-dimensional
    difference-array sweep.
  lane: proof
  derived_from: [X-011]
  strategy_refs: ['proof:22']
  criterion:
    shape: determination
    metric: >-
      exact agreement on the frozen certificate totals, 181 rational direction cells,
      event-cell reductions and minima, global minimum 576/576, and declared
      shrink-and-scaling preconditions, together with rejection of the named mutations
    direction: >-
      accepted only if every frozen invariant agrees exactly and every named mutation is
      rejected; rejected if the independently written path produces a reproducible exact
      disagreement after both paths and their fixtures pass their guards; unresolved if
      implementation independence, provenance, or a guard cannot be established
    threshold: exact equality on every frozen invariant
  instrument: >-
    Exp-049 statically extracts the hash-pinned retained fixture through
    cases/n17_weighted_certificate/extract.py at
    db176a8eff7235991c63c8e7f098e2e2979edf64905d8f76427e0cd218b011e2. Its
    clean-room direct Cartesian accumulator is frozen at
    cases/n17_weighted_certificate/independent.py SHA-256
    55d36239f1f7e860f059030d87f655d2ac0c82685d788b599a7dd23d33d18de0;
    the separate source-faithful difference-array adapter is
    cases/n17_weighted_certificate/source_faithful.py at
    aaccd145c61fb20bc2b83a8ded83dfdd3f2d4b6d6c730ff46df31e1f1d8ae305.
    cases/n17_weighted_certificate/run.py at
    177e8545400799b6a701f258b685f2712f2529132803d78bf984575b897d027c
    emits exact canonical manifests and the five frozen mutation decisions. The focused
    suite in tests/test_n17_weighted_certificate.py passes under normal and optimized
    project Python, with Ruff and BasedPyright clean. The SHA-256 of the sorted
    `sha256sum` manifest for every Python file in cases/n17_weighted_certificate is
    309ec24158f73dd2e9b837c773b1e5c1642f357de5bdf73311b73232abdb6d54,
    which also binds the fixture, shared geometry, canonical model, production self-test
    and target adapter. The self-test emits receipt hash
    9c43160ad7b9f7407c5c1f7057838a925a13b4553b4edcde580f8abc58d9ec00;
    its normal and optimized canonical stdout lines both hash to
    459af1bd0345bee04e5a3af0d1c7a93cec635920774b3d647be13bed9d617579.
  instrument_ready: true
  regime: >-
    The retained 168-atom Massaccesi certificate, its source hash, the 181-cell rational
    direction net, and the published shrink-and-scaling argument are fixed before either
    evaluation. All comparisons use exact rationals; the second implementation may
    share the fixed certificate, mathematical definitions, and invariant manifest but
    not the published accumulation control flow.
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: >-
    one 130-minute experiment round, executed through the agenda's 15–30-minute cells;
    freeze the invariant and mutation manifests before measurement, and stop unresolved
    when a provenance or independence guard fails
  prereqs:
  - hash-verified retained certificate and source-faithful replay
  - frozen exact invariant and mutation manifests
  - separately authored exact accumulation path with an auditable independence receipt
  replication: false
  registered: '2026-09-01'
  notes: >-
    Acceptance establishes implementation agreement for this fixed certificate. It is
    neither proof-method independence nor adoption of 4.5058 as a reviewed lower bound,
    and it makes no cross-n or LP-generalization claim. A disagreement rejects this
    agreement claim but does not by itself refute the mathematical lower bound; the
    discrepancy remains for independent adjudication. Agenda-015 exp-056 stopped at its
    fixed 11:23Z timebox with 170 contiguous agreeing rows through ordinal 169, a
    verified chain and ordinal 170 at independent_started. The canonical result is
    absent, so the larger prefix is review-pending process evidence and gives H-052 no
    disposition.
---
# H-052 — Independent `n = 17` Certificate Agreement

The experiment holds the mathematical input fixed and changes only the exact
accumulation implementation.
The second path must be independently authored and must not translate the published
difference-array sweep line by line.

## Scope

The result measures agreement between two implementations on one retained certificate.
Any later lower-bound adoption requires separate source review and disposition.
The experiment cannot establish a distinct proof method, certificate uniqueness, or
transfer to another value of `n`.

## Resolution — Confirmed at Implementation-Agreement Scope, 2026-09-03

**Confirmed, and the scope in the heading is the whole of it.**
[`exp-059`](../series/series-000-smoke-and-calibration/experiments/exp-059-h-052-n17-fresh-successor-completion.md)
is `accepted` on `BC-149`’s independent review, which returned **PASS**; `needs_review`
is cleared on that review and nothing else moved with it.
The criterion above is **frozen and byte-unchanged** — written before the target work,
never amended for the round or the review, and met as registered.

**What is established.** For the fixed retained Massaccesi `n = 17` certificate, two
separately authored exact accumulation paths agree on every one of the 181 rational
direction cells. Both 181-row `CertificateManifest` summaries are byte-identical: atom
count 168 and atom hash `37d35da0…`, direction count 181 and direction hash `cc789e1a…`,
total weight `203/12`, every one of the 181 row minima exactly `1/1`, and the global
minimum `1/1`, which is the frozen expectation `576/576`. The shrink-and-scaling
preconditions hold, all five frozen mutations are rejected, all twelve frozen
certificate invariants are true, and every decision-bearing field is derived from the
emitted bytes rather than asserted beside them.
The completion ran 08:59:33Z–09:32:44Z, recomputing the interrupted ordinal 170 rather
than promoting it and appending eleven new rows to the 170 carried ones.

**This is assurance evidence, and it is not mathematics.** The registered notes already
fix the scope and the resolution does not widen it: acceptance establishes
implementation agreement for one fixed certificate.
It is **not** proof-method independence, **not** adoption of `4.5058` as a reviewed
lower bound, **not** a certificate-uniqueness claim, and **not** any cross-`n` or
LP-generalization claim; acceptance alone moves no bound.
What did move the verified lower bound at `n = 17, 18, 19` is the separate
source-adoption route, `BC-150` and `BC-151`, resting on the published argument and its
own from-scratch replays rather than on this agreement.
This round is retained beside that route as `E-n017-massaccesi-h052-agreement`, one of
the two frontier evidence entries behind `T-015`; both entries are exact-algebraic
event-cell sweeps over the same reduction, which is why the confidence rung there is
`C3` and not `C4`.

**How independent, exactly.** Accumulation-level, over a *shared* reduction.
Of a `DirectionManifest`’s ten fields, eight — `label`, `direction`, `x_events`,
`y_events`, both event hashes, `event_cell_count` and `evaluated_state_count` — are
outputs of the shared `reduce_event_cells` and are equal by construction; only `minimum`
and `witness` come from different code.
The two paths also share the fixture, the canonical model, the preconditions and the
mutation guards, so an error in the reduction, the fixture reconstruction, the
projection convention, the preconditions or the guards would appear in both paths
identically. The criterion’s frozen phrase “event-cell reductions” is not edited; read
it, here and downstream, as **over the same event-cell reduction**.

**What the residual comparison can and cannot catch**, measured rather than argued.
The reviewer injected three defects into a copy of the sweep and compared against the
frozen independent path on the real direction 0: dropping the second cumulative pass and
flipping the sign on one difference-array corner were both detected; extending every
rectangle’s top edge by one event was **not**. A defect that only raises masses at
non-minimizing cells is invisible to a comparison of minima, which is a scope statement
rather than a flaw — and every lower-bound check in this lane inherits it.

**Three limitations carried, none of which prevented clearance**, all recorded in
`exp-059`’s amendment: `validate_result` does not tie the rebuilt chain spine to the
carried boundary, now filed as [`D-428`](../../../defects.md); there is no assembly path
from a retained disagreement, and re-issuing the identical command after an exit 3
continues past it rather than refusing; and the independence is the accumulation-level
independence described above.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
