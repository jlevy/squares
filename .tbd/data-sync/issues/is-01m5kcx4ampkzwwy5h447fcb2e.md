---
type: is
id: is-01m5kcx4ampkzwwy5h447fcb2e
title: "Close settled intake issues as a standard step: closeable issues close at stage 7 after the verified deploy; only record-blocking questions to the reporter keep an issue open"
kind: task
status: in_progress
priority: 1
version: 2
delegate: c-lane-close-issues-1023
labels:
  - process
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-23T03:29:36.084Z
updated_at: 2026-10-23T03:30:24.440Z
started_at: 2026-10-23T03:30:24.440Z
---
Owner, 23 Oct 03:3xZ: 'if we have actually imported something, it's already on the website, and we validated that, we should close the issues. That should be our standard process.' Things that are unresolved, or need the reporter's feedback, stay open. Finding: check_requests already defines closeable (triage done, every result confirmed or refuted, no ask queued), but 12 issues were closeable and open (317, 470, 529, 570, 573, 582, 584, 624, 670, 672, 675, 728): nothing runs the closing step, intake_sweep does not list closeable issues, and lanes kept issues open for informational questions to the author that the record does not track. Fix: (1) a recorded 'awaiting the author' item for questions whose answer would change the record (credit, lineage, which file), which keeps an issue open and which check_requests counts; informational questions go in the closing comment; (2) intake_sweep's Needs Action lists every closeable issue still open; (3) result-import.md stage 7: after the verified deploy, run check_requests --report and close each closeable issue with its final comment; the six-hourly check-in does the same; (4) a closing pass now. #570 is owner-reserved (#557, #565, #570, #574): never close or reply; list for the owner.
