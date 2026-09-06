---
title: H-093 — the scalar certificate language reaches 61/16 for n = 11
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-093
  kind: hypothesis
  claim: >-
    At container side 61/16, the retained 181-direction net and scalar core side
    B = 9977/10000 admit a finite D4-invariant measure of nonnegative rational
    point atoms with total mass strictly below eleven and mass at least one in
    every admissible core. Such a certificate proves s(11) >= 61/16.
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:21', 'proof:22']
  criterion:
    shape: determination
    metric: exact scalar certificate at side 61/16
    direction: >-
      Accept only after the rationalized certificate passes the production sweep
      and interval decisions and the standalone verifier, including complete
      coverage and total mass below eleven. Reject only upon an exact
      verify_ceiling family at this side, core side and net with maximum
      pointwise depth at most one and total weight at least eleven.
    threshold: exact certificate at side 61/16 with total mass strictly below eleven
  instrument: >-
    The existing frozen scalar 61/16 recipe using packing/devtools/run_fractional_cutting.py,
    its seed certificate, packing/devtools/freeze_cutting_primal.py, and the existing
    declaration, production decision and standalone verification commands.
  instrument_ready: true
  regime: >-
    n = 11; side 61/16; B = 9977/10000; the retained rational 181-direction net;
    exact rational certificate decisions and the unchanged scalar recipe.
  instance: {axis: side, point: '61/16'}
  prereqs: [BC-250 publication, frozen scalar recipe and fresh output paths]
  registered: '2026-09-06'
---
# H-093 — A Scalar Certificate at 61/16

The [scalar probe in Agenda 025](../agendas/agenda-025-adaptive-fractional-frontier.md)
tests the first selected side between the retained 3.81 certificate and the unfinished
3.82 bracket. The
[continuation addendum](../../../docs/project/handoff-2026-09-06-post-381-t2-t10-continuation.md)
owns its literal command, seed mapping and cooperative process deadline.

A row-converged objective below eleven starts the existing rationalization and
verification sequence; it does not establish the bound itself.
A timeout, missing convergence or finite-site optimum above eleven leaves this existence
claim unresolved. An exact ceiling closes only the declared scalar formulation.

Stop variant search when a candidate requires BC-238 review.
Exact basis recovery may support that candidate if rounding consumes its margin.
A different side, net or core mechanism requires a prospective claim; H-064’s 3.85
ceiling and H-090–092’s fixed-weight probes retain their original scopes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
