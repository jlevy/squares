---
type: is
id: is-01m1twvvmwym35651k2zg9eq2p
title: "PR #93 validation V1: bind standalone verifier limits to refusal tests"
kind: bug
status: in_progress
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1tve7ex9akeg5842fnbfesr
created_at: 2026-09-06T08:20:25.371Z
updated_at: 2026-09-06T08:21:19.782Z
---
Broad pre-push at c610d308: test_n68_depth_bound_is_named_by_its_refusal_test fails because verify_claim.py MAX_ATOMS/MAX_DIRECTIONS lack scanner-recognized evidence despite dynamic runpy refusal tests. Preserve guard, bind explicit keys to genuine boundary tests. Pre-existing on main.
