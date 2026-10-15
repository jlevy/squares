---
type: is
id: is-01m4zmmp3v11y25f6b8c6fjgvq
title: Reconcile delivered News and tutorial plan status after live publication
kind: task
status: in_progress
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4vns6xeff13savsant84279
child_order_hints:
  - is-01m4znhtfbdwfewvssggm76b6q
hold: null
hold_until: null
created_at: 2026-10-15T11:19:59.354Z
updated_at: 2026-10-15T12:18:48.808Z
started_at: 2026-10-15T11:20:27.762Z
---
Reader delivery PR617 is merged, live v0.7.5 and hosted publication/full main checks succeeded. Update stale pending delivery statements in the site-changelog and basic/advanced tutorial plans; record actual reviewed/CI/publication receipts and separate longer CI follow-ups. Preserve original scope and existing history. Include the scoped tutorial counting-certificate correction under think-3kk4 and disposition think-rd7a based on current explicit Lean build/expert-review limits.

## Notes

Closure head4ddf4935 reconciles the existing News and basic/advanced tutorial plans with delivered reviewedPR604/617 and actual publication receipts, removes stale pending language and separates ongoing CI follow-ups. PR618 is now mergedfc2ceae79/livev0.7.6 and its delivery+omission are recorded in the News record. New closure sitev0.7.7 is prepared via maintainedcut111pass15deselect; final release impacterrors[] with3unaffected-paper exemptions. Finalreview/validation/publication pending; no claim that the larger CI plan has landed (its source remains unmerged codex/main-test-timing65aff4580).
