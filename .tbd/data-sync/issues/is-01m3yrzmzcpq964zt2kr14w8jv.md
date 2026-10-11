---
type: is
id: is-01m3yrzmzcpq964zt2kr14w8jv
title: Answer every result report
kind: epic
status: open
priority: 1
version: 14
labels:
  - result-import
dependencies: []
parent_id: is-01m3yrdxte02c7bnygkke34ct4
child_order_hints:
  - is-01m3ys10dq5xc2gjw4m5dn086t
  - is-01m3ys11k8svw9337p3gsj48rf
  - is-01m3ys13d4m4f3nsy0mq964m19
  - is-01m3ys14zf9kaxrjz44ksfrhmd
  - is-01m3ys167s43cwbqecd86pvw5k
  - is-01m3ys17qmmqsa0pby2rg6x2hk
  - is-01m3ys19bfzkjp4yrp53ndbc8j
  - is-01m3ys1amqty0xqzyhx0avfssz
  - is-01m3ys1by49bhke0fd8twcff5m
  - is-01m3ys1ddgc8ydwg9vk5bpfrkp
  - is-01m3ys1eyvhd71mxr5nec8w8rs
  - is-01m3ys1fz0a6qc5j6vny00wb2p
created_at: 2026-10-02T17:00:56.683Z
updated_at: 2026-10-06T22:27:23.174Z
---
One bead per open result report on jlevy/squares (and think-75yv for the closed #170), each naming the replies due and the close condition. The record is packing/campaign/result-requests.yaml; `python -m devtools.check_requests --report` from packing/ derives what each issue is owed from it and the register.

The sequence after each merge (campaign/result-import.md, stage 7): on main, `python -m devtools.check_requests --draft N` renders the status comment (it refuses off main, since a T-NNN is provisional until merged); the owner posts it, or an agent at the owner's request; the comment URL, date, kind and the state it reported go into the issue's `replies`; the issue is closed with a final comment when --report says closeable. `--github` lists any reply or comment the record has not taken in.

think-bmze (#295) and think-75yv (#170, and the drafts of 1 October) live under think-20pp and are dependencies.

## Notes

2026-10-06: stale blockers think-75yv and think-bmze (both closed) removed. Open replies: #282 (T-082, after lane R4 merges), #368 (v1.2, think-gcft), #317 (Lean import, after the citation follow-up), and the n = 17 items held under think-x4v4.
