---
type: is
id: is-01m2m6y4gw224dgrwf37bgqnhd
title: "Address review: PR #180 — no-exception browser floor"
kind: task
status: in_progress
priority: 1
version: 15
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
updated_at: 2026-09-16T08:42:40.730Z
---
Track and disposition every published review and addendum finding on PR #180. Reuse think-7o6d for the effective-tsc-coverage fix; create children only for distinct remaining findings. Completion requires fixes or explicit rebuttal/defer, propagation from the final PR #181 head, exact-head CI, and a published disposition map.

## Notes

PR #180 review remediation is integrated locally at exact HEAD 3a9bb2f6e4abf916f4b823e14ca32d1676cd1b5f, a conflict-free merge of held fix head 84ca6cf38fe1d2b88018b7b0ed28816761a742cf with exact main b1b2d30f0aeebaf53cbe4b3acc70938a1864c0a3 (PR #187 session-record hotfix); both are verified ancestors. think-7z01 is closed: both Motion Labs now enforce rendered-pixel paint, ancestor display/visibility/opacity, representative geometry, file-backed layer removal/restoration, and opacity-zero/transparent-paint negative controls, with exact/general committed golden coverage. Root npm typecheck includes tsconfig.explainer.json with parity coverage; think-b9qy remains open only for broader command deduplication. The 280,487-byte golden snapshot-cap regression is fixed with executable proof that no control names or copies it and with change-scope replay coverage. Final integrated validation: git diff --check clean; 213 focused tests passed in one exact-head run; browser floor passed over 552 files with isolated probe gate and 146 Node tests; records tier passed all 33 steps including session gate and synopsis; canonical Ruff/Rust lint passed (1,963 Python files); BasedPyright 0 errors/0 warnings/0 notes; installed Chrome Motion Lab drove exact 36 and general 12 states with visible drawings matching the committed report. Earlier full workbench Chrome and behavioral shard reruns remain valid because the final main delta is record-only and disjoint from the 37-file PR delta. No remaining review finding in PR #180; remaining external publication work is PR body/disposition update, exact-head hosted CI, and deferred checkpoint after the parent pushes.
