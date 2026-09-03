---
title: session-081 — BC-140 target-blind guard repairs
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-081
  title: BC-140 target-blind guard repairs
  date: '2026-09-02'
  started_at: '2026-09-02T05:03:00Z'
  deadline_at: '2026-09-02T06:43:00Z'
  branch: claude/squares-pr-73-resume-5lp3bz
  goal: >-
    Make the three routed W7 guard repairs exist as refusable tools: two named negative
    controls and a complete frozen-input inventory for the n = 54 formula audit, a
    pre-freeze normalization check for content-addressed instrument files, and a check
    that every declared parser or recursion bound under cases/ has a named
    bound-exceeding mutation. Target-blind throughout: no source, target or network
    access.
  workflow_phases:
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Give the n = 54 formula audit two named negative controls that no default path can
      reach, keep its --check receipt byte-identical, and add the retained 2009 DS7 HTML
      digest to its frozen-input table.
    commitment: BC-140
    bead: think-hrw2
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 35
    started_at: '2026-09-02T05:03:00Z'
    deadline_at: '2026-09-02T05:38:00Z'
    expected_output: >-
      A refusable audit with --mutate perturbed-side-basis and --mutate
      changed-minimal-polynomial, two passing refusal tests, and an unchanged receipt hash.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q
      tests/test_audit_n54_source_formula.py
    kill_condition: >-
      Stop if the --check receipt bytes move, if either control reaches a receipt instead
      of a refusal, or if the frozen-input digest would need a fetch to obtain.
    fallback: Retain the exact defect and leave the audit unmutated for BC-141 to inherit.
    outcome: >-
      Artifact: devtools/audit_n54_source_formula.py with a NEGATIVE_CONTROLS table and a
      --mutate flag, two refusal tests, and the retained 2009 DS7 HTML row in the audit
      README. Result: perturbed-side-basis is refused by the side-basis identity with
      ValueError "n=54 source identity failed: side basis"; changed-minimal-polynomial is
      refused by the independent minpoly comparison; both exit 1 and print nothing on
      stdout; the --check receipt kept SHA-256
      3555f8910e0daced8022576bea238951654fface93f0d0b51109c0efd3678cf4
      before and after the change. Guard: the mutations are injected downstream of the
      frozen expressions and can only widen a refusal; the 2009 HTML digest
      f14c7cf36c8bfc47b52be6b5fc4257b77acc154444ed2190b7c9a9eeedf43510 was computed from
      the already-retained resources/web copy, with no fetch. Next: write the pre-freeze
      normalization check for content-addressed instrument files.
    evidence:
    - packing/devtools/audit_n54_source_formula.py
    - packing/tests/test_audit_n54_source_formula.py
    - packing/resources/web/n54-source-formula-audit-2026/README.md
    stop_reason: Both named controls refuse, the five focused tests pass and the receipt hash is unchanged.
    next_action: Write devtools/check_instrument_normalization.py with one positive and one negative control.
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Refuse, before a freeze rather than after it, any Python file bound by an immutable
      result that a later ruff format pass would rewrite and thereby sever from its own
      recorded digest.
    commitment: BC-140
    bead: think-hrw2
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: The n = 54 controls refuse and the audit receipt is unchanged, so the first routed repair is done.
    budget_minutes: 35
    started_at: '2026-09-02T05:08:00Z'
    deadline_at: '2026-09-02T05:43:00Z'
    expected_output: >-
      A --json check over every immutable result carrying instrument bindings, passing on
      this repository today and refusing a synthetic unformatted unexcluded binding.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q
      tests/test_check_instrument_normalization.py
    kill_condition: >-
      Stop if the check would need to modify a bound file, or if the real repository
      cannot pass without one.
    fallback: Retain the first typed normalization defect and leave every bound file untouched.
    outcome: >-
      Artifact: devtools/check_instrument_normalization.py and its controls. Result: 38
      immutable results scanned, 9 bound Python files found across the
      instrument_bindings, bindings and binding fields of exp-050, exp-052 and exp-055;
      4 are formatter-clean, 5 are excluded, none violate, exit 0. Guard: a first draft
      refused resources/web/n17-lower-bounds-2026/massaccesi-verify-n17-lower-bound-4_5058.py
      as unformatted, which was a false refusal: resources is a tool.ruff extend-exclude
      scope, so the formatter never reaches it. Exclusion is now read from both the
      per-file tool.ruff.format list and the directory scopes, and anything the
      configuration does not settle is handed to ruff format --check --force-exclude, so
      the check cannot disagree with the formatter that would do the editing. No bound
      file was modified. Next: write the declared-bound check over cases/.
    evidence:
    - packing/devtools/check_instrument_normalization.py
    - packing/tests/test_check_instrument_normalization.py
    stop_reason: The real repository passes, the synthetic unexcluded binding is refused, three focused tests pass.
    next_action: Write devtools/check_declared_bounds.py with the n = 68 depth guard as its positive control.
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      List every module-level MAX_ bound under cases/ and refuse any that no test reaches,
      accepting a test that reaches a guard by its refusal message rather than by the
      constant's name.
    commitment: BC-140
    bead: think-hrw2
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: The normalization check passes its positive and negative controls, so the second routed repair is done.
    budget_minutes: 30
    started_at: '2026-09-02T05:12:00Z'
    deadline_at: '2026-09-02T05:42:00Z'
    expected_output: >-
      A --json check listing all declared bounds, with MAX_XML_DEPTH named by
      test_selected_path_scan_enforces_depth_before_python_recursion and a synthetic
      unnamed bound refused.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q
      tests/test_check_declared_bounds.py
    kill_condition: >-
      Stop if the matching rule cannot accept the n = 68 depth control without also
      accepting a coincidental word, or if a case file would have to be edited.
    fallback: Register the unreachable bounds with reasons and report them rather than editing case files.
    outcome: >-
      Artifact: devtools/check_declared_bounds.py and its controls. Result: 10 declared
      bounds found; MAX_XML_ELEMENTS and MAX_XML_DEPTH are named by
      test_selected_path_scan_enforces_depth_before_python_recursion through the guard
      message "SVG structure exceeds the bounded parser limits", which that test matches
      as "bounded parser limits"; the remaining 8 have no naming test and are registered
      in ALLOWLIST with the reason "pre-existing; registered by BC-140" and a specific
      clause each. Guard: the tool's own control file quotes MAX_XML_DEPTH as data and
      would otherwise have counted as the naming evidence, so it is listed in
      EXCLUDED_REFERENCES and the report names every reference rather than the first;
      guard-message matching requires a literal of at least 12 characters so a
      coincidental word cannot pass. No case file, pyproject.toml or bound file changed.
      Independent readmission later found that the eight allowlist entries do not meet
      BC-140's frozen named-mutation criterion. Next: retain this tool as a diagnostic
      and terminalize the third repair as partial.
    evidence:
    - packing/devtools/check_declared_bounds.py
    - packing/tests/test_check_declared_bounds.py
    stop_reason: >-
      Two bounds are named, but eight pass through a reason-only allowlist and therefore
      do not meet BC-140's literal exit criterion.
    next_action: >-
      Run the mechanical gates, retain the first two repairs, and hand the n = 54 subset
      to W2 readmission without claiming the declared-bound repair complete.
  - workflow: factual-review
    focus: process
    recording: contemporaneous
    clock_role: work
    objective: >-
      Validate the three tools together, record the exact hashes and control names, and
      terminalize this session for the coordinator's different-lane readmission.
    commitment: BC-140
    bead: think-hrw2
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: All three routed repairs exist and refuse their named mutations.
    budget_minutes: 20
    started_at: '2026-09-02T05:16:00Z'
    deadline_at: '2026-09-02T05:36:00Z'
    expected_output: A validated terminal session record with per-file digests and both control names per tool.
    validation_command: >-
      uv run --frozen --all-extras --group dev python -m devtools.validate_schemas && uv
      run --frozen --all-extras --group dev python -m devtools.check_session_clocks
    kill_condition: Stop if any tool's positive control fails on the real repository at the recorded revision.
    fallback: Report the first typed stop naming which repair could not be made refusable.
    outcome: >-
      Artifact: session-081 and the six written files. Result: ruff format leaves all six
      unchanged, ruff check passes, basedpyright reports 0 errors, and the three focused
      suites pass 12 tests together; the n = 54 --check receipt is still SHA-256
      3555f8910e0daced8022576bea238951654fface93f0d0b51109c0efd3678cf4. Guard: the write
      scope stayed inside the seven declared paths; no immutable result, case file,
      pyproject.toml, Git or tbd state changed, and no packing-validate tier ran.
      Independent review admits the n = 54 subset and records the declared-bound repair
      as partial. Next: the coordinator decides whether that narrower subset earns
      BC-141.
    evidence:
    - packing/campaign/agent-sessions/session-081-bc140-target-blind-guard-repairs.md
    - packing/devtools/check_declared_bounds.py
    - packing/devtools/check_instrument_normalization.py
    stop_reason: >-
      The n = 54 controls and normalization check are refusable and validated; the
      declared-bound tool inventories all 10 bounds but leaves eight without the named
      exceeding mutations the agenda requires.
    next_action: >-
      Hand only the readmitted n = 54 controls and frozen-input inventory to the
      coordinator for BC-141 routing; keep the declared-bound repair partial.
  primary_bead: think-hrw2
  status: completed
  budget:
    wall_minutes: 100
    max_cycles: 4
    checkpoint_minutes: 25
    slice_minutes: 35
    finalization_minutes: 20
  stop_conditions:
  - The 2026-09-02T06:43:00Z W2 gate arrives and the coordinator runs readmission.
  - The n = 54 --check receipt bytes move, which would void the audit's frozen output.
  - A repair would require editing a bound instrument file, a case file or pyproject.toml.
  - Any positive control fails on the real repository, which makes the tool unusable rather than strict.
  progress:
    metric: routed W7 guard repairs existing as tools with a passing positive and negative control
    before: zero of three; the n = 54 audit had positive-only tests and no way to be refused
    after: >-
      two repairs complete; the declared-bound inventory finds all 10 bounds, but only
      two have named exceeding controls and eight remain allowlisted
  delegations: []
  outputs:
  - packing/devtools/audit_n54_source_formula.py
  - packing/tests/test_audit_n54_source_formula.py
  - packing/resources/web/n54-source-formula-audit-2026/README.md
  - packing/devtools/check_instrument_normalization.py
  - packing/tests/test_check_instrument_normalization.py
  - packing/devtools/check_declared_bounds.py
  - packing/tests/test_check_declared_bounds.py
  - packing/campaign/agent-sessions/session-081-bc140-target-blind-guard-repairs.md
  checks:
  - >-
    The n = 54 --check receipt had SHA-256
    3555f8910e0daced8022576bea238951654fface93f0d0b51109c0efd3678cf4 before the negative
    controls were added and the same digest after, so the frozen output is unmoved.
  - >-
    devtools.audit_n54_source_formula --mutate perturbed-side-basis exits 1 with an empty
    stdout and "n=54 source identity failed: side basis"; --mutate
    changed-minimal-polynomial exits 1 with an empty stdout and the 8896 mismatch.
  - >-
    devtools.check_instrument_normalization exits 0 over the real repository: 38 results
    scanned, 9 bound Python files, 4 formatter-clean, 5 excluded, 0 violations.
  - >-
    devtools.check_declared_bounds exits 0 over the real repository: 10 declared bounds,
    2 named by test_selected_path_scan_enforces_depth_before_python_recursion, 8
    allowlisted as pre-existing and registered by BC-140.
  - >-
    ruff format leaves all six Python files unchanged, ruff check passes, and basedpyright
    reports 0 errors, 0 warnings and 0 notes over the same six files.
  - >-
    The three focused suites pass together: 5 n = 54 audit tests, 3 normalization tests
    and 4 declared-bound tests, 12 in 32.84 seconds.
  resource_rollups:
  - packing/campaign/resource-usage/agent-a5403a5fd8d5e9f8b.yaml
  stop_reason: >-
    Independent readmission admitted the n = 54 controls and frozen-input inventory but
    stopped the full BC-140 claim because eight declared bounds have no named exceeding
    mutation.
  next_action: >-
    Return the readmitted n = 54 subset to BC-143 under think-8hcp for the frozen routing
    decision; track the eight missing bound controls under D-418 / think-ifgr.
---
# Session-081 — BC-140 Target-Blind Guard Repairs

Two complete repairs and one typed partial stop.
The n = 54 audit gains two named negative controls without its receipt moving a byte;
the normalization check asks, before a result is frozen, whether the formatter could
later sever it from its own digest; the declared-bound check lists every `MAX_` bound
under `cases/`.

Eight bounds have no naming test today.
The lane registered them with reasons because repairing them would mean editing case
files outside its scope.
That makes the inventory useful, but it does not satisfy the frozen rule that every
parser or recursion bound have a named bound-exceeding mutation.
BC-140 is therefore partial, while its independently replayed n = 54 subset remains
eligible to route BC-141.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
