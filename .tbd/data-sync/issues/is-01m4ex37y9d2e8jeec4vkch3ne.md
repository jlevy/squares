---
type: is
id: is-01m4ex37y9d2e8jeec4vkch3ne
title: Normalize responsive case-page and popover layouts
kind: task
status: closed
priority: 1
version: 4
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
created_at: 2026-10-08T23:20:39.625Z
updated_at: 2026-10-10T18:55:56.943Z
started_at: 2026-10-09T00:25:38.377Z
closed_at: 2026-10-10T18:55:56.943Z
close_reason: |-
  Completed the reviewed implementation and CI repair published in PR462 (https://github.com/jlevy/squares/pull/462) at exact head d3c99face8fa81fd6ad265111265e4f6a6067106. The coordinator's sole final CI watch exited 0: 31 PASS, 26 intentional SKIP, 0 failures, 0 pending; frontend PASS and all final-head checks green.

  Final behavior supersedes stale descriptions: single centered n=53 hero; homepage Triangle preview 36→100→324→36; About H1; inline homepage video; complete Atlas and Frontier Survey, shared navigation/design and case/result previews retained. The canceled scientific PDF change is excluded. No assertion, 300ms startup bound or scientific content is changed by this closeout.

  Earlier local 901-second incomplete validation and the 195c80948 startup failure remain preserved in prior notes and durable receipts; final hosted success does not relabel those runs. This closes implementation and CI-repair beads only. Full checkpoint think-xio5, epic think-2u4x, process owner think-ht59 and scoping follow-up think-9k61 remain open.
resolution: null
duplicate_of: null
---
Share consistent content widths, headings, spacing, bounds, drawings and math across standalone case records and fetched popover articles. Balance the first viewport so an oversized drawing does not displace title, interval and summary. Keep long expressions contained, close controls reachable, scrolling usable, and keyboard focus restored. Cover representative n=5,11,17,291,324 at desktop, mobile and a narrow overflow width. See L2 and the layout acceptance in the spec.
