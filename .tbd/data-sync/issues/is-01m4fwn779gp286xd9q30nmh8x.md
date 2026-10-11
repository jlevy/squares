---
type: is
id: is-01m4fwn779gp286xd9q30nmh8x
title: "Integrate #464 after the research stack lands and restore source-copy headroom"
kind: task
status: closed
priority: 1
version: 5
delegate: claude-code@vm
labels:
  - n-17
dependencies: []
parent_id: is-01m4fhz39j0nmrca9x38tyrnsg
hold: null
hold_until: null
created_at: 2026-10-09T08:32:14.569Z
updated_at: 2026-10-09T10:13:36.708Z
started_at: 2026-10-09T08:32:20.188Z
closed_at: 2026-10-09T10:13:36.708Z
close_reason: "#464 merged to main b96a82c63 with traced prune under 192 MiB"
resolution: null
duplicate_of: null
---
#464 (SOS/global-optimization source review) conflicts with the stack in SYNOPSIS.md and docs/project/document-map.yaml, and folded with everything measures 201,512,362 bytes, 185,770 over the 192 MiB source-copy cap. Main alone is 200,978,830 (347,762 under). Resolve conflicts after #404 lands, restore headroom per the owner's decision (raise or traced option-b prune), qualify, land.

## Notes

2026-10-09T09:46Z Pushed #464 5e8b65d7b (main merge) + 360f7608f (UNREAD_WORKER_OUTPUTS prune, 200,145,032 bytes, 1,181,560 under cap). Review C https://github.com/jlevy/squares/pull/464#pullrequestreview-5468437708: no blocking; numbers re-measured; own strace driver confirms; 132 tests + 174/174 controls. Non-blocking C1-C3 go to follow-up think bead (after landing). CI + deep gate 37911402679 pending.



2026-10-09T10:13Z LANDED #464 at b96a82c63 (head 360f7608f: Packing/Pages/mergeability + deep gate 37911402679 green; Review C no blocking).
