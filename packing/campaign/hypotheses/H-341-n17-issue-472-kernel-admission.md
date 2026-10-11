---
title: H-341 — the twelve kernel certificates of issue 472 replay in full and admit
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-341
  kind: hypothesis
  claim: >-
    Each of the twelve kernel certificates reported in issue 472 (masks 214101,
    14353473, 983396, 3869440, 5707072, 6177056, 7815200, 1000708, 935012, 7799616,
    5116178 and 4657489 on the H-266 cover at U = 1169/250), fetched by digest from the
    contributor's HostedData/v1 manifests, passes devtools/verify_n17_kernel_certificate
    in full mode from a clean worktree (dirty: false) under a verifier blob the ledger
    lists, passes the Rust kernel verifier of PR 410 with receipt parity outside the
    provenance fields, binds to the exp-247 cover's 24 polygons and the cap U, touches no
    image of the family's state, and their admission makes the census consumer report
    3,636 orbits and 28,528 states with the distance-2 tail at 94 orbits and 736 states.
  lane: proof
  derived_from: [X-052]
  criterion:
    shape: determination
    metric: >-
      Per certificate: digest match against the contributor's manifest; the standing
      verifier's full-mode verdict, wall time and peak RSS from a clean worktree; the Rust
      verifier's verdict and receipt parity; the endpoint-state control (the census
      refuses any entry touching the family's state). After admission: the census
      consumer's orbit and state counts and the distance partition.
    direction: >-
      Confirm when all twelve pass both verifiers with parity, none touches the family's
      state, and the census reports 3,636 / 28,528 with the distance-2 tail at 94 / 736.
      A full-mode refusal, a parity disagreement or a census mismatch refutes it for that
      certificate; the others are still admitted and counted.
    threshold: >-
      12 of 12 full-mode passes; 12 of 12 Rust parity; census 3,636 orbits / 28,528
      states; distance-2 tail 94 / 736.
  instrument: >-
    devtools/verify_n17_kernel_certificate.py in full mode at a listed blob (1ad706c21
    at commit 601bbf110, or main's be8135f6e once a listing with a review pointer is
    added); the n17_kernel_verify crate of PR 410; sqpack.hosted_data for the fetch and
    digest check; devtools/census_n17_certified.py for the join and the endpoint
    control.
  instrument_ready: true
  regime: >-
    n = 17; the H-266 cover in the U frame; the contributor's objects at the digests the
    issue-472 manifests pin (411,682,476 bytes in all); one full replay per certificate
    on a host with 16 GB; the ledger's admission rule unchanged.
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: >-
    About 1.9 CPU-hours of full verification at the contributor's timings (147 to 1,618 s
    each), minutes for the Rust verifier, and about 4 agent-hours for custody, the
    verifier listing decision, the joins and the admission review.
  prereqs: [H-266, H-267]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-052's direction 1. The contributor made these with the repository's own producer
    (devtools/check_n17_subpattern, mode A) and passed them with the standing verifier
    at blob 1ad706c21, the listed kernel-streamed version that admitted every entry
    since exp-251. The global-side review of 9 October projected them exactly onto the
    60-entry ledger: -1,047 orbits and -8,240 states, every "alone on main" figure in
    the issue reproduced, row 34 contained in the admitted s182-m7844815 which it
    subsumes, and row 23 (mask 935012) the only one touching the distance-2 tail (orbit
    1965787). The receipts the contributor supplied carry dirty: true, a wrapper
    revision and one hand-edited directory field each, which is why a clean-worktree
    replay is the admission step rather than the receipts themselves. H-332 covers the
    BB-format contributor certificates; this is the kernel-format batch.
---
# H-341: Admitting the Batch a Contributor Already Verified

**Mechanism.** A kernel certificate’s meaning is fixed by the frame the verifier binds
(the cover’s 24 polygons, the cap, the mask) and by the closure the verifier derives;
the producer’s identity is irrelevant to soundness.
These twelve are in the format and frame of 59 admitted entries and were passed by the
listed verifier blob; what the ledger’s rule still lacks is a clean replay, parity on a
second implementation, custody the census can read, and an admission record.

**Falsifier.** A full-mode refusal on any object, a receipt disagreement between the
Python and Rust verifiers, an entry touching the family’s state, or a census count that
differs from the projection.

**Expected information.** The largest exclusion movement available to the program for
the smallest cost, and the admission path exercised on externally produced objects.

**Limits.** Containment projections become census facts only through the admission
round; the verifier listing for `main`’s current blob is a review decision this
hypothesis does not make.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
