---
type: is
id: is-01m5k51ees0skkkd01y57eh8j7
title: Migrate overview assertions to dedicated Frontier and complete Atlas
kind: task
status: closed
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: sol-frontier-tests
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T01:12:08.906Z
updated_at: 2026-10-23T01:29:52.448Z
started_at: 2026-10-23T01:12:20.140Z
closed_at: 2026-10-23T01:29:52.447Z
close_reason: Frontier canonical test and fixture migration validated and pushed; integration acceptance remains open separately.
resolution: null
duplicate_of: null
---
Own only Frontier/Atlas stale expectations in test_overview.py; preserve route/content/navigation behavior and run focused tests alongside final CI.

## Notes

Completed and pushed in combined25a7040669cbe4941d975c946b885f0a0a835c18; normal hooks passed. Full site_documents module71passed77.45s; result_overview66passed101.05s; canonical5passed27.07s; focused overview17 plus serif-intro1; forwarder1passed3.70s; Frontier math-face3passed27.91s; screen/print radical negative-controls2passed11.02s. Ruff/format/diff clean; scoped basedpyright0errors0warnings. Source gaps found and repaired by owner: Frontier fragment validator and STATUS.md canonical mapping (authorized one-line mapping included). Latest visible label Frontier Survey matched. Root now sole committer/pusher after coordinated combined checkpoint. Integration/current CI remains tracked by kmpp/z3lz; subsequent All Results consolidation is new requested scope.
