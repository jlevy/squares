# Statement Audit: the Lean Formalization of Eleven-Square Optimality

**Date:** 2026-10-06. **Lane:** N11 of epic `think-wyf4`, bead `think-8spq`, stages 1 to
3 of the [result import runbook](../../../packing/campaign/result-import.md) for the
formalization of `T-060`. **Reviewer:** Claude Opus 5.5 (AI), the importing lane.
This is the lane’s own audit.
It is not the separately prompted
[adversarial review](review-2026-10-06-n11-lean-formalization-adversarial.md), whose
findings §9 dispositions, and **it is not the human expert formalization review that
`V5` needs** (§8).

**In one line:** read line by line and checked in Lean where it can be,
`ElevenSquare.optimality` states `T-060`’s claim, $s(11) = T$ with $T$ the register’s
exact endpoint, over the register’s model of closed unit squares with arbitrary
independent rotations, boundary contact allowed and open interiors disjoint.
By the source’s final audit, the only thing on its critical path besides Lean’s kernel
and the three standard axioms is `native_decide`: 10,464 numerical declarations, 13,308
auxiliary axioms, trusted to Lean’s compiler, as the source itself says.
The full proof was not built here, and the source’s run is private, so the formalization
is recorded as the source’s report.

## 1. What Was Audited

| Field | Value |
| --- | --- |
| Source | [Queuingtheorydotcom/11SquaresFormalized](https://github.com/Queuingtheorydotcom/11SquaresFormalized) at `cdc746ed907d258057c283aeb6d077cb2c27e349`, retained in the [6 October packet](../../../packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/README.md) |
| Claim | `T-060`: $s(11) = T = (6u+4)/(1+2u-u^2)$, $u$ the unique root in $(9/25, 37/100)$ of $5u^8-10u^7-2u^6+14u^5+12u^4-6u^3+2u^2+2u-1$, independent rotations and boundary contact allowed |
| Read in full | `Geometry.lean`, `BasicGeometry.lean`, `Endpoint.lean`, `EndpointBounds.lean`, `Foundations.lean`, `Optimality.lean`, `Verification.lean`, `Pending/S09_GlobalLowerBound.lean`, `Tasks/T07/UnfinishedCapture.lean`, `Tasks/T07/GlobalComposition.lean`, `Tasks/T07/Ext/Case438Global.lean`, `Cases.lean`; the declarations of `Construction.lean`; `lakefile.lean`, `lake-manifest.json`, `lean-toolchain`; `README.md`, `MISSING.md`, `ASSEMBLY.md`, `PROVENANCE.md`, `ACKNOWLEDGEMENTS.md`, `AGENTS.md`, `docs/VERIFICATION_20261006.md`; the run’s `summary.json`, `provenance.json`, `independent-review.json`; the final audit’s structure and axiom map |
| Run here | [`devtools.audit_n11_lean`](../../../packing/devtools/audit_n11_lean.py): `scan`, a streamed read of the commit’s archive with every Lean module hashed and scanned ([`receipts/tree-scan.json`](../../../packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/receipts/tree-scan.json)); `axioms`, the axiom receipt extracted from the pinned final audit ([`receipts/lean/axioms-public-theorems.json`](../../../packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/receipts/lean/axioms-public-theorems.json)); `build`, the statement closure built from the retained bytes (§5) |
| Not done here | A build of the whole proof: 7,920 modules, which the source ran on a 64-worker runner and whose compiled objects alone are about 7.94 GB beyond Mathlib’s, on a host with 4 shared cores and under 12 GB of free disk |

## 2. The Claim Against the Theorem, Line by Line

The public theorems are in `Optimality.lean`, in `namespace ElevenSquare`:

```lean
theorem optimal_side_lower_bound {S : ℝ} (h : Packable 11 S) : T ≤ S
theorem optimality : Optimality
```

with `Optimality` from `Foundations.lean`:

```lean
def Optimality : Prop := Packable 11 T ∧ ∀ S : ℝ, Packable 11 S → T ≤ S
```

| `T-060` says | The formalization says | Where | Agrees |
| --- | --- | --- | --- |
| $s(11) = T$: the least side of a square holding eleven unit squares is $T$, attained | `Packable 11 T` and every `S` with `Packable 11 S` has `T ≤ S`; definitionally `IsLeast {S | Packable 11 S} T` (§5 checks this by `Iff.rfl`) | `Foundations.lean`, `Optimality.lean` | Yes |
| Eleven squares | `squares : Fin 11 → UnitSquare` | `Geometry.lean`, `Packing` | Yes |
| Unit squares, closed | `UnitSquare` is a `center : ℝ × ℝ` and an `axis : ℝ × ℝ` with `normSq axis = 1`; `ClosedSquare q p` is `|localX q p| ≤ 1/2 ∧ |localY q p| ≤ 1/2`, the coordinates of `p - center` along `axis` and its perpendicular | `Geometry.lean` | Yes: side 1, closed |
| Any orientation, independently | Each square has its own unconstrained real unit axis | `UnitSquare` | Yes |
| The container | `InContainer S p` is `0 ≤ p.1 ≤ S ∧ 0 ≤ p.2 ≤ S`; `contained`: every point of every closed square is in it | `Geometry.lean`, `Packing` | Yes: the closed $[0,S]^2$, axis-aligned without loss of generality |
| Boundary contact allowed | Containment is of closed squares in a closed container; only open interiors must be disjoint | `Packing` | Yes |
| Disjoint interiors | `OpenSquare` is the strict version of `ClosedSquare`; `interior_disjoint`: for `i ≠ j` no point is in both open squares | `Geometry.lean`, `Packing` | Yes |
| A packing exists at side $S$ | `Packable n S := Nonempty (Packing n S)`; `Packing` also carries `side_nonneg : 0 ≤ S`, which any packing of a unit square implies | `Geometry.lean` | Yes; the extra field is harmless |
| $T = (6u+4)/(1+2u-u^2)$ | `def T : ℝ := (6*u+4)/(1+2*u-u^2)` | `Endpoint.lean` | Yes, symbol for symbol |
| The polynomial | `endpointPolynomial x = 5 * x^8 - 10 * x^7 - 2 * x^6 + 14 * x^5 + 12 * x^4 - 6 * x^3 + 2 * x^2 + 2 * x - 1` | `Endpoint.lean` | Yes, term for term |
| $u$ the unique root in $(9/25, 37/100)$ | `u := Classical.choose endpoint_root_exists`, a root in `(rootLo, rootHi)`, two 30-digit rationals inside $(9/25, 37/100)$; `u_unique`: any root in the closed $[9/25, 37/100]$ equals `u`, from the derivative’s positivity there | `Endpoint.lean` | Yes: existence, location and uniqueness are proved, not assumed |
| $T = 3.8770835900228141773078970601…$ | Not stated; `EndpointBounds.lean` proves $191/50 < T < U$ with `U = 387708359002281417731/10^20`, and the register’s decimal is below `U` by about $2 \times 10^{-21}$ | `EndpointBounds.lean` | Consistent; the decimal is the register’s |
| No uniqueness of the packing | None stated | — | Yes |

**Name resolution.** `Optimality.lean` writes `Optimality`, `Packable` and `T` inside
`namespace ElevenSquare` with no `open`. They resolve to the definitions above: Lean
refuses a second declaration of the same name, the namespace’s own declarations come
before any at the root, no module defines a `Pending.T`, `Pending.Packing` or
`Pending.Packable` (`ElevenSquare/Pending/`, `Interop/` and `Simplified/` were
searched), and in code no module anywhere in the archive has an `export`, an
`open … renaming`, a notation, macro, syntax or elaborator declaration or attribute
(§4). The four `instance` declarations in the archive are `Decidable` instances, and an
instance declared later cannot change a definition already elaborated in `Foundations`’
closure, which was built here from the same bytes at the same toolchain.
The probe of §5 declares a root-level `T` and `Packable` and checks that inside
`namespace ElevenSquare` the names still mean the source’s, by `rfl` and `Iff.rfl`. Two
things need the full environment and were not done: printing the type of
`ElevenSquare.optimality` itself, and re-checking the compiled declarations in the
kernel with `lean4checker`.

**The top of the lower bound.** `Pending.global_lower_bound P` is
`Tasks.T07.global_lower_bound_of_case438_certificate case438_near_certificate P`
(`GlobalComposition.lean`): from a packing at side $S < T$ it builds a centred case-438
packing, and the certificate `Case438NearCertificate` places its squares in the focused
local chart of Trump’s construction, where `focused_centered_requires_T` forces side
$T$. The certificate is `Ext.case438_near_certificate'` (`UnfinishedCapture.lean`,
`Ext/Case438Global.lean`), proved from the role-near-box state of the capture traces.
These three modules are retained; what they import is pinned by hash only.

## 3. The Axiom Receipt

The source’s finalizer parses `#print axioms` from the run’s compiler logs into the
final audit, which is pinned in the packet by SHA-256 and whose decompressed digest
matches `summary.json`. For `ElevenSquare.optimality`,
`ElevenSquare.optimal_side_lower_bound` and `ElevenSquare.Pending.global_lower_bound`,
it records exactly:

- `propext`, `Classical.choice` and `Quot.sound`;
- 13,308 axioms named `<declaration>._native.native_decide.ax_<i>_<j>`, owned by 10,464
  declarations, the whole of the audit’s `native_certificate_axioms`.

No `sorryAx` and no other axiom appears for any of the audit’s 2,234 targets.
The three certificate targets depend on 3,346 (baseline), 1,832 (prior) and 3,920
(returned) of the native axioms.
This is the source’s record of its run, consistent with itself; nothing here ran
`#print axioms` on the full proof.

**What the native axioms trust.** Each is the proposition a `native_decide` call
evaluated with compiled code, admitted as an axiom; the kernel never checks it.
The theorem therefore trusts Lean’s compiler, code generator and runtime, and any
`implemented_by` or `extern` in Lean core, Batteries or Mathlib that the evaluated code
reaches, such as the GMP-backed arithmetic of `Nat`. The project itself adds none (§4).
That is the trust model the source names, `lean_kernel_and_native_compiler`, and it is
weaker than a kernel-only check: the record must not describe this theorem as using “the
standard axioms only”.

**What the axiom map cannot exclude.** The source’s finalizer recognises an approved
native axiom by its name, `(.+)\._native\.native_decide\.ax_[0-9]+_[0-9]+`
(`native_axiom_owner` in `scripts/verify_support.py`). A hand-written
`axiom <owner>._native.native_decide.ax_1_1 : False` would pass it.
That no such declaration exists is the archive scan’s finding (§4), so for this one
property the scan is load-bearing and not a premise check beside the axiom map.

**A difference from the 4 October report.** wand125 reported on jlevy/squares#317 that
the 76 prior-family and the 173 returned cases are kernel-checked with Lean’s standard
axioms only. That describes wand125’s proofs of those components.
In this integrated snapshot, `prior_certificate_exists` and
`returned_certificate_exists` depend on 1,832 and 3,920 `native_decide` axioms: the
integrated certificates are decided natively.

## 4. Kernel Escapes on the Critical Path

`devtools.audit_n11_lean scan` read all 7,928 `.lean` files of the commit’s archive,
1,053,173,196 bytes, from 19:20 to 19:31 UTC, without extracting it.
For each of 25 tokens,
[`tree-scan.json`](../../../packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/receipts/tree-scan.json)
records its pattern, its counts in the raw text and in the code (comments, strings, raw
strings and character literals blanked, offsets kept), zeros included, and the path,
line and in-code flag of every raw hit of a token with at most 200:

| Token | In code | Raw hits | Load-bearing |
| --- | --- | --- | --- |
| `native_decide` | 10,464 uses in 1,839 files: the inventory’s counts exactly | the same | Yes. All 13,308 generated axioms are in the public theorem’s axiom set |
| `axiom` declaration | 0 | 1, a doc-comment of `Pending/S06_Baseline.lean` line 11 (“axiom acceptance”) | Yes: §3 |
| `sorry`, `admit` | 0 | 4 `sorry`, in doc-comments of `Pending/S06_Data.lean`, `S07_Bridge.lean`, `S08_Packet.lean` and `Types.lean` | — |
| `implemented_by`, `extern`, `unsafe`, `opaque`, `csimp`, `ofReduceBool`, `trustCompiler`, `decide +native` | 0 | 0 | — |
| `debug.skipKernelTC`, `#exit`, `#eval`, `run_cmd`, `run_elab`, `run_meta`, `run_tac`, `modifyEnv`, `addDecl`, `setEnv`, `initialize` | 0 | 0 | — |
| `notation`, `infix`, `prefix`, `postfix`, `macro`, `macro_rules`, `syntax`, `elab`, `declare_syntax_cat`, elaborator attributes, `export`, `open … renaming` | 0 | 0 | — |
| `instance` | 4, in 3 files, each a `Decidable` instance | 4 | No escape |
| `import Lean…` | 9 files, each `import Lean.Elab.Tactic.Omega` (the `omega` tactic); 8 in the build | 9 | No escape |

**The scanned bytes are the run’s.** The SHA-256 of every one of the 7,920 modules in
the archive equals the final audit’s `source_sha256` entry for it; none is missing and
none differs. The eight other `.lean` files (the lakefile, two script fixtures, five
simplification benchmarks) are outside the build.
The three build pins hash to the digests in `provenance.json`, and the `ElevenSquare`
and `Sqpack` trees are the Git objects `summary.json` records for the verified commit
`1bf942a7`.

The scan is a token count, not a parse: a construct spelled in a way no pattern matches
would pass it. `tests/test_audit_n11_lean.py` holds each pattern to an example of the
construct and the stripping to nested comments, strings, raw strings and character
literals.

## 5. The Statement Closure Built Here

`ElevenSquare.Foundations` imports no `Pending` module, so every definition the public
statements use, and the construction that attains $T$, build without the proof.
Its closure is 18 modules, about 410 KB, retained in the packet byte for byte.
`devtools.audit_n11_lean build` staged them from the packet’s retained bytes, which
`devtools.acquire_source --check` holds to the upstream manifest, and built them on 6
October from 19:34 to 19:42 UTC one module at a time in import order, with `nice -n 10`
and `LEAN_NUM_THREADS=2`, on `leanprover/lean4:v4.34.1` (commit `5045d005`, the compiler
string the source’s run reports) and Mathlib `d13f23b7` from its official cache, which
was fetched whole and then pruned to the 1,836 Mathlib modules the closure imports to
fit the disk. All 18 built with exit 0, and no Mathlib module was rebuilt.
[`build-statement-closure.log`](../../../packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/receipts/lean/build-statement-closure.log)
is the receipt, every command with its complete output.
A first build, from 18:49 to 18:57 UTC by a one-off script, gave the same results.

Then
[`AuditN11Statement.lean`](../../../packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/receipts/lean/AuditN11Statement.lean),
written for this audit, elaborated against those definitions with no error; its output
is at the end of the same receipt.
It checks the claim against the formal statement in Lean rather than by reading:

- `Optimality ↔ IsLeast {S : ℝ | Packable 11 S} T` by `Iff.rfl`: the statement is
  $s(11) = T$ with the minimum attained, by definition;
- `T = (6u+4)/(1+2u-u^2)` by `rfl`, and `endpointPolynomial x` equal by `rfl` to the
  register’s polynomial written out term by term here;
- `u ∈ (9/25, 37/100)`, `endpointPolynomial u = 0`, and every root in $[9/25, 37/100]$
  equal to `u`, from the source’s lemmas;
- `#print` of `Point`, `dot`, `normSq`, `perp`, `UnitSquare`, `localX`, `localY`,
  `ClosedSquare`, `OpenSquare`, `InContainer`, `Packing` and `Packable`, which are the
  definitions §2 quotes;
- two controls that the definitions are not vacuous: the axis-aligned square at centre
  $c$ is exactly $[c_1 - 1/2, c_1 + 1/2] \times [c_2 - 1/2, c_2 + 1/2]$, and two unit
  squares do not pack in a square of side 1 (`¬ Packable 2 1`);
- with decoys named `T` and `Packable` declared at the root, `T` and `Optimality` inside
  `namespace ElevenSquare` are still the source’s, by `rfl` and `Iff.rfl`.

`#print axioms` gives `[propext, Classical.choice, Quot.sound]` for
`construction_packable : Packable 11 T`, the upper half, and for `u_unique`, `T_lt_U`,
`optimality_of_lower_bound`, `improvement_within_cover` and
`packing_has_canonical_mask`. The upper half is therefore kernel-checked here with the
standard axioms only: Trump’s packing at side $T$, in the source’s exact construction.
The lower half, `optimal_side_lower_bound`, is the part that needs the 7,920 modules,
and this build says nothing about it.

The build is recorded as `E-n011-lean-statement-closure-build`, an upper-bound entry
replayed here, cited by the case record and not by `T-060`, whose `C` rests on its lower
half. `devtools.audit_n11_lean stage` writes the same closure and probe for anyone to
build.

## 6. Findings

None blocks recording the formalization as the source’s report.

- **F-1, the source’s comments are stale** (non-blocking).
  The doc-comment of `Optimality.lean` says its conclusions remain “UNPROVED until
  `global_lower_bound` and all of its dependencies have clean audits”; that of
  `global_lower_bound` calls it “conditional on the explicitly admitted exclusions and
  case438 capture”; that of `Pending/S06_Baseline.lean` says “full compiler and axiom
  acceptance of the new dependency path remains to be checked”; and
  `verification/admissions.json` still reads `SOURCE_COMPLETE_REPLAY_PENDING`. The proof
  bodies are unconditional, and the final audit’s axiom map, with no `sorryAx`, is the
  source’s record that the bound is proved.
  Worth reporting upstream.
- **F-2, compiler trust** (non-blocking for statement fidelity; binding on wording).
  The theorem is not kernel-only (§3). Every view of `T-060` that mentions the
  formalization must say so, and a human formalization review has to accept that trust
  explicitly under its `axioms` check.
- **F-3, the run is not public** (non-blocking for the import; it sets the encoding).
  EvolvingPrograms/11SquaresEvolving and run 37414883750 answered 404 here.
  What the source publishes of the passing run is its summary, provenance, integration
  review and final audit; the integration commit itself was not run in Actions, and its
  acceptance rests on the byte correspondence that §4 re-checked at module level.
  A run nobody here can inspect is the source’s report, and the evidence entry says so.
- **F-4, a resumed run** (non-blocking).
  The run reused validated receipts; the finalizer checked each compiled object’s hash
  against its receipt and the axiom reports against the logs, and the integration review
  did not rehash the objects.
  No cold build of the whole proof is on record anywhere.
- **F-5, two libraries, two settings** (non-blocking).
  `Sqpack` compiles with `autoImplicit=true`, `ElevenSquare` with `false`. The public
  statements are in `ElevenSquare`, so an implicit variable cannot enter them silently.

## 7. Verdict

Read here, the formal statement says what `T-060` says, with the same exact $T$ and the
same model, and the definitions of square, rotation, containment and disjoint interiors
are the register’s. By the source’s final audit and the scan here, the critical path
holds no `sorry`, no declared axiom and no `implemented_by`; it holds 10,464
`native_decide` declarations, which are load-bearing and disclosed by the source.
Recorded as `E-n011-lean-formalization-report`, the source’s reported proof-assistant
run with its axiom receipt, and the build here as `E-n011-lean-statement-closure-build`.

## 8. What `V5` Still Needs

Two records, neither of which exists.

**A complete build the record can rest on.** `V5` asks for proof-assistant evidence with
a certificate, a passing replay and an axiom receipt.
The source’s run is private and is recorded as reported, so the build has to be one this
record holds: the 7,920 modules built from the retained pin at its toolchain, here as a
`replayed-here` entry with its own `#print axioms` receipt, or by a third party whose
build is retained here.
The source’s workflow is manually dispatched and resumable on a GitHub runner, and its
README gives the command, `bash scripts/run_verification.sh --bootstrap --jobs N`; a
host needs room for about 8 GB of compiled objects beyond Mathlib’s.

**A human expert’s formalization review.**
[epistemics.md → Review Records](../../../epistemics.md#review-records) asks for one:
`kind: formalization`, `reviewer_kind: human`, `independent_of_author: true`, by a named
person who states their competence in Lean and in the mathematics and is not the
formalization’s author, with `checked` including `statement-fidelity`, `definitions`,
`axioms` and `build`, an accepting verdict, and the document mapped in
[`document-map.yaml`](../document-map.yaml) as a non-superseded review.
The `build` check should read the build above, not the source’s self-report.
This audit is none of that: its reviewer is an AI and the importing lane.

**Whether the owner can serve.** The epistemics names no exception for him and none
against him, and he may write the record if he can state that competence and has checked
the four items himself.
Two facts bear on `independent_of_author`, and his record should state both: the
announcement thanks him, as @ojoshe, “for aiding in the process”, and the
formalization’s exact $T$ and construction come from this project’s formulas, which
`ACKNOWLEDGEMENTS.md` credits.
A reviewer outside both would make the independence plain.
No such record exists, and none is written here on his behalf.

## 9. The Adversarial Review and Its Dispositions

The [adversarial review](review-2026-10-06-n11-lean-formalization-adversarial.md), by a
separately prompted Claude Opus 5.5 (tbd-strong agent, xhigh reasoning) on commit
`22208da56`, found the statement faithful and returned `defect-open` with two blocking
and six non-blocking findings.
Each is dispositioned here, in the commit that follows it.

| Finding | Disposition |
| --- | --- |
| 1, blocking: the source’s private run was encoded as `assurance: verified`, `replay_status: passed`, which let one review derive `V5` | Accepted. Re-encoded as the source’s report (`E-n011-lean-formalization-report`: `reported`, `reported_method: proof-assistant-checked`, `not-attempted`), as stage 3 and the precedent `E-k2m4-evand-lean-report` do. `T-060`’s `next_rung` and §8 now ask for a build the record holds as well as the review. Counting a source’s own run toward `V` is the owner’s policy decision, not this record’s |
| 2, blocking: the receipts came from one-off code and recorded less than the audit claimed | Accepted. [`devtools.audit_n11_lean`](../../../packing/devtools/audit_n11_lean.py) now does the scan, the extraction and the build, with `tests/test_audit_n11_lean.py`. The scan was re-run: every token’s pattern and counts, zeros included, and every raw hit with its line; `export`, `open … renaming`, elaborator attributes, `addDecl`, `setEnv` and `instance` added; character literals and raw strings handled. The build was re-run with every command’s complete output. §3 and §4 now say the absence of `axiom` declarations is load-bearing |
| 3: Square Packing Fan credited as an author without support | Accepted. Removed from the bibliography’s `authors`; the post is described as the announcement, which names neither the repository nor who did the work |
| 4: `after Kleddamag` not in the source’s files | Accepted. The credit is `Queuingtheorydotcom et al. after Levy, Daniel` |
| 5: “complete build” and “states exactly” overstate | Accepted. Each view now says the source reports a full verification run, resumed from earlier receipts, and that the statement audit reads the theorem as $s(11) = T$ |
| 6: `V5`’s requirements and the owner question understated; the checker does not tie a formalization review to a formalization | Accepted for the first two (§8, `next_rung`). The checker gap is reported to the coordinator for a bead, outside this lane |
| 7: the lower bound’s immediate dependencies not retained | Accepted. `UnfinishedCapture.lean`, `GlobalComposition.lean` and `Ext/Case438Global.lean` are retained, and §2 reads them |
| 8: trust model and AI assistance stated correctly | No action |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
