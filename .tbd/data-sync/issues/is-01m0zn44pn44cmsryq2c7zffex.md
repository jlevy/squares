---
type: is
id: is-01m0zn44pn44cmsryq2c7zffex
title: Document a reuse basis for the committed Kingbird SVG corpus
kind: bug
status: closed
priority: 1
version: 3
labels:
  - packing
  - pr-45-review
dependencies: []
created_at: 2026-08-26T18:25:38.517Z
updated_at: 2026-08-27T01:32:20.990Z
closed_at: 2026-08-27T01:32:20.989Z
close_reason: The 34 raw Kingbird SVGs are absent from the entire PR-reachable history; attributed numerical facts and a conservative non-legal retention policy remain; strict and final-head CI are green.
resolution: null
duplicate_of: null
---
PR #45 commits 34 complete Kingbird SVG source assets for n<=100, while its prospective policy excludes Kingbird geometry above 100 pending license review. The retained catalogue page and SVGs inspected in the review do not state reuse terms. Before merge, establish and document the permission/license/retention basis that makes the below-100 corpus acceptable, or retain only metadata/derived facts under a reviewed policy. This is a source-governance question, not a conclusion about infringement.

## Notes

Implemented conservatively in the reviewed PR 45 draft candidate: removed all 34 raw Kingbird SVG paths, retained attributed metadata and derived numerical facts only, and documented that this is a retention policy rather than a legal conclusion. Candidate-tree and planned reachable-history checks cover the removed paths. Leave open until fresh strict and CI receipts complete integration.
