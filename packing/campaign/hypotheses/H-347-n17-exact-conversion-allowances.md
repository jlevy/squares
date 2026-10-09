---
title: H-347 — the capture-to-local conversion allowances are exact and small
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-347
  kind: hypothesis
  claim: >-
    For each of the 45 non-slider coordinates of the local family theorem, the
    allowance E_j that converts a capture radius delivered in the U' numeric-cap frame
    (angles as owner intervals, positions as cell-relative bounds, the D4 group element
    carried) into the exact root's frame with H254 angle lifts, including the u*
    enclosure charge E_u M_i + ||u*||_1 E_i of the proof-interfaces contract and the
    exp-237 root-box residual, computes exactly in rationals from the retained receipts
    and is below one tenth of the per-coordinate radius r_j of the 1/1216 vector.
  lane: proof
  derived_from: [X-052]
  criterion:
    shape: determination
    metric: >-
      The 45 exact rational values E_j with their derivation receipts; the ratio E_j /
      r_j for the 1/1216 vector and for the uniform 1/5000 radius; the group element and
      frame identities the conversion used.
    direction: >-
      Confirm when every E_j is exact and below r_j / 10 for the 1/1216 vector. Any
      E_j at or above r_j / 10 refutes the claim and shrinks the terminal target the
      capture receipt must deliver to r_j - E_j, which the record must then state.
    threshold: 45 of 45 exact; max E_j / r_j < 0.1 on the 1/1216 vector.
  instrument: >-
    Unbuilt: a devtools module reading the exp-237 root box, the H254 lift conventions
    of devtools/check_n17_local_minimum.py, the exp-276 and exp-280 frame identities and
    the proof-interfaces contract's allowance formula, in exact Fraction arithmetic; its
    receipt becomes the allowance table the composition checker (H-334) consumes.
  instrument_ready: false
  regime: >-
    n = 17; the family's state; cap U'; the exact root's frame; the per-coordinate
    radius vector of H-340 and the uniform 1/5000 radius as the two targets.
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: 10 to 20 agent-hours; seconds to run.
  prereqs: [H-288, H-340]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-052's item 3 of the minimum set. The proof-interfaces contract states the
    allowance and charges it to capture; no receipt computes it, and the composition
    cannot be written without it. The local-side review of 9 October found the frame
    joins correct (centred container, f1 canonicalisation, slider premises) and the
    allowance the one unwritten number between a capture receipt and the local theorem.
---
# H-347: The Number Between Capture and the Local Theorem

**Mechanism.** The local theorem is stated at the exact root in the H254 lift chart; a
capture receipt is stated at the numeric cap in owner intervals and cell-relative
bounds.
The conversion is linear in the root-box width, the frame offset and the $u^\ast$
enclosure, and every ingredient is a retained rational.

**Falsifier.** An allowance at or above a tenth of its coordinate’s radius.

**Expected information.** The terminal target capture must actually deliver, coordinate
by coordinate, and the first receipt in the composition’s format.

**Limits.** It computes nothing about capture; it fixes what capture is asked for.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
