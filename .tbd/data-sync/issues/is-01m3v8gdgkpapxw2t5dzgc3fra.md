---
type: is
id: is-01m3v8gdgkpapxw2t5dzgc3fra
title: Case popovers are taller on larger screens
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T08:15:17.008Z
updated_at: 2026-10-01T10:13:12.584Z
closed_at: 2026-10-01T10:13:12.557Z
close_reason: "196cbcd2c, on the follow-up branch claude/site-polish-3 (f00ec72fe): one height token (the window's height less a margin) replaces the fixed caps; the case popover is 828/1104/1344 px tall in a 900/1200/1440 window, was 792/896/896."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: the popovers for cases like the frontier should be taller for larger screens. The case popover (frontier rows, atlas grid, case records) uses more of the window height on tall or large screens instead of a fixed cap, keeping its margins and its own scrolling; measured at 900, 1200 and 1440 px window heights.
