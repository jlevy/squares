---
type: is
id: is-01m5k43m5fe3n8y79bk535ddtt
title: Finish News topic palette, shared intro typography and profile table refinements
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: navigation-components
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T00:55:51.726Z
updated_at: 2026-10-23T01:17:48.797Z
started_at: 2026-10-23T00:56:58.615Z
closed_at: 2026-10-23T01:17:48.796Z
close_reason: null
resolution: null
duplicate_of: null
---
Apply a shared neutral surface with readable topic-colored ink to all News tags, Topic dropdown options and selected summaries in both themes; preserve result/status/significance palettes. Right-align Reset above the count. Reduce shared H1/site-title bottom spacing from 2.5rem to 2rem while preserving top/hero spacing. Rename visible report invitations Report a Result and replace the homepage documentation preview with About the Squares Project linking about.html while retaining legacy anchors. Use one purpose-only serif sentence for Contributor Profiles and give Accounts room without splitting usernames; preserve responsive table scrolling and resource URL wrapping. Latest user override restores all bare standalone introductions to serif while navigation, headings, buttons, filters and metadata remain sans; delete the Results Archive introduction entirely. Update palette/typography validation and design notes. Parent integrates builds, commits and CI.

## Notes

Completed source checkpoint pushed by coordinator as 1f682c650 (earlier News/About changes in 99439432c). Focused validation: tests/test_rung_scale.py 24 passed in 4.46s, including real News both themes at 1280/390/320px, all neutral topic surfaces/colored ink, Reset above count/right alignment, 32px H1 bottom and no page overflow. Palette CLI passed; minimum topic contrast 6.8:1 light and 7.3:1 dark. Focused profile renderer and browser tests 2 passed in 14.89s: one-purpose-sentence serif intro, sans table, Accounts labels whole at 1280/390/320 with narrow table scrolling. Node overview_table/table.test.mjs and filters.test.mjs: 37 passed; Node/probe TypeScript clean. Safeleaf News/Overview assets refreshed without pruning; latest full preview is coordinator session35075. Source frozen. Plan and paper-design final edits handed to frontier_split for integrated docs checkpoint; parent handles final full build/CI.
