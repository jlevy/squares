# Stage 4 Review: Hosono’s Lean Kernel Proof of ValidTilt9

**Date:** 2026-10-26. **Lane:** the mathematical review of
[stage 4](../../../packing/campaign/result-import.md#stage-4-validate) of the result
import runbook for `T-251`, Hiroaki Hosono’s (wand125’s) Lean 4 proof of Evan Daniel’s
`ValidTilt9` and, with Daniel’s reduction, of $s(k^2 - 4) = k$ for every $k \ge 8$
(issue [#643](https://github.com/jlevy/squares/issues/643); import bead `think-jh0n`,
review bead `think-90po`). **Reviewer:** Claude (AI), strong tier (`tbd-strong`, acting
name `w-643-1026`), at the reasoning setting the coordinator launched it with, in a
worktree of its own.

It read the retained packet
[`wand125-validtilt9-lean-2026-10-16`](../../../packing/resources/web/wand125-validtilt9-lean-2026-10-16/README.md)
at wand125/square-packing `319a779`, the 50 machinery modules that packet’s list shares
with the
[Valid7 packet](../../../packing/resources/web/evand-valid7-lean-2026-10-11/README.md),
and the 16 statement modules of the
[3 October evand packet](../../../packing/resources/web/evand-square-packing-2026-10-03/README.md).
It read the source as data, ran no code from it, built nothing and downloaded none of
the release `validtilt9-lean-v1`’s three assets.
Before writing it had read `T-251`’s and `T-081`’s register entries, the packet README,
the evidence entry `E-k2m4-wand125-validtilt9-lean-report` and the 16 October triage in
`think-jh0n`. No earlier review of this formalization exists.
The two reviews of `T-081`, of 3 and 6 October, were read only after §1–§8 were written,
for §9.

It is not a replay, and it is not the human expert formalization review that `V5` needs.

**In one line:** `SquarePacking.LemmaELeaf.bentz4 : ∀ k : ℕ, 8 ≤ k → minSide (k ^ 2 - 4)
= k` states this record’s $s(k^2 - 4) = k$ for every $k \ge 8$ with no hypothesis, over
closed unit squares with arbitrary independent rotations, disjoint interiors and
boundary contact allowed; every definition its statement and those of `validTilt9` and
`valid9` use lies in the 16-module closure of `ValidSplit9.lean`, which this record
built itself on 3 October; the hand-written new code (`Tilt.lean`, `Bridge.lean`,
`RowMinN.lean`, the four hunks of `LemmaEKM.lean`) is correct as mathematics and holds
no kernel escape; and the 1,275,911 generated modules that carry the computation are not
stored, so their kernel check is the source’s report, of which only the assembly and the
axiom printout are retained here.

**Verdict: accepted.** No blocking defect and no mathematical defect.
One major finding (M-1) binds how the result is described: nothing here has seen an
execution record of the module checks.
Three minor findings and five notes follow (§8).

## Summary for the Author

- **The statement is faithful.** `minSide n = sInf {s | Packs n s}`, where `Packs n s`
  places `n` closed unit squares, each at its own centre and angle, inside the closed
  `[0, s]²` with pairwise disjoint open interiors.
  That is $s(n)$ as this record defines it, and `bentz4` has no premise.
- **Every statement definition is Daniel’s and the record’s.** The three theorems are
  stated in the import closure of `ValidSplit9.lean`: 16 modules plus Mathlib, each
  byte-identical to the copy this repository built on 3 October with its axiom receipt.
- **The glue is right.** `validTilt_of_tree` turns a `CovT` root over
  `[0, 9/2]² × (0, 1/2]` into `ValidTilt 9` of the mixed cover, and
  `box9Cover_eq_mcoverP` identifies that cover with `Bentz4.box9Cover` term by term
  (§3). `Main.lean` uses each of the 16,200 roots once, with 16,199 splits on the 45 ×
  45 × 8 grid.
- **`rmChk_sound` is a sound reflection lemma.** The natural-number digit loop is the
  balanced-digit loop of `RowMinK` shifted by `maskR K L`, and the `LemmaEKM` change
  only strengthens a check that appears as a hypothesis (§5).
- **No kernel escape** in the 56 modules of `library.sha256`, in `Main.lean`, in
  `Axioms9.lean`, in the emitter’s templates or on the driver’s `lean -o` command line.
- **What a reader cannot check from the published files** is the execution of the
  1,275,911 module checks (M-1): the per-module log is in the logs asset, the sources
  are not stored, and the axiom printout cannot see a declaration added without a kernel
  check or a name shadowed in `Main.lean`’s statements (m-1). Loading the certificates
  means unpickling them (m-2).

## 1. What Was Read

Paths are relative to the packet’s
`square-packing/problems/square-lower-bounds/certificates/k2m4_n77_L9/lean/` unless they
name another packet.

| Depth | Files |
| --- | --- |
| Read in full | `README.md`, `ENVIRONMENT.md`, `Sqpack/V9/Bridge.lean`, `Sqpack/V9/Tilt.lean`, `Sqpack/V9/Data.lean` (structure, and its segment lists counted), `Axioms9.lean`, `library/Sqpack/RowMinN.lean`, `library/LemmaEKM.diff`, the four hunks of `library/Sqpack/LemmaEKM.lean` and its `rowOkM` and the soundness step that uses it, `receipts/main.log`, `main_try1.log`, `sha256_final.txt`, `ASSETS.sha256`, `MANUAL.tsv`, `SANITIZE.sha256`, both `manual_machine*.log`, `scripts_manual/emit_v7.py`, `scripts_manual/gen_main9.py`, `scripts/gen_tree.py`, the header and Lean invocations of `driver/run9.py`; from the 3 October packet, `ValidSplit9.lean` and its build’s `receipts/lean/axioms_bentz4.log`; from the Valid7 packet, `Bentz4.lean`, the definitions in `Basic.lean`, `Chord.lean` and `S32.lean`, `ValidTilt`, `ValidAxis` and `valid_of_tilt_axis` in `ValidSplit.lean`, `CovT` and its split, clip, scale and leaf lemmas in `ExTree.lean` and `ExTreeX.lean`, `rectSet`, `rectMass` and `mcoverP` in `CovMP.lean`, `segMass` in `CovM.lean`, `segNorm` and `STree` in `SegTree.lean`, `MixedCover` and its `measure` in `MixedMeasure.lean`, `fileCover` in `BentzFam.lean` |
| Read in part | `Sqpack/V9/Main.lean`: its 16,202 import lines by count, the final block (lines 16,203–16,235) in full, the 479,730-character `v9_tree` term by its split points and root names; `scripts_manual/run_v7.py` (lines 1–120) |
| Scanned | the six closure modules outside the Valid7 packet’s closure receipt, `Main.lean`, `Axioms9.lean`, and the emitters `emit_v7.py`, `gen_exact.py`, `capk.py`, `gen_tree.py`, `enc_cert.py` and `gen_main9.py` in both script directories, for the kernel-escape tokens of §6 |
| Not read | the soundness proofs of the leaf checkers (`LemmaE*`, `CapK`, `ZMTree*`, `KArith`, `RowMinK`, `LBlock*`, `Leb*`, `CovM*` and the rest of the 50 shared machinery modules) beyond the statements named above; `gen_exact.py`, `capk.py`, `tree_rebuild.py` and the other generators beyond the scan; the release assets, not downloaded; the 1,275,911 generated modules, which are not stored |

Words used below: *kernel-checked by the source* means the source’s text proves it and
its axiom printout is consistent with that, and nothing here compiled it.
*Built here* means compiled in this repository, which applies only to the closure of
`ValidSplit9.lean` (`E-k2m4-evand-bentz4-lean-build`, 3 October).

## 2. Statement Fidelity

The final block of `Sqpack/V9/Main.lean` (lines 16,212–16,235), in namespace
`SquarePacking.LemmaELeaf` with `ZMTreeM` and `ZMTree` open:

```lean
theorem validTilt9 : Bentz4.ValidTilt9 := by
  have h := validTilt_of_tree 5 128 45 4722366482869645213696 2361183241434822606848 2000000000000 PTree.leaf segsT trects
    (by decide) (by decide) (by decide) (by decide) (by rw [segsT_toList]; exact v9_tree) (by decide)
  unfold Bentz4.ValidTilt9
  rw [box9Cover_eq_mcoverP]
  convert h using 1
  norm_num
theorem valid9 : Bentz4.Valid9 := Bentz4.valid9_of_tilt validTilt9
theorem bentz4 : ∀ k : ℕ, 8 ≤ k → minSide (k ^ 2 - 4) = k := Bentz4.bentz4_of_validTilt9 validTilt9
```

**The definitions `bentz4` uses.** `S32.lean` lines 34–39, `Basic.lean` lines 28–38 and
`Chord.lean` line 28:

```lean
def Packs (n : ℕ) (s : ℝ) : Prop :=
  ∃ (ctr : Fin n → ℝ × ℝ) (ang : Fin n → ℝ), (∀ i, sq (ctr i) (ang i) 1 ⊆ box s) ∧
    ∀ i j, i ≠ j → Disjoint (sqInt (ctr i) (ang i) 1) (sqInt (ctr j) (ang j) 1)
noncomputable def minSide (n : ℕ) : ℝ := sInf {s | Packs n s}
-- coord c θ p rotates p − c by −θ; sq c θ L = {p | |(coord c θ p).1| ≤ L/2 ∧ |(coord c θ p).2| ≤ L/2}
-- sqInt is the same with <; box t = {p | 0 ≤ p.1 ∧ p.1 ≤ t ∧ 0 ≤ p.2 ∧ p.2 ≤ t}
```

Read against the record’s $s(n)$:

- Each square is closed, of side one, at an arbitrary centre and an arbitrary real
  angle, independently of the others.
  Boundary contact, with the wall and between squares, is allowed; only open interiors
  must be disjoint. There is no wrong quantifier, no symmetry restriction and no
  open-closed slip.
- `minSide` is Mathlib’s `sInf` on ℝ, which returns 0 for an empty set or one unbounded
  below. The set is bounded below by 0 (a unit square in `box s` needs $s \ge 1$) and
  nonempty (the grid), and the theorem’s value $k \ge 8$ is not 0, so the equation
  states the true infimum.
  It excludes every packing at a side below $k$, and since `Packs (k² − 4) k` holds by
  the grid (`packs_grid`, used inside `minSide_eq`), the infimum is attained:
  $s(k^2 - 4) = k$ with both halves.
- `k ^ 2 - 4` is natural subtraction, which truncates nothing for $k \ge 8$.

**The definitions `validTilt9` and `valid9` use.** `Bentz4.ValidTilt9` is
`ValidSplit.ValidTilt 9 Bentz4.box9Cover.measure`: every closed unit square with centre
in `[0, 9/2]²` and angle `2 arctan u`, `0 < u`, `u² + 2u ≤ 1` (so $0 < \theta \le 45°$),
inside `[0, 9]²`, has mass at least one under the box cover.
`Bentz4.Valid9` is the same for every centre and angle.
`box9Cover` is `fileCover 2·10¹² boxSegs boxPolyVerts
boxPolyW`, the file `K4_k008_box9.txt` as `Bentz4Data.lean` transcribes it: 2,076
segments indexed by position, and the polygon `[14/5, 31/5]²` with mass
23,120,000,000,000/(2·10¹²) = 289/25, its area, so density one.

**Where the statements live.** Every constant in the three statements is defined in the
import closure of `ValidSplit9.lean`: `ValidSplit9`, `ValidSplit`, `ValidSplitData`,
`Bentz4`, `Bentz4Data`, `BentzFam`, `Bentz`, `BentzData`, `MixedMeasure`, `S32`,
`S32Data`, `Cover`, `D4`, `ZeroMargin`, `Chord` and `Basic`, 16 modules over Mathlib.
Checked here with `sha256sum --check` against `library/library.sha256`, all 16 and the
three build pins are byte-identical to the 3 October packet’s copies, which this record
built on 3 October (`E-k2m4-evand-bentz4-lean-build`); that build’s
`receipts/lean/axioms_bentz4.log` prints the elaborated statements with full names:

```text
SquarePacking.Bentz4.bentz4_of_validTilt9 : SquarePacking.Bentz4.ValidTilt9 →
  ∀ (k : ℕ), 8 ≤ k → SquarePacking.minSide (k ^ 2 - 4) = ↑k
```

The same `sha256sum --check` against the Valid7 packet finds 53 of the 59 entries
identical; the other six are `ValidSplit9.lean` (the 3 October packet’s) and
`LemmaEKM.lean`, `RowMinN.lean` and `V9/{Bridge,Data,Tilt}.lean` (this packet’s).
`minSide`, `Packs`, `box`, `sq`, `sqInt`, `coord`, `Valid9` and `ValidTilt9` each have
one definition in the 56 modules.

So `bentz4`’s statement says what `T-081` claims at $k \ge 8$, and what `T-251`’s claim
and scope say: the cases this record holds are $k = 8$ to 18, $n = 60$ to 320. It says
nothing at $k = 5, 6, 7$, which `T-081` holds by other certificates.
`bentz4`’s truth does not depend on the cover at all; the cover enters only the
statements of `validTilt9` and `valid9`, and through them the proof.

## 3. From the Roots to `bentz4`

**`Main.lean`.** It imports `Sqpack.V9.Tilt`, `Sqpack.V9.Bridge` and `Sqpack.V9.R00000`
to `R16199`, each once.
`v9_tree`’s term names each `root_00000` to `root_16199` exactly once, under 16,199
split nodes, as a binary tree with 16,200 leaves needs: 7 `CovT.splitU` at the multiples
of $2^{68}$ (with $R = 2^{72}$, angle cells of $1/16$ in $u \in (0, 1/2]$), and 6,208
`CovT.splitX` and 9,984 `CovT.splitY` at the multiples of 64 (over $D \cdot S = 640$,
centre cells of $1/10$ in $[0, 9/2]$). That is the 45 × 45 × 8 grid of `qxzm_full`’s
roots, as `gen_main9.py` asserts.
Its type is

```lean
CovT 5 128 45 4722366482869645213696 2000000000000 [] tsegs trects 0 2880 0 2880 0 2361183241434822606848
```

**`CovT`** (`ExTree.lean` lines 32–40) is a plain proposition: every closed unit square
with centre in `[x0, x1] × [y0, y1]` over $D S$, `u0/R < u ≤ u1/R`, `u² + 2u ≤ 1`,
inside `box (Mq/D)`, captures point, segment and rectangle mass at least `W`. `splitX`,
`splitY` and `splitU` are proved by cases on the split coordinate, so the kernel accepts
`v9_tree` only if the leaves’ boxes tile the root exactly.

**`Tilt.lean`, `validTilt_of_tree`,** re-derived.
Let $m = M_q/D$ and $\mu$ the measure of `mcoverP D W pts segs rects`. For a square with
centre $c \in [0, m/2]^2$, $u > 0$, $u^2 + 2u \le 1$ and inside `box m`:

1. The measure of a measurable set is $\mathrm{ofReal}((\text{pt} + \text{seg} +
   \text{rect mass})/W)$ (`hmass`, from `MixedCover.measure_apply` and `gw_areaFrac`,
   which turns the polygon weight $\rho \cdot |R|/W$ times the area fraction into
   $\rho |Q \cap R| / W$), and the cover is nonnegative.
2. $m/2 \le (M_q S - \lfloor M_q S/2 \rfloor)/(D S)$, since $M_q S \le 2(M_q S - \lfloor
   M_q S / 2 \rfloor)$; here $5760 - 2880 = 2880$ and $2880/640 = 9/2$, so the bound is
   equality.
3. $u^2 + 2u \le 1$ and $u > 0$ give $u \le 1/2$, and $R \le 2 U_m$ gives $u \le U_m/R$
   (here $R = 2 U_m$).
4. The root `CovT` then gives $W \le$ mass, so the mass over $W$ is at least one.

That is `ValidTilt (Mq/D) μ` with nothing assumed; its hypotheses `0 < D`, `0 < S`,
`0 < R`, `R ≤ 2·Um` and `0 < W` are decided for the constants in `Main.lean`.
`convert h using 1; norm_num` closes the remaining `9 = 45/5`. The angle convention,
`2 * Real.arctan u`, is the same in `CovT` and `ValidTilt`, and roots past $45°$
($u > \sqrt 2 - 1$) hold vacuously by the `u² + 2u ≤ 1` hypothesis.

**`Bridge.lean`, `box9Cover_eq_mcoverP`,** re-derived.
Both measures are sums of points, segments and polygons (`MixedCover.measure`).

- Points: both empty.
- Segments: `box9Cover` sums over `Fin boxSegs.length` and `mcoverP` over the finset of
  `segsT.toList`, which is `tsegs` (`segsT_toList`, kernel).
  The map $j \mapsto \mathrm{segNorm}(\mathrm{boxSegs}_j)$, which orders a segment’s
  endpoints lexicographically and keeps its weight, is injective (`boxSegs_norm_nodup`)
  and onto `tsegs` (`boxSegs_norm_sub`, `tsegs_sub`), all decided in the kernel; each
  term agrees because `segMeasure` is symmetric in its endpoints (`segMeasure_segNorm`)
  and both weights are $w/(2 \cdot 10^{12})$. The injectivity matters: `mcoverP` takes a
  finset, so two file entries normalizing to the same tuple would merge, and `Nodup`
  excludes that. The file lists 16 unit pieces twice, each time with a different weight
  (a reading of `Bentz4Data.lean` with `awk`, which decides nothing: the kernel decides
  `Nodup`), so both copies survive in the finset, as `fileCover`, indexed by position,
  counts both. I counted 2,076 tuples in `tsegs`, in `segsT` and in `boxSegs`.
- Polygon: `convPoly 5 boxPolyVerts` is `rectSet 5 (14, 14, 31, 31, ·)`, the square
  `[14/5, 31/5]²`, and both weights are $289/25$.

So `ValidTilt9` follows from `v9_tree` with nothing assumed, given the kernel’s check of
the roots. `valid9_of_tilt` and `bentz4_of_validTilt9` are Daniel’s, in
`ValidSplit9.lean`, and are built here: the D4 reduction, Lemma Z in Lean (`axis9`) and
the family’s accounting (`famCover_total4`, $\mu_k([0,k]^2) = k^2 - 4D$ with $4D > 4$).

## 4. The Leaves

The root theorems are not retained, but their shape is fixed by `scripts/gen_tree.py`:
each is a term of the library lemmas `CovT.splitX/Y/U`, `CovT.clip`, `CovT.of_degen`,
`of_empty`, `of_sym`, `of_top_zero`, `of_leb`, `of_cap`, `of_exact`, `of_exactX`,
`scaleS'` and `scaleR'`, with side conditions closed by `decide` and leaf facts
`name_ok : exOk … = true` (or `exOkX`, `capOk`) closed by `decide +kernel` in the leaf
and row-group modules.
Each lemma is a theorem of `ExTree.lean` or `ExTreeX.lean` whose conclusion is `CovT`
and whose hypotheses are Boolean checks; I read their statements and the proofs of the
splits, `clip`, `of_degen`, `of_sym`, `of_top_zero` and the scalings.
The proofs of `CovMPo.of_exact(X)`, `CapK.capOk_sound` and the vertex tests they rest on
were not read (§1); they are upstream’s, byte-identical to the Valid7 packet, and
kernel-checked by the source.

The driver emits with `V7_X=1` (`run9.py` line 188), so the EXACT leaves go through
`LemmaELeafX.exOkX` and `LemmaEK.vertOkM`, whose rows test is `rowOkM`, the function the
`LemmaEKM` change touches.
The change is therefore on the path of most leaves.

The certificates are data.
`run_v7.py` rebuilds each root’s pose tree from Daniel’s `qxzm_full` leaf record
(`run_k4x_k008_leaves.jsonl.gz`) and the cover file, writes exact certificates for its
EXACT-type leaves with `gen_exact.py`, and splits a leaf further where one fails.
Nine roots were finished by hand (`receipts/MANUAL.tsv`), four of them with new
generator options (`V7_TOUCH`, `V7_SGK`) from `scripts_manual/`; the `V7_SGK` roots are
glued at the finer grid and moved back by `CovT.scaleS`. None of this can make a false
root theorem pass: a wrong certificate fails its kernel check.

## 5. `RowMinN.lean` and the `LemmaEKM` Change

`rmLoop K ε L rows fx` (`RowMinK`) checks, digit by digit over $L$ digits of base $2^K$,
that the sum over the rows of each row’s minimum of $\varepsilon \cdot
\mathrm{balD}_K(v)$, plus the sum of $\varepsilon \cdot \mathrm{balD}_K(v)$ over the
fixed terms, is nonnegative, then shifts every value by `shiftD K`. In a kernel
evaluation the shifted integers stay unevaluated, which is the cost `RowMinN` removes.

`rmChk` first requires $\varepsilon = \pm 1$ and $v + H \ge 0$ for every value, with
$H = \mathrm{maskR}_K(L)$, the number whose $L$ base-$2^K$ digits are each $2^{K-1}$. It
then runs `rmLoopN` on the naturals $w = v + H$, taking each digit as `w &&& (2^K − 1)`
(or $2^K$ minus it when $\varepsilon = -1$) and shifting by `>>> K`. Re-derived:

- **`digit_step`.** If $w = v + \mathrm{maskR}_K(m+1)$, write $w = r + 2^K q$ with
  $0 \le
  r < 2^K$. Since $\mathrm{maskR}_K(m+1) = 2^{K-1} + 2^K \mathrm{maskR}_K(m)$,
  $v = (r - 2^{K-1}) + 2^K (q - \mathrm{maskR}_K(m))$ with $-2^{K-1} \le r - 2^{K-1} <
  2^{K-1}$, so the balanced digit of $v$ is $r - 2^{K-1}$ and its shift is $q -
  \mathrm{maskR}_K(m)$ (`balD_shiftD'`). The invariant $w = v + \mathrm{maskR}_K(\cdot)$
  passes to the next digit.
- **`digN_eq`.** $\pm \mathrm{balD}_K(v) = \mathrm{digN} - 2^{K-1}$, with $\mathrm{digN}
  = 2^K - r$ for the negative sign, which needs $r \le 2^K$, as it is.
- **`minL_eq`, `sum_eq`.** A row’s minimum of $\mathrm{digN} - 2^{K-1}$ is its minimum
  of `digN` less $2^{K-1}$ (both empty cases give 0), and a sum of $\ell$ such terms is
  the sum of `digN` less $\ell \cdot 2^{K-1}$.
- **`rmLoopN_sound`.** So the integer test $0 \le \sum$ is the natural test
  $\mathrm{cnt} \cdot 2^{K-1} \le \sum \mathrm{minN} + \sum \mathrm{digN}$ with
  $\mathrm{cnt}$ the number of rows and fixed terms, which `rmLoopN` checks with
  `Nat.ble`; by induction on $L$ every digit passes.

`rmChk_sound : rmChk K ε L rows fx = true → rmLoop K ε L rows fx = true` (for `0 < K`)
follows. It is one-directional, which is all that is needed: a passing natural loop
implies the passing integer loop, and `rmLoop_sound` does the rest unchanged.

`LemmaEKM.lean` differs from `060c1a1`’s by exactly the four hunks of
`library/LemmaEKM.diff`: the import, a doc sentence, `rmChk` in place of `rmLoop` in
`rowOkM`’s Boolean test, and `rmLoop_sound … (rmChk_sound hK hloop)` in the soundness
proof. The *definition* `rowOkM` changes, which the source’s “no statement change” does
not say (N-1), but `rowOkM` appears only in hypotheses of the form `rowOkM … = true`;
`rowOkM_sound`’s conclusion is unchanged, and no final statement mentions it.
A changed check can make a leaf fail; it cannot make a false leaf pass.

## 6. Axioms and the Trust Boundary

`receipts/main.log` reports Lean 4.33.1 (aarch64, commit `819816b2e0a3…`) building
`Main.lean` (SHA-256 `39f42605…`, the retained file’s) in 584 s at 230,597,216 kB, and
`Axioms9.lean` (`9bfeda36…`, the retained file’s) printing `[propext, Classical.choice,
Quot.sound]` for all three theorems.
A `native_decide` or `decide +native` anywhere in the proof would add
`Lean.ofReduceBool`, and a `sorry` would add `sorryAx`; neither appears.
`main_try1.log` is the earlier attempt that failed on `vm.max_map_count`, as the README
says, with the same two digests.

The escape scan, by token, of `devtools.lean_closure.ESCAPES` (`sorry`, `axiom`,
`native_decide`, `ofReduceBool`, `implemented_by`, `@[extern`, `debug.skipKernelTC`,
`unsafe`, `+native`, `native := true`, `reduceBool`/`reduceNat`, `trustCompiler`) plus
`admit`, `opaque`, `#eval`, `run_cmd`, `elab` and `initialize`:

- the 50 shared modules: none, by the Valid7 packet’s `receipts/lean-closure.json`,
  which counts every module of that closure with comments removed;
- `ValidSplit9.lean`, `LemmaEKM.lean`, `RowMinN.lean`, `V9/{Bridge,Data,Tilt}.lean`,
  `Main.lean` and `Axioms9.lean`: none, by `grep -c` with comments included.
  Their only options are `maxRecDepth` and `maxHeartbeats`;
- the emitters: none; their only `set_option` lines are `maxRecDepth 100000` and
  `maxHeartbeats 0`, and every generated module opens `noncomputable section`;
- `driver/run9.py`: `lean -o OUT M.lean` with no `-D` option.

The trust boundary, then: the Lean 4.33.1 kernel, including the built-in GMP arithmetic
on `Nat` that every `decide +kernel` check here evaluates through, to which `RowMinN`
adds `Nat.land` and `Nat.shiftRight`; Mathlib at the manifest’s `0df444a`, whose
packages the run built once in another checkout and shared through `LEAN_PATH` (N-2);
the three standard axioms; and the integrity of 1.27 million `.olean` files moved
between two machines, since an import loads an `.olean` without checking it again.
No compiler or native evaluator is trusted.

## 7. The Generated Files, and What the Unbuilt Replay Leaves Open

**`Main.lean` needs no trust in its generator:** it is retained, its digest is the built
one, and its text is 16,202 imports and five declarations, read above.

**The 1,275,911 root, leaf and row-group modules are not stored.** `SOURCES.sha256` (an
asset, pinned by digest, not downloaded) lists their digests, and they can be
regenerated from `v9-certs.tar.zst` with `emit_v7.py`. Their content is constrained
twice: the emitter’s templates write only `def`, `theorem` and the two options above,
and the kernel’s check of `Main.lean` fixes the type of every `root_NNNNN`. Two things
the axiom printout cannot exclude:

- a declaration added under `set_option debug.skipKernelTC true` contributes no axiom;
- a generated module could declare a new name that shadows one in `Main.lean`’s
  statements, such as `SquarePacking.LemmaELeaf.minSide`. For `bentz4` itself the
  elaborator requires its stated type to be definitionally equal to the type of
  `Bentz4.bentz4_of_validTilt9`, so a shadowed `minSide` would have to mean the same
  thing, unless the proof term’s own name were shadowed too.

Neither is suggested by anything in the templates, whose generated names are `r…l…`,
`…_ok` and `root_…`; both are excluded only by text this repository does not hold, or by
a statement receipt that names the constants in full (m-1).

What the held replay (`think-rw3i`, about 7,390 CPU-hours of kernel checks and 230 GB
for the assembly) would settle, and what cheaper steps settle first:

| Step | Cost | What it settles | Rung |
| --- | --- | --- | --- |
| Retain `v9-logs.tar.zst` and `SOURCES.sha256.zst`, and audit that every listed module has an exit-0 `lean -o` task under v4.33.1 | minutes of CPU, the assets’ download | the producer’s execution record is complete and on file (M-1) | the source-build admission `V3` needs, with a qualifying audit |
| Regenerate every module from `v9-certs.tar.zst` in an isolated environment (m-2), compare with `SOURCES.sha256` and scan for escapes and foreign names | about 0.9 CPU-hours of `emit_v7.py`, streamed to keep disk low | the generated text is the emitter’s and holds no escape | none: a premise check |
| Build every module and `Main.lean`, print the axioms and the full statements | about 7,390 CPU-hours, 22–32 GB a module, 230 GB for `Main.lean` | the kernel accepts the proof here | `C3` |

## 8. Findings

Graded blocking, major, minor or note.
None is blocking.

**M-1 (major; binds the description).** No execution record of the 1,275,911 module
checks has been read here.
The retained receipts are `main.log` (the assembly and the axiom printout) and the
README’s table summed from `tasks.jsonl`; `tasks.jsonl` itself is in `v9-logs.tar.zst`,
which is pinned by digest and not retained, and the sources are not stored.
Lean does not recheck an imported `.olean`, so `main.log` shows that `Main.lean` checks
against the oleans present, and not how they were made.
Until the logs are retained and audited (§7, first row; bead `think-ahfg`), the kernel
check of the leaves is the source’s report, and `T-251` stays `V0`. *For the record.*

**m-1 (minor; for the author).** `Axioms9.lean` prints axioms only.
Adding, in a file that imports `Sqpack.V9.Main` and opens no namespace,

```lean
example : SquarePacking.Bentz4.ValidTilt9 := SquarePacking.LemmaELeaf.validTilt9
example : ∀ k : ℕ, 8 ≤ k → SquarePacking.minSide (k ^ 2 - 4) = k := SquarePacking.LemmaELeaf.bentz4
```

or `#check` with `pp.fullNames`, would bind the published theorems to the library’s
constants by name, so that no generated declaration could change what they say.
A replay here should add it in any case.

**m-2 (minor; for the author and the replay).** The certificates are Python pickles, and
`emit_v7.py` calls `pickle.load`, which can execute code.
Regenerating the sources, which any audit of `SOURCES.sha256` needs, therefore runs
whatever the asset holds; the replay must do it in an isolated environment.
A text or JSON certificate format would remove the risk.

**m-3 (minor; for the record, fixed).** `T-251`’s claim said “The proof checks Daniel’s
k2m4 certificate qxzm_full … 16,200 per-root certificates”.
The kernel checks pose trees rebuilt root by root from `qxzm_full`’s leaf record,
refined where needed, with exact leaf certificates that Hosono’s `run_v7.py` wrote;
`qxzm_full`’s own leaf verdicts are not what is checked.
The claim now says so.

**N-1 (note).** “No statement changes” in the README is true of every theorem, and the
definition `rowOkM` does change (§5); this cannot affect any final statement.

**N-2 (note).** `run9.py` puts on `LEAN_PATH` the packages of another checkout
(`~/s59/sp/lean/.lake/packages`); `ENVIRONMENT.md` says they are as `lake-manifest.json`
pins them, which is not recorded by digest.
A replay builds its own.

**N-3 (note).** `receipts/sha256_final.txt` lists 31 scripts under `scripts_sgk/`; 27
match `scripts/` and the 4 that differ match `scripts_manual/`, consistent with the
README.

**N-4 (note; for the record).** The replay bead `think-rw3i` says its receipts are to be
cited by `T-250`; the entry is `T-251`.

**N-5 (note; significance).** The draft `S3` is changed to `S4` (§10).

**Questions for the author.**

1. Could the release carry a statement check like m-1’s, and a one-line coverage summary
   of `tasks.jsonl` against `SOURCES.sha256` (modules listed, modules with an exit-0
   task)?
2. Were the Mathlib and dependency oleans on `LEAN_PATH` built from the manifest’s
   revisions in that checkout, and is there a record of it?

## 9. Earlier Reviews, Compared

Read after §1–§8 were written: the claim-chain review of 3 October
([`review-2026-10-03-evand-k2m4-claim-chain.md`](review-2026-10-03-evand-k2m4-claim-chain.md))
and the review of Hosono’s checker run of 6 October
([`review-2026-10-06-wand125-validtilt9-independent-check.md`](review-2026-10-06-wand125-validtilt9-independent-check.md)),
both of `T-081`.

**Where they agree with this review.** Both read `sq`, `box`, `Packs`, `minSide` and
`ValidTilt` as §2 does, from the same `axioms_bentz4.log`; the claim-chain review’s root
grid for `qxzm_full` (16,200 roots, centre pitch $1/10$ on $[0, 9/2]^2$, 8 bins of
$1/16$ on $u \in [0, 1/2]$) is the grid `Main.lean` glues (§3); its cover facts (2,076
segments, one polygon of mass $289/25$, 16 pieces listed twice) are the ones
`Bridge.lean` depends on, and the 6 October review’s point that a doubled segment counts
twice under `fileCover` is the one §3 checks for `mcoverP`. Neither found a defect that
bears on this proof, and this review found none in them.

**What this proof changes in them.** The claim-chain review says the Lean “does not
prove `ValidTilt9`” and records as R-4 that nothing formal ties the run’s pose boxes to
`sq c (2 arctan u) 1`, a tie that “would need the leaves themselves in Lean”.
This formalization is that tie: its `CovT` boxes are stated with `sq` itself, and the
leaves are kernel checks.
If its build is admitted or replayed, R-4 is closed for this route.

**Trust boundaries, set side by side.** The claim-chain review lists `qx2_zm.py`’s trust
in paper lemmas and one float filter (`lines_in_reach`); the 6 October review lists the
second checker’s trust in python-flint, its driver and a sampled record check.
The Lean route trusts neither: every leaf lemma is a Lean theorem, and no floating-point
value or compiled code enters a decision.
It shares with `qx2_zm.py` the pose trees, rebuilt from its leaf record, which are not a
trust item since the kernel checks that the leaves tile each root; and it shares with
both checkers the cover bytes, the statement and Daniel’s reduction.
An error in those three would pass all three routes.

**What stays as they left it.** The 6 October review’s W-8 applies here too: the source
names Claude as co-author of the Lean, Daniel’s library and both checkers were written
with Claude models, and this review is another instance of that system family.
A kernel check does not depend on who wrote the proof, but the statement reading does,
which is one reason `V5` asks for a human expert.

## 10. Rungs and Significance

**Rungs.** This read qualifies as `C1` for `T-251`: it records what was examined and
what remains unchecked, and finds no defect.
It is recorded as the `external_review` of `E-k2m4-wand125-validtilt9-lean-report` and
in `T-251`’s `reviews`. `V` stays `V0`: no build of the proof and no admitted
source-build record is on file (M-1). `V3` needs either a complete build here or by a
third party retained here, or a source-build entry admitted under
[epistemics.md, Reported Formal Proofs and Source Builds](../../../epistemics.md#reported-formal-proofs-and-source-builds),
which needs the logs audited (§7; `think-ahfg`). `C3` needs the build (`think-rw3i`).
`V4` and `C4` need two accepting adversarial AI reviews and a human oversight record;
`V5` needs a named human expert’s formalization review.
Nothing here moves a bound, and the verified lower bounds at $k = 10$ to 18 are
unchanged.

An admitted source build would also bear on `T-081`: its reduction build
(`E-k2m4-evand-bentz4-lean-build`) is conditional on `ValidTilt9` with nothing
discharging it, and a producer’s admitted formal build can discharge a premise for `V`
without discharging it for `C`. That is for the lane that admits it to weigh.

**Significance: `S4`.** The draft scored a machine audit, `S3`, below `T-081`’s `S4`,
following `T-236` and `T-250`. Those formalize results the record holds at `V3`; this
one formalizes a value the record holds only as a report, at `V0`, and if correct it
establishes the whole family at $k \ge 8$, settling the open cases $k = 10$ to 18, which
is `T-081`’s anchor, a bound family.
The score is of the claim, and `T-154`, the formalization of a value held only as
`T-153`’s candidate, takes its candidate’s score for the same reason.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
