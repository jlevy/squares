# chelokot’s Lean Proofs of s(2) to s(5), Pinned 2026-09-05

This packet retains the Lean proofs of $s(2) = s(3) = s(4) = 2$ and
$s(5) = 2 + \sqrt{2}/2$ in chelokot’s
[square-packing-archive](https://github.com/chelokot/square-packing-archive), at
`753079eb`, the commit this repository already pins for `T-086` and built in full on 2
October 2026. The values are classical (Göbel 1979; Friedman’s survey DS7) and the record
holds them by published proofs; these are machine routes to them, and of the reports this
record holds, the first in a proof assistant. Evan Daniel’s later Lean route to the same
values is in the [21 October rectangle packet](../evand-rect-small-n-lean-2026-10-22/README.md).

Its proposed Frontier key is **[chelokot small-n Lean 2026-09-05]**. No issue asked for
it: the triage of 22 October found it from Daniel’s literature note, which points to
chelokot’s `s5_eq_goebel`, and bead `think-7l2j` owns its import. The claims below are
stated as the source states them. Nothing was built for this packet; what the build of 2
October logged for these theorems is in [Checks Made Here](#checks-made-here).

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/chelokot/square-packing-archive> |
| Revision | `753079eb37d8d16225a5dc1f56e493a3c3b243f4`, tree `45c9761da5ee4f963f4b003fb4b1dfd36f3dafc6`, the pin of the [Nagamochi-counterexample packet](../chelokot-nagamochi-counterexample-2026-09-05/README.md) of the same date, and of `T-086`’s replay |
| Committed | 2026-09-05T21:42:12Z (00:42:12 on 6 September by the author’s clock, `+03:00`) |
| The theorems’ commits | `s4_eq_two` at `32e110f` (2026-08-16T19:29:10Z); `s2_eq_two` and `s3_eq_two` at `74ce49f` (2026-08-16T19:40:17Z); `s5_le_goebel` at `0757329` (2026-08-29T14:27:23Z); `s5_ge_goebel` and `s5_eq_goebel` at `4f4ece12` (2026-08-29T18:39:38Z) |
| Licence | Apache-2.0 for code and Lean sources (`LICENSE`, with `NOTICE`); CC BY 4.0 for archive data (`LICENSE-DATA`, retained by the Nagamochi-counterexample packet) |
| Retrieved | 2026-10-23T06:23Z, a blobless clone, head `e1e9ef5d` (7 October), with a sparse checkout of the pin |
| Pinned subtree | 19 files, 296,078 bytes, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) |
| Retained here | 18 files, 295,350 bytes, byte-identical under [`square-packing-archive/`](square-packing-archive/) |

**After the pin.** The 34 commits from `753079eb` to the head `e1e9ef5d` (4 to 7
October) prove $s(1)$ to $s(9)$ in Bend as well, $s(5)$ among them (`9309180`, merged
in PR #33), and at `878596b` move proofs of $s(1)$ to $s(4)$ and $s(6)$ to $s(9)$ to
Bend: `formal/` loses 1,736 lines, `s4_eq_two` with them (from `Records/SquareNumbers.lean`)
and the six-square modules. `Records/Square5.lean` and `Records/NearSquare.lean` have the
same blobs at the head, so `s2_eq_two`, `s3_eq_two` and `s5_eq_goebel` are still in Lean
there. The Lean proof of $s(4) = 2$ is at this pin and not at the head, which is one
reason the pin is `753079eb`; the other is that this repository built it.

## Credit and AI Assistance, as the Source States Them

`ATTRIBUTION.md` at the pin credits “**chelokot:** project creator, concept, and product
direction” and “**GPT 6 Astra:** AI-produced research, packing optimizations, and Lean
formalizations credited under this name in the archive”, and says: “Formalizing or
reconstructing a published result does not transfer its discovery credit: the original
discoverer, optimizer, and prover keep their respective roles.” `NOTICE` credits the
historical catalogue to Erich Friedman’s survey and David Ellsworth’s tracker. The $s(5)$
lower bound is Friedman’s four-point unavoidable set, as
`docs/friedman-unavoidable-formalization.md` says; the value is Göbel’s.

## What Is Retained

Retained byte-identical at their upstream paths, under `square-packing-archive/`:

- **The theorem modules** `formal/SquarePackingArchive/Records/Square5.lean`,
  `Records/NearSquare.lean` and `Records/SquareNumbers.lean`, and the rest of their
  import closure: `Geometry.lean` (the definitions), `Area.lean`, `Triangle.lean`,
  `Unavoidable.lean` and `Friedman.lean`;
- **the root module** `formal/SquarePackingArchive.lean` and **the archive’s axiom
  probe** `formal/SquarePackingArchive/Audit.lean`, which imports the whole library;
- **the build pins** `formal/lean-toolchain` (`leanprover/lean4:v4.33.0`),
  `lakefile.toml` and `lake-manifest.json` (Mathlib `db584cd6`);
- **the two formalization notes** `docs/friedman-unavoidable-formalization.md` and
  `docs/small-records-formalization.md`; and `LICENSE`, `ATTRIBUTION.md` and the root
  `README.md`.

`NOTICE` is pinned by digest and byte-identical in the Nagamochi-counterexample packet.
[`acquisition/sources.json`](acquisition/sources.json) records each file, and from
`packing/`,
`uv run --frozen --all-extras --group dev python -m devtools.acquire_source chelokot-small-n-lean-2026-09-05 --checkout CHECKOUT`
rebuilds the packet; `--check` re-derives it without a checkout.

[`receipts/lean-closure.json`](receipts/lean-closure.json), written by
`devtools.lean_closure`, is the import closure of the three theorem modules at the pin:
eight project modules, 229,645 bytes, eleven imports of `Mathlib` modules outside them,
no generated module, and no `sorry`, `axiom`, `native_decide` or other kernel escape in
their code.

This packet also closes, for these theorems, a departure the Nagamochi-counterexample
packet records: that packet retained the archive’s note only and pinned the Lean
development by commit, and `T-086`’s replay cloned it.

## The Claims, as the Source States Them

`Geometry.lean` defines a `Packing n side` as $n$ placed squares, each a centre and a
frame (cosine and sine with $\cos^2 + \sin^2 = 1$), that fit in the closed square
$[0, \mathit{side}]^2$ and are pairwise interior-disjoint; then

```lean
def HasPacking (squareCount : ℕ) (side : ℝ) : Prop := Nonempty (Packing squareCount side)
def IsLowerBound (squareCount : ℕ) (side : ℝ) : Prop :=
  ∀ candidateSide, HasPacking squareCount candidateSide → side ≤ candidateSide
def IsMinimumSide (squareCount : ℕ) (side : ℝ) : Prop :=
  HasPacking squareCount side ∧ IsLowerBound squareCount side
```

and the theorems, in namespace `SquarePackingArchive.Records`:

```lean
theorem SquareNumbers.s4_eq_two : IsMinimumSide 4 2
theorem NearSquare.s2_eq_two : IsMinimumSide 2 2
theorem NearSquare.s3_eq_two : IsMinimumSide 3 2
theorem Square5.s5_le_goebel : HasPacking 5 (2 + Real.sqrt 2 / 2)
theorem Square5.unavoidable_points : Unavoidable unavoidablePoints side
theorem Square5.s5_ge_goebel : IsLowerBound 5 (2 + Real.sqrt 2 / 2)
theorem Square5.s5_eq_goebel : IsMinimumSide 5 (2 + Real.sqrt 2 / 2)
```

`s5_le_goebel` is Göbel’s packing: four axis-parallel squares in the corners and one at
45° in the centre, in a side $2 + d$ with $d = \sqrt{2}/2$. `s5_ge_goebel` applies
`lowerBound_succ_of_unavoidable` to the four points $(1, 1)$, $(1, 1 + d)$, $(1 + d, 1)$
and $(1 + d, 1 + d)$, which every closed unit square in $[0, 2 + d]^2$ contains one of
(`unavoidable_points`, by the centre’s cell: corner, side strip, or one of two triangles
of the central cell). `IsMinimumSide n s` is the record’s $s(n) = s$ with the minimum
attained: `T-086`’s replay read these definitions for `IsMinimumSide`, and Evan Daniel’s
`SpecChelokot` proves it equivalent to his `minSide n = s` for every $n \ge 1$, which the
[4 October evand packet](../evand-square-packing-2026-10-04/README.md) retains.

## Checks Made Here

Nothing was built for this packet. The full build of this commit that this repository
made on 2 October 2026 for `T-086`
([`receipt.json`](../../../campaign/series/series-000-smoke-and-calibration/results/chelokot-lean-replay/receipt.json)
and its `build.log`, by `devtools.replay_chelokot_lean`) built every module from source
over Mathlib’s cache: an uninterrupted build ran 2,920 of its 2,944 jobs, a first run of
the tool finished the other 24, and the receipted run rebuilt four modules on that tree,
`Audit.lean` among them. Its `build.log` records `Audit.lean`’s output for all seven
theorems above:

```text
'SquarePackingArchive.Records.SquareNumbers.s4_eq_two' depends on axioms: [propext, Classical.choice, Quot.sound]
'SquarePackingArchive.Records.NearSquare.s2_eq_two' depends on axioms: [propext, Classical.choice, Quot.sound]
'SquarePackingArchive.Records.NearSquare.s3_eq_two' depends on axioms: [propext, Classical.choice, Quot.sound]
'SquarePackingArchive.Records.Square5.s5_le_goebel' depends on axioms: [propext, Classical.choice, Quot.sound]
'SquarePackingArchive.Records.Square5.unavoidable_points' depends on axioms: [propext, Classical.choice, Quot.sound]
'SquarePackingArchive.Records.Square5.s5_ge_goebel' depends on axioms: [propext, Classical.choice, Quot.sound]
'SquarePackingArchive.Records.Square5.s5_eq_goebel' depends on axioms: [propext, Classical.choice, Quot.sound]
```

(`build.log` lines 330 and 338 to 343). The receipt names only `T-086`’s theorem and two
file blobs, and the modules these theorems live in were compiled in the uninterrupted
build before it, whose log is not retained; its source scan found no `sorry`, `axiom`
declaration or `native_decide` in any of the 277 `.lean` files. So the axioms of these
theorems were printed here from oleans built here at this commit, and no receipt yet
binds them.

## The Build Plan, Priced

A receipt-bound rebuild of the three theorem modules with their axioms printed, from
this packet’s retained bytes rather than a clone: `lake exe cache get`, then
`lake build SquarePackingArchive.Records.Square5 SquarePackingArchive.Records.NearSquare SquarePackingArchive.Records.SquareNumbers`
and a probe that prints the seven theorems’ axioms, accepted only with the three standard
axioms. It is eight modules over Mathlib `db584cd6`’s cache (Lean v4.33.0): minutes, under
0.5 CPU-hours, a few GB of memory, and about 10 GB of disk for the toolchain and cache,
which this host lacked on 23 October (5.2 GB free). The import bead holds it as a
validation item. Its toolchain differs from Daniel’s rectangle proofs’ (v4.33.1, Mathlib
`0df444a3`), so the two routes need two caches.

## Limitations

- **The build of 2 October is not a receipt for these theorems.** It logged their axioms;
  a rebuild under a receipt that names them is what would make it one.
- **No review has read these proofs for this record.** The mathematical review of stage
  4 starts from this packet: the four-point lemma, the side and centre cases, and
  `lowerBound_succ_of_unavoidable`.
- **The Bend proofs after the pin are not retained.** They are a second proof checker’s
  routes to the same values; a bead of their own holds them.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
