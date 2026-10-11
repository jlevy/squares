---
type: is
id: is-01m4eyv4t9xeyna4bxqpr11c76
title: Publish an About page for The Squares Project
kind: feature
status: closed
priority: 1
version: 10
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10.local
labels:
  - website
dependencies:
  - type: blocks
    target: is-01m4ex3c459d9jrd6mds18ftqg
  - type: blocks
    target: is-01m4ex3gpzxxh9eqemc2r78p4e
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-08T23:51:11.432Z
updated_at: 2026-10-10T18:55:57.069Z
started_at: 2026-10-08T23:52:39.031Z
closed_at: 2026-10-10T18:55:57.069Z
close_reason: |-
  Completed the reviewed implementation and CI repair published in PR462 (https://github.com/jlevy/squares/pull/462) at exact head d3c99face8fa81fd6ad265111265e4f6a6067106. The coordinator's sole final CI watch exited 0: 31 PASS, 26 intentional SKIP, 0 failures, 0 pending; frontend PASS and all final-head checks green.

  Final behavior supersedes stale descriptions: single centered n=53 hero; homepage Triangle preview 36→100→324→36; About H1; inline homepage video; complete Atlas and Frontier Survey, shared navigation/design and case/result previews retained. The canceled scientific PDF change is excluded. No assertion, 300ms startup bound or scientific content is changed by this closeout.

  Earlier local 901-second incomplete validation and the 195c80948 startup failure remain preserved in prior notes and durable receipts; final hosted success does not relabel those runs. This closes implementation and CI-repair beads only. Full checkpoint think-xio5, epic think-2u4x, process owner think-ht59 and scoping follow-up think-9k61 remain open.
resolution: null
duplicate_of: null
---
Keep the Squares Project narrative, contribution invitation and project documentation on about.html, using About navigation immediately before GitHub and a centered homepage project card. Split dense narrative into paragraphs, including before Now several others, and add the H2 Contribute Your Results! above the result-reporting invitation. Remove Reading and Research from About. Papers retains the existing paper/tutorial cards and PDFs; omit Frontier Survey and Workbench cards because they are already accessible elsewhere and are not papers. Latest owner steering supersedes adding those cards to Papers. Preserve the shared shell, resource destinations and content meaning.

## Notes

Local About now has readable paragraph breaks before Now several others, Separately and This project; Contribute Your Results! H2 above reporting invitation, separate group-chat paragraph, project documentation retained. Reading and Research removed fromAbout. Papers retains3papers+Tutorial+2PDFcards, no redundant FrontierSurvey/Workbenchcards.15 bounded source checks passed; Ruff and format checks clean; pinned Flowmark applied. Only About/Papers preview pages rebuilt and served at127.0.0.1:8766. Local draft only; publication verification remains open.
