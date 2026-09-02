---
title: session-074 — BC-124 n = 68 production adapter
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-074
  title: BC-124 n = 68 production adapter
  date: '2026-09-01'
  started_at: '2026-09-02T00:15:00Z'
  deadline_at: '2026-09-02T02:45:00Z'
  branch: codex/agenda014-six-hour-run
  goal: >-
    Build and independently admit exp-054's complete target-blind production adapter so
    a later block can reach one bounded n = 68 parent without weakening provenance,
    transform, serialization, proof, cleanup or publication guards.
  workflow_phases:
  - workflow: insight-iteration
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Bind the current post-review exp-047 and exp-051 hashes to their historical Packet
      B transition, freeze the literal command and complete adapter boundary, and refuse
      every target or network surface before W7 begins.
    commitment: BC-124
    bead: think-3i67
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 15
    started_at: '2026-09-02T00:15:00Z'
    deadline_at: '2026-09-02T00:30:00Z'
    expected_output: A validated exp-054 adapter contract and literal injected-stream command.
    validation_command: >-
      uv run --frozen softschema validate
      campaign/series/series-000-smoke-and-calibration/experiments/exp-054-h-058-n68-one-parent-production-serialization.md
    kill_condition: >-
      Stop if the authorized review-flag transition is not the only Packet B difference,
      the adapter omits any production seam, or a target/network command would run.
    fallback: Retain the exact provenance or adapter-contract defect and stop before W7.
    outcome: >-
      Artifact: session-074 and exp-054 bind launch revision 909efafa, the current
      exp-047 SHA-256 f209cd6f5fd6daa6c883143f97457dff441d4b61541829a9243bd55cc09e3b27
      and exp-051 SHA-256 ed4a45f2e02a39fe1833d7405ded90472aba008662f58aeeb1dfbe5b37354c54.
      Result: comparison with Packet B reproduced exactly one authorized field change in
      each experiment, `needs_review: true` to `false`; session-069, refusal/run.py,
      refusal/verify.py and the focused baseline test retain their packet hashes. The
      exp-054 result is absent. Guard: this cell opened no network, parent, child, gain or
      target geometry and ran no scientific command. H-058 stays unmeasured; this round
      admits only selected-polygon wall-proof machinery and synthetic pair controls.
      Next: enter the 00:30--00:50 W7 cell and require the exact `--record` argv to reach
      an injected in-memory adapter boundary before its deadline.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-054-h-058-n68-one-parent-production-serialization.md
    - packing/campaign/hypotheses/H-058-n68-one-parent-production-serialization.md
    stop_reason: The target-blind W3 provenance and adapter contract passed.
    next_action: Run the fixed 00:30--00:50 literal-entry W7 cell without target access.
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Implement the executable production CLI and fresh-output skeleton, then drive its
      exact `--record` argv through an injected bounded byte stream and temporary output
      root without exposing a target or network channel.
    commitment: BC-124
    bead: think-3i67
    status: completed
    entered_by: planned_checkpoint
    switch_reason: The W3 contract and provenance bridge passed at the fixed boundary.
    budget_minutes: 20
    started_at: '2026-09-02T00:30:00Z'
    deadline_at: '2026-09-02T00:50:00Z'
    expected_output: >-
      A production module whose literal exp-054 argv reaches injected dependencies,
      refuses the real output root during selftest and publishes only below a temporary
      root.
    validation_command: >-
      uv run --frozen python -m cases.unitsquare_precision.production.run
      --record
      campaign/series/series-000-smoke-and-calibration/results/exp-054-h-058-n68-one-parent-production-serialization.json
    kill_condition: >-
      Stop if the CLI cannot reach the injected adapter by 00:50Z, invokes a default
      opener, creates the canonical result, accepts a mismatched path or authorization,
      or depends on assertion-only checks.
    fallback: >-
      Retain the first literal-entry defect in session-074 and exp-054 and stop before
      scanner or model implementation.
    outcome: >-
      Artifact: run.py executes the exact bare exp-054 `--record` argv behind injected
      dependencies; adapter.py and verify.py provide the first executable scanner,
      transform, model and whole-result seams, and the focused production test owns the
      command controls. Result: the literal injected boundary was reached at
      00:31:54Z, before the fixed 00:50Z gate. The final bare command then ran all
      three isolated models and produced byte-identical normal and optimized receipts;
      19 focused tests, Ruff and BasedPyright pass. Guard: the command used only an
      in-memory SVG and temporary output root. The real-parent dependency constructor is
      import-only, the canonical result remains absent, and no default opener, network,
      target, parent, child or gain channel was invoked. Next: harden the bounded opener,
      strict scanner and exact transform parser with the named mutation matrix in the
      fixed 00:50--01:15 W7 cell.
    evidence:
    - packing/cases/unitsquare_precision/production/run.py
    - packing/tests/test_unitsquare_precision_production.py
    stop_reason: The literal-entry gate passed before its fixed deadline.
    next_action: Run the fixed 00:50--01:15 parser and provenance W7 cell.
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Complete and mutation-test the exact-URL bounded opener, digest-before-parse
      structural scanner, unambiguous container parser and exact nested-transform
      implementation without opening any external source.
    commitment: BC-124
    bead: think-3i67
    status: completed
    entered_by: planned_checkpoint
    switch_reason: The literal injected production command passed before minute 35.
    budget_minutes: 25
    started_at: '2026-09-02T00:50:00Z'
    deadline_at: '2026-09-02T01:15:00Z'
    expected_output: >-
      Named normal and optimized controls for byte caps, exact URL and cleanup,
      container ambiguity, XML structure, transform order, singular maps and refused
      uncertified decimal rotations.
    validation_command: >-
      uv run --frozen pytest -q tests/test_unitsquare_precision_production.py -k
      'bounded or scanner or transform or digest'
    kill_condition: >-
      Stop if parsing can precede the digest guard, a redirect or oversize source can
      reach XML, transform order is ambiguous, or cleanup depends on assertions.
    fallback: Retain the first typed opener, scanner or transform defect and stop target-blind.
    outcome: >-
      Artifact: adapter.py SHA-256
      525c485c7d023d3dcb308c19f11d0c2dfacae8b55148f1522a914ff9ad739183,
      run.py ededfb794b01d452083b5866734cebec31d9850562604e3c9c3942782de9d5dd,
      verify.py e39a6a725e7af01a2e1796e1a218576f76b8a2ec2cecf7fbde3f38aeb9630a7a
      and the focused test
      a8ef4fe33a95665352d7950f8eea87bbb01633065a9478913fa78a06a9a4f3c8
      freeze the complete instrument at the observed 01:07:36Z boundary. Result: the
      exact URL and no-redirect opener, four-megabyte stream bound, cleanup, the rule
      that the digest gate precedes parsing, a strict selected-container scanner and
      exact nested transform composition, all three serialization models, adaptive exact
      wall proof and independent whole-result verifier integrate. Thirty-four focused tests, Ruff and
      BasedPyright pass. The literal normal and optimized receipts are byte-identical,
      1,112 bytes and SHA-256
      becb4c7f865f2f4b3a9d6bd22b11bb736efe73ba2d7dc97e025cd4becbd55906.
      Guard: the receipt uses an injected in-memory SVG and a temporary output root; the
      canonical result is absent and no network, target, parent, child, gain or surgery
      surface opened. Next: run the complete named mutation matrix against these frozen
      hashes and retain the first remaining refusal before W2 considers admission.
    evidence:
    - packing/cases/unitsquare_precision/production/adapter.py
    - packing/tests/test_unitsquare_precision_production.py
    stop_reason: The complete parser, model, proof and verifier integration passed target-blind.
    next_action: Run the integrated normal and optimized mutation cell on the frozen hashes.
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Exercise the complete literal command and every registered opener, scanner,
      transform, model, proof, verifier and publication mutation under normal and
      optimized Python, then name the first remaining refusal without changing the
      frozen instrument.
    commitment: BC-124
    bead: think-3i67
    status: completed
    entered_by: planned_checkpoint
    switch_reason: The complete strict parser, model and verifier integration passed.
    budget_minutes: 25
    started_at: '2026-09-02T01:07:36Z'
    deadline_at: '2026-09-02T01:32:36Z'
    expected_output: >-
      A named mutation matrix, byte-identical normal and optimized literal receipts and
      the exact first still-closed production refusal.
    validation_command: >-
      uv run --frozen pytest -q tests/test_unitsquare_precision_production.py && uv run
      --frozen python -m cases.unitsquare_precision.production.run --record
      campaign/series/series-000-smoke-and-calibration/results/exp-054-h-058-n68-one-parent-production-serialization.json
    kill_condition: >-
      Stop on any accepted mutation, normal/optimized difference, frozen hash drift,
      canonical-result creation or external-source access.
    fallback: Retain the first exact mutation or boundary failure and stop before W2.
    outcome: >-
      Artifact: the literal selftest's 20-name mutation receipt is byte-identical under
      normal and optimized Python at SHA-256
      becb4c7f865f2f4b3a9d6bd22b11bb736efe73ba2d7dc97e025cd4becbd55906.
      Result: it rejects wrong path, mismatched authorization, existing result, changed
      source byte, failed response cleanup, duplicate id, wrong polygon count, singular
      and uncertified transforms, reversed noncommuting transforms, wrong URL, redirect,
      oversize stream, model reorder, forged half-angle identity, missing cover evidence,
      wall sign across zero, separated-pair-to-overlap, child-channel and the rule that
      verification precedes publication. The 34-test focused suite additionally passes the strict XML,
      model isolation, exact proof, side-refusal, zeroing and interrupted-publication
      controls; the wrong-path CLI exits 2 with identical normal and optimized stderr.
      Guard: code and test hashes remain frozen at the preceding cell values, and the
      canonical result is absent. The exact first still-closed production boundary is
      `reported side token lacks exact or directional semantics`; production converts it
      to `serialization-refusal` for each model. It is expected premeasurement behavior,
      not a target sample, instrument defect or H-058 decision. Next: retain the exact
      proof/publication and import-boundary receipts, then stop W7 for cross-lane W2.
    evidence:
    - packing/cases/unitsquare_precision/production/adapter.py
    - packing/cases/unitsquare_precision/production/run.py
    - packing/cases/unitsquare_precision/production/verify.py
    - packing/tests/test_unitsquare_precision_production.py
    stop_reason: Every registered target-blind mutation fired its named guard.
    next_action: Freeze final proof, publication and import-boundary evidence for W2.
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Freeze final proof, verifier, cleanup and atomic-publication evidence without
      changing the admitted bytes, and prepare the exact read-only handoff for a
      different-lane W2 reviewer.
    commitment: BC-124
    bead: think-3i67
    status: completed
    entered_by: planned_checkpoint
    switch_reason: The complete normal and optimized mutation matrix passed.
    budget_minutes: 25
    started_at: '2026-09-02T01:22:36Z'
    deadline_at: '2026-09-02T01:47:36Z'
    expected_output: >-
      Final immutable instrument hashes, an explicit producer/verifier import boundary,
      publication and cleanup receipts, and a canonical-result absence guard.
    validation_command: >-
      uv run --frozen ruff check cases/unitsquare_precision/production
      tests/test_unitsquare_precision_production.py && uv run --frozen basedpyright
      cases/unitsquare_precision/production tests/test_unitsquare_precision_production.py
    kill_condition: >-
      Stop if an instrument byte changes, the verifier imports the production generator,
      a cleanup or publication guard is not reproducible, the result appears or an
      external source is accessed.
    fallback: Preserve the first exact handoff defect and stop before W2.
    outcome: >-
      Artifact: final author-side SHA-256 values are adapter.py
      525c485c7d023d3dcb308c19f11d0c2dfacae8b55148f1522a914ff9ad739183,
      run.py ededfb794b01d452083b5866734cebec31d9850562604e3c9c3942782de9d5dd,
      verify.py e39a6a725e7af01a2e1796e1a218576f76b8a2ec2cecf7fbde3f38aeb9630a7a
      and test_unitsquare_precision_production.py
      a8ef4fe33a95665352d7950f8eea87bbb01633065a9478913fa78a06a9a4f3c8.
      Result: the producer and verifier have no assertion nodes; verify.py imports only
      the frozen refusal contract and independent proof verifier, not the production
      parser or generator. The focused suite reproduced verification-before-publication,
      existing-result no-overwrite, interrupted-link cleanup, response cleanup and buffer
      zeroing before the 01:40Z shared quiet window. Guard: no instrument byte changed
      after the mutation receipt, no CPU-heavy check ran after 01:40Z, the canonical
      result remains absent and H-058 remains unchanged. Next: a different-lane reviewer
      must reproduce the target-blind contract before any readiness transition.
    evidence:
    - packing/cases/unitsquare_precision/production/adapter.py
    - packing/cases/unitsquare_precision/production/run.py
    - packing/cases/unitsquare_precision/production/verify.py
    - packing/tests/test_unitsquare_precision_production.py
    stop_reason: Final proof, verifier, cleanup and publication evidence is frozen for W2.
    next_action: Await cross-lane W2 without changing the instrument or H-058.
  - workflow: factual-review
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Have a different-lane reviewer reproduce the frozen target-blind adapter, literal
      receipt, mutation matrix, import boundary and record contracts without target or
      network access.
    commitment: BC-124
    bead: think-3i67
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: Author-side W7 closed with immutable hashes and no readiness transition.
    budget_minutes: 15
    started_at: '2026-09-02T01:47:36Z'
    deadline_at: '2026-09-02T02:02:36Z'
    expected_output: An independent pass or the first exact target-blind admission defect.
    validation_command: >-
      uv run --frozen pytest -q tests/test_unitsquare_precision_production.py && uv run
      --frozen ruff check cases/unitsquare_precision/production
      tests/test_unitsquare_precision_production.py && uv run --frozen basedpyright
      cases/unitsquare_precision/production tests/test_unitsquare_precision_production.py
    kill_condition: >-
      Stop on hash drift, a failed guard, a loaded production generator in the verifier
      probe, result creation or external-source access.
    fallback: Preserve the reviewer discrepancy and leave H-058 instrument-unready.
    outcome: >-
      Artifact: the different-lane reviewer matched all four author-side hashes. Result:
      34 focused tests passed, Ruff was clean, BasedPyright reported zero findings, the
      normal and optimized literal selftests exited zero with byte-identical 1,112-byte
      receipts at SHA-256
      becb4c7f865f2f4b3a9d6bd22b11bb736efe73ba2d7dc97e025cd4becbd55906,
      and all 20 registered mutations fired. Import probing loaded production.verify and
      the frozen refusal.run and refusal.verify modules, but neither production.adapter
      nor production.run. Guard: the canonical result remained absent; no target,
      network, source or geometry surface opened. Whole-result shape, binding and
      publication checks are separate, but proof replay shares frozen refusal.verify
      SHA-256 1533210f9d8e17cbdfa822da59187d280fc4ab063816644825c50d7b8b24552f
      with the producer path. The production side remains unbound and therefore yields
      three typed `serialization-refusal` outcomes. Next: admit instrument readiness only
      and retain H-058 as scientifically unmeasured.
    evidence:
    - packing/cases/unitsquare_precision/production/adapter.py
    - packing/cases/unitsquare_precision/production/run.py
    - packing/cases/unitsquare_precision/production/verify.py
    - packing/tests/test_unitsquare_precision_production.py
    stop_reason: Independent W2 passed with two bounded caveats and no scientific sample.
    next_action: Apply only the authorized readiness and terminal record transitions.
  - workflow: insight-iteration
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Retain the independently admitted target-blind instrument, both bounded caveats and
      the unchanged scientific boundary in H-058, exp-054 and session-074.
    commitment: BC-124
    bead: think-3i67
    status: completed
    entered_by: planned_checkpoint
    switch_reason: Independent W2 passed and the coordinator authorized readiness-only closeout.
    budget_minutes: 15
    started_at: '2026-09-02T01:54:03Z'
    deadline_at: '2026-09-02T02:09:03Z'
    expected_output: >-
      H-058 instrument readiness, an unresolved review-pending exp-054 admission record
      and a completed session with no target result.
    validation_command: >-
      uv run --frozen softschema validate
      campaign/hypotheses/H-058-n68-one-parent-production-serialization.md && uv run
      --frozen softschema validate
      campaign/series/series-000-smoke-and-calibration/experiments/exp-054-h-058-n68-one-parent-production-serialization.md
      && uv run --frozen softschema validate
      campaign/agent-sessions/session-074-bc124-n68-production-adapter.md
    kill_condition: >-
      Stop if closeout changes H-058's claim, criterion, threshold, regime or target,
      creates a result, drops either caveat or promotes instrument evidence to a sample.
    fallback: Leave the records review-pending and retain the first schema or boundary defect.
    outcome: >-
      Artifact: H-058, exp-054 and session-074 retain the independent W2 hashes, checks
      and both bounded caveats. Result: H-058 is instrument-ready for a separately
      preregistered BC-130 target phase; exp-054 is unresolved and `needs_review: true`
      because it admitted only the target-blind instrument. Guard: H-058's claim,
      criterion, threshold, regime and target are unchanged. No result exists, no source
      opened and no H-058 sample or disposition occurred. Next: BC-130 must preserve the
      three-refusal side-semantics boundary unless a separate preregistration binds exact
      or directional semantics.
    evidence:
    - packing/campaign/hypotheses/H-058-n68-one-parent-production-serialization.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-054-h-058-n68-one-parent-production-serialization.md
    - packing/campaign/agent-sessions/session-074-bc124-n68-production-adapter.md
    stop_reason: The authorized readiness-only closeout preserves every scientific boundary.
    next_action: Return terminal hashes to the coordinator for independent campaign review.
  primary_bead: think-3i67
  status: completed
  budget:
    wall_minutes: 150
    max_cycles: 7
    checkpoint_minutes: 25
    slice_minutes: 25
    finalization_minutes: 15
  stop_conditions:
  - The fixed 2026-09-02T02:45:00Z deadline arrives.
  - Any network, parent, child, gain or target geometry surface is opened.
  - The literal command cannot reach its injected adapter boundary by minute 35.
  - A normal/optimized, cleanup, verifier, mutation or atomic-publication guard fails.
  progress:
    metric: complete target-blind production adapters admitted by independent review
    before: zero; exp-051 stops at an absent production CLI seam
    after: >-
      one independently admitted target-blind production adapter; H-058 instrument-ready
      with zero target samples and an intentionally unbound side-semantics refusal
  delegations: []
  outputs:
  - packing/cases/unitsquare_precision/production/adapter.py
  - packing/cases/unitsquare_precision/production/run.py
  - packing/cases/unitsquare_precision/production/verify.py
  - packing/tests/test_unitsquare_precision_production.py
  - packing/campaign/agent-sessions/session-074-bc124-n68-production-adapter.md
  - packing/campaign/hypotheses/H-058-n68-one-parent-production-serialization.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-054-h-058-n68-one-parent-production-serialization.md
  - packing/campaign/resource-usage/codex-task-tree-session-074.yaml
  checks:
  - >-
    The original 34-test author and W2 phases remain historical. Prepublication review
    repaired a selected-path precheck that recursed before enforcing the depth bound;
    fresh different-lane W2 admitted the complete corrected bytes with 35 focused tests.
  - >-
    Current SHA-256 bindings are adapter.py
    9b503050115a5a48b01ec9f4d348b869495fbe4ee4847dc83188b05a3352f539, run.py
    8cef0f9cd4f473e594ed55e650be2fe7b286a798d2a94e5edb0a35efb7b12d54, verify.py
    e39a6a725e7af01a2e1796e1a218576f76b8a2ec2cecf7fbde3f38aeb9630a7a and test
    17f4be0611fb02419d9007222f07b3f585b290c03866403a1d2bd5da954f01df.
  - Ruff and BasedPyright passed on the production package and focused test.
  - >-
    Normal and optimized non-assert literal receipts were byte-identical at SHA-256
    becb4c7f865f2f4b3a9d6bd22b11bb736efe73ba2d7dc97e025cd4becbd55906.
  - All 20 registered mutations fired their named guards.
  - H-058, exp-054 and session-074 pass their enforced soft-schema contracts.
  - The canonical exp-054 result path remained absent.
  resource_rollups:
  - packing/campaign/resource-usage/codex-task-tree-session-074.yaml
  stop_reason: >-
    Fresh prepublication W2 admitted the corrected target-blind adapter; the no-sample
    boundary remains preserved.
  next_action: >-
    Route only to separately preregistered BC-130; preserve the typed side-semantics
    refusal unless a later contract binds exact or directional semantics.
---
# Session-074 — BC-124 `n = 68` Production Adapter

This session is target-blind.
It may use injected synthetic streams and temporary outputs only; the parent URL and
digest are declarations, not access authority.

## Prepublication Correction

The phase-local hashes above record what the original author and reviewer examined.
During the coordinator’s manual diff review, the selected-path marker was found to walk
deep XML recursively before the later bounded visitor ran.
The marker now checks both element count and depth before descent, and the focused suite
includes a document deeper than the Python recursion limit.

A fresh different-lane W2 pass bound the complete corrected four-file set recorded in
the top-level checks.
It passed 35 focused tests, Ruff, BasedPyright, all 20 named mutations and
byte-identical normal and optimized receipts.
The canonical exp-054 result remained absent, so this correction changes instrument
closure only, not H-058’s scientific status.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
