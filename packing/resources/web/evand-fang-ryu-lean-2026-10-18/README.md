# Daniel’s Lean Proofs of Fang’s Theorems 1 and 2 and Ryu’s Bound, Pinned 2026-10-18

This packet pins two Lean formalizations that
[evand/square-packing](https://github.com/evand/square-packing) committed nine minutes
apart on 18 October 2026 (UTC), each of a construction this record holds from another
author:

- **Kevin Fang’s Theorems 1 and 2**, unconditional:
  $s(n^2 - n + 1) < n$ for every $n \ge 15$, and $n^2 - n + 1 + p + 2q$ squares in a
  side below $n$ whenever $16p + 21q \le n - 15$. The record holds them as `T-163`
  (`V2`/`C1`), tracked on GitHub by
  [jlevy/squares#603](https://github.com/jlevy/squares/issues/603); `f4883b41`, bead
  `think-57ei`.
- **Sungjoon Ryu’s Theorem 1.4**, $c^*(k) \le 8\lceil\sqrt{k - 4}\rceil - 1$ for every
  $k \ge 6$, where $c^*(k) = \max\{c : s(k^2 - c) = k\}$. The record holds it as a
  reported row of the asymptotic register, from issues #471 and #486, and not in the
  result register, since it settles no count $n \le 324$; `8475bdf4`, bead
  `think-ahr2`.

Its proposed Frontier key is **[Daniel Fang and Ryu Lean 2026-10-18]**. No issue asked
for either: the intake read of 18 October found both (`think-xmxb`). The two share their
library modules, Ryu’s geometry imports Fang’s gluing module, and `f4883b41` is the
parent of `8475bdf4`, so one packet at the later commit holds both. The claims below are
stated as the source states them; nothing here has built either proof, and no review has
read them yet.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/evand/square-packing> |
| Revision | `8475bdf41571c59c8c240aedaddc48e19e0e4707`, tree `89c618cbb17711033b6d9ca9ac70188f2dbb4389`: “Ryu’s c*(k) ≤ 8⌈√(k−4)⌉ − 1 (jlevy#471) in Lean, every k ≥ 6” |
| Its parent | `f4883b41853732b240606b3a532ce48d542ead28`, committed 2026-10-18T02:08:26Z: “Fang’s s(n² − n + 1) < n (jlevy#603) in Lean, unconditional”. Every file it adds for Fang’s theorems is unchanged at the pin; `git diff --stat f4883b41 8475bdf4` touches only `TODO.md`, `lean/Sqpack.lean`, the two Ryu modules and `tasks/fang-gluing/README.md` |
| Committed | 2026-10-18T02:17:40Z (20:17:40 on 17 October by the author’s clock, `-06:00`), by Evan Daniel |
| Licence | MIT, “Copyright (c) 2026 Evan Daniel” (`LICENSE`) |
| Retrieved | 2026-10-23T06:23Z, a blobless clone, head `7982d7a9`, with a sparse checkout of the pin |
| Pinned subtree | 46 files, 1,362,382 bytes, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) |
| Retained here | 25 files, 354,564 bytes, byte-identical under [`square-packing/`](square-packing/) |

## Credit and AI Assistance, as the Source States Them

`certificates/fang-gluing/README.md` credits the theorems to “Kevin Fang, *Packing
n² − n + 1 unit squares in a square of side less than n, for every n ≥ 15* (draft v0.6,
2026-10-13; `TheSnakeFang/squarepack-certs@078789a`; jlevy/squares#603, T-163), after
Arslanov, Mustafin and Shangitbayev (Electron. J. Combin. 28(4) P4.22, 2021), whose
decomposition is the gluing lemma”, and the formalization (“gluing lemma, induction,
checkers”) to the repository, 17 October 2026. It credits each piece’s packing and its
certificate: Kevin Fang’s two rectangles and nine direct packings, copied byte for byte
from `078789a`; David Ellsworth’s 110; Arslanov, Mustafin and Shangitbayev’s 132, 156
and 182; Joost de Winter’s 211; and David Ellsworth’s and Peter Stead’s 241 and 273,
with Daniel’s exact certificates of the last seven. `RyuBound.lean` and `RyuBand.lean`
credit Ryu’s *k² − c upper bounds* (squarepacker/k2-minus-c-upper v1.1). The task note
`tasks/fang-gluing/README.md` names T-163 and the credit line this record gives it.
`CREDITS.md` says the repository’s work was produced by Claude (Anthropic) under human
direction.

## What Is Retained

Retained byte-identical at their upstream paths, under `square-packing/`:

- **The theorem modules**: `lean/Sqpack/FangGlue.lean`, `FangTheorem.lean` and
  `FangFinal.lean` (Fang), and `RyuBand.lean` and `RyuBound.lean` (Ryu);
- **the rest of their closure** not retained elsewhere: `Conjectures.lean`,
  `ConjecturesProofs.lean`, and the checker modules the generated piece modules import,
  `ExactQuad.lean`, `ExactCheckCut.lean` and `ExactRect.lean`;
- **the root module** `lean/Sqpack.lean` and **the axiom probe** `lean/Axioms.lean`;
- **the pieces**: `certificates/fang-gluing/README.md`, its `SHA256SUMS`, and the seven
  certificates `inputs/P110.cert` to `P273.cert`, Daniel’s exact forms of the record’s
  packings;
- **the build recipe**: the generator `search/exact/fang_pieces.py`, its converter
  `search/exact/lean_cert.py` and `lean/scripts/build_chunks.sh`; and the task note
  `tasks/fang-gluing/README.md`, which records the measured costs.

Pinned by digest only, each byte-identical to a copy this repository already retains:

| Upstream path | Retained in |
| --- | --- |
| `certificates/fang-gluing/inputs/P308.cert`, `P343.cert` | [Fang two-wedge packet](../fang-two-wedge-certificates-2026-10-10/README.md), `n0308/`, `n0343/` |
| `inputs/P381.cert` to `P651.cert`, seven files | [Fang direct-certificates packet](../fang-direct-certificates-2026-10-13/README.md), `n0381/` to `n0651/` |
| `inputs/R257.cert`, `R443.cert` | [Fang excess-theorem packet](../fang-excess-theorem-2026-10-13/README.md), `rectangles/` |
| `lean/Sqpack/Spec.lean`, `ExactPack.lean`, `ExactCheck.lean`, `ShadowCheck.lean`, and `lean/lean-toolchain`, `lakefile.toml`, `lake-manifest.json` | [7 October evand packet](../evand-exact-and-local-reports-2026-10-07/README.md), under `source/s12/lean/` |
| `LICENSE`, `CREDITS.md` | [12 October evand exact-data packet](../evand-exact-data-2026-10-12/README.md) |
| `README.md` | [17 October evand n271 packet](../evand-n271-2026-10-17/README.md) |

[`acquisition/sources.json`](acquisition/sources.json) records each file, and from
`packing/`,
`uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-fang-ryu-lean-2026-10-18 --checkout CHECKOUT`
rebuilds the packet from a checkout at the pin; `--check` re-derives it without one.

**The closure.** [`receipts/lean-closure.json`](receipts/lean-closure.json), written by
`devtools.lean_closure` from the Git objects at the pin, follows every import from
`FangFinal`, `RyuBound` and the three checker modules: 14 project modules, 141,375
bytes, `Mathlib` the only import outside them, and no `sorry`, `axiom`, `native_decide`,
`implemented_by`, `extern`, `unsafe` or `debug.skipKernelTC` in their code. It lists as
missing the 18 piece modules `Sqpack.Exact.Fang.P110` to `R443`, which are generated
and gitignored. The build pins are `leanprover/lean4:v4.33.1` and Mathlib `0df444a3`,
those of the `s(13) = 4` and Bentz builds made here.

## The Claims, as the Source States Them

Both theorems state packings with `Packs` of `Spec.lean`, the repository’s common
specification: `Packs n s` holds when $n$ closed unit squares `unitSq (c i) (θ i)`, the
images of $[-1/2, 1/2]^2$ under a rotation and a translation, lie in
`container s = [0,s]²` with pairwise disjoint interiors.

**Fang’s theorems** (`FangFinal.lean`, namespace `UnitSquarePacking.FangGlue`):

```lean
theorem theorem1 (n : ℕ) (hn : 15 ≤ n) : ∃ s < (n : ℝ), Packs (n * n - n + 1) s
theorem theorem2 (n p q : ℕ) (hn : 15 ≤ n) (hpq : 16 * p + 21 * q ≤ n - 15) :
    ∃ s < (n : ℝ), Packs (n * n - n + (1 + p + 2 * q)) s
```

with “axioms propext / Classical.choice / Quot.sound only” (the pieces’ README). These
are `T-163`’s Theorem 1 and, with $F(n) = 1 + \max\{p + 2q : 16p + 21q \le n - 15\}$, its
Theorem 2, both for every $n \ge 15$ with no hypothesis. The proof: `FangGlue.glue` is
Fang’s Lemma 3 on `PacksIn` for any real $d \ge 0$; `FangTheorem.lean` defines
`Squeezable`, `Excess` and the `FangPieces` structure and proves its `theorem1` and
`theorem2` by induction on $n$; `FangFinal.lean` builds `fangPieces` from the 18
certificates, each checked by `decide +kernel` in a generated module: the rectangles
`R257` (257 squares in $17 \times 16$) and `R443` (443 in $22 \times 21$), the bases
$r^2 - r + 1$ in a side below $r$ for $r = 15$ to 26 (`P211` to `P651`, `P308` with one
square dropped), and $m^2 - m$ for $m = 11$ to 14 (`P110` to `P182`).

Fang’s own repository, read for `T-163` by `think-494l`, narrows its Lean statement on
19 October to “Theorem 1 and the unmixed bounds of Theorem 2”; this formalization is
another author’s, and states Theorem 2 in full.

**Ryu’s bound** (`RyuBound.lean`, namespace `UnitSquarePacking.Ryu`):

```lean
theorem packs_sub_8b (k b : ℕ) (hb : 2 ≤ b) (hkb : b + 4 ≤ k) (hk : k ≤ b ^ 2 + 4) :
    ∃ s < (k : ℝ), Packs (k * k - 8 * b) s
theorem packs_sub_8sqrt (k : ℕ) (hk : 6 ≤ k) :
    ∃ s < (k : ℝ), Packs (k * k - 8 * (Nat.sqrt (k - 5) + 1)) s
```

For $k \ge 6$, `Nat.sqrt (k - 5) + 1` is $\lceil\sqrt{k - 4}\rceil$, so $k^2 - 8b$ squares
pack in a side below $k$ and $c^*(k) \le 8\lceil\sqrt{k - 4}\rceil - 1$: Ryu’s Theorem
1.4. The commit message and the task note say “standard axioms, no certificates”:
`RyuBand.lean` proves the geometry of Ryu’s L-shaped packing (his Theorem 1.3, Lemmas
3.1 to 4.1) at any angle with $\cos\theta > 0$ and $\sin\theta \ge 0$, and
`RyuBound.lean` takes $R_1 = k - 4$ rows on the right and $R_2 = k - b - 4$ on top at the
angle $\theta = 2\arctan t$ with $t = 1/b + 1/((b^2 + 1)(6k + 4b))$, an explicit choice
that replaces Ryu’s mean-value argument (Lemma 4.2) and his $M = 14kb^2 + 1$.

## The Build Plan, Priced

From the retained files staged at `lean/`, with the piece modules generated by the
retained generator:

```sh
lake exe cache get
lake build Sqpack.RyuBound                                   # Ryu: no certificates
python3 search/exact/fang_pieces.py                          # -> lean/Sqpack/Exact/Fang/
for m in P110 P132 P156 P182 P211 P241 P273 P308 P343 P381 P421 P463 P507 P553 P601 P651 R257 R443; do
  lean/scripts/build_chunks.sh Sqpack.Exact.Fang.$m 1; done
lake build Sqpack.FangFinal
lake env lean AXIOMS.lean    # #print axioms for theorem1, theorem2, packs_sub_8sqrt
```

each accepted only with `propext`, `Classical.choice` and `Quot.sound`.

| Item | Ryu | Fang |
| --- | --- | --- |
| Toolchain | `leanprover/lean4:v4.33.1` and Mathlib `0df444a3`’s cache, about 10 GB of disk with the toolchain | the same, and Python 3 with mpmath for the generator |
| CPU | under 0.5 CPU-hours: seven modules, no certificates (an estimate from their size; the source reports no time) | about 1.5 to 3 CPU-hours: about 19 minutes wall at 8 chunks in parallel at the source, about 2.5 CPU-hours at most, and about a minute of generation (the task note) |
| Memory | a few GB for `import Mathlib` | at most about 8 GB per chunk with the sweep-line cut, so one chunk at a time fits a 15 GB host; a plain `lake build` of every chunk at once reached 120 of 125 GB at the source |

Both are under the owner’s 40 CPU-hour item cap; Ryu’s fits this lane’s 2 CPU-hour
single run and this host’s memory, and Fang’s is at or above it. Neither ran here: this
host had 5.2 GB of free disk on 23 October, short of the toolchain and Mathlib cache.
The import beads hold each as a validation item.

## Limitations

- **Nothing was built or run here.** The axiom sets are the source’s report; no build
  log or axiom output is published.
- **The piece modules are generated and gitignored.** A rebuild regenerates them; the
  kernel checks what the generator writes, so the generator is untrusted by design, and
  that each module encodes its retained certificate is the review’s to read.
- **No review has read either proof.** The mathematical review of stage 4 starts from
  this packet: it reads `Packs` against the record’s $s(n)$, the gluing lemma and the
  induction for Fang, and the band geometry and the length condition for Ryu.
- **Later Ryu work is not here.** `a645fe36`, `4b456fe1` and `13da782d` (17 and 18
  October) change `RyuBand.lean` and add the filled L-shape bound and Ryu’s
  $k^{2/5}$ bound in Lean; `think-f8py` and `think-pf37` hold them, each for a packet at
  its own revision. The other closure modules here are unchanged at those commits, so
  their packets can pin them as identical to this packet’s copies.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
