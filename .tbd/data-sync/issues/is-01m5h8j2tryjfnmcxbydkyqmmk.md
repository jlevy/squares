---
type: is
id: is-01m5h8j2tryjfnmcxbydkyqmmk
title: "Owner decision: stub copy-back for stat-only files in the mutation-worker snapshot (the structural lever)"
kind: task
status: in_progress
priority: 1
version: 2
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
delegate: coord-intake-1021b
labels:
  - decision
  - packing
dependencies: []
parent_id: is-01m1sx5m1p5868jhwcdzfkvada
hold: null
hold_until: null
created_at: 2026-10-22T07:35:10.935Z
updated_at: 2026-10-22T07:35:12.179Z
started_at: 2026-10-22T07:35:12.178Z
---
From the 22 October snapshot analysis (c-snapshot-analysis-1022; data in the coordinator scratchpad snapshot-1022/). Growth is about 2.5 MB/day; option-(b) prunes buy about 2 days each. At #720, 100,272,238 bytes in 1,516 non-code, non-Markdown files are only stat-ed by workers; with all 1,516 stubbed to zero bytes the 50-command baseline is unchanged (24 identical, 26 times only). A stub is a third worker state (present but not Git's bytes), so it is in no existing class: the owner decides. Guardrail: a contract test keeps anything a checker loads (e.g. schemas validate_schemas loads) and every control file: target out of the stub set (a first attempt stubbed schemas and crashed validate_schemas). Trend after: about 1.5 MB/day (0.9 with continued pruning). Alternatives: raise the cap (about 0.4 day per MiB); B2 (about 0.95 MB). Recommendation: approve the stub copy-back this week; a modest cap raise is the bridge if it slips.
blocked_on: none
