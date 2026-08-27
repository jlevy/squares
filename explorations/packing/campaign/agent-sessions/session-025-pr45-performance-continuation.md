---
title: session-025 — PR 45 performance continuation
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-025
  title: Stack the fast lane and shorten the known-best atlas check
  date: '2026-08-26'
  started_at: '2026-08-26T17:33:27-07:00'
  deadline_at: '2026-08-26T23:02:52-07:00'
  goal: >-
    Integrate PR 41's landed validation infrastructure into PR 45, reduce the measured
    known-best atlas bottleneck without changing retained evidence or claim boundaries,
    then resume the ordered PR 45 review dispositions and merge-readiness gates.
  workflow_phases:
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: efficiency
    objective: >-
      Stack PR 41's landed validation infrastructure onto PR 45 and replace repeated
      partition candidate-list scans with an equivalent candidate-index bitset traversal.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 30
    started_at: '2026-08-26T17:33:27-07:00'
    deadline_at: '2026-08-26T18:03:27-07:00'
    expected_output: >-
      A clean PR 45 merge of exact main, collision-free durable session records, a small
      partition bitset patch, and byte-identical census plus focused regression receipts.
    validation_command: >-
      uv run --directory explorations/packing --frozen python -m
      devtools.census_known_best_chunks --check && uv run --directory
      explorations/packing --frozen pytest -q tests/test_chunk_components.py
      tests/test_known_best_chunk_evidence.py tests/test_known_best_atlas.py
      tests/test_validation_cli.py
    kill_condition: >-
      Stop on any changed retained byte, candidate count, search-state count, cap
      boundary, selected certificate, exact/near status, or scientific claim boundary.
    fallback: >-
      Keep the exact-main merge and the read-only profile, omit the optimization, and
      record the first differing retained field under think-4vni.
    outcome: >-
      Merged the exact landed PR 41 tree locally, reconciled all durable session IDs and
      additive documentation conflicts, and replaced repeated partition candidate-list
      scans with an order-preserving candidate-index bitset traversal.
    evidence:
    - Ten chunk-component regressions passed in 1.05 seconds.
    - Forty-four known-best atlas and validator regressions passed in 10.98 seconds.
    - The byte-for-byte 100-record census check passed in 97.30 seconds.
    - >-
      The isolated five-command atlas validator step passed in 173.48 seconds, down from
      743.07 seconds: a 4.28-fold speedup and 76.7 percent wall-time reduction.
    stop_reason: The bounded patch met every retained-output invariant before the slice deadline.
    next_action: >-
      Independently review bitset equivalence and spend one bounded follow-up slice on
      the measured 56.45-second pricing step and safe process-local lattice memoization.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: efficiency
    objective: >-
      Independently review the bitset patch and remove the next largest repeated pure
      computations only when exact output, memory bounds, and hash policy remain unchanged.
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      The first optimization passed equivalence and reduced the atlas step by 76.7
      percent, while pricing still consumes 56.45 seconds and the user authorized one
      more performance cycle before resuming review work.
    budget_minutes: 30
    started_at: '2026-08-26T17:45:29-07:00'
    deadline_at: '2026-08-26T18:15:29-07:00'
    expected_output: >-
      An independent correctness disposition for the bitset patch and either one second
      byte-preserving optimization with measured benefit or a typed stop at the next bottleneck.
    validation_command: >-
      uv run --directory explorations/packing --frozen python -m
      devtools.census_known_best_chunks --check && uv run --directory
      explorations/packing --frozen packing-validate --only 'known-best n=1..100 atlas'
    kill_condition: >-
      Stop on an equivalence concern, persisted-cache proposal, unbounded memory growth,
      changed retained byte, or less than 10 percent measured gain from a second patch.
    fallback: >-
      Keep only the validated bitset change, record pricing as the next bottleneck, and
      resume think-oo1p without another full performance cycle.
    outcome: >-
      Independently accepted the bitset solver, added its exact off-frame/state-cap
      regression, and replaced pricing's 2.905-million-object complete-orbit path with a
      normalized-edge comparison that retains the legacy path for every partial or richer orbit.
    evidence:
    - The old and bitset solvers matched on 39,348 randomized solution/state/cap cases.
    - >-
      Five hundred uniform wall-free canonicalizations matched the legacy full-orbit
      label, scaffold, witness, raw-image count, and unique-image count exactly.
    - Pricing retained-byte validation passed in 8.20 seconds, down from 56.45 seconds.
    - >-
      The isolated atlas step passed in 123.93 seconds, down from 743.07 seconds: a
      6.00-fold speedup and 83.3 percent wall-time reduction.
    - >-
      A raw module-global lattice cache was rejected as unbounded; the bounded variant's
      projected 10.2 percent gain was not stacked after the larger pricing result.
    stop_reason: The second patch exceeded its benefit threshold and passed independent equivalence controls.
    next_action: >-
      Commit the two performance patches, re-audit the implemented PR 45 review
      dispositions, and run the complete strict validator with PR 41's worker settings.
  - workflow: process-review
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Package the independently reviewed performance changes, prove the five PR 45
      review corrections remain implemented on merged main, and obtain one complete strict receipt.
    status: in_progress
    entered_by: evidence_checkpoint
    switch_reason: >-
      Two bounded performance slices reduced the dominant atlas step by 83.3 percent;
      correctness disposition and complete validation are now the critical path.
    budget_minutes: 30
    started_at: '2026-08-26T17:58:00-07:00'
    deadline_at: '2026-08-26T18:28:00-07:00'
    expected_output: >-
      A clean performance commit, green focused contracts for think-oo1p, think-givb,
      think-4axm, think-9jny, and think-rov3, and one complete strict receipt.
    validation_command: >-
      uv run --directory explorations/packing --frozen packing-validate --strict --jobs
      2 --inner-jobs 2 --timeout-seconds 1200
    kill_condition: >-
      Stop on retained-output drift, a reopened review finding, a scientific claim
      expansion, or one strict step that exhausts its 1,200-second cap.
    fallback: >-
      Preserve the performance commit and focused receipts, isolate the first strict
      failure once, and leave all review beads open with its typed blocker.
    outcome: null
    evidence: []
    stop_reason: null
    next_action: >-
      Finalize the performance commit, run the review-focused contract set, then start
      one complete strict validation with two outer and two inner workers.
  primary_bead: think-eyix
  status: in_progress
  budget:
    wall_minutes: 330
    max_cycles: 9
    orientation_minutes: 8
    checkpoint_minutes: 20
    slice_minutes: 30
    finalization_minutes: 30
  stop_conditions:
  - The user-extended absolute deadline 2026-08-26T23:02:52-07:00 is reached.
  - The last 30 minutes are reserved for terminal reconciliation and handoff.
  - No optimization may change partition certificates, caps, source policy, or scientific claim boundaries.
  - No fast-path result may substitute for a complete strict or cross-platform integration receipt.
  - Three consecutive failures at one boundary stop that line with a typed blocker.
  progress:
    metric: PR 45 known-best atlas and complete strict wall seconds with identical retained evidence
    before: >-
      PR 45's first complete strict receipt used 1,589.65 seconds. The known-best atlas
      step alone used 743.07 seconds, including repeated Python candidate-list scans over
      1,823,004 retained partition-search states.
    after: null
  delegations:
  - task: Identify a sound optimization for the PR 45 atlas census.
    operator: atlas_perf
    status: completed
    recording: retrospective
    outcome: >-
      Located the dominant repeated candidate-list scans in partition MRV selection and
      prototyped an equivalent candidate-index bitset traversal.
    evidence:
    - The n=100 prototype improved from 17.46 seconds to 1.515 seconds.
    - >-
      A 71.244-second full prototype rebuild matched all 200 retained partition entries,
      including candidates, search states, selected chunks, caps, and statuses.
    files: []
    checks: []
    uncertainty: The stacked PR 41 tree still requires an independent census and strict atlas receipt.
    elapsed_seconds: 1108
    elapsed_quality: operator_reported_approximate
    next_action: Coordinator implements the bounded traversal and runs independent equivalence checks.
    phase: 1
  - task: Independently review the candidate-index bitset traversal.
    operator: bitset_review
    status: completed
    recording: contemporaneous
    outcome: >-
      Found no production-path issue and confirmed identical candidate eligibility, MRV
      ties, traversal order, cache states, residual ordering, off-frame handling, and caps.
    evidence:
    - Thirty-nine thousand three hundred forty-eight randomized cases matched the old solver exactly.
    - Ten preexisting chunk-component regressions passed in 1.00 seconds.
    files: []
    checks: []
    uncertainty: Private malformed masks outside square_count remain unsupported; production mask construction excludes them.
    elapsed_seconds: null
    elapsed_quality: unavailable
    budget_minutes: 20
    started_at: '2026-08-26T17:44:54-07:00'
    deadline_at: '2026-08-26T18:04:54-07:00'
    expected_output: A semantic-equivalence review and the smallest missing regression, if any.
    validation_command: git diff -- explorations/packing/src/sqpack/chunks.py
    kill_condition: Stop on any changed candidate eligibility, MRV tie, traversal order, state, or cap.
    fallback: Return the first divergent state and omit approval.
    write_scope:
    - none (read-only audit)
    excluded_commands:
    - git commit
    - git push
    - tbd
    - gh
    next_action: Coordinator retains the patch and adds the recommended direct state-cap regression.
    phase: 2
  - task: Profile the retained contact-enumeration pricing check.
    operator: pricing_perf
    status: completed
    recording: contemporaneous
    outcome: >-
      Isolated 2.905 million materialized symmetry images in legacy n=4
      canonicalization and prototyped an exact normalized-edge complete-orbit fast path.
    evidence:
    - The retained pricing document remained byte-identical.
    - Prototype expected_document time fell from 56.45 seconds to 7.676 seconds.
    files: []
    checks: []
    uncertainty: The optimization is intentionally unavailable to capped, mixed-color, or wall-bearing orbits.
    elapsed_seconds: null
    elapsed_quality: unavailable
    budget_minutes: 25
    started_at: '2026-08-26T17:44:58-07:00'
    deadline_at: '2026-08-26T18:09:58-07:00'
    expected_output: A measured exact-output optimization or typed next bottleneck for the 56.45-second check.
    validation_command: uv run --directory explorations/packing --frozen python -m devtools.price_contact_enumeration --check
    kill_condition: Stop on a changed pricing model, retained output, source scope, or calibration boundary.
    fallback: Return the hottest pure call path without recommending an unmeasured patch.
    write_scope:
    - none (read-only audit)
    excluded_commands:
    - git commit
    - git push
    - tbd
    - gh
    next_action: Coordinator implements the fast path with a legacy-orbit differential and cap fallback test.
    phase: 2
  - task: Audit process-local memoization of lattice deltas.
    operator: lattice_cache
    status: completed
    recording: contemporaneous
    outcome: >-
      Rejected raw unbounded module caching and measured a safe 65,536-entry bounded
      alternative without retained-output or hash-policy changes.
    evidence:
    - The bounded variant reduced the full census sequence from 96.524 to 78.898 seconds.
    - It retained about 22 MiB beyond normal allocator retention on this host.
    files: []
    checks: []
    uncertainty: The projected whole-atlas gain is only about 10.2 percent and was not replayed after the pricing patch.
    elapsed_seconds: null
    elapsed_quality: unavailable
    budget_minutes: 20
    started_at: '2026-08-26T17:45:03-07:00'
    deadline_at: '2026-08-26T18:05:03-07:00'
    expected_output: A cache-lifetime, memory, hash-policy, equivalence, and timing disposition.
    validation_command: rg -n "_lattice_delta" explorations/packing/src/sqpack/chunks.py
    kill_condition: Stop on persisted cache state, unhashable inputs, output drift, or unbounded retained memory.
    fallback: Reject memoization and report the measured duplicate-call ratio only.
    write_scope:
    - none (read-only audit)
    excluded_commands:
    - git commit
    - git push
    - tbd
    - gh
    next_action: Do not stack this marginal cache in the current performance cycle.
    phase: 2
  outputs:
  - campaign/agent-sessions/session-025-pr45-performance-continuation.md
  - src/sqpack/chunks.py
  - tests/test_chunk_components.py
  checks:
  - PR 41 merged as exact main revision 45238b0cd339e7862c6f1209dcd405a8918775fb.
  - The landed main workflow passed Linux in 7 minutes 1 second and macOS in 6 minutes 25 seconds.
  - The byte-for-byte census check passes in 97.30 seconds.
  - The isolated known-best atlas step passes in 173.48 seconds, down from 743.07 seconds.
  - Pricing retained-byte validation passes in 8.20 seconds, down from 56.45 seconds.
  - The final isolated atlas step passes in 123.93 seconds, down from 743.07 seconds.
  stop_reason: null
  next_action: >-
    Under BC-019, think-eyix, and think-4vni, commit the independently reviewed
    performance patches, confirm think-oo1p, think-givb, think-4axm, think-9jny, and
    think-rov3 on the merged tree, then run one complete strict receipt.
---
# Session 025 — PR 45 Performance Continuation

This continuation begins at the clean boundary where PR 41 landed and passed complete
Linux and macOS integration.
It preserves PR 45’s calibration-only use of the source-complete corpus and makes no new
geometry, feasibility, or optimality claim.

The first slice changes only how the existing partition search represents eligible
candidates in memory.
Retained candidate order, MRV ties, cache keys, state counts, caps, certificates, and
exact/near classifications remain acceptance invariants.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
