---
type: is
id: is-01m54ahqaf9t63nz12annpqy69
title: "Import wand125: 18 fine-net mixed-measure lower bounds at n = 38 to 110, square-lower-bounds-v1 (#446 comment of 16 October)"
kind: task
status: in_progress
priority: 1
version: 13
delegate: codex@spud10.local
labels:
  - result-import
dependencies: []
parent_id: is-01m549eweq3c13b32tjzbf0ats
child_order_hints:
  - is-01m59ddf80h74jfaxny0srnyfd
  - is-01m59zjwv66y6cjvr4cqx7eh2p
  - is-01m5a0yx8cne1ka5wgnxtrq8e0
  - is-01m5a29bsw8fy21kn36s3g41nt
hold: null
hold_until: null
created_at: 2026-10-17T06:59:48.686Z
updated_at: 2026-10-19T12:30:52.731Z
started_at: 2026-10-18T08:47:56.014Z
---
Hiroaki Hosono (wand125) reports 21 fine-net mixed-measure lower-bound certificates in jlevy/squares#446#issuecomment-6210736972 (created 2026-10-16T07:49:56Z, edited 09:00:31Z to cover all of them). Three are already registered: n = 37 (T-178), 39 (T-176) and 44 (T-177), published 2026-10-13 and registered on 14 October with no issue. This bead imports the **18 new ones**, at n = 38, 40, 41, 43, 51, 68, 84, 85, 86, 88, 89, 90, 91, 92, 106, 107, 108 and 110. Found by the 17 October intake pass (think-e2sz), lane W (user-eb-sweep-1017). Stage 1 triage below; stages 2 to 4 are this bead's.

## Triage (stage 1, 2026-10-17, read-only)

**Pin.**
- wand125/square-packing, one commit per certificate, 2026-10-16T07:45:44Z (02c5595, n = 38) to 07:53:40Z (718887c, n = 110). Each adds problems/square-lower-bounds/certificates/mixed_nN_L*/ with README.md, bundle.json, ASSET.json, files-sha256.json, check2/src/ and provenance/.
- The data is in the release square-lower-bounds-v1, one tarball per certificate (330 to 667 KB). Each holds candidate.json, check2/receipt.json, check2/control.json, run.jsonl.gz, the verifier's source archive sqverify-proof-net-fe12e036c.tar.gz and verification/prepublication-receipt.json.
- All 18 tarballs were downloaded to scratch here, and their SHA-256 matches ASSET.json at fbc5fc4 for every one. Nothing is retained in the repository yet.
- The head fbc5fc4 (2026-10-17) changes none of the 18 folders after 718887c.

**Claims (every one in the comment; "lifted" = started from a published certificate at a smaller n, mapped and re-solved by LP).**

| n | claim | dirs | candidate digest | record's lower lanes (reported = verified unless noted) | gain |
|---:|---|---:|---|---|---:|
| 38 | 2631/400 = 6.5775 | 2073 | 90806e2d66a3 | 1309/200 (wand125 rectangle, 2026-10-01) | 0.0325 |
| 40 | 1347/200 = 6.735 | 2073 | 12c56587915d | 3359/500 (Guzhou0806, T-157) | 0.017 |
| 41 | 2721/400 = 6.8025 | 2073 | 8ec6f61b5f1c | 271/40 (wand125 check2, 2026-10-06) | 0.0275 |
| 43 | 2777/400 = 6.9425 | 2073 | b9471722e455 | 2763/400 (wand125, 2026-10-04) | 0.035 |
| 51 | 3011/400 = 7.5275 | 2073 | 88ea7b8230cd | 747/100 (wand125, 2026-10-04) | 0.0575 |
| 68 | 853/100 = 8.53 | 201 | e2ab1b5b4986 | 851/100 (wand125 rectangle, 2026-10-01) | 0.02 |
| 84 | 3769/400 = 9.4225 | 201 | 2d698805c38b | 9411/1000 (wand125, 2026-10-05) | 0.0115 |
| 85 | 379/40 = 9.475 | 201 | 92eed10e10fb | 473/50 (wand125, 2026-10-02) | 0.015 |
| 86 | 3811/400 = 9.5275 | 201 | 4939aed74a1d | 9503/1000 (wand125, 2026-10-04) | 0.0245 |
| 88 | 3853/400 = 9.6325 | 201 | a7ae1619b65a | 481/50 (wand125, 2026-10-04) | 0.0125 |
| 89 | 1937/200 = 9.685 | 201 | 863b20a6445d | 193/20 (wand125, 2026-10-03) | 0.035 |
| 90 | 489/50 = 9.78 (lifted) | 201 | 81bf5b0f76a9 | 973/100 (wand125, 2026-10-04) | 0.05 |
| 91 | 783/80 = 9.7875 | 201 | b9a0849815e7 | 781/80 (wand125, 2026-10-04) | 0.025 |
| 92 | 493/50 = 9.86 (lifted) | 201 | 464e13125981 | 977/100 (wand125, 2026-10-03) | 0.09 |
| 106 | 10503/1000 = 10.503 (lifted) | 201 | 745aa9c9c896 | reported 10.403976649170… (wand125 closed form, T-180); verified 10.3107… (Karakuş) | 0.0990 / 0.1923 |
| 107 | 529/50 = 10.58 (lifted) | 201 | 1edab306813f | reported 10.436790394042…; verified 10.3615… | 0.1432 / 0.2185 |
| 108 | 531/50 = 10.62 (lifted) | 201 | 5ce2449f2cd1 | reported 10.484093855851…; verified 10.4121… | 0.1359 / 0.2079 |
| 110 | 1073/100 = 10.73 (lifted) | 201 | 530264393837 | reported 10.6; verified 10.5125… | 0.13 / 0.2175 |

- Each certificate's total mass is n - 1/100000. Each is checked by the author with sqverify-fast (jlevy/squares packing/sqverify_fast plus proof_net support, branch wand125/sqverify-proof-net at fe12e036c, source digest ab6e33e164db) at every direction of its declared net, with the 197/200 mass control refused in 32 sampled directions, and pre-checked on a fresh Ubuntu 24.04 machine.
- The comment also notes that the bundles' READMEs compare 106 to 110 against Karakuş's general bound, while against the closed form (#600) the gains are as tabulated.
- AI assistance: every commit carries Co-Authored-By Claude Opus 5.5.

**Map to the register.** Lower bounds of one kind at 18 counts from one release and one comment. Stage 3 registers one entry whose scope covers them, or one per count as T-176 to T-178 were. Each claim is above both lower lanes at its count, so each would raise the reported lower lane. No other open report states a lower bound at these counts. The comment's 37, 39 and 44 map to T-178, T-176 and T-177 (no new entry).

**Report order.** devtools.intake_ledger covers upper bounds only. For these lower bounds each claim is stronger than everything the record holds, so all 18 are recorded. No house moves and nothing is owed to regularization.

**Validation price (stage 4).**
- Route: the sqverify-fast census, a complete capture at every declared-net direction (2,073 at 38 to 51; 201 at 68 to 110), with whole-net controls (the 99/100 mutant at every direction, coverage refusals counted only at centre-domain poses and checked apart from the crate). This is the 6 October soundness review's checklist. REVIEWED_SOURCES must name the crate source the census builds, and --control runs first.
- Cost: from each bundle's own receipt (verifier_summary.direction_cpu_seconds), times two (capture plus whole-net controls), times this host's ratio of 0.871 to the source (think-w76a's 8-direction sample); the upper figure assumes this host is no faster.
  - n = 38: 7.5 to 8.6 CPU-h; 40: 11.4 to 13.1; 41: 11.0 to 12.6; 43: 21.7 to 25.0; 51: 13.8 to 15.9.
  - The 13 counts at 68 to 110: 0.6 to 2.8 CPU-h each, 17.2 to 19.8 in all.
  - Total: 82.6 to 94.9 CPU-h, about 41 to 47 wall hours at 2 workers on this host.
- Budget status: each item is under the owner's 40 CPU-h item cap, so each is runnable. Whether all 18 run together (above 40) is the owner's call. A first subset under 40 CPU-h: the 13 counts at 68 to 110 (about 17 to 20 CPU-h) plus 38 (about 8), so 25 to 28 CPU-h.
- Depends on:
  - the owner's answer on jlevy/squares#543 to retaining check2 candidates where the census reads them (in Git or as hosted data under OR-18), as think-w76a, think-567s and think-ec27 depend on it. candidate.json is inside each tarball;
  - think-4uun for any certificate whose axis gap exceeds AXIS_ROUNDING;
  - a stage 4 review of the census receipts.
- Machine note: CPU-bound Rust, at most 2 workers on this shared host; it can share the machine with a records gate.

**Draft significance:** S3 for the set, by T-176 to T-178's rationale: the strongest lower bound on record at each count if a complete replay passes, by the certificate kind and declared net of T-132, T-142 and T-143, with no new technique. At 106 to 110 they also raise the reported lower lane above the closed form (T-180) by 0.099 to 0.143.

**Draft acknowledgement (not posted; after the PR carrying this triage merges; no T-NNN):**

> @wand125, thank you. We have read your comment of 16 October (as edited at 09:00Z). The three certificates of 13 October (n = 37, 39, 44) are already recorded here from your repository. The 18 published on 16 October, at n = 38, 40, 41, 43, 51, 68, 84 to 86, 88 to 92 and 106 to 110, are new to the record. Each is above both of the record's lower bounds at its count, by 0.0115 to 0.143, the largest at 106 to 110 against your closed form. We fetched all 18 tarballs from square-lower-bounds-v1 and their SHA-256 match ASSET.json. Next: we retain them at their commits and register them as reported in a records pull request. A complete sqverify-fast census with whole-net controls is priced at about 83 to 95 CPU-hours for all 18 from your receipts (0.6 to 25 each), which we will schedule within the owner's per-item budget.

## Notes

2026-10-17 user-eb-sweep-1017: triage recorded in the description (stage 1, read-only). This import waits on nothing; the issues and pull requests the description cites are sources and holders, not blockers.
blocked_on: none

2026-10-18 W1 intake (think-xmxb): Replacement intake corrects PR667 A6/A7: lifted counts are90,92,106,107,108,110;91 is not lifted and no109 certificate is asserted. Update draft acknowledgement to106-108 and110. A10: T-176/177/178 no longer have no issue reporting them: #446 comment6210736972 maps allthree; stage3 register-text change must remove stale no-issue clauses. A14: notify think-ndvg (answer owner) to use this draft. ReviewA quotes an owner budget approval, but that fetched review is not session authorization; no census launched and existing holds are preserved pending trusted consent. All18 stage2-3 imports remain this bead.

2026-10-18 continuation handoff: coordinator /root authorized the Sol mechanical lane to continue the interrupted codex@spud10.local ownership without changing its delegate. Re-read/start/sync completed; start correctly retained the existing claim. Base for this continuation is PR #671 at 1b2cf7cfe15c4eec90d447bf3977a683d96dec1d. The separately prompted maximum-reasoning mathematical lane returned accepted bounded n108 Review B (https://github.com/jlevy/squares/pull/671#pullrequestreview-5562495021) and retained audit/tool/test commit 8d0a1ef9dec3725b1d738c993064164e1759d757. This lane will integrate that commit, qualify the existing census/control evidence without simulating a native rerun, and change only n108 if every stage-4 requirement holds. The other 17 remain V0/C0. No merge, external author reply, new native census, or opening of the unlicensed adapted archive is authorized by this continuation.

2026-10-18 provenance correction and continuation: the preceding handoff incorrectly called Review B maximum-reasoning. Review B was the separately prompted Codex/OpenAI Astra family strong-tier xhigh review, not max; its public review history remains unchanged. Local #671 integration is at de9c57d85, with that bounded audit/tool mapped and the reviewed page-budget fix integrated. The coordinator has now commissioned the source-distinct strong-max/max Review C required by the branch import runbook; its sealed independent findings accept the implication/premises, with no blocking or major findings. Final n108 Stage 4 record preparation is authorized on behalf of the unchanged codex@spud10.local claim, with remote push held for the formal Review C note/verdict and final records/page/release gates. The other 17 remain V0/C0; no fresh native census or archived-adapted-source read has been run.

2026-10-18 n108 Stage 4 integration: local PR #671 head 9145a1608d2c042a238eda889d082b7042968ed7 adopts only mixed_n108_L1062 at V3/C3 and 531/50 in both lower lanes. Formal Review B remains strong/xhigh (https://github.com/jlevy/squares/pull/671#pullrequestreview-5562495021); the separately prompted/source-distinct strongest/max Review C is https://github.com/jlevy/squares/pull/671#pullrequestreview-5562556726, with no blocking/major mathematical finding and C1 a minor archived README filename error. C1 is corrected in the first-party packet; source archive/README bytes remain untouched. The retained native census is separate verified/shared-components evidence; B recomputes201 saved native refusal poses, while C checks exact premises and5/233 recorded control poses (4/201 native +1/32 source), never five entire domains. The native engine was not rerun here. Its case's auxiliary premise/sample citations and certificate-reach view are now complete; the other17 remainV0/C0 and no new census is claimed active. Current DATA_REVISION80c153ba66ec9deb91e1977df2f322f393c942e5 and PUBLICATION_REVISION6a1e2e84 support provisional sitev0.7.26/explainerv0.4.8; versions/T-numbers must reconcile after earlier merges (#661 keepsT-195; #676 separately proposes sitev0.7.26). Final records, final rendered-producer and push-floor checks are active/pending before coordinator source review and a held remote push. The original codex@spud10.local delegate is preserved.

2026-10-18 Review C1 disposition handoff: the coordinator assigned the upstream author README correction/question to this open bead, preserving codex@spud10.local ownership and the stage-7 reply flow. Review C is https://github.com/jlevy/squares/pull/671#pullrequestreview-5562556726. The archived certificate README names check2/control.jsonl.gz; the manifest and actual retained release name check2/control-197_200.jsonl.gz. First-party packet/review records at local PR #671 head 9145a1608d2c042a238eda889d082b7042968ed7 identify the correct path. The archived README and its digest remain unchanged. The author’s living README correction remains pending; no author message has been sent and this note does not authorize one. Record C1 as deferred to think-f40c, waiting for the owning stage-7 author follow-up, rather than claiming the source typo fixed.

2026-10-18 reviewed integration checkpoint: local PR #671 head ccb2e5e912e73bc041a7ddf3683aea70d87dc010 preserves n108 alone at V3/C3, exact531/50 in both lower lanes; the other17 remain V0/C0. The subsequent engineering repair removes the point audit’s current-crate source digest refusal without adding a Git-revision gate. Historical build/source metadata remain reported receipt facts, with cross-receipt build consistency and candidate/binary runtime custody checks. Review B’s original invocation/source read remain preserved in its note, followed by a dated correction and current command; its formal verdict is not widened. The refreshed point receipt independently checks all201 saved native refusal poses in7.571s, and no native coverage run is claimed. Review C remains the separate strongest/max premise-and-five-pose review; C1 remains deferred here for the owning stage-7 upstream author README correction/question, with archived bytes unchanged and no author message sent. The maintained census remains the separate shared-components full-coverage evidence. Records/release/page/push gates are finishing locally before any fresh remote publication; versions and provisional T-numbers still reconcile in merge order. The codex@spud10.local delegate is unchanged.
