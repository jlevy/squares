---
type: is
id: is-01m3w4rzag8w6087gtbgx38ypy
title: "Project documentation cards: review RESULTS.md, STATUS.md and SYNOPSIS.md; drop defects.md; README and epistemics first"
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T16:29:17.519Z
updated_at: 2026-10-01T19:05:21.018Z
closed_at: 2026-10-01T19:05:21.016Z
close_reason: "Merged into jlevy/squares#276 (8994befae): README and epistemics lead the cards; RESULTS, STATUS and defects pages leave the site with forwarders; review at docs/project/reviews/review-2026-10-01-site-documentation-records.md. Owner follow-ups: keep generating RESULTS.md and STATUS.md (recommended); seven drifted narrative passages of SYNOPSIS.md; two stale README sentences (lines 111-117)."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: 'on the Squares Project Documentation, lets review if we still should have results.md and status.md still. are they even maintained? probably remove here unless they play a key role. we may even wish to see if they are subsumed fully by our other records now or if they are a good internal summary. we should check if synopsis.md is properly maintained. we don't need to link to defects.md from this site it can be internal to the github repo. the readme.md and epistemics.md should be the first two and are most important.' A separate agent devoted to the internal records and the links to them: for each document the site's documentation section lists, establish how it is produced (hand-written, generated, generated blocks), by what and when it was last really updated, what checks hold it current, what it duplicates (the Results page, the Frontier page, the case records), who links to it; recommend keep on site / keep in repository only / retire; then reorder (README, epistemics first), remove defects.md and whatever the review retires from the site, and clean up every link to a removed page (site pages, reader documents, forwarders, SITE_PAGES, check_published_site).

## Notes

2026-10-01, branch claude/site-docs-records at 8994befae (7 commits on origin/main 3e5322f93; not pushed, no PR; coordinator integrates). Review: docs/project/reviews/review-2026-10-01-site-documentation-records.md. Findings: RESULTS.md and STATUS.md are generated, current and gate-held; the results table and frontier atlas show all but four things (lineage headings, replay-queue order, register review date; per-case review date), so both leave the site and stay in the repository, still generated. SYNOPSIS.md: 31 statements checked at fe6399451, 12 current, 17 stale, 2 wrong, all drift in unchecked prose; main's PR 274 fixed 8, this branch 4 (n<=100 -> 324 three times, corpus counts, s(13)=4 Lean check); 7 narrative ones left for the owner, listed in the review. Site: cards now README, epistemics, SYNOPSIS, conventions, development; results.html -> all-results.html, status.html -> frontier.html, defects.html -> defects.md on GitHub, each a forwarder with a no-script refresh (render_overview.MOVED_PAGES, templates/site-forwarder.html, forward.js data-moved-to); links to RESULTS.md/STATUS.md/case files in reader documents and case records now lead to the site's pages. Gates on the merged tree: --records 38/38 selected steps, --edit 53/53, focused pytest 779 passed 3 skipped, node forwarder 7/7. Open for the owner: the narrative rewrites in SYNOPSIS.md and README lines 111-117; whether to repoint the two papers' RESULTS.md links at the results table once the papers move settles. Merge note: the paper-slugs branch builds the same forwarder mechanism (MOVED_PAGES, forwarder_pages, site-forwarder.html, forward.js); union the table entries and keep FORWARDER_TITLES for non-paper targets.
