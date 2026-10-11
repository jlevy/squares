---
type: is
id: is-01m3ys1ddgc8ydwg9vk5bpfrkp
title: "Answer #247: correct the reply's T-058 to T-061 at V3/C3, then close"
kind: task
status: closed
priority: 1
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m41csdc2gp36ry5p6n7c2x2y
created_at: 2026-10-02T17:01:54.480Z
updated_at: 2026-10-03T18:49:12.912Z
closed_at: 2026-10-03T18:49:12.912Z
close_reason: null
resolution: null
duplicate_of: null
---
Answer jlevy/squares#247 (XiaoLiaoShe, opened 2026-09-29): New exact lower bound for s(11): 3.875000003875... with reproducible certificate

Replies due, from `python -m devtools.check_requests --report` on 2026-10-02:
- a follow-up: the reply of 2026-09-30 said the review is linked on the branch claude/determined-goldberg-ura2ed
- a follow-up: the reply of 2026-09-30 said T-061 is the verified lower bound in the n = 11 case record (s(11) is settled by T-060)
- s11: the reply of 2026-09-30 named T-061 as T-058
- s11: the reply of 2026-09-30 stated T-061 at V4/C4, confirmed; it is now V3/C3, confirmed

Closeable now: yes, with a final comment.
Close condition: A correction is posted: the result is T-061, not T-058, at V3/C3, and superseded by T-060. Nothing the authors asked for is then queued; the revised Zenodo record they offered can be retained without the issue open.

Sequence: once the pull request holding the ids above is on main, from packing/ on main run `uv run --frozen --all-extras --group dev python -m devtools.check_requests --draft 247`; the owner posts it (or an agent at the owner's request); record the comment's URL, date, kind and reported state under the issue's `replies` in packing/campaign/result-requests.yaml; rerun --report and close the issue with a final comment when it says closeable. Import beads: none yet.
