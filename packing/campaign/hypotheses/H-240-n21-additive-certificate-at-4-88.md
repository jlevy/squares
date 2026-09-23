---
title: H-240 — a point certificate reaches s(21) >= 122/25
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-240
  kind: hypothesis
  claim: >-
    A weighted fractional unavoidable-set certificate with point atoms on a
    window-enriched site set retains at n=21, side 122/25 = 4.88, shrink 9977/10000,
    with total mass strictly below 21.
  lane: search
  derived_from: [X-047, X-044]
  criterion:
    shape: determination
    metric: >-
      The decide_certificate verdict on a frozen certificate produced by
      run_fractional_colgen at (n, L, B) = (21, 122/25, 9977/10000)
    direction: >-
      Confirm only on RETAINABLE from decide_certificate with mass below 21, followed
      by a Fable max W2 review before any register entry. Reject the named site sets,
      not the target, when the converged value is at least 21 on two distinct site sets
      or the run returns the grid. A timeout decides nothing.
    threshold: 21
  instrument: >-
    devtools/run_fractional_colgen.py with window-enriched grids, freeze, and
    devtools/decide_certificate
  instrument_ready: true
  regime: >-
    n=21; side 122/25; shrink 9977/10000; 181-direction net unless the run log states
    otherwise; point atoms only; D4-symmetric nonnegative weights; exact decision
  instance: {axis: n, point: 21}
  priority: 2
  cost_estimate: One or two runs of at most 3,600 s each, then the decision gate
  prereqs: [think-nbij]
  replication: false
  registered: '2026-09-23'
  notes: >-
    X-047 estimates the additive crossing at n21 near 4.886 because its budget sits far
    above the T-021 mass that pins n20; the estimate is not a bound and 4.88 is frozen
    below it. X-047's lane table wrote the side as 22/5, which is 4.4; the target is
    122/25.
---
# H-240: A Point Certificate at s(21) ≥ 4.88

X-047’s additive-ceiling map finds n21 to be the one low case with real additive
headroom: its charge slack is 5.48 per cent, 36 times n20’s. The claim uses only stock
instruments, so it runs as soon as it is registered, beside the n11 lanes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
