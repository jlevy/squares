---
type: is
id: is-01m4ex39sxfwhfwk0g061nr0mn
title: Publish the complete atlas on a dedicated page
kind: feature
status: closed
priority: 1
version: 8
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
created_at: 2026-10-08T23:20:41.532Z
updated_at: 2026-10-10T18:55:57.022Z
started_at: 2026-10-09T00:25:38.385Z
closed_at: 2026-10-10T18:55:57.022Z
close_reason: |-
  Completed the reviewed implementation and CI repair published in PR462 (https://github.com/jlevy/squares/pull/462) at exact head d3c99face8fa81fd6ad265111265e4f6a6067106. The coordinator's sole final CI watch exited 0: 31 PASS, 26 intentional SKIP, 0 failures, 0 pending; frontend PASS and all final-head checks green.

  Final behavior supersedes stale descriptions: single centered n=53 hero; homepage Triangle preview 36→100→324→36; About H1; inline homepage video; complete Atlas and Frontier Survey, shared navigation/design and case/result previews retained. The canceled scientific PDF change is excluded. No assertion, 300ms startup bound or scientific content is changed by this closeout.

  Earlier local 901-second incomplete validation and the 195c80948 startup failure remain preserved in prior notes and durable receipts; final hosted success does not relabel those runs. This closes implementation and CI-repair beads only. Full checkpoint think-xio5, epic think-2u4x, process owner think-ht59 and scoping follow-up think-9k61 remain open.
resolution: null
duplicate_of: null
---
Add atlas.html for the full 324-case atlas, reusing drawing assets, views, controls and canonical case pages/popovers. Expose it through shared navigation while retaining the Frontier survey. Register its URL, crawl metadata, builder assets, preview coverage and Pages scope. Forward existing homepage atlas fragments and query view state to the full atlas. Preserve published case/result addresses. See L4 in the spec.

## Notes

DedicatedAtlas defaultsTriangle inmarkup,tabs,bootstrap andsharedengine querysemantics. Explicit?atlas=grid persists/reloads; legacy?atlas=trianglevalid; unrelatedsize/query/hash preserved. Dedicated-only bootstrap/CSSguards preserveprepaintGrid andhomepage scopedGrid36. Servertriangle positions/noJSall324retained. Checks:41Node,1markupdefault,14measurementhelpers,5focusedlive36.40s1280/390; liveincludesdefault/gridreload/view+size+resize/strict324/persistentnodes/reducedmotion/noJS/deepcase/homeunchanged/focuspopover/collapse. Ruff/Biome/overview+probegroupTS/diffclean. RefreshedAtlas usescurrenthashedengine/grid. Rootrevieweddefaulttriangle screenshot;Astra boundedapprove nofindings. Fullpublicationgates separatelythink-xio5.
