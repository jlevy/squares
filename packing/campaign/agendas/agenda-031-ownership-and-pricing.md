---
title: agenda-031 — ownership continuation and paired pricing at n = 11
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-031
  title: Ownership Continuation and Paired Pricing at n = 11
  updated: '2026-09-08'
  status: active
  objective: Publish the exact ownership results derived during PR 127 review, run the independent readers
    needed to use them safely, and test one pointwise full-support pricing mechanism at q = 96/25. The
    bracket remains unchanged. No cell may infer a global packing certificate from a local proof, a numerical
    LP proposal, or a finite site set.
  items:
  - id: BC-305
    purpose: research
    owner_focus: insight
    instances:
    - 11
    state: complete
    priority: 1
    question: Which reviewed segment and corner ownership constraints survive independent exact replay,
      and what global complement remains?
    budget: Thirty-minute integration slice from 2026-09-08T23:23:55Z, with the reviewed proof sources
      and exact known-example readers; no numerical target search.
    entry: X-022 and its reviewed cap-two, cap-four, separator, signed-angle, counterexample and fixed-pattern
      proof sources.
    exit: X-022 and every cited proof source are published with independent exact readers or analytic
      checks, each local scope is explicit, and the unresolved ownership complement is named without changing
      the packing bracket.
    bead: think-qfog
    workflows:
    - insight-iteration
    - factual-review
    depends_on: []
    parallel_group: funded-ownership
    program: n11-structure-and-conditional-dots
    artifacts:
    - packing/campaign/explorations/X-022-segment-ownership-continuation.md
    next_evidence: Published proof files, exact reader receipts, and a scoped statement of the remaining
      global ownership problem.
  - id: BC-306
    purpose: research
    owner_focus: efficiency
    instances:
    - 11
    state: in_progress
    priority: 1
    question: Does full retained-state dual support expose a pointwise new-site orbit missed at that same
      point by the first 32 rows?
    hypotheses:
    - H-135
    budget: One 30-minute pricing process with a two-second TERM grace and one LP solve on the ten-logical-CPU
      host. Solver threading uses its default; no four-core allocation is enforced. The dense LP matrix
      is 346.6 MiB; its negated copy and solver workspace raise peak memory materially above 700 MiB.
      The line-pair guard bounds candidate construction separately. No candidate or cutting iterations.
    entry: The published paired-pricing instrument and controls, the retained BC-232 state, its exact
      unit-square transport at q, and preregistered H-135 and exp-134.
    exit: A retained solved-support record written before arrangement work and a priced record with either
      an exact same-witness paired32 depth <= 1 < full depth at an absent-from-state orbit, a scoped negative,
      or an unresolved guard, timeout or error disposition. No numerical witness is accepted without exact
      replay.
    bead: think-7lp3
    workflows:
    - efficiency-loop
    - research-loop
    depends_on: []
    parallel_group: funded-pricing
    program: n11-structure-and-conditional-dots
    artifacts:
    - packing/campaign/hypotheses/H-135-paired-full-support-pricing.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-134-paired-full-support-pricing.md
    next_evidence: The actual exp-134 launch receipt and its solved-support and paired-pricing artifacts,
      or a truthful never-opened disposition.
  - id: BC-307
    purpose: research
    owner_focus: correctness
    instances:
    - 11
    state: tentative
    priority: 2
    question: Should H-125's finite kernel test be renewed after the two funded lanes report?
    hypotheses:
    - H-125
    budget: 'Optional reserve only: one fresh 60-second producer and one conditional 60-second independent
      reader, each with a two-second grace, on published source.'
    entry: The BC-305 and BC-306 results, the kernel renewal admission note, and a fresh prospective record
      using the next unallocated experiment id; exp-129 remains never invoked.
    exit: Either retain a fresh producer artifact and conditional-reader verdict within the original finite-kernel
      scope, or record that the reserve was not opened. Never reinterpret exp-129 as a run or lift its
      guard.
    bead: think-98z2
    workflows:
    - research-loop
    - factual-review
    depends_on:
    - BC-305
    - BC-306
    program: n11-structure-and-conditional-dots
    next_evidence: Coordinator selection after both funded lanes, with fresh clocks and published-source
      identity if opened.
  - id: BC-308
    purpose: measurement_validation
    owner_focus: process
    instances:
    - 11
    state: blocked
    priority: 2
    question: What did the funded continuation establish, what remains unresolved, and which next entry
      should be selected?
    budget: One bounded closeout and generated-view pass after BC-305 and BC-306 terminate.
    entry: Terminal records for both funded cells and a truthful disposition for the optional reserve.
    exit: Every Agenda 031 cell has a terminal outcome and disposition, partial and unrun work remains
      named, the session is closed against actual validation evidence, and generated campaign views are
      refreshed.
    bead: think-9yow
    workflows:
    - review-planning-oversight
    - documentation-pass
    depends_on:
    - BC-305
    - BC-306
    program: n11-structure-and-conditional-dots
    next_evidence: Terminal BC-305 and BC-306 artifacts, then the coordinator's reserve decision and closeout
      selection.
---
# Agenda 031 — Ownership and Pricing Continuation

This is the distinct continuation of Agenda 030’s selected ownership and fractional
pricing work.
BC-305 retains and validates the analytic results and tools prepared during
the handoff review. BC-306 funds one prospective paired-pricing round; its instrument
commit and actual launch allocation will be frozen in exp-134 before use.
BC-307 is an optional kernel reserve, selected only after the two funded lanes report.
The next block records each result’s exact scope and the remaining global problem.

Usage is separate from the handoff: session 111 starts at 2026-09-08T23:23:55Z, when the
continuation branch was created.
Preparation before that cutoff remains in session 110. The stacked PR links the two
receipts and does not add the same activity twice.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
