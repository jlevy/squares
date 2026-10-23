---
type: is
id: is-01m4pv16sta8jkhsfkk7sgc46n
title: Codify replies on every intake issue, posted after merge, and read two watched repositories (2026-10-12)
kind: task
status: closed
priority: 1
version: 5
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T01:18:31.226Z
updated_at: 2026-10-23T06:12:24.133Z
started_at: 2026-10-12T01:18:35.823Z
closed_at: 2026-10-23T06:12:24.133Z
close_reason: 'Tracker audit 2026-10-23 (c-audit-b-1023, think-ioqe), checked by coord-intake-1023: STALE-CLAIM + DONE. Reply rule in packing/campaign/result-import.md ("standing instruction of 2026-10-11", 3 hits) and intake-watch.yaml reads 52cf1cc7ba00 and f30cc2cf345a (cdf608574) on main via #563 merge d22861a18 (2026-10-14). Its gap went to think-qh9a.'
resolution: null
duplicate_of: null
---
Owner's rule of 2026-10-11/12: every issue a pass touches gets a comment, and every later change of state a follow-up, until it is closed with a final comment; comments are posted after the PR merges, linking only to main, after validating main and the deployed site; agents post them as part of the pass. Codify in packing/campaign/result-import.md (Running an Intake Pass, The Prompt, Stage 1 step 5, Stage 7, After the Merge) and epistemics.md#import-integration-and-reply. Also record two watched-repository reads in packing/campaign/intake-watch.yaml: RobertBarnettProjects/square-packing-research 52cf1cc7ba00 and wand125/square-packing f30cc2cf345a (the latter naming a new evaluation bead).

## Notes

## 2026-10-12, Claude Opus 5.5 (lane on the 2026-10-11 intake stack, layer 2, 1e41643e8)

**Part 1, the owner's reply rule.** The owner, 2026-10-11/12: "be sure the process codifies that you need to comment on every issue and follow up on each", and "An update on the issues as they are approved. We should validate everything follows and then comment after the PRs are merged." Codified as the standing instruction of 2026-10-11 in packing/campaign/result-import.md (Running an Intake Pass steps 6 and 7 and its closing rule; The Prompt steps 7 and 8 and its closing rule; the Sequence table's stage 7 row; Stage 1 step 5; Verify the Published Result's first paragraph; Stage 7; the gate sentence under The Requests Record; After the Merge steps 2 and 3) and in epistemics.md, Import, Integration, and Reply, end point 3. "Never merge without the owner's word", "never push to main" and the CPU-hour budget rule are kept; "never post ... without the owner's word" is replaced. The same "owner's next move" wording in the check_requests docstring and the packing-validate step comment now reads "owed after the merge". No test pinned the old wording (grep of packing/tests for "owner's word" and "Never merge, never push": none).

Gap found, not fixed here: check_requests --report flags replies due from ids, rungs and the four statuses (recorded, reviewed, confirmed, incomplete), and from `outdated`; it does not flag a case adopting a result, a supersession, or an issue whose new comments a pass only read. The runbook now says the pass that makes such a change follows it up.

**Part 2, two watched-repository reads** (packing/campaign/intake-watch.yaml).
- RobertBarnettProjects/square-packing-research 52cf1cc7ba00: three commits of 11 October past #505's pin 2573ff5 (fa1322a, 9947091, 52cf1cc). Six certificates of 10 October (70, 103, 123, 129, 146, 295) archived under superseded/; read here exactly from their headers (SHA-256 each equal to the threshold file's), above T-146 at 70, 103, 123, 129, 295 by 1.31e-13 to 1.24e-12 and above T-150 at 146 by 4.89e-10; the author marks all superseded. n146/n261 unchanged. Nothing to import; a read with no bead.
- wand125/square-packing f30cc2cf345a: tools/sqverify_continuous/ (v3, source_sha256 1266a8b9...), the continuous-angle mode of this repository's sqverify-fast. Read with bead think-xzob, which holds what it is, its licence, what it reuses (blob-level comparison with dee22b88 and 910b6b12c) and the price of a soundness review and replay.

**Commits** on worktree-agent-acdfff04486c4f34e (from 1e41643e8, not pushed): 3558ec428 (docs: the reply rule), b4c030f11 (intake: the two reads). Beads opened: think-xzob (wand125's sqverify_continuous), think-qh9a (check_requests reply-due gap).

**Checks.** packing-validate --records: 49 of 49 selected steps passed before the commits and again on b4c030f11 (see the final report); make format-check clean; ruff on the two Python files clean. The online sweep (GitHub reachable) lists both reads as accepted and no watched repository needing action; it still lists #500 and #506 as not in result-requests.yaml, which the import lanes for think-ga3m and think-om5l own, not this lane.
