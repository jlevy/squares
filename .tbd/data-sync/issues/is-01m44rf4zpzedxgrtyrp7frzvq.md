---
type: is
id: is-01m44rf4zpzedxgrtyrp7frzvq
title: "devtools.intake_sweep: one command that lists every unimported input across sources"
kind: task
status: closed
priority: 1
version: 6
delegate: claude-code@vm
labels:
  - result-import
dependencies:
  - type: blocks
    target: is-01m44rf66ed9fn40rwb0c010gy
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
hold: null
hold_until: null
created_at: 2026-10-05T00:47:22.613Z
updated_at: 2026-10-05T07:19:49.830Z
started_at: 2026-10-05T00:49:41.998Z
closed_at: 2026-10-05T07:19:49.830Z
close_reason: "Done in jlevy/squares#353 / #359 (merged 2026-10-05)"
resolution: null
duplicate_of: null
---
Combine check_requests --github (unread issues/comments), watched repositories whose head is past their newest retained packet pin, the Kingbird recapture diff (diff_kingbird_catalogue) when a new capture exists, pending_catalogue_intake entries with age and owning bead, queued asks; markdown report + nonzero exit when an item lacks a bead.

## Notes

2026-10-05: 57b05f65f adds devtools/intake_sweep.py, devtools/capture_kingbird_catalogue.py, campaign/intake-watch.yaml, check_requests.backlog_rows and page-by-number gh_fetch, make intake. 52c4ddd39 (coordinator's second request) adds Blocked imports (a bead or queued item whose stated blocker merged/closed: think-e6ss/#305), queued results/asks owned only by their own bead, structured pins only, and commits a pin contains that no packet retains (wand125 c56b9b7, 1ebd484). Live sweep 18 s: 29 items without an owner, 8 waits whose blocker resolved. Follow-up think-du1e makes bead required on queued request items after the merge.
