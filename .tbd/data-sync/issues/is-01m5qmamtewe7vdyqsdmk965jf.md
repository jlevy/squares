---
type: is
id: is-01m5qmamtewe7vdyqsdmk965jf
title: "PR #795 B2: the report-order gate lets through a tie in time when one claim has no first_committed, and the walk takes it first (intake_ledger.py:643, :1936, :2369)"
kind: bug
status: closed
priority: 1
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m5qmak2fqxxtyp28ye418qxr
created_at: 2026-10-24T18:56:16.717Z
updated_at: 2026-10-24T19:21:23.913Z
closed_at: 2026-10-24T19:21:23.912Z
close_reason: "fixed at bdf789c9b on #795 (14b006d42): the tie gate refuses unless every tied claim has a distinct first_committed; test_a_tie_in_time_with_one_unknown_commit_time_is_refused; dispositions https://github.com/jlevy/squares/pull/795#issuecomment-6388475419"
resolution: null
duplicate_of: null
---
Severity Medium. PR #795, review B: https://github.com/jlevy/squares/pull/795#issuecomment-6388080390. the report-order gate lets through a tie in time when one claim has no first_committed, and the walk takes it first (intake_ledger.py:643, :1936, :2369).
