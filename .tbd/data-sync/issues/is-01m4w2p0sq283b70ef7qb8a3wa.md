---
type: is
id: is-01m4w2p0sq283b70ef7qb8a3wa
title: Use canonical serialized changelog artifact URLs in publication audit
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
labels: []
dependencies: []
parent_id: is-01m4vns6xeff13savsant84279
created_at: 2026-10-14T02:08:25.394Z
updated_at: 2026-10-14T02:08:25.394Z
---
Candidate senior A1: an artifact fragment containing parentheses is safely percent encoded by the shared renderer but compared raw by check_published_site. Use the same serializer for audit expectations and cover validate-render-audit round trip.
