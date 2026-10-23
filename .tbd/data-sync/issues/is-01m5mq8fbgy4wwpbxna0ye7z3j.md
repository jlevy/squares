---
type: is
id: is-01m5mq8fbgy4wwpbxna0ye7z3j
title: "Replay gradec.py on the 233 grade-C configurations: the C3 route of #545's grade-C claim (about 10.6 CPU-hours)"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-23T15:49:48.015Z
updated_at: 2026-10-23T15:49:48.015Z
---
The C3 replay of Evan Daniel's grade-C local-minimality claim (#545, think-7scz): the source's own checker, search/exact/gradec.py at ad86d42 (byte-identical at 31523f8; V-evand-gradec-py), run from its retained copy on all 233 configurations the release's gradec-233.tar.zst certifies, 230 and 261 with GRADEC_DROPZERO=1, each output compared with the published n-N.gradec.json. Priced from the source's logs at 38,026 s, about 10.6 CPU-hours (author's machine, 8 jobs; may be slower here); 154 runs are under a minute (about 21 CPU-minutes), the longest is n = 313 at 1,741 s. Above a lane's 2 CPU-hour single-run limit, so it needs the coordinator's or owner's budget; at most 2 workers on the shared host. Result-import.md Stage 4 accepts the source's checker as the replay without a soundness review; the 23 October review's check_theorem_c.py run (receipts/review-theorem-c-233.jsonl, V-evand-gradec-review-check) is the second route beside the rung, as at T-225 and T-229 (review A1 of PR #751, https://github.com/jlevy/squares/pull/751#issuecomment-6368595518). Waits on: a T-NNN for the claim and a budget.
