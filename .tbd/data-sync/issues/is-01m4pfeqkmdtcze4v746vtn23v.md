---
type: is
id: is-01m4pfeqkmdtcze4v746vtn23v
title: "Import wand125: register #446's s(19) >= 1931/400, s(20) >= 393/80, s(26) >= 1111/200, s(27) >= 1131/200 as reported (#446)"
kind: task
status: in_progress
priority: 2
version: 11
delegate: c-lower-1023
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-11T21:56:11.508Z
updated_at: 2026-10-24T03:31:43.704Z
started_at: 2026-10-23T06:18:58.822Z
---
Found by the 2026-10-11 wand125/evand survey (think-1jnr). wand125/square-packing INDEX.json at 04fbef0 (2026-10-11) lists, as its best certificate at four counts, the #446 fine-net bundles mixed_n19_L48275 (1931/400 = 4.8275), mixed_n20_L49125 (393/80 = 4.9125), mixed_n26_L5555 (1111/200 = 5.555) and mixed_n27_L5655 (1131/200 = 5.655, the bf85d6b follow-up), all on the 2,073-direction net, data in release square-lower-bounds-v1. The record holds them only as evidence (E-wand125-fine-net-lower-bounds-446-report, E-wand125-fine-net-n27-5655-followup-report), #446's result-requests entry and case-record blockers; no register entry states them, unlike the same release's n = 28, 29, 30 values (T-142, T-132, T-143). Each is above its case's reported and verified lower bound (by 1/400, 3/400, 1/100 and 23/2000) and above every register claim at its count (T-103, T-104, T-105, T-106). Runbook row: bounds of one kind at several counts in one release, one entry whose scope covers them, registered as reported (V0/C0, pending adoption) with unfinished_confirmations naming think-ndvg's replay. Price: registration minutes (records lane); replay about 3.3 to 4.5 CPU-hours per certificate on the T-142/T-143 measurements, so about 13 to 18 CPU-hours for the four, under think-ndvg's owner budget.

## Notes

Overlap: think-dc0p (in_progress since 2026-10-06, unlabelled, no notes) names the n = 19 value with three superseded ones from square-packing-bounds f8e0178; #446's import (PR #450, think-ndvg) superseded it. Owner of the replay: think-ndvg. This bead owns only the registration (one entry, scope n = 19, 20, 26, 27), for the records lane.

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): existing issue https://github.com/jlevy/squares/issues/446; its 2026-10-12 reply (https://github.com/jlevy/squares/issues/446#issuecomment-6116243055) does not yet mention this registration. Listed on the tracker https://github.com/jlevy/squares/issues/544.
2026-10-23 c-lower-1023 (records lane of coord-intake-1023), branch claude/intake-2026-10-23-lower-bounds: registered as T-233 (V0/C0, recorded, pending adoption at n = 19, 20, 26, 27) in 7b90d47d2, over E-wand125-fine-net-lower-bounds-446-report and E-wand125-fine-net-n27-5655-followup-report, published 2026-10-08 (n19 and n26 first in 7400660 on 2026-10-07, n20 at 61e37d5, n27 at bf85d6b 2026-10-08T16:53Z; all four directories unchanged through head e48de24). Gains over T-103 to T-106: 1/400, 3/400, 1/100, 23/2000. #446's requests entry maps fine-net-n19, -n20, -n26 and -n27-5655-followup to T-233; the issue's n27 2261/400 is superseded in the same release and stays unregistered. #446 has no new author comment after read_through 2026-10-16T09:00:31Z (later comments are the project's replies of 19 and 20 October).
- Price (unfinished_confirmations, think-ndvg): the four assets downloaded (digests equal the #446 packet's) and their check2 receipts read: direction CPU 3,584 / 8,353 / 8,158 / 12,676 s (n19 at 6 threads, the rest at 12), 32,770 in all; twice over each net at this host's 0.689 ratio (think-wop1's n31 sample) is 12.54 CPU-h, 18.21 at the source's CPU. Per certificate: n19 1.37-1.99, n20 3.20-4.64, n26 3.12-4.53, n27 4.85-7.04 CPU-h. No replay runs in this lane; a census needs each candidate retained where it reads it first (fine_net_followup retain into a packet, as wand125-fine-net-n31-2026-10-11 does).

## Stage 7 draft for #446, after this branch merges (not posted)

@wand125, thank you. Four more of your fine-net lower bounds are now registered on `main`, as reported results:

- **T-233, V0/C0, recorded:** s(19) ≥ 1931/400 (`mixed_n19_L48275`), s(20) ≥ 393/80 (`mixed_n20_L49125`) and s(26) ≥ 1111/200 (`mixed_n26_L5555`) from this issue, with your 8 October follow-up s(27) ≥ 1131/200 (`mixed_n27_L5655`), which replaces the issue's 2261/400. Each is above its case's lower bound on `main` (T-103 to T-106) by 1/400, 3/400, 1/100 and 23/2000.

Until now the record held these four only as evidence entries. The case records do not change yet: n = 19, 20, 26 and 27 keep 193/40, 981/200, 1109/200 and 11287/2000 in both lower lanes until each certificate has a complete replay here.

Separately, your repository's `mixed_n31_L59775` (23e3186, 11 October), s(31) ≥ 2391/400, is registered as **T-232, V0/C0**. It goes above this issue's 597/100 by 3/400 and above the case's 2381/400 by 1/40. Its retained candidate and receipts are in `packing/resources/web/wand125-fine-net-n31-2026-10-11/`.

**What remains.** For each of the four in T-233: a complete `sqverify-fast` census at all 2,073 directions from a candidate retained where the census reads it, with the whole-net control (the 99/100 mutant at every direction), and a review that reads the certificate. From your check2 receipts we estimate about 12.5 to 18 CPU-hours for the four (`think-ndvg`). For T-232 the same census and review are under way. As with T-205 to T-207, a `sqverify-fast` replay here is a re-implementation that shares components with your checker, since `sqverify-proof-net` adapts this repository's crate.

This issue stays open while that work is queued, and a reply follows each change in the record.

(Before posting: confirm the ids are on `main`, update T-232's line to its state at merge (census, controls and review), and link the result pages.)
2026-10-23 c-lower-1023, at the coordinator's request: release packet packing/resources/web/wand125-fine-net-lower-bounds-446-release-2026-10-08/ (commit 5690db065, pushed), pinned at bf85d6b, retains the four assets' candidates, receipts and logs (fine_net_followup retain; each asset held to the 8 October packet's stored size and SHA-256 and to SHA256SUMS lines 19, 435, 22, 436) with premises receipts (EXACT_PREMISES_HOLD at all four); acquire_source --check PACKET_MATCHES_ITS_CONTRACT; check-retained 0 problems. The census reads it (MIXED_PACKETS, SHARED_CRATE_PACKETS), so think-ndvg's census can run from it. The 8 October authored-facts packet is unchanged apart from a cross-reference section. The coordinator starts T-233's stage 4 review from this head.
2026-10-23 c-lower-1023: the stage 4 review (c-review-t233-math, think-bwis) accepted all four certificates; mapped in 1b0ae50fd: docs/project/reviews/review-2026-10-23-wand125-446-fine-net.md, programs and receipts in the release packet's review/review-2026-10-23/. T-233 now V0/C1 (reads on E-wand125-fine-net-446-n19-n20-n26-report, split from the seven-count entry by F-2, and on E-wand125-fine-net-n27-5655-followup-report); S3 confirmed; credit aligned to "Hosono after Tokoharu and Levy" (F-1); re-priced 10.5 to 19.2 CPU-h (F-3). The census of the four is approved by the coordinator under the 40 CPU-h item cap: after think-wop1's n31 capture and controls, one count at a time, nice -n 19, --threads 2; stop if the measured total heads above 22 CPU-h.

## Stage 7 draft for #446, revised after the review (not posted; supersedes the draft above)

@wand125, thank you. Four more of your fine-net lower bounds are now registered on `main`:

- **T-233, V0/C1, reviewed:** s(19) ≥ 1931/400 (`mixed_n19_L48275`), s(20) ≥ 393/80 (`mixed_n20_L49125`) and s(26) ≥ 1111/200 (`mixed_n26_L5555`) from this issue, with your 8 October follow-up s(27) ≥ 1131/200 (`mixed_n27_L5655`), which replaces the issue's 2261/400. Each is above its case's lower bound on `main` (T-103 to T-106) by 1/400, 3/400, 1/100 and 23/2000.

**What was checked here.** The candidates, receipts and logs of the four release assets are now retained in this repository. The maintained readers accept every exact premise. A mathematical review read all four certificates and accepted them, with no blocking or major finding ([review](docs/project/reviews/review-2026-10-23-wand125-446-fine-net.md)):
- it re-derived the argument and recomputed every premise with programs of its own;
- it decided direction 0 of each net completely, by an independent vertex argument;
- it read your run and control logs exactly, and your 124 oblique control witnesses agree with its exact captures as fractions;
- at 32 sampled directions per count it found no capture below 1, and none below your certified bound.

Coverage at the other directions still rests on your runs, so the case records keep 193/40, 981/200, 1109/200 and 11287/2000 until a complete `sqverify-fast` census with whole-net controls runs here; that census is approved and queued. As with T-205 to T-207, such a replay is a re-implementation that shares components with your checker.

Separately, your repository's `mixed_n31_L59775` (23e3186, 11 October), s(31) ≥ 2391/400, is registered as **T-232**. It goes above this issue's 597/100 by 3/400. [State at merge: its census, controls and review.]

**Notes and questions from the review:**
1. Each bundle's README lists `check2/control.jsonl.gz`; the asset holds `check2/control-197_200.jsonl.gz`, as with the 16 October bundles. Could you correct that?
2. The `check2/src/SOUNDNESS.md` beside the archive is this repository's file of 3 October, before lemma N0 (the declared net's premises (a) to (e)) was added. Your `SPEC.md` states the net lemma correctly, but a reader of that file does not find the premises. Could you put the archive's own copy beside it, or quote lemma N0 in `SPEC.md`?
3. `UPSTREAM_COMMIT` names `42534d95…`, which jlevy/squares does not hold, and `fe12e036c` does not resolve either. By file digest, the archive is this repository's `e020eb1e2` with four files changed (`src/certificate.rs`, `tests/adversarial.rs`, `README.md`, `SOUNDNESS.md`). Could the bundle name a public commit, or publish the `certificate.rs` diff?
4. Does the adapted `certificate.rs` refuse a declared net that fails any of lemma N0's (a) to (e), and does its per-bin domain read the declared step?
5. The n = 19 check2 run used 6 threads and the others 12. Were the 12-thread runs on 12 physical cores? Per-node CPU differs by a factor of two, which matters for pricing the replay here.

This issue stays open while that work is queued, and a reply follows each change in the record.

(Before posting: confirm the ids are on `main`, fill T-232's line, and link the result pages and the review on `main`.)
2026-10-23 c-lower-1023, census status (PR #745): captures VERIFIED at all 2,073 directions for n19, n20, n26 and n27; whole-net controls CONTROLS_REFUSED at n19, n20 and n27. At n26 the control failed closed on AXIS_ROUNDING (gap 3.28e-9 > 1e-9), which is think-tcsl. On the coordinator's option (a), T-233's replay evidence is held until think-tcsl lands, and T-233 stays V0/C1. The n26 receipt is kept byte-identical as mixed_n26_L5555.control-failed-v2.json (9c38ae281), outside the receipts the census tests hold to CONTROLS_REFUSED; the control logic is unchanged.2026-10-23 c-fix-745-1023 (review A of PR #745): T-233's records now say what the 23 October censuses found (7e12d05ce): claim, next_rung and unfinished_confirmations on think-tcsl (n26 re-judge or rerun, at most 0.32 CPU-h; the spent 10.5 to 19.2 price dropped, about 7.8 spent), notes on why n19, n20 and n27 wait for n26 (one entry takes the least rung; held together rather than split), the eight census receipts as artifacts; both evidence entries, the four case blockers, both coverage notes, #446's request summary (V0/C1), the bibliography note and the release packet README follow. The stage 7 draft above predates this: its "census is approved and queued" line should say the four captures passed and n26's control waits on think-tcsl. Branch head bdf7fe618.
2026-10-24 c-land-745-1024 (landing lane of coord-intake-1023), PR #745 at d8138ad5f: the stage 7 draft is revised below for the four censuses (the stale "census is approved and queued" line) and for T-232's state at merge (V3/C3, census, controls, review). It supersedes both drafts above.

## Stage 7 draft for #446, revised 24 October at PR #745's head d8138ad5f (not posted; supersedes both drafts above)

@wand125, thank you. Four more of your fine-net lower bounds are now registered on `main`:

- **T-233, V0/C1, reviewed:** s(19) ≥ 1931/400 (`mixed_n19_L48275`), s(20) ≥ 393/80 (`mixed_n20_L49125`) and s(26) ≥ 1111/200 (`mixed_n26_L5555`) from this issue, with your 8 October follow-up s(27) ≥ 1131/200 (`mixed_n27_L5655`), which replaces the issue's 2261/400. Each is above its case's lower bound on `main` (T-103 to T-106) by 1/400, 3/400, 1/100 and 23/2000.

**What was checked here.** The candidates, receipts and logs of the four release assets are now retained in this repository. The maintained readers accept every exact premise. A mathematical review read all four certificates and accepted them, with no blocking or major finding ([review](docs/project/reviews/review-2026-10-23-wand125-446-fine-net.md)):
- it re-derived the argument and recomputed every premise with programs of its own;
- it decided direction 0 of each net completely, by an independent vertex argument;
- it read your run and control logs exactly, and your 124 oblique control witnesses agree with its exact captures as fractions;
- at 32 sampled directions per count it found no capture below 1, and none below your certified bound.

Complete `sqverify-fast` censuses then ran here from the retained candidates. All four certificates verified at every one of the 2,073 directions of their net, each with your node total. The whole-net controls, your certificate scaled to 99/100 at every direction, were refused at 19, 20 and 27. At 26 the control failed closed. The mutant was refused at every direction, but at the axis direction its exact capture, below 1, sits 3.28e-9 above the sweep's certified bound, beyond the control's fixed 1e-9 rounding allowance. That is a tolerance in this project's control logic, not a finding about your certificate, and a reviewed fix is queued. Until it lands the four replays are held together, T-233 stays V0/C1, and the case records keep 193/40, 981/200, 1109/200 and 11287/2000.

Separately, your repository's `mixed_n31_L59775` (23e3186, 11 October), s(31) ≥ 2391/400, is registered as **T-232, V3/C3, confirmed**, and is now the verified lower bound at n = 31 in both lower lanes. A complete census here verified all 2,073 directions with 787,004,724 nodes, your total. Its whole-net control was refused at every direction. A mathematical review accepted it and decided 122 sampled directions again with an exact checker of its own ([review](docs/project/reviews/review-2026-10-23-wand125-n31-fine-net.md)). It goes above this issue's 597/100 by 3/400 and above the standing 2381/400 by 1/40, so the interval at 31 is now 2391/400 ≤ s(31) ≤ 6.

As with T-205 to T-207, a `sqverify-fast` replay here is a re-implementation that shares components with your checker, since `sqverify-proof-net` adapts this repository's crate.

**Notes and questions from the review of the four:**
1. Each bundle's README lists `check2/control.jsonl.gz`; the asset holds `check2/control-197_200.jsonl.gz`, as with the 16 October bundles. Could you correct that?
2. The `check2/src/SOUNDNESS.md` beside the archive is this repository's file of 3 October, before lemma N0 (the declared net's premises (a) to (e)) was added. Your `SPEC.md` states the net lemma correctly, but a reader of that file does not find the premises. Could you put the archive's own copy beside it, or quote lemma N0 in `SPEC.md`?
3. `UPSTREAM_COMMIT` names `42534d95…`, which jlevy/squares does not hold, and `fe12e036c` does not resolve either. By file digest, the archive is this repository's `e020eb1e2` with four files changed (`src/certificate.rs`, `tests/adversarial.rs`, `README.md`, `SOUNDNESS.md`). Could the bundle name a public commit, or publish the `certificate.rs` diff?
4. Does the adapted `certificate.rs` refuse a declared net that fails any of lemma N0's (a) to (e), and does its per-bin domain read the declared step?
5. The n = 19 check2 run used 6 threads and the others 12. Were the 12-thread runs on 12 physical cores? Per-node CPU differs by a factor of two, which matters for pricing the replay here.

This issue stays open while the control fix is queued, and a reply follows each change in the record.

(Before posting: confirm T-232 and T-233 are on `main` at these rungs, link the result pages and both reviews on `main`, and check whether think-tcsl has landed, which would change the T-233 paragraph. The n31 review's M-1 to M-3 and its five questions go to the author on the owner's word, since no issue asked for n31; decide whether they ride this reply.)

2026-10-24 c-final-745-1024 (final lane of coord-intake-1023), PR #745 review B2 (https://github.com/jlevy/squares/pull/745#issuecomment-6379074892): the 24 October draft's T-233 census sentence said the four certificates "verified", but T-233 is V0/C1 and verified names a lane in this record; it now says the four captures "passed", as T-233's own claim does. T-232's "verified" stays. Nothing else changes. The corrected draft below supersedes the 24 October draft above. Branch head 984f7e132.

## Stage 7 draft for #446, corrected 24 October at PR #745's head 984f7e132 (review B2; not posted; supersedes every draft above)

@wand125, thank you. Four more of your fine-net lower bounds are now registered on `main`:

- **T-233, V0/C1, reviewed:** s(19) ≥ 1931/400 (`mixed_n19_L48275`), s(20) ≥ 393/80 (`mixed_n20_L49125`) and s(26) ≥ 1111/200 (`mixed_n26_L5555`) from this issue, with your 8 October follow-up s(27) ≥ 1131/200 (`mixed_n27_L5655`), which replaces the issue's 2261/400. Each is above its case's lower bound on `main` (T-103 to T-106) by 1/400, 3/400, 1/100 and 23/2000.

**What was checked here.** The candidates, receipts and logs of the four release assets are now retained in this repository. The maintained readers accept every exact premise. A mathematical review read all four certificates and accepted them, with no blocking or major finding ([review](docs/project/reviews/review-2026-10-23-wand125-446-fine-net.md)):
- it re-derived the argument and recomputed every premise with programs of its own;
- it decided direction 0 of each net completely, by an independent vertex argument;
- it read your run and control logs exactly, and your 124 oblique control witnesses agree with its exact captures as fractions;
- at 32 sampled directions per count it found no capture below 1, and none below your certified bound.

Complete `sqverify-fast` censuses then ran here from the retained candidates. All four captures passed at every one of the 2,073 directions of their net, each with your node total. The whole-net controls, your certificate scaled to 99/100 at every direction, were refused at 19, 20 and 27. At 26 the control failed closed. The mutant was refused at every direction, but at the axis direction its exact capture, below 1, sits 3.28e-9 above the sweep's certified bound, beyond the control's fixed 1e-9 rounding allowance. That is a tolerance in this project's control logic, not a finding about your certificate, and a reviewed fix is queued. Until it lands the four replays are held together, T-233 stays V0/C1, and the case records keep 193/40, 981/200, 1109/200 and 11287/2000.

Separately, your repository's `mixed_n31_L59775` (23e3186, 11 October), s(31) ≥ 2391/400, is registered as **T-232, V3/C3, confirmed**, and is now the verified lower bound at n = 31 in both lower lanes. A complete census here verified all 2,073 directions with 787,004,724 nodes, your total. Its whole-net control was refused at every direction. A mathematical review accepted it and decided 122 sampled directions again with an exact checker of its own ([review](docs/project/reviews/review-2026-10-23-wand125-n31-fine-net.md)). It goes above this issue's 597/100 by 3/400 and above the standing 2381/400 by 1/40, so the interval at 31 is now 2391/400 ≤ s(31) ≤ 6.

As with T-205 to T-207, a `sqverify-fast` replay here is a re-implementation that shares components with your checker, since `sqverify-proof-net` adapts this repository's crate.

**Notes and questions from the review of the four:**
1. Each bundle's README lists `check2/control.jsonl.gz`; the asset holds `check2/control-197_200.jsonl.gz`, as with the 16 October bundles. Could you correct that?
2. The `check2/src/SOUNDNESS.md` beside the archive is this repository's file of 3 October, before lemma N0 (the declared net's premises (a) to (e)) was added. Your `SPEC.md` states the net lemma correctly, but a reader of that file does not find the premises. Could you put the archive's own copy beside it, or quote lemma N0 in `SPEC.md`?
3. `UPSTREAM_COMMIT` names `42534d95…`, which jlevy/squares does not hold, and `fe12e036c` does not resolve either. By file digest, the archive is this repository's `e020eb1e2` with four files changed (`src/certificate.rs`, `tests/adversarial.rs`, `README.md`, `SOUNDNESS.md`). Could the bundle name a public commit, or publish the `certificate.rs` diff?
4. Does the adapted `certificate.rs` refuse a declared net that fails any of lemma N0's (a) to (e), and does its per-bin domain read the declared step?
5. The n = 19 check2 run used 6 threads and the others 12. Were the 12-thread runs on 12 physical cores? Per-node CPU differs by a factor of two, which matters for pricing the replay here.

This issue stays open while the control fix is queued, and a reply follows each change in the record.

(Before posting: confirm T-232 and T-233 are on `main` at these rungs, link the result pages and both reviews on `main`, and check whether think-tcsl has landed, which would change the T-233 paragraph. The n31 review's M-1 to M-3 and its five questions go to the author on the owner's word, since no issue asked for n31; decide whether they ride this reply.)
