---
title: H-333 — which hand lemmas of the n17 proof formalise in Lean within a day each
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-333
  kind: open_question
  claim: >-
    Of the hand lemmas the n17 argument rests on, which admit a Lean 4 proof against
    Mathlib within one agent-day each, with the statement audited against the record's
    wording: the depth-width wall lemma of the cover; the centred-container lemma (every
    packing of side at most V embeds concentrically in the U-container with its centres in
    the centre box); the separation lemma of the slide-coverage tool; the D4 transfer of
    occupancy states; and recipe lemmas 1 to 6 of the local theorem (necessary local
    system, two-row reduction, tightness along the family, existence of coordinate duals,
    the ratio test with residual, the angle chart modulo a quarter turn)?
  lane: proof
  derived_from: [X-051]
  instrument: >-
    A Lean 4 project pinned to the toolchain of the n11 formalisation audit, one file per
    lemma, built with an axiom receipt; the statement-fidelity audit of each file by a
    reviewer who is not its author.
  instrument_ready: false
  regime: >-
    The lemmas as stated in the depth-width wall lemma review, the proof-interfaces
    document, the composition review and the recipe review; no certificate replay is
    formalised, only the hand layer.
  instance: {axis: n, point: 17}
  priority: 3
  cost_estimate: 10 to 30 agent-hours for the first three lemmas; the six recipe lemmas separately, after the first three price the work.
  prereqs: []
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-051's route K. The hand layer is what a reader of the final proof must take on
    one AI review; the lemmas are short real-analysis statements about squares,
    half-planes and supports, and the n11 formalisation establishes the conventions. An
    open question because the answer is a list, not a verdict; the first discriminator
    is whether the wall lemma and the centred-container lemma close in a day.
---
# H-333: Mechanising the Hand Layer

**Mechanism.** Every n17 certificate is machine-checked, but the lemmas that say what
the certificates mean (why a cell holds at most one centre, why a state read in the
centred box is the state the certificate excludes, why a shrunk nominal square lies
inside the moved one) are hand proofs with one review each.
They are short, and the n11 Lean work supplies the vocabulary.

**First discriminator.** The depth-width wall lemma and the centred-container lemma,
each in one day with an axiom receipt and a statement audit.

**Expected information.** How thin the trusted hand layer of a foolproof package can be
made, and at what price.

**Limits.** Formalising the lemmas does not formalise the checkers or the composition; a
lemma that resists in a day is deferred, not refuted.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
