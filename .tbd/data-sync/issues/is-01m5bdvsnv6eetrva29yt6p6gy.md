---
type: is
id: is-01m5bdvsnv6eetrva29yt6p6gy
title: "Replay #666's eighteen large certificates (509-1568): the exact routes exceed the 600 s job ceiling"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m5733rrtrvkg93nmregwfe2a
created_at: 2026-10-20T01:12:25.531Z
updated_at: 2026-10-20T01:12:25.531Z
---
The maintained exact routes decide every pair (C(n,2)) and de Winter's #666 certificates carry 80-digit half-angle tangents: the n = 464 positive job took 450 CPU-s (510 s wall) on 20 October 2026, so every count from 509 to 1568 exceeds the kernel's 600 s per-job ceiling (devtools.evand_arrangement_reports.JOB_TIMEOUT), and all nineteen would cost about 34 CPU-h. The #666 import replays 464 and registers the other eighteen beyond-horizon rows from their claims, unreplayed. Options: a sound centre-distance prefilter in both routes (two unit squares whose centres are at least sqrt(2) apart cannot overlap), which makes the pair work linear, reviewed as a verifier change; or a deliberately selected larger ceiling for a priced run. Either needs review before the rows can cite a replay.
