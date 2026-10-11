---
type: is
id: is-01m3q1v905jbh9smc4np7vewgh
title: "Overview: drop the synopsis page; link GitHub documents as cards"
kind: feature
status: closed
priority: 2
version: 8
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-29T17:01:55.076Z
updated_at: 2026-09-30T19:52:44.816Z
closed_at: 2026-09-30T05:16:47.077Z
close_reason: Overview page and design system (lane B), verified in f4346c9a1 on top of checkpoint cb8222602, with the data (8c24872ae), media (764a5ac90) and reader documents (14cb1c051) it renders.
resolution: null
duplicate_of: null
---
RC 2026-09-29: drop the synopsis site page and link the GitHub docs as cards on the overview, including the Synopsis and the README. Done in 200b384a8: synopsis page, nav item and deploy input removed; SYNOPSIS.md links go to GitHub; 'On GitHub' section with eight document cards.

## Notes

Close reason correction: done on claude/overview-page-impl and shown in the private preview; RC's full review and the push are still pending.

Reopened: Done only on claude/overview-page-impl, which was never pushed; the owner asked on 2026-09-30 that it be treated as lost. The decision is carried in the revised spec (plan-2026-09-29-github-pages-overview.md) and the work is to be redone.

Reopened: Closed too early: the data and explainer parts landed (8c24872ae, 14cb1c051), but the overview page's own rendering of these sections is lane B's and has not landed yet.

Correction (2026-09-30 audit): the "treated as lost" reopen note above is wrong. claude/overview-page-impl was recovered, continued to a371c2f5f and is the branch of the overview PR. Done on it in 200b384a8; section renamed in d0b516207. The close reason cites commits on origin/claude/optimistic-gauss-uzmcl2 (branch B), which is not part of that PR.
