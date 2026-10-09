---
type: is
id: is-01m4faf19r6n8bz35rfvv5xs8t
title: Place the full Frontier Survey after the Atlas graphics
kind: feature
status: in_progress
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
created_at: 2026-10-09T03:14:17.527Z
updated_at: 2026-10-09T03:43:30.097Z
started_at: 2026-10-09T03:14:49.784Z
---
Move the entire Frontier Survey onto atlas.html after the graphical Atlas and remove separate Frontier navigation tab. Preserve all survey prose, controls, table, record popovers and math. Keep frontier.html legacy addresses working via forwarding with query/fragment preservation. Give Atlas graphical case targets and survey-row targets distinct stable fragments, so graphical targets fully expand before revealing their tile while survey targets reveal the correct row. Update case-popover buttons, hero references, canonical/deployment route declarations and affected checks without changing scientific records.

## Notes

Implemented full Frontier Survey below Atlas graphics with one shared case popover and distinct survey-row #n-N / diagram #atlas-n-N targets. Remove separate Frontier top-nav item; canonical links and Dataset metadata reach Atlas. Legacy frontier.html/status.html preserve row/section/query arrivals. Combined served HTML862357bytes:688112Survey+174245graphics/sharedshell, evidence-based1MB allowance. Verification:64scoped source checks passed across initial62 and repaired2;24live table/legacy-forwarder browser cases passed at8766; typed/Python floors clean. Root canonical declaration/size assertions,14consumer linkchecks,20nodeforward checks and3result-link checks passed. Astra reviewclean; fullcore, paperHTML andWorkbench preview rebuilt. Desktop/mobile transition screenshots inspected. No commits/pushes; broader verification remains think-xio5.
