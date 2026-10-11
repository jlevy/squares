---
type: is
id: is-01m3q1va3a17zgvtsvkb2ry39s
title: "Site: math face matches its text (serif with serif, sans with sans)"
kind: bug
status: closed
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-29T17:01:56.201Z
updated_at: 2026-09-30T19:52:46.691Z
closed_at: 2026-09-30T05:16:47.167Z
close_reason: Overview page and design system (lane B), verified in f4346c9a1 on top of checkpoint cb8222602, with the data (8c24872ae), media (764a5ac90) and reader documents (14cb1c051) it renders.
resolution: null
duplicate_of: null
---
RC 2026-09-29: some serif text used sans math. Cause: kpress sets math inside <details> in sans, and the results table summaries were serif (55 bounds). Fixed in 4cfb962e6: summaries use the sans face; preview_site now reports any formula whose computed face disagrees with its surrounding text (probe preview_site/math_face); zero on every page at 1280 and 390.

## Notes

Close reason correction: done on claude/overview-page-impl and shown in the private preview; RC's full review and the push are still pending.

Reopened: Done only on claude/overview-page-impl, which was never pushed; the owner asked on 2026-09-30 that it be treated as lost. The decision is carried in the revised spec (plan-2026-09-29-github-pages-overview.md) and the work is to be redone.

Correction (2026-09-30 audit): the "treated as lost" reopen note above is wrong. claude/overview-page-impl was recovered, continued to a371c2f5f and is the branch of the overview PR. Done on it in 4cfb962e6. The close reason cites commits on origin/claude/optimistic-gauss-uzmcl2 (branch B), which is not part of that PR.
