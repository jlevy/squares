---
type: is
id: is-01m5abdk4yben7cenfr24rs3ms
title: Capture wire diagnostics only for required serial site forwarders
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
assignee: codex-forwarder-wire-diagnostic-20261019
delegate: codex-forwarder-wire-diagnostic-20261019
labels: []
dependencies: []
parent_id: is-01m59khvbyx370mcm1z4t18tyy
hold: null
hold_until: null
created_at: 2026-10-19T15:10:28.509Z
updated_at: 2026-10-19T15:16:21.686Z
started_at: 2026-10-19T15:10:46.123Z
closed_at: 2026-10-19T15:16:21.681Z
close_reason: "Bounded local implementation committed fa7878e4137c891a1fab1f820ae5c1c325792e57, tree3b6998f820b76f94385028abe7d5bf878b2da8e4, exact parent178507647c94fb9990ea2f29d0831de89f0434a1; only validate.py/test_validation_cli.py changed. Serial forwarders only: pytest -s and DEBUGP=1/DEBUG=pw:api; require Chromium, selection, native writer/progress/supervisor, failure propagation and original shared900s deadline preserved. RED2failed1.35s; final GREEN14puremockcasespassed1.32s; focused Ruff/format/types clean; normal hooks2.35s. Preserved646=4bdf7,658=d0b9,CSS1785,388ignoredpaths/sharednode_modules link. Evidence .codex/intake-resume-20261019/forwarder-wire-diagnostic-preparation/. No browser/build/CI/sourcepush/PR/merge. Actual runtime, wire-log capture, overhead and original hang cause remain unknown. Causal think-3gfi/think-yops stay open with existing delegates. Root owns fresh Astra final-delta review and next necessary hosted qualification; prior CSS review is not final-head coverage."
resolution: null
duplicate_of: null
---
Recurrent actual-main run39268295319 at f3d5 waits in test_the_deployed_site_check_follows_the_same_forwarders CALL after 18 serial cases. Add pytest -s and existing DEBUGP=1/DEBUG=pw:api only to browser-forwarders in _site_layout_tests; preserve selection, native writer/progress, worker identity, failure propagation and shared900s deadline. Pure mocked red/green contracts only under W44 local hold; no browser, CI dispatch, push or PR. Commit on a new local branch atop reviewed CSS178507647 in reused review-661 checkout; root owns fresh final delta review and necessary hosted qualification. Root cause and runtime overhead remain unresolved. Preserve parent think-3gfi and think-yops ownership/status.
