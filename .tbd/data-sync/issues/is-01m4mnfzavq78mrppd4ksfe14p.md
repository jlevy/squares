---
type: is
id: is-01m4mnfzavq78mrppd4ksfe14p
title: "PR #496 F1: verify-deployment ceiling kills the audit before it prints any verdict"
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-code@spud10
labels: []
dependencies: []
parent_id: is-01m4mneswbxt0m4w1caxy0x320
hold: null
hold_until: null
created_at: 2026-10-11T05:03:14.778Z
updated_at: 2026-10-12T23:39:09.710Z
started_at: 2026-10-11T05:03:44.520Z
closed_at: 2026-10-12T23:39:09.710Z
close_reason: "PR #496 review F1 fixed in PR #507 (merged 2026-10-12): verify-deployment runs the audit with --deadline-minutes 25 under the 30-minute ceiling."
resolution: null
duplicate_of: null
---
Medium. .github/workflows/pages.yml:2245, packing/devtools/check_published_site.py:2040-2043. Job 114313930741 (run 38086162268) ran 58m31s with 79 GitHub 503s; under the 30-minute ceiling it would be cancelled with no verdict list. Fix (coordinator decision): a checker wall deadline below the job ceiling with margin for setup; on expiry stop new work, print collected verdicts, one FAIL naming the phase, the summary, exit 1; best-effort on KeyboardInterrupt; wire through the workflow with a derivation comment; controlled tests. PR #496, review F: https://github.com/jlevy/squares/pull/496#pullrequestreview-5481911429
