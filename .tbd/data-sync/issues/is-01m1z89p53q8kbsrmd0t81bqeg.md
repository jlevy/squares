---
type: is
id: is-01m1z89p53q8kbsrmd0t81bqeg
title: Scope release-only pre-push checks without rebuilding unchanged atlas geometry
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels:
  - validation
dependencies: []
parent_id: is-01m1sd4d4a37f6kf2hfb93xg0a
created_at: 2026-09-08T00:57:10.562Z
updated_at: 2026-09-08T01:16:33.862Z
---
Observed during PR117 / think-1z5n after pinning publication artifacts to cef19bfe. The diff changed only release.py, eight atlas exports, and three generated claim documents; no geometry inputs, witnesses, certificates, verifiers or manifests changed.

Coordinator-reported evidence: packing-validate --push --since cef19bfe --jobs 4 --inner-jobs 1 selected about 40 test modules / 850 tests with -m 'not exhaustive_exact'. Its reachable behavioral step timed out at the 900-second cap, approximately 46% through, with no assertion failure observed before cutoff; the other 44 steps passed and total wall time was 997.02 seconds. Log: /tmp/v024-integrated-prepush.json (prose preamble followed by JSON). Before that run, an independent complete known-best selection passed 3/3 in 558.37 seconds and 106 focused publication tests passed in 475.24 seconds. These are separate completed runs, not a claim that their evidence is automatically reusable by the current selector. Preserve or link durable receipts before the temporary log disappears.

Static cause: devtools.reachable_tests selects at file granularity. Its changed-module import closure follows sqpack.release into build_known_best_atlas and render_explainer and then their test modules; changed generated filenames also select consumers. This is a narrow selection, not the .github whole-suite fallback tracked by think-oe1g. The --run subprocess is pytest without xdist and deliberately includes slow tests. test_known_best_composite_contains_every_case_and_square calls expected_outputs(worker_count(CORPUS.count)); PACK_JOBS=1 therefore makes it repeat the complete 324-case geometry build serially in a fresh process. The corrupted-source control separately calls expected_outputs() with the API's default one worker until its expected rejection, and the full witness/manifest test loops serially. The gate's outer --jobs pool does not parallelize a single pytest process.

Immediate supported rerun: --jobs 2 --inner-jobs 4 preserves the selected files and marker expression and gives the full-corpus consumer four process workers. It does not enable pytest xdist or change the serial/default-one controls. No success or speedup is claimed in this bead until that rerun finishes.

Narrow follow-up proposal: under the existing W5 family-selection/reuse plan, define one explicit publication-only change contract. Recognize only declared release-literal changes and corresponding stamp/date/permalink export changes, keep direct edition, link, claim-byte and export-receipt checks, and avoid re-deciding unchanged geometry only when the complete geometry input closure and a trusted completed baseline verdict justify that reuse. Explain the selected obligations and any reused/deferred family in the output. If a source, witness, renderer, certificate, verifier, non-publication SVG content, or unknown path changes, or evidence is missing/stale, retain the current conservative selection. Do not simply exclude all slow tests, raise the timeout, or replace whole-geometry coverage with a sample. Keep the existing full/deferred checks and mathematical negative controls intact.

Acceptance requires a release-only fixture, exact selected-family assertions (related selector-control gap: think-mo7r), and negative controls for changed geometry, corrupted retained source, changed certificate/verifier bytes, stale exports, missing baseline evidence, and a tree that changes after selection. Compare identical checked-source/coverage obligations and report wall time separately from total work. This is a follow-up under think-xejq, not a blocker for completing PR117; no selector, test, process-budget or gate change was made by this review.

## Notes

PR117 closeout disposition, reported by the coordinator: the user explicitly asked not to wait for duplicated local and hosted checks and to land promptly. The supported local rerun (--jobs 2 --inner-jobs 4, session 16116) was stopped with Ctrl-C, exit 130, after confirming that all required hosted jobs had passed except the bead-tree check. No matching local validation or selector process remained. This interrupted run is not a pass and establishes no worker speedup.

The remaining hosted failure was unrelated bead hierarchy: open follow-ups think-ycuo and think-6l2l sat under completed audit think-muns. Only those parent links were removed; the follow-ups remain open and the audit remains closed. think-dyyc remains under open think-xejq. The coordinator will retry only the failed hosted job, then merge and check deployment. This case reinforces the follow-up's requirement to avoid paying for duplicate extensive local and CI suites on publication-only edits while retaining explicit source-bound coverage and honest interruption/failure status. No code or gate policy was changed to complete this PR.
