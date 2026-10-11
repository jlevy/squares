---
type: is
id: is-01m4ex3c459d9jrd6mds18ftqg
title: Tighten the homepage with visible atlas and results previews
kind: feature
status: closed
priority: 1
version: 19
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
created_at: 2026-10-08T23:20:43.908Z
updated_at: 2026-10-10T18:55:57.048Z
started_at: 2026-10-08T23:47:57.505Z
closed_at: 2026-10-10T18:55:57.048Z
close_reason: |-
  Completed the reviewed implementation and CI repair published in PR462 (https://github.com/jlevy/squares/pull/462) at exact head d3c99face8fa81fd6ad265111265e4f6a6067106. The coordinator's sole final CI watch exited 0: 31 PASS, 26 intentional SKIP, 0 failures, 0 pending; frontend PASS and all final-head checks green.

  Final behavior supersedes stale descriptions: single centered n=53 hero; homepage Triangle preview 36→100→324→36; About H1; inline homepage video; complete Atlas and Frontier Survey, shared navigation/design and case/result previews retained. The canceled scientific PDF change is excluded. No assertion, 300ms startup bound or scientific content is changed by this closeout.

  Earlier local 901-second incomplete validation and the 195c80948 startup failure remain preserved in prior notes and durable receipts; final hosted success does not relabel those runs. This closes implementation and CI-repair beads only. Full checkpoint think-xio5, epic think-2u4x, process owner think-ht59 and scoping follow-up think-9k61 remain open.
resolution: null
duplicate_of: null
---
Compact homepage layout with native three-case hero11/53/203 and exactproblem introduction/projectcard, native SVG Atlaspreview second, recentS4+cap12 third, LearnMore paper/PDFcards+inlinevideo, MoreResources. Keep prominent page navigation, uppercase controls and shared headings. LatestLegend refinement: retain centered whole-card link to all-results.html#verification-ladders, remove What each rung means text, use consistent two-column rows with icons/chips in the left column and their labels aligned to the right. Preserve S/V/C/star marks, titles and colors, centeredLegendH2 and the separate completeResults legend. Track deeper sharedAtlasrow/default tasks separately; scientificPDF edit excluded.

## Notes

Homepagelegend now has4alignedicon/labelrows undercenteredLegendH2, no What each rung means helpertext, samecentered52remwhole-cardlinkto all-results.html#verification-ladders. All17marks/titles/colors/star retained; completeResultslegend independentlybyte-identical. Scopeddisplay:grid overridescardflex. Helperunit1passed5.67s;6livegeometry/linkchecks passed13.02s at1280/390/320:<=1pxverticalcentering,nooverflow,pointer/keyboardtarget. Biome/probeTS/Ruff/diffclean. Rootnarrowtestfixturevariable rename clearedtypecollision; affectedtestBasedPyright0errors. Rootreviewed390legend;Astrainspecteddesktop/320andapprovedboundedAtlas+legend increment,nofindings. Indexonlyrefresh retains latestAtlas/gear source, originalhomepageorder/S4+cap12/hero11-53-203caption/media/About. Publicationgates remainthink-xio5; no commit/publication/merge.
