---
type: is
id: is-01m3yspaa1c7e1zr6y0tkz72y0
title: "Overview: the Frontier Survey card stands alone at the top of the page cards, which run in lines of one, two and two"
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-02T17:13:19.424Z
updated_at: 2026-10-02T22:41:20.941Z
closed_at: 2026-10-02T22:41:20.941Z
close_reason: "Merged in jlevy/squares#310 (46ea721e6): the page cards run one, two and two, the Frontier card first."
resolution: null
duplicate_of: null
---
Owner, 2026-10-02: 'also let's move the Frontier survey card to a place of its own right at the top, so it is 5 cards in pattern 1, 2, 2 per row'. Follows think-ec5k (#306), which set the page cards two over three with the Frontier card last. The Frontier page's card moves first in PAGES and SECTION_CARD_LINES becomes {pages: (1, 2, 2)}: the Frontier card alone, then the two papers, then the tutorial and the workbench, every line at the width of two to a line (the longest line). Tests, paper-design.md (Card sizes, Overview sections) and shots at 1280 and 390 follow.

## Notes

2026-10-02: committed 46ea721e6: Frontier card first, lines (1, 2, 2), half-width cards; Overview tests 271 passed; shots at 1280 checked. PR jlevy/squares#310 opened 2026-10-02 (head 38346bf4a); close when it merges.
