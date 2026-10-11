---
type: is
id: is-01m3razc6hwms10f04btg028vv
title: Consolidate evidence storage without losing replay or review history
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies:
  - type: blocks
    target: is-01m3rb0t4zqdze43drjkx9cqx2
parent_id: is-01m3ra1hjvn4bdh3h13aggqgvb
created_at: 2026-09-30T05:00:41.040Z
updated_at: 2026-09-30T05:04:27.438Z
---
Inventory all consumers before migrating duplicate stdout/results, large JSON and session logs. Preserve exact decoded bytes and source-bound historical executions; archive unique failed/incomplete evidence. Use deterministic gzip plus concise summary and a small shared bounded reader only where needed. Validate links, pinned identities, negative corruption controls and old-to-new byte equality. Do not block remaining proof geometry on this cleanup.
