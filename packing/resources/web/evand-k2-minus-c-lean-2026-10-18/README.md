# Daniel’s Lean Proof of c*(k) ≤ 4⌈√(2k − 7)⌉ − 1, Pinned 2026-10-18

This packet pins Evan Daniel’s Lean proof that for every integer $k \ge 7$,
$k^2 - 4b$ unit squares fit in a square of side less than $k$ with
$b = \lceil\sqrt{2k - 7}\rceil$, so
$c^*(k) \le 4\lceil\sqrt{2k - 7}\rceil - 1$, where $c^*(k) = \max\{c : s(k^2 - c) = k\}$.
It is `UnitSquarePacking.Ryu.packs_sub_4sqrt2_layers` in
[evand/square-packing](https://github.com/evand/square-packing), first committed at
`4b456fe` on 18 October 2026 and retained here at `aa12b98`, which in the same push adds
the bundle’s README, its build script and the write-up
[*Short of a Square*](https://evand.github.io/square-packing/k2c/).

No issue reported it: the intake read of 19 October found it, and bead `think-f8py` holds
the import. Its Frontier key is **[Daniel k2-minus-c Lean 2026-10-18]**, and the
asymptotic register records it as a reported row of `deficiency_upper_bounds`, before
Kevin Fang’s Theorem A of 24 October (#797, the
[fang-theorem-a-2026-10-24 packet](../fang-theorem-a-2026-10-24/README.md)), which proves
a bound of the same strength independently and credits this one as earlier.
Nothing here has built the proof, and no mathematical review has read it yet.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/evand/square-packing> |
| Revision | `aa12b989aa7d4244c57ea6c3b06bb36318bd41ea`, tree `31fd5f6efc25c2e3f479570bf283256e7d69adc8`: “k² − c package: Lean bundle, write-up page /k2c/, index and notes” |
| Committed | 2026-10-18T06:49:22Z (00:49:22 by the author’s clock, `-06:00`), by Evan Daniel |
| The theorem’s commit | `4b456feee16e25e4831326a2bad5ced2122881b7`, committed 2026-10-18T05:44:46Z and pushed at 15:47:56Z with `13da782` and `aa12b98`: “c*(k) ≤ 4⌈√(2k−7)⌉ − 1 for every k ≥ 7, in Lean (filled L-shape with two top layers)”. It adds `RyuEnds.lean` and `RyuLayers.lean`; every module of the closure has the same bytes there and at the pin |
| The +5 milestone | `a645fe3610425507ddfb9825045094028c1d28f4`, committed 2026-10-18T02:28:04Z and pushed at 05:14:06Z: $c^*(k) \le 4\lceil\sqrt{2k-7}\rceil + 5$ (`RyuFill.packs_sub_4sqrt2`), one axis layer at each band end; it adds `RyuFill.lean` and changes `RyuBand.lean` |
| Not retained | `13da782` (06:40:31Z) adds the staircase modules of Daniel’s $c^*(k) < 18.9k^{2/5} + 35.7k^{1/5} + 122$ for $k \ge 3 \cdot 10^5$, which bead `think-pf37` holds |
| Licence | MIT, “Copyright (c) 2026 Evan Daniel” (`LICENSE`) |
| Retrieved | 2026-10-24T21:02Z, a blobless clone, head `659ee62`, with a sparse checkout of the pin |
| Pinned subtree | 23 files, 209,303 bytes, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) |
| Retained here | 11 files, 129,116 bytes, byte-identical under [`square-packing/`](square-packing/) |

## Credit and AI Assistance, as the Source States Them

`certificates/k2-minus-c/README.md` credits the L-shaped packing, the waste identity and
the staircase to Sungjoon Ryu’s preprint *k² − c upper bounds* (squarepacker/k2-minus-c-upper
v1.1), with H. D. Bui’s construction behind the staircase and Erdős and Graham behind the
L-shape, and the bounds $4\lceil\sqrt{2k-7}\rceil + 5$ and $4\lceil\sqrt{2k-7}\rceil - 1$ to
“this repository”. It says the axis-filled ends “were suggested by a literature-reading
agent of this repository (2026-10-17)”, that the formalization is “this repository (Evan
Daniel, with Claude), 2026-10-17/18”, that novelty was “checked against jlevy’s register
(`packing/frontier/asymptotic-waste-bounds.yaml`, 2026-10-18) and Ryu’s paper”, and that
the work is “Not peer reviewed.” `CREDITS.md`, byte-identical to the 12 October exact-data
packet’s, says the repository’s work was produced by Claude (Anthropic) under human
direction. The record credits the bound to Evan Daniel after Sungjoon Ryu.

## What Is Retained

Retained byte-identical at their upstream paths, under `square-packing/`:

- **the theorem modules** `lean/Sqpack/RyuLayers.lean` (`packs_layers`,
  `packs_sub_4sqrt2_layers`), `RyuEnds.lean` (Ryu’s Lemma 5.1 in general form, the
  rotation by π, half-plane separation, axis layers), `RyuFill.lean` (the +5 milestone)
  and `RyuBand.lean` as it stands from `a645fe3` on (the band, transposition and the
  L-shape);
- **the root module** `lean/Sqpack.lean` and **the axiom probe** `lean/Axioms.lean`, both
  changed since the 18 October Fang and Ryu packet;
- **the bundle**: `certificates/k2-minus-c/README.md`, the table of bounds and what each
  rests on, and `verify.sh`, which rebuilds the modules and accepts each theorem only if
  `#print axioms` lists exactly `propext`, `Classical.choice` and `Quot.sound`;
- **the write-up** `site/www/k2c/index.html`, *Short of a Square*, as served at
  evand.github.io/square-packing/k2c/ (no scripts); and
- **the numerical companions** `search/ryu/r1prime.py`, the axis-filled L-shape in exact
  rationals with a pairwise check, which the README cites for “no other $b$ or axis layering
  of this construction does better” for $7 \le k \le 3 \cdot 10^5$, and
  `search/ryu/endcost.py`, an exploration of end costs. Neither was run here.

Pinned by digest only, each byte-identical to a copy this repository already retains:

| Upstream path | Retained in |
| --- | --- |
| `lean/Sqpack/Conjectures.lean`, `ConjecturesProofs.lean`, `FangGlue.lean`, `RyuBound.lean` | [18 October Fang and Ryu Lean packet](../evand-fang-ryu-lean-2026-10-18/README.md) |
| `lean/Sqpack/Spec.lean`, `ExactPack.lean`, and `lean/lean-toolchain`, `lakefile.toml`, `lake-manifest.json` | [7 October evand packet](../evand-exact-and-local-reports-2026-10-07/README.md), under `source/s12/lean/` |
| `LICENSE`, `CREDITS.md` | [12 October evand exact-data packet](../evand-exact-data-2026-10-12/README.md) |
| `README.md` | [19 October evand n308 packet](../evand-n308-2026-10-19/README.md) |

[`acquisition/sources.json`](acquisition/sources.json) records each file, and from
`packing/`,
`uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-k2-minus-c-lean-2026-10-18 --checkout CHECKOUT`
rebuilds the packet from a checkout at the pin; `--check` re-derives it without one.

**The closure.** [`receipts/lean-closure.json`](receipts/lean-closure.json), written by
`devtools.lean_closure` from the Git objects at the pin, follows every import from
`Sqpack.RyuLayers`: 10 project modules, 132,870 bytes (`RyuLayers`, `RyuFill`,
`RyuEnds`, `RyuBand`, `RyuBound`, `FangGlue`, `ExactPack`, `ConjecturesProofs`,
`Conjectures`, `Spec`), `Mathlib` the only import outside them, nothing missing, and no
`sorry`, `axiom`, `native_decide`, `implemented_by`, `extern`, `unsafe`,
`debug.skipKernelTC` or native-evaluation token in their code. The build pins are
`leanprover/lean4:v4.33.1` and Mathlib `0df444a360eaa60ab8c11dca51a86af692955474` (input
revision `v4.33.1`), the pins of the `s(13) = 4`, Bentz and T-236 builds.

## The Claim, as the Source States It

`lean/Sqpack/RyuLayers.lean`, namespace `UnitSquarePacking.Ryu`:

```lean
theorem packs_layers (k b : ℕ) (hb : 3 ≤ b) (hkb : b + 4 ≤ k) (hk : 2 * k ≤ b ^ 2 + 7) :
    ∃ s < (k : ℝ), Packs (k * k - 4 * b) s
theorem packs_sub_4sqrt2_layers (k : ℕ) (hk : 7 ≤ k) :
    ∃ s < (k : ℝ), Packs (k * k - 4 * (Nat.sqrt (2 * k - 8) + 1)) s
```

The construction is Ryu’s L: a $(k - b)^2$ grid and two bands of rows of $b$ tilted
squares, $L - 3$ rows in a band of length $L$, at the angle $t = 1/b + \delta$ with
$\delta \cdot b(b^2 + 1)(6k + 4b) = 1$. Below the first row of each band go
$\lfloor (b - 1)/2 \rfloor$ axis squares, above the last row of the right band
$\lfloor b/2 \rfloor$, and above the last row of the top band $\lfloor b/2 \rfloor + 1$ and a
second layer of one: $2b$ end squares in all. The commit message and the bundle’s README
say “standard axioms only”. No build log is published.

## The Definition Bridge, Checked by Reading

The theorem is an existential statement about `Packs`, and the register’s row states a
bound on $c^*(k)$. The bridge holds:

- **`Packs` is this record’s packing.** `Packs n s` (`Spec.lean`, retained by the 7 October
  packet) holds when there are centres `c : Fin n → ℝ × ℝ` and angles `θ : Fin n → ℝ` such
  that every `unitSq (c i) (θ i)`, the image of $[-1/2, 1/2]^2$ under a rotation by any real
  angle and a translation, lies in `container s` $= [0, s]^2$, and every two have disjoint
  interiors. That is a packing of $n$ closed unit squares with disjoint interiors in a
  square of side $s$, the object $s(n)$ minimizes. No other `Packs` is defined in the
  closure: `Conjectures` and `ConjecturesProofs`, which `RyuLayers` opens, define
  `GridOptimal`, `PacksIn` and `rect` on top of it, with `Packs n s ↔ PacksIn n (rect s s)`
  by `Iff.rfl`.
- **The count is the stated one.** For $k \ge 7$, $2k - 8 \ge 6$, so the natural
  subtraction is exact, and `Nat.sqrt (2k − 8) + 1` is the least $r$ with $r^2 \ge 2k - 7$,
  that is $b = \lceil\sqrt{2k - 7}\rceil$. The proof derives $b + 4 \le k$, so
  $4b < k^2$ and `k * k - 4 * b` is exactly $k^2 - 4b$.
- **From a packing to $c^*(k)$.** A packing of $k^2 - 4b$ squares in a side $s < k$ gives
  $s(k^2 - 4b) \le s < k$. Removing squares keeps a packing, so $s$ is nondecreasing in
  $n$ and $s(k^2 - c) < k$ for every $c \ge 4b$. Hence no $c \ge 4b$ has $s(k^2 - c) = k$,
  and $c^*(k) \le 4b - 1 = 4\lceil\sqrt{2k - 7}\rceil - 1$, the row’s statement.

## The Build Plan, Priced

From the retained files staged at `lean/`, with the pinned copies the acquisition record
names:

```sh
lake exe cache get
lake build Sqpack.RyuLayers
lake env lean AXIOMS.lean   # #print axioms UnitSquarePacking.Ryu.packs_sub_4sqrt2_layers
```

accepted only with `propext`, `Classical.choice` and `Quot.sound`. Bead `think-fqp6` holds
it as a validation item: under 1 CPU-hour, an estimate from the T-236 bead’s price for
`RyuBound`’s seven modules (under 0.5 CPU-hours) and the three modules this closure adds
(`verify.sh` reports about 5 minutes from a cold cache on 16 cores for the whole Ryu
line). It did not run here: the toolchain and Mathlib cache need about 9 to 10 GB of disk,
and this host had about 13 GB free, shared by four lanes, on 24 October.

## Limitations

- **Nothing was built or run here.** The axiom set is the source’s report.
- **No review has read the proof.** Its mathematical review, and the kernel build, are
  the gates `think-f8py` and `think-fqp6` hold.
- **Later and related work is not here.** The staircase bound of `13da782` is
  `think-pf37`’s. The junction variant of `search/ryu/junction.py` at `a435c97`, which the
  source reports lowers $c$ by 1 or 2 at most $k$ from 15 to 400, is a finite table of
  values checked by the source’s programs, not a statement for every $k$, and moves no
  count the record tracks; the import declined it (the 21 October `a435c97` read in
  `packing/campaign/intake-watch.yaml`).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
