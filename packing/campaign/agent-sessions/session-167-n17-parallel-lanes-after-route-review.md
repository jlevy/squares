---
title: "Session 167 — n17 parallel lanes after the route review"
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-167
  title: n17 Parallel Lanes After the Route Review
  date: '2026-10-02'
  started_at: '2026-10-02T01:05:34Z'
  branch: claude/busy-goldberg-rouoli
  primary_bead: think-c7kv
  status: stopped
  ended_at: '2026-10-02T06:38:38Z'
  goal: >-
    Carry PR 283's route review onto current main and, over about three hours, make the
    highest-leverage progress toward an n17 optimality proof: dispatch BC-406's lanes,
    test the decisive feasibility questions first, and retain every result with
    independent review.
  workflow_phases:
  - workflow: review-planning-oversight
    focus: insight
    recording: retrospective
    clock_role: work
    commitment: BC-406
    objective: >-
      Fetch PR 283's branch, merge it onto current main on the session branch, restore
      the session's toolchain, and recommend the highest-leverage lanes for three hours.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 30
    started_at: '2026-10-02T01:05:34Z'
    deadline_at: '2026-10-02T01:35:34Z'
    expected_output: A merged, validated branch and a ranked lane plan the owner can approve.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: The merge cannot be made to pass the records tier.
    fallback: Report the conflict and plan from the PR branch alone.
    outcome: >-
      PR 283 merged at 16d79755 with two document-table conflicts resolved by keeping
      both sides; the records tier passed. Two losses from the previous container were
      found: the fourteen exploratory scripts and Session 166's seven beads, which were
      recreated under their original short IDs. The owner approved a four-lane plan, with
      a one-sided charge-floor pilot first because the flat R068 ledger made it the
      likeliest no-go.
    evidence:
    - docs/project/reviews/review-2026-10-01-n17-route-after-pr265.md
    stop_reason: The owner said start.
    next_action: Dispatch lanes A1, A2, B and D.
  - workflow: research-loop
    focus: correctness
    recording: contemporaneous
    clock_role: work
    commitment: BC-406
    objective: >-
      Run the route review's lanes in parallel with disjoint deliverables, replan at
      each lane boundary from measured results, and record every verdict only after an
      independent review and a clean committed-tree run.
    status: stopped
    entered_by: user_request
    switch_reason: The owner approved the lane plan.
    budget_minutes: 180
    started_at: '2026-10-02T04:22:26Z'
    deadline_at: '2026-10-02T07:22:26Z'
    expected_output: >-
      H-258 decided; H-261's instrument built and reviewed; a go/no-go for H-262; a
      capture cost model; follow-up lanes chosen from those results.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: A lane's result contradicts an accepted record.
    fallback: Retain partial instruments with their receipts and hand off.
    outcome: >-
      H-258 accepted (exp-242), H-265 accepted (exp-245), H-262 rejected (exp-243).
      H-261 certified on a declared slider box at r = 1/5000 (exp-244) and H-266's
      24-cell capacity-one cover certified with 43,593 orbits (exp-246); both unresolved
      on stated scope items. The census, not the engine, was found to be the global
      half's first problem.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-242-h258-n17-core-stress.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-243-h262-n17-charge-floor-pilot.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-244-h261-n17-local-minimum.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-245-h265-n17-catalogue-polynomial.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-246-h266-n17-capacity-one-cover.md
    stop_reason: The three-hour window closed with every dispatched lane reported.
    next_action: BC-418 (think-tmz6).
  budget:
    wall_minutes: 240
    finalization_minutes: 30
  stop_conditions:
  - The owner ends the run; a self-declared budget is not a stop condition (OR-8).
  - A verdict is recorded only after an independent review and a clean committed-tree run.
  - Frozen criteria are not retuned after a result is seen; scope gaps are recorded as unresolved.
  progress:
    metric: >-
      How much of an n17 optimality proof is certified, and whether the remaining route
      is affordable.
    before: >-
      The local theorem about half done with H-258's instrument stalled; the global half
      with 20,155,518 orbits and no exclusion engine; capture unpriced.
    after: >-
      H-258 accepted; the local minimum modulo sliders certified at r = 1/5000 on a
      declared slider box, pending one capture-side slide bound; per-cell charge floors
      ruled out; a certified 24-cell capacity-one cover with 43,593 orbits, pending a
      single-state fix; capture priced as logarithmic in the radius; the certified side
      identified with the catalogue's degree-18 polynomial.
  resource_rollups:
  - packing/campaign/resource-usage/9ef40ca7-d637-5e9a-8f7f-e71a05712560.yaml
  - packing/campaign/resource-usage/agent-a01d350a113875e85.yaml
  - packing/campaign/resource-usage/agent-a093f7bf1b5a57a85.yaml
  - packing/campaign/resource-usage/agent-a3ca8f2c2edfd4340.yaml
  - packing/campaign/resource-usage/agent-a58c621f9018195e4.yaml
  - packing/campaign/resource-usage/agent-a625ac54c60aed8cd.yaml
  - packing/campaign/resource-usage/agent-a66f38937bdef6c02.yaml
  - packing/campaign/resource-usage/agent-a67f0edde8ed86505.yaml
  - packing/campaign/resource-usage/agent-a6a437c44c3304b19.yaml
  - packing/campaign/resource-usage/agent-a70b6f243c76b7028.yaml
  - packing/campaign/resource-usage/agent-a7e5b6dec097dce25.yaml
  - packing/campaign/resource-usage/agent-a8a8b79e0239bca0f.yaml
  - packing/campaign/resource-usage/agent-a99354ec00e40e457.yaml
  - packing/campaign/resource-usage/agent-a9d15edf10039fa0e.yaml
  - packing/campaign/resource-usage/agent-abc5e690e5d7d3041.yaml
  - packing/campaign/resource-usage/agent-abeb1a31ad979cecd.yaml
  - packing/campaign/resource-usage/agent-ae8abe09a3292e894.yaml
  - packing/campaign/resource-usage/agent-af4a13e9dbcb00142.yaml
  delegations:
  - task: Lane A1, repair the H-258 stress instrument and run its controls and target
    operator: Opus subagent at extra-high effort
    status: completed
    recording: contemporaneous
    outcome: Ring-arithmetic identity proof in 6.6 s replacing the stalled sympy.cancel; target passed.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-242-n17-core-stress/run-001
    files:
    - packing/devtools/check_n17_core_stress.py
    - packing/tests/test_n17_core_stress.py
    checks:
    - Stall reproduced (exit 124 at 90 s); twelve tests; nine mutation controls refused.
    uncertainty: Same-lane controls and target; independent review followed.
    elapsed_seconds: 919.7
    elapsed_quality: platform_measured
    next_action: None; accepted in exp-242.
    phase: 2
    budget_minutes: 75
    started_at: '2026-10-02T04:27:00Z'
  - task: Independent review of the H-258 instrument and output
    operator: Fable subagent at maximum effort
    status: completed
    recording: contemporaneous
    outcome: No blocking defect; independent recomputation and a grid proof beyond a computed degree bound.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-242-n17-core-stress/output-review.md
    files: []
    checks:
    - Separate exact and 2^-300 interval arithmetic; every weight sign and capacity matched.
    uncertainty: None blocking; four notes recorded.
    elapsed_seconds: 1143.2
    elapsed_quality: platform_measured
    next_action: None.
    phase: 2
    budget_minutes: 75
    started_at: '2026-10-02T04:45:00Z'
  - task: Lane A2-review, adversarial review of the local theorem and the frozen instrument recipe
    operator: Fable subagent at maximum effort
    status: completed
    recording: contemporaneous
    outcome: Both arguments sound with stated repairs; recipe C1-C12; uniform radius about 1/5000 over the slider box.
    evidence:
    - docs/project/reviews/review-2026-10-02-n17-local-theorem-recipe.md
    files: []
    checks:
    - Float LP probes for ratios and cell counts; exact kernel and stress checks.
    uncertainty: Exploratory ratios; the instrument later certified them.
    elapsed_seconds: 1696.2
    elapsed_quality: platform_measured
    next_action: None.
    phase: 2
    budget_minutes: 90
    started_at: '2026-10-02T04:27:00Z'
  - task: Lane A2-build, the point half of the H-261 checker
    operator: Opus subagent at extra-high effort
    status: completed
    recording: contemporaneous
    outcome: Exact kernel, 90 exact optimal duals and 135 option margins at the midpoint.
    evidence:
    - packing/campaign/explorations/X048-session-167-pilots/README.md
    files:
    - packing/devtools/check_n17_local_minimum.py
    - packing/tests/test_n17_local_minimum.py
    checks:
    - Two controls refused; float cross-check within 5.7e-14.
    uncertainty: Single point only.
    elapsed_seconds: 1298.1
    elapsed_quality: platform_measured
    next_action: None; extended by A2-build-2.
    phase: 2
    budget_minutes: 100
    started_at: '2026-10-02T04:27:00Z'
  - task: Lane A2-build-2, the H-261 ratio test over the slider box and the C11, C1 and C2-control follow-up
    operator: Opus subagent at extra-high effort
    status: completed
    recording: contemporaneous
    outcome: All 90 coordinates pass at r = 1/5000 on 93 cells, worst 0.925818; stress along the family nonnegative.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-244-h261-n17-local-minimum.md
    files:
    - packing/devtools/check_n17_local_minimum.py
    - packing/tests/test_n17_local_minimum.py
    checks:
    - n11 replay reproduces 0.676505208203 exactly; seven controls refused.
    uncertainty: Lemmas 1-6 are hand proofs, read by the independent review.
    elapsed_seconds: 2532.7
    elapsed_quality: platform_measured
    next_action: None.
    phase: 2
    budget_minutes: 135
    started_at: '2026-10-02T04:58:00Z'
  - task: Independent review of the H-261 instrument
    operator: Fable subagent at maximum effort
    status: completed
    recording: contemporaneous
    outcome: No blocking defect in mathematics, instrument or certificates; claim scope exceeds the certified box.
    evidence:
    - docs/project/reviews/review-2026-10-02-n17-local-theorem-instrument.md
    files: []
    checks:
    - Own rows, curvature constants, option margins and all four -omega_11 cells recomputed exactly.
    uncertainty: Slide-domain scan is float, one axis at a time.
    elapsed_seconds: 1225.7
    elapsed_quality: platform_measured
    next_action: H-268 (BC-417).
    phase: 2
    budget_minutes: 80
    started_at: '2026-10-02T05:33:00Z'
  - task: Lane B, one-sided go/no-go pilot for H-262's charge floors
    operator: Fable subagent at extra-high effort
    status: completed
    recording: contemporaneous
    outcome: No-go; R068 at U excludes nothing; 7,703,312 orbits survive the cuts.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-243-h262-n17-charge-floor-pilot.md
    files:
    - packing/devtools/pilot_n17_charge_floors.py
    - packing/tests/test_pilot_n17_charge_floors.py
    checks:
    - Validation at R068's own side reproduces Gamma exactly; endpoint control survives.
    uncertainty: The lane overstated its ceiling's scope; corrected after review.
    elapsed_seconds: 1339.6
    elapsed_quality: platform_measured
    next_action: None.
    phase: 2
    budget_minutes: 120
    started_at: '2026-10-02T04:27:00Z'
  - task: Independent adversarial review of lane B's no-go
    operator: Fable subagent at maximum effort
    status: completed
    recording: contemporaneous
    outcome: No-go stands; the 30,966 ceiling is a theorem only for one symmetric linear floor vector.
    evidence:
    - docs/project/reviews/review-2026-10-02-n17-charge-floor-pilot.md
    files: []
    checks:
    - Floors by direct rule evaluation; census by Burnside and a transfer DP; asymmetric search to 6 orbits.
    uncertainty: Realisability of asymmetric floors is open.
    elapsed_seconds: 1251.3
    elapsed_quality: platform_measured
    next_action: None.
    phase: 2
    budget_minutes: 70
    started_at: '2026-10-02T04:53:00Z'
  - task: Lane D, capture feasibility as a function of the local radius
    operator: Fable subagent at extra-high effort
    status: completed
    recording: contemporaneous
    outcome: n11's radii were 6.5e-4 to 6.8e-3, not 1/64; capture cost logarithmic in the radius.
    evidence:
    - docs/project/reviews/review-2026-10-02-n17-capture-feasibility.md
    files: []
    checks:
    - Coordinator spot-checked n11's pose-inclusion receipt before recording the correction.
    uncertainty: Cost model uncertain by about 3x per factor; the contraction rate is unmeasured.
    elapsed_seconds: 1144.0
    elapsed_quality: platform_measured
    next_action: A contraction-rate pilot under BC-418.
    phase: 2
    budget_minutes: 90
    started_at: '2026-10-02T04:27:00Z'
  - task: Lane E, scope of a widened conditional projection theorem
    operator: Fable subagent at extra-high effort
    status: completed
    recording: contemporaneous
    outcome: Plausible at angle radius 5e-3 to 1e-2 as a dual-sheet certificate; nests inside H-261.
    evidence:
    - docs/project/reviews/review-2026-10-02-n17-widened-projection-scope.md
    files: []
    checks:
    - Exploratory parametric LP slopes in all 32 signed directions.
    uncertainty: Patch count unknown.
    elapsed_seconds: 3062.6
    elapsed_quality: platform_measured
    next_action: Optional coarse patching under BC-418.
    phase: 2
    budget_minutes: 80
    started_at: '2026-10-02T04:42:00Z'
  - task: Lane F, bulk exclusion design after the charge-floor no-go
    operator: Fable subagent at maximum effort
    status: completed
    recording: contemporaneous
    outcome: The census is the first problem; a 24-cell capacity-one design and sub-pattern exclusion; H-266, H-267.
    evidence:
    - docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
    files: []
    checks:
    - n11 cover and field statistics read from the receipts; exploratory cover and proxy counts.
    uncertainty: Leaf estimates by analogy with n11.
    elapsed_seconds: 1895.4
    elapsed_quality: platform_measured
    next_action: H-267 under BC-418.
    phase: 2
    budget_minutes: 100
    started_at: '2026-10-02T04:53:00Z'
  - task: Lane G, exact checker for the H-266 capacity-one cover
    operator: Opus subagent at extra-high effort
    status: completed
    recording: contemporaneous
    outcome: The tabbed 24-cell cover passes every exact check; 43,593 orbits; family margin 0.013770.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-246-h266-n17-capacity-one-cover.md
    files:
    - packing/devtools/check_n17_capacity_one_cover.py
    - packing/tests/test_check_n17_capacity_one_cover.py
    checks:
    - Seven controls refused; untabbed design refused on seams.
    uncertainty: Square 6's range declared.
    elapsed_seconds: 1292.6
    elapsed_quality: platform_measured
    next_action: Single-state fix (lane G2).
    phase: 2
    budget_minutes: 90
    started_at: '2026-10-02T05:27:00Z'
  - task: Lane G-proof, independent proof review of the depth-width wall lemma
    operator: Fable subagent at maximum effort
    status: completed
    recording: contemporaneous
    outcome: Lemma correct for every orientation and sharp; margins confirmed; the family realises two states.
    evidence:
    - docs/project/reviews/review-2026-10-02-n17-depth-width-wall-lemma.md
    files: []
    checks:
    - Own Sturm count and counterexample search; checker quartic re-derived.
    uncertainty: None on the lemma.
    elapsed_seconds: 1996.4
    elapsed_quality: platform_measured
    next_action: None.
    phase: 2
    budget_minutes: 75
    started_at: '2026-10-02T05:27:00Z'
  - task: Lane C, identification of the certified side with the catalogue polynomial
    operator: Opus subagent at high effort
    status: completed
    recording: contemporaneous
    outcome: Identical with unit 1 and irreducible; second elimination route agrees.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-245-h265-n17-catalogue-polynomial.md
    files:
    - packing/devtools/check_n17_catalogue_polynomial.py
    - packing/tests/test_check_n17_catalogue_polynomial.py
    checks:
    - Twenty-four tests including perturbed-polynomial controls.
    uncertainty: None.
    elapsed_seconds: 622.2
    elapsed_quality: platform_measured
    next_action: None.
    phase: 2
    budget_minutes: 50
    started_at: '2026-10-02T05:42:00Z'
  - task: Independent review of the H-265 identification
    operator: Fable subagent at extra-high effort
    status: completed
    recording: contemporaneous
    outcome: Criterion holds on all three clauses; no blocker.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-245-n17-catalogue-polynomial/output-review.md
    files: []
    checks:
    - Own resultant chain, Sturm and Descartes counts, irreducibility at four primes.
    uncertainty: None.
    elapsed_seconds: 492.4
    elapsed_quality: platform_measured
    next_action: Update n-017.md (think-yjgk).
    phase: 2
    budget_minutes: 35
    started_at: '2026-10-02T05:52:00Z'
  - task: Lane G2, a unique-state check and a unique-state 24-cell cover
    operator: Opus subagent at extra-high effort
    status: completed
    recording: contemporaneous
    outcome: ring-3-voronoi-8-tabbed-unique passes every check with a unique family state; 43,593 orbits.
    evidence:
    - packing/devtools/check_n17_capacity_one_cover.py
    files:
    - packing/devtools/check_n17_capacity_one_cover.py
    - packing/tests/test_check_n17_capacity_one_cover.py
    checks:
    - The tabbed design fails unique_state on squares 13 and 11; nineteen tests.
    uncertainty: Least unique-state margin 0.002111; not yet independently reviewed; stopped once by an API rate limit and resumed.
    elapsed_seconds: 774.2
    elapsed_quality: platform_measured
    next_action: Review and record under BC-418.
    phase: 2
    budget_minutes: 35
    started_at: '2026-10-02T06:08:00Z'
  - task: Lane H, the H-268 slide bounds from square 6's cover cell
    operator: Opus subagent at extra-high effort
    status: completed
    recording: contemporaneous
    outcome: a <= 21/100, z >= -1/20 and b <= 3/40 proved exactly with square 6 in the tabbed design's side-S2.
    evidence:
    - packing/devtools/check_n17_slider_coverage.py
    files:
    - packing/devtools/check_n17_slider_coverage.py
    - packing/tests/test_check_n17_slider_coverage.py
    checks:
    - Whole-box and square-13-deleted controls refused; six tests.
    uncertainty: Proved on the tabbed design's S2, which the unique design shifts by 0.01; faces a >= 0, b >= 0, z <= 1/16 not covered; no review yet.
    elapsed_seconds: 578.1
    elapsed_quality: platform_measured
    next_action: Re-run on the unique design and review under BC-418.
    phase: 2
    budget_minutes: 40
    started_at: '2026-10-02T06:08:00Z'
  outputs:
  - docs/project/reviews/review-2026-10-02-n17-capture-feasibility.md
  - docs/project/reviews/review-2026-10-02-n17-local-theorem-recipe.md
  - docs/project/reviews/review-2026-10-02-n17-charge-floor-pilot.md
  - docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
  - docs/project/reviews/review-2026-10-02-n17-widened-projection-scope.md
  - docs/project/reviews/review-2026-10-02-n17-local-theorem-instrument.md
  - docs/project/reviews/review-2026-10-02-n17-depth-width-wall-lemma.md
  - packing/campaign/explorations/X048-session-167-pilots/README.md
  - packing/campaign/hypotheses/H-266-n17-minimal-capacity-one-cover.md
  - packing/campaign/hypotheses/H-267-n17-isolated-sub-pattern-residue.md
  - packing/campaign/hypotheses/H-268-n17-local-theorem-slider-coverage.md
  - packing/campaign/agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md
  checks:
  - 'full gate: fast at e51fce98983dc29beef931b52fd774ed58c976b8: passed (follow-up in Session 168 on PR 307: hosted Packing validation run 36979940992 and Certificate page run 36979940948; this head carries the session''s work unchanged)'
  - Every verdict rests on an independent review in code sharing nothing with the producer and on a clean committed-tree run whose outputs match the lane's run apart from timings.
  - The records tier passed at every integration commit.
  - packing-validate --push on the committed head ba95da0f, in a worktree, failed 8 of 3,562 tests and passed the rest; in the main checkout six of the eight pass (the worktree's symlinked node_modules and lane load), and the remaining two, the process-group reaping tests, fail identically on unchanged origin/main 8aaa411d in this container, as Session 166 recorded.
  - The 18 resource rollups were generated by devtools.log_rollup from the session log and every sub-agent transcript; model-identifier keys are redacted to `redacted` under this environment's rule against pushing model identifiers, with counts unchanged.
  - The beads Session 166 created were lost with its container and recreated under their original short IDs so the record's 44 references resolve.
  stop_reason: >-
    The owner's three-hour window closed with every dispatched lane reported and
    integrated. Hosted certification of the branch is pending under think-iuz2.
  next_action: >-
    BC-418 (think-tmz6): close H-266's single-state item and H-268's slide bound, then
    re-record H-261 and H-266; build the H-267 selector and adapt the n11 kernel; pilot
    the capture contraction rate on the endpoint's occupancy state. Lanes G2 and H
    left a unique-state cover and the H-268 slide bounds built but unreviewed; H-268
    must be re-run on the unique design, and B_W's faces a >= 0, b >= 0 and z <= 1/16 still
    need a capture-side argument. Hosted
    certification of this branch is owned by think-iuz2.
---
# Session 167: n17 Parallel Lanes After the Route Review

The owner asked for PR 283’s branch to be continued and for the highest-leverage three
hours toward an n17 optimality proof.
The session merged the route review onto current main, dispatched its lanes, replanned
at each result, and recorded five experiments, each after an independent review.

## Where n17 Stands After This Session

- **Local half.** The local minimum modulo the sliders is certified at radius $1/5000$
  over a declared slider box, with worst ratio $0.926$. The one gap is a capture-side
  bound on the slides of squares 5 and 13, now H-268.
- **Global half.** Per-cell charge floors are ruled out.
  n11’s census was tractable because of its minimal cover, and a certified 24-cell
  capacity-one cover cuts n17’s census from 7.7 million orbits to 43,593. Isolated
  sub-pattern exclusion (H-267) is the next engine.
- **Capture.** It is priced as logarithmic in the radius, because n11’s own radii were
  of the n17 scale. Its contraction rate is the unmeasured risk.
- **Identity.** The certified side is the catalogue’s degree-18 algebraic number.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
