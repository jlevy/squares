---
type: is
id: is-01m2m6y4gw224dgrwf37bgqnhd
title: "Address review: PR #180 — no-exception browser floor"
kind: task
status: in_progress
priority: 1
version: 13
labels: []
dependencies:
  - type: blocks
    target: is-01m2m5zjmj7dsycs1x6yxwcwwt
parent_id: is-01m2k77cev2mj85dkb88nxedp8
child_order_hints:
  - is-01m2m6zpqj2e6aq0af3fv4svzq
  - is-01m2m6zq4fj016spkk035tkn93
  - is-01m2m6zqkgrbwg2j352gjpf6m6
  - is-01m2m6zr27r3b0h6tvnsh2zd1y
  - is-01m2m6zrghb5dv2vjgbzhgxfn9
  - is-01m2m6zrysz50dnrmahfmh4cf7
  - is-01m2m6zsddpzdefgjcjh1xmrq9
created_at: 2026-09-16T04:17:26.555Z
updated_at: 2026-09-16T08:08:45.308Z
---
Track and disposition every published review and addendum finding on PR #180. Reuse think-7o6d for the effective-tsc-coverage fix; create children only for distinct remaining findings. Completion requires fixes or explicit rebuttal/defer, propagation from the final PR #181 head, exact-head CI, and a published disposition map.

## Notes

PR #180 review remediation is integrated locally through 84ca6cf3 on parent main 398e59e4 (merge ba2cde3b; no push). think-7z01 is closed: both Motion Labs have a rendered-pixel paint invariant, file-backed layer removal/restoration probe, live opacity-zero and transparent-paint mutants, and an installed-Chrome 36+12-state committed-golden pass. The final #181 probe-type isolation is preserved while #180 keeps one effective ESLint configuration and repository-wide invocation. Root npm typecheck includes tsconfig.explainer.json with parity coverage (think-b9qy updated but remains open for command deduplication). The 280,487-byte golden's branch-owned mutation-snapshot cap regression is fixed by excluding that generated/non-control input, with executable control-census and change-scope tests. Integrated evidence: 192 focused tests; browser floor over 552 files plus isolated probe gate and 146 Node tests; npm run typecheck; Ruff 1,963 files; BasedPyright 0/0/0; full workbench Chrome check; Motion Lab Chrome check. Full fast reached 3,139/3,138 tests per shard; remaining failures were sandbox/editable-install artifacts or the inherited PR182 closed-debt baseline. The unrelated session-record hotfix is intentionally excluded and will be integrated from main before publication. Remaining: integrate that main hotfix, rerun exact focused/fast surfaces, update PR body/dispositions, and require exact-head hosted CI.
