---
type: is
id: is-01m5h8j2tryjfnmcxbydkyqmmk
title: "Owner decision: stub copy-back for stat-only files in the mutation-worker snapshot (the structural lever)"
kind: task
status: in_progress
priority: 1
version: 4
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
updated_at: 2026-10-22T16:00:19.542Z
started_at: 2026-10-22T07:35:12.178Z
---
From the 22 October snapshot analysis (c-snapshot-analysis-1022; data in the coordinator scratchpad snapshot-1022/). Growth is about 2.5 MB/day; option-(b) prunes buy about 2 days each. At #720, 100,272,238 bytes in 1,516 non-code, non-Markdown files are only stat-ed by workers; with all 1,516 stubbed to zero bytes the 50-command baseline is unchanged (24 identical, 26 times only). A stub is a third worker state (present but not Git's bytes), so it is in no existing class: the owner decides. Guardrail: a contract test keeps anything a checker loads (e.g. schemas validate_schemas loads) and every control file: target out of the stub set (a first attempt stubbed schemas and crashed validate_schemas). Trend after: about 1.5 MB/day (0.9 with continued pruning). Alternatives: raise the cap (about 0.4 day per MiB); B2 (about 0.95 MB). Recommendation: approve the stub copy-back this week; a modest cap raise is the bridge if it slips.
blocked_on: none

## Notes

2026-10-22 09:30 coord-intake-1021b: the owner merged #578 (d660905ec, 09:14:52Z), which raised SNAPSHOT_MAX_BYTES to 255 MiB (267,386,880) and added about 34 MB, leaving main at 266,509,045 (877,835 headroom). The cap raise is the bridge; the trend (about 2.5 MB/day of intake, more with profile work) is unchanged, so this decision stays open. #721 (prune, about 4.9 MB) is re-taking its evidence on the new main.
blocked_on: none

2026-10-22 16:00 c-lane-snapshot-policy-1022 (for coord-intake-1021b): the owner chose a different plan on 22 October instead of the stub copy-back: reset SNAPSHOT_MAX_BYTES to a coarse 512 MiB and stop raising it per pull request; put keeping bulk out of Git in the per-pull-request added-blob check (#406, devtools.check_added_blobs); and send a certificate or evidence set above OR-18's threshold to hosted data at intake (result-import.md, stage 2). PR #726 (https://github.com/jlevy/squares/pull/726, head ecd6cd598) carries the reset and the intake rule; main 76496462b measures 261,568,999 bytes, so 275,301,913 of headroom. The stub copy-back is not being built. This bead closes when #726 merges.
blocked_on: #726 merge
