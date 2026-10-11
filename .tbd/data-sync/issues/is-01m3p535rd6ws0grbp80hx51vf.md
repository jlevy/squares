---
type: is
id: is-01m3p535rd6ws0grbp80hx51vf
title: "Math group 1: README, TUTORIAL, SYNOPSIS, conventions, epistemics"
kind: task
status: closed
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies:
  - type: blocks
    target: is-01m3p537xbc65bk9nkax0mwf07
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-29T08:39:25.197Z
updated_at: 2026-10-01T16:04:18.457Z
closed_at: 2026-10-01T16:04:18.456Z
close_reason: "Merged with jlevy/squares#254 (main 5ec014a25): group 1 migrated; check_math_markup backlog 0."
resolution: null
duplicate_of: null
---

## Notes

Reopened: Done only on claude/overview-page-impl, which was never pushed; the owner asked on 2026-09-30 that it be treated as lost. The decision is carried in the revised spec (plan-2026-09-29-github-pages-overview.md) and the work is to be redone.

Correction (2026-09-30 audit): the "treated as lost" reopen note above is wrong. claude/overview-page-impl was recovered, continued to a371c2f5f and is the branch of the overview PR. Group 1 was migrated on it in 5bff221b2 (README, TUTORIAL, SYNOPSIS, conventions, epistemics) without branch B's GitHub placement rules. Measured on GitHub 2026-09-30 at a371c2f5f (blob views, inline math elements vs literal dollars outside math): README 14 math spans, 0 literal; epistemics.md 3, 0; conventions.md 25, 1; TUTORIAL.md 461, 19 (for example side-B and /45-degree spans); SYNOPSIS.md not measured. The website PR converts those spans back to code so it lands clean; the rules themselves (B: c6798905c, b3c245275, cd36d3ddd, 9db587456) and the re-check of group 1 move to the separate math PR on claude/math-everywhere-phase3.
