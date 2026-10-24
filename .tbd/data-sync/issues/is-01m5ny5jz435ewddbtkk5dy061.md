---
type: is
id: is-01m5ny5jz435ewddbtkk5dy061
title: "Address PR #750 review A (A1-A9), then merge main after #745"
kind: task
status: closed
priority: 2
version: 5
delegate: c-fix-750-1024
labels: []
dependencies: []
parent_id: is-01m5nvt5g3enrh90fphg6y7rwt
hold: null
hold_until: null
created_at: 2026-10-24T03:09:47.876Z
updated_at: 2026-10-24T05:15:51.976Z
started_at: 2026-10-24T03:09:57.242Z
closed_at: 2026-10-24T05:15:51.976Z
close_reason: "#750 merged at 2c58b6373 (head c5f747bf0; review A 6379115396 with dispositions 6379656735; CI green 40064635396, 40064635355, 40064633304)"
resolution: null
duplicate_of: null
---

## Notes

2026-10-24 c-fix-750-1024: review A (https://github.com/jlevy/squares/pull/750#issuecomment-6379115396) addressed on claude/intake-2026-10-23-lean-sources. Commits: 42335743b (A7, lean_closure: native-evaluation tokens, credential-free source_url and --source-url, srcDir; tests written first, 14 failed/5 passed unfixed, 19 pass fixed), d45eda7fb (A1-A5 records: AI assistance in the sources' terms, T-238 as a report, credit chains incl. Ryu dropped from the Fang key, T-237 unfinished_confirmations think-wuo4 C1 and think-vvjk C3, A5 wording), 6b739f337 (merge origin/main 14b14f2d1, clean), f1300d063 (re-pin to d45eda7f; papers' no-change record names the third measurement, all four papers byte-identical with and without review A's edits). Pushed f1300d063; PR body updated (A6, A9); dispositions reply https://github.com/jlevy/squares/pull/750#issuecomment-6379656735. Beads created under think-ezt8: think-wuo4, think-vvjk, think-14s2 (A8). think-4o9c given a correcting note (A9, A5). Local: --records fails on contiguity alone; 22 affected suites 924 passed, 7 failed (all contiguity). Waiting on #745 to merge main and re-cut the explainer.
2026-10-24 c-fix-750-1024, after #745: merged origin/main 1aa953fad (#759, 0411bc48b) and af9c9e850 (#745, 4f1b52b92; T-232/T-233 moved before T-234, views re-rendered, release.py took main's v0.4.23 and pin, credit-attributions curation kept both clauses); stamp_landed --apply dated T-234 to T-236 landed 2026-10-24 (e48b9127d); re-pinned to e48b9127 (9f61e02bb); explainer cut v0.4.24 over #745's v0.4.23 for 238 results, the three other papers byte-identical, the explainer differing only in "one of 238 results" (c5f747bf0). Head c5f747bf0: packing-validate --records passes (53 steps, contiguity included); hosted Packing validation 40064635396 success (12 jobs ok, 12 skipped), Certificate page 40064635355 success, Branch mergeability 40064633304 success. PR body updated; not merged, still draft. Left open for the coordinator.
