# REPORT — run 2026-11-11_fable-5.2

> **Correction made after the run (2026-11-11, about 19:05 -03). The two "candidate improvements"
> reported at the end of the run are not improvements. Both claims are withdrawn.**
>
> Kaggle staff publish a per-puzzle leaderboard for the "Squares in Squares" competition: the smallest
> side the competition's grader has accepted for every n, side only, with the team and the date
> (`https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard`). It already held
> both values, slightly lower than mine:
>
> | n | this run (certified) | Kaggle per-puzzle leaderboard | team, submitted | this run − Kaggle |
> |---|---|---|---|---|
> | 147 | 12.651043556587694… | 12.65104355317263277… | Nevska, 2026-11-07 | +3.4e-9 |
> | 228 | 15.596043120920791… | 15.59604311664627229… | square1000, 2026-10-29 | +4.3e-9 |
>
> I did not find this table during the run. I found it afterwards, when the human asked where these
> records are tracked. I should have found it before claiming anything: the competition was known to
> me from phase 1, and two documents I had fetched during the run point to per-puzzle records (§6).
> `records.json` did not contain this source, so `CERTIFIED IMPROVEMENT` was printed against a table
> that was too high at these two n, and at 33 values of n ≤ 324 in all. The table now includes the
> source (`search/add_kaggle_source.py`), and the frozen verifier prints `does not beat record` for
> all three certificates.
>
> What remains true: the packings are valid and exactly certified, and they are below the two
> catalogues and below every packing with published coordinates that I found. The outcome of the run
> is a **null result**. §1, §6 and §7 are rewritten accordingly. The other sections describe the run as
> it happened; where they say "candidate" or "below record" they mean below the two catalogues, not
> below the best known side. Evidence: `evidence/kaggle_per_puzzle_check.md`.

## 1. Outcome

**No improvement.** The run produced two certified packings that reproduce, from just above, sides
that were already on Kaggle's public per-puzzle leaderboard:

| n | certified side (this run) | the two catalogues | Kaggle per-puzzle leaderboard (side only) | this run − Kaggle | certificate |
|---|---|---|---|---|---|
| 147 | 12.651043556587694… | 12.65685424949238 (= 7 + 4√2) | 12.65104355317263277… (Nevska, 2026-11-07) | +3.4e-9 | `certificates/n147_S65104355.json` |
| 228 | 15.596043120920791… | 15.60460147572967429 | 15.59604311664627229… (square1000, 2026-10-29) | +4.3e-9 | `certificates/n228_S59604312.json` |

(`certificates/n228_S59708491.json`, side 15.597084911486421…, is the first version of the n = 228
packing, before refinement. It is valid too.)

At the end of the run I reported these two as candidate improvements. That was wrong: they are
rediscoveries. They are 5.81e-3 and 8.56e-3 below the two catalogues (the Kingbird page and the
Squares Project), and I found no packing with these sides published with coordinates, so the
certificates, if published, may be the first public witnesses of the two bounds. They are not new
bounds.

Neither came from search power. Both come from one observation: the catalogues are not closed under
removing a diagonal "period" from a band-type packing. Removing one (3, 3) period from the published
n = 229 record leaves 147 squares; removing five periods from a published n = 404 packing leaves 228
squares; after a small repair each is below the catalogue value. Both packings are built on other
people's work (Evan Daniel's n = 229, Francisco Couzo's n = 404).

Everything else in this run is a negative result as well. The calibration shows that my from-scratch
search stops being competitive at about n = 28, and every "search harder" method converged onto
values the tables already hold.

Calibration certificates (not improvements): n = 11, 17, 18, 19, each within 3e-12 of its record.

## 2. Phase 0 — orientation

`sha256sum -c VERIFIER.sha256` is OK and 9/9 unit tests pass; this was repeated before each claim run
and from a fresh clone. The verifier takes rational centres and rotations t = tan(θ/2), checks
containment and pairwise disjoint interiors exactly, and counts a record as beaten only if the side is
below the published value minus half a unit in its last printed digit (`upper_truncated_down` is never
set in my `records.json`).

## 3. Phase 1 — state of the art

- Erich Friedman's Packing Center page now redirects to David Ellsworth's maintained page
  (`kingbird.myphotos.cc/packing/squares_in_squares.html`, HTTP Last-Modified 2026-09-24).
- A second, newer catalogue exists: **The Squares Project** (`jlevy.github.io/squares/frontier.html`,
  case files in `github.com/jlevy/squares`). It is lower than the Kingbird page at **79 values of n**.
- `records.json` (n = 1..324), as built in this phase, held the *smaller* of the two catalogue values
  for every n (after the correction it also carries the Kaggle per-puzzle side, see the top), copied
  digit for digit (`search/build_records.py`); both values are kept in separate fields. 91 values of n
  are flagged `proven_optimal`, including proofs that are only reported (n = 12, 17 and eight more).
- The table is being rewritten daily: 80 of the 146 open non-trivial records date from
  September–November 2026, eleven of them from 9–11 November. The driver is a Google-sponsored
  **Kaggle competition, "Squares in Squares"** (n = 1..1000, started 2026-10-21; 1,942 teams and 22,353
  submissions at 14:10 UTC on 11 November). Its solutions are private; the Squares Project registers
  what participants choose to publish. **What I missed here:** the best *side* per n is public, in a
  per-puzzle leaderboard notebook kept by Kaggle staff, and it is lower than both catalogues at 33
  values of n ≤ 324 (`evidence/kaggle_per_puzzle_check.md`).
- `targets.md`, written before any attack, ranked **n = 147 first** on structural grounds (its record
  was the n = 148 packing with one square deleted, and the neighbouring table entries put the
  expected value near 12.62–12.65). n = 228 was not on that list.

## 4. Phase 2 — calibration

Method (`search/gsearch.py`, reads no published coordinates): random start → L-BFGS on
S + μ·(sum of squared overlap depths), μ increasing → exact-constraint sequential-LP polish → basin
hopping → exact certificate through the frozen `certify.py`.

| n | record | from scratch? | workers that hit it | first hit | certified side | certified − record |
|---|---|---|---|---|---|---|
| 11 | 3.87708359002281 | yes | 4 of 8 (40 s budget) | 10 s | 3.877083590024002 | 1.2e-12 |
| 17 | 4.67553009360455 | yes | 3 of 6 (420 s) | 52 s | 4.675530093606028 | 1.5e-12 |
| 18 | 4.82287565553229 | yes | 5 of 5 (420 s) | 9 s | 4.822875655534004 | 1.7e-12 |
| 19 | 4.88561808316412 | yes | 2 of 5 (420 s) | 95 s | 4.885618083166841 | 2.7e-12 |
| 28 | 5.82444461667405 | **no**, best 5.870829 | 0 of 6 (600 s) | – | – | 0.046 short |
| 29 | 5.93383346267692 | **no**, only the trivial 6.0 | 0 of 5 (600 s) | – | – | 0.066 short |
| 37 | 6.59861960924436 | **no**, best 6.621320 (the 1980 value) | 0 of 5 (600 s) | – | – | 0.023 short |

The requirement (three irregular records within 1e-6, from scratch, certified) is met with four, all
at n ≤ 19. Above that my from-scratch search does **not** reach the records found by the
simulated-annealing programs of 2025–26. My own annealer (`search/sa.py`, about 7·10⁶ moves/s per
core) found no feasible state at the n = 29 record side in 220 runs. I did not fix this. Phase 3
therefore started from published packings, never from random states, and that limits what the
negative results below can say.

## 5. Phase 3 — what was tried

Published packings were loaded from the Squares Project's witness files (`search/witness_io.py`; all
324 validate) and from third-party certificate files in public repositories.

| # | method (code) | scope | result |
|---|---|---|---|
| 1 | Exact polish of every open record (`opt.polish`) | 233 n | each is a converged local optimum; no numerical slack |
| 2 | Table closure: delete a square, add an L, remove clean rows and columns (`closure.py`, `bigclosure.py`) | all n; also 655 published packings with n > 324 and 7,270 of my own intermediate packings | 0 hits |
| 3 | Delete each single square of the (n+1)-record and re-polish (`attack.py delone`) | 52 n | 0 below record; near misses 151 (+0.0015), 234 (+0.0024), 86 (+0.0027) |
| 4 | Approximate un-L / L-insertion transfers between neighbouring bands (`attack.py unl`, `sweep`) | about 100 target/source pairs, 10,000 seeds | 0 below record; losses 0.05–0.35 against margins 0.01–0.07 |
| 5 | Basin hopping from records and from the best seeds of 3, 4 and 8 (`attack.py hop`) | 20 n (147, 290, 151, 234, 86, 266, 130, 88, 199, 177, 152, 300, 230, 19, 201, 172, 174, 67, 50, 228) | on records: every chain converged onto a value already in the tables. On the fresh n = 228 candidate: improved it by 1.04e-3 (see §6) |
| 6 | Tilted-block and rotated-lattice seed generators (`blockseed.py`, `latseed.py`) | 150, 151 | could not even reproduce known records; abandoned |
| 7 | Periodic splice inside the band family 106 → 177 → 266 (`splice.py`) | 177, 266 | reproduces the records to 5e-9: the family's value "ladder" is intrinsic |
| 8 | **Diagonal-period closure** (`diagper.py`, `diagcuts.py`): remove or insert (p, p) periods of a diagonal band, repair, polish | all 324 records, and about 7,800 further public packings from six repositories (table below) | **two leads below the catalogues: n = 147 and n = 228**, both already on Kaggle's per-puzzle leaderboard (correction at the top). Every other optimised lead ends on or above the catalogues |
| 9 | Cross-cut closure (`crossper.py`): remove a vertical and a horizontal strip of width p anywhere, close up, repair, polish | 144 non-trivial records; 1,889 public packings | 0 hits |
| 10 | Basin hopping from the closure's near misses (`refine_near.py`) | 37 n within 0.004 of their record, plus n = 83 | 0 below record: 17 of the 37, and n = 83, fall onto the record itself (to 1e-8); the other 20 stay where they were or improve without reaching it |

Sources and volume for methods 8 and 9 (one line per pass; "leads" are cut positions that passed a
cheap pre-screen and were then repaired and polished):

| operation | sources | leads repaired and polished | below the catalogues |
|---|---|---|---|
| diagonal | 324 records, first pass (remove and insert, p ≤ 6) | 396 | n = 147 |
| diagonal | 324 records, finer cut positions | 2,126 | n = 147 |
| diagonal | 324 records, p ≤ 12 | 8,730 | n = 147 |
| diagonal | 324 records, insertions only, improved fill | 93 | none |
| diagonal | 185 alternative published versions with n ≤ 324 (Squares Project web resources) | 7,164 | n = 147 |
| diagonal | 655 published packings with n > 324 (Squares Project web resources) | 29,935 | n = 228 |
| diagonal | the same 655 packings, targets with integer records only; stopped early | 3,231 of 14,274 | none |
| diagonal | 275 further published packings (Squares Project web resources) | 11,484 | none |
| diagonal | 550 published packings with large n, p = 9..21; stopped with 4 leads hanging | 37,701 of 37,705 | n = 228 |
| diagonal | 4,416 certificates from F. Couzo's repository | 16,501 | none |
| diagonal | 461 certificates from E. Daniel's repository | 3,453 | n = 147 |
| diagonal | 1,234 packings from three more repositories (Minuii 1,000; TheSnakeFang 194; de Winter 40); stopped with 3 leads hanging | 23,889 of 23,892 | n = 147 |
| diagonal | the candidate packings themselves (n = 147, both n = 228) | 83 | none |
| cross-cut | 144 non-trivial records, p ≤ 8 | 2,335 | none |
| cross-cut | 1,234 packings from three more repositories | 18,303 | none |
| cross-cut | 655 published packings with n > 324; stopped with 1 lead hanging | 14,616 of 14,617 | none |
| cross-cut | 1,286 published packings (the 275, the 550 and E. Daniel's 461); the 12,000 most promising of 86,301 screened leads | 11,999 | none |
| | **total** | **192,039** | n = 147 and n = 228 only |

What worked: the exact polish (fast, makes certification routine) and treating the record table as
something that should be closed under structural operations. What did not: every form of searching
harder. In each case the machinery converged within minutes onto values the tables already hold.

### Per-n results for the ranked targets

Best certified side per n: the certificates in `certificates/` (§1, §4). Best float side per n for
the phase-1 targets and for the other n that received individual attention. The record column is the
corrected table (the smallest of the two catalogues and the Kaggle per-puzzle side), so it differs
visibly from what the run saw at n = 147, 228 and 199:

| n | record | methods tried | best float side | best − record | certified |
|---|---|---|---|---|---|
| 147 | 12.651043553 | crossper×4, delone, diagcuts×2, diagper×14, hop×4, lins, sourcecheck, unl×3 | 12.651043557 | +3.42e-09 | 12.651043556588 |
| 228 | 15.596043117 | crossper×3, diagcuts×2, diagper×12, hop×4, lins, sourcecheck, unl | 15.596043121 | +4.27e-09 | 15.596043120921 |
| 290 | 17.535533906 | crossper, delone, diagper×6, hop | 17.535533911 | +5.07e-09 |  |
| 234 | 15.822875656 | crossper×4, delone, diagper×11, hop, lins, refine, unl | 15.822875661 | +4.97e-09 |  |
| 151 | 12.822875656 | crossper×4, delone, diagper×10, hop×5, latscan, refine, unl×3 | 12.822875660 | +4.08e-09 |  |
| 201 | 14.707106781 | crossper×4, delone, diagper×10, hop, lins, refine, unl | 14.707106786 | +4.62e-09 |  |
| 125 | 11.707106781 | crossper×4, diagcuts×2, diagper×10, lins, unl×2 | 11.707106785 | +3.72e-09 |  |
| 203 | 14.778174593 | crossper×4, delone, diagper×10, lins, unl | 14.778174598 | +4.65e-09 |  |
| 226 | 15.535533906 | crossper, delone, diagper×5 | 15.535533911 | +4.87e-09 |  |
| 257 | 16.535533906 | crossper, delone, diagper×6 | 16.535533911 | +5.07e-09 |  |
| 66 | 8.656854249 | crossper×4, diagper×11, lins, unl | 8.656854252 | +2.51e-09 |  |
| 83 | 9.634757649 | crossper×4, diagper×10, hop, lins, unl | 9.634757649 | +0.00e+00 |  |
| 89 | 9.949747468 | crossper×4, diagper×9, unl | 9.960951249 | +1.12e-02 |  |
| 53 | 7.822875656 | crossper×4, delone, diagper×11, lins, refine, unl | 7.822875658 | +2.57e-09 |  |
| 39 | 6.810722083 | crossper×3, delone, diagper×9, lins, unl | 6.818282016 | +7.56e-03 |  |
| 86 | 9.820535407 | crossper×4, delone, diagper×10, hop, lins, refine, unl | 9.822875659 | +2.34e-03 |  |
| 88 | 9.882451030 | crossper×4, diagper×11, hop×3, refine, unl | 9.882451034 | +3.16e-09 |  |
| 102 | 10.605828696 | crossper×4, diagper×10, lins, refine, unl | 10.605828700 | +3.39e-09 |  |
| 130 | 11.902430646 | crossper×4, diagper×10, hop×2, unl | 11.911187700 | +8.76e-03 |  |
| 266 | 16.823028751 | crossper×4, delone, diagper×10, hop×2, refine, splice | 16.823028756 | +5.27e-09 |  |
| 177 | 13.822979734 | crossper×4, delone, diagper×11, hop, refine, splice, unl | 13.822979739 | +4.37e-09 |  |
| 199 | 14.613209876 | crossper×3, diagcuts×2, diagper×10, hop×2, lins, refine | 14.614689858 | +1.48e-03 |  |
| 172 | 13.614689853 | crossper×4, diagcuts×2, diagper×10, hop, lins | 13.614689858 | +4.30e-09 |  |
| 230 | 15.682926829 | crossper×4, delone, diagper×8, hop, lins, refine | 15.684289554 | +1.36e-03 |  |
| 300 | 17.824123388 | crossper×3, delone, diagper×9, hop, refine | 17.824123394 | +5.57e-09 |  |

About 200 values of n were touched by the systematic passes; `python3 search/summarize_attempts.py
--pern` tabulates all of them from `attempts.jsonl`. No result is below a record: n = 147 and n = 228
are below the catalogue values only. (Three basin-hopping log lines for n = 88, 177 and 290 look lower by 6e-9 to 3e-8; those
values were read from a 7-decimal progress log and are rounding, as annotated in the log.)

## 6. The two rediscoveries and the rule-7 checklist

The construction notes below are as written during the run. "Candidate" in them means a packing
below the two catalogues; neither is below Kaggle's per-puzzle side.

### n = 147

Take the published n = 229 record (Evan Daniel, 2026-10-20, side 15.6501615138764…; a three-wide
diagonal band of squares tilted about 27° between two corner-anchored grids). Delete every square
whose centre has 13 ≤ x + y < 19 and move the squares beyond by (−3, −3). 147 squares remain,
overlapping by at most 0.010. A stiff penalty step and the exact polish repair that at a cost of
0.00088, giving side 12.651043557. Other cut positions and seven other published copies or versions of
the n = 229 packing (three by Daniel, and those of Couzo, de Winter, mishapolk and a Kaggle
participant) give between 12.651043557 and 12.651056453. The old record,
7 + 4√2, was the 45° "diamond" shared with n = 148; the new packing is a different arrangement
(`evidence/cand147.png`). Basin hopping from it found nothing lower (10 chains for 8 minutes, and
later 8 chains for 19 minutes at a higher temperature).

### n = 228

Take Francisco Couzo's published packing for n = 404 = 20² + 4 (file `n404.cert` under
`packing/resources/web/couzo-issue763-2026-10-23/` in the Squares Project repository, side 20.5914;
in the band family that already holds the records for n = 123, 259 and 292, all with side
k + 0.591378). Mirror it, delete every square with
13.8 ≤ x + y < 23.8, move the rest by (−5, −5). 228 = 15² + 3 squares remain with overlaps up to
0.101; the repair costs 0.0057 and gives side 15.597084912. Couzo's n = 906 packing with fifteen
periods removed gives the same value. Basin hopping with band-shape moves then re-seats a few cells
at the lower-left end of the band and reaches 15.596043121 (`evidence/cand228_refined.png`). Two
further runs from there (12 chains for 25 minutes; 12 chains for 19 minutes at a higher temperature)
found nothing lower.

Consistency: removing five more periods from either version lands exactly on the existing n = 102
record (10.605828696), and inserting a square into either candidate costs at least 0.1, so there is
no knock-on improvement at 102, 148 or 229.

### Checklist

| check | n = 147 | n = 228 |
|---|---|---|
| Frozen verifier (hash OK, 9/9 tests) against the record table used during the run (two catalogues) | `CERTIFIED IMPROVEMENT` | `CERTIFIED IMPROVEMENT` (both versions) |
| **Frozen verifier against the corrected record table (with the Kaggle per-puzzle sides)** | **`does not beat record`** | **`does not beat record`** (both versions) |
| Same result from a fresh clone of harness commit 680ee04 (during the run, old table) | yes | yes (both versions) |
| Independent exact check (`search/indep_check.py`, rational polygon clipping, shares no code with the verifier): all pairwise intersection areas exactly 0, all vertices inside | pass, 328 close pairs | pass, 525 close pairs (first version: 564) |
| Negative controls rejected by both checkers | yes | (same code) |
| Outside the rounding of the catalogue value | 5.8e-3 against 14 printed decimals | 8.6e-3 against 17 printed decimals |
| Not proven optimal; above the best lower bound | open; lower bound 12.24 | open; lower bound 15.10 |
| Second source for the catalogue value (last re-read 19:05 UTC, Squares Project repository head c8448724ed of 18:36 UTC) | Kingbird 12.65685424949238; Squares Project case, last reviewed 2026-11-04; E. Daniel's repository 12.6568542495; F. Couzo's `best/n147.cert` 12.656854249492 | Squares Project case 15.60460147572967429 (reviewed 2026-10-17); F. Couzo's `best/n228.cert` 15.604601475730; registration request #593 lists the same value; Kingbird has the older 15.60902 |
| Public Kaggle packings | `Minuii/squares-in-squares` on GitHub (a participant's best packings for n = 1..1000, merging about 50 public notebooks as of 2026-11-02) has 12.6568542497. None of its 324 values for n ≤ 324 is below my table | same repository: 15.6046014759 |
| Tracker and repository search for a newer claim | none (tracker queries "s(147)", "n=147", "12.651"; file listings of twelve further public repositories found by a GitHub search, and the values inside the three that publish packings) | none ("s(228)", "n=228", "15.597", "15.596"; same repositories) |
| Catalogues re-read after the run (22:01 UTC) | unchanged | unchanged |
| **Kaggle per-puzzle leaderboard (best side per n; public, side only). Checked only after the run: FAILS** | 12.65104355317263277…, team Nevska, submitted 2026-11-07 06:15:05 UTC. My certificate is 3.4e-9 above it | 15.59604311664627229…, team square1000, submitted 2026-10-29 14:18:39 UTC. My refined certificate is 4.3e-9 above it |
| Written during the run, and wrong | "Cannot be checked: Kaggle submissions are private." The packings are private; the sides are not | same |
| Still not checked | Kaggle discussions, Discord servers, and public Kaggle notebooks newer than 2026-11-02, which could already contain these packings with coordinates. My copy of the per-puzzle table is about three days old (newest entry 2026-11-08 04:29 UTC), so today's sides can only be lower | same |

I claim nothing: both claims are withdrawn. The operation is the diagonal analogue of the classical "remove an
L", and the same family relation already links existing records (106 ↔ 177 ↔ 266; 123 ↔ 259 ↔ 292 ↔ 404). The
Squares Project's own automated closure check (its L-step scan, tracker item #940) covers the L step
and monotonicity, not this diagonal step, which may be why the two catalogue entries were still open. The Kaggle sides agree with mine to eight
decimals, so those teams evidently hold the same arrangements; how they found them is not public.

### What the rule-7 check missed

My search for a newer claim covered the two catalogues, the Squares Project tracker and every public
repository of packings I could find. It did not cover a list of sides without packings, and I wrote
"cannot be checked" about Kaggle without looking for one. Two documents I had fetched during the run
point to it: a participant's walkthrough speaks of "every known per-puzzle record", and tracker item
#940 speaks of side-only leaderboard entries from Kaggle. The per-puzzle leaderboard is linked from a
pinned discussion on the competition page. For this problem it has to be a source of `records.json`
from phase 1 onward.

Nothing was posted or sent to anyone.

## 7. Limits

- The record table of phase 1 was incomplete. It lacked Kaggle's per-puzzle leaderboard, which is lower
  than both catalogues at 33 values of n ≤ 324, by up to 1.1e-2. Every "below record" judgement made
  during the run was against the two catalogues, and that is how two rediscoveries were reported as
  candidates. The per-n table in §5 was regenerated against the corrected table.
- From-scratch search is calibrated only to n ≤ 19. Nothing here shows that records for n ≥ 28 are
  hard; it shows my search could not reach them.
- The two packings rest on a table-consistency argument, so the claim was only as good as my reading of
  the tables on 2026-11-11, and that reading left out a public source. The tables change daily.
- The closure passes can only use packings that somebody published. They say nothing about band
  families whose larger members exist only in private Kaggle submissions.
- The run was not continuous and not like for like with other runs of this harness: compute moved from
  the local machine to two rented CPU pods at the human's request, and the agent was paused twice while
  the human was logged out of the session (12:18–16:03 and 16:16–16:49 -03; `RUN.md`). About 3.6 of the
  8 hours were agent time. The pods kept working through the first pause only until about 13:23.
- My repair code has a rare hang: 9 of about 192,000 leads and one basin-hopping chain never returned.
  They were killed and are not counted; three passes are marked "stopped" for that reason.

## 8. Reproduce

```
sha256sum -c VERIFIER.sha256 && python3 -m unittest discover -s tests
python3 verify.py runs/2026-11-11_fable-5.2/certificates/n147_S65104355.json --compare runs/2026-11-11_fable-5.2/records.json
python3 verify.py runs/2026-11-11_fable-5.2/certificates/n228_S59604312.json --compare runs/2026-11-11_fable-5.2/records.json
python3 runs/2026-11-11_fable-5.2/search/indep_check.py runs/2026-11-11_fable-5.2/certificates/n147_S65104355.json
python3 runs/2026-11-11_fable-5.2/search/indep_check.py runs/2026-11-11_fable-5.2/certificates/n228_S59604312.json
```

With the corrected `records.json` the two `verify.py` lines print `VALID` and `does not beat record`.

To rebuild a packing from its published source (needs numpy, scipy, numba), from the run directory.
The n = 404 source file is in the ignored scratch directory; if it is gone, download it again from
`https://raw.githubusercontent.com/jlevy/squares/main/packing/resources/web/couzo-issue763-2026-10-23/source/certificates/best/n404.cert`
(sha256 of the copy used: `8c8c8b45f40cfb1d1261baa479be41f9de89d83ceabc03f9ce72a1d42bb67f2e`):

```
python3 search/diagper.py run --nmin 229 --nmax 229 --pmax 3 --procs 1          # n = 147 from the n = 229 record
python3 search/diagper.py run --labels cert:work/web/sources/couzo-issue763-2026-10-23__n404.cert --pmin 5 --pmax 5 --margin 0.002 --net 0.4 --maxviol 0.4 --cstep 0.05 --procs 1
python3 search/make_cert.py work/cand/<file written by the step above>.json --den "10**15"
```

Both commands were re-run at the end of the run and reproduce 12.651043557 and 15.597084912 in a few
seconds. The refinement of n = 228 to 15.596043121 is a seeded stochastic search and is not needed to
check the packing (the certificate is self-contained):

```
SQ_MOVES=poly python3 search/attack.py hop 228 work/cand/<n228 file>.json --time 1800 --procs 12 --seed 81 --temp 0.0007 --tag new228 --share hop_new228
```

## 9. Where the data is

- `attempts.jsonl`: 2,223 lines, every method and every negative result. Lines from the pods are
  tagged `[RunPod pod A|B]`.
- `evidence/`: the two pictures, `candidates_notes.md` (the raw facts for the two packings: values, hashes,
  sources, check times) and `kaggle_per_puzzle_check.md` (the post-run comparison with Kaggle's per-puzzle
  sides). Copies of files in `work/`, kept outside it because the repository ignores `work/`.
- `work/remote/A`, `work/remote/B` (scratch, ignored by git): a full mirror of both pods' working directories (logs, leads,
  seeds, and the third-party packings used as sources; about 2.4 GB, of which about 1.7 GB is
  third-party certificates that can be downloaded again from the URL lists in `work/remote/`). The
  pods were deleted at 16:52 -03 only after a final mirror with zero differences (`RUN.md`).
- `search/README.md`: what each script does.
