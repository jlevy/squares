---
type: is
id: is-01m5jqhsjcznm3w2f8kv5sw2b5
title: Integrate and validate navigation across all site page families
kind: task
status: in_progress
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: navigation-integration
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-22T21:16:24.523Z
updated_at: 2026-10-23T00:34:43.651Z
started_at: 2026-10-22T21:28:25.411Z
---
After PR733 merges, apply shared parent/breadcrumb metadata to articles, records, profiles, papers, chapters and workbench; reconcile registry/build/freshness inputs; verify links, keyboard/mobile/no-JS, theme and browser layouts; build the complete site and review the standalone navigation PR. Include the five focused profile/popover/footer follow-up beads.

## Notes

Integrated checkpoint 5f83d1e73 pushed to PR737. Senior Astra review found missing Archive significance readFilters wiring; fixed and independently verified with37Node tests and S2/S5+conflicting legacy filters reproduction. No remaining blocking senior findings; unused old Recent renderer cleanup deferred to think-31fw. Local fullpreview96314 completed successfully with allfourpaperHTML/PDFs, allsitepages andWorkbench. Finalwebrefresh12968 follows latest Archive controls/Atlas ordering; fullpushvalidation33154 reached68/69 checks with reachabletestsactive. Sol owns current-head hostedCI watch. Width audit passed105artifact measurements and17current-source families at5widths; breadcrumbs alignheaderlogo text while standardprose/cardframes remain630px (responsivegutters). Menu keyboard/mobile1test passed5.30s; Profilecanonicalbreadcrumb3tests passed35.11s; URLregistry1157rows0failures. Final Archivebrowser/News mobile regressions, remaining testfollowupcommit, complete refreshedbrowserreview and currentheadCI remain open. Earlier checkpoint outcomes are not substitutes for finalhead evidence.
