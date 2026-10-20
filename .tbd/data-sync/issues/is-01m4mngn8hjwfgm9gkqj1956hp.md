---
type: is
id: is-01m4mngn8hjwfgm9gkqj1956hp
title: "Decide which edit-tier steps claim .gitignore, lefthook.yml, Cargo and hosted paths (PR #496 F7)"
kind: task
status: closed
priority: 3
version: 2
spec_path: docs/project/specs/active/plan-2026-10-10-website-development-loop.md
labels: []
dependencies: []
parent_id: is-01m4ke1dkg5m43rszjm49ar77r
created_at: 2026-10-11T05:03:37.232Z
updated_at: 2026-10-12T23:38:31.568Z
closed_at: 2026-10-12T23:38:31.568Z
close_reason: "Duplicate of think-7qbv (PR #496 review F7), which PR #507 and the website development-loop plan name as the owner."
resolution: duplicate
duplicate_of: is-01m4mth3pwc0w7mabt4qym2t90
---
Deferred from PR #496 review F, suggestion F7: https://github.com/jlevy/squares/pull/496#pullrequestreview-5481911429
This is a correctness decision, not a speedup: in 10 of the last 40 merges, --push prerequisite scoping fell back to all 65 prerequisites because of an unclaimed path such as .gitignore, lefthook.yml, n17_kernel_verify/Cargo.{lock,toml}, packing/hosted/*.yaml, test fixtures or benchmark data. Claiming a path in a Step's touches decides which steps stop running before a push when that path changes, so each claim needs an attribution argument (which steps read it) and a negative control, in the style of PATTERN_PROBES and test_push_prerequisites_keep_scientific_policy_and_browser_coverage.
Waits on: an attribution audit of those paths against every edit-tier step; review G (correctness) of PR #496 may add evidence.
