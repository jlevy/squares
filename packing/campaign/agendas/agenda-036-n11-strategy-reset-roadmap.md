---
title: agenda-036 — n11 strategy-reset roadmap
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-036
  title: N11 Strategy-Reset Roadmap
  updated: '2026-09-16'
  status: active
  objective: >-
    Reconcile the merged research record, then choose among routes that can either
    improve the n=11 bound materially, replace the current certificate with a much
    simpler proof, or resolve another small case through a transferable technique. Keep
    paused incremental lanes out of the execution queue unless new evidence changes
    their expected value.
  items:
  - id: BC-339
    purpose: tool_validation
    owner_focus: process
    instances: [11]
    state: complete
    priority: 0
    question: >-
      Can the post-merge agendas, sessions, explorations, hypotheses, experiments,
      frontier results, strategic boundary, and selected handoff be reconciled into one
      checked reader-facing account?
    budget: >-
      One W7 pipeline-improvement block with three independent read-only audits,
      source-first reconciliation, a durable W8 roll-up procedure, generated-view
      refresh, a focused drift check, and no scientific target.
    entry: >-
      PRs 156, 157, 161–168 have landed; the old selected handoff points at paused work;
      H-160 and H-162 are registered without target receipts; and the owner has selected
      a significant-improvement-or-simplification strategy.
    exit: >-
      SYNOPSIS.md carries a checked current-state block and one current handoff, README.md
      routes readers to it without copying volatile totals, the active plans state the
      strategy reset, and W8 defines how to repeat the roll-up.
    bead: think-uqa4
    depends_on: []
    next_evidence: >-
      BC-347 consumes the checked inventory and scientific boundary without reopening
      the source reconciliation.
    workflows: [pipeline-improvement, documentation-pass]
    program: n11-strategy-reset
    artifacts:
    - SYNOPSIS.md
    - README.md
    - packing/campaign/documentation-pass.md
    - docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
    parallel_group: research-state-rollup
    outcomes:
    - scope: >-
        The reader-facing research inventory, source precedence, generated views,
        current handoff, and repeatable roll-up procedure after the September 14 merge
        stack.
      classification: achieved
      result: >-
        The synopsis now carries a source-derived program snapshot and current handoff;
        README and the active plans route through it; W8 defines the repeatable roll-up;
        and focused checks reject stale counts, lifecycle ordering, and handoff drift.
        No scientific target or frontier claim changed.
      evidence:
      - SYNOPSIS.md
      - README.md
      - packing/campaign/documentation-pass.md
      - packing/campaign/agent-sessions/session-128-research-state-rollup.md
      disposition: retire-success
      follow_up: null
  - id: BC-347
    purpose: research
    owner_focus: insight
    instances: [6, 7, 10, 11, 13]
    state: complete
    priority: 0
    question: >-
      Which mathematically distinct approaches have a credible path to significant
      progress on n=11 or transferable small-n techniques, given the retained theorems,
      scoped negatives, and tooling?
    budget: >-
      One read-only deep mathematical audit delegated to Astra Max. Evaluate Routes A,
      B, S, C, and D, generate additional hypotheses and approaches, rank them by
      information value and material upside, and run no scientific target.
    entry: >-
      BC-339 closes with one checked source inventory, scientific boundary, tool
      inventory, and current handoff.
    exit: >-
      A durable mathematical audit separates proved facts, evidence-backed inference,
      and speculation; ranks the enlarged route set; and gives each serious candidate a
      prerequisite, cheapest discriminator, transfer value, and kill or continue rule.
    bead: think-oj12
    depends_on: [BC-339]
    next_evidence: >-
      BC-346 compares the audited prerequisites, first discriminators, payoff, and cost
      and selects exactly one execution entry.
    workflows: [factual-review, insight-iteration]
    program: n11-strategy-reset
    artifacts:
    - docs/project/reviews/review-2026-09-14-small-n-significant-progress-mathematical-audit.md
    parallel_group: mathematical-strategy-audit
    outcomes:
    - scope: >-
        The retained n11 proof, fractional ceiling, scoped negative results, five shaped
        routes, and additional mechanisms with potential at n=11 or another small n.
      classification: achieved
      result: >-
        Astra Max ranked the original A, S, B, C, and D routes; added E, F1, F2, N, and
        G; corrected premises and discriminators; and advised the order A, S, E, B, F1,
        F2, N, C, D, G. This is a recommendation, not a selected scientific target.
      evidence:
      - docs/project/reviews/review-2026-09-14-small-n-significant-progress-mathematical-audit.md
      disposition: retire-success
      follow_up: null
  - id: BC-346
    purpose: tool_validation
    owner_focus: process
    instances: [11]
    state: complete
    priority: 0
    question: >-
      Given the reconciled state, is the validation-efficiency checkpoint due, and which
      one entry from the enlarged audited route set has the highest information value
      as the next bounded block?
    budget: >-
      One W10 planning block over dependency readiness, expected information value,
      stop rules, and resource cost; no implementation or scientific target.
    entry: >-
      BC-347 closes with a source-bound audit, enlarged approach set, relative priorities,
      and explicit discriminator and stop rules.
    exit: >-
      Exactly one selected next entry, with the remaining candidates explicitly
      continued, paused, or stopped and the active plan and handoff updated together.
    bead: think-9y7p
    depends_on: [BC-347]
    next_evidence: >-
      Reconstruct the W5 cadence, then compare any due checkpoint with Routes A, S, E,
      B, F1, F2, N, C, D, and G using their declared first discriminators; select one
      block rather than a multi-lane research promise.
    workflows: [review-planning-oversight]
    program: n11-strategy-reset
    artifacts:
    - docs/project/reviews/review-2026-09-14-n11-w10-route-selection.md
    - packing/campaign/agent-sessions/session-130-n11-w10-route-selection.md
    parallel_group: route-selection
    outcomes:
    - scope: >-
        The post-audit W5 cadence, recent-merge stability, ten scientific candidates,
        and one bounded next entry, without running an efficiency repair or scientific
        target.
      classification: achieved
      result: >-
        The conservative cadence reaches OR-12's eight-block ceiling, so BC-340 is the
        sole selected next entry. Every scientific candidate remains behind BC-353's
        fresh post-W5 selection; Route A at 3.84 is the presumptive first choice and
        Route S its admission fallback, but neither is authorized.
      evidence:
      - docs/project/reviews/review-2026-09-14-n11-w10-route-selection.md
      - packing/campaign/agent-sessions/session-130-n11-w10-route-selection.md
      disposition: retire-success
      follow_up: think-1ydi
  - id: BC-340
    purpose: measurement_validation
    owner_focus: efficiency
    instances: [11]
    state: complete
    priority: 0
    question: >-
      Does the four-to-eight-block cadence make an efficiency checkpoint due, and if so
      what one demonstrated bottleneck should it address before another large research
      block starts?
    budget: >-
      One W5 checkpoint from actual session and validation receipts; change at most one
      bottleneck behind an equivalence guard, or record a measured no-change decision.
    entry: BC-346 selects this checkpoint from the reconciled sequence and retained costs.
    exit: >-
      One measured bottleneck disposition or an evidence-backed no-change result, then a
      terminal handoff to BC-353's fresh W10 route selection.
    bead: think-1ydi
    depends_on: [BC-346]
    next_evidence: >-
      Reconstruct the cadence from active daytime blocks and retained gate receipts;
      administrative work does not reset the cadence.
    workflows: [efficiency-loop, review-planning-oversight]
    program: n11-strategy-reset
    artifacts:
    - packing/campaign/agent-sessions/session-131-n11-w5-validation-efficiency.md
    - packing/benchmarks/validation-efficiency/experiments/VE-005-rollup-corpus-snapshot.md
    parallel_group: efficiency-checkpoint
    outcomes:
    - scope: >-
        The current pull-request gate at its declared host shape, one demonstrated
        bottleneck, its equivalence guard, and a measured response; no scientific target.
      classification: achieved
      result: >-
        VE-005 removed repeated whole-corpus parsing from the branch-cost rollup. Three
        alternating local pairs reduced its median from 47.72 to 2.31 seconds without
        changing the representative output digest or rendered branch population. The
        first candidate hosted checks tier passed at 106.38 seconds against the
        unchanged 195-second ceiling; further hosted readings are required before a
        measured baseline is recorded.
      evidence:
      - packing/benchmarks/validation-efficiency/experiments/VE-005-rollup-corpus-snapshot.md
      - packing/benchmarks/validation-efficiency/report.md
      - packing/campaign/agent-sessions/session-131-n11-w5-validation-efficiency.md
      disposition: retire-success
      follow_up: think-d3h5
    - scope: >-
        Correction of 2026-09-15, by addition. The checks-tier measured baseline the
        outcome above says is still owed, and who owns it.
      classification: never-opened
      result: >-
        BC-340 misrouted the still-owed hosted baseline to scientific bead think-d3h5.
        Measurement belonged to think-gsz0, which remained unresolved for eight days and
        was later closed as superseded after think-z121 recorded the predecessor
        topology. That seven-run baseline is historical evidence, not a measurement of
        the current seven-part surface. think-97we owns the exact-head replacement
        measurements and their retained history.
      evidence:
      - packing/devtools/gate-budgets.yaml
      - packing/devtools/read_tier_walls.py
      disposition: defer-dependency
      follow_up: think-97we
  - id: BC-355
    purpose: tool_validation
    owner_focus: efficiency
    instances: [11]
    state: in_progress
    priority: 0
    question: >-
      Can the CI topology, gate-cost register, and validation-lane contract keep
      ordinary research feedback within 180 seconds while reserving slow, exhaustive,
      deferred, golden, and strict checks for explicit checkpoints?
    budget: >-
      One W7 pipeline-improvement block over the reconciled pull-request topology, with
      measured W5 decisions and an independent W2 review. Preserve the complete
      seven-part fast surface; move work off the critical path only when an equivalence
      guard retains its coverage and failure behavior.
    entry: >-
      BC-340's correction assigns current-topology measurements to think-97we, while
      PRs 183, 185, and 186 carry overlapping Pages, Packing, and wall-budget changes
      that cannot be merged as independent final designs.
    exit: >-
      Exact-head hosted Packing and Pages aggregates pass within 180 seconds; every
      fast partition remains represented; budget history, attribution, tree reuse, and
      artifact synchronization fail closed; the edit, push, pull-request, and
      checkpoint lanes are documented; and superseded pull requests and beads have an
      explicit disposition.
    bead: think-97we
    depends_on: [BC-340]
    next_evidence: >-
      Complete exact-head hosted measurements and independent re-review, then resume
      BC-343 under think-ufmk without changing H-163, allocating exp-161, or running a
      scientific target.
    workflows: [pipeline-improvement, efficiency-loop, factual-review]
    program: gate-cost
    artifacts:
    - packing/campaign/agent-sessions/session-136-ci-topology-reconciliation.md
    - packing/campaign/agent-sessions/session-137-ci-topology-continuation-recovery.md
    - docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
    - development.md
    - packing/devtools/gate-budgets.yaml
    parallel_group: ci-topology-reconciliation
  - id: BC-353
    purpose: tool_validation
    owner_focus: process
    instances: [11]
    state: complete
    priority: 0
    question: >-
      After the due efficiency checkpoint, which one scientific route has the highest
      information value under the new gate evidence and retained mathematical audit?
    budget: >-
      One fresh W10 planning block after BC-340. Recheck repository stability and all
      scientific candidates; select exactly one execution entry and run no target.
    entry: >-
      BC-340 closes with a measured repair or measured no-change decision, its own merged
      pull request, and a terminal handoff to this block.
    exit: >-
      Exactly one scientific route is selected, every alternative has an explicit
      disposition and resume condition, and only the selected route becomes ready.
    bead: think-d3h5
    depends_on: [BC-340]
    next_evidence: >-
      Reconsider Route A at side 3.84 first, Route S as its admission fallback, and Route
      E in the first tier, while incorporating BC-340's measured result.
    workflows: [review-planning-oversight]
    program: n11-strategy-reset
    artifacts:
    - packing/campaign/agent-sessions/session-132-n11-post-w5-route-selection.md
    - docs/project/reviews/review-2026-09-14-n11-post-w5-route-selection.md
    parallel_group: post-efficiency-route-selection
    outcomes:
    - scope: >-
        The ten-route post-W5 portfolio, exact first discriminators, admission gaps,
        fallback rules, and six active hours of merge-bounded follow-up work.
      classification: achieved
      result: >-
        Route A's complete same-corner root admission at side 96/25 is the sole next
        entry. Route S is the explicit fallback if the physical root and independent
        checker cannot be admitted within 75 minutes. No scientific target ran.
      evidence:
      - docs/project/reviews/review-2026-09-14-n11-post-w5-route-selection.md
      - packing/campaign/agent-sessions/session-132-n11-post-w5-route-selection.md
      disposition: retire-success
      follow_up: think-0t5y
  - id: BC-354
    purpose: tool_validation
    owner_focus: process
    instances: [11]
    state: complete
    priority: 0
    question: >-
      Can one complete same-corner availability-blocker root at side 96/25 be frozen
      with shared physical geometry, conditional capacities, and an independent exact
      checker before any target run?
    budget: >-
      One 75-minute Route A admission block. Freeze the 16-root physical denominator,
      one complete same-corner root, all label/pose/incidence strata, strict-core
      transfer, matched baseline, candidate capacity rows, controls, acceptance rule,
      and representation-level kill rule. Run no scientific target.
    entry: BC-353 selects Route A and merges its planning pull request.
    exit: >-
      The complete root, physical-transfer statement, checker, controls, and target
      contract are admitted in their own merged pull request, or Route A is paused and
      Route S becomes the sole next admission entry.
    bead: think-0t5y
    depends_on: [BC-353]
    next_evidence: >-
      Reopen only after one proposal supplies the complete 80-stratum negative-root
      producer, a rows-complete matched baseline, and two method-distinct exact coverage
      routes with shared physical variables.
    workflows: [factual-review, pipeline-improvement]
    program: n11-strategy-reset
    artifacts:
    - packing/campaign/agent-sessions/session-133-n11-route-a-admission.md
    parallel_group: significant-lower-bound-admission
    outcomes:
    - scope: >-
        Admission of one complete same-corner Route A negative-availability root at side
        96/25, before any scientific target.
      classification: guard-refused
      result: >-
        The block inventoried the domain, checker, and controls but did not freeze the
        complete shared-variable representation, matched exact baseline, conditional
        gate, or independent replay before its deadline. The admission guard therefore
        parked this representation. Zero of the 16 physical roots closed and the n = 11
        frontier did not change.
      evidence:
      - packing/campaign/agent-sessions/session-133-n11-route-a-admission.md
      - docs/project/reviews/review-2026-09-14-n11-post-w5-route-selection.md
      disposition: defer-dependency
      follow_up: think-a1e8
  - id: BC-341
    purpose: research
    owner_focus: insight
    instances: [11]
    state: tentative
    priority: 1
    question: >-
      At side 3.84, can one complete difficult occupancy or wall-contact root family be
      closed by proved capacity caps and conditional certificates, with 3.85 retained
      only as a stretch target after its premises are re-established?
    budget: >-
      One day-or-less Route A discriminator: freeze an original root-family denominator,
      certify each closed domain, and report the unchanged denominator, closed roots,
      and exact worst surviving domain. Subdivided leaves do not change the denominator.
    entry: >-
      A future W10 reselects Route A after a seam-safe physical-root producer,
      shared-variable checker, rows-complete matched exact baseline, and second exact
      coverage route discharge BC-354's representation gaps.
    exit: >-
      A complete difficult root family closes or a precise relaxation witness and worst
      surviving domain identify why it does not. Continue only on new matched strength.
    bead: think-9y6q
    depends_on: [BC-354]
    next_evidence: >-
      Preserve the named Route A gaps and reconsider this discriminator only through a
      future W10 after a complete representation discharges them.
    workflows: [insight-iteration, research-loop]
    program: n11-strategy-reset
    parallel_group: significant-lower-bound
  - id: BC-342
    purpose: research
    owner_focus: insight
    instances: [6, 11]
    state: tentative
    priority: 1
    question: >-
      Does a sound theta-prime or level-two pairwise relaxation pass the n=6 formulation
      controls and improve materially on the strongest matched n=11 point-and-threshold
      baseline at 3.84?
    budget: >-
      One control-first Route B block; no n=11 target until the n=6 formulation,
      discretization soundness, and symmetry handling are independently checked.
    entry: BC-353 selects Route B and a sound placement-graph discretization has an explicit conflict-edge guarantee.
    exit: >-
      A passed n=6 control and measured n=11 separation, or a precise formulation,
      scaling, or soundness obstruction that parks the route.
    bead: think-ol1z
    depends_on: [BC-353]
    next_evidence: Specify the n=6 control and the conflict-edge soundness obligation before selecting a solver.
    workflows: [insight-iteration, research-loop]
    program: n11-strategy-reset
    parallel_group: pairwise-relaxation
  - id: BC-343
    purpose: research
    owner_focus: insight
    instances: [11]
    state: blocked
    priority: 0
    question: >-
      Does T-025's exact atom-support universe admit a certificate at side 3.82 with at
      most 23 positive D4-orbit representatives and unchanged exact coverage?
    hypotheses: [H-163]
    budget: >-
      First, one separate no-target admission PR freezes T-025 as the control, its
      119-orbit support universe, the at-most-23 positive-orbit ceiling, deterministic
      decompression, mutation controls, and exact accept, unresolved, refute, and park
      meanings. Only a later fresh branch may register an experiment, optimize, or
      replay a candidate.
    entry: >-
      BC-354 stops at the Route A representation boundary, T-025 is available as the
      matched Route S control, and T-026 is available as a support and rescaling
      provenance sentinel.
    exit: >-
      H-163 is confirmed by a certificate with at most 23 positive orbit
      representatives, a human-statable generating rule, budget below eleven, and both
      exact coverage routes agreeing; or exact infeasibility refutes it. Bounded search
      without a candidate may park only this family as unresolved.
    bead: think-ufmk
    depends_on: [BC-354, BC-355]
    next_evidence: >-
      Session 139 registered exp-161 on 2026-09-18 and closed the admission-synthetic
      accept hole: live `admit_threshold_compression --check`, `--authorize-target
      exp-161`, forbidden control-manifest SHA-256 values, `generating_account`, and
      timeout maps to unresolved. The named producer is in-tree and emits no candidate;
      a coverage-encoding search is still required before any scientific target.
      BC-355's pull-request walls remain advisory under think-g4n9; that does not
      reopen the admitted instrument.
    workflows: [pipeline-improvement, factual-review, research-loop]
    program: n11-strategy-reset
    artifacts:
    - packing/campaign/explorations/X-032-route-s-threshold-compression.md
    - packing/campaign/hypotheses/H-163-route-s-threshold-compression.md
    - packing/campaign/agent-sessions/session-134-n11-route-s-admission.md
    - packing/campaign/agent-sessions/session-135-n11-route-s-guard-discharge.md
    - packing/cases/n11_threshold_certificate/route-s-compression-admission-receipt.json
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-161-h163-route-s-threshold-compression.md
    parallel_group: proof-simplification
  - id: BC-344
    purpose: research
    owner_focus: insight
    instances: [11]
    state: tentative
    priority: 2
    question: >-
      Can a robust orientation-class theorem rule out every two-orientation packing
      below Trump's recorded side, beginning with the 6+5 class at Trump's angle?
    budget: >-
      One Route C feasibility block with the exact Trump-angle control followed by one
      complete positive-width interval at a rational target near 3.87. Midpoint shrink
      does not make one-degree bins adequate.
    entry: BC-353 selects Route C and the fixed-angle control reproduces a known feasible arrangement before any exclusion claim.
    exit: >-
      A sound excluded orientation window with exact evidence, or a named feasibility or
      interval obstruction that prevents a structural theorem.
    bead: think-29ch
    depends_on: [BC-353]
    next_evidence: Reproduce the 6+5 control at Trump's angle before interpreting any solver infeasibility.
    workflows: [insight-iteration, research-loop]
    program: n11-strategy-reset
    parallel_group: orientation-structure
  - id: BC-345
    purpose: research
    owner_focus: insight
    instances: [11]
    state: tentative
    priority: 3
    question: >-
      What competing local optima appear under a serious orientation-profile-organized
      n=11 search, and can any improve the 1979 upper bound after exact polishing?
    budget: >-
      One background Route D proposer-control block comparing one changed proposal
      mechanism with the stock control at equal pair-test work. A larger campaign is
      admissible only after independent or perturbed starts recover an oblique control.
    entry: BC-353 selects Route D and the runner reproduces Trump's packing and its exact side as a positive control.
    exit: >-
      A new verified upper bound, or a retained catalogue of exact-polished competing
      optima useful to an optimality proof; unverified or unreplayed sub-Trump artifacts
      are presumed bugs until exact verification.
    bead: think-7n2w
    depends_on: [BC-353]
    next_evidence: Design the positive-control and endpoint-polishing contract before allocating the background search.
    workflows: [research-survey, research-loop]
    program: n11-strategy-reset
    parallel_group: upper-bound-search
  - id: BC-348
    purpose: research
    owner_focus: insight
    instances: [11]
    state: tentative
    priority: 1
    question: >-
      Do H-131's proved aggregate angle-count caps, admitted as coherent global
      resources, remove the retained fractional optimal face beyond the strongest
      matched point-and-threshold baseline?
    budget: >-
      One Route E admission-and-discrimination block. Freeze a common angle partition,
      coherent selection semantics, every admissible integer profile, the matched
      baseline, and an exact checker before any synthesis target.
    entry: BC-353 selects Route E and the existing H-131 cap receipts are replayed without strengthening their scope.
    exit: >-
      A valid angular resource removes an optimum retained by the matched baseline, or
      an exact surviving optimum parks this cap family while leaving other angle bands
      and charge functions open.
    bead: think-u15l
    depends_on: [BC-353]
    next_evidence: Test the valid angle-count rows against the entire retained optimal face before building a larger certificate.
    workflows: [factual-review, insight-iteration, research-loop]
    program: n11-strategy-reset
    parallel_group: global-angular-resources
  - id: BC-349
    purpose: research
    owner_focus: insight
    instances: [11]
    state: tentative
    priority: 2
    question: >-
      Can a weighted motif, genuinely multilevel floor atom, or higher-rank composition
      strictly dominate ordinary threshold atoms on one exact realizable trace universe?
    budget: >-
      One Route F1 discriminator. Freeze one candidate charge language, trace universe,
      ordinary-threshold baseline, and exact evaluator; declare whether think-g3j7's
      certificate-format work is a prerequisite.
    entry: BC-353 selects Route F1 and freezes the exact realizable trace universe and matched ordinary-threshold comparison.
    exit: >-
      An exact strict domination gap justifies a larger support-and-atom comparison; an
      ordinary domination proof parks the tested motif without judging other charge
      languages.
    bead: think-o4p9
    depends_on: [BC-353]
    next_evidence: Relate the selected candidate explicitly to adjacent think-yc80 support work and think-g3j7 format admission.
    workflows: [factual-review, insight-iteration, research-loop]
    program: n11-strategy-reset
    parallel_group: stronger-charge-language
  - id: BC-352
    purpose: research
    owner_focus: insight
    instances: [11]
    state: tentative
    priority: 2
    question: >-
      Can joint-parent geometry lower the ordinary budget of one atom by proving that two
      simultaneous physical parents cannot both trigger it in a declared domain?
    budget: >-
      One Route F2 discriminator. Freeze one atom with ordinary budget at least two, one
      joint-parent domain, exact containment and trigger semantics, and a complete pair
      evaluator.
    entry: BC-353 selects Route F2 and separates its physical capacity theorem from charge-language and serializer work.
    exit: >-
      A complete joint-parent exclusion lowers the selected atom's budget, or one feasible
      simultaneous triggering pair rejects that reduction without judging other atoms.
    bead: think-iy9h
    depends_on: [BC-353]
    next_evidence: Decide whether the selected atom needs think-g3j7's K5/K6 format before freezing the scientific target.
    workflows: [factual-review, insight-iteration, research-loop]
    program: n11-strategy-reset
    parallel_group: geometry-dependent-budget
  - id: BC-350
    purpose: research
    owner_focus: insight
    instances: [6, 12, 13]
    state: tentative
    priority: 2
    question: >-
      Can one uniform boundary-capacity or deformation lemma for L = 4 - epsilon turn
      the open n12 bracket into a stable finite reduction toward s(12) = 4?
    hypotheses: [H-039]
    budget: >-
      One Route N discriminator over a nontrivial epsilon interval, with n=6 and n=13
      as solved controls and the flexible side-four n12 family included. Do not resume a
      decimal ladder.
    entry: BC-353 selects Route N and freezes the uniform lemma, interval, control behavior, and exact replay contract.
    exit: >-
      A stable complete case reduction or exact parameterized inequality, or a legal
      flex or boundary degeneration that parks the mechanism without resolving H-039.
    bead: think-0z9b
    depends_on: [BC-353]
    next_evidence: Reuse H-039 and the existing n12 lane with its obsolete pre-T-017 target explicitly superseded.
    workflows: [factual-review, insight-iteration, research-loop]
    program: n11-strategy-reset
    parallel_group: n12-exact-value
  - id: BC-351
    purpose: research
    owner_focus: insight
    instances: [6, 11]
    state: tentative
    priority: 3
    question: >-
      Can an orientation-sensitive two- or three-parent gap lemma be summed without
      double counting to prove geometric waste beyond the one-body density ceiling?
    budget: >-
      One speculative Route G discriminator: one exact local lemma, the Trump and n=6
      angular-rattler controls, and one explicit global accounting map.
    entry: BC-353 selects Route G and freezes the local domain, deficit, degeneration controls, and non-overcounting obligation.
    exit: >-
      Both the uniform local deficit and complete accounting rule hold, or a legal
      degeneration or duplicate charge parks the candidate.
    bead: think-gzjq
    depends_on: [BC-353]
    next_evidence: Register no hypothesis until W10 selects one concrete local lemma and domain.
    workflows: [factual-review, insight-iteration, research-loop]
    program: n11-strategy-reset
    parallel_group: geometric-waste
---
# N11 Strategy-Reset Roadmap

This agenda is the current execution map after the September 14 strategy reset.
It preserves the older portfolio’s completed evidence while removing its paused
incremental lanes from the live queue.

The research-state roll-up, mathematical audit, and BC-346 W10 selection are certified
and closed in declared dependency order.
BC-340 and BC-353 are complete.
BC-354 stopped at Route A’s representation boundary: the complete physical root, matched
exact baseline, conditional gate, and independent replay were not admitted.
No target ran and no physical root closed.
Route S / BC-343 has an admitted no-target instrument and is blocked on BC-355’s
closeout under `think-97we`. Its no-target PR merged as `1d9c49c4` from reviewed head
`609d7d62`, freezing T-025’s exact 119-orbit support universe, the at-most-23
positive-orbit metric, deterministic decompression, and target-blind controls.
Session 135 discharged all four obligations retained by Session 134: complete T-025 and
T-026 contents bound to a declared Git revision and repository-relative paths, both
T-026 sentinels, a canonical source-bound manifest, and the complete X-032 mutation
matrix.
A fresh source-distinct audit found one symlink-alias hole; the repaired boundary
and regression passed re-audit, so the instrument is admitted.
No target, candidate, coverage route, optimizer, or experiment ran.
X-032 and H-163 own the source and hypothesis records; T-026 is only a
support-and-rescaling provenance sentinel.
BC-341 remains tentative behind a future W10 reselection and the named representation
gaps.

The W10 review originally mapped six active hours into five sequential PR-bounded
blocks. BC-340 and BC-353 completed, and BC-354 activated the selected-route admission’s
guard-refusal branch.
After BC-355’s topology merge, the remaining conditional path is the exp-161 target
under `think-ufmk`. Session 139 registered that experiment; the producer it names must
exist before any target access.
Review and replanning follow the bounded run.
BC-355’s pull-request walls stay advisory under `think-g4n9` until they hold 180 s.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
