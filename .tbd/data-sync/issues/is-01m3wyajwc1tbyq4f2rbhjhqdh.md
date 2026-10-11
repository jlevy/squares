---
type: is
id: is-01m3wyajwc1tbyq4f2rbhjhqdh
title: "Post the replies the import review found owing: 256, 279 to 282, 238, and corrections on 227, 247 and 170"
kind: task
status: closed
priority: 1
version: 8
spec_path: docs/project/specs/active/plan-2026-10-01-result-import-first-application.md
labels:
  - packing
  - result-import
dependencies: []
parent_id: is-01m41csdc2gp36ry5p6n7c2x2y
created_at: 2026-10-01T23:55:49.001Z
updated_at: 2026-10-06T22:27:19.849Z
closed_at: 2026-10-03T18:49:16.670Z
close_reason: null
resolution: null
duplicate_of: null
---
Owner posts, or an agent at the owner request. Drafts are in docs/project/specs/active/plan-2026-10-01-result-import-first-application.md. Every statement was checked against main at f25a85cb5; recheck before posting.

## Replies due on #170 (2026-10-02)

Answer jlevy/squares#170 (wand125, opened 2026-09-14): Four weighted fractional certificates for n = 26, 29, 39, 40, accepted by `sqpack.fractional.certificate.verify`

Replies due, from `python -m devtools.check_requests --report` on 2026-10-02:
- an acknowledgement: nothing has been posted on this issue
- point-ten: T-044 at V3/C3: confirmed, and no reply has said so

Closeable now: yes, with a final comment.
Close condition: Closed by its author on 25 September. A late reply stating T-044 at V3/C3 is owed and keeps it closed.

Sequence: once the pull request holding the ids above is on main, from packing/ on main run `uv run --frozen --all-extras --group dev python -m devtools.check_requests --draft 170`; the owner posts it (or an agent at the owner's request); record the comment's URL, date, kind and reported state under the issue's `replies` in packing/campaign/result-requests.yaml; rerun --report and close the issue with a final comment when it says closeable. Import beads: none yet.

## Notes

2026-10-01: drafts are in docs/project/specs/active/plan-2026-10-01-result-import-first-application.md, section Replies Ready for the Owner, corrected against the audit on #290 (commit e23ce23d2). Nothing is posted. Posting needs the owner's word; recheck every statement against main first, and state no T-066..T-069 before #292 merges.
