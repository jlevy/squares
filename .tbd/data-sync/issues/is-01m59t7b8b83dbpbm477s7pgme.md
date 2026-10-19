---
type: is
id: is-01m59t7b8b83dbpbm477s7pgme
title: "PR #665: diagnose combined 665/671/578 private-worker capacity"
kind: task
status: closed
priority: 1
version: 4
delegate: codex-665-adoption-reconcile
labels: []
dependencies: []
parent_id: is-01m59jbf3zmjznc12k8g2b5cwk
hold: null
hold_until: null
created_at: 2026-10-19T10:09:58.026Z
updated_at: 2026-10-19T10:25:23.068Z
started_at: 2026-10-19T10:10:49.349Z
closed_at: 2026-10-19T10:25:23.067Z
close_reason: Read-only diagnosis complete; exact same-selector inventories and explicit merge uncertainty retained in CAPACITY.md. Capacity acceptance and M1 remain open with coordinator.
resolution: null
duplicate_of: null
---
Read-only immutable Git-object capacity diagnosis for 665 at708a372d,671 atf319bdfd and578 atb76a24fd. Reconcile same-selector required input inventory and test whether proposed224MiB cap suffices. No checkout/source edits, cap change, pruning, copies, proof replay, push or publication. Preserve others ownership and write only a bounded durable memo/evidence in root .codex intake handoff.

## Notes

Completed read-only capacity diagnosis. Durable memo: .codex/intake-resume-20261019/665-capacity-20261019/CAPACITY.md; reproducible object-only source project_capacity.py, capacity.json full path deltas/recovered fixed input roster, overlap.json all75ambiguous paths, projection.log. Total evidence about136KB, no source checkout/tree/private worker/bulk packet materialized. No cap/prune/source mutation, proof replay, GitHub edits/pushes or owner takeover.

Pinned refs: 665708a372dcead45623cbda47a3a1e96ddddd7771a;671f319bdfd9771def53383dd6674923e5c29f4bd01;578b76a24fd29bdab28b5c946adeff88313fd28eb47;main e952755bcad005738785ab8bab0d0b7176f34fed. Same proposed578selector acc28b06a6425ddc042b736bf29e0e9a972b97a5, complete665fixed private-copy graph held constant acrossrefs. Prior349228573883 and394227833136byte calibrations reproduced EXACTLY. Current665228580328;671227840036;578232296355;main225788643. Additive235094940=665+(671-394)+(578-main), which is213916over224MiB234881024. Securitydelta6900;578netdelta6507712. This is not a resolved combined-tree measurement.

75paths modified differently on both sides, including results/evidence/T007/SYNOPSIS/URLs. Their conflict resolution/regeneration prevents exact final claim. Fixed unambiguous selected bytes221826854; literal retention of both existing versions at ambiguouspaths totals247768601 before future generated additions. Smaller/larger existing-object choice sensitivity234531832..235063623 straddlescap but neither is a valid semantic-merge guarantee. Thus224MiBnotdemonstrated sufficient; additiveforecast failscap, no M1waiver.

RequiredPDF: Gobel1979blob1ae5fc99a63f9d848f7ff0b046333cfc7398ffea,4982398bytes. Profile+inspectedbyline declarations deduplicate toONEcopy. #578 test requiresordinary private bytes/private index/bothloaders/refusalonremoval, so cannotprune. Newoccurrences manifest701867bytes. Onlyprovedduplicate route witness.schema.yaml9013bytes countedtwice ordinarywalk+namedcopy; avoidingsecondwritewhilepreservingoneordinaryindexedfile is candidateoptimization, not implemented. It alone leavesforecast204903overcap. No largeunusedprivateinputprovedremovable; prior threeprunecandidates remain0safe savings. Safe nextstep: owningintegration reconciles75paths and regenerates contributor/T007/publicationoutputs onacceptedbase, then maintainedinventory+fresh66housecustody. M1/finalrelease decisions remainOPEN inthink-2921/think-fz6p. Original665worktree407/fullintake671untouched.
