---
title: H-335 — the Rust and Python kernel verifiers agree on every admitted entry and refuse every mutant
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-335
  kind: hypothesis
  claim: >-
    The Rust kernel-certificate verifier merged in PR 410 and the Python standing
    verifier devtools/verify_n17_kernel_certificate.py produce the same mathematical
    receipt (every field outside provenance, directory and timing) on all kernel-format
    entries of the admitted ledger in full mode, and both refuse all of a suite of 30
    corrupted objects (a dropped row, a widened cover, a moved core plane, a changed
    cell, a truncated node, an unsound partner cover, and the like) with a named reason.
  lane: proof
  derived_from: [X-051]
  criterion:
    shape: determination
    metric: >-
      Receipt equality outside the declared provenance fields on every kernel-format
      admitted entry; the refusal verdict of both verifiers on each of 30 mutants; wall
      time and peak RSS of each verifier per entry.
    direction: >-
      Confirm when every receipt pair agrees and every mutant is refused by both. One
      disagreement or one accepted mutant refutes it and names a defect in one verifier.
    threshold: all kernel-format entries agree; 30 of 30 mutants refused by both.
  instrument: >-
    The n17_kernel_verify crate at main and the Python verifier at main, run on the
    retained objects once they are fetchable (H-336); a mutation generator in the
    pattern of the W7 and A mutation suites.
  instrument_ready: true
  regime: >-
    n = 17; the H-266 cover at U; kernel-format entries only (the BB format's second
    checker is a separate obligation); ordinary-U container; the centred hull-48 parent
    is out of scope until the Rust verifier supports it.
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: About the Python verifier's full-mode cost per entry (0.10 to 0.18 s a row) plus the Rust cost; a day of two workers for the ledger; one slice for the mutants.
  prereqs: [H-336]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-051's route J. PR 410 reports receipt parity on seven certificates and remains
    unadopted; same-object parity on the whole ledger and a shared mutation suite are
    what make the second checker load-bearing. A foolproof package needs two
    independent checkers per certificate format; this supplies the kernel format's.
---
# H-335: Two Checkers for Every Kernel Certificate

**Mechanism.** Two implementations that share no code and agree on every admitted object
reduce the trust in either to the trust in their common specification; a mutation suite
both refuse shows the agreement is not vacuous.

**Falsifier.** A receipt disagreement or an accepted mutant.

**Expected information.** Whether the standing admissions, 21 sub-patterns and 39 whole
states, rest on two checkers or one.

**Limits.** The Rust verifier does not yet read the centred container or the 48-vertex
hull allowance, so the capture-side objects are out of scope; the branch-and-bound
format needs its own second checker, for which the contributor’s Rust checker is a
candidate that has had no input or schema review here.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
