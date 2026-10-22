---
type: is
id: is-01m5jq8bjb8er6jweszgp9x5mj
title: Emphasize numeric profile tallies without bolding their labels
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: navigation-integration
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-22T21:11:15.274Z
updated_at: 2026-10-22T21:55:32.798Z
started_at: 2026-10-22T21:28:25.430Z
closed_at: 2026-10-22T21:55:32.798Z
close_reason: "Implemented in 09829990c and verified by focused profile/tally/footer tests plus built-in browser review: Accounts second, numeric totals bold, and three-line footer without Profiles."
resolution: null
duplicate_of: null
---
Follow-up PR after #733: profile table summaries show the numeric total in bold (not italic) and result/record/credit labels in regular weight. Preserve muted significance parentheticals and blank zero cells; use the shared tally design component.
