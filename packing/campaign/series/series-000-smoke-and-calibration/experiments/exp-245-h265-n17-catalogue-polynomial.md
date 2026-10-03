---
title: "exp-245 — n17 catalogue polynomial identity"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-245
  series: series-000
  title: Exact identification of the certified n17 side with the catalogue's degree-18 polynomial
  date: '2026-10-02'
  hypotheses:
  - H-265
  tier: confirmatory
  subject:
    label: The H255 chart polynomials Pi2 and Pi3 bound to the exp-237 certificate, the substitution
      S = (6 + 4t)/(1 + 2t - t^2), and the degree-18 polynomial recorded in packing/frontier/n-017.md.
    engine: devtools.check_n17_catalogue_polynomial, with an independent review that recomputed every step
      in separate code
    assurance: verified
    method: exact-algebraic
    host_system: Linux x86_64 remote session container, project Python 3.14.7, sympy, one worker
    selftest_passed: true
    engine_commit: 603d5cb36ed3c9195513956cd5b5c20e5f2cddda
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: A hand-derived toy chart with root 1 + sqrt(13), perturbed catalogue polynomials, a rootless
      box, swapped formulas, an unpassed certificate and malformed inputs are all handled as required.
      Twenty-four tests, ruff and BasedPyright clean.
    candidate: Resultant elimination of b, then t; exact factorization over Q; exact root isolation in the
      outward image of the H255 box; irreducibility by factorization and a Rabin test mod 7; a second
      elimination order with a rigorous cofactor exclusion.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 167; lane C built the instrument, the coordinator ran it from a clean worktree
    entry_point: packing/devtools/check_n17_catalogue_polynomial.py
    command: 'From packing: .venv/bin/python3 -m devtools.check_n17_catalogue_polynomial --output FILE.
      Exact line in run-001 command.txt.'
    budget: One short build slice; seconds of exact algebra.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-245-n17-catalogue-polynomial/run-001
    dirty: false
    commit: 603d5cb36ed3c9195513956cd5b5c20e5f2cddda
  results:
  - shape: determination
    role: outcome
    question: Is the factor vanishing at the certified side the catalogue's polynomial, and is it irreducible?
    outcome: criterion_met
    checked_by: The degree-28 side resultant factors as four squared extraneous factors and one degree-18
      factor, the only one with a root in the outward image of the H255 box; it equals the n-017.md
      polynomial with rational unit 1. Irreducible over Q by factorization and by Rabin tests mod 7 (tool)
      and mod 7, 103, 167 and 173 (review). The review's own resultant chain, Sturm counts and second
      elimination route agree.
  verdict:
    decision: accepted
    primary_criterion: The vanishing factor equals the catalogue polynomial up to a rational unit, the
      polynomial is certified irreducible, and an independent check agrees.
    reason: Every clause holds. S* is an algebraic number of degree 18 with the catalogue's polynomial as
      its minimal polynomial. No packing, feasibility or optimality claim; the admitted rational ceiling
      and the open status of s(17) are unchanged.
    needs_review: false
    commit: 603d5cb36ed3c9195513956cd5b5c20e5f2cddda
  effort:
    timebox: 60 seconds; one worker
    wall_seconds: 0.75
    stopped_by: criterion
---
# exp-245: n17 Catalogue Polynomial Identity

[H-265](../../../hypotheses/H-265-n17-catalogue-polynomial-identity.md) asked whether
the side of the certified n17 chart root is exactly the algebraic number the catalogue
reports. Until now the record could only say that the two agree to every printed digit.

## Outcome

It is the same number.
The chart polynomials’ resultant has one irreducible degree-18 factor with a root at the
certified point. Mapped to the side, that factor is the catalogue’s polynomial
coefficient for coefficient.
The
[independent output review](../results/exp-245-n17-catalogue-polynomial/output-review.md)
reproduced every step in its own code, by a separate resultant chain and Sturm sequence
and a second elimination order, and certified irreducibility at four primes.
It encloses $S^\ast=4.6755300936045509516341112704831466487671\ldots$ to width
$10^{-40}$.

This closes the identification half of the blocker recorded in
`packing/frontier/n-017.md`. The frontier text is unchanged in this session, and its
update is tracked separately.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
