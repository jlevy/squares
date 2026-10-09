---
title: H-340 — the composed local theorem holds with every coordinate at least 1/1216
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-340
  kind: hypothesis
  claim: >-
    The capture-target theorem holds with the per-coordinate radius vector of the local
    radius review: every one of the 45 non-slider coordinates at least 1/1216, omega11 at
    85/16 of that, u11 at 33/16, omega8 and xi8 at 71/64 and omega16 at 67/64, on the
    slider box B_c = [0, 4/25] x [-1/128, 11/100] x [-13/200, 1/30], with the slide
    coverage at R = 9/2048 certifying a in [0, 4/25], b in [-0.0074162, 11/100] and z in
    [-13/200, 0.0314109]; both receipts pass exactly from a clean worktree and every
    control is refused.
  lane: proof
  derived_from: [X-051]
  criterion:
    shape: determination
    metric: >-
      The ratio receipt of devtools/check_n17_local_radius.py at the frozen vector and
      box (worst ratio, cell count, every recipe item C1 to C12 that the wrapper runs)
      and the slide-coverage receipt at R = 9/2048 with its thresholds, both produced
      from a clean worktree at the registration commit.
    direction: >-
      Confirm when both receipts pass with every control refused. A failed item refutes
      the vector as frozen; no retune after the result.
    threshold: worst ratio below 1 on every cell; every control refused; the certified slider box contains the composed box.
  instrument: >-
    devtools/check_n17_local_radius.py ratio and shape modes at the frozen vector, and
    devtools/check_n17_slider_coverage.py run at R = 9/2048 with thresholds a <= 2/5,
    z >= -1/10, b <= 3/20 and tight ones 4/25, -13/200, 11/100, as the review's section 4
    records.
  instrument_ready: true
  regime: >-
    n = 17; the exact root; the H258 roster minus the six zero-weight rows; the H254
    labelling; square 6 confined to side-S2 for the slide coverage.
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: Minutes of exact arithmetic; one registered round.
  prereqs: [H-261, H-268]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-051's route C, prerequisite. The local radius review computed these receipts on 3
    October (worst ratios 0.999317 and 0.999368) and held the vector as a component
    because nothing downstream used it and because it was found against the same
    instrument. H-329 and H-330 use it, so it becomes load-bearing; registering it as
    a round, as exp-248 was, is the honest way to carry it. The frozen vector is the
    review's, unshaved; a shaved copy would be a new registration.
---
# H-340: A Larger Terminal Box, Registered

**Mechanism.** The softest direction $-\omega_{11}$ draws its dual mass from rows that
do not touch square 11, so widening $\omega_{11}$ alone divides its ratio; the local
theorem then passes with every coordinate four to five times wider than $1/5000$, and
the slide coverage composes on a wider slider box.

**Falsifier.** Any recipe item or control failing at the frozen vector from a clean
worktree.

**Expected information.** A registered terminal target of $8.2\times10^{-4}$ in most
coordinates and $4.4\times10^{-3}$ in $\omega_{11}$, which H-329 and H-330 take as their
inner radius.

**Limits.** The ratios sit within $10^{-3}$ of one, so the vector cannot be changed
without a re-run; the frame, cap and $u^\ast$-enclosure obligations are unchanged.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
