# Follow-up after the run (not part of the 8-hour benchmark run)

The run recorded in `REPORT.md` and `RUN.md` ended on 2026-11-11 at 16:54 -03 with a null result.
Everything below was done afterwards, at the human's request, with human steering, and is **not
comparable** with other runs of the harness. It stays inside this run directory because the
repository rules say to write only here. Follow-up code is in `search/fu_*.py`, scratch in
`work/followup/`, and follow-up lines in `attempts.jsonl` start with `[follow-up]`.

## What was asked

- 2026-11-11, evening: the human asked whether something more original could be tried before
  publishing, whether other papers could help, and whether a general solution exists. A literature
  review was written (`work/reports/Ideias originais para quadrados em quadrado.md`, scratch).
- 2026-11-14, 16:20 -03: the human approved the proposed plan with a cap of **US$ 20 on rented pods**.

## Log

### 2026-11-14

- **State check.** Commit be713b7 intact, no pods, no local processes.
- **Kaggle per-puzzle table re-read** (notebook version 31, newest entry 2026-11-14 14:45 UTC, saved
  as `work/web/kaggle_perpuzzle/per_puzzle_v31.tsv`). Against the copy of 11-08: 201 sides lowered,
  sum of per-puzzle bests 22.0509 -> 22.0341. The grid fell at two more counts: n = 157 (K = 13,
  team webmaking, 2026-11-13) and n = 819 (K = 29). n = 383, 274, 466 and 708 are still at the grid.
- **Corner-anchored sub-window closure** (`search/fu_subwindow.py`): 7,775 public packings, 33 s on one
  core. **0 hits** against the Kaggle table for n <= 1000. Negative result.
- **Prior art read** (not known to me during the run):
  - Sungjoon Ryu, L-shaped packing (grid plus two tilted bands), doi:10.5281/zenodo.23278927.
  - Evan Daniel (2026-10-18, Lean): the grid is beaten with 4*ceil(sqrt(2k-7)) squares missing, every k >= 7.
  - Kevin Fang, Theorem A (2026-10-24): k^2 - ceil(sqrt(32k)) - 1 squares fit below side k, every k >= 6
    (`TheSnakeFang/squarepack-certs`, folder `theorem-a/`). Same constant 4*sqrt(2) = 5.66.
  - Mohsen Karimi, filled-end two-band L packings for n = 1182..9946 (K = 35..100), 5,134 exact rows
    (`mohsensbu-jpg/square_packing_records_karimi`). His frontier: 32 squares missing at K = 35, 54 at K = 100
    (about 5.4*sqrt(K)).
  - So a general theorem for "where the grid falls" already exists. What is open is the constant: the
    best numerical packings sit near 4*sqrt(K) (16 missing at K = 17, 24 at K = 31).
- **Where the difference comes from** (waste maps of the public n = 273 packing and of Fang's k = 17
  construction): the exact families run two bands along whole walls (tilt waste about 0.4 per row over
  29 rows, four ends costing about 3.3 squares each); the numerical packing uses two short blocks of
  8 rows around a corner grid (tilt waste 6.4 in all, four tapered ends costing 2.2 to 2.8 each).
- **Generator** (`search/fu_pinwheel.py`): tilted blocks as in Ryu/Fang, upright squares placed by an
  exact maximum-independent-set refill over the four corner-anchored grids (HiGHS MILP, about 10 ms
  per layout at K = 17). It reproduces Fang's count at K = 20 exactly (376 squares). A random scan of
  two-block layouts at K = 17 (`search/fu_scan.py`, 3,000 layouts, 27 s) reaches 20 missing squares:
  one better than the published exact construction (21), four worse than the numerical record (16).
- **Hill climbing with tapered rows** (`search/fu_refine.py`) brings the block model to 19 missing squares at
  K = 17 (270 squares at side 16.999). At K = 35 a scan of 1,500 layouts reaches 32 missing, equal to
  Karimi's exact family.
- **Public indexes above n = 1000** (not known to me before): Francisco Couzo's `certified_bounds.json`
  (all n up to 10000, 2026-10-28) and Mykhailo Polkovskyi's records (2026-10-30). Together with Karimi's
  table the public frontier is 28 missing squares at K = 33 and 34, 29 at K = 35, 32 at K = 40, 38 at
  K = 50, 54 at K = 100. Stretched numerical packings are already registered there, so the block model
  is not a record above n = 1000 either.
- **Exact refill around public cores** (`search/fu_refill_public.py`, 562 packings, K = 9..32): equal to the
  source in 184 cases, lower in 374, higher in 4, never above the Kaggle bar.
- **Core edits with exact refill** (`search/fu_core.py`) from the public parents at n = 344 and n = 465:
  no layout with one more square. These parents are arcs running from wall to wall; a bar cannot be added.
- **One more square by a tolerant refill, then exact polish** (`search/fu_softseed.py`): no seed at all for
  274, 345 and 383; polished sides 22.0296 for n = 466, 27.0186 for n = 707 and 31.0002 for n = 936, all
  above the grid side.
- **Why the closure pass for n = 325..1000 was not run.** In the Kaggle table of 11-14 the leader's
  frontier entries change in linked pairs on the same day (819 and 707; 1000 and 937; 308 and 273).
  That is consistent with removing a cross of two strips, which keeps the number of missing squares;
  it is my inference, not something they state. If they run such closures daily from better parents,
  the pass planned for the pod had no realistic chance. No pod was rented.
- **Sources for the two certificates of the run, re-read at 19:56 UTC.** n = 147: the Squares Project
  case is unchanged (12.65685424949238) and no claim is open. n = 228: a registration request was
  opened today (jlevy/squares#983, by kenaznia-doga for Doğa Özden) with side 15.600801734812; it
  discloses the Kaggle side-only value 15.596043116646. The certificate of this run
  (`certificates/n228_S59604312.json`, 15.596043120920791…) is 0.00476 below that request and 4.3e-9
  above the Kaggle value.

## Where this leaves the plan

- A general theorem for "where the grid falls" exists (Daniel, Fang), with constant 4*sqrt(2). The
  numerical frontier is near 4*sqrt(K) and is maintained daily by teams that apply the same closures.
- The exact-refill block model built here beats the published exact construction by two squares at
  K = 17 and ties the best exact table at K = 35. It is three squares short of the numerical record at
  K = 17 and is not a record anywhere.
- No strict record was found. **Pod spend: US$ 0 of the US$ 20 approved.**
- What is still worth something: the two certificates of the run are, as far as the public sources
  show today, better than any packing registered for n = 147 and n = 228, and others are now filing
  packings for the same counts.

## Registration drafts (2026-11-14, prepared at the human's request; nothing sent)

- Sources re-read at 20:00 UTC: no claim for n = 147 anywhere in the tracker; for n = 228 only the open
  request jlevy/squares#983 (side 15.600801734812). Kaggle per-puzzle table of the same day: n = 147
  Nevska 12.651043553172632… (2026-11-07), n = 228 Nevska 15.596043116631669… (2026-11-08).
- The two certificates touch the walls exactly (wall margin 0; pair margins 3.0e-10 and 2.4e-10). The
  frozen verifier allows that; some public checkers do not. `evidence/registration/` therefore also
  holds the same packings moved by (1e-15, 1e-15) in a square larger by 2e-15, which pass the strict
  check (`search/fu_strict_check.py`) and the frozen verifier.
- `evidence/registration/issue_n147.md` and `issue_n228.md` are the drafts, in the form of the registry's
  result-registration template. They claim a first public packing, not a record, name the Kaggle
  side-only entries first, and ask that Evan Daniel's n = 229 packing and Francisco Couzo's n = 404
  packing be credited as the starts. In these copies the pinned revision is a placeholder, because a
  file cannot name the commit that contains it; the posted requests carry the full commit id.

## Registration requests posted (2026-11-14)

- The human approved the two requests with the credit name "Roberto Ono" and the push of this branch.
- Branch pushed to the public repository at revision fce076f2bf459a25be3645d899e8950b93ed977c. A fresh
  clone of that revision reproduces every check (verifier hash and tests, the frozen verifier on the
  two certificates and on the two strict variants, the independent check, the strict check).
- Last look at the registry before posting, 20:10:56 UTC: no claim for either side; registry head
  fa980f8e70; cases n-147 and n-228 unchanged.
- https://github.com/jlevy/squares/issues/984 : s(228) ≤ 15.596043120921, posted 20:11:25 UTC.
- https://github.com/jlevy/squares/issues/985 : s(147) ≤ 12.651043556588, posted 20:11:26 UTC.
- `evidence/registration/issue_n147.md` and `issue_n228.md` are the texts as posted. Both are claims of a
  first public packing, not of a record.
