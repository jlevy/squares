---
type: is
id: is-01m4x4c32d5wdje51ep66pbzmm
title: Remove cold atlas construction duplication under the enforced call ceiling
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
child_order_hints:
  - is-01m4xdss3rj8a0z06den667k65
hold: null
hold_until: null
created_at: 2026-10-14T11:57:11.614Z
updated_at: 2026-10-14T14:41:57.367Z
started_at: 2026-10-14T11:58:08.702Z
---
Actual PR599 complete run38555598547 head472 canonical atlas call25.205s, observed CPU lower bound23.02s; lazy fixture correctly charges first construction but production cost remains. Profile and remove repeated renderer work while preserving all324cells, both variants, admission/credit/recency/links, validated-metadata trust and complete semantic assertions. Keep12s ceiling/markers and measured first construction. No unmeasured eager fixtures.
