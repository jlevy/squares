# Review Programs, 14 October 2026

The five programs here were written and run by the mathematical review lane of this
import (bead think-tsox), an AI agent, Fable at the strong tier with max reasoning, for
the review
[`review-2026-10-14-wand125-closed-form-lower-bound.md`](../../../../../docs/project/reviews/review-2026-10-14-wand125-closed-form-lower-bound.md).
Each is the lane’s own code, written after reading SPEC.md, README.md, the structure
scripts and the Rust checker, in a file that imports none of the source; none is
clean-room, and the source’s commit names the same system family as co-author.
All were run with the project interpreter, Python 3.14.7, as `python -I`, on one worker
of a four-core host shared with other agents.
Their receipts are under [`outputs/`](outputs/).

None of them decides the theorem.
The first four decide premises and consequences: what the theorem says at each count,
whether that is consistent with the record, the inequalities the proof’s localization
asserts in prose, and the arithmetic of the source’s replay receipt.
The fifth samples the claim itself on three of the 34 intervals: it can refute and cannot
establish.
The review names them as proposed entries for `packing/frontier/verifiers.yaml`; they are
registered nowhere yet.

| Program | SHA-256 |
| --- | --- |
| `a_of_n_by_definition.py` | `6e7ed56592d13c25446f6bd76d1634b9532fef5ec0ca8acb2a8ebaa135bb0ad1` |
| `record_consistency.py` | `a0fc92993452d20da1b9f36e3890c39acf3cce54f7e6598b4b6887266562a0ae` |
| `localization_checks.py` | `b3bbe6413b6e3dae0ab2a0cf1a2eb3c04cb4ff0c0c41e8baf04623ab96c4894a` |
| `replay_receipt_pieces.py` | `3da9b960c45e589150cdc42407683744dd6eb42ebcadbf931da48ee0a5156c96` |
| `family_probe.py` | `bb7a9d1df6d971964752e673230f088755792edced0dff7f6c571974863398b6` |

Run every one from `packing/`:

```sh
P=resources/web/wand125-closed-form-2026-10-14
uv run --frozen --all-extras --group dev python -I $P/review/a_of_n_by_definition.py --out $P/review/outputs/a_by_definition.json
uv run --frozen --all-extras --group dev python -I $P/review/record_consistency.py --out $P/review/outputs/consistency.json
uv run --frozen --all-extras --group dev python -I $P/review/localization_checks.py
uv run --frozen --all-extras --group dev python -I $P/review/replay_receipt_pieces.py
uv run --frozen --all-extras --group dev python -I $P/review/family_probe.py --interval 20 --dir SCRATCH/interval_0.465_0.47 --out $P/review/outputs/probe-20.json
```

## `a_of_n_by_definition.py`

**What it does.** Encloses $a(N)$ from the definition of SPEC.md §1.1 alone, with no
closed form and no square root: on each interval the admissible $\delta$ form an initial
segment because $T_i(\delta) = (k+\delta)^2 - 4(\alpha_i\delta + \beta_i)$ is increasing
(it checks $2(k + d_0) - 4\alpha_i > 0$ at every count), so the supremum on the interval
is $d_1$, nothing, or the root of $T_i = N$, which bisection encloses to $2^{-128}$ and
narrower when a decision needs it; the largest candidate is found by refining the
enclosures until they separate or an exact tie is established.
It decides the facts about the intervals that the corollaries use.

**What it read.** The retained `intervals.json.gz`, refused unless its SHA-256 is the
packet manifest’s (`a91b0b49…`); the retained output of the source’s `a_of_n.py`
(`evaluation/outputs/a_of_n-49-3600.json.gz`) and the intake evaluation’s
`evaluation/outputs/bounds.json`, to compare.

**What it printed** (`outputs/a_by_definition.json`, 10 s). At all 3,498 non-square
counts from 49 to 3,600, the 30-place value $v$ printed by the source’s `a_of_n.py`
satisfies $v \le a(N) < v + 10^{-30}$, and so does the intake evaluation’s at its 264
counts; the attaining interval agrees everywhere; 234 counts are exactly a cap
$k + d_1$ and 3,264 are roots.
The 34 intervals cover $(0, 1]$ with no $j/5$ interior to any; $\max_i \alpha_i = 1.7495351\ldots < 1.7496$;
$I_1$’s line is $\alpha_1\delta$ with $\alpha_1 > 1/2$; the least margin of a certified
line over $\delta/2$ at an endpoint with $\delta \ge 1/50$ is $0.0226439\ldots$ on $I_2$ at
$\delta = 1/50$; $S^*(1) = 0.8528498\ldots > 3/4$. It printed `A-BY-DEFINITION OK`.

## `record_consistency.py`

**What it does.** Reads the enclosures above and the front matter of
`packing/frontier/n-049.md` to `n-324.md` (PyYAML), and places $a(N)$ against the four
lanes of each case: above a recorded upper bound would refute the claim.
It checks the known values the source says its bound recovers, $a(N) = m$ at
$m^2 - 1, m^2 - 2, m^2 - 3$ where the records hold $s(N) = m$ as proved, and $a(N) < m$
at $m^2 - 4$; that $a(N) \le k + 1$; and whether $a(N)$ is nondecreasing in $N$, which is
information, not a requirement.

**What it read.** `outputs/a_by_definition.json` and 276 case records.

**What it printed** (`outputs/consistency.json`, 2 s). Of 264 non-square counts: below
both upper bounds at 231 and equal at the 33 counts $m^2 - 1, m^2 - 2, m^2 - 3$,
$m = 8, \dots, 18$, all proved with value $m$; above the reported lower bound at 156,
equal at 33, below at 75; above the verified lower bound at 189, equal at 33, below at
42, which are the intake evaluation’s counts; below $m$ at the eleven $m^2 - 4$;
$a(N) \le k + 1$ and nondecreasing throughout. `RECORD CONSISTENCY OK`.

## `localization_checks.py`

**What it does.** Decides in exact rational arithmetic the 29 inequalities that SPEC.md
§2.3, §4.1 and §5.1 assert in prose and `validate_family.py` leaves to the
specification: corner and edge reach for $k \ge 7$ and the failure at $k = 6$; the ranges
of the shifted square in the periodic reduction; that the checked regions’ squares stay
inside $[0, 24/5]^2$ (left, straddle, top) or inside the first three bottom-wall periods,
right of the left wall and below the far edge of $U$ (right); the coverage of
$[0, 3.8 + \delta] \times [0, 3.8]$ by the four regions for every $\delta \in [d_0, d_1]$
and where the remainders of steps (3a) and (3b) land; the quarter-turn condition on
$[-13/32, 7/16]$; the half-width bound `hmax`; the window premise $a - 9/5 \ge 24/5$;
and $\alpha_i \le 1.7496$.

**What it read.** `intervals.json.gz`, digest-checked, for the endpoints and slopes.

**What it printed** (under 1 s). All 29 hold.
The worst margin of $a/2 + r < a - W$ is $183/625$ at $k = 7$, $\delta = 1$; $k = 6$
holds it at $\delta = 0.585$ and fails at $0.586$ and $1$ (the threshold is
$2(1 - r) = 0.5856$); the quarter-turn sum is $523/512$. `LOCALIZATION OK`.

## `replay_receipt_pieces.py`

**What it does.** Checks the source’s replay receipt against itself and the published
files: for the 25 records that were cut into pieces for the replay, the pieces’ bounds
tile the region of `intervals.json` exactly (inside, pairwise disjoint, equal area),
their root counts add to the record’s and their line-hash sums add modulo $2^{256}$ to
the record’s; every record’s `roots` and `leaves` equal `intervals.json`’s and every run
is `ok`; the runs and CPU-hours add to the stated totals; every record digest is the
published record’s, every family digest is `families.json`’s old digest whose new digest
is `intervals.json`’s, and the published-build receipt’s eight runs name the published
digests with the published counts and kinds.

**What it read.** `receipts/replay.json.gz`, `receipts/families.json`,
`receipts/published_checker.json` and `intervals.json.gz`, each refused unless its
SHA-256 is the manifest’s.

**What it printed** (under 1 s). 136 records, 25 cut into 158 pieces, 269 runs,
4,294.08 CPU-hours; the published build replayed intervals 1 and 34 in 8 runs; no
problem. `REPLAY RECEIPT OK`.
A receipt is the author’s statement, and this decides only that it is consistent and
names the published files.

## `family_probe.py`

**What it does.** For one released interval whose asset was downloaded into a scratch
directory and checked against `ASSET.json` and the archive’s `SHA256SUMS`, it re-derives
with code of its own: the family format and nonnegativity; the bottom-wall period read
from `T` at $x \in [3, 4)$, its mass $9/5$, its reflection symmetry and its repetition in
the six other stored periods; the left wall of `F` as the transposed reflected period;
the two corner remainders, nonnegative and inside $[0, 2 + d_0] \times [0, 2]$ (`F`) or on
the line $x = 2$ (`T`); the terminal mass $m_v$; the saving
$S(\delta) = 99/25 + 9\delta/5 - M_C(\delta) - m_v$ at both ends against the stored
values and the certified line; the right-side family as `T` row for row.
It builds the global measure of §2.1 for $k = 7, 8, 11$ at $d_0$, $d_1$, the midpoint
and a random $\delta$, and decides the mass identity
$\operatorname{mass} = a^2 - 4S(\delta) - (a - 18/5)^2$, the support inside the container
and equality with the local family on $[0, 24/5]^2$ as a segment measure.
It re-decides each region record: well-formed roots with no unproved leaf, the product
grid over the region’s bounds, the $u$-range and $[d_0, d_1]$, no $u = 0$ inside a root
or a vertex-type leaf, the supported leaf kinds with `intervals.json`’s counts, every
root’s leaves of the root’s volume and inside it, and, for every root of the top record
and a sample of roots of the others, pairwise disjoint leaf interiors, which with the
volume is an exact tiling by a route other than the checker’s midpoint bisection.
Then it computes the mass of the global measure ($k = 7$ and $8$) on closed unit squares
exactly, by Cyrus–Beck clipping of every segment and exact clipping of the square by $U$,
at random admissible poses in the lower-left quarter and a few anywhere, at the delicate
pose families of SPEC.md §8 (3), and at the poses a floating-point pattern search from
random starts finds lowest, snapped to rationals; every exact mass must be at least 1.
Where the centre lies in the left, straddle or top region it also requires the local
family’s mass to equal the global one, and in the right region the right-side family’s
mass, in shifted coordinates, not to exceed it.

**What it read.** The three assets below, unpacked in scratch and not retained;
`intervals.json.gz`, digest-checked; `ASSET.json` through the digests recorded here.
Its author ran the source’s `validate_family.py` once on interval 20’s families to
compare decompositions while fixing a clipping bug of this program.

| Asset | Bytes | SHA-256 (equal to `ASSET.json` and the release API) |
| --- | --- | --- |
| `interval_0.465_0.47.tar.gz` (interval 20) | 4,418,084 | `9b90ca0fdcb7aba169ab9e20af572d8d59a782383896036931a23a262d23b4bb` |
| `interval_0.38_0.4.tar.gz` (interval 7) | 10,690,117 | `616f8fdee44467a1f74855e0420ea287a6a1d47c7f15bfc01be35fab2855ba07` |
| `interval_0.99_1.tar.gz` (interval 34) | 7,241,272 | `04b7a25f5a7bb94fc29a18a80c8e22fb1166a732ea8d61b55608f80559903171` |

**What it printed** (`outputs/probe-20.json`, 174 s wall on one worker, seed 20261014,
150 random poses and four descents per $(k, \delta)$, 200 sampled roots per record except
the top record, which was checked whole). Interval 20, $[93/200, 47/100]$: no format
problem; the right-side family is `T` row for row; every structure check passed, with
$S(d_0) = 0.4801855183756238$ and $S(d_1) = 0.47919140389062376$ equal to the stored
values and to the certified line; all twelve global builds ($k = 7, 8, 11$ at $d_0$, the
midpoint, a random $\delta$ and $d_1$) pass the mass identity, the support and the window
identity; the four records have 10,584, 17,442, 4,158 and 13,338 roots on grids of
$14 \times 28$, $17 \times 38$, $14 \times 11$ and $13 \times 38$ cells by 27 $u$-pieces and
one $\delta$-piece, 832,232 leaves of the published kinds and counts, every root’s leaves
of the root’s volume and inside it, and no overlap among the leaves of any checked root;
of 1,345 admissible poses checked exactly, the least mass is exactly 1 (at
$k = 7$, $\delta = 93/200$, a random pose), none is below 1, the local family’s mass
equalled the global one at all 679 poses in the left, straddle and top regions, and the
right-side family’s mass never exceeded the global one at the 348 poses in the right
region. `FAMILY PROBE OK`.

The runs on intervals 7 and 34 were stopped, to keep the lane inside its CPU budget,
before their receipts were written; an earlier run on interval 7 with a prior revision of
this program passed every structure check and reproduced the example savings of SPEC.md
§3.2, $S(19/50) = 0.589900810970916$ and $S(2/5) = 0.624200093890916$, and no receipt of it
is kept.
The command above, with `--interval 7 --dir SCRATCH/interval_0.38_0.4` or
`--interval 34 --dir SCRATCH/interval_0.99_1`, completes them.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
