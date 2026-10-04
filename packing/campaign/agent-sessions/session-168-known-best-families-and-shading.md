---
title: Session 168 — Families of known-best packings, contact shading, and the large-n limit
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-168
  title: Families of Known-Best Packings, Contact Shading, and the Large-n Limit
  date: '2026-10-02'
  started_at: '2026-10-02T05:15:20Z'
  deadline_at: '2026-10-03T09:30:00Z'
  branch: claude/ecstatic-archimedes-62hj6a
  primary_bead: think-los0
  status: completed
  ended_at: '2026-10-03T06:02:00Z'
  goal: 'Answer the owner''s four questions about the n = 1..324 atlas as one W3 exploration, X-049: whether
    the structural families visible by position relative to k^2 have been studied; whether lighter-than-dark-green
    axis-aligned squares are inexact arithmetic; whether an exact regularization can fix the ones that
    are not; and what is known about the families'' large-n limit and whether the frontier carries it.
    Every retained number comes from a tool with tests.'
  workflow_phases:
  - workflow: insight-iteration
    focus: insight
    recording: contemporaneous
    clock_role: work
    objective: 'Five parallel lanes with disjoint deliverables: a literature survey of families, an asymptotics
      survey, a family-census tool, a contact-shade census tool, and an exact-regularization feasibility
      study with a prototype tool. The coordinator owns the frontier-coverage lane, identifiers, shared
      registries, integration and commits.'
    bead: think-los0
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 180
    started_at: '2026-10-02T05:15:20Z'
    deadline_at: '2026-10-02T08:15:20Z'
    expected_output: X-049 with one section per lane, two census tools and one regularization tool with
      tests, their retained JSON, and dispositions for each bead under think-los0.
    validation_command: cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: A lane's tool cannot replicate the workbench contact rule, or a retained number has
      no tool that reproduces it.
    fallback: Retain the lane's findings as exploratory with the missing instrument named, and leave its
      bead open with that blocker.
    outcome: 'All five lanes reached their exits and the coordinator verified each before integration.
      Literature: the families were studied one construction at a time and never classified by n - k^2;
      Karakus 2026 (arXiv:2609.37410) shows Nagamochi''s Lemma 1 proof incomplete and re-proves only s(k^2-1)=k.
      Family census: 191 of 324 records are L-extensions, 98 non-integer records beat their L bound, symmetry
      follows the source (68 of 97 Kingbird-derived, 0 of 50 packets). Shading census: 7,725 of 45,468
      green squares render light in the homepage atlas, 34 within ten tolerances of contact; the rest
      are geometry. Regularization: exact derived views at the six named cases cut light green squares
      from 545 to 242 under the atlas rule with no change of side. Asymptotics: every fixed-offset family
      converges to k at a rate between k^-1 and k^-2/5, d_max(k)=O(k^(3/5)) and its divergence is open,
      and no source proves the pattern set finite or infinite.'
    evidence:
    - packing/campaign/explorations/X-049-families-shading-and-the-large-n-limit.md
    - packing/campaign/explorations/X049-families-data/family-census.json
    - packing/campaign/explorations/X049-families-data/contact-shade-census.json
    - packing/campaign/explorations/X049-families-data/regularized/run.txt
    - packing/campaign/explorations/X049-families-data/regularized/shades.txt
    stop_reason: Every lane exit reached; X-049 written and its numbers reproduced by the retained tools.
    next_action: 'think-589i: W2 review of T-007 against Karakus 2026.'
  - workflow: insight-iteration
    focus: process
    recording: contemporaneous
    clock_role: work
    objective: Wire the two censuses into the gate, finish the records, and push the integration commit
      for hosted CI.
    bead: think-vhha
    status: completed
    entered_by: planned_checkpoint
    switch_reason: Every lane reached its exit and X-049 is written.
    budget_minutes: 60
    started_at: '2026-10-02T06:00:00Z'
    deadline_at: '2026-10-02T07:00:00Z'
    expected_output: The censuses in the gate, closed lane beads, and a pushed integration commit.
    validation_command: cd packing && uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: The fast gate fails on a step this session did not touch and cannot be repaired within
      the phase.
    fallback: Stop with certification_pending naming a follow-up bead.
    outcome: The census sweep step passes through the gate in 16.42 s; the validation CLI tests (185)
      pass; lane beads closed; integration commit d8473d553 pushed. A local --fast run was stopped after
      eight minutes when the owner asked for the follow-ups, because lane writes would have invalidated
      it; hosted CI on the pull request checks the pushed commit instead, and the certifying run moves
      to the end of the session.
    evidence:
    - packing/src/sqpack/cli/validate.py
    - packing/tests/test_validation_cli.py
    stop_reason: The owner asked for every follow-up bead before the session closes.
    next_action: Open the pull request and dispatch the follow-up lanes.
  - workflow: factual-review
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: 'Work every X-049 follow-up bead in parallel lanes: think-589i, the review of T-007 against
      Karakus 2026 (a mathematical audit and a consumer inventory); think-1n8w with think-hzv3, archive
      acquisition and the asymptotic-record corrections; think-ptt7, codifying the four candidate hypotheses;
      and think-bgkz, the regularized-view layer.'
    bead: think-589i
    status: completed
    entered_by: user_request
    switch_reason: The owner asked to follow up on all follow-up beads with sub-agents.
    budget_minutes: 240
    started_at: '2026-10-02T06:20:00Z'
    deadline_at: '2026-10-02T10:20:00Z'
    expected_output: A dated review of T-007 with a disposition per consumer; archived sources; corrected
      asymptotic record with a defect entry; registered or rejected hypotheses; a regularized-view layer
      or a scoped refusal.
    validation_command: cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: The review finds a register value that is false and cannot be scoped without a decision
      from the owner.
    fallback: Record the finding, keep register values unchanged, and hand the decision to the owner.
    outcome: 'All five lanes reached their exits and the coordinator verified each. think-589i: the W2
      review finds Nagamochi Lemma 1 false for every a > 3, b > 2 (Karakus K_t, checked exactly), the
      gap reaching T-007 for every N >= 10, Karakus Theorem 1.1 sound as read, s(k^2-1) = k recovered
      and s(k^2-2) = k resting on an unreplayed Lean proof; the consumer inventory finds the bound operative
      at 287 records. No register value changed; think-xucp and think-ym34 own the changes and the Lean
      replay. think-1n8w and think-hzv3: sources archived, D-514 and D-515 corrected. think-ptt7: H-269,
      H-270 and H-272 registered. think-bgkz: a regularized-view layer for 51 records cuts the atlas light
      green squares from 7,725 to 5,475 with no square lighter; the homepage toggle remains.'
    evidence:
    - docs/project/reviews/review-2026-10-02-nagamochi-lemma1-karakus.md
    - packing/campaign/series/series-000-smoke-and-calibration/results/t007-consumer-audit.json
    - packing/atlas/known-best/regularized/index.json
    - packing/campaign/hypotheses/H-269-periodic-certificates-k2-minus-4-and-5.md
    - packing/campaign/hypotheses/H-270-k2-plus-1-crossover-kearney-shiu-strip.md
    - packing/campaign/hypotheses/H-272-symmetric-kingbird-records-reoptimized.md
    stop_reason: Every lane exit reached; the register changes need the owner to choose their order with
      the Lean replay.
    next_action: Certify the integration commit and close, once the owner decides the cost-rollup question.
  - workflow: review-planning-oversight
    focus: process
    recording: contemporaneous
    clock_role: work
    objective: Integrate and push the follow-up block, hand the owner the two decisions it raised, then
      certify the final commit and close.
    bead: think-los0
    status: completed
    entered_by: planned_checkpoint
    switch_reason: Every follow-up lane reached its exit.
    budget_minutes: 60
    started_at: '2026-10-02T07:21:03Z'
    deadline_at: '2026-10-02T08:21:03Z'
    expected_output: A pushed, green pull request; the owner decisions recorded; a certified terminal
      record.
    validation_command: cd packing && uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: The owner defers the decisions, leaving the record open.
    fallback: Stop with certification pending under think-los0 and the decisions named.
    outcome: 'The follow-up block is pushed and the pull request green: 8e000025a merges main, renumbers
      this branch''s defects to D-514 and D-515 and re-pins DATA_REVISION, and passed every required check.
      Two safety-net check-ins found nothing new. The owner decisions are named in the pull request: the
      order of think-ym34 and think-xucp, the cost rollups, and the homepage toggle.'
    evidence:
    - packing/src/sqpack/release.py
    stop_reason: The owner asked for the session's cost rollups to be committed and the handoff captured
      on the pull request.
    next_action: Commit the rollups and capture the handoff.
  - workflow: review-planning-oversight
    focus: process
    recording: contemporaneous
    clock_role: work
    objective: Commit the session's eleven cost rollups, record the owner action the session cannot take,
      and capture the full handoff for the next agent on the pull request.
    bead: think-los0
    status: completed
    entered_by: user_request
    switch_reason: The owner asked for every piece of the session's work, its cost included, to be on
      the pull request for handoff.
    budget_minutes: 120
    started_at: '2026-10-02T16:29:54Z'
    deadline_at: '2026-10-02T18:29:54Z'
    expected_output: The eleven rollups committed and declared, a bead for the owner's restoring commit,
      a pull request description that hands off every open bead, and green hosted CI.
    validation_command: cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: A rollup cannot be committed without the model identifiers this session does not
      push.
    fallback: Commit the rollups with the identifiers withheld and give the owner the originals and the
      restoring commit.
    outcome: 'The fallback ran: fefca54a5 commits and declares the eleven rollups with the two model labels
      withheld, think-wqfw carries the owner''s restoring commit, and the pull request description hands
      off every open bead. Hosted validate failed once on the in-progress deadlines, which fb8cc9633 repaired;
      fb8cc9633 and the owner''s 1e035d274 are green on every required check.'
    evidence:
    - packing/campaign/resource-usage/6179239e-fec5-52e8-aabb-a0e229f3f822.yaml
    stop_reason: The owner asked for all the open work to continue.
    next_action: Plan the open beads as parallel lanes.
  - workflow: remediation
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: 'Work every open bead under think-los0 in parallel lanes: the Lean replay (think-ym34),
      the T-007 re-grounding (think-xucp) with its k^2-2 branch decided by the replay, and the regularized
      layer''s remaining scope (think-bgkz: the deferred --verify-atlas checkpoint, the dilation policy,
      the homepage toggle).'
    bead: think-xucp
    status: completed
    entered_by: user_request
    switch_reason: The owner asked for all the open work to continue, the T-007 re-grounding included.
    budget_minutes: 240
    started_at: '2026-10-02T17:16:17Z'
    deadline_at: '2026-10-02T21:16:17Z'
    expected_output: A replay receipt or a recorded failure for chelokot's theorem; T-007 and its consumers
      re-grounded per the review with a defect entry and every view regenerated; the regularized layer's
      remaining items built or refused with reasons; green hosted CI.
    validation_command: cd packing && uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: The replay cannot run on this host, or re-grounding changes a value the review did
      not recommend.
    fallback: Record the replay blocker, apply the re-grounding with s(k^2-2) at V0/C0, and leave the
      blocked layer items on think-bgkz with their reason.
    outcome: 'All four lanes reached their exits and were integrated (dc7867f1f, 6200bcf23 and fixes through
      730f4f2e1, green on every required check). The Lean replay passed, so s(k^2-2) = k stands at V3/C3
      (T-086); T-007 is V0/C1 and 271 case records are re-grounded (T-083, T-084, T-085, D-516); the homepage
      toggle, the deferred regularized-views job and the dilation decision (refusal kept) close think-bgkz
      but for its first hosted measurement.'
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/chelokot-lean-replay/receipt.json
    - packing/frontier/results.yaml
    - packing/atlas/known-best/regularized/rendering/
    stop_reason: The owner asked that the Karakus-based floors stay marked new and be tagged as corrections
      naming the published work they correct.
    next_action: Add the corrects field and its tag, and cite D-516 in the case records' corrections.
  - workflow: remediation
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: 'Tag each recent lower bound that corrects a published result with the work it corrects
      ("corrects Nagamochi 2005"), from a register field on the replacing results, on every surface that
      marks a bound recent; and make every case record''s dated correction cite this register''s own defect
      entry, D-516, so a correction of outside work and a correction of our own record stay distinct.'
    bead: think-los0
    status: stopped
    entered_by: user_request
    switch_reason: The owner asked for the corrections to be marked as new and as corrections, naming the
      previous work corrected, with corrections to our own record kept within our own process.
    budget_minutes: 120
    started_at: '2026-10-02T20:50:30Z'
    deadline_at: '2026-10-02T22:50:30Z'
    expected_output: A checked corrects field on T-083, T-084 and T-086; the tag on the frontier table,
      case pages, homepage atlas popovers and the workbench stage; D-516 cited in every dated correction;
      green hosted CI.
    validation_command: cd packing && uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: A surface cannot carry the tag without dropping a citation or breaking a page ceiling.
    fallback: Carry the tag in the data and on the surfaces that fit it, and list the rest on a bead.
    outcome: 'Half done: the corrects field and its check, and D-516 in all 293 dated corrections, are pushed
      (9bed45b36, green); the surfaces lane wrote the data field, the composite count, the case pages and
      the frontier table before the account''s weekly usage limit stopped it at about 21:05Z.'
    evidence:
    - packing/frontier/results.yaml
    stop_reason: The surfaces lane hit the account's weekly usage limit, and no further delegation was possible.
    next_action: Finish the tag on the remaining surfaces in the coordinator's own hand.
  - workflow: remediation
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: 'Finish the correction tag the surfaces lane left: the workbench stage and the homepage atlas
      popover, the frontier tests, and the gate; then integrate, re-pin and push.'
    bead: think-los0
    status: completed
    entered_by: user_request
    switch_reason: The owner asked to try again after the usage limit stopped the surfaces lane.
    budget_minutes: 120
    started_at: '2026-10-03T04:51:15Z'
    deadline_at: '2026-10-03T06:51:15Z'
    expected_output: The tag on every surface that marks a bound recent, each with a test, and green hosted
      CI.
    validation_command: cd packing && uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: A surface cannot carry the tag without dropping a citation or breaking a page ceiling.
    fallback: Carry the tag on the surfaces that fit it and list the rest on a bead.
    outcome: 'The tag reads "corrects Nagamochi 2005" on the frontier table, case pages, homepage atlas
      popover and workbench stage (e2ba1accd, 075d91dbf); hosted CI green on every required check, the
      workbench browser check included.'
    evidence:
    - packing/atlas/known-best/bound-citations.json
    stop_reason: The owner asked to proceed with all remaining items.
    next_action: Register Basic-Slivkova's bound (think-jkeu), measure the deferred job, close the session.
  - workflow: remediation
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: 'Every remaining item: register Basic and Slivkova''s piercing bound by the new result publication
      sequence (think-jkeu), measure the deferred regularized-views job on hosted runners (think-bgkz),
      and close session-168 with its rollups and a certifying gate.'
    bead: think-jkeu
    status: completed
    entered_by: user_request
    switch_reason: The owner asked to proceed with all remaining items, following the full standard process
      for recording new results.
    budget_minutes: 180
    started_at: '2026-10-03T05:30:00Z'
    deadline_at: '2026-10-03T08:30:00Z'
    expected_output: T-087 registered and published through every surface; the deferred job's first hosted
      reading in gate-budgets.yaml; a terminal session record.
    validation_command: cd packing && uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: The published proof does not survive the read, or the deferred job cannot be dispatched.
    fallback: Record the finding on think-jkeu, or leave the measurement on think-bgkz with its blocker.
    outcome: 'Basic and Slivkova''s Theorem 7 was read and re-derived and registered as T-087 by the new
      result publication sequence: the verified floor at n = 37 (6.158554, not stated in the paper) and
      n = 61 (7.890604, their Theorem 10), the only cases where it beat the held floor. The deep gate''s
      first dispatch measured regularized-views at 310 s of job wall, recorded in gate-budgets.yaml. The
      sixteen rollups are committed with model labels withheld. Hosted CI is green at dd636b4cc.'
    evidence:
    - packing/frontier/results.yaml
    - packing/campaign/series/series-000-smoke-and-calibration/results/piercing-lower-bounds.json
    - packing/devtools/gate-budgets.yaml
    stop_reason: Every remaining item done but the owner's restoring commit for the withheld model labels.
    next_action: 'Owner: think-wqfw, the restoring commit for the sixteen rollups'' withheld model labels.'
  budget:
    wall_minutes: 1696
    slice_minutes: 30
    finalization_minutes: 60
  stop_conditions:
  - The owner ends the run; a self-declared budget is not a stop condition (OR-8).
  - No regularized pose replaces a source witness, changes a side, or promotes a tier.
  - No retained measurement without a tool and tests that reproduce it (OR-1).
  progress:
    metric: Owner questions answered at their evidential scope, with tools retained.
    before: The atlas shows 324 known-best packings and their contact shading; nothing in the record classifies
      them into families, explains the light shading, or connects the families to the asymptotic waste
      register.
    after: 'X-049 answers the four questions. Nagamochi 2005''s Lemma 1 is false, so T-007 is V0 and
      271 case records are re-grounded with dated corrections citing D-516; s(k^2-2) = k stands on a
      replayed Lean proof (T-086), the open floors on Karakus (T-083, T-084), n = 37 and 61 on Basic and
      Slivkova (T-087), and each correcting floor says "corrects Nagamochi 2005". The regularized layer
      has its homepage toggle and a measured deferred job. Open: think-wqfw, the owner''s restoring commit.'
  delegations:
  - task: 'think-zfxi: literature survey of square-packing families by position relative to k^2 (W1-shaped,
      read-only).'
    operator: Claude subagent
    status: completed
    recording: contemporaneous
    phase: 1
    elapsed_quality: platform_measured
    outcome: No taxonomy keyed by n - k^2 exists; named constructions and family theorems tabulated; the
      L step explains the triangle columns; Karakus 2026 proof gap found; nine acquisition follow-ups
      and dated negative searches.
    evidence:
    - packing/campaign/explorations/X-049-families-shading-and-the-large-n-limit.md
    files: []
    checks:
    - coordinator re-read arXiv:2609.37410 abstract on 2026-10-02 and confirmed the claim
    uncertainty: Catalogue values quoted from Kingbird disagree with the atlas at s(301); the atlas uses
      the Couzo packet.
    elapsed_seconds: 745.0
    next_action: Integrated into X-049 by the coordinator.
    write_scope:
    - scratchpad lane note, not retained
  - task: 'think-am9n: asymptotic behaviour of the families and the finite-versus-infinite pattern question
      (read-only mathematics).'
    operator: Claude subagent
    status: completed
    recording: contemporaneous
    phase: 1
    elapsed_quality: platform_measured
    outcome: Fixed-offset, linear-offset and d_max(k) limits derived with status per step; three formulations
      F1-F3 of the finiteness question; four candidate hypotheses; register corrections (Erdős-Graham
      Theta, Göbel origin of 10^-100).
    evidence:
    - packing/campaign/explorations/X-049-families-shading-and-the-large-n-limit.md
    files: []
    checks:
    - coordinator re-derived the fixed-d bracket, the c/2 limit, the d_max upper bound and the mid-row
      Roth-Vaughan bound; Erdős-Graham Theorem (1) checked on the rendered PDF page
    uncertainty: Constants in the O(x^(3/5)) bound are unevaluated, so the bracket is asymptotic only.
    elapsed_seconds: 1036.0
    next_action: Integrated into X-049 by the coordinator.
    write_scope:
    - scratchpad lane note, not retained
  - task: 'think-jkhp: family census tool over the 324 known-best witnesses.'
    operator: Claude subagent
    status: completed
    recording: contemporaneous
    phase: 1
    elapsed_quality: platform_measured
    outcome: Tool, 26 tests and retained JSON; L chains, closed forms, symmetry, grid-held widths, excess
      table and Göbel strip check.
    evidence:
    - packing/campaign/explorations/X049-families-data/family-census.json
    files:
    - packing/devtools/classify_known_best_families.py
    - packing/tests/test_known_best_families.py
    - packing/campaign/explorations/X049-families-data/family-census.json
    checks:
    - coordinator ran the 26 tests, ruff, basedpyright and --check (8.8 s)
    uncertainty: Integer-side records are canonical grid subsets, so their arrangement is convention.
    elapsed_seconds: 1490.0
    next_action: Integrated into X-049 by the coordinator.
    write_scope:
    - packing/devtools/classify_known_best_families.py
    - packing/tests/test_known_best_families.py
    - packing/campaign/explorations/X049-families-data/family-census.json
  - task: 'think-ea3f: contact-shade census replicating the atlas and workbench shading rules.'
    operator: Claude subagent
    status: completed
    recording: contemporaneous
    phase: 1
    elapsed_quality: platform_measured
    outcome: Tool, 13 tests and retained JSON; the homepage atlas uses the house rule at 2e-6; 34 of 7,725
      light green squares are within ten tolerances; replicas agree on all 52,650 squares.
    evidence:
    - packing/campaign/explorations/X049-families-data/contact-shade-census.json
    files:
    - packing/devtools/census_atlas_contact_shades.py
    - packing/tests/test_atlas_contact_shades.py
    - packing/campaign/explorations/X049-families-data/contact-shade-census.json
    checks:
    - coordinator ran the tests, the module-boundary tests and --check (7.6 s), and added the --witness
      mode with a test
    uncertainty: The within-band squares are consistent with optimizer non-convergence; the census cannot
      distinguish that from source rounding.
    elapsed_seconds: 1985.0
    next_action: Integrated into X-049 by the coordinator.
    write_scope:
    - packing/devtools/census_atlas_contact_shades.py
    - packing/tests/test_atlas_contact_shades.py
    - packing/campaign/explorations/X049-families-data/contact-shade-census.json
  - task: 'think-31v0: exact regularization feasibility and prototype.'
    operator: Claude subagent
    status: completed
    recording: contemporaneous
    phase: 1
    elapsed_quality: platform_measured
    outcome: Prototype tool with 7 tests; exact derived views for 102, 103, 106, 206, 268, 269 verified
      twice over Q at the certificate side with no change of side.
    evidence:
    - packing/campaign/explorations/X049-families-data/regularized/run.txt
    files:
    - packing/devtools/regularize_axis_components.py
    - packing/tests/test_regularize_axis_components.py
    checks:
    - coordinator reran the six cases (99 s), re-verified the 106 view with the independent checker, and
      made --output-dir required
    uncertainty: Algebraic-field and interval-enclosure witnesses were not prototyped; a neighbour non-regression
      rule is still missing.
    elapsed_seconds: 1662.0
    next_action: Integrated into X-049 by the coordinator.
    write_scope:
    - packing/devtools/regularize_axis_components.py
    - packing/tests/test_regularize_axis_components.py
  - task: 'think-589i lane A: audit Nagamochi Lemma 1 against Karakus 2026.'
    operator: Claude subagent
    status: completed
    recording: contemporaneous
    phase: 3
    elapsed_quality: platform_measured
    outcome: Lemma 1 false for a > 3, b > 2; gap reaches T-007 for N >= 10; Karakus Theorem 1.1 re-derived;
      recommended statuses.
    evidence:
    - docs/project/reviews/review-2026-10-02-nagamochi-lemma1-karakus.md
    files:
    - docs/project/reviews/review-2026-10-02-nagamochi-lemma1-karakus.md
    - packing/devtools/check_nagamochi_lemma1_counterexample.py
    - packing/tests/test_nagamochi_lemma1_counterexample.py
    checks:
    - coordinator ran the checker (0.23 s) and its 35 tests, read the review, and checked Karakus Corollary
      6.2 in the archive
    uncertainty: chelokot Lean archive not built; Karakus proof read, not machine-checked.
    elapsed_seconds: 1968.0
    next_action: Integrated by the coordinator.
    write_scope:
    - docs/project/reviews/review-2026-10-02-nagamochi-lemma1-karakus.md
    - packing/devtools/check_nagamochi_lemma1_counterexample.py
    - packing/tests/test_nagamochi_lemma1_counterexample.py
  - task: 'think-589i lane B: inventory everything resting on T-007.'
    operator: Claude subagent
    status: completed
    recording: contemporaneous
    phase: 3
    elapsed_quality: platform_measured
    outcome: 287 records cite the bound (238 open, 49 proved; 224 beyond the registered scope); exposure
      classes; document worklist without line numbers.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/t007-consumer-audit.json
    files:
    - packing/devtools/audit_t007_consumers.py
    - packing/tests/test_t007_consumer_audit.py
    - packing/campaign/series/series-000-smoke-and-calibration/results/t007-consumer-audit.json
    checks:
    - coordinator ran --check through the gate (1.15 s) and the 33 tests
    uncertainty: Document scan is word-based; Bentz borrowings from Nagamochi not decided.
    elapsed_seconds: 1890.0
    next_action: Integrated by the coordinator.
    write_scope:
    - packing/devtools/audit_t007_consumers.py
    - packing/tests/test_t007_consumer_audit.py
    - packing/campaign/series/series-000-smoke-and-calibration/results/t007-consumer-audit.json
  - task: 'think-1n8w and think-hzv3: archive sources and correct the asymptotic record.'
    operator: Claude subagent
    status: completed
    recording: contemporaneous
    phase: 3
    elapsed_quality: platform_measured
    outcome: Karakus, chelokot and five Kingbird pages archived; D-514 (Erdos-Graham) and D-515 (McClenagan)
      corrected; register notes added.
    evidence:
    - packing/defects.yaml
    - packing/frontier/asymptotic-waste-bounds.yaml
    files:
    - packing/resources/papers/karakus-2026-counterexample-nagamochi-scoring-lemma.md
    - packing/defects.yaml
    - packing/frontier/asymptotic-waste-bounds.yaml
    checks:
    - coordinator checked the McClenagan page and Karakus Corollary 6.2 against the PDFs
    uncertainty: Book-only sources have no bibliography entry.
    elapsed_seconds: 1697.0
    next_action: Integrated by the coordinator.
    write_scope:
    - packing/resources/
    - packing/defects.yaml
    - defects.md
    - packing/frontier/asymptotic-waste-bounds.yaml
    - docs/project/research/research-2026-08-22-packing-11-unit-squares.md
  - task: 'think-ptt7: codify the X-049 candidate hypotheses.'
    operator: Claude subagent
    status: completed
    recording: contemporaneous
    phase: 3
    elapsed_quality: platform_measured
    outcome: H-269, H-270 and H-272 registered; the beta exponent parked under H-037.
    evidence:
    - packing/campaign/hypotheses/H-270-k2-plus-1-crossover-kearney-shiu-strip.md
    files:
    - packing/campaign/hypotheses/H-269-periodic-certificates-k2-minus-4-and-5.md
    - packing/campaign/hypotheses/H-270-k2-plus-1-crossover-kearney-shiu-strip.md
    - packing/campaign/hypotheses/H-272-symmetric-kingbird-records-reoptimized.md
    checks:
    - coordinator ran the ledger check after updating ideas.md and SYNOPSIS
    uncertainty: H-269 relies on a source-reported LP deficit; H-270 hand estimate unmeasured.
    elapsed_seconds: 1001.0
    next_action: Integrated by the coordinator.
    write_scope:
    - packing/campaign/hypotheses/
  - task: 'think-bgkz: build the regularized-view layer.'
    operator: Claude subagent
    status: completed
    recording: contemporaneous
    phase: 3
    elapsed_quality: platform_measured
    outcome: 51 records regularized with a non-regression rule; atlas light green 7,725 to 5,475; legends
      updated; toggle left as a design note.
    evidence:
    - packing/atlas/known-best/regularized/index.json
    files:
    - packing/devtools/regularize_axis_components.py
    - packing/tests/test_regularize_axis_components.py
    - packing/atlas/known-best/regularized/index.json
    - packages/workbench/src/application.js
    - packing/devtools/overview_sections.py
    checks:
    - coordinator ran the 11 tests and --check-atlas (0.10 s), and the edit tier passed with the layer
      in the tree
    uncertainty: Workbench Chromium step not runnable here (Playwright build mismatch); 89 Kingbird records
      refused at dilation 1.
    elapsed_seconds: 2302.0
    next_action: Integrated by the coordinator.
    write_scope:
    - packing/devtools/regularize_axis_components.py
    - packing/tests/test_regularize_axis_components.py
    - packing/atlas/known-best/regularized/
    - packages/workbench/src/application.js
    - packing/devtools/overview_sections.py
  - task: 'think-bgkz item 1: the homepage House/Regularized atlas toggle.'
    operator: Claude subagent
    status: completed
    recording: contemporaneous
    phase: 6
    elapsed_quality: platform_measured
    outcome: 'An "Atlas drawings" tab strip swaps each of the 51 regularized cases to a badged tile drawn
      by the house renderer from the regularized pose, selected by ?layer=regularized; cases without a
      view keep their house tile. devtools.render_regularized_atlas draws the 51 renderings from index.json,
      refuses digest mismatches, and --check names missing, stale or unexpected files in about 7 s.'
    evidence:
    - packing/atlas/known-best/regularized/rendering/
    files:
    - packing/devtools/render_regularized_atlas.py
    - packing/devtools/overview/atlas-layer.js
    - packing/tests/test_render_regularized_atlas.py
    - packing/tests/node/overview_atlas_layer/atlas-layer.test.mjs
    checks:
    - coordinator ran render_regularized_atlas --check (51 views, 6.6 s), its 5 tests and --check-atlas
      with the rendering directory exempted
    uncertainty: The browser tests ran here on the pre-installed Chromium 141 only; hosted CI runs the
      pinned build. The renderings add 11 MB to the repository and 48 kB gzipped to the homepage.
    elapsed_seconds: 2619.0
    next_action: Integrated by the coordinator with a gate step and the data-revision re-pin.
    write_scope:
    - packing/devtools/render_regularized_atlas.py
    - packing/devtools/overview/
    - packing/devtools/overview_sections.py
    - packing/devtools/render_overview.py
    - packing/devtools/render_frontier_page.py
    - packing/devtools/measure_atlas_views.py
    - packing/devtools/templates/
    - packing/atlas/known-best/regularized/rendering/
    - packing/tests/
    - .github/workflows/pages.yml
  - task: 'think-ym34: replay chelokot''s Lean proof of s(n^2-2) = n with an axiom receipt.'
    operator: Claude subagent
    status: completed
    recording: contemporaneous
    phase: 6
    elapsed_quality: operator_reported_approximate
    outcome: 'The replay passed: SquarePackingArchive.Records.NearSquare.squareMinusTwo_isMinimumSide
      builds at 753079eb under Lean v4.33.0 and Mathlib db584cd6 and depends only on propext, Classical.choice
      and Quot.sound; the archive has 0 sorry, 0 axiom declarations and 0 native_decide in 277 files,
      and its 79 axiom assertions pass. IsMinimumSide reads as the register''s s(N).'
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/chelokot-lean-replay/receipt.json
    files:
    - packing/devtools/replay_chelokot_lean.py
    - packing/tests/test_replay_chelokot_lean.py
    - packing/campaign/series/series-000-smoke-and-calibration/results/chelokot-lean-replay/receipt.json
    - packing/campaign/series/series-000-smoke-and-calibration/results/chelokot-lean-replay/build.log
    checks:
    - coordinator ran replay_chelokot_lean --check (exit 0), the 61 tests, and read the theorem's axiom
      line in the retained build log (line 284)
    uncertainty: The final run rebuilt 4 modules over a same-session build of the other 273 from source;
      a single-run from-source rebuild (about 1 hour) was not repeated. The statement-fidelity read is
      not a human formalization review, so it supports V3/C3, not V5.
    elapsed_seconds: 4690.0
    next_action: The pass branch of think-xucp applies it.
    write_scope:
    - packing/devtools/replay_chelokot_lean.py
    - packing/tests/test_replay_chelokot_lean.py
    - packing/campaign/series/series-000-smoke-and-calibration/results/chelokot-lean-replay/
  - task: 'think-bgkz items 2 and 3: the deferred --verify-atlas checkpoint and the smallest-dilation
      policy.'
    operator: Claude subagent
    status: completed
    recording: contemporaneous
    phase: 6
    elapsed_quality: operator_reported_approximate
    outcome: '--verify-atlas is the deferred step `regularized atlas views re-derive exactly` in its own
      regularized-views job (about 800 cpu-seconds; 223 s at four workers) with a 450 s derived ceiling.
      The smallest verifying dilation opens all 89 refused Kingbird records, but 75 views would sit below
      the register''s verified upper bound (a tier promotion) and 14 would enlarge the container, for
      a gain of two squares, so the refusal stays and the flag remains as the instrument.'
    evidence:
    - packing/atlas/known-best/README.md
    files:
    - packing/devtools/regularize_axis_components.py
    - packing/tests/test_regularize_axis_components.py
    - packing/src/sqpack/cli/validate.py
    - .github/workflows/deep-gate.yml
    - .github/workflows/packing-validation.yml
    - packing/devtools/gate-budgets.yaml
    - development.md
    checks:
    - coordinator ran the validation CLI, module-boundary, deep-gate and post-merge contract tests (194
      passed with the frontier-corpus test deselected for lane B's interim state) and --check-atlas
    uncertainty: The 450 s ceiling is derived from a local four-worker reading on a shared host; the first
      hosted dispatch replaces it.
    elapsed_seconds: 3800.0
    next_action: Integrated by the coordinator.
    write_scope:
    - packing/devtools/regularize_axis_components.py
    - packing/tests/
    - packing/atlas/known-best/regularized/
    - packing/atlas/known-best/README.md
    - packing/src/sqpack/cli/validate.py
    - .github/workflows/
    - packing/devtools/gate-budgets.yaml
    - development.md
  - task: 'think-xucp: re-ground the register''s reliance on T-007 per the 2026-10-02 review, with the
      k^2-2 branch decided by the Lean replay.'
    operator: Claude subagent
    status: completed
    recording: contemporaneous
    phase: 6
    elapsed_quality: operator_reported_approximate
    outcome: 'T-007 to V0/C1 incomplete; E-nagamochi-lower reported with a defect-found review; new
      E-karakus-strip-lower, E-nagamochi-lemma1-counterexample and E-chelokot-square-minus-two-lean; new
      T-083 (Karakus general floor, V3/C1), T-084 (s(k^2-1) = k, V3/C1), T-085 (Lemma 1 correction,
      V3/C3) and T-086 (s(k^2-2) = k on the replayed Lean proof, V3/C3). 271 case records re-grounded:
      perfect squares on the area bound, k^2-1 on Karakus, k^2-2 on the Lean proof (values unchanged),
      238 open floors on Karakus Corollary 6.2, and n = 54, 57, 73 on T-044''s registered monotonicity
      values. No status changed; no verified floor rests on T-007. D-516 records the defect.'
    evidence:
    - packing/frontier/results.yaml
    - packing/frontier/evidence.yaml
    - packing/campaign/series/series-000-smoke-and-calibration/results/t007-consumer-audit.json
    files:
    - packing/frontier/results.yaml
    - packing/frontier/evidence.yaml
    - packing/devtools/generate_frontier_case.py
    - packing/devtools/audit_t007_consumers.py
    - packing/devtools/check_nagamochi_bounds.py
    - packing/devtools/check_basic_bounds.py
    - packing/devtools/render_frontier_page.py
    - packing/defects.yaml
    checks:
    - coordinator set FRONTIER_COUNTS to the lane's measured (261, 249, 0) and the frontier corpus step
      passed; the coordinator's gate run covers the rest
    uncertainty: 'Two departures from the review''s literal text, both by coordinator decision: n = 54,
      57 and 73 carry the stronger registered T-044 values rather than Karakus''s, and n = 61 keeps Karakus''s
      value with a note naming Basic-Slivkova''s stronger archived bound (think-jkeu). T-083 and T-084
      carry S3 by the lane''s judgement.'
    elapsed_seconds: 5200.0
    next_action: Integrated by the coordinator.
    write_scope:
    - packing/frontier/
    - packing/atlas/known-best/bound-citations.json
    - packing/atlas/known-best/composite-figure.json
    - packing/defects.yaml
    - defects.md
    - SYNOPSIS.md
    - docs/project/research/
    - packing/devtools/
    - packing/tests/
    - packing/campaign/series/series-000-smoke-and-calibration/results/t007-consumer-audit.json
  - task: 'Correction tag: carry the corrects field into bound-citations.json and draw "corrects Nagamochi
      2005" beside every recent lower bound on the site and the stage.'
    operator: Claude subagent
    status: canceled
    recording: contemporaneous
    phase: 7
    elapsed_quality: operator_reported_approximate
    outcome: 'Stopped by the account''s weekly usage limit at about 21:05Z, after writing the data field and
      its schema, the composite figure''s correction count, the case pages'' and frontier table''s tag with
      their tests, and the frontier page''s explanatory sentence. The coordinator verified that work (168
      tests passed) and finished the stage and the homepage popover in phase 8.'
    evidence:
    - packing/atlas/known-best/bound-citations.json
    files:
    - packing/devtools/build_bound_citations.py
    - packing/devtools/render_frontier_page.py
    - packing/devtools/render_case_pages.py
    - packing/devtools/build_composite_figure_data.py
    checks:
    - coordinator ran build_bound_citations and build_composite_figure_data --check and the citation, frontier
      page, case page and composite tests (168 passed) on the lane's tree
    uncertainty: The lane left no report; what it changed is read from the working tree.
    elapsed_seconds: 900.0
    next_action: Finished by the coordinator.
    write_scope:
    - packing/devtools/
    - packing/atlas/known-best/bound-citations.json
    - packing/atlas/known-best/composite-figure.json
    - packing/tests/
  outputs:
  - packing/campaign/explorations/X-049-families-shading-and-the-large-n-limit.md
  - packing/devtools/replay_chelokot_lean.py
  - packing/campaign/series/series-000-smoke-and-calibration/results/chelokot-lean-replay/receipt.json
  - packing/devtools/render_regularized_atlas.py
  - packing/devtools/check_piercing_lower_bounds.py
  - packing/frontier/results.yaml
  - packing/campaign/explorations/X049-families-data/family-census.json
  - packing/campaign/explorations/X049-families-data/contact-shade-census.json
  - packing/campaign/explorations/X049-families-data/regularized/run.txt
  - packing/campaign/explorations/X049-families-data/regularized/shades.txt
  - packing/devtools/classify_known_best_families.py
  - packing/devtools/census_atlas_contact_shades.py
  - packing/devtools/regularize_axis_components.py
  - packing/src/sqpack/cli/validate.py
  - packing/campaign/ideas.md
  - docs/project/reviews/review-2026-10-02-nagamochi-lemma1-karakus.md
  - packing/devtools/check_nagamochi_lemma1_counterexample.py
  - packing/devtools/audit_t007_consumers.py
  - packing/atlas/known-best/regularized/index.json
  - packing/resources/papers/karakus-2026-counterexample-nagamochi-scoring-lemma.md
  - packing/campaign/hypotheses/H-269-periodic-certificates-k2-minus-4-and-5.md
  checks:
  - packing-validate --only "known-best family and contact-shade censuses" passed in 16.42 s.
  - 'pytest over the four touched test files: 64 passed; tests/test_validation_cli.py, test_validation_report.py
    and test_validation_timing.py: 185 passed.'
  - 'ruff check, ruff format and basedpyright: zero findings on every new or changed Python file.'
  - 'devtools.check_math_markup: clean, backlog 0.'
  - packing-validate --edit passed (54 steps) with the follow-up lanes in the tree, 187 s.
  - 'packing-validate --records passed after integration; new steps: the T-007 inventory (1.15 s) and
    the regularized atlas check (0.11 s).'
  - 'packing-validate --records passed 42 of 42 at the T-087 registration; build_known_best_atlas --check
    --sample passed (36 of 324 rebuilt, composites trailing the pin as allowed until the next version).'
  - 'full gate: fast at dd636b4ccaea8dff8b7c083cb32ff90d1dbc5e71: passed (hosted Packing validation run
    37101500066: validate, frontend, typecheck, geometry, suite-a to suite-d and sweeps, the nine
    pull-request jobs that together are the fast tier, all succeeded; Certificate page 37101500127 too)'
  resource_rollups:
  - packing/campaign/resource-usage/6179239e-fec5-52e8-aabb-a0e229f3f822.yaml
  - packing/campaign/resource-usage/agent-a30ab1dd97b959c63.yaml
  - packing/campaign/resource-usage/agent-a4a764a6285487659.yaml
  - packing/campaign/resource-usage/agent-a665a16af102749a0.yaml
  - packing/campaign/resource-usage/agent-a68c888b24723b197.yaml
  - packing/campaign/resource-usage/agent-a86fe91008fdb802b.yaml
  - packing/campaign/resource-usage/agent-a92ea862bac5a1405.yaml
  - packing/campaign/resource-usage/agent-a9f4406a56646937f.yaml
  - packing/campaign/resource-usage/agent-abfdcf4d3642c3fe2.yaml
  - packing/campaign/resource-usage/agent-ad8c36a04ebcd61d9.yaml
  - packing/campaign/resource-usage/agent-ae1c5c75727ba7c4d.yaml
  - packing/campaign/resource-usage/agent-ab5f6ac0531baee62.yaml
  - packing/campaign/resource-usage/agent-a2f9102eba6720d45.yaml
  - packing/campaign/resource-usage/agent-a5e0eae4c2694a29b.yaml
  - packing/campaign/resource-usage/agent-a72b23ec598f03d8c.yaml
  - packing/campaign/resource-usage/agent-a0ce03a4c2b6775a7.yaml
  stop_reason: The owner's questions are answered and every follow-up bead is closed, with hosted CI green
    at the certified commit, but think-wqfw, the owner's restoring commit for the sixteen rollups' withheld
    model labels.
  next_action: 'Selected next entry unchanged: think-11ma, the exact geometric-exclusion pilot below the
    certified n17 endpoint. Identifiers T-083 to T-087 and session-168 collide with open PRs 292, 298,
    307 and 311; the one landing second renumbers.'
---
# Families of Known-Best Packings, Contact Shading, and the Large-n Limit

The owner asked four questions after the atlas triangle view put all 324 known-best
packings side by side: whether the visible families have been studied, whether light
contact shading is arithmetic error, whether exact regularization can fix it, and what
happens to the families as $n$ grows.
Five lanes run in parallel under `think-los0`; the coordinator owns the frontier
coverage lane and writes
[X-049](../explorations/X-049-families-shading-and-the-large-n-limit.md).

This record was written about five minutes after the lanes were dispatched at 05:19Z,
not before; the phase start is the epic’s creation time.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
