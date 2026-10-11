---
type: is
id: is-01m3ys11k8svw9337p3gsj48rf
title: "Answer #308: Green's DS7 Theorem 9 not established for k >= 4 (after think-abie's triage)"
kind: task
status: closed
priority: 2
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m41csdc2gp36ry5p6n7c2x2y
created_at: 2026-10-02T17:01:42.376Z
updated_at: 2026-10-03T18:49:15.085Z
closed_at: 2026-10-03T18:49:15.084Z
close_reason: null
resolution: null
duplicate_of: null
---
Answer jlevy/squares#308 (wand125, opened 2026-10-02): E-green-ds7-theorem9-reported-lower (DS7 Theorem 9, Green): the published argument does not establish s(k²+1) ≥ G_k for k ≥ 4

Replies due, from `python -m devtools.check_requests --report` on 2026-10-02:
- an acknowledgement, once triage has mapped the claims

Closeable now: no: triage is pending; asked: Record on E-green-ds7-theorem9-reported-lower that the published argument fails for k >= 4, for example in its external_review.
Close condition: Triage has mapped the claim, the record holds the defect against E-green-ds7-theorem9-reported-lower or the report is refuted, and a reply says which.

Sequence: once the pull request holding the ids above is on main, from packing/ on main run `uv run --frozen --all-extras --group dev python -m devtools.check_requests --draft 308`; the owner posts it (or an agent at the owner's request); record the comment's URL, date, kind and reported state under the issue's `replies` in packing/campaign/result-requests.yaml; rerun --report and close the issue with a final comment when it says closeable. Import beads: think-abie, think-r7yt.
