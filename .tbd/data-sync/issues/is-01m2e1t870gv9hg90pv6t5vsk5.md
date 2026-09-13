---
type: is
id: is-01m2e1t870gv9hg90pv6t5vsk5
title: "R2: reject untyped coordinator and reader invocation identities"
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels: []
dependencies: []
parent_id: is-01m2dzxx9zpj2ft41bs2xbrsec
created_at: 2026-09-13T18:52:29.791Z
updated_at: 2026-09-13T18:52:29.791Z
---
Exact-head verifier review at 878e18d0 found join accepts requested_workers=true when summary and reader proof match. Validate each identity field by exact JSON type and frozen tuple before accepting joined proofs.
