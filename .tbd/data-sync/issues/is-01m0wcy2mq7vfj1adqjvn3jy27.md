---
type: is
id: is-01m0wcy2mq7vfj1adqjvn3jy27
title: Repair the split compound adjective in the receipt runbook
kind: bug
status: closed
priority: 3
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
delegate: codex-root
labels: []
dependencies: []
parent_id: is-01m0ty5dqwk4h5rfqkx2bp3kqw
created_at: 2026-08-25T12:04:47.894Z
updated_at: 2026-08-25T12:05:53.068Z
closed_at: 2026-08-25T12:05:53.067Z
close_reason: "Completed before commit: joined replay-relevant, reran pinned Flowmark, and recorded D-301; the runbook diff is now clean."
resolution: null
duplicate_of: null
---
The first uncommitted runbook sentence split replay-relevant after the hyphen, and Flowmark rendered it as replay- relevant. Diff review caught the malformed phrase before commit. Join the compound adjective, rerun Flowmark, and record D-301.
