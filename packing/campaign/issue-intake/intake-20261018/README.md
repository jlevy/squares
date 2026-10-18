# Intake Evidence, 18 October 2026

[The audit report](../../../../docs/project/reviews/review-2026-10-18-intake-audit.md)
explains the dispositions and limits.
The workflow is W1 intake under think-xmxb, from main
`804eff369193b698d497a9c06847059eb9de0470`, replacing PR #667’s proposed records.

- `open-issues.json`: raw `gh issue list --repo jlevy/squares --state open --limit 1000
  --json number,title,body,comments,updatedAt,createdAt,labels,author,url`; 68 issues,
  with their bodies and comments.
  No source prose is normalized.
- `issue-dispositions.yaml`: one row per open issue, its recorded scope, owner and
  disposition. Existing claim mapping is preserved; this is not a fresh review of all
  earlier mathematical sources.
- `pr-667.json`: read-only PR metadata, description, comments, files and commits at
  `a5b5f0ec28c1880f53bdc161e5224e282e18eb8a`.
- `432-final-reply.json`: the already posted final reply of 17 October, fetched through
  `gh api repos/jlevy/squares/issues/comments/6237819138`.
- `source-commits.json`: source commit messages and changed paths from GitHub compare
  responses for evand `757b40b..5ca0dc3`, wand125 `fbc5fc4..d7afe3e` and Couzo
  `58a7833..c6da0fc`. Messages are source data, including any statements of approval.
- `claim-inventory.json`: transcribed issue-table sides for the eight new reports and
  #674’s comment. A credit correction has no upper-bound rows.
- `manual-source-receipt.json`: UnitSquare byte comparisons and the SQUISH comment and
  closed-issue timestamps.
  Digests bind remotely fetched bytes to the retained source.
- `sweep-initial.txt`: the initial complete online `make intake` receipt, before owner
  reconciliation. Later sweep and validation receipts accompany the completed audit.

The neighboring [upper-bound ledger](../upper-bounds-20261018/README.md) freezes the
base record and walks 225 claims from ten reports, including #659/#664. It compares
reported sides; it does not run source certificate code or finish the broader source
inventories.

All temporary work and environments belong under the task’s external scratch directory.
These files retain unique evidence and belong in source control.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
