# Statement Audit: the Lean Formalization of Twelve-Square Optimality

**Date:** 2026-10-25. **Lane:** the statement audit in the review lane of
[stage 4](../../../packing/campaign/result-import.md#stage-4-validate) of the result
import runbook, for the import of `Jatloe12SquaresFormalized` (bead `think-4l14`, issue
[#810](https://github.com/jlevy/squares/issues/810)). **Reviewer:** Claude (AI), strong
tier (`tbd-strong`, acting name `w-n12-audit-1025`), at the reasoning setting the
coordinator `coord-n12-1025` launched it with, in a worktree of its own.
It read the source as data and ran no code from it.
It is not the mathematical review of the 117 cases, it is not a replay, and **it is not
the human expert formalization review that `V5` needs** (§10).

Before writing, it read the
[statement audit of the same publisher’s eleven-square formalization](review-2026-10-06-n11-lean-formalization-statement-audit.md),
the model for this document, and the coordinator’s triage figures (closure size,
kernel-escape counts, the source’s axiom totals), which §4 and §5 re-measure.
No earlier review of this formalization exists.

**In one line:** read line by line, `N12Compact.Final.optimality :
S12.packingConstant12 = 4` states $s(12) = 4$ in the project’s sense, the infimum of the
sides of squares that hold twelve unit squares with arbitrary independent rotations,
open interiors disjoint and boundary contact allowed, and `PackingConstant.lean` proves
that the 4-by-3 grid attains it.
The theorem has no premise.
By the source’s final audit, its trust base beyond Lean’s kernel and the three standard
axioms is 1,624 `native_decide` axioms owned by 1,525 declarations of the original
numerical classification, which trust Lean’s compiler.
Nothing was built here, and the run that accepted the proof compiled no module itself,
so the formalization is recorded as the source’s report.

## Summary for the Author

- **The statement is faithful.** `UnitPacking`, `feasibleSides` and `packingConstant12`
  are the unrestricted problem: any rotation and translation of a unit square, open
  interiors pairwise disjoint, every interior point in the closed $[0,L]^2$, so contact
  with the wall and between squares is allowed.
  Taking `sInf` matches the project’s definition of $s(n)$, and the value 4 cannot come
  from Mathlib’s convention for an empty or unbounded set.
- **No premise is smuggled in.** The final theorem has no binders.
  The one `Prop` structure on its path, `SourceAssembly.Pending`, is discharged by
  `pending_closed` from `pendingIds = ∅`, decided in the kernel.
- **The 1,624 native axioms agree with the code.** They are exactly the textual
  `native_decide` calls of 1,525 declarations in `source/S12/`, one axiom per call.
  The other 948 calls in the import closure are compiled but are not in the final
  theorem’s axiom set.
- **What the native calls decide is finite and exact:** searches for disjoint owner
  assignments over finite sets of naturals, coverage of auxiliary-point subsets, and
  convex-combination and linear certificates over $\mathbb{Q}$. No floating point
  appears.
- **Two major findings bind how the result is described**, not whether the statement is
  right: the theorem trusts the compiler (M-1), and no build of it is on record outside
  a run that reused cached objects and cannot be inspected (M-2). Two minor findings ask
  for the statement’s definitions in a module of their own (m-1) and for Mathlib to be
  pinned where Lake reads it (m-2).

## 1. What Was Audited

Lean paths below are relative to the project directory `Lean/Proofs/N12-jatloe/`, and
`run/` abbreviates the repository’s `verification/run-38849916588/`.

| Field | Value |
| --- | --- |
| Source | [Queuingtheorydotcom/Jatloe12SquaresFormalized](https://github.com/Queuingtheorydotcom/Jatloe12SquaresFormalized/tree/d0caf4532a7ead68be1389ef87387b126fc2e0ab) at `d0caf4532a7ead68be1389ef87387b126fc2e0ab`, tag `n12-verified-2026-10-16`; by its README a byte copy of `EvolvingPrograms/SquaresLean` at `1f60d412`, which is not publicly reachable |
| Claim | Repository `README.md` lines 5–11: `N12Compact.Final.optimality : S12.packingConstant12 = 4`, arbitrary orientations and translations, disjoint interiors, boundary contact allowed, a 4-by-3 grid attaining side 4 |
| Credits | Jatloe, the mathematical proof and a partial formalization; Ben Gurevitch, help with the formalization; CTJLewis, refactoring and compiling (`README.md` lines 13–15) |
| Read in full | The statement: `source/S12/Diagonal.lean`, `Normalization.lean`, `PackingConstant.lean`, and `NormalizedPacking` in `Packing.lean`. The assembly: `Compact/Assembly/Final.lean`, `SourceAssembly.lean`, `Remaining117.lean`, `Completion/Contracts.lean`, `source/S12/To117.lean`. The definitions behind each family of native sites (§4) and every `macro_rules` and `elab_rules` pattern (§5). The pins: `lakefile.toml`, `lake-manifest.json`, `lean-toolchain`, `verification/toolchain-lock.json`. The record: repository `README.md`, `AGENTS.md`, `SOURCE-PROVENANCE.json`; `run/README.txt`, `GlobalTypeAudit.lean`, `global-type-axiom-audit.log`, `global-native-axiom-audit.json`, `github-replay.json`, `verified-source-manifest.json`. As data: `scripts/audit_native_axioms.py` and `scripts/bootstrap_sources.py` |
| Run here | [`devtools.lean_closure`](../../../packing/devtools/lean_closure.py), the triage’s receipt of the import closure of `Compact.Assembly.Final` at the commit. [`devtools.audit_n12_lean`](../../../packing/devtools/audit_n12_lean.py) over the closure’s bytes, each module read by the Git blob that receipt names, reusing [`devtools.audit_n11_lean`](../../../packing/devtools/audit_n11_lean.py)’s token patterns and its comment and string stripping: a token scan, an instance classifier, a search for declarations that could shadow the statement’s names, the mapping of native axioms to their owners (§4), and the comparison with the source’s manifest (§5), written as the packet’s [`receipts/statement-audit.json`](../../../packing/resources/web/jatloe-n12-lean-2026-10-16/receipts/statement-audit.json). The audit first counted with programs in its scratch space; the tool, written the same day, reproduces every count cited here, and its `check` recomputes the statement closure’s part from the packet’s retained bytes |
| Not done here | Any Lean build, elaboration or `#print axioms`; reading the release’s evidence ZIP or its compiled checkpoint; any part of the mathematics |

## 2. The Claim Against the Theorem, Line by Line

The final theorem is `Compact/Assembly/Final.lean` lines 14–15, in
`namespace N12Compact.Final`:

```lean
theorem optimality : S12.packingConstant12 = 4 :=
  SourceAssembly.optimality SourceAssembly.pending_closed
```

Its type uses these definitions:

```lean
-- source/S12/Diagonal.lean, namespace S12Pilot
def InBands (loU loV a u v : ℝ) : Prop :=
  loU < u ∧ u < loU + a ∧ loV < v ∧ v < loV + a
structure OpenSquare where
  c : ℝ
  s : ℝ
  loU : ℝ
  loV : ℝ
  side : ℝ
  unit_normal : c ^ 2 + s ^ 2 = 1
  side_pos : 0 < side
def OpenSquare.Inside (q : OpenSquare) (x y : ℝ) : Prop :=
  InBands q.loU q.loV q.side (q.c * x + q.s * y) (-q.s * x + q.c * y)

-- source/S12/Normalization.lean, namespace S12, open S12Pilot
structure UnitPacking (L : ℝ) where
  square : Fin 12 → OpenSquare
  congruent : ∀ i,(square i).side=1
  contained : ∀ i x y,(square i).Inside x y → 0≤x ∧ x≤L ∧ 0≤y ∧ y≤L
  disjoint : ∀ i j,i≠j → ∀ x y,¬((square i).Inside x y ∧ (square j).Inside x y)

-- source/S12/PackingConstant.lean, namespace S12
def feasibleSides : Set ℝ := {L | 0<L ∧ Nonempty (UnitPacking L)}
noncomputable def packingConstant12 : ℝ := sInf feasibleSides
```

| The claim says | The formalization says | Where | Agrees |
| --- | --- | --- | --- |
| $s(12) = 4$, where $s(n)$ is the infimum of the sides at which a packing exists ([SYNOPSIS.md, The Problem](../../../SYNOPSIS.md#the-problem)) | `packingConstant12 := sInf feasibleSides`, and the theorem says it is 4 | `PackingConstant.lean` 58–59; `Final.lean` 14 | Yes; the paragraph below rules out the degenerate values of `sInf` |
| Twelve squares | `square : Fin 12 → OpenSquare` | `Normalization.lean` 9 | Yes |
| Unit squares | `congruent`: every side is 1, which makes `side_pos` redundant and excludes degenerate squares | `Normalization.lean` 10; `Diagonal.lean` 60 | Yes |
| Any orientation, independently | Each square has its own $(c, s)$ with $c^2 + s^2 = 1$ and no other constraint; $(x, y) \mapsto (cx + sy, -sx + cy)$ has determinant $c^2 + s^2 = 1$, a rotation | `Diagonal.lean` 53–63 | Yes. Reflections are not needed: a square is its own mirror image, so every congruent copy is a rotated and translated one |
| Any position | `loU` and `loV` are unconstrained reals; in its rotated frame the square is $(loU, loU+1) \times (loV, loV+1)$, and `inside_iff_rotated_box` proves `Inside` is the rotated image of that box | `Diagonal.lean` 62–63, 74–95 | Yes: every open unit square in the plane is such a record |
| Open squares | `InBands` is strict on all four sides | `Diagonal.lean` 23–24 | Yes |
| Inside the container, boundary contact allowed | `contained`: every interior point lies in the closed $[0,L]^2$, which holds exactly when the closed square does, since $[0,L]^2$ is closed | `Normalization.lean` 11 | Yes: the closed container, axis-aligned without loss of generality |
| Interiors disjoint | `disjoint`: for $i \ne j$ no point is in both open squares | `Normalization.lean` 12 | Yes; squares may touch |
| A packing exists at side $L$ | `L ∈ feasibleSides` is `0 < L ∧ Nonempty (UnitPacking L)` | `PackingConstant.lean` 58 | Yes; `0 < L` is implied anyway, since an open unit square in $[0,L]^2$ forces $L \ge 1$ |
| The grid attains 4 | `gridPacking : UnitPacking 4`, square `i` axis-aligned ($c = 1$, $s = 0$) at `loU = i % 4`, `loV = i / 4`, four columns and three rows; `four_feasible : 4 ∈ feasibleSides` | `PackingConstant.lean` 8–15, 32–55, 61 | Yes, by `linarith`, `omega` and casts; the module has no `native_decide` |

**The infimum.** The eleven-square formalization stated `IsLeast` directly, and its
audit checked that by `Iff.rfl`. This one states `sInf feasibleSides = 4`. On
$\mathbb{R}$, Mathlib’s `sInf` is total and is 0 on a set that is empty or not bounded
below (a convention this audit did not re-read at the pinned revision).
Because 4 is not 0, the theorem itself implies that `feasibleSides` is nonempty and
bounded below, and then `sInf` is its greatest lower bound: every feasible side is at
least 4. The source also proves both side conditions in the statement file,
`four_feasible` and `feasibleSides_bddBelow` (lines 61–63), and uses them in
`packingConstant12_eq_four_of_exclusion` (69–77) through `csInf_le` and `le_csInf`. With
`four_feasible` the infimum is attained, so `IsLeast feasibleSides 4` follows in one
step from the source’s lemmas; that step was not elaborated here (§6).

**Name resolution.** `Final.lean` writes `S12.packingConstant12` inside
`namespace N12Compact.Final`. A search of every declaration in the 5,377 modules of the
closure finds exactly one declaration each of `S12.packingConstant12`,
`S12.feasibleSides`, `S12.UnitPacking`, `S12Pilot.OpenSquare`,
`S12Pilot.OpenSquare.Inside` and `S12Pilot.InBands`, and no namespace named `S12` or
`S12Pilot` nested inside another, so the name cannot resolve to an `N12Compact.S12`
declaration.
The source’s own final audit states the type from the root namespace with no
`open`, `example : S12.packingConstant12 = 4 := N12Compact.Final.optimality`
(`run/GlobalTypeAudit.lean` line 2). `Normalization.lean` opens `S12Pilot` inside
`namespace S12`, and no `S12.OpenSquare` exists for `OpenSquare` to collide with.
The 109 modules in which the definitions are elaborated contain no notation, macro,
syntax or elaborator declaration, no `export`, no `open … renaming`, no `attribute`
command, no `OfNat` and no instance except 21 `Decidable` instances on the project’s own
predicates (§5). `ℝ`, `<`, `≤`, `sInf`, the numerals and `Fin 12` therefore mean what
Mathlib means by them.

## 3. The Final Theorem Has No Premise

- `Final.optimality` has no binders, so it takes no hypothesis and no instance argument.
  A premise could reach it only as an axiom, and §4 lists every axiom.
- `SourceAssembly.optimality (work : Pending)` (`SourceAssembly.lean` 139–140) is
  `Remaining117.optimality registry (pending_exclusions work)`. `Pending` (110–113) is a
  `Prop` structure with three fields: `other_cases`, the exclusion of every case in
  `(pendingIds.erase 981).erase 1092`, and `case981` and `case1092`, whose default
  values are `C981Compact.pending_closed` and `C1092Compact.pending_closed`.
- `pending_closed` (129–135) proves `other_cases` from `pending_ids_exact : pendingIds =
  ∅` (94–95, `decide +kernel`), so that field is vacuous, and takes the two defaults: a
  theorem (`Compact/Cases/C981Registry.lean` 82) and a proof of the `Prop` structure
  `C1092Compact.Pending`, all of whose fields have default proofs
  (`Compact/Cases/C1092Compact.lean` 15–25). The registry holds 117 cases and none
  pending (`source_count` and `pending_count`, lines 90–92, `decide +kernel`).
- `Remaining117.optimality` (`Compact/Assembly/Remaining117.lean` 99–104) applies
  `packingConstant12_eq_four_of_exclusion`, whose only premise is `∀ p :
  NormalizedPacking, False`. It proves that premise from `packing_reduction_to_117`
  (`source/S12/To117.lean` 34–37), which places every normalized packing, after one of
  the square’s symmetries, in one of 117 retained marker families, and from the
  registered exclusion of each of them (`Completion/Contracts.lean` 7–14).
- `NormalizedPacking` (`source/S12/Packing.lean` 9–16), twelve squares of a common side
  in $(1, 1001/1000]$ inside $[0,4]^2$, is an intermediate, and its fidelity is not part
  of the statement. `UnitPacking.normalize` (`Normalization.lean` 44–67) builds one from
  any `UnitPacking L` with $L < 4$ by scaling by $\min(4/L, 1001/1000)$, so the proof
  that none exists excludes every packing below 4, whatever `NormalizedPacking` models.

Apart from `native_decide` (§4), none of the constructs that could weaken checking
occurs in code (§5).

## 4. The Axiom Receipt

The source’s final audit elaborates `run/GlobalTypeAudit.lean`, which states the type
and runs `#print axioms N12Compact.Final.optimality` with `pp.fullNames`.
`run/global-type-axiom-audit.log` records exactly:

- `propext`, `Classical.choice` and `Quot.sound`;
- 1,624 axioms named `<declaration>._native.native_decide.ax_<i>`, some with a second
  index `_<j>`.

No `sorryAx` and no other axiom appears.
`run/global-native-axiom-audit.json` lists the same 1,627 names.
The log’s SHA-256 `e76041bc…4b15` and the source manifest’s `95fe302f…09e0` are the
digests `SOURCE-PROVENANCE.json` records (lines 46–47). This is the source’s record of a
run that nobody here can inspect; nothing here ran `#print axioms`.

**The count against the code.** Counted here, the code of the closure has 2,572
`native_decide` calls in 42 modules, all under `source/S12/`, and none in the `Compact`
or `Completion` libraries.
The calls sit in 2,274 declarations, 1,964 theorems and 310 definitions.
The 1,624 axiom names have 1,525 distinct owners.
Every owner is a declaration of the closure with `native_decide` in its body, and each
owner’s number of axioms equals its number of calls, so the 1,624 axioms are exactly the
calls of those 1,525 declarations.
(Declarations were found by matching their headers and open namespaces, not by parsing.)
The other 948 calls, in 749 declarations, are compiled with the closure but are not in
the final theorem’s axiom set: 882 in `Case976Domains.lean`, 24 in `CoverData.lean`, 37
in the four-point data, and five counting or coverage facts, `raw_count`, `early_count`,
`retainedRows_count` and two angle covers (N-2). The second index in the names varies by
file and does not affect the count.

Where the 1,624 sit, and what each call decides:

| Where in `source/S12/` | Axioms | Declarations | What each call decides |
| --- | --- | --- | --- |
| `Case976Domains.lean` | 965 | `query976_*_checked` (750), `domain976_*` (102 definitions, 201 calls), `single976_*_checked` (14) | Case 976’s local rejections, each a `LocalRejection.Check` over exact rational points (the local-query row below), and its owner domains, each a product of two single-owner domains |
| `CoreDataChunks/Chunk00`–`13` | 419 | `coreProof<i>_checked` | `CoreProof.Check` (`CoreExclusion.lean` 67–70): each owner spec belongs to the family and agrees in kind, the masks are distinct, and `feasible` (`DomainSearch.lean` 9), a search for pairwise disjoint owner sets, returns `false`. `CoreProof.sound` (75) turns that into the exclusion of every normalized packing with that marker family |
| `DomainSpecDataChunks/Chunk00`–`07` | 128 | `singleSpec<i>_checked` (103), `combinedSpec<i>_checked` (25) | `SingleSpec.Check` (`DomainSpecs.lean` 53–55): every auxiliary-point subset in a size range is either allowed or refuted by a named local query; `CombinedSpec.Check` (80) does the same for combined owners |
| `FourPointData/Chunk00`–`06` | 74 | `fourDatum<i>_checked` | `FourPointDatum.Check` (`FourPointCertificate.lean` 126–128): a squared distance at most 1, and sixteen certificates, each a nonnegative rational combination of linear constraints that is strict and sums to zero (`LinearCertificate.lean` 72–76) |
| `LocalQueryDataChunks/Chunk00`–`06` | 35 | `queryChunk<i>_checked` | Every query of a chunk passes `LocalQuery.Check` (`LocalQuery.lean` 53–54), 1,721 queries in all: triangle certificates writing a target point as an exact convex combination over $\mathbb{Q}$ (`Convex.lean` 46–50), checked against lists of points inside and outside the square (`LocalRejection.lean` 87–93) |
| `Raw.lean`, `To117.lean` | 3 | `early_covered`, `exclusion_coverage`, `retainedRows_ids` | The enumeration: every marker family passing the early filter lies in one of the 577 listed symmetry orbits (`Raw.lean` 30–31); each of the 577 rows is retained, has a diagonal contradiction or has an excluding core (`To117.lean` 16–18); the retained rows are the 117 named cases (12) |

**What the native axioms trust.** Each one admits, as an axiom, the result of a compiled
evaluation of the goal’s `Decidable` instance; the kernel never re-checks it.
The theorem therefore trusts Lean’s compiler, code generator and runtime, the GMP-backed
arithmetic of `Nat` and `Int` that exact rational arithmetic reduces to, and any
`implemented_by`, `extern` or `csimp` in Lean core, Batteries and Mathlib that the
evaluated code reaches.
The project adds none (§5). The decided propositions are about natural numbers, finite
sets of them and rationals; no floating-point or fixed-width integer type appears in any
module of the closure.
That is the trust model the source names (`README.md` lines 28–33, `AGENTS.md` lines
8–10). It is weaker than a kernel-only check, and the record must not describe this
theorem as using the standard axioms only (M-1). The rest of the proof decides its
finite facts in the kernel: the closure has 15,166 `decide +kernel` calls in 844
modules.

**What the axiom map cannot exclude.** The source’s audit approves a native axiom by its
name’s shape under an authenticated owner, the pattern `re.escape(name) +
r'\._native\.native_decide\.ax_[1-9][0-9]*(?:_[0-9]+)*'`
(`scripts/audit_native_axioms.py` line 184). A hand-written axiom given such a name
would pass that test.
The same script refuses the word `axiom` in the lexed source (line 146). The scan here
finds the word nowhere in the code of the closure’s 5,377 modules, only six times in
comments, and finds no `addDecl`, `modifyEnv` or `setEnv` by which a metaprogram could
add one (§5). For this property the scan is load-bearing, as it was for the
eleven-square formalization.

## 5. Kernel Escapes on the Critical Path

Counted here over the code of the 5,377 modules of the closure of
`Compact.Assembly.Final` by
[`devtools.audit_n12_lean`](../../../packing/devtools/audit_n12_lean.py), with comments,
strings and character literals blanked by `devtools.audit_n11_lean.strip_code`, using
that tool’s token patterns plus the few `EXTRA_TOKENS` adds; every figure below is in
[`receipts/statement-audit.json`](../../../packing/resources/web/jatloe-n12-lean-2026-10-16/receipts/statement-audit.json),
with the place of each hit for a token with at most 100 of them.
The statement closure is the 109 modules that `S12.PackingConstant` imports (§6).

| Token | Whole closure | Statement closure | Load-bearing |
| --- | --- | --- | --- |
| `native_decide` | 2,572 in 42 modules, all in `source/S12/` | 723 in 39 modules | Yes: 1,624 calls are the final theorem’s native axioms (§4) |
| `axiom` declaration, `sorry`, `admit` | 0 | 0 | Yes for `axiom` (§4) |
| `implemented_by`, `extern`, `unsafe`, `opaque`, `csimp`, `ofReduceBool`, `reduceBool`, `trustCompiler`, `decide +native` | 0 | 0 | — |
| `debug.skipKernelTC` or any `debug.` option, `#exit`, `#eval`, `run_cmd` and its kin, `addDecl`, `modifyEnv`, `setEnv`, `initialize` | 0 | 0 | — |
| `notation`, `infix`, `prefix`, `postfix`, `export`, `attribute` commands, elaborator attributes | 0 | 0 | — |
| `syntax`, `macro`, `macro_rules`, `elab`, `elab_rules`, `declare_syntax_cat` | 89 in 24 modules, all under `Compact/Bridge`, `Compact/Core` and `Compact/Cases/C898` | 0 | No escape (below) |
| `instance` | 247 in 163 modules: 245 `Decidable`, `DecidablePred` or `DecidableRel` instances on project predicates, and 2 `Fintype` instances on project types named `Variant` | 21, all `Decidable` | No: a `Decidable` instance is a kernel-checked term and cannot change what a proposition says |
| `import Lean…` | 22 import lines in 14 modules, and `Std.Tactic` once | 0 | The metaprograms below |
| `open … hiding` | 1, `Compact/Geometry/CornerWallMarkerMixed.lean` 11 | 0 | No |
| `set_option` | 8,969: `Elab.async` (4,103), `linter.unnecessarySeqFocus` (1,846), `maxRecDepth` (1,794), `maxHeartbeats` (1,225, some `0`), `synthInstance.maxSize` (1) | 177, of the first, third and fourth kinds | No: none weakens checking |
| `noncomputable` | 3,661 in 2,685 modules | 112 | No: it only stops code generation, so no `native_decide` can evaluate such a definition. In the statement it marks `packingConstant12`, a real infimum, and the scaling in `Normalization.lean` |
| `Float`, `UInt8` to `UInt64`, `USize` | 0 | 0 | — |
| `@[reducible]` or `@[irreducible]`, `OfNat` | 1 each: `@[irreducible] def queryAt` (`source/S12/DomainSpecs.lean` 10), and `OfNat.ofNat` matched by a metaprogram (`Compact/Core/SparseLiteral.lean` 40) | `@[irreducible]` 1, the same; `OfNat` 0 | No: `irreducible` only keeps a definition from unfolding, and the metaprogram reads numerals and declares no instance |

Outside code, `native_decide` occurs twice more in comments, and `unsafe` and `opaque`
occur only in comments.
`lakefile.toml` sets no Lean option for any library, so no option applies silently to
every module (N-3).

**The metaprograms.** The `Compact` layer defines its own commands and term elaborators.
Commands such as `checked_common_fan`, `checked_recipe` and `kernel_matrix` build
declarations from compact data and submit them through `elabCommand`, and term
elaborators such as `materialize_rows%`, `sparse_rows%` and `pose_text%` turn literals
and reductions into terms.
Every `macro_rules` and `elab_rules` pattern was read, and each matches only its own new
syntax. What they emit is ordinary `def` and `theorem` commands whose checks are `decide
+kernel` or `rfl`, and the kernel checks every declaration they add.
The two tactic elaborators, `materialized_fan_rfl`
(`Compact/Bridge/CheckedCommonFanCommand.lean` 17–20) and `c898_numeric_rfl`
(`Compact/Cases/C898/FusedContextSyntax.lean` 43–46), close goals by reflexivity at full
transparency, which the kernel re-checks.
None of this code is in the statement closure, and none redefines `=`, a numeral or an
identifier the statement uses.

**The scanned bytes are the run’s.** Each of the 5,377 modules hashes to its SHA-256 in
`run/verified-source-manifest.json`, which lists the same 5,377 modules; none differs.
The manifest binds them to the upstream commit `1f60d412`, which is not public, so the
correspondence with what the upstream run compiled rests on the source’s manifest.

The scan is a token count, not a parse: a construct spelled in a way no pattern matches
would pass it.

## 6. The Statement Closure, Not Built Here

The eleven-square audit built its statement’s closure, 18 modules checked by the kernel
alone, and checked the statement in Lean.
The same check costs more here.
`UnitPacking` is declared in `Normalization.lean`, whose first line imports `S12.To117`,
the reduction to 117 cases.
The definitions the theorem’s type uses are therefore elaborated only after 109 modules,
1,138,482 bytes, which hold 723 `native_decide` calls in 39 modules (m-1). Those calls
cannot change what the definitions mean, but building the definitions compiles and
evaluates them.

What would settle what reading cannot:

- Building the 109 modules at Lean 4.35.0 and Mathlib `56a00585`, then elaborating a
  probe like the eleven-square one: `#print` of the six definitions of §2;
  `IsLeast feasibleSides 4` from `optimality`, `four_feasible` and
  `feasibleSides_bddBelow`; `#print axioms` of `gridPacking` and `four_feasible`, which
  by reading use only the standard axioms; and two controls that the definitions are not
  vacuous, that a lone axis-aligned square is the expected box and that two unit squares
  do not fit at side 1.
- Printing the type of `N12Compact.Final.optimality` itself, which needs the whole
  closure.
- `#print axioms` on the whole proof after a cold build, and `lean4checker` over its
  objects (M-2).

## 7. Findings

None blocks registering the formalization as the source’s report.

| Id | Grade | Where | Finding |
| --- | --- | --- | --- |
| M-1 | major | `run/global-type-axiom-audit.log`; `README.md` 28–33 | The final theorem depends on 1,624 `native_decide` axioms and trusts the compiler |
| M-2 | major | `SOURCE-PROVENANCE.json` 18–20; `run/README.txt` 42–48 | No build of the theorem is on record that anyone outside the source can inspect; the accepting run compiled no module |
| m-1 | minor | `Normalization.lean` 1, 8 | The statement’s definitions import the reduction, so the statement cannot be built apart from 723 native calls |
| m-2 | minor | `lake-manifest.json` 7–15; `verification/toolchain-lock.json` | Lake pins no Mathlib revision; the pin lives in a file the bootstrap script reads |
| N-1 | note | `SourceAssembly.lean` 11–13, 19, 26; `Compact.lean` 16–17; `Diagonal.lean` 7–17 | Comments describe earlier stages as current |
| N-2 | note | `Case976Domains.lean`, `CoverData.lean`, `FourPointData/`, `Raw.lean`, `To117.lean`, `AngleData64.lean`, `AngleData128.lean` | 948 native calls in the closure are not on the theorem’s path |
| N-3 | note | `lakefile.toml` | `autoImplicit` is left at Lean’s default; it cannot reach the statement |

**M-1, compiler trust** (major; binding on wording).
The final theorem is checked by Lean’s kernel and its compiler, not by the kernel alone
(§4). Every view of the result that mentions the formalization must say so, and a human
formalization review has to accept that trust explicitly under its `axioms` check.
The source says the same (`README.md` lines 28–33).

**M-2, no build on record that anyone can inspect** (major; it sets the encoding).
The accepting run 38849916588 compiled no module: all 5,377 objects were reused
(`SOURCE-PROVENANCE.json` line 18), from a checkpoint saved by an earlier run,
38847898861, at commit `437041a0`, which then failed (`run/README.txt` lines 42–48).
Lean does not re-check declarations it imports from compiled objects, so the kernel
checks of the 5,377 modules are those of whichever compilations produced the objects;
the final audit derived only the theorem’s type and axiom list from them.
The upstream repository and its runs are not publicly reachable, and
`local_independent_full_rebuild_performed` is `false` (line 20). The release’s evidence
ZIP holds the per-module compiler logs, and this audit did not read it.
A run that nobody here can inspect is the source’s report.

**m-1, the statement is not separable from the proof** (minor).
`Normalization.lean` line 1 imports `S12.To117`, so `UnitPacking` (line 8), and with it
`feasibleSides` and `packingConstant12`, can be built only after the reduction and its
723 native calls (§6). Moving `InBands`, `OpenSquare` and `Inside` (`Diagonal.lean`
23–63), `UnitPacking`, `feasibleSides`, `packingConstant12`, `gridPacking` and
`four_feasible` into a module that imports only Mathlib would let anyone check the
statement and the upper bound in the kernel alone, as the eleven-square formalization
allows.

**m-2, Mathlib is pinned outside Lake** (minor).
`lake-manifest.json` lists `mathlib` and eight other packages as `path` packages under
`.lake/packages/`, with no revision (lines 7–15 for `mathlib`). The revision,
`56a005855ea17e0b0958f73ec801ae140b0a1679`, is in `verification/toolchain-lock.json`,
which `scripts/bootstrap_sources.py` reads (lines 61–77) before fetching.
A replay that runs `lake build` without that bootstrap builds against whatever is in
`.lake/packages`, so the record has to state the revision itself.

**N-1, comments describe earlier stages** (note).
`SourceAssembly.lean` lines 11–13 say the source closure “still awaits the final
ordinary Lean replay”, line 19 calls it “source composition, not a fresh replay”, and
line 26 says “the entire new assembly still requires acceptance”.
`Compact.lean` lines 16–17 say “the source is uncompiled”,
`Compact/Geometry/WallChain.lean` line 15 that it was assembled “without a fresh Lean
replay”, and `mathematics/README.txt` line 3 that “no Lean compilation was run”.
`Diagonal.lean` lines 7–17, which hold the statement’s square model, call the file a
pilot that is “not a formalization of the complete packing proof”.
The repository README says its own status supersedes such comments (lines 58–59), and
the proof bodies are unconditional.

**N-2, native calls off the theorem’s path** (note).
948 calls in 749 declarations (§4) are evaluated natively whenever the closure is built,
but the final theorem does not depend on them.
Removing them from the closure would shorten a replay and the list of native sites a
reviewer has to account for.

**N-3, `autoImplicit`** (note).
`lakefile.toml` sets no options, so `S12`, `Compact` and `Completion` compile with
Lean’s default for `autoImplicit`. It cannot enter the statement: the theorem’s type
names only the dotted `S12.packingConstant12`, and in `UnitPacking` every identifier is
bound or resolves to a declaration; an auto-bound `OpenSquare` would make
`(square i).side` fail to elaborate.

## 8. Questions for the Author

1. Would you move the statement’s definitions and the grid into a module that imports
   only Mathlib (m-1)?
2. Can the logs of run 38849916588, or `EvolvingPrograms/SquaresLean` at `1f60d412`, be
   made public (M-2)?
3. Has the whole closure ever been compiled from scratch in one run, and has
   `lean4checker` been run over the objects (M-2)?
4. What would it cost to decide the 1,624 native sites with `decide +kernel`, as the
   `Compact` layer does for its own checks, and is case 976, with 965 of them, the main
   obstacle?
5. Are the 948 native calls the final theorem does not use (N-2) needed in its import
   closure?
6. Would you pin Mathlib’s revision in `lake-manifest.json` (m-2)?

## 9. Verdict

Read here, the formal statement says $s(12) = 4$ in the project’s sense, over the
unrestricted model: unit squares with independent arbitrary rotations, open interiors
disjoint, a closed container and boundary contact allowed; the 4-by-3 grid attains the
infimum. The final theorem has no premise.
By the source’s final audit and the scan here, its trust base is Lean’s kernel, the
three standard axioms and 1,624 disclosed `native_decide` axioms of the original
numerical classification, with no `sorry`, no declared axiom and no `implemented_by` or
`extern` in the project.
The formalization can be recorded as the source’s reported proof-assistant run with its
axiom receipt; nothing here replays it.

## 10. What This Audit Does Not Establish, and What `V5` Still Needs

This audit does not establish:

- that the proof is correct: no module was built, no native evaluation was re-run and no
  `#print axioms` was run here, so the axiom list is the source’s;
- that the 5,377 compiled objects were checked by the kernel, or were compiled from the
  bytes read here, beyond the source’s receipts (M-2);
- the mathematics: the 117 cases and the 258 written chapters under
  `mathematics/current/proofs/` were not read, which is the mathematical review’s lane;
- anything in Lean: the statement was read, not elaborated (§6).

`V5` needs two records, neither of which exists.

**A complete build the record can rest on**: the 5,377 modules built at the pinned
toolchain from retained bytes, with its own `#print axioms` receipt, here as a
`replayed-here` entry or by a third party whose build is retained here.
The source’s workflow is manually dispatched and resumable on a GitHub runner
(`README.md` lines 61–79); the accepting run had 88 CPUs and about 180 GB of memory
available (`run/runner-resources.json`).

**A human expert’s formalization review**, as
[epistemics.md, Review Records](../../../epistemics.md#review-records) asks:
`kind: formalization`, `reviewer_kind: human`, `independent_of_author: true`, by a named
person who states their competence in Lean and in the mathematics and is not the
formalization’s author, with `checked` including `statement-fidelity`, `definitions`,
`axioms` and `build`, an accepting verdict, and the document mapped in
[`document-map.yaml`](../document-map.yaml).
Its `axioms` check must accept the compiler trust of M-1, and its `build` check should
read the build above, not the source’s report.
This audit is neither: its reviewer is an AI.

## For the Records Lane

- **Encode the formalization as the source’s report**, as the eleven-square import did
  with `E-n011-lean-formalization-report`: `reported`, `reported_method:
  proof-assistant-checked`, replay `not-attempted`. Every sentence that mentions it says
  the proof is checked by the kernel and the compiler.
- **Cite the tool’s receipt, not the audit’s programs.** The counts of §2, §4 and §5
  beyond `devtools.lean_closure`’s own (the instance classes, the syntax-extension and
  `set_option` census, the shadowing search, the mapping of 1,624 axioms to 1,525 owners
  and the manifest comparison) first came from programs written for this audit in its
  scratch space.
  [OR-1](../../../operating-rules.md#or-1-build-the-tool-never-leave-a-measurement-in-one-off-code),
  and the second finding of the
  [eleven-square adversarial review](review-2026-10-06-n11-lean-formalization-adversarial.md),
  ask for such receipts to come from a kept tool before an entry cites them, so the
  integration lane made them
  [`devtools.audit_n12_lean`](../../../packing/devtools/audit_n12_lean.py), whose
  receipt is
  [`receipts/statement-audit.json`](../../../packing/resources/web/jatloe-n12-lean-2026-10-16/receipts/statement-audit.json).
- **The record’s inputs are retained** in the packet: the closure receipts, the run
  directory `verification/run-38849916588/` and `SOURCE-PROVENANCE.json`.
- **This review is mapped** in [`document-map.yaml`](../document-map.yaml).
- **“Confirmed”.** Nothing here confirms the proof.
  The statement audit is a reading of the source, and the counts are of its bytes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
