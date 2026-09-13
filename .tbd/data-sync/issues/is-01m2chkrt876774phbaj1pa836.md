---
type: is
id: is-01m2chkrt876774phbaj1pa836
title: Make workbench navigation respect the GitHub Pages project subpath
kind: bug
status: open
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
  - workbench-phase-2
dependencies:
  - type: blocks
    target: is-01m2cm03rtrjcg98ejb9y56jn6
  - type: blocks
    target: is-01m29f4zbw0vv3xj1xbe95narx
  - type: blocks
    target: is-01m28p88qyq83eek30pja3np54
parent_id: is-01m29f3zcv8kfcf70ra7fpkd1j
created_at: 2026-09-13T04:50:05.765Z
updated_at: 2026-09-13T05:43:46.969Z
---
Review R7: build_workbench_site.py NOTE links href=/ while project publishes at https://jlevy.github.io/squares/. From /squares/workbench/ this points to the account site. Use a relative project-root link and smoke-test both page loading and navigation under /squares/; extend existing post-deploy scope think-9x0m to workbench.
