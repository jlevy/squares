---
type: is
id: is-01m4zn9wfkeaagyv78fm101dyr
title: "T1: keep PDF accent guidance accurate about unprinted legend counts"
kind: bug
status: closed
priority: 3
version: 3
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4me9gfnc1denbcj8v7veqnp
hold: null
hold_until: null
created_at: 2026-10-15T11:31:34.002Z
updated_at: 2026-10-15T11:37:18.509Z
started_at: 2026-10-15T11:31:43.208Z
closed_at: 2026-10-15T11:37:18.506Z
close_reason: Corrected local closure preparation with independent review and executed validation. T1 unsupported printed-legend count sentence removed and senior-confirmed clear. External TMPDIR/Cargo/cache directories now exist with writable preflight in tutorial-closure env.sh; pinned Chromium required. Four existing News interaction/facet cases passed55.62s, no skips. Separate109source cases passed49.41s. Earlier4skip/4setup-error receipts retained; no assertion weakened. Parent delivery beads remain open until hosted publication.
resolution: null
duplicate_of: null
---
Independent senior working-tree review of tutorial-closure found the edited figure-playbook row says composite legends display recent-contribution case counts, but _append_summary_legend deliberately omits that count. Remove the inaccurate sentence and keep the numeric-only accent/neutral-label rule. No renderer behavior or tally changes.
