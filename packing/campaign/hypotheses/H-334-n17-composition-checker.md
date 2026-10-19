---
title: H-334 — a composition checker derives the residue and the theorem from the receipts and refuses every mutant
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-334
  kind: hypothesis
  claim: >-
    A composition checker that reads the cover receipt, the admitted ledger with an
    explicit cap on every entry, the near-endpoint stage, the capture receipt and the
    local-theorem receipt reproduces the current residue (4,683 orbits, 36,768 states at
    cap U), states which orbits remain open and at which cap, refuses a ledger with one
    entry removed, one cap raised above the composition's cap, or one certificate digest
    changed, and refuses a missing capture or local receipt; and when every orbit is
    closed it emits the theorem statement with the trusted-base inventory.
  lane: proof
  derived_from: [X-051]
  criterion:
    shape: determination
    metric: >-
      The checker's output on the current receipts; a mutation suite of at least twelve
      objects (entry removed, cap raised, digest changed, orbit double-counted, D4 image
      missing, cell renamed, cover receipt altered, capture receipt absent, local receipt
      at the wrong frame, per-entry cap absent, state read in the wrong box, endpoint
      state admitted); an independent review of the composition rule it encodes.
    direction: >-
      Confirm when the current residue is reproduced exactly, every mutant is refused
      with a named reason, and the review finds no defect in the rule. Any accepted
      mutant refutes it.
    threshold: exact residue; 12 of 12 mutants refused; review accepted.
  instrument: >-
    Unbuilt: a devtools module in the pattern of check_n11_final_composition.py and
    inventory_n11_completion.py, extending census_n17_certified.py with per-entry caps
    and the capture and local joins; its tests.
  instrument_ready: false
  regime: >-
    n = 17; the H-266 cover; the 60-entry ledger at registration; receipts pinned by
    mathematical state identity, not by timing fields; no geometry rerun.
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: One or two W7 slices plus review; 20 to 40 agent-hours.
  prereqs: [H-266, H-267, H-288]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-051's route J. The explainer's item 4 says the composition has never been written
    down; this makes it a program whose refusals are tests. Per-entry caps are needed
    before the cap ladder (H-326) or the near-endpoint stage at U' exists, since today
    every entry's cap is the implicit U. The checker trusts the verifiers' receipts; it
    does not rerun geometry, as the n11 composer does not.
---
# H-334: The Proof as a Checkable Object

**Mechanism.** The global half is a finite statement: every orbit is excluded at some
cap at least $S^\ast$ or captured into the local box, and the local box has side exactly
$S^\ast$. A checker that reads the receipts and derives that statement turns the record
into a proof; its refusals are what make the composition rule testable before the
mathematics is complete.

**Falsifier.** Any mutant accepted, or a residue count that differs from the census
tool’s.

**Expected information.** None mathematical; the proof becomes an object a reader can
run, and the joins the proof-interfaces document lists become refusals rather than
prose.

**Limits.** The checker is only as sound as the receipts it trusts and the rule it
encodes; the rule needs its own review, and the receipts need the custody of H-336.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
