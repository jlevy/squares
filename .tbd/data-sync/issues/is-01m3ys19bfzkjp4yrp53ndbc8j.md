---
type: is
id: is-01m3ys19bfzkjp4yrp53ndbc8j
title: "Answer #280: wand125's s(59) = 8 (T-066), then close"
kind: task
status: closed
priority: 1
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m41csdc2gp36ry5p6n7c2x2y
created_at: 2026-10-02T17:01:50.319Z
updated_at: 2026-10-03T18:49:11.249Z
closed_at: 2026-10-03T18:49:11.249Z
close_reason: null
resolution: null
duplicate_of: null
---
Answer jlevy/squares#280 (wand125, opened 2026-10-01): Exact value s(59) = 8 (k = 8 of the k² − 5 series): registration request (external certificate)

Replies due, from `python -m devtools.check_requests --report` on 2026-10-02:
- an acknowledgement: nothing has been posted on this issue
- s59: T-066 at V3/C3: confirmed, and no reply has said so

Closeable now: yes, with a final comment.
Close condition: T-066 is confirmed, and the reply saying so is posted from main.

Sequence: once the pull request holding the ids above is on main, from packing/ on main run `uv run --frozen --all-extras --group dev python -m devtools.check_requests --draft 280`; the owner posts it (or an agent at the owner's request); record the comment's URL, date, kind and reported state under the issue's `replies` in packing/campaign/result-requests.yaml; rerun --report and close the issue with a final comment when it says closeable. Import beads: think-oy3i.
