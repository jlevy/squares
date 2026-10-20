---
type: is
id: is-01m4mth3pwc0w7mabt4qym2t90
title: "Decide which prerequisites the commonly unclaimed paths affect (.gitignore, lefthook.yml, Cargo files, hosted YAML) (PR #496 review F7)"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-10-10-website-development-loop.md
labels:
  - packing
dependencies: []
parent_id: is-01m4ke1dkg5m43rszjm49ar77r
created_at: 2026-10-11T06:31:14.907Z
updated_at: 2026-10-11T06:31:14.907Z
---
From PR #496 review F, suggestion F7, deferred by the follow-up PR (think-jjs7). This is an attribution (correctness) decision, not a speedup.
In 10 of the last 40 merges, push-tier prerequisite scoping fell back to all 65 prerequisites because of an unclaimed path such as `.gitignore`, `lefthook.yml`, `n17_kernel_verify/Cargo.{lock,toml}`, `packing/hosted/*.yaml`, test fixtures or benchmark data. For each, decide which edit-tier steps actually read it and claim it in their `Step.touches` (packing/src/sqpack/cli/validate.py), keeping the whole-gate fallback for anything genuinely global. The import-graph contract test added by the follow-up PR covers Python imports only; data and config reads still need this review.
