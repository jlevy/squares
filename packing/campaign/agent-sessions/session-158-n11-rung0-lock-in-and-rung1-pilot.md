---
title: "Session 158 — Lock in rung 0, close BC-241, price rung 1"
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-158
  title: Lock In Rung 0, Close BC-241, Price Rung 1
  date: '2026-09-24'
  started_at: '2026-09-24T19:00:00Z'
  deadline_at: '2026-09-25T15:00:00Z'
  branch: claude/n11-rung0-lock-in-and-rung1-pilot
  primary_bead: think-svmp
  status: completed
  ended_at: '2026-09-24T23:54:00Z'
  goal: >-
    Lock in rung 0 of the n11 settlement ladder with a Fable max review, an off-repo
    archive of its certificate tree and a register decision rated by epistemics.md;
    close BC-241 so results ending in Trump-degenerate leaves lose their qualifier; and
    price rung 1 (H-112) with a parameterized-box pilot of the rung-0 instrument, run
    overnight on CPU. Stacked on PR 233.
  workflow_phases:
  - workflow: factual-review
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      BC-381 and BC-382: review the closed rung-0 tree and the BC-241 obligations, and
      admit the parameterized box preset for BC-383, while the tree is archived.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 360
    started_at: '2026-09-24T19:00:00Z'
    deadline_at: '2026-09-25T01:00:00Z'
    expected_output: >-
      Two dated reviews, an archived tree with a checksum manifest, an admitted preset
      and a register decision for H-236.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: A review rejects the closed tree or finds the preset changes h236.
    fallback: Record the rejection or the defect and stop the dependent step.
    outcome: >-
      BC-381 accepted the closed rung-0 tree and registered T-035 (reduction, V4/C5/S3)
      and T-036 (Trump optimal at its own angle, V3/C2/S3); BC-382 closed BC-241 by a
      full radius replay and a method-distinct control; BC-383's pilot (exp-234) found no
      box closing at 150,000 nodes per subtree, with about two-thirds of every box closed
      regardless of width or tilt, so a stronger per-node bound is H-112's prerequisite.
    evidence:
    - docs/project/reviews/review-2026-09-24-rung0-closed-tree.md
    - docs/project/reviews/review-2026-09-24-bc241-closure.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-234-h242-rung1-pilot.md
    stop_reason: All three commitments reached their exits.
    next_action: Close the session with certification pending on one hosted gate.
  budget:
    wall_minutes: 1200
    slice_minutes: 240
    finalization_minutes: 90
  stop_conditions:
  - The owner ends the run; a self-declared budget is not a stop condition (OR-8).
  - No register entry without the Fable max review and an epistemics.md derivation.
  - The h236 path of the instrument must stay byte-identical.
  progress:
    metric: Rung 0 locked in, BC-241 disposition, rung-1 pilot verdicts.
    before: >-
      Rung 0 closed and H-236 confirmed at its scope pending BC-241 (exp-232); rung 1
      unpriced; the certificate tree only in a worktree attic.
    after: >-
      Rung 0 is registered as T-035 and T-036; BC-241 is closed; rung 1 is priced out
      with the present relaxation (exp-234), and BC-384 designs its prerequisite.
  resource_rollups:
  - packing/campaign/resource-usage/e8d698c4-206a-4921-bcc4-4f7e12fa474f.yaml
  - packing/campaign/resource-usage/agent-ab689e6e38eba4fc1.yaml
  - packing/campaign/resource-usage/agent-a68e3e4eecaf16386.yaml
  - packing/campaign/resource-usage/agent-ab7b154b8a93c1b73.yaml
  - packing/campaign/resource-usage/agent-af2ba803dd233242c.yaml
  - packing/campaign/resource-usage/agent-a3cc5d0580f6e2dce.yaml
  delegations: []
  outputs:
  - docs/project/reviews/review-2026-09-24-rung0-closed-tree.md
  - docs/project/reviews/review-2026-09-24-bc241-closure.md
  - packing/frontier/results.yaml
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-234-h242-rung1-pilot.md
  checks:
  - 'full gate: full at a42b0de8eef4acc8e6ea8f83c25ca3c7688094c1: passed (hosted run 36075268969; validate, exhaustive, slow-lane, screen and macOS portability all passed)'
  - check_results passes all 36 registered results.
  - The BC-241 checker accepts at the closed head after the packet's pinned bytes were restored.
  - The release data pin test passes after the re-pin.
  - packing-validate --records passed on the closed records.
  stop_reason: >-
    All three commitments reached their exits, and hosted full run 36075268969 certified
    the closed head.
  next_action: >-
    BC-384 (think-ggk5): design and measure a stronger per-node bound for the fixed-angle
    cell tree.
---
# Lock In Rung 0, Close BC-241, Price Rung 1

The owner selected the three next steps after rung 0 closed: secure what it proved,
remove the BC-241 qualifier its terminal leaves carry, and measure what rung 1 would
cost before building anything new for it.
Three lanes run in parallel, the pilot runs overnight on CPU, and the session is stacked
on PR 233.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
