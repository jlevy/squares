---
type: is
id: is-01m5mq8fbgy4wwpbxna0ye7z3j
title: "Replay gradec.py on the 233 grade-C configurations: the C3 route of #545's grade-C claim (about 10.6 CPU-hours)"
kind: task
status: in_progress
priority: 3
version: 6
delegate: bold-ritchie-l19
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T15:49:48.015Z
updated_at: 2026-11-01T23:25:48.319Z
started_at: 2026-11-01T15:42:05.081Z
---
The C3 replay of Evan Daniel's grade-C local-minimality claim (#545, think-7scz): the source's own checker, search/exact/gradec.py at ad86d42 (byte-identical at 31523f8; V-evand-gradec-py), run from its retained copy on all 233 configurations the release's gradec-233.tar.zst certifies, 230 and 261 with GRADEC_DROPZERO=1, each output compared with the published n-N.gradec.json. Priced from the source's logs at 38,026 s, about 10.6 CPU-hours (author's machine, 8 jobs; may be slower here); 154 runs are under a minute (about 21 CPU-minutes), the longest is n = 313 at 1,741 s. Above a lane's 2 CPU-hour single-run limit, so it needs the coordinator's or owner's budget; at most 2 workers on the shared host. Result-import.md Stage 4 accepts the source's checker as the replay without a soundness review; the 23 October review's check_theorem_c.py run (receipts/review-theorem-c-233.jsonl, V-evand-gradec-review-check) is the second route beside the rung, as at T-225 and T-229 (review A1 of PR #751, https://github.com/jlevy/squares/pull/751#issuecomment-6368595518). Waits on: a T-NNN for the claim and a budget.

## Notes

2026-11-01 bold-ritchie-l14 (PR #868, branch claude/bold-ritchie-xo28us-l14): devtools.evand_gradec_replay committed (76d72c594) and RUNNING detached (PID 10126, setsid, 2 jobs, reniced to 0) in /tmp/claude-0/-home-user-squares/0a01ddbe-91e2-5d1d-98f8-365093a10337/scratchpad/gradec-replay (ledger runs.jsonl, resumable: relaunch with scratchpad/launch-replay.sh), receipt to scratchpad/gradec-replay-233.json. At 16:48Z: 3 controls refused, n=313 and n=276 byte-identical with logs matching (CPU 1839 s and 1653 s vs release 1741/1633), 0 failures; expect ~11 CPU-h total. When complete: copy receipt to packing/resources/web/evand-exact-data-2026-10-12/receipts/gradec-replay-233.json, run scratchpad/patch_t261.py from packing/ (evidence E-evand-gradec-local-minima-233-replay, T-261 to C3, #545 summary, deferral), commit the uncommitted V-evand-gradec-replay verifier entry in frontier/verifiers.yaml, amend site-urls result/t-261.html, regenerate RESULTS/INVENTORY/VERIFIERS/SYNOPSIS headline, update tests/test_site_result_filters.py incomplete list to [t-007], packet README replay section, re-measure release (scratchpad/release-measure.sh), note think-xyek (draft in scratchpad/drafts.md).

2026-11-01 coordinator: HOLD on the rung change. When the replay completes, record its receipt and evidence entry (coverage, controls, CPU) in the packet and register, but do NOT move T-261 to C3 or run scratchpad/patch_t261.py's status flip until the owner answers think-xyek. Under today's rule 1, C3 would flip T-261 from incomplete to confirmed, which is exactly the question think-xyek puts to the owner (option 2 says the replay must not clear it), and the 31 Oct #545 reply told the author the label follows that answer. The tool (devtools/evand_gradec_replay.py) lands in #868; the records follow-up comes in a separate PR after the replay.

2026-11-01 bold-ritchie-l19 (delegate transferred from bold-ritchie-l14 after #868 merged at 18:52Z; PR #875, branch claude/bold-ritchie-xo28us-l19): **the replay is complete and its receipt is retained; the register change is held per the coordinator's HOLD.** 233 of 233 certificates are VALID and byte-identical, 230 and 261 with GRADEC_DROPZERO=1, all 233 logs match, and the 3 controls were refused. 39,646 CPU-seconds for the replays, 39,647 with the controls. The hardened driver adopted the unstamped ledger once (--adopt-unstamped) on a copy, scratchpad/l19/gradec-replay-copy. The original work directory and receipt were left byte-unchanged (checked by SHA-256). Every run record equals the first receipt's; only fields the hardening added differ, and last_invocation is now the adopting run. Committed: the receipt, packing/resources/web/evand-exact-data-2026-10-12/receipts/gradec-replay-233.json, stored plain by write_retained (548 lines, under the gzip threshold); the packet README section "The Replay of 1 November 2026"; and V-evand-gradec-replay, which no evidence entry cites yet. T-261's next_rung and unfinished confirmation now say it is held for think-xyek, as T-253 and T-260 are for think-ikku; rungs, status, evidence and artifacts are unchanged. Not done (held): the evidence entry E-evand-gradec-local-minima-233-replay, T-261 to C3, the #545 summary, the deferral and the result/t-261.html amendment. The entry, ready to apply, and the steps are in think-xyek's notes (2026-11-01 bold-ritchie-l19). This bead stays open until that register change lands.
blocked_on: think-xyek
