---
type: is
id: is-01m3ys10dq5xc2gjw4m5dn086t
title: "Answer #309: squarepacker's s(12) >= 31360/7901 (triage first)"
kind: task
status: closed
priority: 2
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m41csdc2gp36ry5p6n7c2x2y
created_at: 2026-10-02T17:01:41.175Z
updated_at: 2026-10-03T18:49:14.544Z
closed_at: 2026-10-03T18:49:14.544Z
close_reason: null
resolution: null
duplicate_of: null
---
Answer jlevy/squares#309 (squarepacker, opened 2026-10-02): New lower bound for s(12): 31360/7901 = 3.969117833… (Daniel's certificate rescaled, reproducible)

Replies due, from `python -m devtools.check_requests --report` on 2026-10-02:
- an acknowledgement, once triage has mapped the claims

Closeable now: no: triage is pending; asked: An independent replay and, if it holds, the n = 12 frontier record updated.
Close condition: Triage has mapped the claim, its register entry is confirmed or refuted, and the reply saying so is posted from main.

Sequence: once the pull request holding the ids above is on main, from packing/ on main run `uv run --frozen --all-extras --group dev python -m devtools.check_requests --draft 309`; the owner posts it (or an agent at the owner's request); record the comment's URL, date, kind and reported state under the issue's `replies` in packing/campaign/result-requests.yaml; rerun --report and close the issue with a final comment when it says closeable. Import beads: none yet.
