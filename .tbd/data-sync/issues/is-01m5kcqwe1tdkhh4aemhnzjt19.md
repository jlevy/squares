---
type: is
id: is-01m5kcqwe1tdkhh4aemhnzjt19
title: Attribute and bound Packing frontend setup before choosing browser provisioning
kind: task
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: ci-delay-audit
labels: []
dependencies: []
parent_id: is-01m5kcfhfdmgfb03gn3drg43rc
hold: null
hold_until: null
created_at: 2026-10-23T03:26:44.149Z
updated_at: 2026-10-23T03:32:14.495Z
started_at: 2026-10-23T03:32:14.482Z
---
Packing run39892772106 frontend job120216469741 at bf38442f248d089b9862d04ee0658f85b51d7b0c spent524s in combined concurrent npm/Playwright setup (03:03:58-03:12:42 UTC). Comparison39893731935 job120219204931 spent16s; npm and Playwright browser caches hit, npm took1s while apt still updated/downloaded. Current logs unavailable during audit, so npm versus apt attribution is unknown. Retain final logs; add separate process timings, explicit setup ceilings and useful failure output in project-native tooling. Compare a pinned provisioned environment or minimal verified system-dependency path with current --with-deps, including cold/warm cost and storage. Preserve locked inputs, disabled npm scripts, all browser assertions and least privilege. No speedup accepted from one runner observation. Coordinate Pages-specific existing think-fqhc and think-898i; ordinary browser fixture optimization already belongs to think-nqnx. Deliver measured proposal before workflow implementation.
