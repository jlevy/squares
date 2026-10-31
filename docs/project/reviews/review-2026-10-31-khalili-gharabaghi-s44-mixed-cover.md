# Proof Review: Khalili and Gharabaghi’s `s(44) = 7` by a Closed Mixed Cover

**Date:** 2026-10-31. **Lane:** stage 4 of the
[result import runbook](../../../packing/campaign/result-import.md#stage-4-validate) for
issue [842](https://github.com/jlevy/squares/issues/842), bead `think-1v4b` (epic
`think-3guf`). **Reviewer:** Claude, strong sub-agent tier (`tbd-strong`), reasoning
setting not recorded, writing as a distinct pass of the same intake lane that retained
the source and replayed its checker, on the pass coordinator’s instruction.
That departs from the runbook, which asks for a separately prompted lane at the
strongest tier with no shared context; this pass shared the records lane’s context, and
the reader should weigh it as one adversarial read, not as an independent second
opinion. No earlier review of this result exists.

It is an adversarial soundness review of one claim: that 44 unit squares do not fit in a
square of side below 7, so $s(44) = 7$ with the $7 \times 7$ grid.
It re-derives the argument from the certificate to the claim, reads what the checker
that decided it assumes, compares that checker with the version earlier reviews derived,
reads the source’s second checker’s records, and checks the cover at exact poses and
against mutated copies with a program written for it.
What the source reports is said to be the source’s; what was computed here is said to
be.

## Summary

This summary is written for the authors, Mohsen Khalili and Sara Gharabaghi.

**The value stands.** The certificate is a nonnegative measure on $[0,7]^2$: 15,525
point masses and 3,912 pieces of mass spread uniformly along segments of length $1/50$
on the grid lines $x, y \in \lbrace 1, \ldots, 6 \rbrace$, of total
$2199755099/50000000 = 43.99510198 < 44$. If every closed unit square inside $[0,7]^2$,
at every centre and angle, captures mass at least 1, then 44 unit squares cannot fit in
a smaller square, and with the grid $s(44) = 7$. That reduction is correct as stated,
with every hypothesis met (§3). The covering statement is decided by Evan Daniel’s
`zmx2` at the commit your `verify.sh` pins, over the $D_4$ fundamental region and,
separately, over the whole pose space with no symmetry assumed.
Both sweeps were replayed here from retained bytes, and each root’s census equals your
published log’s (§5). I found no mathematical defect and no blocking finding (§9).

**What was checked here.** The cover was re-parsed with this review’s own reader and its
total, slack and $D_4$ invariance recomputed exactly (§4). The `zmx2.rs` that ran,
`e2bb84e9`, had not run in this record before; for a cover with no polygons, an integer
side and the default flags, its code path is the version that the reviews of 28
September and 2 October derived, function for function (§6, F2). The reviewed
`6b7f0f79`, built from retained bytes and run on the cover over the $D_4$ region, gives
every root the same census as `e2bb84e9`. Exact capture at 2,880 sampled admissible
poses, including the near-axis wall “valleys” your separation step targets, was never
below 1, lowest 1.003837 (§7). Two mutated covers are refused by `zmx2`, and at a pose
in each refused root the mutant captures less than 1 exactly while the published cover
captures more (§8). Your `zm_mixed.py` records, read with this review’s own code, cover
all 9,800 roots of their grid once, and every root left uncertified at depth 24 is
certified whole at depth 30 (§6.3).

**What is not established here.** No proof assistant checked anything.
`zmx2` is interval-certified, not exact-rational: its geometry is enclosed in binary64
with outward rounding and its mass comparisons are exact integers (F1). Its lemmas and
code are trusted as the earlier reviews derived them, and the host’s IEEE-754 arithmetic
is trusted. `zm_mixed.py` was not run here; its complete pass is priced at about 138 to
143 CPU-hours and held (`think-qvp6`).

**Questions, none blocking.** Whether the `zm_mixed.py` runs without `--cert-mode` were
deliberate (F4), and whether you can say which `zeromargin.py` the README’s
`DIFFERS FROM PINNED` note refers to beyond its digest (§11).

## 1. What Was Reviewed

| Item | Where |
| --- | --- |
| Source | [moh63-dev/s44-equals-7](https://github.com/moh63-dev/s44-equals-7) at `b5b1bc9d7354a8f62efcb6b7abeb30d1eb576aaf` (tag v1.1), retained whole but for `.gitignore` in the [packet](../../../packing/resources/web/moh63-dev-s44-equals-7-2026-10-29/README.md). The certificate is byte for byte the one first committed in `063c4d6` (tag v1.0), the commit the issue names |
| Certificate | `certificate/s44_cover_7.txt`, SHA-256 `c9fde0f1e7013f3f61f4a8d673b6bcaf9c5e54c914b6462164d7326ba254cae0`, Daniel’s mixed format v1 (`certificate/FORMAT_mixed_v1.md`) |
| Deciding checker | `zmx2` at evand/square-packing `659ee62e`: `verify2/src/bin/zmx2.rs` `e2bb84e9…`, byte-identical to the copy the evand-square-packing-2026-10-04 packet retains; `Cargo.toml` and `Cargo.lock` equal the retained ones |
| Source’s second checker | `zm_mixed.py` `1fd20346…` with `mixed_cover.py` `bb89de15…` and `zeromargin.py` `3cb95fb7…`, at the same commit; records in `verification/logs/zm_mixed/` |
| Source’s own checks | `verification/sanity.py` (exact), `verification/stress.py` (floating point), `search/tilesep.py` (floating point); read, not run |
| Paper | `paper/s44.pdf` and `paper/s44.tex`; the TeX was read in full, its §2 (“The method”) giving the reduction |
| Replay here | The packet’s `receipts/`: `zmx2 cert --d4` and `--full` from retained bytes, two controls |
| Programs written for this review | The packet’s [`review/`](../../../packing/resources/web/moh63-dev-s44-equals-7-2026-10-29/review/README.md) |

## 2. Verdict

**Accepted.** The claim $s(44) = 7$ follows from the cover property and the grid, the
cover property is decided by `zmx2` over the whole pose space twice (reduced and
unreduced), the replay reproduced both decisions root for root, and nothing found here
contradicts them. No finding is blocking; F1 to F6 are notes.

The confirmation is a reproduction with the producer’s code: `zmx2` is the checker the
authors ran, written by Evan Daniel, and its run here shows that the published decision
reproduces from the published bytes, not that a second implementation agrees.
The draft significance, S3, stands (§10).

## 3. From Certificate to Claim

### 3.1 The statement

$s(n)$ is the least side of a square that holds $n$ unit squares with pairwise disjoint
interiors, each at any position and rotation.
The claim is $s(44) \ge 7$; the $7 \times 7$ grid holds 49 squares, so $s(44) \le 7$ and
$s(44) = 7$.

### 3.2 The measure

The file defines $\mu = \sum_i w_i \delta_{p_i} + \sum_j m_j \lambda_{\sigma_j} /
|\sigma_j|$: a point mass $w_i \ge 0$ at each listed point and, for each listed closed
axis-parallel segment $\sigma_j$, mass $m_j \ge 0$ spread uniformly by length.
A closed set $Q$ captures $\mu(Q)$; a point on the boundary of $Q$ counts in full, and a
segment along an edge of $Q$ counts by the length it shares with $Q$. Every coordinate
is a multiple of $1/1000$ and every mass of $10^{-8}$, so $\mu(Q)$ is rational whenever
$Q$ has a rational centre and $\tan(\theta/2)$ rational.

### 3.3 The reduction, hypothesis by hypothesis

Suppose 44 unit squares $S_1, \ldots, S_{44}$ with pairwise disjoint interiors lie in a
square of side $s < 7$, placed as $[0,s]^2$.

1. Scale by $7/s > 1$ about the origin.
   The images $S_i'$ lie in $[0,7]^2$, have side $7/s > 1$ and pairwise disjoint
   interiors.
2. Shrink each $S_i'$ about its own centre to a closed unit square $Q_i$. Since
   $7/s > 1$, $Q_i$ lies in the interior of $S_i'$, so the $Q_i$ are pairwise disjoint
   as closed sets and lie in $[0,7]^2$.
3. Each $Q_i$ is a closed unit square in $[0,7]^2$, so $\mu(Q_i) \ge 1$ by the cover
   property. The $Q_i$ are disjoint, so no point mass and no piece of segment length is
   counted twice: $\sum_i \mu(Q_i) = \mu(\bigcup_i Q_i) \le \mu([0,7]^2)$.
4. Then $44 \le \mu([0,7]^2) = 2199755099/50000000 < 44$, a contradiction.

Every hypothesis is met by the certificate: masses nonnegative (§4), all pieces inside
$[0,7]^2$ (§4), the total below 44 (§4), and the cover property over all closed unit
squares in $[0,7]^2$ (§5). The argument is the one the paper’s §2 gives, as its Lemmas 1
and 2, and the one the record’s earlier mixed covers rest on (T-066, T-184, T-191).

### 3.4 The pose space and the fold

A closed unit square in $[0,7]^2$ is fixed by its centre $c$ and its angle
$\theta \in [0, \pi/2)$; zmx2 writes $u = \tan(\theta/2)$. It is inside the container
exactly when $c$ is at least $w(\theta)/2$ from every wall, where
$w(\theta) = \cos\theta + \sin\theta$.

- **Unreduced** (`--full`): pass 0 covers centres in $[0,7]^2$ and $u \in [0, 1/2]$,
  which is $\theta$ up to $2\arctan(1/2) \approx 53.13°$; pass 1 runs the cover
  reflected by $y \mapsto 7 - y$, which carries a square at angle $\theta$ to one at
  $-\theta \equiv 90° - \theta$. Every $\theta \in [0, 90°)$ is in one pass, so no
  symmetry of the cover is used.
- **Reduced** (`--d4`): centres in $[0, 7/2]^2$ and $u \in [0, 1/2]$. The cover is
  invariant under the eight symmetries of the square (§4), and every pose has an image
  under one of them with centre in $[0,7/2]^2$ and $\theta \in [0, 45°]$, at which $\mu$
  is the same. The region is a superset of what the fold needs.

Both sweeps decided every root of their region, so the claim rests on the unreduced one
alone and the reduced one is a second run over the fold.
The fold lemma itself is proved in Lean upstream and not built here, as for T-066; the
`--full` sweep does not use it.

## 4. The Cover, Checked Here

This review’s `s44_review.py cover` read the file with its own parser
(`review/outputs/cover-n44.json`):

| Fact | Value |
| --- | --- |
| Side, denominators | $7$; coordinates $X/1000$; masses $w/10^8$ |
| Pieces | 15,525 points at 15,525 distinct positions; 3,912 segments, each of length $1/50$; no polygon; no trailing token |
| Lines carrying segments | $x = 1, \ldots, 6$ and $y = 1, \ldots, 6$; none on a wall |
| Total | $2199755099/50000000 = 43.9951019800$; points $117146551/10000000$, segments $201752793/6250000$ |
| Slack below 44 | $244901/50000000 \approx 0.0049$, 0.011% of 44 |
| Nonnegativity | every weight positive |
| $D_4$ invariance | as a measure under all eight symmetries: points by position, each line’s density as a canonical step function |
| Points on loaded lines | none |
| SHA-256 | `c9fde0f1…cae0`, the issue’s |

`devtools.audit_evand_mixed_covers cover --case 44`, the record’s own reader, agrees on
every row it reports, and `zmx2 d4` reports the measure invariant in exact arithmetic
(receipt header).

Against Daniel’s $s(45) = 7$ cover, which the source names as its warm start
(`review/outputs/compare-s45.json`): the same denominators and 3,912 segments, 13,085 of
the 15,525 point positions shared, and 19,989 points there.
The credit the source gives Daniel for the starting cover is borne out.

## 5. `zmx2`: What It Decided, Here and at the Source

### 5.1 The replay

`devtools.replay_evand_zmx2` built `zmx2.rs` `e2bb84e9` from the retained bytes,
refusing any input whose SHA-256 differs from the record’s, with rustc 1.97.0 (binary
`d68a2e35…`), and ran the source’s two commands on two threads of a shared four-core
container:

| Mode | Roots | Boxes | Certified leaves | Empty leaves | Uncertified | Max depth | Wall, CPU |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `--d4` | 4,900 | 16,792,446 | 8,321,795 | 76,878 | 0 | 39 | 131 s, 222 CPU-s |
| `--full` | 39,200 | 134,880,184 | 66,848,724 | 610,968 | 0 | 39 | a run stopped by a container restart after 29,812 roots, and its resume: 311 s and 430 CPU-s for the last 9,388; 2,601 CPU-s by `zmx2`’s own count |

`VERIFIED-D4` and `VERIFIED`. `devtools.audit_evand_mixed_covers check` reads each root
log as one record of its region, every root once with no uncertified and no capped box,
under headers that name this cover by the FNV-1a 64 hash `zmx2` computes
(`bd68795e5855deda`) at the default depth 40, node cap $2 \times 10^7$, $\kappa = 1.5$
and $K = 30$, and finds every root’s census equal to the source’s
`verification/logs/zmx2_d4.log` and `zmx2_full.log` (4,900 and 39,200 roots, headers
identical).

### 5.2 What it trusts

`zmx2` decides, for each closed pose box, a lower bound on $\mu(Q)$ over every
admissible pose in it: points certainly inside $Q$ by an exact integer test (Lemma P),
plus a lower bound on each grid line’s captured segment mass alone or paired with the
line at distance 1 (Lemmas C, Z, W, DP and T of `search/ZMX2.md`). A box is certified
when the bound reaches 1, and halved otherwise, to depth 40. The chord-end geometry is
enclosed in binary64 interval arithmetic widened one ulp outward and rounded outward to
a grid of pitch $1/(D\,2^K)$; everything after is integer arithmetic (Lemma R). It
trusts those lemmas as `ZMX2.md` proves them, its code as written, and correctly rounded
IEEE-754 binary64 without contraction, as Rust gives on x86-64. None of it is formally
verified. The reviews of [28 September](review-2026-09-28-evand-s21-s45-mixed-covers.md)
and [2 October](review-2026-10-02-wand125-s59-s77-mixed-covers.md) derived the lemmas
for `6b7f0f79`; §6 says why they carry to `e2bb84e9` for this cover.

### 5.3 Depth

Both sweeps reach depth 39 against `zmx2`’s limit of 40, at the source and here.
A box at the limit that is not certified is reported uncertified, never certified, so
this bears on how close the cover is to what `zmx2` can decide, not on soundness (F3).

## 6. The Checker Version

### 6.1 `e2bb84e9` against `6b7f0f79`

`zmx2.rs` grew from 2,069 lines at `6b7f0f79` to 4,342 at `e2bb84e9`. This review’s
`zmx2_fn_diff.py` lists every top-level function in both: 34 are the same, 13 changed
besides the module prelude, and 32 are new (`review/outputs/zmx2-fn-diff.txt`). Each
change was read (`--show`), and for this cover each reduces to the earlier code:

| Changed | For this cover |
| --- | --- |
| `parse_cover`, `build_cover`, `reflect_y`, `check_d4`, `g_range` | They add axis-parallel rectangles (`rects`), empty here (`npg = 0`); the grid-line set is now $\{k, s - k\}$ for $1 \le k \le s - 1$, which at the integer side 7 is $\{1, \ldots, 6\}$ as before; the atom assignment moved into `build_lines`, whose default branch (`hfirst = false`) is the old rank rule line for line; `alt` stays `None` without `--sym-atoms` |
| `eval_node` | Calls `mass_bound`, which with no rectangles and no `--first-order` returns `segment_bound` |
| `segment_bound`, `family_bound` | `segment_bound` is now `frames` (the old two frames, verbatim) plus `family_bound_ex` with an empty skip list, which is the old `family_bound` with one test that an empty list makes vacuous; without `--sym-atoms` no mirrored bound is taken |
| `cmd_cert` | A side that is not a multiple of $1/10$ is now accepted with a superset of roots; 7 is a multiple of $1/5$, so the cells, the region and the header are the old ones; `--umin` is unset |
| `float_mass`, `box_empty`, `run_root`, `main`, the prelude | Diagnostics, comments and the new flags’ parsing; no decision path changes |

The new functions (`area_bound`, `first_order_bound`, `cmd_cert0` and the rest) are
reached only through rectangles, `--first-order`, `--sym-atoms`, `--mirror-only` or the
`cert0` and `boxes0` commands, none of which this run used: the header’s `atoms=grid`
and the absence of `area=` and `umin=` say so, and the source’s logs carry the same
header.

The reading has an empirical check.
`zmx2.rs` `6b7f0f79`, built from the 28 September packet’s bytes (binary `cba78a9e…`,
the build of the $s(76)$ and $s(95)$ replays), accepts this cover, since its side is a
multiple of $1/5$ and it has no polygons.
Run over the $D_4$ region by `review/programs/run_zmx2_6b7f0f79.sh`, it certified all
4,900 roots, 16,792,446 boxes, none uncertified, maximum depth 39, and
`audit_evand_mixed_covers compare-zmx2` finds every root’s census and the header
identical to the `e2bb84e9` replay’s (`review/outputs/zmx2/`). The two versions decide
this region box for box.

### 6.2 The trust boundary, then

For this cover the decision rests on the same lemmas and the same bounding code as the
covers the record confirmed with `6b7f0f79` (T-052, T-053, T-062, T-066). Nothing the
new version adds is on the path.

### 6.3 `zm_mixed.py`, the source’s second checker

`zm_mixed.py` is Daniel’s other checker, sharing his authorship and architecture with
`zmx2` but written separately, in exact rationals.
It was not run here.
Its records were read with this review’s own code (`s44_review.py zm-records`,
`review/outputs/zm-records-n44.json`):

- 62 record files, every header naming `zm_mixed.py` `1fd20346`, `mixed_cover.py`
  `bb89de15`, `zeromargin.py` `3cb95fb7` and this cover’s SHA-256, at one setting apart
  from depth and region: D4 mode, pitch $1/10$, 8 bins in $u$ over $[0, 1/2]$,
  `--disj --chain-from 0`, and `cert_mode` false.
- At depth 24, all 9,800 roots of $[0,7/2]^2 \times [0,1/2]$ at that pitch once each,
  2,110,180 boxes, 1,265 uncertified in 27 roots, 403,192 CPU-s.
- For each of those 27 roots, a depth-30 run of the whole root with none uncertified,
  deepest leaf 29, 92,353 CPU-s.

So the records state a complete `zm_mixed.py` decision of the $D_4$ region, about 138
CPU-hours in all, as the issue says.
Two settings differ from the runs this record accepted for $s(76)$ and $s(95)$ (F4).
Without `--cert-mode`, Corollary T′ and the polygon code are reachable; T′ applies only
to points lying on a line that carries segments, of which this cover has none (§4), and
the cover has no polygons, so neither can have fired.
`zeromargin.py` `3cb95fb7` is not the `640fe453` that `zm_mixed.py` pins, and no review
here has read it. These records are the producer’s; read, they decide nothing in the
record, and a run here would add a second machine method beside the rung, not a rung
(`think-qvp6`).

## 7. Exact Poses

`s44_review.py poses` evaluates $\mu(Q)$ exactly, in `fractions.Fraction`, at rational
admissible poses: a point is inside the closed square when both rotated coordinates are
at most $1/2$ in absolute value, and a segment contributes its density times the length
of its line’s intersection with the square, both exact
(`review/outputs/poses-n44.json`).

| Family | Poses | Least exact $\mu$ |
| --- | --- | --- |
| Uniform in the $D_4$ region ($u \le \tan(\pi/8)$) | 1,500 | 1.004888 |
| Near the grid tiles: tilts $0$ to $5 \times 10^{-3}$, offsets up to $3 \times 10^{-3}$ | 448 | 1.003837 |
| Flush against the wall $x = 0$ at tilts of 0.01° to 3°, along the wall | 532 | 1.003897 |
| Near 45° | 400 | 1.007839 |
| Float descents from the 25 lowest, ends evaluated exactly | 25 | 1.003837 |

None of the 2,905 exact values is below 1. The least, $1.003837205$, is a square at
centre $(1/2 + 8 \times 10^{-9}, 3/2)$ tilted by $10^{-6}$ degrees: the wall tile
centred at $(1/2, 3/2)$, the $D_4$ image of the tile at $(3/2, 1/2)$ where the paper
says its search stalled.
As a check on this evaluator, `s44_review.py source-minima` evaluates the source’s six
printed float minima exactly (`review/outputs/source-minima-n44.json`): the three that
are admissible as printed give $1.003088543$, $1.003354014$ and $1.003921031$, the
source’s values to every digit it prints; the other three round to just outside the
container.

The source’s own floating-point search reports a least mass of 1.0031 over 675,000 poses
(`verification/logs/stress.out`) and 1.0034 along the wall valleys
(`tilesep_on_certificate.out`); the exact values here are consistent with both.
A sample decides nothing about the poses it does not reach; it could have found a
violation, and did not.

## 8. Mutated Covers

Two mutations remove one $D_4$ orbit each, keeping the cover invariant: the eight points
at the images of $(1.812, 2.430)$, carrying $0.00998176$ each, and the eight segments at
the images of $(0.98, 1)$–$(1, 1)$, carrying $0.09198265$ each.

| Mutation | Mass removed | Mutant SHA-256 | `zmx2 --d4` on its cell | A pose where the mutant is short | $\mu$ there, mutant / published |
| --- | --- | --- | --- | --- | --- |
| `drop-heaviest-point` | $31193/390625 = 0.0798541$ | `85678ee6…` | $x$ 23, $y$ 17: NOT VERIFIED, 435 uncertified | centre $(2.494, 1.693)$, $\theta = 33.69°$, root $x$ 24, $y$ 16, bin 2 | 0.993201 / 1.003182 |
| `drop-heaviest-segment` | $1839653/2500000 = 0.7358612$ | `eca3c3f3…` | $x$ 8, $y$ 9: NOT VERIFIED, 235 uncertified | centre $(0.50401, 0.50401)$, $\theta = 0.46°$, root $x$ 5, $y$ 5, bin 0 | 0.819939 / 1.003904 |

This review’s `mutants` removes each orbit with its own code; its mutants’ SHA-256 equal
the digests in the retained control receipts, so the two describe the same covers.
Each mutant was swept over the roots around its removed orbit to choose the retained
cell (the point mutant over $x$ 11–25, $y$ 17–31, 32,355 uncertified boxes; the segment
mutant over $x, y$ 0–19, 48,952). Both roots that hold the poses above are refused as
well: the segment mutant’s in that sweep (233 uncertified), the point mutant’s in a run
of its own (cell $x$ 24, $y$ 16: 661 uncertified, 228 of them in bin 2).

Each refusal is true: at a pose in the refused root the mutant captures less than 1,
exactly, so `zmx2` refused a cover that is not a cover.
`tests/test_replay_controls.py` holds both receipts.

## 9. Findings

### F1. `zmx2` is interval-certified, not exact-rational (note, in the source)

The issue calls `zmx2` an “exact checker … i128/rational”, the README’s table says
“exact rational subdivision”, and the paper’s §4 says both checkers certify each box “in
exact rational arithmetic”.
Its mass comparisons are exact integers, but the chord-end geometry is enclosed in
binary64 with outward rounding (`zmx2.rs`, the module comment, and `ZMX2.md` Lemma R).
The record rates the replay interval-certified, and the trust boundary includes the
host’s IEEE-754 arithmetic.
`zm_mixed.py` is the exact-rational one.

### F2. `zmx2.rs` `e2bb84e9` had not run here (note, for the record)

The registry listed the version as retained and not run.
For this cover its decision path is `6b7f0f79`’s, function for function (§6.1), and the
reviewed `6b7f0f79` decides every $D_4$ root of this cover with the same census.
A cover with rectangles, a side not a multiple of $1/5$, or any of the new flags would
need its own read of the new code.

### F3. Both sweeps reach depth 39 of 40 (note, for the record)

The deepest boxes sit one level above `zmx2`’s depth limit.
That is no soundness question, since a box at the limit is reported uncertified, but it
says the certificate is near what `zmx2` decides at its defaults, consistent with the
0.011% slack in mass and with the source’s account of the valleys that blocked earlier
rounds.

### F4. `zm_mixed.py` ran without `--cert-mode`, with a `zeromargin.py` it does not pin (note, in the source)

The source’s `zm_mixed.py` runs record `cert_mode: false` and print
`zeromargin.py … DIFFERS FROM PINNED`. For this cover the extra code certificate mode
disables is unreachable (§6.3), so the first is immaterial.
The second means the route ran a `zeromargin.py`, `3cb95fb7`, that `zm_mixed.py` was not
pinned against and that no review here has read.
Neither affects the claim, which `zmx2` decides; both would matter to a record that
rested on the `zm_mixed.py` route.

### F5. The README’s “0.4 % slack” is the linear program’s gap (note, in the source)

The README’s “With only ≈ 0.4 % slack (LP 43.82 vs.
44)” describes the search; the certificate’s own slack is $244901/50000000$, 0.011% of
44, which the paper’s Remarks state beside it.
A reader comparing covers by margin should use the second.

### F6. The reduction’s Lean proofs were not read (note, for the record)

The README cites `packing_le_measure` and `not_packs_of_measure` in Daniel’s
`lean/Sqpack/MixedMeasure.lean`. They were not read or built here; §3.3 re-derives the
reduction by hand, and that is what the record rests on.

## 10. Significance

S3, the registering lane’s draft, is confirmed: an exact value for a case that was open,
by Daniel’s method at a new count, as T-066 settled $s(59) = 8$ and T-184 and T-191
report $s(76) = 9$ and $s(95) = 10$. It is the case $k = 7$ of $s(k^2 - 5) = k$; each
instance is a separate linear-programming solve, so it is not a family.
The separation step for near-axis wall valleys is a search method, not part of the
proof.

## 11. Questions for the Authors

None holds anything open.

1. Were the `zm_mixed.py` runs without `--cert-mode` deliberate (F4)? A rerun of the 27
   deepest roots in certificate mode would align the route with the record’s other
   `zm_mixed.py` evidence.
2. Is `zeromargin.py` `3cb95fb7` the file at evand/square-packing `659ee62`, as the
   records’ headers say, and did you run any check of it against `640fe453`?

## 12. The Programs

Kept in the packet’s
[`review/`](../../../packing/resources/web/moh63-dev-s44-equals-7-2026-10-29/review/README.md)
with everything they printed.
They decide nothing on their own.

| Program | Does |
| --- | --- |
| `s44_review.py cover` | §4: parse, total, slack, $D_4$ invariance as a measure |
| `s44_review.py compare-s45` | §4: comparison with Daniel’s $s(45)$ cover |
| `s44_review.py zm-records` | §6.3: the source’s `zm_mixed.py` records |
| `s44_review.py poses` | §7: exact $\mu$ at sampled poses, with float descents |
| `s44_review.py mutants` | §8: this review’s own orbit removal, and an exact pose where each mutant captures less than 1 |
| `s44_review.py source-minima` | §7: exact $\mu$ at the source’s printed float minima |
| `run_zmx2_6b7f0f79.sh` | §6.1: the reviewed `zmx2` version over the $D_4$ region, for comparison with the replay |
| `zmx2_fn_diff.py` | §6.1: the two `zmx2.rs` versions function by function |

## 13. For the Records Lane

- The replay and its controls support `C3`, reproduced with the producer’s code; the
  review supports moving the verified lower lane of $n = 44$ to 7 and the case to
  proved.
- `V4` and `C4` need a second adversarial review by a distinct reviewer and a human
  oversight record; this review’s shared context with the records lane is a reason to
  make the second one separately prompted.
- `zm_mixed.py`’s complete pass raises no rung (`think-qvp6`).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
