---
type: is
id: is-01m0zn44pn44cmsryq2c7zffex
title: Document a reuse basis for the committed Kingbird SVG corpus
kind: bug
status: open
priority: 1
version: 2
labels:
  - packing
  - pr-45-review
dependencies: []
created_at: 2026-08-26T18:25:38.517Z
updated_at: 2026-08-26T23:19:46.861Z
---
PR #45 commits 34 complete Kingbird SVG source assets for n<=100, while its prospective policy excludes Kingbird geometry above 100 pending license review. The retained catalogue page and SVGs inspected in the review do not state reuse terms. Before merge, establish and document the permission/license/retention basis that makes the below-100 corpus acceptable, or retain only metadata/derived facts under a reviewed policy. This is a source-governance question, not a conclusion about infringement.

## Notes

Implemented conservatively in the reviewed PR 45 draft candidate: removed all 34 raw Kingbird SVG paths, retained attributed metadata and derived numerical facts only, and documented that this is a retention policy rather than a legal conclusion. Candidate-tree and planned reachable-history checks cover the removed paths. Leave open until fresh strict and CI receipts complete integration.
