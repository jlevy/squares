---
type: is
id: is-01m3vh05cgv7pt63vy17h1cg2y
title: "Prose cleanup: fixes from the independent review of jlevy/squares#266"
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T10:43:41.577Z
updated_at: 2026-10-01T17:12:06.125Z
closed_at: 2026-10-01T17:12:06.121Z
close_reason: Merged with jlevy/squares#271 (main c1f1b2751, 2026-10-01).
resolution: null
duplicate_of: null
---
The review of #266 (no blocking finding) left four medium and eight low findings. On branch claude/prose-review-fixes, cut from 45c2e5a29: M1 RESULTS.md 'Next actions' prints each next_rung as one unbroken bullet (render_results.py:169); M2 n-103, n-152, n-180 state Couzo's priority more strongly than the two timestamps support; M4 T-058 and T-059 lack date, link and AI-assistance statement; L1 seven claims link a repository root instead of the retained revision; L2 two hand-written credit lines still say 'this project'; L3 residual 'pinned'/'first-party' wording; L4 awkward sentences; L5 a typo in T-023; L6 the credit policy's subject rule against T-005 and T-010; checker gaps (printed front-matter fields, ISO timestamps, named clocks). Reviewer's notes: /Volumes/spud-ext1/agent-scratch/review-266/. Not in scope, owner decides: M3, the credit of T-025, T-026, T-033, T-031 (same support as T-024, credited after Burns, Massaccesi) and T-009 (after the packers?).

## Notes

Done on claude/prose-review-fixes (8503e42ab), draft jlevy/squares#271 stacked on #266: M1 next actions in paragraphs; M2 the recommit caveat restored at n = 103, 152, 180; M4 T-058 and T-059 credited with link, date and AI statement; L1 to L6 applied; check_prose_ceremony reads the printed front-matter fields and catches ISO timestamps and named clocks. Records and edit tiers pass. Not changed, owner decides: the credits of T-025, T-026, T-033, T-031, T-009.
