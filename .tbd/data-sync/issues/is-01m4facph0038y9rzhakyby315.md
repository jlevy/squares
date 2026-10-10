---
type: is
id: is-01m4facph0038y9rzhakyby315
title: Open the hero case popover and navigate to expanded Atlas cases
kind: feature
status: closed
priority: 1
version: 15
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
created_at: 2026-10-09T03:13:00.958Z
updated_at: 2026-10-10T18:55:57.152Z
started_at: 2026-10-09T03:14:19.707Z
closed_at: 2026-10-10T18:55:57.152Z
close_reason: |-
  Completed the reviewed implementation and CI repair published in PR462 (https://github.com/jlevy/squares/pull/462) at exact head d3c99face8fa81fd6ad265111265e4f6a6067106. The coordinator's sole final CI watch exited 0: 31 PASS, 26 intentional SKIP, 0 failures, 0 pending; frontend PASS and all final-head checks green.

  Final behavior supersedes stale descriptions: single centered n=53 hero; homepage Triangle preview 36→100→324→36; About H1; inline homepage video; complete Atlas and Frontier Survey, shared navigation/design and case/result previews retained. The canceled scientific PDF change is excluded. No assertion, 300ms startup bound or scientific content is changed by this closeout.

  Earlier local 901-second incomplete validation and the 195c80948 startup failure remain preserved in prior notes and durable receipts; final hosted success does not relabel those runs. This closes implementation and CI-repair beads only. Full checkpoint think-xio5, epic think-2u4x, process owner think-ht59 and scoping follow-up think-9k61 remain open.
resolution: null
duplicate_of: null
---
Restore the homepage single native SVG hero packing for n=53, centered at the original compact single-image width. Exact caption: Best known packing for 53 identical squares. Colors indicate angle. Darker colors mean more common shared faces. Keep the case53 popover opener/canonical noJS link and social card53. Popover Case Record/Frontier row/Atlas diagram actions follow the current case; Atlas fully expands before tile reveal. Latest single53 request supersedes the earlier three-case hero.

## Notes

Restored the single centered native SVG hero for53, capped at18rem, with canonical noJS link and case53 popover. Exact caption: Best known packing for 53 identical squares. Colors indicate angle. Darker colors mean more common shared faces. Social card53 retained. Hero/source checks and final desktop/mobile live checks passed, including all3popover destinations. Root inspected the fresh mobile hero screenshot. Local preview refreshed. This supersedes the earlier three-case hero; no publication or merge.
