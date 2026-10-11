---
type: is
id: is-01m3v5v7qgxh2kmavv0fq6ez97
title: Clean up the merged temporary branches and worktrees from the 30 September integration
kind: chore
status: open
priority: 3
version: 2
labels: []
dependencies: []
created_at: 2026-10-01T07:28:45.803Z
updated_at: 2026-10-06T08:28:56.723Z
---
Merged and no longer needed: claude/overview-fixes-tmp, overview-intro-tmp, overview-papers-tmp, overview-result-pop-tmp, overview-rows-tmp, design-chips-tmp, design-filter-tmp, design-ladders-tmp, design-integration-tmp, ci-runner-variance (after landing), epistemics-ladder-review (its attic/review-inventory.json is the evidence for the no-human-review finding: retain it first), and worktrees under /Volumes/spud-ext1/agent-scratch/worktrees/ (overview-fixes, overview-intro, overview-papers, overview-result-pop, audit-main, epistemics-ladder), plus the older local mirror ~/wrk/github/squares-overview-preview and branch overview-preview. Scratch builds under /Volumes/spud-ext1/agent-scratch/squares-site-*. Not before the stack lands.

## Notes

2026-10-06 (bead review): of the listed branches only claude/ci-runner-variance is still on origin; the local worktrees and the mirror cannot be checked from a cloud session.
