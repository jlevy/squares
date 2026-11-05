---
type: is
id: is-01m6n86trbv1javs88wtdd2j24
title: "Import Özden: s(94) >= 2493/250 by rescaling Hosono's mixed_n94_L995 onto a 4,972-direction net (#910)"
kind: task
status: in_progress
priority: 1
version: 8
delegate: bold-ritchie-l49
labels:
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
child_order_hints:
  - is-01m6na15dgp4fwgm2d24mcwk2w
  - is-01m6na2ne3zs2jq13j0b5n3a7x
hold: null
hold_until: null
created_at: 2026-11-05T07:01:41.771Z
updated_at: 2026-11-05T19:03:42.911Z
started_at: 2026-11-05T07:01:46.219Z
---
Import of jlevy/squares#910 (opened 2026-11-05T06:51:55Z by kenaznia-doga, an AI agent account posting for Doğa Özden): s(94) >= 2493/250 = 9.972, above T-262's 1993/200 by 7/1000. An exact rescaling of Hiroaki Hosono's mixed_n94_L995 measure by 4986/4975 onto a declared net of 4,972 half-angles (step 1/12000), decided by the lab with this repository's unmodified sqverify-fast; "not a new packing arrangement".

## Claim map
- Source: kenaznia-doga/s94-lower-bound-9972@7d21f9bdf707102dd4ebf47e52f81b502a01004d (one commit, 2026-11-05T06:51:31Z, 24 seconds before the issue). Certificate certificate/n94-L9972.json.gz (format M; L = 2493/250, B = 24872661/24875000, proof_net step 1/12000, last 4971; 853 orbits, mass 9399999/100000). Stated digests: .gz f59d4c95...360c (native input_sha256), JSON text d1df3bc6...951c; Hosono's candidate.json at wand125/square-packing-bounds@797bdf6e 64d81953...0667a, its retained gzip df3ae678...d27c; complete receipts .gz 041284d5...7a59 and JSONL 02906bb0...312a; 99/100 mutant .gz 2f72d2dd...1532; LICENSE.md 5b8e1449...a18da4c.
- Claims in the release: (1) s(94) >= 2493/250 [register: a new lower-bound entry; T-262 keeps its claim, superseded at n = 94 once adopted]; (2) native sqverify-fast receipts (crate source d97758bb, rustc 1.98.0, release) VERIFIED at all 4,972 directions, assembled from six disjoint-selected native streams A-F, least certified bound 1.0000000000003892 at r = 3663; (3) a two-direction 99/100 mass control refused natively at r = 0 and 1198 with an exact witness at 1198 capturing 0.991109005346039... (not a whole-net control); (4) the lab's exploratory C checker at all 4,972 directions (not interval arithmetic; supplementary, not offered as evidence); (5) answers to #890's review notes F3-F5 (the quadrant via the D4 symmetry; growth m_old(t) - m_new(t)/lambda, not rho(1 - 1/lambda); the n = 31 aside not reused) and to #890's second question (the route ceiling 99500/9977 stays; no claim for the 49,707-direction 9.97285 partial).
- Consequence: s(95) >= s(94) settles nothing (n = 95 and 96 are proved = 10, T-191).
- Who else holds the value: nobody; the record's best at n = 94 is 1993/200 (T-262, V3/C3), verified and reported.
- Credit: Doğa Özden after Hiroaki Hosono, Tokoharu and this project (T-262's form). AI assistance as given: AI agents in Özden's lab (Claude and OpenAI Codex agents) constructed and rescaled the certificate, ran the checks, audited the receipts and prepared the submission under his direction.
- Licence: LICENSE.md, byte-identical to the declaration #890's packet retains (blob 9803370f): CC BY 4.0 for certificates, witnesses, receipts, data and write-ups; MIT for the lab's code. Hosono's MIT notice and the crate's own licence retained.

## Validation plan (priced)
- Replay: this repository's sqverify-fast (reviewed source d97758bb) through devtools.sqverify_fast_census over all 4,972 declared-net directions, then the whole-net control (--control). Priced on the validation bead under this one.
- Review: a separately prompted stage 4 mathematical review (tbd-strong-max), briefed on its own bead under this one.

Answer bead: this bead.

## Notes

2026-11-05 (bold-ritchie-l49): stages 1 to 3 done on branch claude/bold-ritchie-xo28us-l49, draft PR https://github.com/jlevy/squares/pull/912 (labels intake and S3). Packet ozden-s94-lower-bound-9972-2026-11-05 at 7d21f9b; every stated digest holds; audit PREMISES_HOLD and RECEIPTS_HOLD; 13-direction sample with the census binary agrees; T-266 registered. Replay: think-qcms (priced about 19.4 CPU-h, runnable, not held). Stage 4 review: think-xzxd.

2026-11-05 ~10:00Z (bold-ritchie-l49): the stage 4 review of record (think-xzxd, tbd-strong-max, separately prompted) accepts the certificate with no defect, F1 to F7 all notes, S3 confirmed; retained on #912 as docs/project/reviews/review-2026-11-05-ozden-s94-9972.md with its programs and receipts under the packet's review/review-2026-11-05/, E-ozden-910-n94-9972-review-sample (sampled, 26 of 4,972 directions, independently re-implemented, clean room), the external_review on the report entry and T-266's reviews: T-266 V0/C1. F4 to F6 fixed in the records; F7 followed by the census control. The census of think-qcms started at 09:50:55Z (detached, nice 19, 2 threads, this branch's census code with #892's enclosure rule; scratchpad/scripts/run_census.sh). Owed after #911 merges: merge origin/main into the branch (rehearsed on local l49-trial-merge at 530a9985d: register T-265 then T-266, #895's note then #910's entry, regenerate views, synopsis row 266/234, record reason 265 -> 266, re-pin). Owed after the census and control pass: E-ozden-910-n94-9972-sqverify-fast-replay with the review as audit_record, T-266's rungs as check_results derives them, n-094's verified lane 1993/200 -> 2493/250 under the house rule, and this reply revised to say so.

2026-11-05 ~19:30Z (bold-ritchie-l49): census and control done (think-qcms). Census 09:50-18:25Z, 4,972/4,972 VERIFIED, 59,955.8 CPU-s (16.65 CPU-h), 30,876 s wall, 2,462,923,881 nodes, least leaf bound 1.0000000000003892 at 3663, exact leaf capture 1.0336; control 18:25-18:36Z CONTROLS_REFUSED (original verified at 3663, 99/100 mutant refused at 4,972/4,972, near-threshold mutant refused; axis enclosure [0.9930559807565953, 0.9930559830055209]). audit_dilated_measure compare against the lab's merged archive: EVERY_DIRECTION_AGREES (4,972 identical on every field the lines keep, timings aside; node totals equal), receipts/replay-comparison.json. On #912 at 79d9946b9: E-ozden-910-n94-9972-sqverify-fast-replay (audit record the stage 4 review), T-266 V3/C3 as check_results derives, n-094's verified lane 1993/200 -> 2493/250 (T-262 superseded there), credit attributions moved to T-266; main 249bb82e7 (#913) merged at ac8b8e0be; DATA_REVISION re-pinned at 3560857ee. The reply below is revised to say so. PR stays a draft until the coordinator's senior review.

Stage 7: no acknowledgement is owed before the merge. This PR registers the result, so the reply below is the import reply, and by result-import.md stage 7 it follows the merge. Post it only after the PR merges and the deploy is verified: render from main with `check_requests --draft 910` (it refuses off main), check that main and the site say what the reply says (T-266's rungs, n-094's lanes), adjust T-266 if renumbered, post, then record it under #910's replies (kind: final, closing the issue) in the next change. If the census has landed by then, the reply states T-266 confirmed and the verified lane moved; otherwise it names think-qcms as what remains.

DRAFT of #910's reply (not posted; revised for the stage 4 review and the census replay of 5 November):

---

Thank you, @kenaznia-doga, for posting this, and thank you to Doğa Özden (@dogaozden), whose result it is. This reply records what was done with #910 and closes the issue.

**Received and retained.** `kenaznia-doga/s94-lower-bound-9972` at `7d21f9b`, kept whole as the source packet [`ozden-s94-lower-bound-9972-2026-11-05`](https://github.com/jlevy/squares/blob/main/packing/resources/web/ozden-s94-lower-bound-9972-2026-11-05/README.md), except `.gitignore` and `source/hosono-candidate.json.gz`. That gzip is byte for byte the copy this repository already keeps of Hosono's `candidate.json` for T-091, so it is pinned by digest rather than copied twice. Every digest the issue states holds:

- the candidate gzip (`f59d4c95…360c`) and its canonical JSON (`d1df3bc6…951c`);
- Hosono's source JSON (`64d81953…0667a`) and its retained gzip (`df3ae678…d27c`);
- the complete receipts, `041284d5…7a59` as stored and `02906bb0…312a` decompressed;
- the 99/100 mutant (`2f72d2dd…1532`);
- `LICENSE.md` (`5b8e1449…a18da4c`), which is the same file #890's packet keeps.

**What was checked here.**

- **Premises and the dilation.** `devtools.audit_dilated_measure` recomputes these in exact rationals from the retained bytes:
  - format M on the declared net, and lemma N0's five conditions, with B(1 + D) = 99498934887/99500000000 < 1;
  - the last tangent 1657/4000 covering the endpoint: t² + 2t − 1 = 1649/16000000 > 0;
  - the total mass 94 − 1/100000;
  - each of the 853 rows exactly λ = 4986/4975 times Hosono's, with its mass unchanged;
  - the certificate's text and its gzip, both regenerated byte for byte from Hosono's candidate by the rule `tools/rescale.py` states.
- **Your receipts.** The same tool audits the archive from the retained files, without running anything:
  - Each of the six native runs holds exactly its stated scope.
  - Each run's summary states the certificate's premises and refuses nothing.
  - Each run is a build of the reviewed crate source `d97758bb…`, with the same compiler, profile and target as our census binary.
  - Your copy of the crate is that source.
  - All 4,972 directions appear once, each verified at threshold 1 with a finite bound of at least 1, and each selected line is byte for byte its run's line.
  - The least leaf bound of the search is 1.0000000000003892, at direction 3663. As your README says, it is where one search leaf stopped, not a margin. The review below finds the capture at least 1.0035 everywhere at 3663.
- **Your control.** The mutant is every mass times 99/100 and nothing else. At direction 1198, your rational witness captures exactly the stated 0.991109005346039…, in the per-bin domain and the searched quadrant, where the original captures 1.00112…. The crate's own witness there, and the axis sweep's least vertex at direction 0, also capture below 1 when recomputed exactly.
- **A sample.** This repository's census binary ran 13 directions, including 0, 1198, 3663 and 4971. All verified, with your certified bound at each and your node count wherever your line records one.
- **A mathematical review.** A separately prompted review lane of this project, a Claude agent at the strong tier, [accepted the certificate](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-11-05-ozden-s94-9972.md) with no defect. It is an AI review, not a human one.
  - It recomputed every premise but whole-net coverage exactly.
  - With clean-room code of its own, written from `SOUNDNESS.md` without reading any checker's source, it decided 26 of the 4,972 directions over their whole quadrants: direction 0 exactly, the other 25 with proved bounds. All are verified, and the least capture it found is above 1.0010, at 1198.
  - It held your control's witnesses exactly and read your archive as data. Your 67 repeated directions agree in bound and node count, and compaction removed nothing the proof needs.

- **A complete replay.** This repository's census ran `sqverify-fast` (the reviewed source, our binary) at all 4,972 directions on 5 November: every direction verified, 2,462,923,881 nodes, the least leaf bound 1.0000000000003892 at direction 3663, where the exact capture at that leaf's centre is 1.0336. It took 16.65 CPU-hours at two threads. Every direction's row equals your selected archive line on every field the line keeps, timings aside, and the node totals are equal.
- **A whole-net control.** The original verified again at 3663; the 99/100 mutant was refused at all 4,972 directions, each at a centre whose exact capture is below 1; and a near-threshold mutant was refused with an exact witness. At the axis the control is judged by our census's enclosure rule.

**What is recorded.**

- [T-266](https://squaremath.org/results.html#t-266), `s(94) ≥ 2493/250`, at **V3/C3**: confirmed, reproduced with the producer's code, since your runs used the same checker. The review's own clean-room sample is recorded beside it as independently re-implemented.
- n = 94's [lower bound](https://github.com/jlevy/squares/blob/main/packing/frontier/n-094.md), reported and verified, is now 2493/250, 7/1000 above T-262, which it supersedes there.

**On your answers to #890's notes.** The review finds them right as far as this packet shows. The growth formula is as you now write it. At the 20 nodes your net shares with Hosono's, the centre domain grows by between 1.93e-4 and 1.52e-3 in his coordinates, and by 11/9972 at the axis. The other 4,952 directions are new. Measured the same way, #890's net gives the 6.55e-5 to 1.062e-3 that the earlier review reported.

**Notes from the review**, for the repository if you want them; none affects the bound:

- **F1.** `source/README.md:35` says the C front end's maximum with the core's half-width can make its quadrant smaller. It never binds: ρ(a_r) − Bρ(t_r) ≥ 5.36e-6 at every node (least at r = 1), so the two quadrants coincide.
- **F2.** "An independent implementation" (`source/README.md:64`, also `:39`) is meant relative to your exploratory checker. To this record, `sqverify-fast` is the producer's checker, and our replay is reproduced with it. Saying "independent of our exploratory checker" would remove the ambiguity. "Authentic" (`:39`) is your statement: the receipts carry no binary digest.
- **F3.** Stream E's indices are {0..19} ∪ {round(4971k/128)} ∪ {1195, 2590}, a rule the packet states only in `tools/audit.py`. Stating it, with the reason for 1195 and 2590, in the README or the index would let a reader check E without your code. Separately, the mutant's `derived_from` reads "multiplied by99/100".

**Three questions**, which hold nothing open:

1. What chose E's indices 1195 and 2590?
2. Do the pre-compaction streams B, C and D still exist? They are not needed for the proof, and our replay already agrees with every field they keep and with the total node count; their per-direction node counts would complete the row-for-row comparison.
3. The 49,707-direction run toward 9.97285: did any direction refuse, or were all unfinished? A refusal would locate where coverage first fails on this route, below the ceiling 99500/9977.

**Credit.** The record credits the certificate to Doğa Özden, after Hosono, Tokoharu and this project, as your README does. It states the AI assistance as the issue does: AI agents in Doğa Özden's lab, Claude (Anthropic) and OpenAI Codex agents, constructed and rescaled the certificate, ran the checks, audited the receipts and prepared the submission, under his direction. It claims no human review of the new certificate.
