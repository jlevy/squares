---
type: is
id: is-01m4afz4e7q3jfxprscpf38ab4
title: Prepare reusable Codex cloud development environment
kind: task
status: closed
priority: 2
version: 6
delegate: codex@17e132e9b179
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-07T06:14:15.750Z
updated_at: 2026-10-07T07:45:48.124Z
started_at: 2026-10-07T06:14:24.511Z
closed_at: 2026-10-07T06:45:00.086Z
close_reason: null
resolution: null
duplicate_of: null
---
Install locked Python/Node dependencies, native tools and browser runtime; validate
documented workflow and save onboarding configuration without source edits.

## Notes

Environment provisioned and saved script verified end to end.
Python 3.14.7, Node 24.18.0, Rust 1.98.0, frozen dependencies, pinned Chromium
installed. Codex tbd setup/session hooks and gh 2.97.0, verified gh-stack 0.1.0 plus
pinned skill verified; gh authenticated and repository API read passed.
Rust gates and 212 Node tests passed.
B/C/D shards passed; all A assertions passed but one census remains over 12s call
ceiling (12.97s with 4 workers; 13.44s with 2; isolated 11.43s). Both browser checks
passed, including 98 layout tests.
Saved install/start configuration includes reaper and sandbox memory guidance; tracked
source unchanged. Git proxy still denied bead-sync push; local outbox preserved.
Publication belongs to user.
