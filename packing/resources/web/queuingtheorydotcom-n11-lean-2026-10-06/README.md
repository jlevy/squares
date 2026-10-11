# The Lean Formalization of Eleven-Square Optimality, Pinned 2026-10-06

This packet retains
[Queuingtheorydotcom/11SquaresFormalized](https://github.com/Queuingtheorydotcom/11SquaresFormalized)
at the commit that integrated what it presents as a complete Lean 4 proof of `T-060`’s
claim: Trump’s packing of eleven unit squares is optimal, $s(11) = T$. The repository’s
public theorem is `ElevenSquare.optimality : ElevenSquare.Optimality`, and its README
reports that the proof passed a full verification run and final axiom audit, with
numerical certificates trusted to Lean’s compiler through `native_decide`.

Mannaseh Ahmed, who posts on X as
[@ManassehA06](https://x.com/ManassehA06/status/2107508501610217640), announced the
formalization on 6 October 2026, so the announcement is the author’s own.
The retained post is the first of a thread and does not name the repository; the rest of
the thread was not retrieved (X answered 429). The same day the owner, Joshua Levy,
quoted it in [a post of his own](https://x.com/ojoshe/status/2107513739222380935) that
gives the formalization’s context and calls it “a Lean formalization from @ManassehA06”,
and confirmed that @ManassehA06 on X and Queuingtheorydotcom on GitHub are the same
person. The same X account announced 11SquaresOptimal, `T-060`’s source, on 29
September, when this record took it down as @MathCompSciFTW’s.
This import has no issue of its own: jlevy/squares#317, the owner’s $n = 11$ umbrella,
is where wand125 reported on 4 October that both Lean formalizations were in progress.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/Queuingtheorydotcom/11SquaresFormalized> |
| Revision | [`cdc746ed907d258057c283aeb6d077cb2c27e349`](https://github.com/Queuingtheorydotcom/11SquaresFormalized/tree/cdc746ed907d258057c283aeb6d077cb2c27e349), tree `54168511`, “Credit Julian-JJ for enabling proof execution on an HPC cluster”, the third of three commits that day after `b237948f` of 30 September |
| Committed | 2026-10-06T05:23:42Z (01:23:42 in the commit’s −04:00), by the generic identity “Square Packing Contributors” that `docs/PUBLICATION.md` describes |
| Retrieved | 2026-10-06T18:41Z, a blobless, depth-1, sparse clone; `main` pointed at this commit |
| Licence | No licence file at the root and none stated in `README.md`. `integrations/wand125/` keeps three MIT notices for the incorporated work of wand125 and Evan Daniel, and `PROVENANCE.md` says it assigns no new licence to anything else |
| Announcement | Ahmed as @ManassehA06 (display name “Square Packing Fan”, account 1499452114313129988), 2026-10-06T16:29:17Z, retained as [`receipts/announcement/tweet-2107508501610217640.json`](receipts/announcement/tweet-2107508501610217640.json), the post as X’s syndication endpoint returned it at 18:43Z |
| Owner’s post | Joshua Levy ([@ojoshe](https://x.com/ojoshe/status/2107513739222380935)), 2026-10-06T16:50:05Z, quoting the announcement; retained as [`receipts/announcement/tweet-2107513739222380935.json`](receipts/announcement/tweet-2107513739222380935.json), as the same endpoint returned it at 22:22Z. It is a long post, edited once from 2107513041701273913 of 16:47:19Z; the endpoint returns only its first 276 characters, as does X’s oEmbed endpoint, and the rest was not retained |
| Earlier announcement | 11SquaresOptimal’s, 2026-09-29T03:17:20Z, which the 29 September intake recorded as @MathCompSciFTW’s and the [review article](../../../devtools/templates/n11-optimality-review-article.md) still links at that handle; retained as [`receipts/announcement/tweet-2104772485816168618.json`](receipts/announcement/tweet-2104772485816168618.json), fetched at 22:22Z, when X served it as @ManassehA06’s, from account 1499452114313129988 |
| Request | None. Bead `think-8spq` (epic `think-wyf4`) imports it at the owner’s request; jlevy/squares#317 is the $n = 11$ umbrella |

The proof sources are not this repository’s own history. `README.md`, `ASSEMBLY.md` and
`PROVENANCE.md` say they were imported unchanged from EvolvingPrograms/11SquaresEvolving
commit `1bf942a7af1ea330e95489d8997deebd4227ca71`, the commit whose Actions run
37414883750 passed. That repository and its run are not public: the API answered 404 to
both on 6 October. What is public is this commit, and the run’s portable evidence it
publishes under `verification/completed-run-20261006/`. The `ElevenSquare` and `Sqpack`
trees here, `675fd364` and `fba7b404`, are the Git objects `summary.json` records for
the verified commit.

## Credit and AI Assistance

The repository’s own files say who did what, in `ACKNOWLEDGEMENTS.md`:

- EvolvingPrograms and @ctjlewis provided the verification infrastructure and supported
  the complete replay in 11SquaresEvolving;
- @wand125 wrote the n11-optimality-lean formalization, certificate checkers, generated
  proofs, interoperation work and Lean-version ports that are incorporated;
- Benjamin Gurevitch helped with T03 and its returned-case formalization;
- @Julian-JJ, a collaborator, worked out how to run the proof on an HPC cluster;
- @Guzhou0806 contributed proof, transport and independent verification work;
- @Queuingtheorydotcom made the underlying computer-assisted proof
  (11SquaresOptimal, `T-060`’s source) and developed and integrated this formalization;
- Walter Trump found the packing, jlevy/squares supplied the exact packing formulas and
  related mathematical work, and Evan Daniel the square-packing definitions and
  containment checker the upstream formalization uses.

The announcement reads, in full: “The optimality of the packing for 11 squares has been
formalized in lean thanks to Astra and Claude! Huge thanks to @ojoshe, @kleddamag,
@wand_125, @guzhou0806, and @ctjlewis for aiding in the process.” @ojoshe is Joshua Levy,
this project’s owner. The post links this project’s $n = 11$ page as its image credit.
It is the author’s own announcement: @ManassehA06 is Ahmed, whom
`ACKNOWLEDGEMENTS.md` credits with developing and integrating the formalization.
The owner’s post quoting it reads, as far as X returned it: “Exciting to see a
resolution of the long-standing geometry problem of packing 11 squares.
The proof is layered with an optimality proof and now a Lean formalization from
@ManassehA06 assembled over the last few days, with assistance from @ctjlewis
@guzhou0806 and others. It…”. The record credits the formalization from
`ACKNOWLEDGEMENTS.md`.

**AI assistance, in the source’s own terms.** The author’s announcement credits Astra and Claude
for the formalization. The repository’s files make no statement of AI assistance:
`AGENTS.md` is a set of rules addressed to agents working on the formalization, and
`PC_RESUME.md` and `SIMPLIFICATION_HANDOFF.md` name working branches with the prefix
`codex/`. No commit at the pin carries an AI co-author trailer.

## What the Source Claims

From `README.md`, `MISSING.md` and `docs/VERIFICATION_20261006.md`, with the run’s
`summary.json`, `independent-review.json` and final audit:

- **The theorem.** `ElevenSquare/Optimality.lean` proves
  `optimal_side_lower_bound {S : ℝ} (h : Packable 11 S) : T ≤ S` and
  `optimality : Optimality`, where `Foundations.lean` defines
  `Optimality := Packable 11 T ∧ ∀ S : ℝ, Packable 11 S → T ≤ S`.
- **The run.** All 7,920 local modules were accepted in run 37414883750 at Lean
  `v4.34.1` and Mathlib `d13f23b7`, with zero inventoried admissions and 2,234 audited
  theorem targets; status `OPTIMALITY_PROVED_WITH_NATIVE_CERTIFICATES`.
- **The trust model.** `lean_kernel_and_native_compiler`: 10,464 approved numerical
  declarations in 1,839 files use `native_decide`, which adds 13,308 auxiliary axioms;
  geometry, checker soundness and assembly are ordinary kernel-checked proofs. The
  README says outright that this is not a kernel-only verification.
- **What the integration did not do.** The integration review reconciled the run’s
  source hashes, receipts, dependency edges and axiom logs, but did not recompile the
  proof or rehash the roughly 7.94 GB of compiled objects. The run resumed from validated
  receipts, so its duration is no cold-build timing.

## What Is Retained

The scope is the files a reader needs to judge the statement and the build: the root
files and build pins, the documentation and notices, the 18 modules of
`ElevenSquare.Foundations`’ closure (every definition the public statements use, and the
construction that attains $T$), `Optimality.lean`, `Verification.lean`,
`Pending/S09_GlobalLowerBound.lean` and the three modules the lower bound is assembled
from at the top (`Tasks/T07/UnfinishedCapture.lean`, `GlobalComposition.lean` and
`Ext/Case438Global.lean`), the verification runner, finalizer and source checker, and
the completed-run evidence. Its 59 files, 2,678,406 bytes, are in the manifest
([`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256)); 57 are
retained under [`11SquaresFormalized/`](11SquaresFormalized/), byte-identical, 546,987
bytes. Two are **pinned by digest only**:

- `verification/completed-run-20261006/final-audit.json.gz` (965,439 bytes), because an
  upstream `.gz` cannot be stored as itself here; its decompressed SHA-256 is the
  `d66a07c2…` that `summary.json` records, and the receipts below keep what this record
  uses from it;
- `verification/native-certificates.json` (1,165,980 bytes), the inventory of approved
  `native_decide` declarations, as bulk data (`OR-18`).

The rest of the tree, 7,920 Lean modules and about 1.09 GB, is pinned by the commit and
by the per-module SHA-256 map in the final audit.
[`devtools.acquire_source`](../../../devtools/acquire_source.py) `--check` re-derives the
packet from its manifest.

## Receipts

- [`receipts/lean/axioms-public-theorems.json`](receipts/lean/axioms-public-theorems.json)
  is the axiom receipt, extracted from the pinned final audit, whose decompressed SHA-256
  matches `summary.json`. `ElevenSquare.optimality`, `optimal_side_lower_bound` and
  `Pending.global_lower_bound` each depend on exactly `propext`, `Classical.choice`,
  `Quot.sound` and the 13,308 auxiliary axioms that `native_decide` generated, owned by
  10,464 declarations; no `sorryAx` and no other axiom appears for any of the audit’s
  2,234 targets. The certificate targets `baseline_certificate_exists`,
  `prior_certificate_exists` and `returned_certificate_exists` depend on 3,346, 1,832
  and 3,920 of them. The source’s finalizer parsed these from the compiler logs of the
  run; nothing here ran `#print axioms` on the full proof.
- [`receipts/lean/native-axioms.txt.gz`](receipts/lean/native-axioms.txt.gz) lists the
  13,308 auxiliary axioms, sorted, one per line.
- [`receipts/tree-scan.json`](receipts/tree-scan.json) is a streamed read of the
  commit’s archive from `codeload.github.com` on 6 October, from 19:20 to 19:31 UTC,
  nothing extracted to disk. The SHA-256 of every one of the 7,920 modules equals the
  final audit’s `source_sha256` entry for it, none missing and none different. For each
  of 25 tokens it records the pattern, the counts in raw text and in code (comments,
  strings and character literals blanked), zeros included, and every raw hit’s path,
  line and in-code flag. In code there is no `sorry`, `admit`, `axiom` declaration,
  `implemented_by`, `extern`, `unsafe`, `debug.skipKernelTC`, `#eval`, `run_cmd`,
  environment modification, `export`, `open … renaming`, notation, macro, syntax or
  elaborator attribute; the raw `sorry` and `axiom` hits, four and one, are in comments
  of `Pending/` modules. `native_decide` appears 10,464 times in 1,839 files, the
  inventory’s counts; `instance` four times, each a `Decidable` instance; and
  `import Lean.Elab.Tactic.Omega` in nine files.
- [`receipts/lean/build-statement-closure.log`](receipts/lean/build-statement-closure.log)
  is the build here, on 6 October from 19:34 to 19:42 UTC by
  `devtools.audit_n11_lean build`, of the 18-module closure of `ElevenSquare.Foundations`
  from these retained bytes, at `leanprover/lean4:v4.34.1` with Mathlib `d13f23b7` from
  its official cache: every command with its complete output, every module exit 0, and
  then the output of
  [`receipts/lean/AuditN11Statement.lean`](receipts/lean/AuditN11Statement.lean), the
  probe written here: the definitions printed,
  `Optimality ↔ IsLeast {S | Packable 11 S} T` by `Iff.rfl`, `T` and the polynomial
  checked by `rfl` against the register’s exact form, two controls, and
  `construction_packable : Packable 11 T` on `propext`, `Classical.choice` and
  `Quot.sound` only. A first build, from 18:49 to 18:57 UTC by a one-off script, gave the
  same results. The
  [statement audit](../../../../docs/project/reviews/review-2026-10-06-n11-lean-formalization-statement-audit.md)
  reads them.

The three checks are repeated from this packet by
[`devtools.audit_n11_lean`](../../../devtools/audit_n11_lean.py): `axioms` and `scan`
take a downloaded copy of the final audit and refuse one whose SHA-256 is not the
manifest’s, and `stage --out W` writes the statement closure, the pins and the probe,
ready for `lake exe cache get`, `lake build ElevenSquare.Foundations` and
`lake env lean AuditN11Statement.lean`. The register records the build as
`E-n011-lean-statement-closure-build` and the source’s run as
`E-n011-lean-formalization-report`.

## Compressed Files

| Stored file | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `receipts/lean/native-axioms.txt.gz` | receipt | `486abace0097387f6d5067e53bb24f8754819c8e` | `597a75fb856f7159d637d101f21270b6a39bfc93cdb5cb4756173125e879f418` |
