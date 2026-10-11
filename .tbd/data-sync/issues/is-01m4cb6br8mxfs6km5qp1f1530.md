---
type: is
id: is-01m4cb6br8mxfs6km5qp1f1530
title: "PR #427 A7 — Medium: historical first-update citation tests now read the second-update cases."
kind: bug
status: closed
priority: 2
version: 3
delegate: codex@17e132e9b179
labels: []
dependencies: []
parent_id: is-01m4cb68shtz5h0braprdqj1qb
hold: null
hold_until: null
created_at: 2026-10-07T23:29:18.600Z
updated_at: 2026-10-08T00:20:40.445Z
started_at: 2026-10-08T00:20:35.228Z
closed_at: 2026-10-08T00:20:40.445Z
close_reason: Source fixes9ff422a/6c615115 at f1d7 are independently reviewed E/F/G/H with0newfindings and hosted final-head CI30SUCCESS26documentedSKIP. Focused379+190+3+11owner checks passed; selected broad assertions completed with original capability failure retained and unchanged supported profiler/heavy completions. Actual broad allowance1800 is unchanged. These source findings are fixed; parent422 intake/confirmation/deployment remain open until atomic stack merge and publication.
resolution: null
duplicate_of: null
---
Review https://github.com/jlevy/squares/pull/427#pullrequestreview-5449633758 head83748.

**A7 — Medium: historical first-update citation tests now read the second-update
cases.** `packing/tests/test_bound_citations.py:583` and `:603` iterate the original
twelve first-update counts but load current case records.
Four suite C failures at n=179 and n=263 expect the first-update source or a matching
T-115 confirmation for what is now a smaller second-update report.
This is a stale test-fixture scope, not evidence that current primary citations should
be reverted or that old confirmations apply to new bounds.

**Fix:** retain the complete historical twelve-count citation regression using explicit
earlier reported and verified inputs reconstructed from the retained first-update
packet. Add separate current second-update assertions that no earlier confirmation is
inherited. Do not drop the two superseded cases from historical coverage or mark their
new reports confirmed.
