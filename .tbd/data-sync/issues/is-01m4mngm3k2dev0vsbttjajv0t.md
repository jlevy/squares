---
type: is
id: is-01m4mngm3k2dev0vsbttjajv0t
title: "Handle GitHub repository-link checks at the host level in the live audit (PR #496 F6)"
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/specs/active/plan-2026-10-10-website-development-loop.md
labels: []
dependencies: []
parent_id: is-01m4ke1dkg5m43rszjm49ar77r
created_at: 2026-10-11T05:03:36.050Z
updated_at: 2026-10-11T05:03:36.050Z
---
Deferred from PR #496 review F, suggestion F6 (pre-existing, design): https://github.com/jlevy/squares/pull/496#pullrequestreview-5481911429
In the complete local audit of deployed 6038af33 the repository-links phase took 252.18 s of 511.65 s: 357 sequential HEADs to github.com at about 0.71 s each. Every failure in the three failing hosted audits was a github.com 503 (12, 25 and 79). Per-URL retries at 2, 4, 8 and 16 s during a host-wide throttle add about 40 s per link and did not recover them.
Options: per-host backoff, or stop after K consecutive 503s and mark the rest unverified; honor Retry-After; or answer blob/<ref>/<path> existence from the checked-out history and keep a small live sample. The progress and retry lines PR #496 added will show how often a retry actually recovers; use them as the evidence.
Waits on: retry-recovery evidence from the progress lines of future hosted audits, and a decision on what an 'unverified' link verdict means.
