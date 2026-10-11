---
type: is
id: is-01m4mth36y8c6m269nh0wpk3g6
title: "Handle github.com link checks at the host level in the published-site audit (PR #496 review F6)"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-10-10-website-development-loop.md
labels:
  - packing
dependencies: []
parent_id: is-01m4ke1dkg5m43rszjm49ar77r
created_at: 2026-10-11T06:31:14.397Z
updated_at: 2026-10-11T06:31:14.397Z
---
From PR #496 review F, suggestion F6, deferred by the follow-up PR (think-jjs7).
In the live receipt the repository-links phase took 252.18 s of a 511.65 s audit: 357 sequential HEADs to github.com at ~0.71 s each. Every failure in the three failing hosted audits was a github.com 503 (12, 25, 79). Retrying one URL at 2/4/8/16 s during a host-wide throttle adds ~40 s per link and did not recover them; with the new 25-minute checker deadline (follow-up PR) a throttle now ends the audit early with partial verdicts instead.
Options: per-host backoff, or stop after K consecutive 503s and mark the rest unverified; honour Retry-After; or answer blob/<ref>/<path> existence from checked-out history and keep a small live sample. Use the progress lines (retries per phase) to measure how often a retry recovers before choosing.
