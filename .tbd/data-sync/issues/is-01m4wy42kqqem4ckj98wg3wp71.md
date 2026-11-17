---
type: is
id: is-01m4wy42kqqem4ckj98wg3wp71
title: "Import wand125 release data/n17-m2048064-v1 (2026-10-13): one n = 17 sub-pattern certificate for #413"
kind: task
status: open
priority: 2
version: 6
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: blocked
hold_until: null
created_at: 2026-10-14T10:07:57.558Z
updated_at: 2026-11-17T21:52:42.349Z
---
wand125's GitHub release data/n17-m2048064-v1 (2026-10-13) holds one n = 17 sub-pattern certificate for jlevy/squares#413. Found by the squares-43 watch read of 2026-10-14 (think-5pn5); no bead covered it. Unowned: the n = 17 work belongs to the stoic-clarke session's lanes (see think-1s3i, BC-416 / H-267, the certified isolated sub-pattern residue on the minimal n17 cover). Stage 1: pin the release asset by digest, map the certificate to the sub-pattern ladder, price its replay. Do not run anything above 30 minutes without a status.

## Notes

2026-10-14: wand125 commented on #413 at 2026-10-13T00:32Z that row 4 now has an unmodified standing FULL receipt (devtools.verify_n17_bb_certificate at main 657cc48, verifier blob e6e400e7f, on the certificate of release data/n17-m2048064-v1; 924,233 nodes). Unanswered and unrecorded on #413 (check_requests --github flags it). The n = 17 lanes should read it, record it and reply.

2026-10-15 reads lane (think-mq0k): the 02:30Z sweep at main 6964362b5 still lists #413 issuecomment-6135318000 (wand125, 2026-10-13T00:32:14Z) as unread; #413's entry reads through 2026-10-11T02:22:21Z. Read again: row 4 now has an unmodified standing FULL receipt. devtools.verify_n17_bb_certificate at main 657cc48 (dirty: false, verifier blob e6e400e7f, which includes #452), run as is, one process, full mode, on the certificate of release data/n17-m2048064-v1: 924,233 nodes, no failures, PASS in 78,224 s, peak memory 6.2 GB; the receipt verification.json is on the release. The release's certificate joins the producer's 500-node chunks into 5,000-node chunks for the asset limit, node records unchanged. Row 4 still stalls under the kernel, so this branch-and-bound certificate is what the author offers for it.

Owner: this bead (the release). It also answers #413's subpatterns-33-standing-scope-correction-2026-10-08 entry (think-bmwd), which retracted the earlier standing FULL attribution for rows 3-4 pending #445's memory issue: row 4 now reports one; row 3 is not mentioned. Both beads sit under the owner's 13 October suspension of new n17 work pending T-153 (Overbeck), so nothing is replayed: the claim is to be mapped into #413's entry as a dated author report (no admission, no exclusion or coverage credit) and #413's read_through moved to 2026-10-13T00:32:14Z in the next records PR. A replay is a full standing verifier run, about 21.7 CPU-h at the source (78,224 s single process) and 6.2 GB of memory: under the 40 CPU-h cap but held by the suspension, and too large for a shared four-core host with about 4 GB free.

2026-10-31 bold-ritchie-l6 (stalled-bead triage of the 31 October intake pass, think-ztcy): Waits on the owner's standing n = 17 hold of 13 October (pending T-153); retaining the row-4 release and its 21.7 CPU-hour, 6.2 GB replay resume only when the owner lifts it.

2026-11-17 w5-audit-1117r (think-uz0m, the stalled-bead audit of the 17 November intake pass, think-p02d; read against main f9ddfeeef): (c) waits on the owner. The owner's n = 17 intake hold of 13 October (pending T-153, Overbeck's s(17) = L) still stands, checked today: T-153 reads V0/C1 in packing/frontier/results.yaml, its ten trees (about 21 CPU-h, under the cap) and its capture recomputation (about 1,273 CPU-h) are unrun (think-lqtu), and none of the eight 17 November decisions (think-b0w5, -fibh, -gmoj, -k2lh, -l7j0, -x30l, -0mup, -k8vt) touches n = 17. The hold is 35 days old; whether to keep it, lift it for T-153's ten trees, or lift it goes to the owner through the coordinator (think-uz0m's report). Nothing here runs until then. Retaining wand125's data/n17-m2048064-v1 (row 4; replay about 21.7 CPU-h and 6.2 GB) stays queued. Now held the way #413's entry already queues it (blocked_on think-x4v4): hold blocked, no claim.
blocked_on: think-x4v4
