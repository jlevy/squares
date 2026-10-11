---
type: is
id: is-01m41hprm9fep7d20thmgfhyd0
title: "Set a policy for bulk retained data: report bytes per PR, move files of 1 MB or more out of git, use xz"
kind: task
status: closed
priority: 2
version: 6
labels:
  - session-169
  - owner-decision
dependencies: []
parent_id: null
created_at: 2026-10-03T18:51:28.776Z
updated_at: 2026-10-10T22:43:23.941Z
closed_at: 2026-10-10T22:43:23.937Z
close_reason: "Close the policy decision: OR-18 and hosted-data handling landed; enforcement remains separately tracked by think-h8d8. Reconciled under think-p2z4; evidence: tbd show think-giqi: notes identify PRs #347 and #349 as the policy answer and think-h8d8 as enforcement; PR #347 merged 2026-10-06: https://github.com/jlevy/squares/pull/347; PR #349 merged 2026-10-05: https://github.com/jlevy/squares/pull/349"
resolution: null
duplicate_of: null
---
Lane D measured 250 MB of the 389 MB added across refs in the week to 3 Oct as gzip certificates, receipts and transfer shards. Proposal: CI reports the packed bytes a PR adds; files of 1 MB or more go to release assets, a data repository or LFS with their digest recorded; new archives use xz. Trade-offs: offline clones lose the data, readers need a fetch, it runs against the self-contained-repository convention, LFS adds quota and CI bandwidth. Owner decision; relates to devtools.retained_data and plan-2026-10-01-release-assets-on-demand.md.

## Notes

2026-10-04 01:05 UTC: moved out from under think-gmef to the top level. think-gmef was closed at 00:37 UTC with this bead open, and an open bead under a closed parent fails check_bead_tree (D-025's first invariant) in every pull request's validate job (jlevy/squares#315 at 6c5036895). Kept open as the owner decision it is; re-parent it wherever it belongs.

2026-10-05 (PR 347 status survey). OR-18 (#345) and devtools.hosted_data (#349) answer the policy; enforcement is think-h8d8. This is an owner-decision bead, so the owner closes it.
