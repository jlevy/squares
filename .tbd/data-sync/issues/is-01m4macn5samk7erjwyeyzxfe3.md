---
type: is
id: is-01m4macn5samk7erjwyeyzxfe3
title: Deduplicate published-site HTTP requests across URL fragments
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-10-website-development-loop.md
delegate: codex@spud10
labels:
  - ci
dependencies: []
parent_id: is-01m4ke1dkg5m43rszjm49ar77r
hold: null
hold_until: null
created_at: 2026-10-11T01:49:11.736Z
updated_at: 2026-10-11T02:15:33.908Z
started_at: 2026-10-11T02:02:43.758Z
closed_at: 2026-10-11T02:15:33.886Z
close_reason: Implemented and focused controls pass; source frozen for coordinator integration. Exact-head CI and full live-audit recovery remain separate parent work.
resolution: null
duplicate_of: null
---
The deployed-site auditor caches full URLs, repeating network requests for distinct #L anchors to the same resource. Normalize transport/cache identity by removing fragments while retaining query strings and original diagnostic URLs. Preserve every semantic check, registry row and retry contract. Acceptance: different anchors share a request; different queries remain distinct; measure request counts and elapsed time before claiming improvement.

## Notes

Implemented in check_published_site.py: fragment-free transport/cache identity, query distinction, GET-to-HEAD reuse, separate HEAD-to-GET fetch, and unchanged original per-link diagnostics. Regression was red before normalization; final test also proves cached 404/503 responses remain failures. Full checker module: 104 passed in 81.89s. Scoped Ruff/format and BasedPyright: zero findings. Retained main run38101925790 log contains 359 distinct repository-link verdict URLs and 357 fragment-free HTTP identities: two prospective requests saved (0.6%), not a measured network-wall improvement. Historical 170-anchor source comment was removed; historical evidence remains in ht59. Source frozen for root integration; no commit or GitHub mutation by this worker. Durable receipts: /Users/levy/.codex/visualizations/2026/10/08/01a11dc7-6f9d-7060-be5c-4cff21839702/website-cleanups/audit/.
