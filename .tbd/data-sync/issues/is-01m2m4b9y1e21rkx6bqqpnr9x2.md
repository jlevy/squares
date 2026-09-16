---
type: is
id: is-01m2m4b9y1e21rkx6bqqpnr9x2
title: "PR #175 review R4: the ESLint promise floor runs over a hand-kept directory list"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T03:32:12.352Z
updated_at: 2026-09-16T04:10:14.001Z
closed_at: 2026-09-16T04:10:14.001Z
close_reason: "Fixed on PR #175 in commit 0ab75b7c, each with a check watched failing on the pre-fix source first."
resolution: null
duplicate_of: null
---
packing/src/sqpack/cli/validate.py:1536-1541. Biome uses **/*.js, tsconfig uses a glob, check_probes walks; ESLint names seven directories by hand. Also raised as #179 R3. Fix: derive from check_probes.probe_trees() plus the fixed roots, or a contract test. (PR #175, review 5218208204)
