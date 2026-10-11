---
type: is
id: is-01m3qt4tn0qda132ey59mz7x4v
title: On GitHub links point at the default branch, not the build commit
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-30T00:06:33.888Z
updated_at: 2026-09-30T19:53:02.521Z
closed_at: 2026-09-30T05:16:47.163Z
close_reason: Overview page and design system (lane B), verified in f4346c9a1 on top of checkpoint cb8222602, with the data (8c24872ae), media (764a5ac90) and reader documents (14cb1c051) it renders.
resolution: null
duplicate_of: null
---

## Notes

Reopened: Done only on claude/overview-page-impl, which was never pushed; the owner asked on 2026-09-30 that it be treated as lost. The decision is carried in the revised spec (plan-2026-09-29-github-pages-overview.md) and the work is to be redone.

Correction (2026-09-30 audit): the "treated as lost" reopen note above is wrong. claude/overview-page-impl was recovered, continued to a371c2f5f and is the branch of the overview PR. Done on it in 30c2d10c0, generalized in 8ffa5fba1 (every repository link on main via repo_links.py). The close reason cites commits on origin/claude/optimistic-gauss-uzmcl2 (branch B), which is not part of that PR.
