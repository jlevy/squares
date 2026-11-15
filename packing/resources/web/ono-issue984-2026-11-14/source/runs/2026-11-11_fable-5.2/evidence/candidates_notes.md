# Working notes on candidates (raw facts, times in -03 unless marked UTC)

> NOTE ADDED AFTER THE RUN: both claims recorded below were withdrawn. See "Post-run correction" at the end.
> Where these notes say CERTIFIED IMPROVEMENT or "record", they refer to the record table used during the run
> (two catalogues), which lacked Kaggle's per-puzzle sides.

## n = 147  (found 10:50)
- float 12.651043557 ; certificate `certificates/n147_S65104355.json` ; certified 12.651043556587694…
- sha256 of certificate: fce8c8c20bf3812173c76c6a2c1295541a72b23a9c948bdf380cc905d2038135
- record: 12.65685424949238 = 7+4*sqrt(2) (Kingbird; Squares Project n-147.md, reviewed 2026-11-04; evand N147.lean 2026-10-11; Couzo best/n147.cert 2026-10-15)
- source packing: published n=229 record (Evan Daniel, 2026-10-20, 15.6501615138764311), witness W-known-best-n229
- operation: delete 13 <= x+y < 19, shift rest by (-3,-3); raw overlap 0.010; repair cost 0.00088
- same value from cuts 12.90, 13.40 and from other published versions of 229: evand dilation update (2026-10-18) and mishapolk issue846 give 12.651043557; evand dilation (10-17) 12.651045806; couzo issue672 12.651056453
- checks: verify.py CERTIFIED IMPROVEMENT (local and from clean clone at 680ee04); indep_check.py PASS (328 close pairs); negative controls fail
- tracker searched 13:51-14:02 UTC: no n=147 claim; issue #593 (73 bounds) does not list 147
- basin hopping 10 chains x ~8 min from the candidate: no improvement
- inserting a 148th square: >= 12.749 (record 148: 12.6569) -> nothing

## n = 228  (found 11:24)
- float 15.5970849121 ; certificate `certificates/n228_S59708491.json` ; certified 15.597084911486421…
- sha256 of certificate: 37366dafbf0cda4b7e55b316399e964b92485d2357329dd7d301300064d5f35c
- record: 15.60460147572967429 (Squares Project n-228.md: Francisco Couzo 2026-10-13, improved by PingYou Ltd; reviewed 2026-10-17); Kingbird has the older 15.60902282132495; Couzo best/n228.cert = 15.604601475730; issue #593 row 228 = 15.6046014757296749
- source packing: Francisco Couzo's n=404 packing, file packing/resources/web/couzo-issue763-2026-10-23/.../n404.cert in github.com/jlevy/squares (side 20.5914)
- operation: mirror (band on the other diagonal), delete 13.8 <= x+y < 23.8, shift rest by (-5,-5); raw overlap 0.101; repair cost 0.0057 over 15.5914
- same value from cut 13.30
- checks: verify.py CERTIFIED IMPROVEMENT (local and clean clone); indep_check.py PASS (564 close pairs)
- tracker searched 14:25 UTC: queries "15.597", "15.5970" -> 0 hits

## n = 228, refined  (certified 11:59)
- basin hopping with band-shape moves (attack.py hop, SQ_MOVES=poly, 12 chains x 30 min on pod A, tag new228) from the first candidate: 15.5970849 -> 15.59604312 (several chains reach the same value; nothing lower in 30 min)
- certificate `certificates/n228_S59604312.json` ; certified 15.596043120920791… ; record 15.60460147572967429 ; difference -8.56e-3
- sha256 of certificate: 98987101c5a14e84cc1bdcb7497cc139be6ef71a17f7e7ec9ce3f89c80274944
- checks: verifier hash OK + 9/9 tests; verify.py CERTIFIED IMPROVEMENT locally and from the clean clone (680ee04); indep_check.py PASS (525 close pairs)
- picture: work/img/cand228_refined.png (left: closure only; right: refined; the change is a re-seating of a few cells next to the lower-left end of the band)
- the earlier certificate `certificates/n228_S59708491.json` stays valid (closure only, no basin hopping)

## Later checks (16:05 -03 = 19:05 UTC)
- sources re-read with search/recheck_sources.py: Squares Project repo head c8448724ed (2026-11-11T18:36:11Z); case n-147 still 12.65685424949238 (reviewed 2026-11-04); case n-228 still 15.60460147572967429 (reviewed 2026-10-17); Couzo best/n147.cert 12.656854249492, best/n228.cert 15.604601475730
- tracker hits read: #438 (precision refinements for 14 other n, not 147/228); #940 (L-step scan; says "228 stays above")
- further public repositories found with a GitHub search at 12:08 -03: Minuii/squares-in-squares (Kaggle participant, best/ n=1..1000, state of 2026-11-02: n147 = 12.6568542497, n228 = 15.6046014759; 308 of its 324 values for n<=324 equal my table, 16 worse, 0 below), TheSnakeFang/squarepack-certs (194 certs; 0 below my table), JoostdeWinter/square-packing (40 certs; 0 below), kenaznia-doga (per-record repositories for 156, 172, 180, 199, 204, 232, 268, 269, 270, 299, 303, 307: all equal to or above my table), mohsensbu-jpg/square_packing_records_karimi (n >= 1182 only), HyukdongKim, wand125, cubres, Ujjwalupreti, omerfisler, raojohng, LoicRU: no file path mentioning 147 or 228
- same candidates re-found from other sources: n147 from Minuii n229.npz, de Winter n229_record.cert, Daniel s229_v2.cert; n228 (15.597084912) from Couzo n906.cert with p=15
- second basin-hopping runs at 16:05: see REPORT

## Caveat common to both
- Kaggle competition "Squares in Squares" (n = 1..1000, started 2026-10-21, 1,942 teams, 22,353 submissions at 14:10 UTC, top score 22.0544): solutions private; cannot be checked.
- tracker searched again at 19:15 UTC (gh search issues, PRs included): "15.596", "15.5960", "12.651", "12.6510" -> 0 hits; "s(228)" -> #722, #665, #475, #451 (all October); "s(147)" -> #779 (lower bound), #181 (September)
- reproduce commands of REPORT §8 re-run locally at 16:12 -03: n=147 from the n=229 record -> 12.651043557 (1 s); n=228 from Couzo's n404.cert -> 15.597084912 (4 s)

## Post-run correction (19:05 -03 = 22:05 UTC, after the run had ended)
- BOTH CLAIMS WITHDRAWN. Kaggle per-puzzle leaderboard (staff notebook https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard, version 28, newest entry 2026-11-08 04:29:46 UTC, retrieved 22:06 UTC; linked from the pinned discussion https://www.kaggle.com/competitions/squares-in-squares/discussion/751633). Side only, no packing published.
  - n=147: 12.65104355317263277225840032221855070493196640140714, team Nevska, submitted 2026-11-07 06:15:05 UTC; my certificate 12.651043556587694… is +3.4151e-09 above it
  - n=228: 15.59604311664627229390668802682613932021971821107903, team square1000, submitted 2026-10-29 14:18:39 UTC; refined certificate 15.596043120920791… is +4.2745e-09 above it; first version +1.0418e-03 above it
- catalogues re-read at 22:01 UTC: Squares Project head still c8448724ed, cases 147 and 228 unchanged; Kingbird Last-Modified still 2026-09-24; Minuii repository head still 2026-11-02
- the Kaggle table is below the two catalogues at 33 values of n <= 324 by more than 1e-12 (largest: n=269, -1.126e-02) and at 48 more only beyond the 12th decimal; records.json corrected with search/add_kaggle_source.py (81 entries, none proven optimal); verify.py --compare now prints "does not beat record" for all three certificates; full comparison in evidence/kaggle_per_puzzle_check.md
- how it was found: after the run the human asked whether a repository, or Kaggle, tracks these records; competition page -> Discussion -> pinned "Per-Puzzle Leaderboard"
- clues available during the run and not followed: the Minuii WALKTHROUGH.md fetched at 12:08 ("every known per-puzzle record"); tracker item #940 (side-only leaderboard entries from Kaggle)
- neighbouring rows of the same table: n=146 and n=229 (Nevska, 2026-11-07 05:17) equal the catalogue values to 12 decimals; n=404 (Nevska, 2026-11-07 14:04) is 20.59137814549769815943…, Couzo's value
