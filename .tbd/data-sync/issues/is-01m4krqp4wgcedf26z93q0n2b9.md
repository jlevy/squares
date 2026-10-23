---
type: is
id: is-01m4krqp4wgcedf26z93q0n2b9
title: "intake_sweep: say a pinned read can be removed only when removing it leaves nothing unretained"
kind: bug
status: closed
priority: 3
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T20:40:38.812Z
updated_at: 2026-10-23T06:12:22.161Z
closed_at: 2026-10-23T06:12:22.161Z
close_reason: "Tracker audit 2026-10-23 (c-audit-a-1023, think-s4ld), checked by coord-intake-1023: SUPERSEDED/DUPLICATE. 4dd74cf17 'fix(intake): a read through a pinned head goes only when nothing it covers is left unretained' on main; intake_sweep._pinned_read_note"
resolution: null
duplicate_of: null
---
intake_sweep's repositories_section prints "a packet now pins <head>, so intake-watch.yaml's read of it can be removed" for any read at a pinned head without checking whether _unretained still needs that read. On 2026-10-10 lane L26 measured franciscouzo/square-packing: removing the 3ef7634 read (which the #488 packet pins) turns 3ef7634 into a Needs Action item, because the read is what covers 65 SVGs across 02f9690 and 3ef7634 and the 102/103/272 pose files and SVGs 9bf90e7 deletes, which no packet retains. The note cannot be cleared without making the sweep's result worse.

Fix: emit the note only when removing the read leaves the unretained list unchanged; add a test with a pinned head whose read still covers unretained paths. File: packing/devtools/intake_sweep.py (repositories_section, _unretained); tests in packing/tests/test_intake_sweep.py.
