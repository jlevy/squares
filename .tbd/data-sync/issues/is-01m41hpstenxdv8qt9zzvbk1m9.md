---
type: is
id: is-01m41hpstenxdv8qt9zzvbk1m9
title: Fetch only main and the PR head in the six full-history CI jobs
kind: task
status: open
priority: 3
version: 4
labels:
  - session-169
  - owner-decision
dependencies: []
parent_id: null
created_at: 2026-10-03T18:51:29.997Z
updated_at: 2026-10-04T01:09:58.204Z
---
Six jobs on every PR push (validate, suite-a to suite-d, frontend) use actions/checkout fetch-depth 0, which fetches refs/heads/* and tags: about 950 MB each, 5.7 GB a push. Fetching main and the PR head only would save about 217 MB a job (about 1.3 GB a push), for cycle time (OR-14), not storage; the jobs need main's history for ancestry and provenance checks, which a two-ref fetch keeps. Owner decision on CI configuration.

## Notes

2026-10-04 01:05 UTC: moved out from under think-gmef to the top level. think-gmef was closed at 00:37 UTC with this bead open, and an open bead under a closed parent fails check_bead_tree (D-025's first invariant) in every pull request's validate job (jlevy/squares#315 at 6c5036895). Kept open as the owner decision it is; re-parent it wherever it belongs.
