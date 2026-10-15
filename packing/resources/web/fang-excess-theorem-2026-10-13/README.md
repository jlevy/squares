# Kevin Fang’s Excess Theorem: n² − n + F(n) Squares Below Side n

[TheSnakeFang/squarepack-certs](https://github.com/TheSnakeFang/squarepack-certs/tree/078789a4cfd36f915f1bfbe76d742413d79b2965)
at `078789a4cfd36f915f1bfbe76d742413d79b2965` (tree
`89b612b787b7a2004e26cc217011b0999dc5b092`, committed 2026-10-13T06:57:58Z, the
repository’s head when read) states two theorems of a note, *Packing n² − n + 1 unit
squares in a square of side less than n, for every n ≥ 15* (Kevin Fang, draft v0.6,
2026-10-13), and ships the certificates and the program behind them:

- **Theorem 1.** $s(n^2 - n + 1) < n$ for every integer $n \ge 15$, that is
  $c^*(n) \le n - 2$.
- **Theorem 2.** For $n \ge 15$ and integers $p, q \ge 0$ with $16p + 21q \le n - 15$,
  $n^2 - n + 1 + p + 2q$ unit squares pack in a square of side less than $n$; in
  particular $s(n^2 - n + F(n)) < n$ with
  $F(n) = 1 + \max\{p + 2q : 16p + 21q \le n - 15\}$, that is $c^*(n) \le n - 1 - F(n)$.

The proof glues a squeezable 17 × 16 rectangle R, or a 22 × 21 rectangle R′ that adds
two squares, onto a square packing (Lemma 3, implemented in `tools/glue.py`), and
inducts on $n$ from finitely many certificates.
The note itself is not in the repository.
Nothing on GitHub reported this release; the 2026-10-14 watch survey found it, and bead
`think-0esw` owns its import.
The sources were retrieved at 2026-10-14T09:19:47Z.

The direct square packings of the same commit (`nNNNN/`, 380 to 814 squares) are another
packet’s, owned by bead `think-7bw3`, and are not retained here.

## The Source’s History

Theorem 1 first appears in the README at `6028f31` (2026-10-12T19:16:34Z), with Theorem
2 in an earlier form, $s(n^2 - n + \lfloor (n + 1)/16 \rfloor) < n$, which is the case
$q = 0$ of the present one.
The rectangles R and four others came at `3f9896a` (2026-10-12T19:07:21Z), the gluing
program at `ba40e75`, the composites of the note’s Section 5 at `bef5c42`
(2026-10-12T19:13:41Z), R′ at `c284cd0` (2026-10-13T00:05:31Z), and the theorem
inventory `theorem/` at `5f3bdbf` (2026-10-13T05:54:24Z). The head adds only the
README’s v0.6 statement of Theorem 2, the changelog, the verification notes and the
manifest.

## Every Claim of the Release

| Claim | Where | Register action ([triage table](../../../campaign/result-import.md#stage-1-triage)) |
| --- | --- | --- |
| Theorems 1 and 2 for every $n \ge 15$ | `README.md` lines 12–17 | One entry stating the theorem, whose scope lists the cases the record holds: 211, 241, 273, 307 |
| Lemma 3, the gluing step | `tools/glue.py` lines 1–38, 84–165 | Part of that entry, for the review |
| R: 257 squares in $(17 - \delta) \times (16 - \delta)$, $\delta \ge 7.436 \times 10^{-4}$; R′: 443 squares in $(22 - d) \times (21 - d)$, $d \ge 0.0094$; four further rectangles of waste $b - 1$ | `rectangles/*/` | Premises of that entry |
| Base cases: $m^2 - m$ squares below side $m$ for $m = 11, \dots, 15$, and $n^2 - n + 1$ below side $n$ for $n = 15, \dots, 26$ | `third_party/daniel/`, the direct packings, de Winter’s 211 | Premises, each already a record bound or another import’s |
| 50 certificates of $n^2 - n + F(n)$ squares at side $n - 1/20000$ for $n = 15..64$, and 26 of a larger excess at the same side | `theorem/` | Finite bounds; see [Against the Record](#against-the-record) |
| 230 composites of draft v0.3’s Section 5, 38 of them shipped | `composites/` | An import of its own, below |
| Three checkers accept all 76 inventory certificates | `VERIFICATION.md`, last addendum | The source’s checks, for the claim’s text |

## Retained Here

`devtools.acquire_source` wrote the packet from a blobless clone checked out at the pin,
from the declaration in [acquisition/declaration.json](acquisition/declaration.json);
every file is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.

The scope is 200 files, 40.8 MB: the root `README.md`, `ATTRIBUTION.md`, `CHANGELOG.md`,
`VERIFICATION.md`, `LICENSE`, `MANIFEST.sha256` and `verify.py`, and the directories
`theorem/`, `rectangles/`, `tools/`, `third_party/` and `composites/`. 69 files, 1.6 MB,
are retained: every table, note and program in scope, the six rectangle certificates
(their JSON copies stored as deterministic gzip), the five small Daniel pieces below,
and the six inventory certificates the exact sample replays, at 211, 241, 273, 307, 308
and 932 squares. 131 files are pinned by digest only:

- **The other 70 inventory certificates, 16 MB:** decided bulk data under
  [`OR-18`](../../../../operating-rules.md#or-18-keep-bulk-data-out-of-git-and-never-bind-code-or-verdicts-to-a-git-commit-or-blob)
  before any history held them, as the 2.6 MB and 4.5 MB Theorem 1.6 certificates of the
  [Ryu upper-bound packet](../squarepacker-k2-minus-c-upper-2026-10-09/README.md) were.
  When they are replayed, a hosted-data release or the packet of the W7 checker that
  replays them retains them, under bead `think-0esw`. Until then
  [acquisition/inventory-headers.json](acquisition/inventory-headers.json) freezes each
  one’s header and digest, the digest the manifest records, so the arithmetic below
  still covers all 76.
- **17 that another packet retains, compared byte for byte:** `verify.py`, unchanged
  since the [2026-10-10 packet](../fang-two-wedge-certificates-2026-10-10/README.md);
  Evan Daniel’s `verify_cert.py`, his licence, his three issue #489 certificates and 11
  of his 16 piece certificates, which the
  [2026-10-05 Daniel packet](../evand-square-packing-2026-10-05/README.md) and the
  [Hunt 3 packet](../evand-record-hunt3-2026-10-10/README.md) retain.
  The other five, `n-5`, `n-11`, `n-19`, `n-29` and `n-89`, are retained here.
- **The 38 shipped composites, 23 MB:** each regenerates bit for bit, by
  `tools/glue.py`, from pieces retained here and the direct packings, under the SHA-256
  that `composites/table.csv` lists.
  Their table, `REPRODUCE.md`, `reproduce.sh` and the two inputs are retained.
- **The six rectangle drawings**, under CC0, as no claim rests on them.

Five inventory certificates, at $n = 15, 31, 36, 52$ and $57$, whose base is the
211-square piece, contain Evan Daniel’s exact certificate of Joost de Winter’s
unlicensed packing, scaled; the source’s README says that piece is fetched and not
redistributed. The two of them retained here, at 15 and 31, are kept as factual data
under the owner’s decision of 9 October 2026
([Retained Factual Data](../known-best-packings/README.md#retained-factual-data)), and
the record already retains that certificate in the Daniel packet.
No program of the source was run.

## Exact Checks

### Every Header and Table

[`cases/asymptotic/fang_excess_inventory.py`](../../../cases/asymptotic/fang_excess_inventory.py),
written here from the README’s statement and sharing no code with the source, decides
the arithmetic of the whole release exactly from the retained files and the frozen
header list; its receipt is
[receipts/inventory-and-deficiency.json](receipts/inventory-and-deficiency.json).
The list must name exactly the 76 certificates the tables name, and each of the six
retained certificates must state its row’s header.
`--freeze-headers` wrote it from the checkout at the pin, holding each file’s bytes to
the SHA-256 the manifest pinned at acquisition, the one boundary a digest crosses here
([`OR-16`](../../../../operating-rules.md#or-16-use-git-for-repository-integrity-reserve-checksums-for-real-trust-boundaries),
allowlisted as an external checkout), and it reproduces the list byte for byte; each row
keeps that digest for the release that retains the file.
All five checks hold:

- **The inventory.** $F(n)$ and its maximiser, ties to the larger $q$, are recomputed
  for $n = 15..64$; every row of `theorem/inventory.tsv` names that $(p, q)$, a base
  $r = n - 16p - 21q$ in 15..30 and the count $n^2 - n + F(n)$, and each of the 50
  certificates’ headers states that count at side exactly $(20000n - 1)/20000$.
- **The best excess.** Each of the 26 `theorem/best/` headers states $n^2 - n + j$
  squares at the same side, with $j > F(n)$, as `best.tsv` lists.
- **The composites.** Each of the 230 rows of `composites/table.csv` has the count
  $n^2 - n + j$ and a printed side below $n$, and no row’s $j$ exceeds the inventory’s
  at its $n$.
- **The rectangles’ headers.** Each states its count and its exact width and height; the
  waste is $b - 1$, or $b - 2$ for R′, and the squeezes are
  $\delta_R = 0.000743692\ldots \ge 7.436 \times 10^{-4}$ and
  $d_{R'} = 0.009439616\ldots \ge 0.0094$, as the README states.
  Whether the squares lie in the rectangle is not decided: no checker here reads a
  rectangular container.
- **The uniform squeeze.** $1/10000$ is below every piece squeeze the record retains:
  the six rectangles, Daniel’s seven pieces, the 211 piece and $n = 308, 343, 344$. The
  least is 308’s, 0.000690145. The direct packings of `think-7bw3`, among them 814,
  which `PIECES.md` names as the least at 0.000126396, are not retained on `main`.

### Exact Replay of a Sample

`devtools.upper_bound_reports` reads the six retained certificates in Daniel’s format
and admits each at the side its table prints, and its claim record compares each with
the record (below). The geometry runs through the maintained two-route kernel of
`devtools.evand_arrangement_reports`: `sqpack`’s exact witness verifier and the
independent rational corner checker, each deciding every wall and every pair over
$\mathbb{Q}$ after an exact half-angle conversion, with a duplicate-square and an
outside-container control for each count, each job in its own child process, one worker.

All six positives pass both routes, and both routes refuse all twelve controls, each on
the overlap or the wall it was built to break.
In every positive the two routes find the same least wall clearance and least pair gap,
exactly. Each is close to what the final strictification adds: with $d_0 = 1/10000$ and
$\lambda - 1 = d_0/(2(n - d_0))$, the least pair gap is $\lambda - 1$ and the least wall
clearance $(\lambda - 1)/2$, exactly at 932, where the integer blocks touch, and larger
by a relative $3 \times 10^{-15}$ to $3 \times 10^{-9}$ at the five base pieces, whose
own margins remain. 307 and 308 share theirs, since 307 is 308 truncated.

| Count | Certificate | Chain | Positive, both routes | Controls refused | Least pair gap | Route CPU s, three jobs |
| --- | --- | --- | --- | --- | --- | --- |
| 211 | `theorem/n015_F1.cert` | the 211 piece | pass | 2 of 2 | $3.33336 \times 10^{-6}$ | 51.5 |
| 241 | `theorem/n016_F1.cert` | the 241 piece | pass | 2 of 2 | $3.12502 \times 10^{-6}$ | 65.5 |
| 273 | `theorem/n017_F1.cert` | the 273 piece | pass | 2 of 2 | $2.94119 \times 10^{-6}$ | 85.6 |
| 307 | `theorem/n018_F1.cert` | 308, truncated | pass | 2 of 2 | $2.77779 \times 10^{-6}$ | 150.1 |
| 308 | `theorem/best/n018_j2.cert` | 308 | pass | 2 of 2 | $2.77779 \times 10^{-6}$ | 153.4 |
| 932 | `theorem/n031_F2.cert` | the 211 piece and R | pass | 2 of 2 | $1/619998$ | 772.5 |

The 18 jobs made 3,697,788 pair decisions in 1,278.6 route CPU seconds and 1,733.9 job
wall seconds, summed; the longest job took 485.4 seconds, and the one-worker run 29
minutes 57 seconds on a machine other lanes shared.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.
The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. No source program ran here.

The kernel decides every pair, $N(N - 1)/2$ per job and route: 0.69 ms a pair and job in
this run, so the 76 certificates would take about 100 CPU-hours, and the 44 above 1,263
squares exceed the kernel’s 600-second ceiling for one job.
The sample is the five counts the record holds, whose certificates are the theorem’s
base pieces at a larger side, and 932, the first count at which the inventory’s
certificate is the smallest report and the first instance of Lemma 3 in the sample: R
glued onto the 211 piece.

### What Was Not Run

- **The other 70 inventory certificates**, 343 to 4038 squares: 99.2 CPU-hours with this
  kernel, and not possible for the 44 above 1,263 squares inside its job ceiling, nor
  for the largest inside its 4 MB bound on one receipt.
  A bucketed route, deciding a pair only where the centres are at most $\sqrt 2$ apart
  (an exact rational test; farther pairs are disjoint), would cut each job to about ten
  pairs a square and all 76 to under an hour.
  That route is new deciding code, a W7 slice that needs its own soundness review, and
  so is a receipt that keeps verdicts and digests in place of every input.
  The certificates are pinned here, so that slice begins by retaining them, in a
  hosted-data release or its own packet, from the digests the frozen list carries.
- **The six rectangles in both dimensions:** no first-party checker reads an `n W H`
  container, and Daniel’s checker reads only the width, so it checks the square of side
  $W$. A rectangle route is a W7 slice, priced at under a minute for all six once
  written.
- **Lemma 3 and the induction:** the mathematical review, from the retained README and
  `tools/glue.py`, runs in its own lane.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes the six retained certificates
against the record as it stood when read (`main` at `f73e9de13`, 14 October 2026), and
`check-claims` rebuilds it.
The other 70 are compared from the frozen header list by
`fang_excess_inventory --print`, against the record’s rows that its receipt freezes, the
composites’ table and the direct packings’ table, which a test holds to the counts
below. Every count with a row on `main` is above that row:

- **211, 241, 273, 307 and 308**, the counts in the case corpus: above each case’s
  bound, Daniil Ostashev’s 14.99634 (T-149), Daniel’s exact optima 15.98813 and 16.98393
  (T-098), SQUISH’s 17.98086 (T-136) and Daniel’s 17.99827 after Fang (T-141), and at
  308 above Fang’s own 17.99931 (T-135). The theorem’s base pieces are those packings or
  copies of them at a larger side.
- **343, 344 and 381:** above the current beyond-horizon rows, Daniel’s 18.97823 and
  Couzo’s 18.99435 and 19.99266.
- **12 counts from 382 to 814:** above the direct packing of the same count in this
  commit, `think-7bw3`’s.
- **26 counts from 703 to 3084:** above a Section 5 composite of the same count, from
  the earlier commit `bef5c42`.

At the other **30 counts the inventory’s certificate is the only report below the
grid**: 932, 1486, 1564, 1643, 1644, 1725, 1726, 1809, 1810, 1895, 1896, 1983, 2073,
2165, 2356, 2975, 3085, 3197, 3311, 3427, 3545, 3546, 3665, 3666, 3787, 3788, 3911,
3912, 4037 and 4038, each at $n - 1/20000$. Of those, only 932’s certificate is
retained, so
[acquisition/beyond-horizon-claims.json](acquisition/beyond-horizon-claims.json), the
record a beyond-horizon row is read from, holds its claim alone; the other 29 join it
when their certificates are retained.

The composites are a release of their own, from `bef5c42`. The receipt’s composite map
finds a composite the smallest report at 81 of their 84 counts, 38 of them shipped
certificates and 43 table rows the source regenerates and does not ship; at 306, 342 and
380 a record row is smaller.
They are not imported here.

## The Deficiency Bounds

`deficiency_upper_bounds` in
[asymptotic-waste-bounds.yaml](../../../frontier/asymptotic-waste-bounds.yaml) holds
Sungjoon Ryu’s $c^*(k) \le 8\lceil\sqrt{k - 4}\rceil - 1$ for $k \ge 6$ and quotes
Arslanov, Mustafin and Shangitbayev’s $c^*(k) \le k - 1$. Theorem 2 is smaller than both
at every $k$ from 15 to 78 and at 86; it ties Ryu’s at 79 and 87, and Ryu’s is smaller
at 80–85 and at every $k$ from 88 to 2,000, where the search ends.
For large $k$, $F(k) \approx 2k/21$, so Theorem 2 reads $c^*(k) \lesssim (19/21)k$,
against Ryu’s $O(\sqrt k)$.

| k | F(k) | AMS | Ryu | Thm 1 | Thm 2 | Inventory | Record rows | Theorems: before → after |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15 | 1 | 14 | 31 | 13 | 13 | 13 | 13 | 14 → 13 |
| 16 | 1 | 15 | 31 | 14 | 14 | 14 | 14 | 15 → 14 |
| 17 | 1 | 16 | 31 | 15 | 15 | 15 | 15 | 16 → 15 |
| 18 | 1 | 17 | 31 | 16 | 16 | 15 | 15 | 17 → 16 |
| 19 | 1 | 18 | 31 | 17 | 17 | 16 | 16 | 18 → 17 |
| 20 | 1 | 19 | 31 | 18 | 18 | 17 | 18 | 19 → 18 |
| 21 | 1 | 20 | 39 | 19 | 19 | 18 | – | 20 → 19 |
| 22 | 1 | 21 | 39 | 20 | 20 | 19 | – | 21 → 20 |
| 23 | 1 | 22 | 39 | 21 | 21 | 20 | – | 22 → 21 |
| 24 | 1 | 23 | 39 | 22 | 22 | 22 | – | 23 → 22 |
| 25 | 1 | 24 | 39 | 23 | 23 | 23 | – | 24 → 23 |
| 26 | 1 | 25 | 39 | 24 | 24 | 24 | – | 25 → 24 |
| 27 | 1 | 26 | 39 | 25 | 25 | 25 | – | 26 → 25 |
| 28 | 1 | 27 | 39 | 26 | 26 | 25 | – | 27 → 26 |
| 29 | 1 | 28 | 39 | 27 | 27 | 26 | – | 28 → 27 |
| 30 | 1 | 29 | 47 | 28 | 28 | 28 | – | 29 → 28 |
| 31 | 2 | 30 | 47 | 29 | 28 | 28 | – | 30 → 28 |
| 32 | 2 | 31 | 47 | 30 | 29 | 29 | – | 31 → 29 |
| 33 | 2 | 32 | 47 | 31 | 30 | 30 | – | 32 → 30 |
| 34 | 2 | 33 | 47 | 32 | 31 | 30 | – | 33 → 31 |
| 35 | 2 | 34 | 47 | 33 | 32 | 31 | – | 34 → 32 |
| 36 | 3 | 35 | 47 | 34 | 32 | 32 | – | 35 → 32 |
| 37 | 3 | 36 | 47 | 35 | 33 | 33 | – | 36 → 33 |
| 38 | 3 | 37 | 47 | 36 | 34 | 34 | – | 37 → 34 |
| 39 | 3 | 38 | 47 | 37 | 35 | 34 | – | 38 → 35 |
| 40 | 3 | 39 | 47 | 38 | 36 | 35 | – | 39 → 36 |
| 41 | 3 | 40 | 55 | 39 | 37 | 36 | – | 40 → 37 |
| 42 | 3 | 41 | 55 | 40 | 38 | 37 | – | 41 → 38 |
| 43 | 3 | 42 | 55 | 41 | 39 | 38 | – | 42 → 39 |
| 44 | 3 | 43 | 55 | 42 | 40 | 39 | – | 43 → 40 |
| 45 | 3 | 44 | 55 | 43 | 41 | 41 | – | 44 → 41 |
| 46 | 3 | 45 | 55 | 44 | 42 | 42 | – | 45 → 42 |
| 47 | 3 | 46 | 55 | 45 | 43 | 43 | – | 46 → 43 |
| 48 | 3 | 47 | 55 | 46 | 44 | 44 | – | 47 → 44 |
| 49 | 3 | 48 | 55 | 47 | 45 | 44 | – | 48 → 45 |
| 50 | 3 | 49 | 55 | 48 | 46 | 45 | – | 49 → 46 |
| 51 | 3 | 50 | 55 | 49 | 47 | 46 | – | 50 → 47 |
| 52 | 4 | 51 | 55 | 50 | 47 | 47 | – | 51 → 47 |
| 53 | 4 | 52 | 55 | 51 | 48 | 48 | – | 52 → 48 |
| 54 | 4 | 53 | 63 | 52 | 49 | 49 | – | 53 → 49 |
| 55 | 4 | 54 | 63 | 53 | 50 | 49 | – | 54 → 50 |
| 56 | 4 | 55 | 63 | 54 | 51 | 50 | – | 55 → 51 |
| 57 | 5 | 56 | 63 | 55 | 51 | 51 | – | 56 → 51 |
| 58 | 5 | 57 | 63 | 56 | 52 | 52 | – | 57 → 52 |
| 59 | 5 | 58 | 63 | 57 | 53 | 53 | – | 58 → 53 |
| 60 | 5 | 59 | 63 | 58 | 54 | 53 | – | 59 → 54 |
| 61 | 5 | 60 | 63 | 59 | 55 | 54 | – | 60 → 55 |
| 62 | 5 | 61 | 63 | 60 | 56 | 55 | – | 61 → 56 |
| 63 | 5 | 62 | 63 | 61 | 57 | 56 | – | 62 → 57 |
| 64 | 5 | 63 | 63 | 62 | 58 | 57 | – | 63 → 58 |
| 65 | 5 | 64 | 63 | 63 | 59 | – | – | 63 → 59 |
| 66 | 5 | 65 | 63 | 64 | 60 | – | – | 63 → 60 |
| 67 | 5 | 66 | 63 | 65 | 61 | – | – | 63 → 61 |
| 68 | 5 | 67 | 63 | 66 | 62 | – | – | 63 → 62 |
| 69 | 5 | 68 | 71 | 67 | 63 | – | – | 68 → 63 |
| 70 | 5 | 69 | 71 | 68 | 64 | – | – | 69 → 64 |
| 71 | 5 | 70 | 71 | 69 | 65 | – | – | 70 → 65 |
| 72 | 5 | 71 | 71 | 70 | 66 | – | – | 71 → 66 |

*Inventory* is $k - 1 - j$ for the largest excess $j$ a certificate of `theorem/`
reaches. *Record rows* is $k^2 - m - 1$ for the largest count $m \le k^2$ whose recorded
upper bound is below $k$: the case records to 324, the beyond-horizon rows above.
At $k = 15, 16, 17$ Theorem 2 equals the record’s own finite rows, since its bases are
those packings; at 18 and 19 the record is one smaller, from the 308 and 344 packings;
at 20 the inventory’s 382 is one below the record.

## Register Plan

For the records lane, which takes the `T-NNN` and writes stage 3:

- **One register entry for the theorem.** `kind: upper-bound`; scope
  `n_values: [211, 241, 273, 307]`, the counts $n^2 - n + F(n)$ for $n = 15..18$, where
  $F = 1$; `attribution.published: 2026-10-13`, the inventory’s first commit and the
  note’s date, with source key **[Fang excess theorem 2026-10-13]**. Headline:
  “$s(n^2 - n + 1) < n$ for every $n \ge 15$, and $n^2 - n + F(n)$ squares below side
  $n$, from Kevin Fang”.
  The claim states Theorems 1 and 2 as above, then the in-scope bounds the inventory
  certifies, in the checker’s form: `s(211) <= 14.99995`, `s(241) <= 15.99995`,
  `s(273) <= 16.99995` and `s(307) <= 17.99995`. Each is above its case’s bound, so
  `check_standing` derives *superseded* at all four, by T-149, T-098 and T-136. That is
  true of those finite bounds and silent on the theorem past the case corpus, which no
  other result implies; whether the entry should carry the mark is the owner’s question.
- **Ratings.** `V2`, declared, since the note that holds the proof is not public and the
  argument is recoverable only from the README’s outline and `tools/glue.py`; `C0` until
  the review lands. The replayed sample is `C3` evidence for the four in-scope sides, and
  the `composition` note says the induction sets the minimum.
  Significance `S4`, draft: a bound family.
  Novelty `previously-published`.
- **`next_rung`:** the mathematical review of Lemma 3 and the induction; the note, draft
  v0.6, asked of the author; the 70 unreplayed inventory certificates, retained by a
  hosted-data release or the W7 packet, by a bucketed exact route, and the six
  rectangles by a rectangle route (W7).
- **`unfinished_confirmations`:** the review of Lemma 3 and the induction, rung `C1`,
  bead `think-0esw`, no CPU price.
  The 70 replays move no rung of this entry and are not listed; they are the
  beyond-horizon rows’ evidence.
- **Evidence.** `E-fang-excess-theorem-report` (`assurance: reported`,
  `novelty: previously-published`, the theorem and its four in-scope cases) and
  `E-fang-excess-theorem-exact-feasibility` (`origin: replayed-here`, exact-algebraic,
  scope the replayed counts 211, 241, 273, 307 and 308, with 932 beyond the corpus, and
  the receipt in `receipts/`), naming `sqpack`’s exact verifier and the independent
  rational checker in `verifiers`,
  `relationship_to_generator: independent-implementation`.
- **Coverage.** A `source-coverage.yaml` entry for this packet whose `claims_record` is
  `acquisition/beyond-horizon-claims.json`, and one `beyond_horizon_claims` row at 932,
  `assurance: reported` (`verified` once its replay evidence is registered),
  `disposition: tracked-outside-case-corpus`, bead `think-0esw`. The other 29 counts
  wait for their certificates to be retained, by the hosted-data release or the W7
  packet, which then adds their claims to this packet’s claims record or its own.
  No case record changes.
- **The deficiency list.** A new row in `deficiency_upper_bounds`: “REPORTED:
  $c^*(k) \le k - 1 - F(k)$ for every integer $k \ge 15$ (Theorem 2), in particular
  $c^*(k) \le k - 2$ (Theorem 1)”; exponent 1; kernel “k, at integer sides approached
  from below”; constant “$F(k) = 1 + \max\{p + 2q : 16p + 21q \le k - 15\}$, about
  $2(k - 15)/21$”; corollary “smaller than Ryu’s Theorem 1.4 for $15 \le k \le 78$ and
  at $k = 86$, tied at 79 and 87, larger at 80–85 and from 88; smaller than Arslanov,
  Mustafin and Shangitbayev’s $k - 1$ for every $k \ge 15$”. Ryu’s corollary, which says
  it improves Arslanov, Mustafin and Shangitbayev’s $k - 1$ at 65–68 and from 73, gains
  that Fang’s Theorem 1 gives $k - 2$ at every $k \ge 15$. The file’s `open_problem` and
  `relevance_to_small_n`, which call the deficiency bounds weaker than every atlas value
  for $k \le 18$, gain that this one equals the atlas at $k = 15, 16, 17$.
- **Bibliography and credit.** `bibliography.yaml` and the
  [resources README](../../README.md) define the key, in this change.
  Credit:
  `Fang after Arslanov, Mustafin, Shangitbayev, Ellsworth, Stead, de Winter, Daniel, Couzo`,
  `lineage: independent`. `ATTRIBUTION.md` now thanks the Squares Project for replaying
  308, 343 and 344 and registering de Winter’s 211; that credits verification, not
  method, so there is no `after Levy`.
- **Not registered.** The 26 best-excess certificates and the 50 others at counts beyond
  324 enter no register entry, and the composites wait for an import of their own.

## For the Mathematical Review

The argument is spread over these retained files:

- `source/README.md` lines 9–17, the statements and the outline; lines 19–30, which
  piece serves which step; lines 94–102, the certificate convention (centres in the open
  box, strict separation along an edge normal).
- `source/tools/glue.py` lines 1–38, Lemma 3 as the docstring states it; lines 84–107,
  the four regions and their tiling check; lines 115–165, the hypotheses ($a > b$,
  $d = \min(d_A, d_B, 1/2) > 0$, $n = b + b' \ge a$, $c = n - a' \ge 0$, $c \le a - d$),
  the placement, the count $n^2 - w_A - w_B$ and the scaling by $1 + 2^{-64}$; lines
  24–34, the uniform squeeze and the final scaling by $1 + d_0/(2(n - d_0))$ to side
  $n - d_0/2$.
- `source/theorem/README.md` and `source/theorem/PIECES.md`, “Definitions”: the uniform
  construction, the base for each residue $r = 15..30$, the `[k]` truncation of a base
  to excess 1, and what `best.tsv` ranges over.
- `source/theorem/inventory.tsv`, column `chain`: the gluing order of each certificate.
- `source/rectangles/r17x16_n0257/NOTES.md` and
  `source/rectangles/r22x21_n0443/NOTES.md`: R’s and R′’s box, waste and exact squeeze.
- `source/CHANGELOG.md`, the 2026-10-13 entries: R′ gives $j(n) \ge j(n - 21) + 2$.
- `source/ATTRIBUTION.md`, “Review”: another model reviewed an early draft, and v0.2
  corrected the errors it found.

The base cases the induction needs are Daniel’s $m^2 - m$ certificates at $m = 11..14$
(the [2026-10-05 packet](../evand-square-packing-2026-10-05/README.md)), the 211, 241
and 273 pieces, $n = 308$ truncated to 307, and the direct packings at $n = 19..26$,
which `think-7bw3` retains.

## What Is Not Established

The certificates establish finite upper bounds at side $n - 1/20000$ and nothing more.
The theorems for every $n \ge 15$ rest on Lemma 3 and an induction stated in a note that
is not public, and no review of them has been made here.
The rectangles are checked here by their headers only.
No exact form, local minimality or optimality is claimed by the source or established
here. `best.tsv` is, in the source’s words, a lower-bound inventory of these pieces, not
a claim that no other packing does better.

## Credit and Licence

Kevin Fang wrote the source.
`LICENSE` puts `verify.py`, `tools/glue.py`, `tools/rectcheck.py` and the shell scripts
under the MIT licence; the README and `ATTRIBUTION.md` release the certificates, text
files, tables and drawings in `nNNNN/`, `rectangles/` and `composites/` under CC0 1.0
and name no licence for `theorem/`. `third_party/daniel/` and
`tools/verify_cert_daniel.py` are Evan Daniel’s, under the MIT licence of
`third_party/daniel/LICENSE`. `ATTRIBUTION.md` credits the construction to Arslanov,
Mustafin and Shangitbayev (Electronic Journal of Combinatorics 28(4), P4.22, 2021, doi
10.37236/8586), whose decomposition is Lemma 3; seeds to David Ellsworth and Tej Stead
(241, 273 and 307), Joost de Winter (211, the base case $n = 15$) and Francisco Couzo
(342, the seed of 380, 381, 421 and the 21 × 20 and 22 × 21 rectangles); the format, the
checker and the pieces to Evan Daniel; and the JSON layout to SQUISH. It names Daniil
Ostashev’s later 211, which no certificate uses, and thanks the Squares Project for
replaying 308, 343 and 344. The source states that the search, the verifier and the
bundle were written and run with Claude (Anthropic) as a coding and research agent,
directed and reviewed by Kevin Fang, and that another model, GPT-6 Astra, reviewed an
early draft of the note.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source fang-excess-theorem-2026-10-13 --check
uv run --frozen --all-extras --group dev python -m cases.asymptotic.fang_excess_inventory --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports fang-excess-theorem-2026-10-13 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports fang-excess-theorem-2026-10-13 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports fang-excess-theorem-2026-10-13 check --replay
```

`check` admits the sample receipt structurally against the retained certificates; only
`--replay` decides the geometry again, about 21 CPU-minutes.
`fang_excess_inventory --write` reads the live record again and rewrites its receipt;
`--print` prints the deficiency table and each of the 76 certificates against the
record; `--freeze-headers CHECKOUT` rewrites the frozen header list from a checkout at
the pin. The importer’s `register-plan` prints its finite-certificate template, which
assumes the certificates improve their cases; it does not fit this import, and the
[Register Plan](#register-plan) above takes its place.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `source/rectangles/r17x16_n0257/r17x16_n0257.cert.json.gz` | upstream | `246b79f35467289a06e54679e4ad9a63af7748b7` | `271c39af557c68c8687f9adcba34070473e3cf4b9a84d23ca2a93dc433a193ea` |
| `source/rectangles/r18x17_n0290/r18x17_n0290.cert.json.gz` | upstream | `95ef560af4e94cbe3539834b723b2ef8bd736fc4` | `95b76f875d804c3b70585fba600ff80198ddacbc3c6022396fd64b5eb9c80246` |
| `source/rectangles/r19x18_n0325/r19x18_n0325.cert.json.gz` | upstream | `0318228e15bbf49e7a732b983c97006ff4ab9f68` | `e3eb56866a44a8287053d9901157b1b0c657e0353ece3155439bc66100031ba8` |
| `source/rectangles/r21x20_n0401/r21x20_n0401.cert.json.gz` | upstream | `f5fd314a07bd4a0a0db31adcc541ce697afa0943` | `586f856c75f52e9f6aeb73f7586412eea8b9e31ab1d9b527235082e419c76c6d` |
| `source/rectangles/r22x21_n0442/r22x21_n0442.cert.json.gz` | upstream | `f9b2caf17bb677f38c99332e3bf80e3b1d51f8d7` | `c0ed9623194484476f6c2d0fa52624fceed99a16b239b11d1533a165ef0acfec` |
| `source/rectangles/r22x21_n0443/r22x21_n0443.cert.json.gz` | upstream | `dd39a8bd17b6d4e8576b09c9959393d3500e8963` | `e9dce6cd6d60e138309200b0e00b35c826d522743d3ede9caf9b4efb9a0106b3` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
