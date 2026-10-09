---
type: is
id: is-01m4ex3gpzxxh9eqemc2r78p4e
title: Verify the website layouts, math, previews and Headroom interactions
kind: task
status: in_progress
priority: 2
version: 14
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10.local
labels:
  - website
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-08T23:20:48.607Z
updated_at: 2026-10-09T01:59:25.891Z
started_at: 2026-10-08T23:50:51.591Z
---
Verify the combined website changes after its nine implementation issues. Cover final homepage order, S4+ results capped at12 with unchanged full-results defaults, sans count/scope chrome, paper/PDF/video cards under Learn More, centered solo-card groups, uppercase button styles, project card and About narrative/nav position, complete Atlas and Results, reversible fetched Atlas expansion with keyboard/busy/error/retry behavior and dynamic case popovers, canonical and legacy routes, n291/n324 narrow case geometry/math, and one visible accessible T115 result title after loading. Include Headroom across all four shells, desktop/mobile/320widths, themes, reduced motion and noJS. Retain reviewed screenshots and keep the local draft available. Browser/output builds currently encounter intermittent external scratch ENOSPC; an explicit internal-scratch override or stable external capacity is pending. PDF description editing is excluded.

## Notes

Final frozen localdraft at127.0.0.1:8766 includesall latestownerrequirements. Homepage16browserpassed66.94s +17contentpassed12.37s (nativeSVGgeometry/pointeropens/cachedexpand/retry/noJS/liveSystem-light-darkcontrast/palette; H1/H2styles, MoreResourcescards-only, removals, centered4-lineLegend). Case6matrixpassed163.16s; result/documentpopover7passed; gear6widthsx6shells andheadroom8passed; Nodeforward20 androwpopover26passed. Astra finalproductionreviewclean; testhelper H1boundaries corrected andcurrenttests green. OwnRuff/Biome/fullprobe-type floors green aftereditfindingfixes. Broadeditgate remainsred because branchURLhistory differs fromadvancedmain t117/t118 amendments, generatedURLdocdrift, andexpiredsuite_dcostmeasurement think-t7k5; do notclaimpush/fast/fullcheckpointgreen. No merge/publication. Allsourceuncommitted in managedwebsiteworktree; verificationepicremainsopen.
