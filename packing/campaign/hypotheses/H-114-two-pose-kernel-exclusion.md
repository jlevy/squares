---
title: H-114 — a two-pose kernel can exclude eleven squares
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-114
  kind: open_question
  claim: >-
    Can a small explicitly fixed two-pose feature family at side 96/25 yield a
    symmetric kernel K with K-1 positive semidefinite, diagonal at most b < 11,
    and nonpositive values on every distinct compatible pair of contained unit squares?
  lane: proof
  derived_from: [X-017]
  instrument: >-
    Proposed feature-family SDP proposer, adversarial compatible-pair separator,
    exact PSD evidence and independent continuum diagonal/pair verifier.
    A finite necessary-constraint obstruction is an alternative discriminator.
  instrument_ready: false
  regime: >-
    n=11 at side 96/25; full bounded pose domain, including walls and legal touching
    pairs; only joint D4 symmetries may reduce a pair
  instance: {axis: n, point: 11}
  priority: 2
  cost_estimate: price one small fixed feature family before building a general hierarchy
  prereqs: [reviewed kernel bound, prospectively fixed features and exact acceptance contract]
  replication: false
  registered: '2026-09-07'
  notes: >-
    This is an interaction kernel, not H-096's inner witness geometry. Register a
    concrete feature-family claim before running its target. No theorem promises
    that a low-degree family is adequate or that pair separation is inexpensive.
---
# H-114 — A Small Interaction-Kernel Discriminator

[X-017](../explorations/X-017-compatibility-and-complete-case-covers.md#c-two-pose-kernels-a-separate-bounded-opportunity)
states the proof obligations and stop conditions.
[Agenda 027](../agendas/agenda-027-compatibility-and-restricted-families.md) keeps the
pilot independent of success on the angle-family theorem.

Session095 selected BC264's bounded pricing. Session097 completed it with an
[exact cubic-feature obstruction](../series/series-000-smoke-and-calibration/results/agenda-027/bc-264-kernel-feature-design.md#an-exact-obstruction-before-any-solver)
and an independently admitted eleven-feature proposal.
The obstruction excludes center-polynomial restrictions of total degree at most three
on one fixed-angle fiber, not all finite features or H114 itself.
The [independent admission](../series/series-000-smoke-and-calibration/results/agenda-027/bc-264-kernel-acceptance-review.md#post-freeze-admission-the-finite-lp-instrument)
permits a source-free finite refutational LP instrument and a separate exact reader.
No target has been admitted.

An exact finite necessary-constraint obstruction needs a prospectively fixed family,
source-bound rows and an independently checked objective certificate.
It does not need a continuum verifier because it rejects that family.
A positive full-domain certificate still needs exact PSD evidence and complete diagonal
and compatible-pair coverage; that continuum cost remains unknown.

A sampled PSD matrix is only a proposal, and feasibility of the weaker outer LP does
not even establish PSD or supply a kernel candidate.
Acceptance requires exact positive semidefiniteness and inequalities on the full
diagonal and compatible-pair domains.
An exact finite necessary-constraint obstruction can reject the chosen feature family;
failure of a heuristic separator cannot.
At the Trump side a sound control cannot produce b below eleven.
A certificate with b equal to eleven there does not prove s(11)=U.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
