---
type: is
id: is-01m3qhytx3t5c4gz825rgaddk2
title: "Overview: every card opens a popover previewing its target, with a button to go there"
kind: feature
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-29T21:43:28.931Z
updated_at: 2026-09-30T19:52:54.158Z
closed_at: 2026-09-30T05:16:47.134Z
close_reason: Overview page and design system (lane B), verified in f4346c9a1 on top of checkpoint cb8222602, with the data (8c24872ae), media (764a5ac90) and reader documents (14cb1c051) it renders.
resolution: null
duplicate_of: null
---
RC 2026-09-29: from the popover show a preview of the next page with a button to expand it, or a preview of the result with a button to take you there. Supersedes the popover-or-link split of think-oqbh.

## Notes

Reopened: Done only on claude/overview-page-impl, which was never pushed; the owner asked on 2026-09-30 that it be treated as lost. The decision is carried in the revised spec (plan-2026-09-29-github-pages-overview.md) and the work is to be redone.

Correction (2026-09-30 audit): the "treated as lost" reopen note above is wrong. claude/overview-page-impl was recovered, continued to a371c2f5f and is the branch of the overview PR. Done on it in 1a4b6d371. The close reason cites commits on origin/claude/optimistic-gauss-uzmcl2 (branch B), which is not part of that PR.
