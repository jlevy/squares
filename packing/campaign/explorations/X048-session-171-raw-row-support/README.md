# Session 171: lazy raw-row support

[D1 report](d1-report.md) records the frozen diagnostic, limits and controls.
D1 freshly replayed (same implementation, no search) support for **55 of 96 rows**; 41
remain unresolved after the 100,000-node ceiling.
No unsupported row or exclusion was claimed.

[Result summary](receipts/D1_result-summary.json) links counts and resource evidence.
[B support packet](receipts/D1_B-support-packet.json) and
[fresh replay](receipts/D1_B-independent-replay.json) retain the witnesses.

These are solutions of the frozen binary constraint network, not geometric packings.
Any further search protocol requires separate preregistration.

[D2 report](d2-report.md) records the separately frozen forward-checking/MRV trial:
69/96 rows supported by fresh replay (+14), 27 unresolved at the unchanged pair ceiling.

Commits cited in this record that are not in this branch’s history resolve at the tag
`archive/guzhou-review-a-333` (Guzhou’s original nine-session branch); those from PR 307
and PR 325 also resolve at `refs/pull/325/head`. The references are provenance only; no
code reads them (`OR-18`). “Fresh replay” here means the same implementation re-run in a
separate process without search; receipt names ending in `-independent-replay.json`
predate that wording.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
