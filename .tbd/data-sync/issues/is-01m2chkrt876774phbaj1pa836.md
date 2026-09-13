---
type: is
id: is-01m2chkrt876774phbaj1pa836
title: Make workbench navigation respect the GitHub Pages project subpath
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m29f3zcv8kfcf70ra7fpkd1j
created_at: 2026-09-13T04:50:05.765Z
updated_at: 2026-09-13T04:50:05.765Z
---
Review R7: build_workbench_site.py NOTE links href=/ while project publishes at https://jlevy.github.io/squares/. From /squares/workbench/ this points to the account site. Use a relative project-root link and smoke-test both page loading and navigation under /squares/; extend existing post-deploy scope think-9x0m to workbench.
