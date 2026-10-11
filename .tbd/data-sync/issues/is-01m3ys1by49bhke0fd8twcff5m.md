---
type: is
id: is-01m3ys1by49bhke0fd8twcff5m
title: "Answer #256: Daniel's s(60) = 8 and s(61) = 8 (T-062, T-063), then close"
kind: task
status: closed
priority: 1
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m41csdc2gp36ry5p6n7c2x2y
created_at: 2026-10-02T17:01:52.963Z
updated_at: 2026-10-03T18:49:12.378Z
closed_at: 2026-10-03T18:49:12.378Z
close_reason: null
resolution: null
duplicate_of: null
---
Answer jlevy/squares#256 (evand, opened 2026-09-30): Exact value s(60) = 8 (corollary s(61) = 8): registration request (external certificate)

Replies due, from `python -m devtools.check_requests --report` on 2026-10-02:
- an acknowledgement: nothing has been posted on this issue
- s60: T-062 at V3/C3: confirmed, and no reply has said so
- s61: T-063 at V3/C3: confirmed, and no reply has said so

Closeable now: yes, with a final comment.
Close condition: T-062 and T-063 are confirmed, and the reply saying so is posted from main.

Sequence: once the pull request holding the ids above is on main, from packing/ on main run `uv run --frozen --all-extras --group dev python -m devtools.check_requests --draft 256`; the owner posts it (or an agent at the owner's request); record the comment's URL, date, kind and reported state under the issue's `replies` in packing/campaign/result-requests.yaml; rerun --report and close the issue with a final comment when it says closeable. Import beads: think-x73z.
