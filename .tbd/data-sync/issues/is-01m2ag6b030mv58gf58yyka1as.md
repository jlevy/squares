---
type: is
id: is-01m2ag6b030mv58gf58yyka1as
title: Reconcile the BC329 runner source lock with the published T-026 claim
kind: bug
status: in_progress
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m2aj2ewckram8ww4458w74hr
  - type: blocks
    target: is-01m2aj7q4y8raaw35s0jq3ty2y
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T09:46:48.180Z
updated_at: 2026-09-12T10:43:13.081Z
---
The unfinished fixed_core_packet.py pins T-026 blob e12789cd with SHA fe786eff, while PR148 head 989fd544 carries the published T-026 limit blob baeb8c43 with SHA 04fd6bbc. The observed artifact diff is endpoint_status prose; mathematical fields and the T-025 input appear unchanged. Rebase the runner onto the publication stack, independently compare every consumed mathematical field, update the source/revision lock deliberately, and retain refusal controls for unexpected source drift. Port only the WIP plan/preflight additions: the old worktree also reintroduces the corrected-away phrase weak limit and points retention at the old CLI. Preserve PR148's direct statement that T-026 proves the ordinary exact lower bound s(11)>=C, while keeping the separate strict-inequality question distinct, and point the run protocol at the admitted fixed-core runner. Leave a clean committed branch. Do not weaken source binding and do not register or run BC329 until this and the parent admission are complete.

## Notes

Root rechecked the clean PR149-based stack against the published sources. T025 is blob 684a6b7adf4524691a4fb996fa3625d909d171ac, SHA-256 3935651af614eb3e9a1926179925f98643beb17ed1764a323fe83a527f4bad5c, 673639 bytes. T026 is blob baeb8c4329cebf783ebe3546a9400710664ef317, SHA-256 04fd6bbca1941671ddbabbe359219011b8217818b0a291f4c9a00f5fa7834f8e, 3965 bytes. The runner constants match. Its T026 comparison reads the exact bounded-side square from the strict JSON record. Closure admission still requires committing the runner, proving discover_implementation_paths contains every runtime module, and exercising source_manifest against that exact clean revision before this bead can close.
