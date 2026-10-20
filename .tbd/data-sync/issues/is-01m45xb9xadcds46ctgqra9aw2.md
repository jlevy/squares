---
type: is
id: is-01m45xb9xadcds46ctgqra9aw2
title: Negative controls on check_readme, validate_schemas and ledger check run over a red worker baseline
kind: bug
status: in_progress
priority: 1
version: 8
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m1sx5m1p5868jhwcdzfkvada
child_order_hints:
  - is-01m502aqkn2f7anfqwnc26v3ff
  - is-01m504ante81cj7exkdeek6n50
hold: null
hold_until: null
created_at: 2026-10-05T11:31:53.898Z
updated_at: 2026-10-15T16:01:15.959Z
started_at: 2026-10-15T13:49:13.882Z
---
Three checks that negative controls are built on already exit 1, unmutated, inside a mutation worker snapshot. A control is scored as "exited non-zero and printed its expected message", with no green baseline demanded. So the 4 + 10 + 35 controls on these commands are currently scored over a checker that is red before any mutation is applied. That is the blinding class the `PRUNE` comments in `packing/devtools/run_negative_controls.py` warn about (bibliography.yaml, 2026-09-22). A looser `expect:` string, or a mutation whose message happens to coincide, would let a control pass over a checker that never reached the code it rehearses.

Measured 2026-10-05 on PR 347 (`claude/n17-sessions-167-168`) at c89b841d4, with and without the composite-vector prune 40aa3be3a. The output was byte-identical in both cases, so neither prune causes it. Method: `clone_tree` into a temp dir, then each command run unmutated with the harness's environment (`UV_NO_SYNC=1`, `PYTHONPATH` = worker src/packing/workbench tools, fresh `PYTHONPYCACHEPREFIX`, venv `python3` on PATH).

1. `python3 -m devtools.check_readme` (4 controls) exits 1 with "README.md has drifted from the directory". The README layout tree names 14 root entries the snapshot does not copy: CLAUDE.md, Makefile, biome.json, eslint.probes.json, lefthook.yml, package-lock.json, tsconfig.base.json, tsconfig.devtools-node.json, tsconfig.motion-lab.json, tsconfig.n11-lower-bounds-explainer.json, tsconfig.overview.json, tsconfig.probes.json, vendor, vendor/kpress. `ROOT_DOCUMENTS` copies only README/SYNOPSIS/docs/packages and similar, not these.

2. `python3 -m devtools.validate_schemas` (10 controls) exits 1 with 44 FAIL lines:
   - `FAIL bibliography.yaml: declared schema not found: bibliography.schema.yaml`. `COPY_SEPARATELY` rescues `resources/bibliography.yaml` but not its schema.
   - 43 verifier cross-checks naming files under the pruned `packing/resources/web/...`, for example `V-tokoharu-verify-cpp names packing/resources/web/external-square-certificates-2026-09-22/tokoharu-density/src/run_verify.py, which does not exist`; also V-evand-*, V-burns-n17-verify-py, V-anabologyco-n17-checker, V-wand125-*.

3. `python3 -m sqpack.campaign.ledger check` (35 controls) exits 1 with two failures:
   - `FAIL agenda-015-ten-hour-earned-routes-and-guard-repairs.md: closeout change post-agenda-discipline references missing path .github/PULL_REQUEST_TEMPLATE.md`. `.github/` is not copied, apart from workflows reached through links.
   - `FAIL series/series-000-smoke-and-calibration/experiments/exp-249-h267-n17-first-certified-sub-patterns.md: dead link -> ../../../explorations/X048-session-168-pilots/certificates/`. PR 347 prunes `X048-session-168-pilots` whole, and `linked_pruned_targets` restores linked FILES, not directories (`resolved.is_file()`). A link to a pruned directory is therefore dead in every worker. PR 360's 93a6839ca prunes the Sessions 169-179 folders the same way and may add more such cases.

`check_generated_markdown` and `check_synopsis` were green in the same worker.

Evidence: the full outputs from the 2026-10-05 session are `baseline-pruned/*.txt` and `baseline-unpruned/*.txt`, and the reproduction script is `snapbaseline.py` (session scratchpad, not committed). The script clones one worker with the current `PRUNE` and runs the given commands unmutated; set `UNPRUNE_COMPOSITES=1` for the comparison run.

Suggested acceptance:
- A harness mode or test that runs each distinct control command unmutated in a fresh worker and demands the clean result each control's rehearsal assumes. Where a command cannot be green in a worker, record that explicitly with its reason.
- Then fix the three causes. Options: copy, or rescue in COPY_SEPARATELY, the root files the README layout names and `resources/bibliography.schema.yaml`. Decide whether verifier cross-checks treat a pruned `resources/` path as present (the existence-only manifest idea in think-t1lk's Sol audit note). Copy `.github/PULL_REQUEST_TEMPLATE.md`. Make `linked_pruned_targets` restore a linked pruned directory, or make the ledger check consult the worker manifest.
- None of this may weaken the real gate's checks on the full checkout.

## Notes

2026-10-12 reconciliation: 74e4a0819 (on main since 2026-10-05) made check_readme and the ledger check green unmutated in a worker; validate_schemas (verifier-registry paths under pruned resources/web/) and test_change_scoped_selection.py (vendor/kpress) remain red and are this bead's remaining scope.

2026-10-15, PR #611 (review A2): another instance of this class was found and fixed. Under
`CI`, `check_gate_budgets` refuses an advisory bead it cannot confirm, and a worker's fresh
repository held no bead store. So in every hosted worker it exited 1 unmutated, and its six
controls (controls.yaml "gate budgets - ...") were scored over a red checker. This was on main
as well as the branch.

Found by: hosted suite-c at 227c345eb, after the PR had added `check_gate_budgets` to
`GREEN_BASELINE_COMMANDS`.

Fix: `index_tree` now points each worker at the source's sync-branch refs through
`objects/info/alternates` plus `update-ref` (`_carry_bead_store`). Nothing is fetched, so the
worker is not shallow.

Evidence, with `CI=1`:
- `check_gate_budgets` exits 1 in a worker built by c8181dd77's runner and 0 in one built by
  the fix.
- All six controls fire.
- `test_gate_budgets_reads_its_wall_workflows_in_a_worker` asserts green under `CI` wherever
  the source holds the refs.

Remaining scope is unchanged: `validate_schemas` and `test_change_scoped_selection.py`.

2026-10-15 current-source audit at main 31eaf633 / PR620 cf9003e0 confirms the remaining scope. Snapshot COPY_SEPARATELY restores only three formerly review-rescued verifier files, while verifier_registry still stats all declared source/version/independence paths. vendor/kpress is still absent from ROOT_DOCUMENTS, COPY_SEPARATELY and LINK_BACK. GREEN_BASELINE_COMMANDS excludes validate_schemas and change-scoped selection tests. No new worker was instantiated; historical failure counts and source-size figures are not current measurements. The earlier README, ledger and gate-budget repairs remain landed. Preserve those fixes and address only the remaining schema/vendor input closure, alongside mutated-output equivalence under think-7wpx. Real local before/after acceptance needs more external scratch than the available roughly 76 MiB; other authorized hosts with adequate scratch may proceed. Evidence: assurance-followup-current-source.json.

2026-10-15T16:01:15.672800+00:00: Gate-selection directory closure63k0 is source-reviewed and actualbefore/afterverified (unmutated red->green; both intended mutations retained). Remaining schema closure is active childthink-ezpi. Actual CURRENT before schema baseline exits1 with148missing-pathFAILlines, no timeout; all10existingmutations still scorepassed. Full decodedbefore records retained. Metadata diagnosis: net118exactfiles4342876B and5emptydirs; projected218892501B against226492416cap. Author now implements shared pure four-class declaration extraction and requested-revision inventory protection; no checker/control changes. This is intentional baselinecorrection, not7wpxoutputequality.
