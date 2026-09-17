---
type: is
id: is-01m2phfjztg9q7vckn8he9jb9e
title: "Pages deploy is skipped on every main push since PR #183"
kind: bug
status: open
priority: 0
version: 2
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels:
  - ci
  - pages
dependencies: []
parent_id: is-01m2m5zjmj7dsycs1x6yxwcwwt
created_at: 2026-09-17T02:00:13.049Z
updated_at: 2026-09-17T02:29:14.089Z
---
The last GitHub Pages deployment is 8484d616 at 2026-09-16T06:51:50Z. Every main push since PR #183 merged (4ef41be3, 06:57Z) has scope, prepare, publish and pages-required succeeding while deploy and verify-deployment are skipped (runs 35066124740, 35069352666, 35082799418, 35147913438), so nothing merged since is published. deploy's condition (github.ref == refs/heads/main && event != pull_request) is true on those pushes. It carries no status function, so its implicit success() also covers skipped ancestors, and #183 added explainer-unchanged/workbench-unchanged pairs to pages-required's needs, one of which always skips. PR #188's pages.yml keeps the same deploy and verify-deployment conditions. Fix on #188: give deploy and verify-deployment explicit !cancelled() plus needs.<job>.result == 'success' conditions, add a contract test in packing/tests/test_pages_workflow.py that no job on the deploy path relies on implicit success() while an ancestor can skip, and confirm the first main push after merge records a new github-pages deployment and a passing verify-deployment.

## Notes

2026-09-17: fixed on PR #188 in 2def8265 (deploy and verify-deployment now require !cancelled() and success of their direct needs; contract test test_the_deploy_path_does_not_inherit_skips_from_its_ancestors with a negative control reproducing the pre-fix condition). Focused Pages tests 273 passed; packing-validate --edit 48 of 80 steps passed. Diagnosis evidence: at 8484d616 (last deploy) deploy's ancestors were build, font-loading, prepare with no conditional jobs; from 4ef41be3 (#183) they include startup-timing (dispatch-only) and explainer-unchanged/workbench-unchanged, which skip on every push. Close after #188 merges and the first main push records a new github-pages deployment with verify-deployment passing.
