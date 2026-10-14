---
type: is
id: is-01m4mtdc4km4sy3qqmsftn3rnq
title: "PR #496 follow-up: fix review findings E, F and G on main"
kind: task
status: closed
priority: 1
version: 4
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4mdnpf7raye5cx00cmdfb55
hold: null
hold_until: null
created_at: 2026-10-11T06:29:12.466Z
updated_at: 2026-10-12T23:39:25.705Z
started_at: 2026-10-11T06:29:13.240Z
closed_at: 2026-10-12T23:39:25.705Z
close_reason: "Completed: PR #507 merged (e96e9ea95), fixing or deferring every #496 review E/F/G finding."
resolution: null
duplicate_of: null
---
PR #496 merged before its review findings were addressed. This follow-up PR (branch claude/pr496-review-fixes from main 8aba95081) fixes or defers every finding from review E (senior, Fable: https://github.com/jlevy/squares/pull/496#pullrequestreview-5481683586), review F (performance, Opus: #pullrequestreview-5481911429) and review G (correctness, Fable: #pullrequestreview-5481975880), posts one disposition reply per review on #496 linking this PR, gets a Fable follow-up review (owner's choice), and merges with the owner's confirmation for the new PR number.

Coordinator decisions: F1/E5: a checker wall deadline below the 30-minute verify-deployment ceiling, with partial verdicts printed on expiry. F2: retry timeouts and OS-level errors. E1/G4: --push banners on stderr under --format json, listing unclaimed paths. E2: always pass on_retry. E3: pin the ceiling and deadline bounds. E6: tests for mutual exclusion and NUL rejection. G1 (High): complete the touches claims and add an import-graph contract test. G2: the browser floor claims workbench JSON. G3: messages name the snapshot file. G5: settle or defer. E4: docs. F3: note on think-ht59. F5-F7: beads under think-ht59.

## Notes

2026-10-11 11:30 PT: PR #507 opened (https://github.com/jlevy/squares/pull/507), head 5fa8a3c0f (fix commits 1412a273e audit deadline + transport retries, 0d90b5022 import-closure attribution + JSON banners, d9f1c4c4d docs, 546f4480d test double, merge 5fa8a3c0f of main for PR #398).
Dispositions posted on #496: E issuecomment-6112141969, F -6112142219, G -6112142468 (all fixed except F3/F5/F6/F7 deferred to think-ri5z/think-tqwo/think-h7c0/think-7qbv; G5 rebutted).
Local: focused modules 568+2 (both resolved) then 216/216 on merged code; edit tier 65/65; --push 63/63 prerequisites then behavioral timeout at 900 s (F3, think-ri5z).
Next: Fable review A on #507 (owner's follow-up round), address, merge gate; merging #507 needs the owner's confirmation in chat.
