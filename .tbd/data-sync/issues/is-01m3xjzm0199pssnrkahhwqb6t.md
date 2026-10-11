---
type: is
id: is-01m3xjzm0199pssnrkahhwqb6t
title: "Overview: drop The Frontier Survey section; one Frontier Survey card joins the page cards under The Squares Project, and those cards sit in two rows"
kind: task
status: closed
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
child_order_hints:
  - is-01m3yrqjwzmyheqrc7wecfhrxq
created_at: 2026-10-02T05:56:49.792Z
updated_at: 2026-10-02T16:56:32.407Z
closed_at: 2026-10-02T16:27:37.864Z
close_reason: "Merged in jlevy/squares#306 (322ef34cd and 7b1142497): The Frontier Survey section is gone from the Overview, its card to every case is the fifth page card, and the page cards stand two over three; forward.js sends the section's two fragments to frontier.html."
resolution: null
duplicate_of: null
---
Owner, 2026-10-02: 'and drop the whole section: The Frontier Survey — The frontier survey is the record the atlas is drawn from: … when a bound by others counts as verified. — and then move one Frontier Survey card to the top below The Squares Project headers, and put the cards into two rows instead of one'. The Overview loses The Frontier Survey heading, its paragraph and its two cards (added in #299). One Frontier Survey card (the one to the Frontier page, every case from n = 1 to 324) joins the page cards under The Squares Project (today four: the optimality paper, the explainer, the tutorial, the workbench), and that group is laid out in two rows instead of one. Every inbound link to the Overview's #the-frontier-survey (README, other pages) is repointed to the Frontier page.

## Notes

2026-10-02 07:50 UTC: PR jlevy/squares#306 open, green and mergeable at 7b1142497 (322ef34cd this bead; 7b1142497 the Frontier math-face test's leftover from wz9d and the card-lines refusal through page_cards). The Frontier Survey section, its paragraph and two cards are gone; the card to every case is the fifth page card; the page cards stand two over three (SECTION_CARD_LINES = {pages: (2, 3)}), chosen over three over two from shots at 1280; forward.js sends #the-frontier-survey and #the-survey to frontier.html; README, epistemics.md and paper-design.md updated. Local push tier at 7b1142497: type floor clean, 3762 passed, 2 failed (fixed_core_packet reaping tests, sandbox-only; hosted suite-d passes them). Hosted CI all green. Close when #306 merges.
