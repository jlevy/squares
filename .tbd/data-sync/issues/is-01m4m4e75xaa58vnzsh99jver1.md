---
type: is
id: is-01m4m4e75xaa58vnzsh99jver1
title: Replace Workbench recency stars with red values
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: workbench_recency_color
labels: []
dependencies: []
parent_id: is-01m4m3qpfthbc1wzc2rvjyy3d8
hold: null
hold_until: null
created_at: 2026-10-11T00:05:11.477Z
updated_at: 2026-10-12T23:39:28.922Z
started_at: 2026-10-11T00:06:54.038Z
closed_at: 2026-10-12T23:39:28.922Z
close_reason: "Delivered in PR #462 (merged 2026-10-11): Workbench recency renders as red case numbers titled 'Recent result', recency symbols removed (13b4f557e, packages/workbench/src/view/facts.ts)."
resolution: null
duplicate_of: null
---

## Notes

Implemented and staged 13 files under packages/workbench. Recency renders as red case numbers with a Recent result title; both recency symbols and the redundant new-result badge are removed. O/= /approx/R, bounds, citations and corpus recency data are preserved. Current Workbench README and layout/candidate checker vocabulary updated; obsolete cross-producer polygon oracle removed, legacy corpus geometry retained. Verified 216 package Node tests (5.87s), 74 layout-oracle tests (0.88s), TypeScript, Biome, retained JS promise lint, Ruff, BasedPyright and real Chromium layout across 7 views and 3 viewports (21 measurements, 1.8s). Source frozen and staged for parent consolidation and final Astra review; no commit/push performed by this agent. Pending existing animation check, local preview publication and exact-head PR CI.
