---
type: is
id: is-01m3qa5y5c3d51w29cysefsb56
title: Repin atlas data revision after frontier results update
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m3nzy6gqfv60whzzvww0ffa0
created_at: 2026-09-29T19:27:33.034Z
updated_at: 2026-09-29T19:33:33.233Z
closed_at: 2026-09-29T19:33:33.215Z
close_reason: Repinned DATA_REVISION to 81141896a, regenerated the eight atlas outputs, and mapped release.DATA_PATHS into reachable-test import closure with a frontier/results.yaml regression; 44 focused tests, Ruff check/format, sampled atlas check, and exact pin/live comparison pass.
resolution: null
duplicate_of: null
---
Hosted CI at 81141896a fails test_release.py::test_the_pinned_data_revision_is_the_last_data_commit because packing/frontier/results.yaml changed in commit 81141896ae137c77f2a7627b98b22fbef7ad7dd5 while release.py remains pinned to 3dab8e1. Repin DATA_REVISION, regenerate the known-best atlas, and add a targeted reachable-test selector regression for frontier/results.yaml so the change-scoped local gate reaches test_release.
