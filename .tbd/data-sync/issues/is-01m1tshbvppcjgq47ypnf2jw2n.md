---
type: is
id: is-01m1tshbvppcjgq47ypnf2jw2n
title: "campaign record: session-087's in-progress workflow deadline has passed, failing the full gate on main"
kind: bug
status: closed
priority: 2
version: 4
labels: []
dependencies: []
created_at: 2026-09-06T07:22:15.797Z
updated_at: 2026-09-06T08:05:14.798Z
closed_at: 2026-09-06T08:05:14.793Z
close_reason: Fixed in PR 94 commit 9c82dc2a. All required CI checks passed in run 34020582886; page build passed in 34020582877. Focused regression tests, final 31-step records gate, both revised negative controls, and n11/n17 package controls passed.
resolution: null
duplicate_of: null
---
packing-validate's 'campaign record' step fails on main at 235bfc50 (run 34017401849, the complete integration surface) and locally on 2026-09-06 with: FAIL session-087-agenda022-continuation.md: in-progress workflow phase 2 deadline_at has passed. The check is time-based: an in-progress session record with a declared phase deadline goes red once the clock passes it, whichever branch is checked out. Close or extend session-087's phase 2 in its record, or give the check a grace rule for records whose session is still open. Not a change of any pull request; the PR surface (--checks) does not run this step.

## Notes

PR 94 review: latest run 34018965403 on 3655bfd1 fails campaign record in the required validate job; contrary to the description, this IS on the PR surface. Local ledger check reproduces. Deadline is compared with HEAD committer date, not current wall time. Disposition expired phase/session with evidence rather than padding deadline.
