# A closed-form lower bound for packing unit squares in a square (all N ≥ 49)

Let s(N) be the side of the smallest square that holds N unit squares with disjoint interiors (any positions,
any angles). This folder contains a computer-assisted proof of a lower bound for s(N) that holds for every
non-square N ≥ 49 and is given by one square root on each of 34 intervals of the fractional part.

## What is claimed

Write a = k + δ with k = ⌊√N⌋ and 0 < δ ≤ 1. The interval (0, 1] is split into 34 intervals I₁, …, I₃₄
(listed in `INTERVALS.md`; exact data in `intervals.json`). On each interval the certificate proves a saving
S_i(δ) = α_i δ + β_i with exact rationals α_i, β_i.

**Theorem.** Let N ≥ 49 be a non-square integer and k = ⌊√N⌋. If δ ∈ (0, 1] lies in I_i and
(k + δ)² − 4(α_i δ + β_i) < N, then s(N) ≥ k + δ. Hence

    s(N) ≥ a(N) = max over i of min( 2α_i + √(4α_i² + N + 4β_i − 4α_i k),  k + d1_i ),

the maximum taken over the intervals I_i = [d0_i, d1_i] whose root 2α_i + √(…) exceeds k + d0_i
(SPEC.md §1.1 gives the precise statement).

**Computing a(N).** `python3 a_of_n.py N` (or a range `N1-N2`) prints a(N) rounded down and the interval that
attains it, for example `50: a(N) = 7.126165352 (k = 7, interval 4)`; `--exact` also prints the exact form; all choices are made in exact rational arithmetic, so the printed decimal is
itself a valid lower bound. Example: for N = 50 we have k = 7, and the interval I₄ = [3/25, 4/25] gives
a₄(50) = 2α₄ + √(4α₄² + 50 + 4β₄ − 28α₄) = 7.126165352… ∈ (7 + 3/25, 7 + 4/25], which is the maximum, so
s(50) ≥ 7.126165352. For comparison, Karakuş's formula gives 1/2 + √(173/4) = 7.076473….

| N | k | a(N) (rounded down) | interval | Karakuş 1/2 + √(N − k + 1/4) |
|---|---|---|---|---|
| 50 | 7 | 7.126165 | 4 | 7.076473 |
| 56 | 7 | 7.646996 | 29 | 7.517834 |
| 61 | 7 | 8 | 34 | 7.865460 |
| 62 | 7 | 8 | 34 | 7.933034 |
| 65 | 8 | 8.102316 | 3 | 8.066373 |
| 72 | 8 | 8.625600 | 29 | 8.515610 |
| 78 | 8 | 9 | 34 | 8.881527 |
| 79 | 8 | 9 | 34 | 8.940972 |
| 82 | 9 | 9.084905 | 3 | 9.058621 |
| 90 | 9 | 9.608267 | 28 | 9.513878 |
| 97 | 9 | 10 | 34 | 9.894147 |
| 98 | 9 | 10 | 34 | 9.947222 |
| 101 | 10 | 10.072531 | 3 | 10.052487 |
| 110 | 10 | 10.600000 | 27 | 10.512492 |
| 118 | 10 | 11 | 34 | 10.904326 |
| 119 | 10 | 11 | 34 | 10.952272 |
| 122 | 11 | 11.063292 | 3 | 11.047512 |
| 132 | 11 | 11.600000 | 27 | 11.511358 |
| 141 | 11 | 12 | 34 | 11.912712 |
| 142 | 11 | 12 | 34 | 11.956439 |
| 145 | 12 | 12.056135 | 3 | 12.043396 |
| 156 | 12 | 12.591233 | 27 | 12.510412 |
| 166 | 12 | 13 | 34 | 12.919742 |
| 167 | 12 | 13 | 34 | 12.959936 |

The rows are N = k² + 1, k² + k, (k + 1)² − 3 and (k + 1)² − 2. The last column is rounded to six decimals
and capped at k + 1. The table for every N ≤ 3600 is in the write-up linked below.

**Comparison.** Nagamochi's formula F(N) = 1 + √(N − 2k + 1) corresponds in the same framework to the saving
δ/2, and Karakuş's formula 1/2 + √(N − k + 1/4) (arXiv:2609.37410, Corollary 6.2) corresponds to the saving δ/4. The certified saving exceeds δ/2 on all of
(0, 1] (by more than 0.0226 for δ ≥ 1/50, and by more than 1.229δ below). Therefore, for every non-square
N ≥ 49, with F(N) capped at k + 1 (since trivially s(N) ≤ k + 1):

- a(N) = F(N) = k + 1 for N = (k + 1)² − 1 and N = (k + 1)² − 2;
- a(N) > F(N) for every other N.

Likewise a(N) is strictly larger than Karakuş's value except at N = (k + 1)² − 1, where both are k + 1.
A gap in the proof of the key lemma behind F(N) has been publicly discussed (chelokot; jlevy/squares#295). Karakuş (arXiv:2609.37410) constructs counterexamples to the scoring assertion in Lemma 1 of Nagamochi's paper, which show that the published proof of Nagamochi's rectangle bound is incomplete; the paper states that they do not disprove the bound itself. It then proves a weaker rectangle bound with a strip measure, from which it derives s(N) ≥ 1/2 + √(N − k + 1/4) for every non-square N ≥ 8 and s(k² − 1) = k; it does not establish Nagamochi's full bound or s(k² − 2) = k. Our proof uses neither Nagamochi's lemma nor Karakuş's bound.

At the top of each block the bound gives s(N) = k + 1 for N = (k + 1)² − 1, (k + 1)² − 2 and (k + 1)² − 3
(k ≥ 7), because the certified saving at δ = 1 exceeds 3/4. These values are not new. s(n² − 1) = s(n² − 2) = n were stated by Nagamochi (2005); the proof of a key lemma there has a publicly discussed gap (jlevy/squares #295). Our bound gives these values for n ≥ 8 without using that lemma; Karakuş (arXiv:2609.37410) gives a proof of s(n² − 1) = n that also avoids it. s(n² − 3) = n for n ≥ 6 was proved by Evan Daniel (the Valid7 certificate in
github.com/evand/square-packing; an independent check is in github.com/wand125/square-packing/tree/main/checks/valid7).
Here they come out of the same general bound.

References: H. Nagamochi, Packing unit squares in a rectangle, Electron. J. Combin. 12(1) (2005), #R37, doi:10.37236/1934. H. Karakuş, A counterexample to Nagamochi's scoring lemma and a new rectangle packing bound, arXiv:2609.37410v1 [math.CO] (2026), https://arxiv.org/abs/2609.37410. jlevy/squares issue #295 (github.com/jlevy/squares/issues/295). E. Daniel, the Valid7 certificate for s(n² − 3) = n, github.com/evand/square-packing.

A longer write-up with the full table of the 34 intervals, a table of a(N) for N ≤ 3600 next to the best
known bounds, and comparison plots is at https://wand125.github.io/square-packing/paper-closed-form.html.

## How the proof works (short)

For a container of side a = k + δ we build a nonnegative measure μ on [0, a]² with μ(Q) ≥ 1 for every closed
unit square Q inside it. If the total mass is below N, then N unit squares cannot fit in any smaller square
(SPEC.md §1.2). The measure is a periodic wall profile along the four sides, line measures in the four corners
and Lebesgue measure in the middle; its total mass is a² − 4S(δ), where S is the saving (§1.3). A finite
"family" of line segments per interval of δ describes the measure for every k ≥ 7 at once (§§2–3).

That μ(Q) ≥ 1 for every square Q is checked on a box grid of square positions and angles in four local
regions (§4). Each root box of the grid is split into leaves, and each leaf is accepted by one of a fixed set
of exact tests (§5). The record of a region lists every root with its leaves and test kinds (§6). The checker
`replay4d` reads a family and a record, checks that the roots form exactly the grid of the region and the
leaves tile each root, and recomputes every leaf from scratch in exact rational arithmetic. Of a record it
uses only the boxes and the names of the tests.

Two parts of the argument are not done by `replay4d`. (1) The structure of each family: that its weights are
nonnegative (`replay4d` silently drops rows of weight ≤ 0 instead of rejecting them), that each wall period
carries mass 9/5, that the family's saving at both ends of the interval is at least the certified line,
that the measure assembled for k = 7, 8 and 9 agrees with the local model inside the checked windows, and
that the four regions cover the windows (SPEC.md §2.3 and §7.1, steps 1, 2 and 5). These are checked by
`structure/validate_family.py` (exact, Python standard library), run on all 68 families by
`structure/structure_all.py`, which also checks that each certified line is exactly the line through the
recomputed savings at the two ends and that the region bounds are the required ones. (2) Independence: `seam4d_core`, the core of
`replay4d`, is the same code that our search tools use to evaluate leaves, so the replay checks the records
against that code, not against an independent implementation.

## What was checked

- 34 intervals cover (0, 1].
- 136 records (4 regions per interval), 187,183,108 leaves in total.
- The structure of all 68 families was checked: `receipts/structure.json` (ALL STRUCTURE OK).
- Every leaf of every record was recomputed once by `replay4d` and accepted: `receipts/replay.json`.
  The replay ran on freshly installed Ubuntu 24.04.5 machines with rustc 1.86.0. Records larger than a set
  size were cut along grid lines into pieces for that run; each piece is again an exact grid of a sub-box,
  the pieces tile the region, and together they contain the lines of the original record. The receipts give,
  for each piece, its bounds, its number of roots (one line per root) and the sum modulo 2²⁵⁶ of the
  SHA-256 values of its lines; these sums are a consistency check that the pieces add up to the original
  record, not a proof. The published records are the original, uncut files.
- The replay used the same Rust code as `checker/`. For publication the comments were translated to English
  and the workspace was reduced to the two crates `seam4d_core` and `replay4d` (so the top-level
  `Cargo.toml` lists only these two, and `Cargo.lock` no longer lists the packages of the removed crates;
  the versions of the remaining packages are unchanged). Outside comments the `.rs` files are identical.
  The source hash printed by `replay4d` covers the manifests, `Cargo.lock` and the `.rs` files except
  `b3d_sort.rs`, so it differs: 306ad4b58b7e962f90e430b1adeaa8c52ad70f02f4807c96493036f6bb6cb476 for the replay,
  92002e0e8924d96f0e5962eabb8fce6e4de67a2f350ca66d4889abee0762c193 for the published sources. The published
  checker passes the same tests (28), and its exact build replayed all eight records of intervals 1 and 34
  from the published assets with REPLAY OK (3,138,681 leaves): `receipts/published_checker.json`.
- For publication two keys that no checker reads (`note`, a free-text comment, and `target`, a search
  target) were removed from the family files; otherwise the families are the ones that were replayed
  (`receipts/families.json` lists old and new SHA-256). That replay of intervals 1 and 34 used
  the published families.

The Python record checker used during development is not included either: it shares code with the search tools,
so it is not independent of them.

- An independent checker, `indep-checker/` (`cfcheck`, Rust), was written from `SPEC.md` and the published
  assets only and shares no code with `replay4d`, `seam4d_core` or the search tools. It checks the structure
  of the families and every leaf of the records with exact rational arithmetic. It replayed intervals 1 and 34
  completely (all four regions of each) and accepted every leaf with zero refusals: 91,044 roots and
  3,138,681 leaves, the same leaf count as `replay4d` on these two intervals. The reports are in
  `indep-checker/receipts/`. The other 32 intervals have not been checked with it.

## Files

- `SPEC.md`: the full specification (mathematics, family and record formats, every leaf test, the checks).
- `INTERVALS.md`, `intervals.json`: the 34 intervals, the certified lines, and for each region the record
  hash, region bounds, root and leaf counts by kind.
- `a_of_n.py`: computes a(N) from `intervals.json` (Python 3 standard library).
- `structure/`: `validate_family.py` and `structure_all.py`, the structure check of the families.
- `checker/`: the Rust checker (`seam4d_core` and `replay4d`) and `replay_all.py`.
- `indep-checker/`: the independent checker `cfcheck` (its own README, tests and receipts).
- `receipts/`: `replay.json` (the full replay), `structure.json` (the structure check), `families.json`
  (old and new family hashes) and `published_checker.json` (runs of the published build).
- Release `closed-form-v1`: one asset per interval, `interval_<d0>_<d1>.tar.gz`, containing `family.json`,
  `family_right.json`, `straddle.rec`, `left.rec`, `top.rec`, `right.rec` and `SHA256SUMS`, plus a
  `SHA256SUMS` over the 34 assets (about 0.8 GB in total; about 18 GB unpacked).

## How to check

Build the checker (Ubuntu; GMP is built from source, hence `m4`):

    sudo apt-get install -y build-essential m4 curl ca-certificates
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain 1.86.0
    cd problems/closed-form/checker
    cargo +1.86.0 test --locked --release -p seam4d_core -p replay4d
    cargo +1.86.0 build --locked --release -p replay4d

On macOS (with Homebrew) the GMP build of `gmp-mpfr-sys` can stop with "supports GMP 6.3.0, but 6.2.0 was found"
when an older GMP is found first; point the build at GMP 6.3 with, for example,
`export CPATH="$(brew --prefix gmp)/include" LIBRARY_PATH="$(brew --prefix gmp)/lib"` (after `brew install gmp`).

Download and check the data, then replay (from `problems/closed-form`):

    mkdir assets && cd assets && gh release download closed-form-v1 && sha256sum -c SHA256SUMS && cd ..
    python3 structure/structure_all.py --assets assets
    python3 checker/replay_all.py --assets assets --threads 16 --jobs 4

`structure_all.py` checks the families in about a minute and prints `ALL STRUCTURE OK`. `replay_all.py` checks every hash, runs `replay4d` on all 136 records and compares the root and leaf counts
with `intervals.json`; it prints `ALL REPLAY OK` at the end. It can be restarted and skips finished regions;
`--only 1,34` replays selected intervals. One full replay of all 136 records took 4,294 CPU-hours (each record replayed once; per-record and
per-region times are in `receipts/replay.json`).

## Author

Hiroaki Hosono (wand125).

## Licence

MIT (see `LICENSE`). `checker/seam4d_core/src/b3d_sort.rs` is a port of CPython's list sort and keeps its
licence in `checker/seam4d_core/src/CPYTHON_SORT_LICENSE`.
