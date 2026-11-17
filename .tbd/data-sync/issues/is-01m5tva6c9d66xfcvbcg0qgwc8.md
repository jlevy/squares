---
type: is
id: is-01m5tva6c9d66xfcvbcg0qgwc8
title: "News and result pages: link each entry to the GitHub issues that reported it (40 of 55 News entries and every result page link none)"
kind: task
status: closed
priority: 1
version: 4
delegate: w-newslinks-1026
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-26T00:56:05.257Z
updated_at: 2026-10-26T04:12:46.145Z
started_at: 2026-10-26T00:56:11.627Z
closed_at: 2026-10-26T04:12:46.145Z
close_reason: "Shipped in #820 (85a1919d) and #822 (91831e17). The Pages deploy of 91831e17 (run 40265176001) passed its verify step, which checks News issue links and result-page Issues rows (T-245 → #810). Mobile inline-math fix live."
resolution: null
duplicate_of: null
---
Owner ask of 26 Oct: confirm News renders all changes legibly and links to the issues. Live check at deployed main 2f974835 (check_published_site 5942/5942 pass): 40 of 55 site-changelog entries link no jlevy/squares issue (issue links appear only where a summary mentions #NNN); result pages (result/t-NNN.html) and all-results.html link no issue or PR. Fix: an issues field on site-changelog entries rendered beside pull_requests, backfilled from result-requests.yaml (issue -> reported result ids) for entries with result_ids, a check that holds it, and the reporting issue(s) on each result page. Also: on mobile (390px) the Fitzharding n=19 entry orphans the period after its inline math onto a new line.

## Notes

2026-10-26 ~03:00Z coord-n12-1025: PR #820 (branch claude/friendly-einstein-gf9z0h-news-issue-links, head c62cea31). Issues field + backfill + check, result-page Issues row, mobile News math CSS fix, opening-day rule (no issue opened after an entry's date; #776-#780 removed from earlier entries). Papers measured byte-identical. Hosted CI pending at c62cea31; f2341b95 was green.
