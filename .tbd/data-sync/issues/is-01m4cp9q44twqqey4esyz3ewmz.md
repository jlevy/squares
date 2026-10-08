---
type: is
id: is-01m4cp9q44twqqey4esyz3ewmz
title: Resolve solver-dependent Mac snapshot assertions with exact certificate controls
kind: task
status: open
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: null
labels: []
dependencies: []
parent_id: is-01m4cee7q2jdj5scgd5wa72y24
hold: null
hold_until: null
created_at: 2026-10-08T02:43:22.883Z
updated_at: 2026-10-08T07:43:28.895Z
started_at: 2026-10-08T07:43:22.124Z
---
Follow-up from PR435 Mac whole-suite push at fa93843ed (1298.70s). Three unchanged parent assertions fail: test_n17_local_minimum.py:655 compares a retained exact worst_ratio; test_pilot_n17_subpattern_bb.py:607 compares fixed chunk hashes for OBBT=3 cases2.80/2.94. Independent Astra replay found all13 n17 exact checks true,90 directions/93 cells verified, the same printed ratio0.925931049178 with a slightly stronger exact bound; both pilot certificates fully verify, and the OBBT=0 control retains its old hash. A32-module transitive source closure, mathematical inputs, lockfile and interpreter configuration are unchanged against d948311d8. Precise cause of floating solver proposal variation remains unproved; no parent execution was performed. Investigate that cause and replace cross-platform proposal-byte snapshots with controls that preserve the intended mathematical/algorithmic contract. Do not weaken certificate replay or change retained mathematical verdicts. Fresh unique evidence is preserved outside disposable scratch at /Volumes/spud-ext1/agent-evidence/polynomial-catalogue-01a118e4/mac-snapshot-controls; full raw run is validation/mac-push.log. The supported complete checkpoint is Linux, as development.md states.

## Notes

The same three unchanged solver-dependent snapshot assertions recur in the web precommit Mac push: n17 retained worst_ratio and pilot OBBT=3 chunks at 2.80/2.94. Raw web-push.log is preserved under the external agent-evidence validation directory. This web slice changes no mathematical solver/source closure; earlier independent exact certificate controls remain evidence, while the cross-platform proposal cause remains open.
