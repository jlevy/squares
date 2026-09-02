---
title: session-080 — BC-138 n = 68 side-semantics binding
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-080
  title: BC-138 n = 68 side-semantics binding
  date: '2026-09-02'
  started_at: '2026-09-02T05:03:00Z'
  deadline_at: '2026-09-02T06:43:00Z'
  branch: claude/squares-pr-73-resume-5lp3bz
  goal: >-
    Preregister the exp-057 side semantics before any network access, then bind them in
    code by composing the frozen exp-054 adapter, runner and verifier without editing one
    of their bytes, so the three declared models can return a geometry outcome instead of
    three typed serialization refusals.
  workflow_phases:
  - workflow: insight-iteration
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Preregister exp-057 with the per-model side binding, the one-quarter directional
      rule, the declared parent URL and digest, the result path, the registered command,
      the claim boundary and the stopped-by rules, all before any network access.
    commitment: BC-138
    bead: think-ymjp
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 25
    started_at: '2026-09-02T05:03:00Z'
    deadline_at: '2026-09-02T05:28:00Z'
    expected_output: >-
      A validated enforced exp-057 record whose binding is stated exactly, with the
      exp-054 instrument bytes untouched and the exp-057 result path absent.
    validation_command: >-
      uv run --frozen --all-extras --group dev python -c "from sqpack.campaign.ledger
      import load, ROOT; load(ROOT / 'series', 'experiment',
      '*/experiments/exp-057*.md')"
    kill_condition: >-
      Stop if the side semantics cannot be stated exactly from the adapter code, if any
      threshold would exceed one quarter of the released gain, or if a network, source or
      target channel would be opened to write the record.
    fallback: >-
      Retain the typed binding refusal in exp-057 and stop before touching any module.
    outcome: >-
      Artifact: exp-057 registers the binding at SHA-256
      e2c5a743ca941f4ac6d364b556f6980d6ba87d09f90b4ec0aadf5d55fc0a06e7 — under
      `declared:svg-literal` the reported token `8.80345993651653` is the exact decimal
      rational 880345993651653/100000000000000, already in lowest terms; under `nearest-6`
      it is that value plus or minus half the frozen 1/1000000 quantum; under `truncate-6`
      it is that value plus one whole quantum away from zero, the printed value being the
      lower endpoint. Result: both interval widths are 1/1000000 and both half-widths are
      at most 1/1000000, against a one-quarter ceiling of
      768618004216131/40000000000000000000 ≈ 1.9215450105403275e-5, so every directional
      threshold clears the X-011 rule by more than an order of magnitude; the record also
      binds the parent URL, the digest 558fbddd, the model order, the result path, the
      claim boundary and five stopped-by rules. Guard: the cell opened no network, source
      or target channel, wrote no module and left the exp-054 bytes at their frozen
      hashes. H-058 stays unmeasured and exp-057 carries no result. Next: enter the W7
      cell and express the binding without editing a frozen file.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-057-h-058-n68-one-parent-localization.md
    stop_reason: The target-blind preregistration passed its enforced contract.
    next_action: Bind the semantics in code without editing adapter.py, run.py or verify.py.
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Add the frozen side-semantics module and the bound entry point, composing the
      unchanged adapter, runner and verifier so the scalar the frozen factory accepts is
      derived from the reported token, with no bare assert anywhere.
    commitment: BC-138
    bead: think-ymjp
    status: completed
    entered_by: planned_checkpoint
    switch_reason: The preregistration passed before its fixed boundary.
    budget_minutes: 25
    started_at: '2026-09-02T05:09:00Z'
    deadline_at: '2026-09-02T05:34:00Z'
    expected_output: >-
      A semantics module and a bound entry point whose `--selftest` emits a canonical
      receipt, with the frozen files unmodified.
    validation_command: >-
      uv run --frozen --all-extras --group dev python -m
      cases.unitsquare_precision.production.bound_run --selftest
    kill_condition: >-
      Stop if the binding cannot be expressed without editing adapter.py, run.py,
      verify.py or anything under cases/unitsquare_precision/refusal/, or if the entry
      point would reach a network or target channel.
    fallback: >-
      Retain the typed binding refusal naming the semantic that could not be bound and
      leave every module unwritten.
    outcome: >-
      Artifact: `semantics.py` at SHA-256
      dfdbc57724adbc9cc878afe6ff0b3fb0d2c549ac3eb9bbdf7dba772c82f28932 returns one
      `SideBinding` per declared model with typed refusals for an unbound token, a
      malformed token, an unknown model, a wrong direction, a wrong quantum, a threshold
      wider than a quarter of the gain and a changed released gain; `bound_run.py` at
      SHA-256 5d6303f228748e76e4a85512d41011a6200602216d925cc8e4de2773a4d90331 composes
      the unchanged `production_model_factory` per model with that scalar. Result: the
      binding needed no frozen edit. `production_model_factory` takes a scalar
      `Fraction`, so the interval models admit the printed value, which lies inside each
      declared interval; because every normalized cell is the side times a nonnegative
      container ratio and the sought outcome is the existence of a compatible pose,
      the scalar cells are a subset of the interval cells and a `compatible` outcome
      transfers upward while a refusal transfers to nothing. Guard: adapter.py, run.py,
      verify.py and the exp-054 test still hash to 9b503050…, 8cef0f9c…, e39a6a72… and
      17f4be06…; the bound frozen-parent constructor delegates its URL and digest guard
      to the unchanged `run.production_dependencies` and performs no I/O. Next: fire every
      named mutation and prove the receipts identical under `python -O`.
    evidence:
    - packing/cases/unitsquare_precision/production/semantics.py
    - packing/cases/unitsquare_precision/production/bound_run.py
    stop_reason: The binding was expressed with no frozen file modified.
    next_action: Write the named mutation controls and the normal/optimized receipt control.
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Write the named mutation controls, cross-check the declared directions against the
      adapter's own coordinate rule, and prove byte-identical receipts under normal and
      optimized Python while the exp-054 suite still passes unchanged.
    commitment: BC-138
    bead: think-ymjp
    status: completed
    entered_by: planned_checkpoint
    switch_reason: The two modules reached a green selftest before the cell boundary.
    budget_minutes: 25
    started_at: '2026-09-02T05:12:00Z'
    deadline_at: '2026-09-02T05:37:00Z'
    expected_output: >-
      A focused test module whose named mutations all reject and whose subprocess control
      shows identical normal and optimized receipts.
    validation_command: >-
      uv run --frozen --all-extras --group dev python -m pytest
      tests/test_unitsquare_precision_semantics.py
      tests/test_unitsquare_precision_production.py -q
    kill_condition: >-
      Stop if any named mutation does not fire, if the receipts differ by one byte, if the
      exp-054 suite changes behavior, or if the canonical exp-057 result appears.
    fallback: Retain the first silent mutation and stop before the final cell.
    outcome: >-
      Artifact: `tests/test_unitsquare_precision_semantics.py` at SHA-256
      e8f91e3fb85cb370c617049ef1c7cc23bae04c8f71c83481cc786020afbba3cd carries 27 controls,
      including a public cross-check that the adapter's own retained source cells are
      `["1","1"]`, `["1999999/2000000","2000001/2000000"]` and `["1","1000001/1000000"]`
      for the three models, which is the direction and quantum the binding declares.
      Result: 62 focused tests pass — 27 new and the 35 exp-054 tests unchanged — and all
      thirteen named guards fire in fixed order: `unbound-token`, `malformed-token`,
      `unknown-model`, `wrong-direction`, `wrong-quantum`,
      `threshold-exceeds-quarter-gain`, `changed-released-gain`,
      `scalar-outside-declared-interval`, `unbound-side-refuses-every-model`,
      `bound-side-admits-geometry`, `unfrozen-parent-contract`,
      `frozen-contract-side-is-bound` and `wrong-result-path-before-open`. Guard: normal
      and optimized receipts are byte-identical at SHA-256
      790a973ee5e11e079a3c41dab578311d491eabe5dee76a120ee3a12f5702d76b, the bound synthetic
      run yields three `compatible` outcomes where the unbound one yields three
      `serialization-refusal` outcomes, and the canonical exp-057 result stays absent.
      Next: run the style and type gates, record every hash and close the session at the
      W2 gate.
    evidence:
    - packing/tests/test_unitsquare_precision_semantics.py
    - packing/cases/unitsquare_precision/production/bound_run.py
    stop_reason: Every named mutation fired and both receipts matched byte for byte.
    next_action: Run Ruff and BasedPyright, record hashes and stop at the different-lane gate.
  - workflow: factual-review
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Run the style and type gates on the three new files, record the SHA-256 of every
      created file and of the selftest receipt under both interpreters, validate the
      records, and stop at the W2 different-lane readmission gate.
    commitment: BC-138
    bead: think-ymjp
    status: completed
    entered_by: planned_checkpoint
    switch_reason: The controls and receipts passed before the cell boundary.
    budget_minutes: 25
    started_at: '2026-09-02T05:15:00Z'
    deadline_at: '2026-09-02T05:40:00Z'
    expected_output: >-
      Clean Ruff and BasedPyright runs, a complete hash table, validated exp-057 and
      session-080, and a returned Artifact / Result / Guard / Next.
    validation_command: >-
      uv run --frozen --all-extras --group dev python -m devtools.check_session_clocks
    kill_condition: >-
      Stop if a style or type gate fails, if any frozen hash drifted, or if a record does
      not validate against its enforced contract.
    fallback: Record the failing gate verbatim and hand the lane back unreadmitted.
    outcome: >-
      Artifact: the five files this lane owns are exp-057
      (e2c5a743ca941f4ac6d364b556f6980d6ba87d09f90b4ec0aadf5d55fc0a06e7), semantics.py
      (dfdbc57724adbc9cc878afe6ff0b3fb0d2c549ac3eb9bbdf7dba772c82f28932), bound_run.py
      (5d6303f228748e76e4a85512d41011a6200602216d925cc8e4de2773a4d90331), the focused test
      (e8f91e3fb85cb370c617049ef1c7cc23bae04c8f71c83481cc786020afbba3cd) and this record.
      Result: `ruff format --check` and `ruff check` are clean on all three modules and
      BasedPyright reports 0 errors, 0 warnings, 0 notes; exp-057 and session-080 load
      cleanly through the enforced campaign contracts, and `devtools.validate_schemas`,
      `devtools.check_declared_commands` and
      `devtools.check_session_clocks` pass. Guard: no frozen file was modified — adapter,
      runner, verifier and the exp-054 test hold their registered hashes and nothing under
      `cases/unitsquare_precision/refusal/` was touched; no network, source or target
      access occurred; no Git, tbd or generated-view state changed; the exp-057 result
      path is absent. Next: hand the binding, the thirteen named guards and the receipt
      hash to the coordinator for the different-lane W2 readmission that opens BC-139.
    evidence:
    - packing/campaign/agent-sessions/session-080-bc138-n68-side-semantics-binding.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-057-h-058-n68-one-parent-localization.md
    stop_reason: The lane reached the W2 gate with every author-side control green.
    next_action: >-
      The coordinator runs the different-lane readmission; BC-139 opens only on its
      receipt.
  primary_bead: think-ymjp
  status: completed
  budget:
    wall_minutes: 100
    max_cycles: 4
    checkpoint_minutes: 25
    slice_minutes: 25
    finalization_minutes: 25
  stop_conditions:
  - The fixed 2026-09-02T06:43:00Z deadline arrives.
  - Any network, source or target channel would be opened.
  - The binding cannot be expressed without editing a frozen instrument file.
  - A named mutation does not fire, or the normal and optimized receipts differ.
  - A frozen adapter, runner, verifier or exp-054 test hash drifts.
  progress:
    metric: declared serialization models carrying an admissible n = 68 side binding
    before: >-
      zero; the reported side token is unbound and the production path returns three
      typed serialization refusals
    after: >-
      one defensible literal printed-rational point model and two mechanically consistent
      but source-unsupported six-decimal side models; H-058 still carries zero target
      samples
  delegations: []
  outputs:
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-057-h-058-n68-one-parent-localization.md
  - packing/cases/unitsquare_precision/production/semantics.py
  - packing/cases/unitsquare_precision/production/bound_run.py
  - packing/tests/test_unitsquare_precision_semantics.py
  - packing/campaign/agent-sessions/session-080-bc138-n68-side-semantics-binding.md
  checks:
  - >-
    New SHA-256 bindings are semantics.py
    dfdbc57724adbc9cc878afe6ff0b3fb0d2c549ac3eb9bbdf7dba772c82f28932, bound_run.py
    5d6303f228748e76e4a85512d41011a6200602216d925cc8e4de2773a4d90331, the focused test
    e8f91e3fb85cb370c617049ef1c7cc23bae04c8f71c83481cc786020afbba3cd and exp-057
    e2c5a743ca941f4ac6d364b556f6980d6ba87d09f90b4ec0aadf5d55fc0a06e7.
  - >-
    The frozen exp-054 instrument is unmodified: adapter.py
    9b503050115a5a48b01ec9f4d348b869495fbe4ee4847dc83188b05a3352f539, run.py
    8cef0f9cd4f473e594ed55e650be2fe7b286a798d2a94e5edb0a35efb7b12d54, verify.py
    e39a6a725e7af01a2e1796e1a218576f76b8a2ec2cecf7fbde3f38aeb9630a7a and test
    17f4be0611fb02419d9007222f07b3f585b290c03866403a1d2bd5da954f01df.
  - 62 focused tests pass; the 35 exp-054 controls are unchanged and still green.
  - >-
    All thirteen named guards fired, including the four required binding mutations
    `unbound-token`, `wrong-direction`, `wrong-quantum` and `changed-released-gain`.
  - >-
    Normal and optimized receipts were byte-identical at SHA-256
    790a973ee5e11e079a3c41dab578311d491eabe5dee76a120ee3a12f5702d76b.
  - Ruff format, Ruff check and BasedPyright pass on the three new files.
  - exp-057 and session-080 pass their enforced soft-schema contracts.
  - The canonical exp-057 result path remained absent throughout.
  - >-
    Later independent Max-level review refused readmission: `_source_interval` supplies
    six-decimal semantics for coordinate tokens, not for the fourteen-digit release-text
    side token. The literal point model survives, but the conjunctive three-model
    criterion does not.
  resource_rollups:
  - packing/campaign/resource-usage/agent-a2713c7d417bc60cc.yaml
  stop_reason: >-
    The author lane reached W2 with its mechanical controls green; later independent
    review stopped BC-138 on missing semantic provenance before any network access.
  next_action: >-
    Retain the literal point-model instrument and the typed refusal. Do not open BC-139;
    a future literal-only route requires a new prospectively frozen hypothesis and
    experiment.
---
# Session-080 — BC-138 `n = 68` Side-Semantics Binding

This session is target-blind.
It opened no network, source or target channel; the parent URL and digest are
declarations carried from `run.py`, not access authority.

Independent readmission later found that the source justifies only the literal
printed-rational point model.
The two six-decimal side intervals reuse coordinate-token semantics without source
evidence for the fourteen-digit release-text side token.
Accordingly, this record preserves the useful target-blind instrument but does not
readmit BC-138 or open BC-139.

## What Was Bound

The reported side token was unbound, so `_exact_side()` refused it and the production
path returned three typed `serialization-refusal` outcomes.
Exp-057 now states what each declared model reads the token as, and `semantics.py`
returns exactly that:

| Model | Side | Direction | Width |
| --- | --- | --- | ---: |
| `declared:svg-literal` | `880345993651653/100000000000000` | exact | `0` |
| `nearest-6` | that value ± `1/2000000` | symmetric | `1/1000000` |
| `truncate-6` | that value to `+1/1000000` | away from zero | `1/1000000` |

Both widths sit far below the one-quarter ceiling
`768618004216131/40000000000000000000`, and every comparison is exact rational
arithmetic.

## No Frozen File Was Edited

`production_model_factory` accepts a scalar `Fraction`, and this lane may not change
that signature. The binding therefore admits the printed value, which lies inside all
three declared intervals, and `bound_run.py` composes the unchanged factory once per
model.
That is an under-approximation of the interval semantics, recorded as one: because
the sought outcome is the existence of a compatible pose and the scalar cells are a
subset of the interval cells, a `compatible` outcome transfers upward to the interval
model while a refusal transfers to nothing.
An interval-valued side would need a different factory signature, which would mean
editing a frozen file, so it is left to whoever may reopen the instrument.

## Boundary

Nothing here measures H-058. The bound entry point runs only the literal target-blind
path against a synthetic SVG under a temporary root, and the canonical exp-057 result
stays absent. Retrieval of the one declared parent belongs to BC-139, and BC-139 opens
only on the coordinator’s different-lane readmission.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
