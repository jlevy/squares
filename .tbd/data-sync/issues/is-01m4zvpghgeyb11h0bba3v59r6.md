---
type: is
id: is-01m4zvpghgeyb11h0bba3v59r6
title: Fix PR620 audit layout and missing durable-document map entry
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels:
  - pr-620
dependencies: []
parent_id: is-01m4zsr7m7gexqq4fsexm5jx9x
hold: null
hold_until: null
created_at: 2026-10-15T13:23:19.215Z
updated_at: 2026-10-15T13:37:09.187Z
started_at: 2026-10-15T13:23:35.479Z
---
Ordinary Packing38741375831 failed two fast checks on head82b81649: the new retrospective JSON used 9103-line generic layout rather than maintained retained_json layout, and the new plan lacked its durable document-map entry. Re-lay JSON with the maintained formatter without changing decoded values; add the plan to the existing document map without weakening coverage. Run both actual fast checker commands locally, then re-review the small fix and retain original failed receipts. Cancel the superseded full trial rather than pay for a known-red source.
