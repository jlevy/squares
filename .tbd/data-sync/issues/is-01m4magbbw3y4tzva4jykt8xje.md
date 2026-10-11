---
type: is
id: is-01m4magbbw3y4tzva4jykt8xje
title: Measure forwarder arrival waits in the published-site audit
kind: task
status: closed
priority: 3
version: 4
spec_path: docs/project/specs/active/plan-2026-10-10-website-development-loop.md
delegate: codex@spud10
labels:
  - ci
dependencies: []
parent_id: is-01m4ke1dkg5m43rszjm49ar77r
hold: null
hold_until: null
created_at: 2026-10-11T01:51:12.763Z
updated_at: 2026-10-11T02:15:33.929Z
started_at: 2026-10-11T02:02:43.852Z
closed_at: 2026-10-11T02:15:33.929Z
close_reason: Implemented and focused controls pass; source frozen for coordinator integration. Exact-head CI and full live-audit recovery remain separate parent work.
resolution: null
duplicate_of: null
---
Independent Astra inspection found forwarder_arrivals documents arrival commitment but uses wait_until=load. After phase timing is available, measure this discrepancy and use commitment waiting if appropriate. Preserve exact destination, query and fragment assertions; a deliberately slow destination should not delay arrival verification. This is a secondary hypothesis, not the cause of the twelve GitHub503 failures. Do not claim a speedup before measuring.

## Notes

Confirmed the documented arrival-commit contract was violated by initial goto(load): an actual rendered forwarder reached the correct query/fragment destination but a held image consumed its two-second timeout (2.375s observed, one captured real Playwright load timeout). Changed only initial goto to commit; exact wait_for_url and URL verdict remain. Final smaller routed-forwarder control completed in 0.317s with zero load timeouts. These are bounded controlled observations, not matched live-audit wall measurements. New regression avoids rebuilding Home/Atlas and the existing all-forwarder check reused canonical preview at 127.0.0.1:8766; together 2 passed in 13.64s, including wrong-destination failure. Scoped Ruff/format and BasedPyright zero findings. No test timeout increased or semantic check removed. Durable red/green receipts: /Users/levy/.codex/visualizations/2026/10/08/01a11dc7-6f9d-7060-be5c-4cff21839702/website-cleanups/audit/.
