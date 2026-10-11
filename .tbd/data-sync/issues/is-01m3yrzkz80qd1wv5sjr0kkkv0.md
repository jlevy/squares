---
type: is
id: is-01m3yrzkz80qd1wv5sjr0kkkv0
title: Validate or refute every reported result
kind: epic
status: open
priority: 1
version: 7
labels:
  - result-import
dependencies: []
parent_id: is-01m3yrdxte02c7bnygkke34ct4
child_order_hints:
  - is-01m3yrznz7wy514qfhxwt27pnc
  - is-01m3yrzq6717hg0acsn9bfhgxw
  - is-01m3p04nvawjqqtx8cynyj2pwy
  - is-01m3q3346jb4mfsg5c35w99eyw
  - is-01m3vbf7g19w4t32avqckzqszk
  - is-01m3xew4qbkb7qqr891grbxs7z
created_at: 2026-10-02T17:00:55.656Z
updated_at: 2026-10-02T17:01:12.066Z
---
Every register entry below V3 or C3 on 2026-10-02, each with the bead that finishes it: a child, or a dependency where the bead already lives under think-20pp. Each bead's description says how to finish: the commands, the packet, the expected CPU, what would refute the result, and what moves the rung.

The list is `python -m devtools.check_requests --backlog` from packing/ (the register read live; packing/campaign/result-requests.yaml says which issue each entry serves). An entry leaves it when `devtools.check_results` derives V3/C3, or when a refutation or defect is recorded against it. Done when the backlog holds no result by others without a recorded decision.

T-007 and T-036 are new children; T-058 think-xgjo, T-059 think-11z6, T-064 think-4k80 and T-071 think-fb6h were reparented here; T-046 think-j8f1, T-048 and T-055 think-4r1m, T-067 think-xujq, T-068 think-6ei5, T-069 think-ye2x, T-072 think-09ag and T-073 think-m7cm live under think-20pp and are dependencies. T-067 and T-072 reached V3/C3 on PR #298's branch and leave the backlog when it merges.
