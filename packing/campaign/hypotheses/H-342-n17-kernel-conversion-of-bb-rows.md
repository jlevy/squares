---
title: H-342 — the kernel producer closes most wall-anchored issue-413 rows that only branch and bound has reached
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-342
  kind: hypothesis
  claim: >-
    Of the issue-413 rows whose only reported evidence is a branch-and-bound
    certificate checked by the contributor's fast verifier, a parallel node check, or a
    computation without a certificate (rows 3 to 22, 26 to 28, 32, 15, 27 and 33 at the
    38-row roster), those with at least one wall cell among their named cells close under
    devtools/check_n17_subpattern in mode A (64 or 128 bins, SW9's adaptive rows) within
    30 minutes of production each in at least two thirds of cases, with a certificate
    under 100 MB that the standing kernel verifier passes in full.
  lane: proof
  derived_from: [X-052]
  criterion:
    shape: determination
    metric: >-
      For each eligible row: the producer outcome (closed, stalled, time cap), production
      wall time, certificate size, the full-mode verifier verdict and time; the count of
      eligible rows fixed before the first launch from the roster's named cells.
    direction: >-
      Confirm when at least two thirds of the eligible rows close within 30 minutes with a
      certificate under 100 MB and a full-mode pass. Fewer than two thirds refutes the
      claim and says which crowds the kernel cannot reach, routing them to the branch
      and bound or to H-344.
    threshold: at least 2/3 of eligible rows; 30 minutes each; under 100 MB; full-mode pass.
  instrument: >-
    devtools/check_n17_subpattern.py mode A with --bins 64 or 128 and the adaptive-row
    options SW9 used; devtools/verify_n17_kernel_certificate.py in full mode;
    devtools/census_n17_certified.py for the marginal count of each closure.
  instrument_ready: true
  regime: >-
    n = 17; the H-266 cover at U = 1169/250; the issue-413 roster as read on 9 October
    (38 rows), the eligible set frozen from its named cells; one production run per row
    at each of the two bin counts at most; closures admitted only after a full-mode
    pass.
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: >-
    About 10 CPU-hours of production and verification over the eligible rows at the
    issue-472 timings (2 to 18 minutes production, 2 to 27 minutes verification each);
    about 6 agent-hours for the roster freeze, launches and admission rounds.
  prereqs: [H-341]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-052's direction 1, second half. Issue 472 showed twelve of twelve arity-8 and 9
    selector flags with wall cells closing under the kernel in minutes with certificates
    of tens of megabytes, where the same patterns as branch-and-bound certificates run
    to tens or hundreds of gigabytes (row 33's estimate: 116 million nodes, 480 GB). The
    contributor is already retrying row 33 with the kernel producer. If the rule holds,
    branch-and-bound custody and verification cost matter only for genuinely interior
    crowds, where B2 (H-331) matters.
---
# H-342: Route Wall Crowds to the Kernel

**Mechanism.** A wall cell gives the ownership induction owned points from the seed: the
half-extent of a square in a closed wall row is bounded by the proved quadratic, so the
wall-side cells carry cores the interior cells lack.
Every arity-8 and 9 flag with a wall cell that the contributor ran closed in minutes.

**Falsifier.** Fewer than two thirds of the eligible rows close within the ceilings.

**Expected information.** About a thousand more orbits of residue removed by the engine
that works, and a measured routing rule between the two provers.

**Limits.** Interior crowds (pattern A’s kind, issue 358’s two classes with five
interior cells) are out of scope and stay with the branch and bound; a closure is an
admission only after the standing verifier’s full pass.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
