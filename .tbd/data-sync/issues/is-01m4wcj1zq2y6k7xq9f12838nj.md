---
type: is
id: is-01m4wcj1zq2y6k7xq9f12838nj
title: "Import Benjamin Greff (bengreff): s(76) = 9 by a mixed cover (#594)"
kind: task
status: open
priority: 1
version: 7
delegate: null
labels:
  - result-import
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-14T05:01:01.303Z
updated_at: 2026-10-23T06:16:15.118Z
started_at: 2026-10-14T05:01:05.888Z
---
Stage 1 triage of jlevy/squares#594 (bengreff, Benjamin Greff, opened 2026-10-14T02:06:46Z, labelled intake, no comments when read at 04:44Z): "Exact value s(76) = 9 (k = 9 of the k² − 5 series): registration request (external certificate)". "External certificate" is wand125's title template of #279/#280: the author's own certificate in his own repository, not a citation of another's published result.

Source pin: https://github.com/bengreff/s76-certificate at 1cb924fa2fb7e8e30d8ddeb9b5e0dfcfae4f9f1f (tree b7c5ee885d529b258078afeb8687c68923269440, committed 2026-10-14T02:05:47Z, head of main when retrieved at 2026-10-14T04:45Z; four commits, the cover first committed in 7c78327 at 2026-10-14T01:57:08Z). MIT, Benjamin Greff. Retained whole in packing/resources/web/bengreff-s76-certificate-2026-10-14/ (151 files, about 1.5 MB, declaration-driven).

Claim map (result-import.md register table):
- s(76) = 9 (new exact value; the record holds s(76) open at 1793/200 = 8.965, T-091, n-076.md): one new entry, kind optimality, scope n = 76. Lower half: the mixed cover cover/s76_cover_v5.txt.gz (unpacked SHA-256 b6a1214b99f00e5dd136d74c8d87bccd178df38a1063b2c7be90517eb2b862b2), 41,633 points and 9,744 segments, D = 8000, W = 4e8, total 3788361049/50000000 = 75.76722098 < 76, exactly D4-invariant; upper half: the 9 x 9 grid (E-basic-grid-upper). No other count follows: the total is above 75, and s(77) to s(81) = 9 are already held (T-067, T-064, T-086, T-084, the grid).
- The covering statement is decided by a composite of Evan Daniel's two checkers, used unchanged from evand/square-packing@b91d70b6: zmx2 cert --d4 (6b7f0f79, outward-rounded binary64) certifies 8,096 of the 8,100 D4 roots and leaves 18 boxes in 4 roots (records/zmx2/failing_roots.txt); zm_mixed.py cert --d4 --cert-mode --disj --chain-from 0 --pitch 1/20 --ubins 16 --depth 24 (ee3e2915, exact rationals) certifies the 64 sub-roots of those 4 roots, 4,950 boxes, max depth 15, none uncertified; tools/check_coverage.py checks the tiling. No root rests on both checkers.
- Lean: lean/S76Lower.lean, theorem s76_eq_9 (hcov : S76Cover) : minSide 76 = 9 on Daniel's Sqpack at 1718a58 (Lean v4.33.1), axioms propext, Classical.choice, Quot.sound. Data facts kernel-checked (nodup, D4, total < 76); S76Cover (CovM on [0,9/2]^2 x u in [0,1/2]) is a hypothesis. Not a proof-assistant proof of the claim.
- In progress at the source: zm_mixed.py alone over all 129,600 D4 roots, 42,000 done with none uncertified when the issue was written; records to be published at a later commit (a new packet then; an evidence update, not a new entry).
- Construction (corners from wand125's s(59) cover with s(77)'s band insertion, cross re-optimised by LP): research code, not part of the proof; no claim to register.
- Stated next work: s(95) = 10 and s(116) = 11 by the same pipeline. Nothing to register now.

Credit read from the source: Benjamin Greff; after Evan Daniel (method at margin zero, mixed format, zmx2, zm_mixed.py, zeromargin.py, Lean library) and wand125 (the s(59) = 8 cover reused for the corners, the band-insertion construction). AI assistance, in the source's terms: "Benjamin Greff directed the work. The search, LP and verification pipeline were built and run with Claude (Anthropic) as an AI assistant" (README); the issue adds that Claude in Claude Code built and ran the LP search, export, verification script, coverage checks, Lean wrapper and replay, and drafted the write-up. No outside review. Lineage: independent (the source names no debt to this project; the issue reads n-076.md for the standing bound).

Validation plan, priced:
- Stage 4 replay (W2): the composite with the source's checkers from retained bytes, same-implementation. zmx2 --d4 is 239 to 436 CPU-s here; zm_mixed on the 64 sub-roots is 1,359 CPU-s at the source; both were run in this triage (notes). Still owed for C3: register case 76 in devtools.replay_evand_zmx2 and devtools.audit_evand_mixed_covers (a W7 slice: a zm_mixed composite audit, zmx2 root set plus sub-tiling, which neither tool reads today), commit receipts through them, and two mutated-cover controls refused by both checkers (seconds each).
- Stage 4 review (W2, separate lane): re-derive certificate to claim; trust boundaries as in review-2026-10-02-wand125-s59-s77-mixed-covers.md; the shapes new to the checkers: D = 8000, segments of length 1/16 (1,664), and 16 segments on the container walls x, y in {0, 9} (minimum weight 1/(4e8) each, 4e-8 in all), the first wall-line segments in any mixed cover this record holds; and the composite itself (zm_mixed partial-region options, tiling, D4 fold over a union of runs).
- Optional second sweeps: zmx2 --full (64,800 unreduced roots, about 1 CPU-hour by T-066's 8x ratio, plus zm_mixed on its failing images); the source's full zm_mixed pass, several hundred CPU-hours at 4 cores here (audit its published records instead, seconds).
- Lean: build of S76Lower.lean on Sqpack 1718a58, 15 min 21 s at the source, needs Mathlib's cache and more disk than this machine had (4.8 GB free). Discharging S76Cover in the kernel is the route wand125 took for s(59) at the same Sqpack (think-xk3f); unpriced here.

Draft ratings (registering lane's draft, for the reviewer): enters V0/C0 as reported (T-066's path), V3/C3 after the replay evidence and a review with no blocking defect, confirmation reproduced with the producer's code (Daniel's checkers, which the author ran); V4/C4 needs two adversarial AI reviews and a human oversight record; V5/C5 needs S76Cover proved in Lean and expert formalization review. S3 (a substantive case result), beside T-066 and T-067. Novelty previously-published (the source).

## Notes

2026-10-14, triage resumed after a container restart (Claude Opus 5.5, xhigh; worktree review-594 at aeef99ef0). Issue re-read at 05:2xZ: body unchanged since the 04:44Z read, no comments, label intake. bengreff/s76-certificate head still 1cb924f (git ls-remote).

## Spot checks (all receipts in the packet's receipts/; the comparisons re-run by receipts/programs/triage_checks.sh into receipts/n76_triage_checks.log)

- Packet = pinned checkout (diff -r, 151 files); the source's SHA256SUMS passes 150/150 (it omits itself); acquire_source --check PACKET_MATCHES_ITS_CONTRACT; retained_data check clean. Cover, records and Lean unchanged since the first commit 7c78327 (2026-10-14T01:57:08Z).
- Data facts: devtools.audit_evand_mixed_covers.audit_cover with the stated Case: total 3788361049/50000000 = 75.76722098 equals the stated, counts 41,633/9,744 as stated, D4-invariant entry by entry and as a measure, no point on a loaded line, no problems. The source's check_total.py agrees. Segments on x, y in {0..9}, lengths 1/500 (2,104), 1/50 (5,976), 1/16 (1,664); 16 lie on the container walls, 1/(4e8) each, 4e-8 in all.
- Lean data: every (X, Y, w) and segment of S76T_Pts.lean equals the cover as mk_s76_lean.py aggregates it; same total; S76Cover = CovM over centres [0, 9/2]^2, u in [0, 1/2], D = 8000, W = 4e8. Lean not built.
- Corner [0, 5/2)^2 = wand125's s(59) cover (6f4d2b64): 1,140 points and 452 segments, identical masses. The credit stands.
- zmx2 replay (6b7f0f79 built from retained bytes, rustc 1.97.0, binary cba78a9e): 8,100 roots, 14,672,104 boxes, 7,268,720 certified, 71,364 empty, 18 uncertified in the 4 roots of failing_roots.txt, none capped; 147 s wall, 239 CPU-s. Every root's census and all 18 UNCERT boxes identical to the source's zmx2_v5.log.
- zm_mixed.py replay (ee3e2915, bb89de15, 640fe453 from the retained evand packets, verify.sh's flags, 3 parallel): 64/64 VERIFIED-D4 (PARTIAL), 4,950 boxes, depth 15, 0 uncertified, 1,168 CPU-s; 04:52Z to 05:07Z. Headers (input path aside) and censuses (CPU aside) equal the source's 64 records. Read with exact fractions: 64 distinct 1/20 x 1/20 x 1/32 grid cells tiling the 4 failing roots exactly, settings and digests as pinned. The source's check_coverage.py accepts the replay's own logs. zeromargin.d4_roots covers the whole [0, m/2]^2 x [0, 1/2], so the partial-region filter selects exactly one root per job.
- Controls (zmx2, default uncert cap, one root each): drop-heaviest-segment (8 x 44176716/4e8 at (0.98..1, 4) and images) refused at x5 y35, 234 uncertified, float-min 0.8968; drop-heaviest-point (8 x 2514512/4e8 at (1.49, 1.87) and images) refused at x15 y15, 235 uncertified, float-min 0.9968. zm_mixed.py pose, exact: the mutants capture 0.896817460548 and 0.997358632856 at poses where the published cover captures 1.007259250548 and 1.009931192856, so both refusals are true. A zm_mixed sweep of a mutation at depth 24 was not run (refusal needs the depth limit, exponential).
- Wall control: zmx2 cert --d4 on the cover without its 16 wall segments (a253ed85): all 8,100 roots with identical census, box for box, same 18 boxes. No zmx2 decision depends on the wall segments, which no unit square needs (a flush square is a limit of squares moved off the wall).
- The zmx2-failing poses near the 3-4-5 angle: exact mu 1.0066 to 1.0231 (zm_mixed pose), so they are discontinuities, not violations; zm_mixed closes them.

## Assessment

What is proved, if the checkers are sound: every closed unit square in [0,9]^2 captures mass >= 1 from a measure of total 75.767 < 76, hence s(76) >= 9; with the grid, s(76) = 9. The reduction is the T-066/T-067 one (scaling to side 9, concentric closed unit squares, exact D4 invariance, u = tan(theta/2) in [0, 1/2] covering theta <= 45 deg), and the checker digests are the ones the 2 October review of the s(59) and s(77) covers read. It is a checkable machine certificate (interval-certified plus exact-rational), not a published citation or an assertion, and it is re-run here with the producer's code (relationship same-implementation). New to the record, for the review lane: D = 8000; segments of length 1/16 and 1/500 on integer lines; the 16 wall segments; the zmx2 + zm_mixed composite, with zm_mixed's partial-region options (--cx-lo .. --u-hi) and its D4 partial mode, the first time zm_mixed would back a confirmation here (verifiers.yaml V-evand-zm-mixed-py: no confirming entry runs it yet); and the corner/cross seam the source's note 3 names.

Novelty: no s(76) >= 9 anywhere the record looks: n-076.md open at 1793/200 (T-091, wand125); the literature archive (Friedman DS7: s(n^2-2) = s(n^2-1) = n, Nagamochi 2005; Kingbird lists 9 as best known); wand125/square-packing at c470527 (13 Oct: only mixed_n76_L894/L896/L8965 and rect_n76_*), evand/square-packing at fc094b1 (13 Oct: Exact/Packs/N76 is an upper-bound packing at 9). Novelty previously-published (the source), apparently first.

The series: s(k^2-1) = k (Nagamochi 2005; held via Karakus, T-084, since Lemma 1 is false, T-085), s(k^2-2) = k (T-086, chelokot's Lean), s(k^2-3) = k for k >= 3 (T-064 with Bentz), s(k^2-4) = k for k >= 5 reported (T-081, V0/C1; s(21), s(32), s(45), s(60), s(77) each C3). s(k^2-5) = k: only k = 8 (T-066); k = 5, 6, 7 (n = 20, 31, 44) open with gaps 0.095, 0.0475, 0.0275; k = 10, 11 (n = 95, 116) open; k <= 4 false (s(11) < 4). This certificate is one instance: its cross was re-optimised by LP, so nothing carries to other k without an insertion lemma for a periodic band (H-269's d = 5 cell, corner deficit > 5/4, open). The author's next targets, s(95) and s(116), are per-instance runs.

## Ratings draft (registering lane's draft, for the reviewer)

Enters V0/C0 as reported. V3/C3 needs the replay evidence entry (zmx2 + zm_mixed composite, receipts committed) and a stage 4 review with no blocking defect: confirmation reproduced with the producer's code. V4/C4: two adversarial AI reviews by distinct reviewers and a human oversight record. V5: S76Cover proved in Lean (kernel discharge, as wand125 did for s(59) at the same Sqpack, think-xk3f) and an expert formalization review. S3, "a substantive case result", beside T-066 and T-067: an exact value for an open case by the recipe the record already holds, with no new technique.

## Not checked, priced

- Lean build of S76Lower.lean: Lean v4.33.1, Mathlib cache (about 5 GB) and Sqpack at evand 1718a58, which no packet retains (think-ilwc owns the read); 15 min at the source, about 45 to 90 min here plus the download; 12 GB free.
- zmx2 cert --full (64,800 unreduced roots): about 8x the D4 run, 0.5 to 1 CPU-hour, plus zm_mixed on the images of its failing roots.
- The source's full zm_mixed pass (129,600 roots): several hundred CPU-hours; audit its records when published (minutes).
- W7 slice owed for C3: register case 76 in devtools.replay_evand_zmx2 (CONTROLS: drop-heaviest-point d4 x15 y15, drop-heaviest-segment d4 x5 y35) and devtools.audit_evand_mixed_covers, plus a zm_mixed composite audit (zmx2 root set plus sub-tiling) that neither reads today; then evidence entries. About 2 to 4 hours of agent work.
- S76Cover kernel discharge: unpriced (wand125's s(59): 6,400 root cells, 290 batches, 43,154 generated files).

## Packet

Finished per stage 2: README, Original Gzip and Compressed Files tables, bibliography key [bengreff s76 certificate 2026-10-14] (Greff after Daniel, wand125; lineage independent, as the source states it) with credited name Benjamin Greff, resources README rows, receipts. Committed as e25e1c1b6e0bf1aa11b7dee97ea7847e6860f105 and pushed to claude/wizardly-meitner-wqn4x3-review-594 (no pull request opened). Not edited: results.yaml, evidence, coverage, result-requests.yaml, SYNOPSIS.md, case records. No person record in atlas/known-best/credit-attributions.json: the owner sets those.

## Draft acknowledgement (not posted; stage 1, no T-NNN, no rung)

Thank you for the report, and for publishing the cover with the run records of both checkers. We have pinned bengreff/s76-certificate at 1cb924fa2fb7e8e30d8ddeb9b5e0dfcfae4f9f1f and retained the whole tree here, with the credit and AI-assistance statements as your README and this issue give them.

In triage we ran your certificate with Evan Daniel's checkers, built from the copies this repository already holds at the digests your verify.sh pins. zmx2 cert --d4 leaves the same 18 boxes in the same four roots, with every root's census equal to records/zmx2/zmx2_v5.log, and zm_mixed.py with your flags certifies all 64 sub-roots, with records equal to yours apart from the input path and the CPU time. The total, the D4 invariance and the tiling check exactly, the corners are wand125's s(59) cover as you say, and the Lean data matches the cover file. Two mutated covers are refused by zmx2, and zm_mixed.py pose finds a pose in each where the capture is below one.

Next, the result is registered as reported, and a separate review of the mathematics, including the composite of the two checkers, decides how it stands. When the full zm_mixed.py pass is published, please post its commit here: we will retain it as a new revision. One small question: the cover carries sixteen segments of mass 1/(4·10⁸) on the container's walls. They change no zmx2 decision (we checked), so they look like LP residue; were they intended?

## Validation of the commit

packing-validate --push: all 16 edit checks passed (basedpyright and the browser floor included); its reachable-tests phase selected the whole suite and was stopped at the 25-minute limit under a load average near 20, unfinished, no failure reported. The tests reachable from the change then passed directly: 640 passed in 348 s (test_bound_citations, test_acquire_source, test_acquire_original_gzip, test_retained_data, test_retained_json, test_retained_json_layout, test_results_register, test_state_ai_assistance, test_check_archive_annotations, test_certificate_citations, test_evand_mixed_covers, test_intake_sweep, test_check_requests). acquire_source --check: PACKET_MATCHES_ITS_CONTRACT. The lefthook pre-commit hook did not run in this worktree (lefthook not on PATH); packing/resources/README.md was formatted with the pinned flowmark-rs 0.4.0 before the commit, and packet READMEs are excluded from flowmark.

Registered on 2026-10-14 in the 14 October records PR (branch claude/wizardly-meitner-wqn4x3-records-1014): T-184, s(76) = 9, V0/C0, S3; the author's second route at 06993982 (comment of 14 October) is not yet retained.

## 2026-10-15 reads lane (think-mq0k, branch claude/wizardly-meitner-wqn4x3-reads-1015): the second route at 06993982, and #594's comment on the wall segments

**Pin.** bengreff/s76-certificate 06993982e83dba37ca12121bd876396a15571fcb (2026-10-14T08:16:10Z, "Add the second route: zm_mixed alone over the whole region, with R rerun at depth 34"), one commit past the packet's 1cb924f and the head at the 02:30Z sweep. Not retained (no packet pins it). It changes README.md, SHA256SUMS, records/toolchain.txt and verify.sh and adds records/zm_full/ (roots.jsonl.gz, manifest.json, full.log.gz, rerun.txt, rerun_R_depth34.{jsonl,log,sh}) and tools/check_full.py. The cover, the zmx2/zm_mixed composite records and the Lean are unchanged. The tree's SHA256SUMS (158 lines) passes on the extracted archive.

**The source's claim.** zm_mixed.py (ee3e2915, bb89de15, 640fe453, the pinned digests) with verify.sh's flags over all 129,600 roots of [0, 9/2]^2 x u in [0, 1/2] at pitch 1/20 x 1/20 x 1/32, depth 24, 24 processes: 2,227,114 boxes, 129,599 roots certified, 6 boxes uncertified in one root R = [27/20, 7/5] x [13/10, 27/20] x [1/4, 9/32]; R alone at depth 34 certifies with 13,767 boxes, max depth 26, none uncertified. 651,314 CPU-s (181 CPU-h, 27,729 s wall on 24 processes, i7-14700K) and 2,661 CPU-s for R. R lies in the corner inherited from wand125's s(59) cover; the README says wand125's own full s(59) zm_mixed run left the same 6 boxes in this root, and the same 13,767 at depth 34 (not checked here). So the covering statement rests on zm_mixed's exact rationals alone, without zmx2's binary64.

**Records audit here (seconds; my script, not the author's).** roots.jsonl.gz decompresses to the manifest's records digest 564bac26108eaae6...; one header (cover b6a1214b..., checker digests as pinned, D4, depth 24, pitch 1/20, ubins 16, cert_mode, the whole region); 129,600 records, no duplicates, exactly the 90 x 90 x 16 grid cells; every census sum equals the manifest's (boxes 2,227,114; CPU 651,314 s); max depth 24; exactly one root with uncertified boxes, R, UNCERT 6 with six listed boxes; the rerun record's header names the same digests at depth 34 and region R, and certifies R with 0 uncertified. Per-root CPU: median 0.07 s, p99 92 s, max 2,270 s (R). check_full.py (stdlib, 59 lines) was read, not run; it does not check the rerun's other settings beyond cert_mode, D4, pitch and ubins, nor the manifest's records digest, which this audit does.

**What it adds to T-184's rung.** Nothing moves by itself: T-184 stays V0/C0 until the replay evidence and the review land. It gives the review a second route that drops two trust elements of the first, zmx2's outward-rounded binary64 and the composite's tiling and D4 fold over a union of runs, leaving one exact-rational checker (still Daniel's, so same-implementation, no independence gain for the C rung). Its records agree with the composite: the 64 sub-roots of the four zmx2-failing roots are certified in the full run too, and R is certified by zmx2 in the first route. T-184's note "The source's full zm_mixed.py pass over all 129,600 D4 roots is not at the pinned revision" is out of date once a packet pins 06993982; that packet and an evidence update are this bead's (new revision, no new entry).

**Replay, priced (not run).** Whole second route: 181 CPU-h at the source; here about 155 to 181 CPU-h (the triage's 64 sub-roots ran at 0.86x the source's CPU): HELD under the owner's 40 CPU-h cap (think-lh7d). R alone at depth 34: 2,661 CPU-s, single process, about 40 to 45 min wall here: over this lane's 30-minute ceiling, not run; runnable within the cap. A random sample of roots is cheap (mean 5 CPU-s a root, so 200 roots is about 17 CPU-min) but a sampled replay is never confirmation. The composite replay already done in triage (zmx2 239 CPU-s + zm_mixed 1,168 CPU-s) remains the cheap C3 route.

**#594 issuecomment-6181807169 (bengreff, 2026-10-15T00:50:37Z), the answer to the triage's question.** The sixteen wall segments were not intended; they are LP residue. Every 1/20-lattice point on an integer line had a candidate segment of length 2/1000 along that line (one along each line at a crossing: 81 on the wall x = 0 inside the cross, with images); the interior-point solve without crossover gave weight 0 to all but four D4 orbits, at the crossings (0, 3), (0, 4), (0, 5), (0, 6) and images, about 1.04e-12; export_cover.py rounds every weight up to the unit 1/(4e8), so each became one unit. Rounding up only adds mass, and their 4e-8 is in the stated total. The horizontal partners at those crossings ([0, 2/1000] and [0, 1/16] on y = 3..6 and images) also carry one unit each, for the same reason. "The pinned cover stays as it is." This agrees with the triage's control (zmx2 decides every root identically without the 16 wall segments). Nothing to register; the review should record the answer. #594's read_through moves to this comment in the next records PR.

**Intake-watch read for the records PR:** bengreff/s76-certificate read_through 06993982e83dba37ca12121bd876396a15571fcb, read_on 2026-10-15, bead think-osvq (the second route, owned until a packet pins it).
