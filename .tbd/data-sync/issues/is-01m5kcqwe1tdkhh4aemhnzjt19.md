---
type: is
id: is-01m5kcqwe1tdkhh4aemhnzjt19
title: Attribute and bound Packing frontend setup before choosing browser provisioning
kind: task
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: ci-delay-audit
labels: []
dependencies: []
parent_id: is-01m5kcfhfdmgfb03gn3drg43rc
hold: null
hold_until: null
created_at: 2026-10-23T03:26:44.149Z
updated_at: 2026-10-23T03:32:34.218Z
started_at: 2026-10-23T03:32:14.482Z
---
Packing run39892772106 frontend job120216469741 at bf38442f248d089b9862d04ee0658f85b51d7b0c spent524s in combined concurrent npm/Playwright setup (03:03:58-03:12:42 UTC). Comparison39893731935 job120219204931 spent16s; npm and Playwright browser caches hit, npm took1s while apt still updated/downloaded. Current logs unavailable during audit, so npm versus apt attribution is unknown. Retain final logs; add separate process timings, explicit setup ceilings and useful failure output in project-native tooling. Compare a pinned provisioned environment or minimal verified system-dependency path with current --with-deps, including cold/warm cost and storage. Preserve locked inputs, disabled npm scripts, all browser assertions and least privilege. No speedup accepted from one runner observation. Coordinate Pages-specific existing think-fqhc and think-898i; ordinary browser fixture optimization already belongs to think-nqnx. Deliver measured proposal before workflow implementation.

## Notes

Confirmed final log attribution: run39892772106 job120216469741 npm installed96packages in2s at03:04:01; apt reports Fetched25.9MB in8min32s(50.6kB/s) at03:12:37. The524s setup delay is apt package download time, mostly fonts. Final site step663.84s, workbench181.63s and browserfloor111.8s overlap. Setup attribution is established for this run; provisioned/minimal-dependency solution and controlled speedup remain unmeasured. Audit retained /Volumes/spud-ext2/agent-notes/squares/review-2026-10-22-ci-release-latency.md; implementation deferred to cleanup PR.
