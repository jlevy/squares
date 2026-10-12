---
type: is
id: is-01m4f31r4a3ngh0jcqmkcn0e9r
title: Separate homepage PDFs and video and place them on their dedicated pages
kind: task
status: closed
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10.local
labels:
  - website
dependencies:
  - type: blocks
    target: is-01m4ex3gpzxxh9eqemc2r78p4e
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-09T01:04:42.121Z
updated_at: 2026-10-10T18:55:57.120Z
started_at: 2026-10-09T01:07:36.152Z
closed_at: 2026-10-10T18:55:57.120Z
close_reason: |-
  Completed the reviewed implementation and CI repair published in PR462 (https://github.com/jlevy/squares/pull/462) at exact head d3c99face8fa81fd6ad265111265e4f6a6067106. The coordinator's sole final CI watch exited 0: 31 PASS, 26 intentional SKIP, 0 failures, 0 pending; frontend PASS and all final-head checks green.

  Final behavior supersedes stale descriptions: single centered n=53 hero; homepage Triangle preview 36→100→324→36; About H1; inline homepage video; complete Atlas and Frontier Survey, shared navigation/design and case/result previews retained. The canceled scientific PDF change is excluded. No assertion, 300ms startup bound or scientific content is changed by this closeout.

  Earlier local 901-second incomplete validation and the 195c80948 startup failure remain preserved in prior notes and durable receipts; final hosted success does not relabel those runs. This closes implementation and CI-repair beads only. Full checkpoint think-xio5, epic think-2u4x, process owner think-ht59 and scoping follow-up think-9k61 remain open.
resolution: null
duplicate_of: null
---
Show PDF cards on both Papers and the homepage. Show video on both Visualize and the homepage. Remove the combined PDFs and Videos heading/group and remove the media section from the dedicated Atlas. Retain publication/source/download links, legacy fragments where useful, and centered solo video cards. Preserve all paper cards under Learn More.

## Notes

Implemented latest owner refinement: homepage replaces video card with responsive native inline player using existing ascent film URL/poster, controls, playsinline and preload=none; no autoplay. Full Visualize player unchanged. PDFs remain homepage+Papers, separate from video. Live draft refreshed at 127.0.0.1:8766. Verification: 2 desktop/mobile browser cases and 5 media/content cases passed; zero initial video requests, click initiates existing film URL with requests intercepted, no full download. Player centered at16:9 and fits both widths. All7main homepage headings gain0.5rem above; Legend spacing unchanged. Ruff/format, Biome, probe types and diff check clean; Astra review clean. Durable screenshot homepage-inline-video.png. No commit/push; combined verification remains think-xio5.
