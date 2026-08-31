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
  - id: BC-107
    purpose: measurement_validation
    owner_focus: correctness
    instances: [17, 18, 46]
    state: complete
    priority: 0
    question: >-
      Can the epistemic vocabulary the verification review applied by hand
      become a codified, machine-enforced rubric -- so a result's verification
      and confirmation levels are granted by the gate rather than by anyone's
      judgment, and the repository presents its results in one prioritized,
      structured surface?
    hypotheses: []
    budget: >-
      about 240 minutes, W7, in slices of 45
    entry: >-
      The 2026-08-31 verification review surfaced four rubric gaps and showed
      the cost of scattered epistemics: the atoms live across five evidence
      fields, conventions.md section 4 carries semantics outside its
      formats-and-naming scope, results have no first-class record (the
      identity table reserves T-N with no registry behind it), and a visitor
      cannot tell from the README whether the project carries novel results.
      The owner approved the design: a root epistemics.md owning four axes --
      verification V0-V5 (of the claim, anywhere), confirmation C0-C5 (ours,
      end-to-end, each rung a conjunction of machine-checkable predicates),
      significance S1-S5 (declared, anchored, never gating), novelty (the
      existing enum) -- with a T-NNN results register, a derivation checker
      that fails on declared rungs the atoms do not support, a generated
      RESULTS view, and README/SYNOPSIS orientation.
    exit: >-
      epistemics.md landed as the vocabulary's single owner; the register,
      schema, checker (with a firing negative control), and generated RESULTS
      view in the gate; conventions.md section 4 reduced to field formats with
      the T-NNN identity row pointing at the register; the README orientation
      section distinguishing survey content from first-party results by level,
      SYNOPSIS matching; packing-validate --push green; the work on a new PR
      from the restarted branch.
    bead: think-n8vl
    depends_on: [BC-106]
    workflows: [pipeline-improvement]
    next_evidence: >-
      Discharged by session-061. epistemics.md at the repository root owns the
      four axes; frontier/results.yaml declares T-001 through T-013 and
      devtools/check_results.py re-derives every declared V and C from the
      cited atoms in the records tier, refusing inflation and unexplained
      understatement, with a firing negative control and the generated
      RESULTS.md view; conventions.md section 4 points result-level semantics
      at epistemics.md and the identity row points T-NNN at the register; the
      README's What Has Been Established separates first-established-here
      from audited-from-the-literature by T-id; SYNOPSIS defers its results
      section to the register and its night handoff names the session;
      softschema is at 0.8.0 across the toolchain. Deferred rather than
      force-fitted: the Trump local-isolation entry (derives C3, no
      adversarial control test to name) and the translation-escape survey
      observation, both typed on think-n8vl.
    artifacts:
    - frontier/results.yaml
    - frontier/results.schema.yaml
    - frontier/RESULTS.md
    - devtools/check_results.py
    - devtools/render_results.py
    - tests/test_results_register.py
    - campaign/agent-sessions/session-061-epistemics-codification.md
---
# Agenda-011 — The Verification Review

One cell: the owner moved the review from their queue to the repository's own
rubric, so the six held results get determinations here, with the independent
interval certifier built where first-party independence was missing.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
