---
type: is
id: is-01m5jzwxrmhyeh1tcpxtg8cvjh
title: Match every menu destination heading and title to its navigation label
kind: task
status: closed
priority: 2
version: 9
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: sol-tracker-audit
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-22T23:42:17.875Z
updated_at: 2026-10-23T01:36:52.427Z
started_at: 2026-10-22T23:43:19.295Z
closed_at: 2026-10-23T01:36:52.427Z
close_reason: Completed narrow implementation and verified integrated preview receipts recorded in notes; latest follow-up requirements and global CI remain separately tracked.
resolution: null
duplicate_of: null
---
Current canonical naming requirements: actual menu destinations share their menu label in browser metadata, rendered headings and current ancestry breadcrumb. Homepage is the explicit exception: menu/browser Overview, H1 The Square Packing Problem, then Visual Atlas and Results preview headings; preserve baseline IDs and remove the duplicate problem subtitle. Overview and News have no standalone visible or structured breadcrumb. Project Documentation, Contributor Profiles and Workbench use those exact page names. Report a Result is last under Results and absent from About. Verification and the detailed Project Epistemics page follow the separate extraction under think-7r1w. Keep the current plan, route map, button tracking rule and bead references reconciled with the latest user steering.

## Notes

Earlier close_reason receipts describe superseded user instructions (including homepage H1 Overview and Verification and Ratings). They are historical evidence, not the current contract. Latest homepage exception actual-render regression passed 1 test in 85.59s; shared title/profile integration and Workbench head/H1 checks passed earlier. Root and components own final integrated preview/interaction verification.

Completed shared canonical-title behavior and explicit homepage exception. Actual homepage/title regression passed1case85.59s; canonical title/contributor2cases and profile breadcrumb3cases passed. Root all-web/Workbench rebuild and7452site-check recheck passed. Latest user All Results naming and Frontier Survey labels are separate active follow-up under think-6ts0/current worker; prior labels are historical, not pending work in this bead.
