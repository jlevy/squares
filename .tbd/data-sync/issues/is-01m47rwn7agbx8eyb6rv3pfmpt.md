---
type: is
id: is-01m47rwn7agbx8eyb6rv3pfmpt
title: Add Sessions 182 and 183 resource rollups from retained host logs
kind: task
status: open
priority: 2
version: 4
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-06T04:52:28.522Z
updated_at: 2026-10-07T06:23:10.673Z
---
Session 182 (session-182-n17-overnight-lanes) closes stopped with
resource_usage_unmeasured reason rollup_withheld_model_identifiers: its harness and
sub-agent logs exist, but every rollup this repository's contract writes
(ClaudeEfficiencyRollup/v1) keys turns by model identifier, which the agents that ran the
session may not commit. Measured, not committed.

The inputs, on the run container under
/root/.claude/projects/-home-user-squares/ (file names only):

- The coordinator's harness log, 6b1ed85f-ba08-5540-8095-4fd66881916f.jsonl, from
  2026-10-04T05:54Z. It also spans work before the session's start at
  2026-10-05T08:14:04Z, so its rollup is shared, as 913a5de0's is by eleven sessions.
- The 15 sub-agent logs under 6b1ed85f-ba08-5540-8095-4fd66881916f/subagents/ started at
  or after 2026-10-05T08:13:53Z: agent-a0b0e4ddf405acc39.jsonl agent-a3ad468c1d0eaa494.jsonl agent-a4c8fa035f1ffcdfe.jsonl agent-a53bf696b86d675e4.jsonl agent-a5876044abe43c05d.jsonl agent-a76f70717495baf45.jsonl agent-a819f6f47909bde6a.jsonl agent-a9984cf91e54e97ec.jsonl agent-aa7f27534be946dec.jsonl agent-ab2288a20d80178d9.jsonl agent-ab708fe86a4d2a573.jsonl agent-ac87a45cbae726fa6.jsonl agent-acf4d10a9500316cf.jsonl agent-af38a7dfb4a15a2aa.jsonl agent-af521cc6fd2b8c3aa.jsonl 
- Excluded: agent-af4f5ec641151fc81.jsonl and agent-ab6ed7d52f8584026.jsonl, which
  started at 2026-10-05T04:46Z, before the session, and ran into its window.

To discharge (owner): from packing/, run
`uv run --frozen --all-extras --group dev python -m devtools.close_session --update --session session-182 --log <harness log> --agent-logs <the 15 logs>`,
set the session's resource_rollups to the written receipts, remove
resource_usage_unmeasured, then run `close_session --render` and
`packing-ledger render`. The logs exist only on that container.

## Notes

Also covers Session 183 (session-183-n17-draw-31, PR #385), which closes stopped with resource_usage_unmeasured reason rollup_withheld_model_identifiers for the same cause. Its inputs on the run container under /root/.claude/projects/-home-user-squares/: the harness log 6b1ed85f-ba08-5540-8095-4fd66881916f.jsonl and the run operator's sub-agent log subagents/agent-a3c879fa91b776b5e.jsonl (started 2026-10-06T15:52Z).
