---
type: is
id: is-01m4f2239ewxyae710qvy3tw45
title: Expand the homepage Atlas in place with an Explore destination
kind: feature
status: closed
priority: 1
version: 12
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
created_at: 2026-10-09T00:47:24.965Z
updated_at: 2026-10-10T18:55:57.080Z
started_at: 2026-10-09T00:48:47.737Z
closed_at: 2026-10-10T18:55:57.080Z
close_reason: |-
  Completed the reviewed implementation and CI repair published in PR462 (https://github.com/jlevy/squares/pull/462) at exact head d3c99face8fa81fd6ad265111265e4f6a6067106. The coordinator's sole final CI watch exited 0: 31 PASS, 26 intentional SKIP, 0 failures, 0 pending; frontend PASS and all final-head checks green.

  Final behavior supersedes stale descriptions: single centered n=53 hero; homepage Triangle preview 36→100→324→36; About H1; inline homepage video; complete Atlas and Frontier Survey, shared navigation/design and case/result previews retained. The canceled scientific PDF change is excluded. No assertion, 300ms startup bound or scientific content is changed by this closeout.

  Earlier local 901-second incomplete validation and the 195c80948 startup failure remain preserved in prior notes and durable receipts; final hosted success does not relabel those runs. This closes implementation and CI-repair beads only. Full checkpoint think-xio5, epic think-2u4x, process owner think-ht59 and scoping follow-up think-9k61 remain open.
resolution: null
duplicate_of: null
---
Homepage native SVG Atlas starts in Triangle with first5mathematicalrows through25. FirstExpand immediately reveals100, secondExpand reveals324; thenCollapse restores25. Reuse sharedSiteAtlasView layout/FLIP throughout, persistentnativeSVGlinks/colors/boundlabels andcasepopovers. Prepareallartworkatstartupfrominertcompressedpayload; no click-timefetch/delay. KeepExplore,doubledownchevronsuntilfull,doubleupatCollapse, stage-awareaccessiblelabels, live themes,reducedmotion,keyboard andnoJSinitial25Triangle fallback. DedicatedAtlasdefault/responsivecollapsedrows unchanged. Preserve2MBhomepageceiling; previous36caseGridpreview superseded.

## Notes

Homepage starts in Triangle with25nativeSVGcases (5square-numberrows); Expand100then324, fullCollapse25. SharedSiteAtlasView.change/arrange andper-stagewidest9/19/35, persistentboundaryanchor moves;startup299preparedfrombyte-exactinertcompressedpayload,no clickfetch/delay. Accurateactual/nextcountlabels,double-down/down/up chevrons,scopedstate;dedicatedAtlas unchanged. Markup1passed;2focusedlivechecks passed28.29s1280/390 coveringexact25->100->324->25,cached/rapidcycles,all324anchor/SVGidentity,synchronousshared360mszero-delayarrivalanimation,reducedmotion,collapseviewport,themes/contrast,case291popover/focus,noJS25Triangle/Explore,andzero clickSVGrequests. Ruff/Biome/overview+probeTS/diffclean. Sourcefrozen;servedindex1,169,593bytes<2MB. Rootviewedinitial25desktop/mobile screenshots,clean;allstageimages retained. Astra boundedsourceapprove,noremainingfindings. Earlier36caseGridpreview superseded. Localdraftonly,publicationgatesremainthink-xio5.
