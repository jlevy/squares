---
type: is
id: is-01m5kj4x05qegkx7pft7sa9w2n
title: "PR #736 A9: the intro's 'in full' wording no longer matches the Results page's seven days"
kind: bug
status: closed
priority: 3
version: 3
delegate: c-addr-736-1023
labels: []
dependencies: []
parent_id: is-01m5khvkc9y6prw31wexsamsc4
hold: null
hold_until: null
created_at: 2026-10-23T05:01:13.605Z
updated_at: 2026-10-23T06:11:31.983Z
started_at: 2026-10-23T05:01:18.890Z
closed_at: 2026-10-23T06:11:31.983Z
close_reason: "Fixed: 79abd064d reworded the intro; after #737 retired the Results page's seven days, 947d28632 points it at All Results (results.html#all-results) and keeps per-day ?added= links. Confirmed by test_home_recent::test_the_section_links_all_results_and_news."
resolution: null
duplicate_of: null
---
Low. packing/devtools/templates/overview-article.md: the intro said the Results page lists the last seven days in full, but Recently Added's window ends on the newest arrival of any kind and the Results page's on its newest result. Review A round 2 of PR #736: https://github.com/jlevy/squares/pull/736#issuecomment-6356372182
