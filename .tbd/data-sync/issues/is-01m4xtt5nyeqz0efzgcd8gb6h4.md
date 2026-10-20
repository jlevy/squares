---
type: is
id: is-01m4xtt5nyeqz0efzgcd8gb6h4
title: "News604 hosted browser assertions: article headings and settled width-cap control"
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4xm9zrn7p4nygg25gwy9cxw
hold: null
hold_until: null
created_at: 2026-10-14T18:29:21.714Z
updated_at: 2026-10-14T18:51:18.997Z
started_at: 2026-10-14T18:29:36.774Z
closed_at: 2026-10-14T18:51:18.997Z
close_reason: Fixed in pushed News604 repair d08551e0aba9cc92eb4d17389bb8c7a4bd1cdf81; B dispositions https://github.com/jlevy/squares/pull/604#issuecomment-6175849755; accepted-kind and corrected real rigidity regression, all 6 affected browser cases, full overview/rung/publication contracts and scoped static checks pass. Parent coordinator owns final hosted CI and review D; tbd sync reserved to root.
resolution: null
duplicate_of: null
---
Current-head Packing38614518600 frontend116026059173 has3failures: global homepage H3/H4/H5/H6 count expects2 though3Newsarticle headings nowexpected; atlas.html scripted negativecontrol reads same-frame computed maxWidth3120 after140rem injected, affected by KPress0.01ms reduced-motion allproperty transition. Preserve all actual width/gutter/panning assertions and >500px negativegap. Update outside-News heading contract and separately assert3Newsarticles, make injected cap deterministic, retain targeted realChromium proof. 419othercasespassed6skipped. Batch with independent review findings before nextpush.

## Notes

Final cohort38614518600 also has three suite-A contract failures: test_overview::test_every_heading_and_headline_shares_one_leading now6 token usesvs5 fromnewNewsH3; test_the_icon_set_is_one_drawing_in_the_stylesheet treatsNewsfade linear-gradient mask asarrowicon; test_rung_scale::test_the_status_chips_take_fills_from_the_scale losesreviewed because rung_scale.status_fills fullmatchesanentireselector and nowreviewed+newverificationtopicshareacomma-selector. Repair maintainedmeasurementparser (or sharedCSSstructure) tokeepreviewedcontrastmeasurement, notremoveassertion. Runfulltest_overview/test_rung_scale plus changedtopic/selection contracts and affected realbrowsercases before singlepush. Pages38614518630success; allotherPackingjobsfunctionalpassed. Logsretainedprimary evidence news-suite-a-38614518600.log andnews-frontend-38614518600.log.
