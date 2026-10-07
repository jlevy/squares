---
type: is
id: is-01m47sgmearcg58z4fbatsxayk
title: Certify Session 182's handover with a qualifying gate
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-06T05:03:23.082Z
updated_at: 2026-10-07T06:23:10.673Z
closed_at: 2026-10-06T17:33:57.244Z
close_reason: "Merged in jlevy/squares#384 (stack #386) on 2026-10-06."
resolution: null
duplicate_of: null
---
Session 182 (session-182-n17-overnight-lanes) closes stopped with certification_pending:
no qualifying gate ran on its handed-over source inside the finalization reserve.

Why: on the run container, with BC-428's two kernel workers still running, a timed
`packing-validate --fast` trial on fc9774dcb was still going when its 900 s timeout
stopped it (exit 124), against the fast tier's 600 s ceiling, so a run started by 07:40
UTC could not be relied on to finish before 08:10 UTC, ahead of the 08:14:04 UTC session
deadline. The full tier (3,600 s ceiling) fits even less.

To discharge: run `packing-validate --fast` (or the full gate) at or after the session's
close commit on claude/n17-session-182-continued, or rely on a hosted fast run of that
head. Then replace certification_pending with the canonical
`full gate: fast at <sha>: passed` line in the session's checks.

## Notes

2026-10-06: addressed on jlevy/squares#384 (claude/n17-session-certification, 7c4f758f5 and 6f635886d); closes when #384 merges.
