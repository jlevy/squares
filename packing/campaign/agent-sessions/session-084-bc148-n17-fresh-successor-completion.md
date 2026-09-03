---
title: session-084 — BC-148 n = 17 fresh successor completion
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-084
  title: BC-148 n = 17 fresh successor completion
  date: '2026-09-03'
  started_at: '2026-09-03T06:51:00Z'
  deadline_at: '2026-09-03T16:48:00Z'
  branch: claude/squares-pr76-overnight-run-tpc888
  goal: >-
    Execute BC-148: build a fresh H-052 successor package that repairs the result
    boundary exp-056's child assembler cannot decide, give it two explicit terminal
    schemas whose decision is derived rather than asserted, prove every named refusal,
    and then compute the remaining eleven direction cells inside one process-exclusive
    lease — without editing exp-052, exp-056 or either frozen package.
  workflow_phases:
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Build the fresh completion package and result assembler in a fresh path, bind
      exp-056 as the immediate parent checkpoint and exp-052 as the carried-chain genesis
      so neither can substitute for the other, give the assembler its two terminal
      schemas with the decision derived from the emitted evidence, and prove every named
      refusal on synthetic directions only.
    commitment: BC-148
    bead: think-5j8d
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 80
    started_at: '2026-09-03T06:51:00Z'
    deadline_at: '2026-09-03T08:11:00Z'
    expected_output: >-
      A readiness report naming what was built, what each schema requires, which refusal
      tests pass, the exact writer command and a measured runtime estimate.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q
      tests/test_n17_weighted_certificate_successor.py
    kill_condition: >-
      An edit to a frozen package or an exp-052 or exp-056 artifact, a swapped ancestry
      binding that verifies, or a refusal test that fails to refuse.
    fallback: >-
      Report NOT-READY with the exact guard that could not be established, and run no
      writer.
    outcome: >-
      Artifact: cases/n17_weighted_certificate_successor/ and
      tests/test_n17_weighted_certificate_successor.py, with the readiness report at
      scratchpad/bc148/h052-successor-readiness.md -- a container-local directory, not
      retained in the repository. Result: 115 named self-test guards
      pass with zero skips and byte-identical normal and optimized receipts, 17 focused
      controls pass, and both terminal schemas derive all six decision-bearing fields
      rather than asserting them. Two pre-writer confirmations ran against the real
      retained data: recomputing ordinal 169 reproduced row hash 8947b38e exactly, and
      rebuilding the chain from the two certificate summaries alone reproduced all 170
      retained row hashes. Guard: no exp-052 or exp-056 record, result, checkpoint or
      progress path was written, the frozen package manifest still computes to 309ec241,
      the exp-056 driver was never invoked, and no target direction was evaluated. Two
      allocation errors were caught by checking rather than assuming — session-083 is
      the coordinator's own session, and exp-058 was claimed by the concurrent n = 5 lane
      mid-build — so the round is registered as exp-059 in session-084. Next: hold
      readiness until the coordinator authorizes the writer at 08:58Z.
    evidence:
    - 'selftest: 115 guards, passed true, skipped 0, receipt 0109332a, normal and optimized byte-identical'
    - 'pytest: 39 passed across the successor, child and base n17 suites'
    - 'ruff check, ruff format --check and basedpyright all clean on the new files'
    - 'calibration: ordinal 169 recomputed to 8947b38e in 182.6 s; remaining 11 directions are 10.988x its cell count'
    - 'chain rebuilt from the two summaries alone reproduces all 170 retained row hashes'
    stop_reason: >-
      The design, build and refusal-test budget closed with the package frozen, every
      gate green and the writer deliberately not started.
    next_action: >-
      Register exp-059 and session-084, then run the exact writer inside the
      08:58Z--09:58Z process-exclusive lease on the coordinator's authorization.
  - workflow: research-loop
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Register the round and this session, stand by without running any process until the
      lease opens, then run one quiet exact writer from ordinal 170 through 180 and
      assemble either complete agreement from a complete verified chain or a typed
      disagreement from the verified prefix through its exact discrepant pair.
    commitment: BC-148
    bead: think-5j8d
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      The build phase closed on its readiness verdict; what remains is registration, a
      standby interval the lane must not fill with processes, and the measurement itself,
      which is governed by a repository-wide process-exclusive lease rather than by this
      lane's own budget.
    budget_minutes: 141
    started_at: '2026-09-03T07:45:00Z'
    deadline_at: '2026-09-03T10:06:00Z'
    expected_output: >-
      A canonical exp-059 result carrying the complete H-052 envelope for all 181 exact
      pairs, or the first exact disagreement with its declared suffix absences, or a
      frozen checkpoint with an explicit canonical-result absence.
    validation_command: >-
      ./.venv/bin/python3 -m cases.n17_weighted_certificate_successor.run --status
      campaign/series/series-000-smoke-and-calibration/results/exp-059-h-052-n17-fresh-successor-completion.checkpoint.json
    kill_condition: >-
      A frozen-input, ancestry or chain-link verification failure, the first exact
      disagreement, or the 09:58:00Z lease boundary.
    fallback: >-
      Freeze the checkpoint, progress marker, receipt and typed stop reason with an
      explicit canonical-result absence; a time-limited agreeing prefix is process
      evidence and is not a negative result.
    outcome: >-
      Reached complete agreement on all 181 exact direction cells. The writer replayed
      the retained 170-row prefix, recomputed the interrupted ordinal 170 rather than
      promoting it, and completed ordinals 170 through 180 inside the process-exclusive
      lease, releasing it twenty-one minutes early. BC-149's independent review returned
      an exact pass, at the scope of implementation agreement only.
    evidence:
    - >-
      writer ran 08:59:33Z to 09:32:44Z, 1991 s against a 3600 s lease and a 2100 s
      estimate, exit 0
    - >-
      terminal schema complete-agreement, decision accepted, instrument_valid true, 181
      rows, first_disagreement_ordinal null
    - >-
      result 438dfc1f, checkpoint bb45ed2a, last row hash 60e58a70, carried boundary
      8947b38e at ordinal 169
    - >-
      both 181-row summaries byte-identical, every row minimum 1/1, global minimum 1/1,
      total weight 203/12, atom count 168
    - >-
      published bytes re-validated in a separate process: canonical, and validate_result
      rebuilt all 181 chain links from the two summaries alone
    - >-
      four frozen ancestor digests unchanged, frozen package 309ec241 intact, exp-052 and
      exp-056 never acquired a result file
    stop_reason: >-
      The registered criterion decided: all 181 exact pairs agree and the terminal schema
      is complete-agreement.
    next_action: >-
      Hand BC-149 a terminal outcome with every input, output, command, decision,
      declared absence and mutation bound at one revision, including the named
      --assemble instrument limitation.
  - workflow: documentation-pass
    focus: process
    recording: contemporaneous
    clock_role: work
    objective: >-
      Support the Agenda 016 closeout from a terminal lane: answer replay questions
      against the frozen exp-059 artifacts, carry the successor's named instrument
      limitations into the closeout record, and run no further target work.
    status: in_progress
    entered_by: evidence_checkpoint
    switch_reason: >-
      The n = 17 target is terminal and independently reviewed, so the lane's
      remaining obligation is closeout support rather than measurement.
    budget_minutes: 417
    started_at: '2026-09-03T09:36:00Z'
    deadline_at: '2026-09-03T16:33:00Z'
    expected_output: >-
      Closeout answers bound to the frozen artifacts, and the instrument
      limitations carried into the agenda's outcome rows.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      Any new target computation, or any edit to the frozen exp-059 artifacts.
    fallback: >-
      Report the limitation unanswered rather than recomputing it.
    outcome: null
    evidence: []
    stop_reason: null
    next_action: >-
      Hand the lane's limitations and receipts to BC-155 and close the session with
      its resource rollup.
  primary_bead: think-5j8d
  status: in_progress
  budget:
    wall_minutes: 597
    finalization_minutes: 15
  stop_conditions:
  - A frozen input, ancestry hash, package manifest or chain link that fails verification.
  - A refusal test that fails to refuse, or a swapped ancestry binding that verifies.
  - The first exact disagreement between the two accumulators.
  - Any write that would reach an exp-052 or exp-056 artifact or a frozen package.
  - The 09:58:00Z process-exclusive lease boundary, whatever the row count.
  progress:
    metric: >-
      Exactly agreeing n = 17 direction cells in a chain whose assembler can decide H-052
    before: >-
      170 of 181 in exp-056, in a chain whose assembler omits both certificate summaries,
      the global minima, the preconditions, the mutation map and instrument_valid
    after: null
  delegations: []
  outputs:
  - packing/cases/n17_weighted_certificate_successor/run.py
  - packing/cases/n17_weighted_certificate_successor/__init__.py
  - packing/tests/test_n17_weighted_certificate_successor.py
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-059-h-052-n17-fresh-successor-completion.md
  - packing/campaign/agent-sessions/session-084-bc148-n17-fresh-successor-completion.md
  checks:
  - 'selftest: 115 named guards, passed true, skipped 0, receipt hash 0109332a'
  - 'selftest receipts byte-identical under normal and optimized Python: 875722ce'
  - 'pytest: 39 passed across the successor, child and base n17 suites'
  - 'ruff check, ruff format --check and basedpyright clean on both new files'
  - 'ancestry verification against the real artifacts with 0 target directions evaluated'
  - 'exp-052 and exp-056 checkpoint and progress digests unchanged: db5c1569, 08e301b0, 0d39a7e7, 0875f31f'
  stop_reason: null
  next_action: >-
    Stand by without running any process until 08:58:00Z, then run the registered writer
    on the coordinator's authorization and assemble whichever terminal schema applies.
---
# Session-084 — BC-148 `n = 17` Fresh Successor Completion

Agenda 016 block BC-148, hypothesis H-052, lane `agenda016-lane-n17`.

Exp-056 left H-052 at 170 of 181 exactly agreeing direction cells.
The remaining arithmetic is short, but its child assembler cannot decide the hypothesis,
so this session repairs the result boundary in a fresh successor before computing
anything.

## What the Fresh Successor Adds

The exp-056 child result carries the chain and nothing else.
The exp-059 successor result carries, in both of its terminal schemas, the evidence
H-052’s criterion actually names: both 181-row `CertificateManifest` summaries with
their atom and direction hashes, total weight, every row minimum and the global minimum;
the shrink-and-scaling preconditions; all five frozen mutation results;
`all_mutations_rejected`; and `instrument_valid` — with the decision derived from those
fields rather than asserted beside them.

It also separates two things exp-056 conflated into a single parent block: exp-056 is
the **immediate parent checkpoint** this round resumes from, and exp-052 is the
**carried-chain genesis** that row 0 is anchored to.
Both are verified, they are cross-checked against each other, and neither can be
substituted for the other.

## Process Notes

Three deviations are worth recording rather than smoothing over.

**No sub-agents were run.** OR-2 asks for three to five.
This lane’s work was a single serial build against one frozen boundary, inside a window
that ends in a repository-wide process-exclusive lease; a fan-out would have contended
for the very CPU the calibration was measuring, and the runtime estimate is evidence
here. The lane agent was itself the delegated sub-agent under the coordinator’s BC-148
delegation.

**Two identifier collisions were caught, not avoided.** `session-083` turned out to be
the coordinator’s own session rather than a free lane id, and `exp-058` was claimed by
the concurrent `n = 5` lane while this package was being built.
Both were found by checking the working tree and the gate output rather than by trusting
the highest id seen at the start of the session.
The round is exp-059 in session-084.

**The package sits in `packing/cases/`, not `packing/src/sqpack/`.** The lane’s declared
write scope named the latter.
A library module under `src/sqpack/` importing `cases.*` would invert the layering, and
the successor’s three siblings all live in `cases/`. The coordinator confirmed the
placement.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
