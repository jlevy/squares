---
type: is
id: is-01m3xjh0s95sxnbkc0hzyan46k
title: Verification Ladders moves from the Overview to the Results page; Recent Results gains one sentence on what the ratings indicate, pointing to the Results page
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-02T05:48:51.368Z
updated_at: 2026-10-02T07:09:29.709Z
closed_at: 2026-10-02T07:09:29.709Z
close_reason: "Merged in jlevy/squares#304 (7f29897a1, merge 81cb5716): Verification Ladders is the Results page's, under its table; Recent Results has the chips sentence; inbound links and forward.js repointed."
resolution: null
duplicate_of: null
---
Owner, 2026-10-02: 'let's move the Verificaiton Ladders section entirely to the Results page, and then add a line on the New Results seciton mentioning what the verification levels indicate and pointing to the full results page. similar to how we have a sentence mentioning what the red star is'. The section (heading, its prose, the three-column S, V, C ladder diagram) leaves the Overview and becomes part of all-results.html, integrated with that page's own account of the ratings so nothing is said twice. The Overview's Recent Results paragraph gets one sentence, in the manner of the star legend, saying what the S, V and C chips indicate and linking the ladders on the Results page. Every inbound link to #verification-ladders (README's 'verification ratings', nav, cards, papers, epistemics pointers) is repointed; the ladder's layout tests follow the diagram to its new page.

## Notes

2026-10-02 09:30 UTC, branch claude/ladders-to-results at 7f29897a1, draft PR #304 (one PR for think-hqb3, think-wz9d, think-l38m, think-ec5k, one commit each). Done: Verification Ladders is the Results page's, under its table, headed as before with the #verification-at-a-glance anchor; its lead defines S/V/C once with the results-by-others policy; the Results intro points down to it; Recent Results has the chips sentence after the star legend (ceiling 90 -> 125 words); README's verification-ratings link, the Overview statement's link and forward.js (both ladder fragments -> all-results.html) repointed; test_site_ladders and the diagram tests read the Results page; design doc updated. Gates and shots run once on the final head after the other three slices and the merge of origin/main (7a1e92e24).
