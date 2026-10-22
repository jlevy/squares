---
type: is
id: is-01m5jczh01a1tdr0x7h4dc686j
title: Order shared cards and profile work as Records Results Credits
kind: task
status: in_progress
priority: 2
version: 2
delegate: squaremath-tally-order
labels: []
dependencies: []
parent_id: is-01m5jct23n8s7fj3ydf94n0yhv
hold: null
hold_until: null
created_at: 2026-10-22T18:11:40.159Z
updated_at: 2026-10-22T18:11:53.400Z
started_at: 2026-10-22T18:11:53.399Z
---
Implement the delegated tally/section ordering portion of the user follow-up: use Records, then Results, then Credits in shared project/resource cards, per-profile tally summaries, and profile work sections. Directory summaries and table columns already use that order and must remain correct. Preserve exact counts, significance formatting, hyperlinks, blank/zero rules, and pending-comparison semantics.

Write ownership: overview_sections.project_tally; render_contributors.profile_tally and _credited_work; corresponding targeted tests. Coordinator separately owns naming functions and documentation in shared files. No commit or push.
