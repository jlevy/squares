---
title: "agenda-011 — the verification review: determinations, not deferrals"
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-011
  title: "The verification review: determinations, not deferrals"
  updated: '2026-08-31'
  status: active
  objective: >-
    The owner's direction after the agenda-010 run closed: stop deferring
    verification to owner review. Apply the project's own assurance rubric --
    conventions.md section 4 (reported / numerically-checked / verified, with
    method and origin as separate recorded facts) plus the frontier evidence
    contract -- to each of the run's six held results, and make the
    verified/not-verified call. Where independence is insufficient for a call,
    build the independent verification rather than flagging it; where the rubric
    itself is ambiguous, surface the ambiguity explicitly in the review document
    rather than deciding it silently. The owner reviews the assembled case on
    PR #66 afterward; nothing in this agenda waits on that review to land.
  items:
  - id: BC-106
    purpose: measurement_validation
    owner_focus: correctness
    instances: [13, 17, 18, 46]
    state: complete
    priority: 0
    question: >-
      Which of the agenda-010 run's six held results are verified under the
      repository's own assurance rubric, and what independent verification does
      each call rest on?
    hypotheses: []
    budget: >-
      about 210 minutes, W2 with one W7 instrument slice, in slices of 45
    entry: >-
      Six results are held unresolved with needs_review: Theorem 8 certifying
      as printed; the exp-046/H-044 verdict; the Lemma 10 settlement; the
      s(17) >= 17/4 and s(18) >= 17/4 certificate; the m = 8 sizing statement;
      the tau* diagnostic. The rubric already exists -- assurance `verified`
      means an exact check, rigorous certificate, or complete proof decides the
      claim and its preconditions, with verification origin recorded separately
      -- and the independence picture differs per result: the three Bentz
      results have the published proof as an independent derivation on one side
      of the comparison, while the green17 certificate is first-party with no
      external derivation, so it is the one place a second, code-independent
      formal method is needed before a frontier move.
    exit: >-
      A determinations review document under docs/project/reviews/ stating the
      rubric, the per-result call, and the evidence chain each call rests on;
      the register and evidence moves those calls imply (frontier
      verified_lower_bound at n = 17 and n = 18 gated on the independent
      interval certifier passing; audit evidence entries at n = 13 and n = 46;
      the exp-046 verdict resolved under H-044's registered amendment; the
      Lemma 10 source-layer settlement recorded); every needs_review hold from
      the run either resolved or replaced by a typed final status; validation
      green and PR #66 refreshed with the assembled case.
    bead: think-ngf0
    depends_on: []
    workflows: [factual-review, pipeline-improvement]
    next_evidence: >-
      Discharged 2026-08-31 by session-060. All six determinations are final:
      Theorem 8's audit verified (E-bentz46-theorem8-audit); the Lemma 10
      settlement verified and source-settled against the published page image
      (journal transposition; E-bentz13-figure2-audit, defect-found on
      E-bentz-2010-proof); exp-046 resolved with H-044 undisposed by its
      registered amendment; the m = 8 statement standing as exact arithmetic;
      the tau* diagnostic typed uncertified-final. The green17 determination
      became an upgrade: the independent interval certifier proved 17/4 was
      the cell plan's ceiling, both methods now certify 4426213/1000000, and
      verified_lower_bound moved at n = 17 and n = 18 on two independent
      formal methods; the exact ceiling 753/250 + sqrt 2 is bracketed and
      typed on think-iye2. The assembled case is
      docs/project/reviews/review-2026-08-31-overnight-run-verification-determinations.md;
      the owner reviews the PR as a whole.
    artifacts:
    - cases/green17/interval_audit.py
    - campaign/agent-sessions/session-060-verification-review.md
    - frontier/evidence.yaml
---
# Agenda-011 — The Verification Review

One cell: the owner moved the review from their queue to the repository's own
rubric, so the six held results get determinations here, with the independent
interval certifier built where first-party independence was missing.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
