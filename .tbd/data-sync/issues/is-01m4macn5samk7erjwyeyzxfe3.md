---
type: is
id: is-01m4macn5samk7erjwyeyzxfe3
title: Deduplicate published-site HTTP requests across URL fragments
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-10-10-website-development-loop.md
labels:
  - ci
dependencies: []
parent_id: is-01m4ke1dkg5m43rszjm49ar77r
created_at: 2026-10-11T01:49:11.736Z
updated_at: 2026-10-11T01:49:11.736Z
---
The deployed-site auditor caches full URLs, repeating network requests for distinct #L anchors to the same resource. Normalize transport/cache identity by removing fragments while retaining query strings and original diagnostic URLs. Preserve every semantic check, registry row and retry contract. Acceptance: different anchors share a request; different queries remain distinct; measure request counts and elapsed time before claiming improvement.
