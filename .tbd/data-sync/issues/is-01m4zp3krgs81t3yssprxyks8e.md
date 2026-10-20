---
type: is
id: is-01m4zp3krgs81t3yssprxyks8e
title: Fix the lower-bounds paper release command missing its required PDF update mode
kind: bug
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels:
  - pr-619
dependencies: []
parent_id: is-01m4zh3apr6q86jmjggvd08bhr
hold: null
hold_until: null
created_at: 2026-10-15T11:45:37.028Z
updated_at: 2026-10-15T13:17:34.419Z
started_at: 2026-10-15T11:46:10.735Z
closed_at: 2026-10-15T13:17:34.419Z
close_reason: Delivered in PR619, merged 31eaf6333c5d5b6b3d111241768cdd3d30982588. All 43 executed PR checks and selected Deep38735581202 passed. Main Pages38739226771 published site v0.7.7, shared infographics v0.6.1 and lower-bounds paper v0.4.7; actual deployment audit job116439283652 passed 4460/4460 checks. Main full Packing remains independently in progress; no three-minute performance claim. Focused CI safety and performance work continues under think-3d1m and think-kxmq.
resolution: null
duplicate_of: null
---
The real maintained paper v0.4.7 cut exposed an existing generation-command defect: cut_release steps invokes devtools.render_n11_lower_bounds_explainer_pdf without --update, but its real parser requires a mode. HTML/Markdown and release.py are prepared; PDF step correctly refused before publication. Add the required mode and a meaningful contract through the actual renderer parser, keep v0.4.7 fixed, then resume its remaining PDF/test commands. Preserve failed cut receipt; this defect predates PR618 and must be fixed on tutorial-closure rather than restarting its unchanged selected deep gate.

## Notes

Fixed at closure head4ddf4935: planned lower-bounds PDF command includes --update. Real-parser regression was red (SystemExit2), then all23 release-cut cases passed3.59s. Actual paper v0.4.7 PDF generation succeeded; final output869250bytes,2/2page loads agreed. Original failed cut log preserved. Owning selection313pass/15deselect/1stale edition-reference failure; tutorial now referencesv0.4.7 and exact corrected oracle passed0.81s. No repeated version bump. Await hosted delivery/publication; think-8iml remains open until this fix ships.
