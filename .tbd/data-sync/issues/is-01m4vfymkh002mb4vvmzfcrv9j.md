---
type: is
id: is-01m4vfymkh002mb4vvmzfcrv9j
title: "Runbook: every imported proof gets a Fable Max mathematical-correctness review at intake, shared with its author"
kind: task
status: open
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-10-13T20:41:04.878Z
updated_at: 2026-10-14T02:11:30.374Z
---
Owner, 13 October 2026: 'this should be part of our intake process in general', after asking for 'a strong Fable Max subagent for mathematical correctness on both n=17 proofs, with full review docs we can share back with the authors' and 'once these return and issues are addressed, these should go into the validation logs and we should update any V or C levels as appropriate'. Change packing/campaign/result-import.md: Running an Intake Pass (a step after 3), Stage 4's review lane (who reviews and when: tbd-strong-max on claude-fable-5-1 at effort max, in its own worktree, blind to earlier reviews until its findings are written, written for the author; when it returns, fix the record's findings, map the review, update unfinished_confirmations and the validation backlog, re-derive V and C with check_results, draft the share-back in the answer bead), and The Prompt. Draft at the coordinator's scratchpad runbook-review-lane.md. Lands with the two n = 17 reviews (think-32rl, think-0393) in their pull request, under the same sub-agent review.

## Notes

2026-10-14, writer lane on claude/stoic-clarke-jhfnru (local commit 4667528c0, not pushed): result-import.md stage 4 "Who reviews, and when", the intake pass step 3 and The Prompt step 4.
