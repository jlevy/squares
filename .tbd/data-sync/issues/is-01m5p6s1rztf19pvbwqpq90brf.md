---
type: is
id: is-01m5p6s1rztf19pvbwqpq90brf
title: "PR #770 (merge): senior review"
kind: task
status: in_progress
priority: 2
version: 4
delegate: c-rev-770-1024
labels: []
dependencies: []
parent_id: is-01m5ntqg8kza7vn9e3v650vndr
child_order_hints:
  - is-01m5p8429qc67tp6wdz5y536n0
hold: null
hold_until: null
created_at: 2026-10-24T05:40:14.239Z
updated_at: 2026-10-24T06:03:43.799Z
started_at: 2026-10-24T05:40:18.937Z
---

## Notes

2026-10-24 c-rev-770-1024: Review A (senior, round 1) posted as a PR comment: https://github.com/jlevy/squares/pull/770#issuecomment-6380669495, at head 294fbfc08 (base 2c58b6373). No earlier tbd:review marker on the PR.
Verdict: approve; nothing blocks merge. Fix A1 and A2 before the delivery record is written.
- A1 (Medium): at the head, check_requests --pending gives 48 pending reviews, 5 with no tracking issue: T-234 to T-238, from #750, merged at 49da5d7e0. The PR body says 43 and 0, the S2 coverage omission says every pending review has an issue, and the record index is 126 current, not 121. The stage 7 rule has the pass report the five to the owner.
- A2 (Medium): #773 (T-046), #778 (T-144) and #779 (T-179) credit "Hosono after Tokoharu and Levy", dropping Stromquist, Nagamochi, Burns and Massaccesi from the bibliography's credit line (attribution.md). 30 register claims have the same gap; it predates this PR and needs a bead.
- Low: A3, text nits (ledger :400 Theorem 1.4 window, the think-dgrc price, the release.py:8164 wording); A4, an undated own source wins every tie; A5, a row edited in place is not refused; A6, the stage 7 rule against --pending (holds, closed issues, settled comparisons, asks); A7, Fang's profile prints superseded counts for a current Record (no bead); A8, T-163's declared V2 with its premise gone.
- Verified: k = 15, 68, 69, 76 and 77 by hand, and k = 15 to 400 by my own program, both matching; the tail lemma; Theorem 1.3's best b; the refusal probes; the "credit both" negative control against five mutants; the record-index delta (only T-073, T-080, T-083 and T-084); the nine issues against main's entries, with T-192 stated as V0.
- Tests at 294fbfc08: 111 passed (deficiency_family, profile_records, check_requests); deficiency_family, check_results, check_requests, release_pin, check_release_impact, three records-tier steps, ruff and basedpyright all clean.
- Dedicated reviews: none recommended.
- main moved to c5697c2f2 (#757). merge-tree conflicts in result-requests.yaml and release.py, as expected.
