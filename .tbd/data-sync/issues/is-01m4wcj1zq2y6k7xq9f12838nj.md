---
type: is
id: is-01m4wcj1zq2y6k7xq9f12838nj
title: "Import Benjamin Greff (bengreff): s(76) = 9 by a mixed cover (#594)"
kind: task
status: in_progress
priority: 1
version: 2
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-14T05:01:01.303Z
updated_at: 2026-10-14T05:01:05.889Z
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
