---
type: is
id: is-01m3wx2eq38fknmccejhr309vy
title: "Import ledger: a typed link from a register entry to the issue that asked for it, an answered date, and a generated view of every import and its stage"
kind: feature
status: closed
priority: 1
version: 3
labels:
  - packing
  - result-import
dependencies: []
parent_id: is-01m3nrt5zy2g6dpegq1fbczpzg
created_at: 2026-10-01T23:33:54.018Z
updated_at: 2026-10-10T22:43:27.500Z
closed_at: 2026-10-10T22:43:27.498Z
close_reason: "Request ledger and offline checker landed through merged PR #298. Reconciled under think-p2z4; evidence: tbd show think-rs0t version 2: status=open; https://github.com/jlevy/squares/pull/298 (merged 2026-10-03T17:52:17Z); packing/campaign/result-requests.yaml is present in current history"
resolution: null
duplicate_of: null
---
W7. No field links a result to its request and nothing records that an author was answered: issue 170 has no reference anywhere in the repository and was never answered; issue 256 was registered as T-062/T-063 without a reply. Add an optional request block to a register entry (issue, answered), and devtools.import_ledger to render one row per result by others: status, next move, issue, answered. Offline and deterministic; reading GitHub is a separate dated step.

## Notes

2026-10-02 (lane Q of the result import, branch worktree-agent-a3ee6306dabf4ebe2, stacked on claude/zealous-gauss-jem7l9): built as the inverse join rather than a block in results.yaml, which another lane owns. packing/campaign/result-requests.yaml (schema campaign/schemas/result-requests.schema.yaml) holds one entry per issue: the register and evidence ids each reported result maps to, beads, answer bead, every reply with the state it reported, close condition. devtools.check_requests derives state, reply due and closeable offline (a records-tier gate step), and has --report, --backlog, --draft N (refuses off origin/main) and --github (read-only). Close this bead when that branch merges, unless the owner still wants the per-entry request block.
