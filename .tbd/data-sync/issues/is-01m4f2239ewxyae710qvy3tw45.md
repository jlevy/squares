---
type: is
id: is-01m4f2239ewxyae710qvy3tw45
title: Expand the homepage Atlas in place with an Explore destination
kind: feature
status: in_progress
priority: 1
version: 10
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
updated_at: 2026-10-09T05:28:52.417Z
started_at: 2026-10-09T00:48:47.737Z
---
Homepage native SVG Atlas starts in Triangle with first5mathematicalrows through25. FirstExpand immediately reveals100, secondExpand reveals324; thenCollapse restores25. Reuse sharedSiteAtlasView layout/FLIP throughout, persistentnativeSVGlinks/colors/boundlabels andcasepopovers. Prepareallartworkatstartupfrominertcompressedpayload; no click-timefetch/delay. KeepExplore,doubledownchevronsuntilfull,doubleupatCollapse, stage-awareaccessiblelabels, live themes,reducedmotion,keyboard andnoJSinitial25Triangle fallback. DedicatedAtlasdefault/responsivecollapsedrows unchanged. Preserve2MBhomepageceiling; previous36caseGridpreview superseded.

## Notes

Implemented local shared SiteAtlasView layout/animation with scoped state.36 native SVG cases initially; all324 prepared at startup from byte-exact inert gzip. Expand synchronously animates into triangle without click fetch; reversible collapse settles scrolling inside shared mutation.21 engine Node tests and3 focused source/browser cases passed (63.32s), including1280/390, persistent nodes, zero fetch, scroll delta0,360ms/easing,reduced motion0, unchangedURL/globalstate and unclipped216x252 native cards. Live desktop/mobile native291popover, Light/Dark palette/background/contrast and collapsedbutton visibility passed. Finalhomepage1,220,393bytes <2MB. Ruff/Biome/TS clean; root reviewed fresh triangle/mobile/preview images; Astra bounded review has no remaining actionable findings. Refreshed index+Atlas served at127.0.0.1:8766. Local draft only; publication gates remain think-xio5.
