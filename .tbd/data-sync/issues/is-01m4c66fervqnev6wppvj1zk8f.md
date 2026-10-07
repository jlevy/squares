---
type: is
id: is-01m4c66fervqnev6wppvj1zk8f
title: Fix popover close accessibility state exposed by SQUISH import browser gate
kind: bug
status: in_progress
priority: 1
version: 3
delegate: codex@17e132e9b179
labels: []
dependencies: []
parent_id: is-01m4bvqnk2d26b8ydnvt3h07n1
hold: null
hold_until: null
created_at: 2026-10-07T22:01:59.512Z
updated_at: 2026-10-07T22:21:28.171Z
started_at: 2026-10-07T22:02:29.317Z
---
PR421 final affected gate exposed reproducible Escape closure race: hidden case popover retains aria-expanded=true until asynchronous toggle. Unchanged complete browser replay1failed19passed; math fixtures passed. Sol engineering repair moves accessibility cleanup to synchronous noncancelable closing beforetoggle, leaves focus restoration on toggle, strict tests unchanged. Strong Astra scoped review accepted. Source b4c59000c3ba8ec4bc19fb89a4cc8b175ed6ef7d; complete repaired two-module replay20passed77.99s; required88-selector push since2a27 underway. Track actual source repair/review/CI/publication, keep prior broad failure receipt.

## Notes

2026-10-07 checkpoint: Finalfrozenb4c590 repair: documentedrequiredpush61selectedof101PASS494.78s; actual97commandendreceiptsallPASSED, reachable313.912<900normal3294PASS19skip295.35s/zeroerrorsfailures. Exact /workspace/squares-validation-artifacts/followup-popover-final-push-outcome.json preserves shellsupervisorhandle65557lostafterresumption, outerexitnull(nofabricatedexit0). Hostedcurrentb4call30SUCCESS26SKIP/CLEAN. Fformalstrongfollowup5448936448 acceptedJSonlydelta andunchangedscience. Clean/pinb5fb, CPUreleased. Holdcloseuntilwhole424addressing/merge/publication; no rerunpassinggateforshellbookkeeping.
