# Proof Review: Benjamin Greff’s `s(76) = 9` and `s(95) = 10` by Mixed Covers

**Date:** 2026-10-16. **Lane:** the review lane of the W2 phase that is stage 4 of the
[result import runbook](../../../packing/campaign/result-import.md#stage-4-validate),
for issues [594](https://github.com/jlevy/squares/issues/594) and
[610](https://github.com/jlevy/squares/issues/610), bead `think-l8wi` (epic
`think-hg5s`). **Reviewer:** Claude, strong sub-agent tier, max reasoning, separately
prompted, with no shared context with the records lane that registers cases 76 and 95 in
the replay tools (`think-ccjt`); nothing of that lane’s work was read.
It covers `T-184` ($s(76) = 9$) and `T-191` ($s(95) = 10$), both registered at V0/C0. It
is an adversarial soundness review: it re-derives the argument from each cover to its
claim, reads the two checkers’ composite over the $D_4$ region and the wall segments,
and checks the retained records with programs written for it.
The verdicts of the two checkers are the source’s, reproduced at retention from the
bytes the source pins; what was computed here is said to be.

## Summary

This summary is written for the author, Benjamin Greff.

**Both values stand.** For each count, the cover is a nonnegative measure of points and
of mass spread uniformly along axis-parallel segments, with total
$3788361049/50000000 = 75.767\ldots < 76$ on $[0,9]^2$ and
$3791753447/40000000 = 94.794\ldots < 95$ on $[0,10]^2$. If every closed unit square
inside the container captures mass at least 1, then $n$ unit squares cannot fit in a
smaller square, and the $k \times k$ grid gives the matching upper bound.
That reduction is correct as stated, with every hypothesis met (§3). The covering
statement is decided on the $D_4$ fundamental region by two of Evan Daniel’s checkers
that never decide the same cell: `zmx2` on 8,096 of 8,100 root cells for $s(76)$ and
9,981 of 10,000 for $s(95)$, and `zm_mixed.py` on the 64 and 304 cells of side
$1/20 \times 1/20 \times 1/32$ that tile the rest.
Read from the retained records with exact fractions, every cell of each region carries a
certified decision of exactly one checker, under the pinned checker digests, the cover’s
digest and the certificate-mode settings; no root was capped, and no `zm_mixed.py` cell
came near its depth limit (§7.2, §8.2). I found no mathematical defect in either claim,
and no finding is blocking (§10).

**What was checked here, with programs written for this review.** Both covers were
re-parsed independently and their data facts recomputed exactly, including $D_4$
invariance as a measure under all eight symmetries.
The composite was audited cell by cell from the source’s records and from the
retention’s replay. Exact $\mu(Q)$ was evaluated at 26,645 sampled poses, among them
every `zmx2`-failing root, the corners of every uncertified box it lists, the tile
germs, the two coincidence angles, and 3,000 random poses checked before and after the
$D_4$ fold; none captured less than 1. The lowest values found were $1.000418$ for
$s(76)$, at a germ on the bottom wall, and $1.003389$ for $s(95)$. Eight mutated covers
were also built. Each captures less than 1 at an exhibited pose, exactly.
`zmx2` refuses six of them at that pose’s root and certifies the published cover there.
`zm_mixed.py` refuses a seventh on the one cell that holds its hole, at a depth limit of
12, where it certifies the published cover’s cell at the same limit.
At the source’s depth limit of 24, neither that mutant nor an eighth, more local one
finished within its time limit (§7.4, §8.4, [§12](#12-the-programs)).

**The wall segments contribute nothing.** The packing argument only uses squares inside
the open container, which meet no wall.
`zmx2` makes every decision identically without them, and no `zm_mixed.py` cell has a
wall line within reach (§3.6).

**The findings** are about the author’s coverage script and small things in the files
(§10). `tools/check_coverage.py` accepts five mutated record sets that leave part of the
region undecided or unbound to the pinned checkers: a misaligned cell, foreign settings,
a foreign checker digest, a headerless record, and a `zmx2` log of another cover (F1,
minor). The records you published pass the stricter check this review ran, so the claims
are unaffected. A few questions are in §11.

## 1. What Was Reviewed

| Field | Value |
| --- | --- |
| Sources | `bengreff/s76-certificate` at `1cb924fa2fb7e8e30d8ddeb9b5e0dfcfae4f9f1f` and `bengreff/s95-certificate` at `dd7297d06adc664268c65005369b895e4ded7547`, retained whole in [`bengreff-s76-certificate-2026-10-14`](../../../packing/resources/web/bengreff-s76-certificate-2026-10-14/README.md) and [`bengreff-s95-certificate-2026-10-15`](../../../packing/resources/web/bengreff-s95-certificate-2026-10-15/README.md) |
| Claims | $s(76) = 9$ (`T-184`, issue 594); $s(95) = 10$ (`T-191`, issue 610) |
| $s(76)$ cover | `cover/s76_cover_v5.txt.gz`, unpacked 996,130 bytes, SHA-256 `b6a1214b99f00e5dd136d74c8d87bccd178df38a1063b2c7be90517eb2b862b2`, FNV-1a 64 `96e61ce6a0aa2545` |
| $s(95)$ cover | `cover/s95_cover_v2.txt.gz`, unpacked 1,160,654 bytes, SHA-256 `8b2d2152867585c82920bc90c6c3ec2a2458ef2ba57311ccd7dd436d1344cb7c`, FNV-1a 64 `e6e0d4182d7f6e43` |
| Checkers, pinned by both `verify.sh` at `evand/square-packing` `b91d70b6` | `s12/verify2/src/bin/zmx2.rs` `6b7f0f79…3fed`, `s12/search/zm_mixed.py` `ee3e2915…60ac` and `mixed_cover.py` `bb89de15…aae5`, retained in the [September 28 evand packet](../../../packing/resources/web/evand-square-packing-2026-09-28/README.md); `s12/search/zeromargin.py` `640fe453…86ab`, with the crate files, in the [September 26 packet](../../../packing/resources/web/evand-square-packing-2026-09-26/README.md) |
| Records read | per source: `records/zmx2/` (root log, summary, `failing_roots.txt`), every `records/zm_mixed/j*.jsonl` with `jobs.txt`, `records/toolchain.txt`; per packet: the retention’s `zmx2` root log, its `zm_mixed.py` records, the wall control’s root log, the control pose receipts |
| Source files read | both `README.md`, `verify.sh`, `tools/check_total.py`, `tools/check_coverage.py`; `lean/S76Lower.lean`, `lean/S95Lower.lean`, `mk_s76_lean.py`, `mk_lean.py`, both `build_summary.txt`; the first lines of both covers; issues 594 and 610 with their comments, as data |
| Checker code read | `zmx2.rs`: the parser and its input bounds, `build_cover`, `check_d4`, `line_ends` with Lemma W, `line_atoms`, `family_bound`, `box_geo`, `box_empty`, `segment_bound`, `pt_certain_in`, `eval_node`, `split`, `run_root`, `cmd_cert`; `zm_mixed.py`: the module docstring, `Cover` with its $D_4$ test, `LineMass`, `line_pieces`, the reach window of `piece_bound`, `run_box`, `exact_mass`, `run_sweep`, `run_header`, `main` with the partial-region filter; `zeromargin.py`: `trig`, `bin_data`, `clip_bin`, `roots`, `d4_roots`; `mixed_cover.py`: `load`, `validate`, `total` |
| Write-ups read | `search/ZMX2.md` (all), `ZMX2_AUDIT.md` §0, `ZM_MIXED.md` §1, §5, §8, `ZM_MIXED_AUDIT.md` verdict; in Daniel’s Lean library as retained at `f58a017` (the [October 7 evand packet](../../../packing/resources/web/evand-exact-and-local-reports-2026-10-07/README.md)): `Sqpack/CovM.lean` (`CovM`, `le_minSide_mixed`), the statements of `not_packs_of_measure` and `d4_reduction_measure_u` in `MixedMeasure.lean`, `Packs` and `minSide` in `Spec.lean`, `sq` in `Basic.lean` |
| Earlier reviews relied on | [the $s(21)$ and $s(45)$ review](review-2026-09-28-evand-s21-s45-mixed-covers.md), which re-derived every lemma of both checkers against their code at these exact digests (its §2 and §3.4 were read before this review’s findings were written, the rest not); the model for this one, [the $s(59)$ and $s(77)$ review](review-2026-10-02-wand125-s59-s77-mixed-covers.md), whose reading is disclosed in §14 |
| Programs written for this review | `k2m5_review.py` and `corner_scan.py`, standard library only, kept with their outputs under [`bengreff-s76-certificate-2026-10-14/review/`](../../../packing/resources/web/bengreff-s76-certificate-2026-10-14/review/README.md) (§12) |

## 2. Verdict

**(a) $s(76) = 9$, `T-184`: no mathematical defect found.** The cover is well formed and
totals exactly $3788361049/50000000 < 76$, and it is $D_4$-invariant as a measure.
The reduction from the covering statement to the bound is correct, with every hypothesis
met (§3). The covering statement on the $D_4$ region is the conjunction of `zmx2`’s
certificates on 8,096 roots and `zm_mixed.py`’s on 64 cells.
Read from the retained records, those cells tile the region exactly, and each record is
bound to this cover, the pinned checkers and the certificate-mode settings (§7.2). Both
checkers are the versions reviewed at these digests on 28 September.
The shapes these covers bring that the earlier ones did not are handled inside the
bounds both checkers enforce (§4.3, §5.3).

**(b) $s(95) = 10$, `T-191`: no mathematical defect found.** The same holds, with 9,981
`zmx2` roots and 304 `zm_mixed.py` cells.
One root holds 8,192 of the 8,263 boxes `zmx2` leaves uncertified.
Its 16 cells are certified by `zm_mixed.py` with 964 boxes at depth at most 11, and the
lowest $\mu$ found there exactly is $1.0077$ (§8.2).

**For both:** the upper half is the $k \times k$ grid, exactly the claimed side (§3.7).
The confirmation the retained replay gives is a reproduction with the producer’s code.
The two checkers share no code but are not a second route: no cell rests on both (§6).
Nothing found here blocks raising either entry when its replay is recorded as evidence
(§13).

## 3. From Certificate to Claim

### 3.1 The statement

$s(n)$ is the least side of a closed square holding $n$ closed unit squares with
pairwise disjoint interiors, each at any position and angle.
The claims are $s(76) = 9$ and $s(95) = 10$; the new content is the lower halves
$s(76) \ge 9$ and $s(95) \ge 10$. Both counts are $k^2 - 5$, with $k = 9$ and $10$.

### 3.2 The measure and the closed conventions

A cover in Daniel’s `mixed 1` format defines a measure on $[0,k]^2$:
$$\mu = \sum_p w_p\,\delta_p + \sum_\sigma \frac{w_\sigma}{|\sigma|}\,\lambda_\sigma ,$$
with point masses $w_p$ at points $p$, and mass $w_\sigma$ spread uniformly by length
along each closed axis-parallel segment $\sigma$. Coordinates are integers over
$D = 8000$ and masses integers over $W = 4 \cdot 10^8$ in both files.
For a closed unit square $Q$, $\mu(Q)$ counts every point of $Q$, its boundary included,
and the length fraction of each segment inside $Q$, so a segment along an edge of $Q$
counts in full. Both checkers implement exactly this: `zmx2`’s point test and chord ends
are non-strict (Lemma P, §3 of `ZMX2.md`), `zm_mixed.py` clips parameter intervals by
closed half-planes, and the exact evaluator written here (§12) and `zm_mixed.py pose`
agree to the last digit on every pose where both were run.

### 3.3 The reduction, hypothesis by hypothesis

**Lemma.** Let $\mu$ be a finite nonnegative Borel measure on $[0,k]^2$ with
$\mu([0,k]^2) < n$, and with $\mu(Q) \ge 1$ for every closed unit square
$Q \subset (0,k)^2$. Then $s(n) \ge k$.

*Proof.* Suppose $n$ unit squares pack into $[0,L]^2$ with $L < k$. Scaling the packing
by $\lambda = k/L > 1$ about the origin gives closed squares $S_i \subset [0,k]^2$ of
side $\lambda$ with pairwise disjoint interiors.
Let $Q_i$ be the closed unit square with the centre and angle of $S_i$. Every point of
$Q_i$ is within $1/2 < \lambda/2$ of the centre in $S_i$’s own frame, so
$Q_i \subset \operatorname{int} S_i \subset (0,k)^2$, and the $Q_i$ are pairwise
disjoint. Then $n \le \sum_i \mu(Q_i) = \mu(\bigcup_i Q_i) \le \mu([0,k]^2) < n$. ∎

The hypotheses, against the files:

| Hypothesis | Where it is met |
| --- | --- |
| $\mu \ge 0$, finite | every weight is a nonnegative integer, and every point and segment lies in $[0,k]^2$: checked by both checkers’ parsers, by `tools/check_total.py`, and by this review’s parser |
| $\mu([0,k]^2) < n$ | the exact totals above; slack $11638951/50000000 = 0.2328$ and $8246553/40000000 = 0.2062$ |
| $\mu(Q) \ge 1$ for closed unit $Q$ in the open container | implied by the stronger covering statement that the composite certifies: every closed unit $Q \subseteq [0,k]^2$ (§3.4, §3.5) |
| additivity on the disjoint closed $Q_i$ | $\mu$ is a finite sum of point masses and length measures on segments, a Borel measure |

The covering statement is used only through squares in the open container.
That is why the wall segments are irrelevant (§3.6). The same reduction is proved in
Lean in Daniel’s library: `not_packs_of_measure`, read at the retained revision
`f58a017`, states it for every closed unit square inside the box.
Its use for these covers is in the wrapper, which this repository has not built (§3.8).

### 3.4 The pose space and the fold

A pose is a centre $c$ and an angle $\theta$. Since
$Q(c, \theta + 90^\circ) = Q(c,\theta)$, $\theta \in [0^\circ, 90^\circ)$ is all of
them. Both checkers write $u = \tan(\theta/2)$, so that $\cos\theta = (1-u^2)/(1+u^2)$
and $\sin\theta = 2u/(1+u^2)$ are rational in $u$. A pose is admissible
($Q \subseteq [0,k]^2$) iff $w/2 \le c_x, c_y \le k - w/2$ with
$w = \cos\theta + \sin\theta$.

**The fold.** The reflections $x \mapsto k-x$ and $y \mapsto k-y$ of the container map
$Q(c,\theta)$ to $Q(gc, -\theta) = Q(gc, 90^\circ - \theta)$, and so does
$x \leftrightarrow y$. Apply $x \mapsto k-x$ if $c_x > k/2$, $y \mapsto k-y$ if
$c_y > k/2$, then $x \leftrightarrow y$ if the angle exceeds $45^\circ$. Any pose maps
to one with $c \in [0, k/2]^2$ and $\theta \in [0^\circ, 45^\circ]$, so
$u \le \tan 22.5^\circ = \sqrt2 - 1 < 1/2$. The map preserves the container, so
admissibility is preserved.
If $\mu$ is invariant under the group, it preserves $\mu(Q)$. So the covering statement
on the region $$R_k = [0, k/2]^2 \times \{u \in [0, 1/2]\}$$ implies it everywhere.
In $u$, a reflection is $u \mapsto (1-u)/(1+u)$. The program here applies the fold
exactly to 1,500 random admissible poses of each whole container.
In every case the image lies in $R_k$ and is admissible, and $\mu$ is equal at the pose
and at its image, exactly (§7.3).

**The invariance.** `zmx2 d4` checks invariance under the generators $x \mapsto k-x$ and
$x \leftrightarrow y$, as a measure: point weights aggregated by position, and line
densities in canonical form.
`zm_mixed.py --d4` checks a stricter condition, equality of raw multisets.
This review’s parser checks the measure, in canonical form, under all eight elements.
All three pass for both covers.

### 3.5 The composite over the $D_4$ region

Each checker, run on a closed pose box, decides one statement: every admissible pose of
the box has $\mu(Q) \ge 1$. `zmx2` decides it when every leaf of its subdivision is
certified or empty (`run_root`). `zm_mixed.py` decides it when every leaf is certified
or empty (`run_box`). Halves are closed and cover their parent, so the leaves cover the
box. Neither checker uses the symmetry inside a box: `run_root` and `MixedChecker` take
no symmetry argument.
In both, the `--d4` flag only chooses the root list and runs the invariance test first.
So the composite needs nothing from the checkers beyond their per-box statements:
$$\text{covering on } R_k \iff \bigwedge_{\text{zmx2 roots } B}\ \mathrm{Cov}(B)\ \wedge \bigwedge_{\text{zm\_mixed cells } C}\ \mathrm{Cov}(C),$$
provided the boxes cover $R_k$ and every statement is about this cover.
Both provisos are facts about the records, checked exactly in §7.2 and §8.2. The `zmx2`
log header carries the FNV-1a hash of the cover’s bytes, which is the cover’s. Every
`zm_mixed.py` header names the cover’s SHA-256, and its region is its record’s root.

The statement each checker decides on a box, term by term:

| Term of the covering statement | `zmx2` (`run_root`) | `zm_mixed.py` (`run_box`) |
| --- | --- | --- |
| centre in the closed box, $u$ in the closed bin | `PBox` with centre denominators $10 \cdot 2^j$ and $u$ denominators $8 \cdot 2^l$; closed halves | `Fraction` boxes; closed halves at the midpoint |
| $Q \subseteq [0,k]^2$ | Lemma E drops boxes with no admissible pose; Lemma W uses admissibility at lines one unit from a wall | `EMPTY` and `clip_bin` drop inadmissible poses; the wall bounds of Lemma B |
| a point counts iff in the closed $Q$ | the four violation polynomials $\le 0$ (Lemma P) | containment inequalities $\le 1/2$ (Lemma A/B/C, `in_rot_square`) |
| a segment counts by its length fraction in the closed $Q$ | closed certain chords $[lo^*, hi^*]$ (Lemmas C, M, S, Z, H) | parameter intervals clipped by closed half-planes (Lemmas S, T, L) |
| total at least 1 | $L(B) \ge W \cdot \mathrm{Lc} \cdot 2^{30}$ in integer units | an exact bound $\ge 1$ |
| this cover | its own parser; the log header’s FNV-1a of the bytes | `mixed_cover.load`; the header’s SHA-256 of the input |

`zm_mixed.py`’s partial-region options (`--cx-lo` to `--u-hi`) keep a root iff it meets
the open region (`main`, `keep`). The region of every job is one aligned cell of the
$1/20 \times 1/20 \times 1/32$ grid that `zeromargin.d4_roots` generates over $R_k$
($90 \times 90 \times 16$ and $100 \times 100 \times 16$ cells), so exactly that cell is
kept. In every record, the root equals the header’s region.

### 3.6 The wall segments

The $s(76)$ cover has 16 segments on the container’s walls, 4 per wall, each of length
$1/500$ and one unit $1/(4\cdot10^8)$ of mass.
On $x = 0$ they are centred at $y = 3, 4, 5, 6$, and they total $4 \cdot 10^{-8}$. The
$s(95)$ cover has 404: 101 per wall, centred on the $1/20$-lattice points from $5/2$ to
$15/2$, totalling $1.01 \cdot 10^{-6}$. These are the LP candidates the author describes
on issue 594 (comment of 2026-10-15T00:50:37Z), rounded up to one unit.

They contribute nothing to the proof:

- **The reduction never sees them.** The squares $Q_i$ of §3.3 lie in the open container
  and meet no wall. The cover without its wall segments satisfies every hypothesis there,
  with totals $3788361047/50000000$ and $18958767033/200000000$, both still below $n$.
- **`zmx2` does not use them.** The retention’s wall control (`receipts/controls/`, both
  packets) ran `zmx2 cert --d4` on each cover without them.
  Read here, every root has the published run’s census, root for root, and the same
  listed uncertified boxes.
  The search tree is decided by the bounds, so every leaf certified for the published
  cover was certified without the wall mass, and `zmx2` has in effect certified the
  wall-less cover on the same roots.
- **`zm_mixed.py` never reads them.** Every one of its cells has centres at least $11/5$
  (for $s(76)$) or $3/2$ (for $s(95)$) from the walls $x = 0$ and $y = 0$, and the
  region lies in $[0, k/2]^2$. `piece_bound` drops a line whose distance from the box
  exceeds $0.7072 + \tfrac12\operatorname{diag}$, and `clip_bin` changes nothing when
  $2\min(c_{x1}, k - c_{x0}, c_{y1}, k - c_{y0}) > \sqrt 2$. So no wall line enters any
  bound, and no cell’s angle bin is clipped.
  Every pose of every cell is admissible: the nearest wall is more than $w/2 \le 0.7072$
  away.
- **Flush squares do not need them.** At 1,600 sampled axis-parallel squares flush with
  a wall, the minimum of $\mu$ with and without wall segments is the same: $1.009510$
  for $s(76)$ and $1.010092$ for $s(95)$.

The retention’s argument, that a flush square is a limit of squares moved off the wall,
is also correct: $\mu$ restricted to closed sets is upper semicontinuous under Hausdorff
limits. The open-container observation makes it unnecessary.

### 3.7 The upper half and the exact value

The $9 \times 9$ grid packs 81 unit squares in $[0,9]^2$, and any 76 of them are a
packing, so $s(76) \le 9$. Likewise the $10 \times 10$ grid gives $s(95) \le 10$. Since
$\lceil\sqrt{76}\rceil = 9$ and $\lceil\sqrt{95}\rceil = 10$, the grid is the trivial
upper bound. With the lower halves, $s(76) = 9$ and $s(95) = 10$: both upper bounds are
exactly the claimed side.

### 3.8 The Lean wrappers

`lean/S76Lower.lean` and `lean/S95Lower.lean` prove `minSide 76 = 9` and
`minSide 95 = 10` from a hypothesis `S76Cover` or `S95Cover`, on Daniel’s `Sqpack` at
`1718a58`; the build summaries report three standard axioms.
Each hypothesis is `CovM D 4096 (kD) 2^32 W pts segs 0 h 0 h 0 2^31` with
$h/(4096 D) = k/2$: centres in $[0, k/2]^2$, $u \in [0, 2^{31}/2^{32}] = [0, 1/2]$. In
`CovM` as retained at `f58a017`, this is the statement of §3.5: every closed unit square
inside $[0, k]^2$ (`box (Mq/D)` with `Mq` $= kD$) with centre and $u$ in those closed
ranges has point mass plus segment mass at least $W$. `le_minSide_mixed` then needs the
data facts, which the wrappers kernel-check by `decide` (no repeated atom, $D_4$
invariance, total $< nW$), and $n \le k^2$.

The wrappers add a kernel-checked reduction and kernel-checked data facts.
They do not add the covering statement, and they were not built here.
The retention notes the build needed 25 GB for $s(95)$, more than this host has.
`Sqpack` at `1718a58` is not retained, so `CovM` there was not read (F7, Q2).

## 4. `zmx2`: Trust Boundary

### 4.1 What it decides and what it trusts

`zmx2` decides, for each closed root box, that a lower bound $L(B)$ on $\mu(Q)$ holds at
every admissible pose of every leaf box and is at least 1, or that the leaf is empty
(Lemma E). It trusts:

- **Its lemmas as implemented:** P, C, M, S, Z, W, H, T, E, DP and R of `ZMX2.md`. The
  review of 28 September re-derived them against `6b7f0f79`, and `ZMX2_AUDIT.md` audited
  them; I read the lemma statements and the code paths listed in §1 and found them as
  stated.
- **IEEE-754 binary64** with correct rounding of $+,-,\times,\div,\sqrt{\ }$ and no
  contraction. Chord ends are enclosed in outward-rounded intervals and then rounded
  outward onto the grid $1/(D \cdot 2^{30})$. Everything after that is exact `i128`.
- **`i128` without overflow:** release builds do not check it, so the parser bounds
  every input. The covers are inside those bounds (§4.3).
- **The compiler and the binary.** The author’s binary (`8b4dfd1e…`, rustc 1.99.0) and
  the retention’s (`cba78a9e…`, rustc 1.97.0) produced the same census at every root and
  the same uncertified boxes.
  The binary built here by `devtools.replay_evand_zmx2 build` is bit-identical to the
  retention’s.

Its float pre-filters (`pt_float_class`, the candidate buckets) only skip work.
Its `float-min` at an uncertified box is a diagnostic and certifies nothing (F6).

### 4.2 What the composite asks of it

It decides 8,096 roots of $R_9$ and 9,981 of $R_{10}$, outside the four and nineteen
roots it leaves.
Certified roots reached depth 36 and 38 at most, inside the limit of 40.
No root reached the node cap ($2 \cdot 10^7$) or the uncertified-box cap ($2\cdot10^5$,
which `verify.sh` sets).
The failing roots all reached depth 40, which is what makes them fail.

### 4.3 The shapes these covers bring

| Shape | Where it enters | Read here |
| --- | --- | --- |
| $D = 8000$, $k D = 72000$ and $80000$ | grid integers, chord rounding | inside the parser’s bounds ($D < 2^{20}$, $kD < 2^{27}$) |
| segment lengths $1/500$, $1/50$, $1/16$ | `Lc` = lcm of lengths in $1/D$ units $= 4000$ | below the $2^{24}$ limit; `zmx2 info` agrees |
| $W = 4\cdot10^8$, weights up to $6.6\cdot10^7$, totals $3.0$ and $3.8 \cdot 10^{10}$ units | `F` values, targets | inside $W, w < 2^{50}$ and total $< 2^{56}$, the bounds for which `ZMX2.md` §5 proves `F`$\cdot 2^{30}\cdot$`Lc` $< 2^{110}$ |
| 6,744 and 7,476 overlapping segment pairs on one line | `build_cover` | densities are summed into one piecewise-constant density per line, so overlap is additive |
| segments on the walls $x, y \in \{0, k\}$ | `vl`, `hl` gain lines at $0$ and $k$ | chords on a wall line use the generic Lemmas C, M, S and Z, which hold for every pose; Lemma W modifies only the lines at distance 1 from a wall. The wall control shows no decision depends on them (§3.6) |
| no point on any line | atoms | every point is an ordinary point (Lemma P); the atom code is unused |

## 5. `zm_mixed.py`: Trust Boundary

### 5.1 What it decides and what it trusts

`zm_mixed.py` decides, for a root box, that every leaf is closed by an exact bound.
The bound is either a piece bound $L \ge 1$ on segment mass (Lemmas S, T, L, L′, V, R of
`ZM_MIXED.md`), or one of `zeromargin.py`’s point primitives (ADM, P1, MIX, CHAIN) with
a phantom point of weight $L$. Otherwise the leaf is empty.
It trusts those lemmas as implemented at `ee3e2915` and `640fe453`, which the reviews of
27 September (`ZM_MIXED_AUDIT.md`) and 28 September re-derived against this code.
It also trusts Python’s `Fraction` and integers, which are exact.
Certificate mode removes Corollary T′ and the polygon code from the trusted surface;
neither cover has a polygon or a point on a segment line.
Its floats only choose what to try or drop.

### 5.2 What the composite asks of it

It decides 64 cells of $R_9$ and 304 of $R_{10}$, all inside failing `zmx2` roots and
all at least $11/5$ and $3/2$ from the nearest wall.
It ran in partial mode, one cell per job, under `--d4 --cert-mode --disj --chain-from 0
--pitch 1/20 --ubins 16 --depth 24`. The maximum depth used was 15 and 13, so no cell
was close to the limit of 24. This is the first time a result here rests on
`zm_mixed.py` in partial mode.
What that mode adds is the root filter `keep`, read in §3.5; the per-box computation is
the one the earlier reviews read.

### 5.3 The shapes these covers bring

Its exact arithmetic has no size limits to meet.
`LineMass` builds a line’s mass from separate prefix sums of start and end points, so
overlapping segments add.
The cells lie at the angles where the author reports exact coincidences that defeat it
at any depth: $u = 1/3$, the 3-4-5 angle, for both covers, and $\theta = \arctan(1/5)$
for $s(95)$. The construction removed the coincident points.
A coincidence makes certification harder, not easier, and the records show every cell
closed well before the limit.
The `clip_bin` zero-width case cannot arise here: the clip is inactive on every cell
(§3.6).

## 6. What the Two Checkers Share

| Element | `zmx2` | `zm_mixed.py` | Shared? |
| --- | --- | --- | --- |
| Code | Rust, one file | Python, with `zeromargin.py` and `mixed_cover.py` | no code; `ZMX2.md` states it was written without reading `zm_mixed.py` or its write-ups |
| Cover reader | own tokenizer and parser | `mixed_cover.load` and `validate` | the format, and the convention that `#` starts a comment |
| Pose space | $u = \tan(\theta/2)$, closed boxes, admissibility $w/2 \le c \le k - w/2$ | the same | yes, by design |
| Region and grid | roots of $1/10 \times 1/10 \times 1/8$ over $R_k$ | cells of $1/20 \times 1/20 \times 1/32$ | the region $R_k$ and the fold, which neither applies inside a box |
| Arithmetic | outward-rounded binary64, then `i128` | `Fraction` | no |
| Author | Evan Daniel’s project | Evan Daniel’s project | yes |

In this composite the two checkers do not back each other up.
Each cell rests on exactly one of them, so the claim needs both to be sound: its trust
base is the union of the two, larger than either alone (F5). The source’s second route
for $s(76)$ (06993982, not retained, §7.5) puts every cell under `zm_mixed.py` alone.
A route of that kind is a second route, not a confirmation by a second checker.

## 7. The $s(76)$ Certificate (`T-184`)

### 7.1 The cover, checked here

| Fact | Value |
| --- | --- |
| Header | `mixed 1`, side $9/1$, $D = 8000$, $W = 4\cdot10^8$, no polygons |
| Points | 41,633, all at distinct positions, none on an integer line or a segment line, none on the boundary; heaviest $157157/25000000$ at $(1.49, 1.87)$ and its images |
| Segments | 9,744 on the lines $x, y \in \{0,\dots,9\}$: 2,104 of length $1/500$, 5,976 of $1/50$, 1,664 of $1/16$; 16 on the walls; 6,744 overlapping pairs |
| Total | $3788361049/50000000 = 75.76722098$, slack $0.23277902$ |
| $D_4$ | invariant as a measure under all eight elements; raw multisets invariant under the two generators |
| Corners | the four blocks $[0,5/2)^2$ and images carry $99792933/5000000 = 19.9586$, the same in both covers, as the band-insertion construction from wand125’s $s(59)$ cover implies |

### 7.2 The composite, from the records

| Check | Source’s records | Retention’s replay |
| --- | --- | --- |
| `zmx2` header | `hash=96e61ce6a0aa2545` (the cover’s FNV-1a), `mode=d4 atoms=grid depth=40 node_cap=20000000 kappa=1.5 K=30`, region $x, y \in 0..44$, bins $0..3$ | the same |
| roots | 8,100 lines, exactly the $45 \times 45 \times 4$ grid, ids consistent, each census a full binary tree | the same, census equal root by root |
| decided by `zmx2` | 8,096 roots, uncertified 0, none capped, depth $\le 36$ | the same |
| left | 4 roots, 18 boxes at depth 40, equal to `failing_roots.txt`; the summary line of `zmx2_v5.out` equals the sum of the root lines | the same 18 boxes |
| `zm_mixed.py` records | 64 files, one header and one record each; digests `ee3e2915`, `bb89de15`, `640fe453` and the cover’s; the certificate-mode settings; region equal to the record’s root; `UNCERT 0`; census a full binary tree; 4,950 boxes, depth $\le 15$ | equal apart from the input path and CPU time |
| tiling | the 64 cells are aligned, distinct, and exactly the 16 sub-cells of each failing root; `jobs.txt` matches them one to one | the same |
| verdict | every cell of $R_9$ decided by exactly one checker | the same, from the replay’s own logs |

The failing roots are $[11/5, 23/10] \times [22/5, 9/2] \times u[3/8, 1/2]$ (2 boxes),
$[21/5, 43/10] \times [43/10, 22/5] \times u[3/8, 1/2]$ (4),
$[43/10, 22/5] \times [21/5, 43/10] \times u[1/4, 3/8]$ (6), and
$[22/5, 9/2] \times [11/5, 23/10] \times u[1/4, 3/8]$ (6). All are in the cross.
Two contain $u = 1/3$, and the top edge $u = 1/2$ of the other two is its image under
$x \leftrightarrow y$ ($\tan\theta = 4/3$).

### 7.3 Exact poses

The program evaluates $\mu$ exactly at 9,326 poses of $s(76)$, plus a local descent:

- 3,000 uniform in $R_9$;
- 200 in each failing root;
- 180 inside, and 144 at the corners of, the 18 listed uncertified boxes;
- 400 at $u = 1/3$ exactly, in the two failing roots that contain it;
- 1,800 at tile germs and one-cut germs ($\theta \to 0^+$ with edges on or near the unit
  grid lines);
- 1,500 random admissible poses of the whole container and their 1,500 folded images.

None captures less than 1. The lowest values are $1.0059$ inside the listed uncertified
boxes, $1.004806$ at one of their corners, and $1.000418$ overall, found by descent at a
bottom-wall germ near $(3.5, 0.5)$, $\theta = 0.0041^\circ$. At the retention’s two
control poses this evaluator and `zm_mixed.py pose` give identical fractions, for the
published cover and for both mutants.
Sampling refutes nothing and proves nothing about the poses it misses.
What it shows is that the certified regions contain no violation the program found, and
how tight the cover is: the bottom-wall tile germs have about 0.04 % to spare.

### 7.4 Mutated covers

| Mutation (D4 orbits removed or every mass scaled) | Exact $\mu$ of the mutant at the pose | `zmx2` on the root holding it |
| --- | --- | --- |
| heaviest point orbit removed (8 points, $0.0503$ in all) | $0.997359$ at the retention’s germ pose near $(1.5, 1.5)$ | root $(15, 15, 0)$: NOT VERIFIED, 235 boxes; the published cover certifies it in 1,709 boxes |
| heaviest segment orbit removed (8 segments, $0.8835$) | $0.905766$ near $(0.533, 3.545)$, $0.896817$ at the retention’s pose | root $(5, 35, 0)$: NOT VERIFIED, 234 boxes; published 6,617 boxes |
| every mass $\times\, 999/1000$ | $0.999417$ at the descent’s lowest pose | root $(35, 5, 0)$: NOT VERIFIED, 234 boxes; published 8,455 boxes |
| every mass $\times\, 199/200$ | $0.999782$ at the lowest corner of the uncertified boxes in root $(44, 22, 2)$ | not run; that root’s cells are `zm_mixed.py`’s (below) |

The roots are given as indices $(i, j, k)$, for centres
$[i/10, (i+1)/10] \times [j/10, (j+1)/10]$ and $u \in [k/8, (k+1)/8]$. In each refused
root, `zmx2`’s default cap of 200 uncertified boxes stopped the run.
For the two scaled mutants, the float minimum that `zmx2` prints at its first
uncertified box is above 1 ($1.00237$, and $1.00015$ for $s(95)$), where the exact value
is below 1. This is the author’s note 1 on issue 594, seen on a control (F6).

**`zm_mixed.py` on a mutant.** The 199/200 mutant puts a hole inside the `zm_mixed.py`
region.
Its exact $\mu$ is $0.999782$ at $(364053/81920,\ 11561/5120,\ u = 21845/65536)$,
which lies in the cell $[22/5, 89/20] \times [9/4, 23/10] \times u[5/16, 11/32]$. The
source’s record `j054` certifies that cell for the published cover in 121 boxes at depth
at most 9. I ran `zm_mixed.py` with `verify.sh`’s flags on that one cell, from copies of
the retained files with digests checked:

- **Depth limit 24, the source’s:** the mutant ran 15 minutes without a verdict and was
  stopped. Scaling by 199/200 takes 0.5 % from every mass, about the cell’s whole margin,
  so the mutant is nearly tight across the cell, not only at the hole.
- **Depth limit 12, for both covers:** the published cover certifies the cell with the
  census of record `j054` (121 boxes, depth 9, 27 CPU-s). The mutant is refused: NOT
  VERIFIED (PARTIAL), 879 boxes, 44 uncertified, 191 CPU-s. Exactly one of the 44
  uncertified boxes holds the hole’s pose.
- **A local mutant, depth limit 24:** this mutant removes the $D_4$ orbit of the
  heaviest segment the square at that pose captures: 8 segments of length $1/16$, among
  them $[73/16, 37/8] \times \{2\}$, $0.198$ in all.
  It gives $\mu = 0.955233$ at the pose.
  `zm_mixed.py` ran 10 minutes on the cell without a verdict and was stopped.
  Its hole is deep, a deficit of $0.045$, so it is not small either.

The depth-12 pair, at equal settings, is the refusal the runbook asks for (F8).

### 7.5 The six boxes at depth 34

The author’s second route (comment of 2026-10-14T08:25:57Z, commit `06993982`) runs
`zm_mixed.py` alone over all 129,600 cells of $R_9$. It leaves six boxes in one cell,
$R = [27/20, 7/5] \times [13/10, 27/20] \times u[1/4, 9/32]$, at depth 24, and closes
$R$ in a rerun at depth 34. That route is not retained here, and this review did not
read its records. The composite route does not depend on it: $R$ lies in the `zmx2` root
$[13/10, 7/5]^2 \times u[1/4, 3/8]$, which `zmx2` certifies in 208,957 boxes at depth up
to 30. The six boxes are therefore covered in the first route by a decision of the other
checker. When the second route is retained, its records can be audited the way §7.2
audits the first. Read with this one, every cell of $R_9$ would then be certified by
`zm_mixed.py`, and all but 64 cells by both.

## 8. The $s(95)$ Certificate (`T-191`)

### 8.1 The cover, checked here

| Fact | Value |
| --- | --- |
| Header | `mixed 1`, side $10/1$, $D = 8000$, $W = 4\cdot10^8$, no polygons |
| Points | 48,352, all at distinct positions, none on any line, none on the boundary |
| Segments | 11,438 on $x, y \in \{0,\dots,10\}$: 3,222 of length $1/500$, 5,976 of $1/50$, 2,240 of $1/16$; 404 on the walls; 7,476 overlapping pairs |
| Total | $3791753447/40000000 = 94.793836175$, slack $0.206163825$ |
| $D_4$ | invariant as a measure under all eight elements; raw multisets invariant under the two generators |

### 8.2 The composite, from the records

As for $s(76)$, with header `hash=e6e0d4182d7f6e43` and region $x, y \in 0..49$. There
are 10,000 roots, each census a full binary tree.
Of these, 9,981 are certified at depth at most 38, and 19 are left with 8,263
uncertified boxes, all at depth 40, none capped; that set equals `failing_roots.txt`.
There are 304 aligned `zm_mixed.py` cells, exactly the sub-cells of those 19 roots.
They use 9,614 boxes at depth at most 13, each record under the pinned digests and the
certificate-mode settings, with its region equal to its root.
The retention’s replay is equal root for root and record for record.
Every cell of $R_{10}$ is decided by exactly one checker.

Of the 19 roots, 11 are in the first $u$ bin ($\theta \le 14.25^\circ$, which contains
$\arctan(1/5) = 11.31^\circ$) and 8 in the bins around the 3-4-5 angle.
One root, $[3/2, 8/5] \times [47/10, 24/5] \times u[0, 1/8]$, holds 8,192 of the
uncertified boxes. They form a slab at $c_y \approx 4.75$, $\theta \to 0^+$, where
`zmx2`’s float minimum is about $1.016$. `zm_mixed.py` closes its 16 cells with 964
boxes at depth at most 11, and the lowest exact $\mu$ found in the root is $1.0077$.

### 8.3 Exact poses

The program evaluates $\mu$ exactly at 17,319 poses, plus a local descent:

- 3,000 uniform in $R_{10}$;
- 200 in each of the 19 failing roots;
- 1,110 inside, and 888 at the corners of, the 111 listed uncertified boxes;
- 3,000 at the two coincidence angles, in the 15 failing roots whose $u$ bin holds one;
- 2,519 at tile and one-cut germs;
- 1,500 random admissible poses of the whole container and their 1,500 folded images;
- the retention’s two control poses.

None captures less than 1. The lowest values are $1.005382$ at the sampled poses inside
the uncertified boxes, and $1.003389$ overall, found by descent near $(3.5, 2.5)$ at
$\theta = 0.016^\circ$.

### 8.4 Mutated covers

The heaviest point orbit (the same corner atom as for $s(76)$) gives $0.997359$ at the
same germ pose; `zmx2` refuses root $(15, 15, 0)$ with 235 boxes, where the published
cover certifies it in 1,709. The heaviest segment orbit lies on the centre line $y = 5$.
It gives $0.854567$ near $(0.554, 4.540)$, and $0.846185$ at the retention’s pose;
`zmx2` refuses root $(5, 45, 0)$ with 234 boxes, published 2,383. Every mass
$\times\, 249/250$ gives $0.999376$ at the descent’s lowest pose; `zmx2` refuses root
$(35, 25, 0)$ with 235 boxes, published 5,141.

## 9. The $k^2 - 5$ Framing

The series names the counts $n = k^2 - 5$: is $s(k^2 - 5) = k$, so that removing five
squares from the $k \times k$ grid still does not let the rest fit in a smaller square?
It is false for $k \le 4$, since $s(11) \le 3.8771$ (`n-011.md`). It is open for
$k = 5, 6, 7$ ($n = 20, 31, 44$). It is proved for $k = 8$ by `T-066`, and now reported
for $k = 9$ and $10$. Each instance is its own certificate.
The corners are wand125’s $s(59)$ cover with bands inserted, but the cross is
re-optimised by LP for each $k$, so nothing here carries to another $k$ without a lemma
for the inserted band.
The register’s rationales say exactly this (`T-191`’s significance), and its headlines
name an instance, not a family.
The consequences the record draws are right.
$s(77)$ to $s(81) = 9$ were already held (`T-067`, `T-064`, `T-086`, `T-084`, the grid).
$s(95) \ge 10$ gives $s(96) \ge 10$ by monotonicity, a second route to the $k = 10$ case
of `T-081`.

## 10. Findings

Graded blocking, major, minor or note.
None is blocking for either claim.

### F1. `tools/check_coverage.py` checks less than its docstring says (minor, in the source)

The script is the step that turns two record sets into a verdict on the whole region.
In `s76-certificate/tools/check_coverage.py`, it reads the `zmx2` log without its header
(lines 18–25), so a log of another cover passes.
It checks a `zm_mixed.py` header only if the file has one, and then only the input
digest (lines 38–40), so a headerless record, or a record naming another `zm_mixed.py`
or other settings, passes.
It accepts the cells inside a failing root when they are distinct, inside the root, of
size $1/20 \times 1/20 \times 1/32$ and of total volume equal to the root’s (lines
46–49). That does not make them a tiling: a cell shifted by $1/40$ overlaps its
neighbour and leaves a slab of the root undecided, with every check passing.
The $s(95)$ copy has the same lines at 20–27, 40–42 and 48–51. The `tiling` controls
(§12) run the retained script, read first and run with `-I`, on mutated copies of the
source’s records. It accepts five of the eight that this review’s check refuses: the
shifted cell, `cert_mode false` with depth 6, another `zm_mixed.py` digest, a removed
header, and a `zmx2` log naming another cover.
It refuses the other three: a removed record, another cover digest, and a missing root.
The published records and the replay’s pass the stricter check, so the claims are
unaffected. In `verify.sh` the records are produced fresh by the pinned checkers with
fixed flags, so the gap matters for anyone auditing the shipped records without
rerunning, which is what a reader of the repository does.
Fix: check cells by their integer grid indices, require a header in every record file
and compare its digests, settings and region with `verify.sh`’s, and compare the log’s
`hash=` with the FNV-1a of the cover.

### F2. `verify.sh` is sound only as a whole (note, in the source)

`zmx2`’s exit status is discarded (`verify.sh` line 60; $s(95)$ line 64). `zm_mixed.py`
exits 0 on NOT VERIFIED, so the `zm_mixed.py` step relies on a `grep` for that string
(line 76; $s(95)$ line 80). A crashed job still stops the script: under `set -e`,
`xargs` returns non-zero.
A job that never ran leaves no record, so `check_coverage.py` fails its volume test.
I found no way for the script to print its final line on a false statement, given F1’s
inputs come fresh from the pinned checkers.
This is why F1 is minor and not major.

### F3. Each cover calls itself a candidate (note, in the source)

Line 2 of `s76_cover_v5.txt` reads
`# s(76) candidate: band-inserted s(59) corners + cross LP, free part x 1.000000`, and
the $s(95)$ file’s line 2 is the same.
Both checkers ignore comments, so this changes nothing, but a reader holding only the
certificate sees a working label.

### F4. The $s(95)$ wrapper’s doc comment names `S76Cover` (note, in the source)

`lean/S95Lower.lean` line 11, from `lean/mk_lean.py` line 56, says “`S76Cover` is the
covering statement”; the definition is `S95Cover`. The retention found it; confirmed.

### F5. Two checkers, one per cell (note, for the record)

The register says the covering statement is decided by two checkers, each on its own
cells (`packing/frontier/results.yaml`, `T-184`’s claim from line 24885 and `T-191`’s
from line 26028), and that is accurate.
The record should keep that shape when it raises the entries: the composite is a
reproduction with the producer’s code (same-implementation).
Its trust base is the union of the two checkers’, and it is not a confirmation by two
programs (§6).

### F6. `zmx2`’s float minimum is not evidence (note, for the record)

At an uncertified box, `zmx2` prints the least float $\mu$ of 300 sampled poses
(`zmx2.rs` line 1976, in `cmd_cert`). On this review’s two scaled mutants, it printed
$1.00237$ and $1.00015$ at boxes holding poses where the exact value is $0.99942$ and
$0.99938$. That confirms on a control the author’s note 1 on issue 594. The retention
used exact `zm_mixed.py pose` values for its statements about the failing roots, as it
should. A record that cites a float minimum for a failing box should do the same.

### F7. `CovM` at the wrapper’s revision was not read (note, for the record)

The wrappers build on `Sqpack` at `1718a58`, which no packet retains.
`S76Lower.lean` and `S95Lower.lean` state their hypotheses in terms of it at line 24.
§3.8 reads `CovM` and `le_minSide_mixed` at `f58a017` instead.
If `1718a58` changed `CovM`, the match between the hypothesis and the composite’s
statement needs re-reading.
The wrappers matter only for a future V5 route, not for V3/C3.

### F8. `zm_mixed.py`’s refusal of a mutant is shown at depth 12 only (note, for the record)

Stage 4 asks that two mutated certificates be refused by every checker that accepted the
original, and that a test hold them (`result-import.md` line 508). For `zmx2` the
retention’s refusals and those of §7.4 and §8.4 meet that.
For `zm_mixed.py` the retention judged a refusal at depth 24 unaffordable.
This review has one, at a depth limit of 12 with the published cover certifying at the
same limit (§7.4). The 199/200 mutant at the source’s limit of 24 did not finish in 15
minutes. A test can hold the depth-12 pair as it is.
A local mutant, one segment orbit removed, did not finish at depth 24 within 10 minutes
either (§7.4); its hole was deep.
The design left to try, under a time limit, is a mutant whose hole is both local and
shallow: one that removes just more than the margin at one pose.
For $s(95)$ no `zm_mixed.py` control was run.
None of this bears on the claims; it is what the records lane’s control needs.

## 11. Questions for the Author

1. Would you tighten `tools/check_coverage.py` as F1 proposes (grid indices, every
   header field, the `zmx2` header hash)?
   The repository’s audit tool will check the same things when cases 76 and 95 are
   registered.
2. Is `Sqpack` at `1718a58` public, and is its `CovM` the definition at `f58a017`, the
   revision this repository retains?
   If it changed, what changed?
3. For $s(95)$, if you run the full `zm_mixed.py` pass you offered, publishing its
   records in the format of $s(76)$’s second route would let them be audited cell by
   cell beside the composite.
   Neither claim needs it.
4. Out of curiosity, and with no bearing on the claim: do you know what makes `zmx2`
   leave 8,192 boxes in the $s(95)$ root $[3/2, 8/5] \times [47/10, 24/5]$ near
   $c_y = 4.75$, $\theta \to 0^+$, where $\mu$ is about $1.016$?

## 12. The Programs

`k2m5_review.py` (standard library only; imports nothing from the source, the checkers
or this repository) and `corner_scan.py` are kept, with their outputs, under
[`packing/resources/web/bengreff-s76-certificate-2026-10-14/review/`](../../../packing/resources/web/bengreff-s76-certificate-2026-10-14/review/README.md).
The README there says what each subcommand read, how to run it, and what it printed:

- `cover`: the data facts;
- `records`: the composite;
- `poses`: exact $\mu$ at sampled poses, and the fold;
- `mutants`: the mutated covers;
- `cellmin`: the lowest $\mu$ in one cell;
- `tiling`: mutated record sets through the author’s script.

The `zmx2` and `zm_mixed.py` control receipts are there too.
The `zmx2` binary was built from retained bytes by the project’s
`devtools.replay_evand_zmx2 build`. `zm_mixed.py` ran from copies of the retained files,
digests checked, read before they ran, with nothing fetched.
In all, the programs and controls used about 35 CPU-minutes on a shared four-core host,
one process at a time.

## 13. For the Records Lane

- **What this review supports.** No blocking defect is open for `T-184` or `T-191`.
  Recorded as `external_review` (`informally-verified`) on `E-bengreff-594-cover-report`
  and `E-bengreff-610-cover-report`, and listed in each entry’s `reviews`
  (`kind: adversarial`, `reviewer_kind: ai`, verdict `accepted`), it supports C1. It
  does not move V or C to rung 3 by itself.

- **What C3 and V3 need beyond it** (each entry’s `next_rung`): the retained
  reproduction recorded as evidence through the tools that register cases 76 and 95
  (`think-ccjt`). That is the replay’s `zmx2` root logs and `zm_mixed.py` records,
  decided by a composite audit that checks what §7.2 lists: the full root grid, the
  header hash, every record header, cell alignment, region equal to root.
  This review’s `records` subcommand is one such audit, not a registered tool.
  With that evidence, nothing here stands in the way of V3/C3, with the confirmation
  worded “reproduced with the producer’s code”.

- **Mutated certificates** (runbook, stage 4: refused by every checker that accepted the
  original, and held by a test).
  The `zmx2` refusals are in §7.4 and §8.4, and in the retention’s receipts.
  `zm_mixed.py` has one refusal, for $s(76)$ at a depth limit of 12, with the published
  cell certifying at the same limit (§7.4). A second for $s(76)$, and two for $s(95)$,
  are still owed (F8).

- **Rung 4** needs a second adversarial AI review by a distinct reviewer and a human
  oversight record.

- **Not machine-checked**, as the 2 October review listed for its covers:
  1. `zm_mixed.py`’s lemmas and program, with `mixed_cover.py`;
  2. `zeromargin.py`’s program;
  3. `zmx2`’s lemmas, program and parser;
  4. the IEEE-754 behaviour of the hosts that ran `zmx2`;
  5. the composite’s bookkeeping, checked here by a program that is not a registered
     tool;
  6. the totals and the invariance, by three parsers here, and kernel-checked at the
     source in wrappers not built here;
  7. the reduction, proved in Lean upstream (not built here) and on paper in §3.3.

  That the source’s runs came from the pinned files on these bytes is no longer an
  assumption: the retention reproduced both from retained bytes, equal root for root and
  record for record.

- **Significance:** S3 for each, confirmed.
  Each is an exact value at an open count, by a recipe the record already holds; neither
  is a new technique or a family.

- **Text to update when the rungs move:** `next_rung` of both entries (the review is
  done), and `T-184`’s notes, which can name the second route at `06993982` once a
  packet retains it (`think-osvq`).

## 14. Comparison With the Review of 2 October, and What Was Read First

The model for this review is the
[review of 2 October](review-2026-10-02-wand125-s59-s77-mixed-covers.md) of wand125’s
$s(59) = 8$ (`T-066`) and $s(77) = 9$ (`T-067`), by the same method and the same
checkers.

**What was read first.** Before the first draft of §1 to §13 here was written, I read
four parts of that review: its title and front matter, its one-line summary, its §1 and
§2 (lines 1–86), and its list of headings, which names its findings F1 to F7. Its §3 to
§12 were read after this review’s findings F1 to F7 were drafted.
Two things were added here after that reading: the “not machine-checked” list in §13,
which follows its §12, and this section.
The paragraph on the `zm_mixed.py` control in §7.4 and finding F8 were written after the
control finished, from its results.
Of the [28 September review](review-2026-09-28-evand-s21-s45-mixed-covers.md) I had read
§2 and §3.4; its term-by-term table is the model of the one in §3.5. What that early
reading may have shaped:

- the overlapping-pair count in the cover audit, since its §2 names 632 overlapping
  pairs in the $s(77)$ cover;
- the sentence in §5.3 that `clip_bin`’s zero-width case cannot arise, since its §2 says
  the guard Daniel added after the pin could not fire in its runs; the reason given here
  is different and shorter (no cell is clipped at all);
- F3 here, whose kind of finding I had seen in its heading F7;
- §7.5, since its §2 had told me that the $s(59)$ depth-24 sweep left six boxes in the
  root its depth-34 run certified; the brief and issue 594 say the same of $s(76)$’s
  second route.

**Where the two reviews agree.** On the reduction: the concentric shrink, closed
squares, and no limit argument, so that a cover at margin zero in scale is a proof.
On the fold and its $u$ range, and on the closed conventions, overlapping segments
included. On each checker’s trust boundary: the lemmas, Lemma R’s IEEE-754 model, the
parser bounds, certificate mode, and the program’s own bookkeeping.
On the shared architecture and authorship, and on what C1, V3/C3 and rung 4 need.
And both confirm S3.

**Where the covers differ, and so the reviews.**

- **The composite is load-bearing here.** For `T-066`, `zmx2` decided the whole region,
  folded and unfolded (§7.5 there), and the `zm_mixed.py` composite was a second route
  whose premise could not be checked.
  Here `zmx2` leaves 4 and 19 roots, so `zm_mixed.py` is in the trust base, and in
  partial mode for every job.
  The 2 October review read that mode as a root filter, used there for one rerun (§5 and
  §7.3 there); here every job uses it (§3.5).
- **Its F1 does not arise.** The records that review found pinned but absent are here
  retained in full, and §7.2 and §8.2 audit them cell by cell.
  The nearest relative is this review’s F1, that the author’s audit script checks less
  than it says. That review said the like of `verify.sh --zm`, which tested its premise
  from a rounded print.
- **Its F2 and F3 do not arise.** Both trees pass their own `SHA256SUMS` (the retention
  checked it), and the issues, READMEs and logs agree on the flags: no `--pair-points`,
  and `atoms=grid` in both log headers.
- **Its F5 has an analogue that is real.** There the register’s stated worry (points on
  loaded lines) did not apply.
  Here the register names the wall segments, which exist; §3.6 shows they are harmless.
- **Its F6 is moot here, for a shorter reason.** `clip_bin` never changes a cell (§3.6),
  so no box reaches `region_phi` with $u_1 = u_0$.
- **Its F7 and F3 here** are the same kind of note.
- **New here:**
  - the wall segments (§3.6);
  - the demonstrations behind F1;
  - F6, seen on controls;
  - the Lean wrappers and F7, which `T-066` lacked;
  - the $k^2 - 5$ framing (§9);
  - the fold checked exactly at sampled poses (§3.4);
  - mutated covers refused, run by the reviewer (§7.4, §8.4).
- **Which sweep to record.** That review recommended the `--full` sweep as the one to
  replay, because it needs no symmetry and `zmx2` alone closed it.
  Here `zmx2 --full` meets the images of the poses it cannot close, so a `--full` route
  would presumably need `zm_mixed.py` on those images’ cells too (`think-eucc` prices
  it). The fold is proved (§3.4) and the invariance checked three ways, so the $D_4$
  composite is the one to record, and a `--full` route would be a second route.

Anything this review says that the 2 October one also said was re-derived here from the
files of these covers, not taken from it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
