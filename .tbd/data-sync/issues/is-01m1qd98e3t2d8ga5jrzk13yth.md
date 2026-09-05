---
type: is
id: is-01m1qd98e3t2d8ga5jrzk13yth
title: Upgrade flowmark-rs to 0.4.0 and re-measure the archive exclusion
kind: chore
status: closed
priority: 2
version: 2
labels:
  - tooling
dependencies: []
created_at: 2026-09-04T23:50:23.923Z
updated_at: 2026-09-04T23:50:24.719Z
closed_at: 2026-09-04T23:50:24.717Z
close_reason: Commit cc971b01.
resolution: null
duplicate_of: null
---
First-party release, exempt from the cool-off. 0.4.0 keeps math spans whole: 0 of 7,618 spans broken across 18 transcriptions against 605 under 0.3.2, with the 2026-08-22 figures reproduced exactly. The archive exclusion stays for the .raw.md ground truth and for not editing transcribed characters; AGENTS.md says so.
