---
type: is
id: is-01m21fpzqxsqhpkc2x3wnxx83a
title: PR rollups key on the agent's logged branch, so an agent-built branch can never render its own cost block
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-08T21:45:15.258Z
updated_at: 2026-09-08T21:45:15.258Z
---
Third occurrence: PRs #119, #128 and #134 each spent a paragraph explaining why `devtools.close_session --render` and `devtools.render_pr_rollup --branch <branch>` answer 'No rollup records any turn on <branch>' and hand-counted the OR-9 cost block instead.

The mechanism, from PR #134's block: an agent spawned from a parent session records the parent's branch (`claude/kpress-pt-serif-fonts-1ec7e6`) in its own log, while the work lands on the branch the PR is opened from (`claude/adopt-planetaire`). `turns.by_branch` is the only branch-aware field in the record (`packing/devtools/render_pr_rollup.py`), so the branch the reviewer asks about matches nothing, and the parent's branch aggregates sessions of unrelated earlier work that cannot be subtracted.

Three occurrences is a tooling defect rather than a per-PR footnote. The fix is to key the rollup on the branch the work actually landed on -- the checked-out branch at session close, or an explicit `--branch` that maps onto the log's turns rather than requiring the log to have recorded that name -- so the fourth such PR generates its block instead of counting it by hand.

Raised by the senior engineering review of PR #134 (the OR-9 section).
