# Fitzharding: A Lean Proof That s(17) = L, Pinned 2026-10-13

This packet retains
[ofitzharding/sq17-lean](https://github.com/ofitzharding/sq17-lean) at the head of
`main` on 13 October 2026, a Lean 4 proof that John Bidwell’s 1998 packing of seventeen
unit squares is optimal. Its theorem is

```lean
Sq17.square17_optimality (L : ℝ) :
  Sq17.HalfPlaneAssembly.PlainPacking L ↔ Sq17.EndpointGeometry.side ≤ L
```

where `EndpointGeometry.side` is the exact algebraic side of Bidwell’s packing,
approximately 4.675530093604551. The source trusts Lean’s compiler for 13,343
`native_decide` facts and reports a clean rebuild of the theorem’s 4,951-module import
closure.

The author, Oscar Fitzharding, announced it on X as
[@ofitzharding](https://x.com/ofitzharding/status/2109798000008597616) at
2026-10-13T00:06:56Z. He asked for its registration on this repository in
[issue #565](https://github.com/jlevy/squares/issues/565), opened at 2026-10-12T22:23:37Z;
the owner reported the repository and the post on 13 October 2026, asked for a full
intake crediting everything, and set Oscar Fitzharding as the definitive name. Bead `think-hcqr` imports it, and this packet
is its stage 2 retention (`think-acbk`). Nothing in the packet is a register entry, and
nothing here built the proof or ran the source’s scripts.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/ofitzharding/sq17-lean> |
| Revision | [`e6ee548090dc1dbf938ecf8590481de837a6a454`](https://github.com/ofitzharding/sq17-lean/tree/e6ee548090dc1dbf938ecf8590481de837a6a454), tree `5bee8a45`, “Cite published release while Zenodo DOI awaits activation”, the last of four commits |
| Committed | 2026-10-13T01:59:58Z (21:59:58 on 12 October in the commit’s −04:00), author and committer ofitzharding |
| History | `915afab` 2026-10-12T20:42:00Z, “Release source proof of optimality for seventeen unit squares”; `0a7167e` 22:06:08Z, “Record successful clean source rebuild and verification receipts”; `dc67357` 2026-10-13T01:31:15Z, “Add citation metadata and Zenodo release DOI”; then the pin. No commit carries a co-author trailer |
| Release | `v1.0.0`, which `CITATION.cff` ties to commit `0a7167efa8dcae7fa73855890630fb7e2de550ed` and dates 2026-10-12. The pin’s tree differs from that commit’s only by `CITATION.cff`. The import’s triage (bead `think-hcqr`) records the release as published at 2026-10-12T22:06:23Z |
| DOI | `dc67357` gave `doi: "10.5281/zenodo.23329216"` in `CITATION.cff`; the pin removes it, “while Zenodo DOI awaits activation” |
| Retrieved | 2026-10-13T17:37Z, a full clone; `main` pointed at this commit |
| Licence | MIT: `LICENSE`, “Copyright (c) 2026 Oscar Fitzharding”; `README.md`, “Project sources are licensed under the MIT License. Dependencies, including Mathlib, retain their own licenses.” |
| Announcement | Fitzharding as @ofitzharding (display name “Oscar”, account 2097726704118603776), 2026-10-13T00:06:56Z, retained as [`receipts/announcement/tweet-2109798000008597616.json`](receipts/announcement/tweet-2109798000008597616.json), the post as X’s syndication endpoint returned it at 2026-10-13T17:52:07Z |
| Request | [Issue #565](https://github.com/jlevy/squares/issues/565), “Complete Lean proof of s(17) optimality: registration request”, opened by ofitzharding at 2026-10-12T22:23:37Z; and the owner’s report of 13 October 2026 |
| Bibliography key | **[Fitzharding n17 Lean 2026]** |

## Credit and AI Assistance

`CITATION.cff` names one author, given name Oscar and family name Fitzharding, and asks:
“If you use this formal proof or its verification software, please cite this release.”
`LICENSE` carries the same name. The owner set Oscar Fitzharding as the definitive name
on 13 October 2026.

`README.md`, section Credits, reads in full:

> John Bidwell discovered the packing in 1998, improving Pertti Hämäläinen’s 1980
> arrangement; see [Friedman’s survey](https://erich-friedman.github.io/papers/squares.pdf).
> The [Squares Project](https://github.com/jlevy/squares) collects the wider research
> record. Mannaseh Ahmed and collaborators’
> [eleven-square formalization](https://github.com/Queuingtheorydotcom/11SquaresFormalized)
> provided a useful reference for computer-assisted formalization and its trust
> boundary. David MacIver’s
> [earlier Lean work](https://github.com/DRMacIver/square-packing-research) concerns a
> lower bound for seventeen squares.
>
> A search on 12 October 2026 of public Lean repositories, theorem statements, the
> Squares Project records, arXiv and public Lean-community indexing found no earlier
> complete Lean proof of this optimality result. Earlier formalizations of
> seventeen-square constructions or weaker lower bounds do not establish its global
> optimality.
>
> Marc Overbeck published an independent
> [candidate proof of seventeen-square optimality](https://github.com/Kleddamag/the-seventeenth-square-candidate)
> on 12 October 2026, using mathematical arguments and Python and JavaScript certificate
> checkers. This repository presents a separate Lean formalization.
>
> This project was developed with substantial assistance from Claude and Codex. The
> published theorem, source files and explicit trust boundary are the basis for
> assessing the result.

The record holds each work it names: the eleven-square formalization is
[`[Ahmed 11SquaresFormalized 2026]`](../queuingtheorydotcom-n11-lean-2026-10-06/README.md),
MacIver’s repository is the
[MacIver packet](../maciver-square-packing-2026-09-07/README.md), and Overbeck’s
candidate is [`[Overbeck n17 candidate 2026]`](../kleddamag-n17-candidate-2026-10-12/README.md).

The announcement reads, in full: “17 squares. No smaller square. I’ve released the first
complete Lean proof of optimality for Bidwell’s 1998 packing of 17 squares. Built with
@OpenAI Astra + @AnthropicAI Opus 5.5. Thanks to @ManassehA06 & @ojoshe for prior
work.” It links this repository and an image. @ManassehA06 is Mannaseh Ahmed and
@ojoshe is Joshua Levy, this project’s owner. X reported a conversation count of 3 when
it was retrieved; no reply was retrieved.

**AI assistance, in the source’s own terms.** `README.md` says the project “was developed
with substantial assistance from Claude and Codex”; the announcement says it was “Built
with @OpenAI Astra + @AnthropicAI Opus 5.5”.

## What the Source Claims

From `README.md`, the retained Lean files and `verification/`:

- **The statement.** `PlainPacking L` (`PackingStatement.lean`) says there are 17 sets,
  each a unit square in the sense of `SquareBase.lean` (the closed square of some centre
  whose sides are parallel to a unit vector and its normal), each inside
  `containerBox L = [0, L]²` (`PropagationWall.lean`), with pairwise disjoint interiors.
  Rotations are arbitrary and boundary contact is allowed. `side = (6+4t)/(1+2t−t²)`
  (`EndpointGeometry.lean`), where `(t, β)` is the common zero of two integer
  polynomials in the box of radius `1/10¹²` about a stated 60-place decimal midpoint, which
  `EndpointRoot.lean` proves unique there by a Newton contraction (`EndpointRootData.lean`,
  `PolynomialNewtonRoot.lean`, `PolynomialBoxContraction.lean`). The theorem includes
  existence at the endpoint, `endpoint_plainPacking : PlainPacking EndpointGeometry.side`.
  The theorem file also proves `square17_feasible_iff` for `Feasible L`, the same
  statement over centres and unit directions (`HalfPlaneAssemblySkeleton.lean`), and
  `feasible_iff_plainPacking` proves the two predicates equivalent.
- **The trust boundary.** “The geometric soundness arguments are checked by Lean’s
  kernel. The large finite certificate checks are evaluated as compiled native code and
  introduced through `native_decide`.” The Lean compiler, native evaluator and C
  toolchain are trusted, alongside `propext`, `Classical.choice` and `Quot.sound`. The
  README says this follows the eleven-square formalization’s trust model and that “This
  is not a kernel-only computation claim.”
- **The clean rebuild.** “All 4,951 modules in the final theorem’s import closure were
  rebuilt from the published sources on Linux with Lean 4.34.1. No precompiled project
  proof objects from the research checkout were used; the pinned third-party dependency
  cache was reused.” Independent checks were distributed between two Linux machines.
  `clean-build-receipt.json` records `CLEAN_SOURCE_BUILD_ACCEPTED`, 4,951 modules
  rebuilt, 13,343 `native_decide` facts, no unexpected axiom, the axiom set matching the
  local build, and both optional controls at exit 0.
- **What it does not claim.** “The receipt records successful reproduction; it does not
  replace the proof sources or the stated trust assumptions.” The controls, a feasible
  two-square packing, nonvacuity of the production wrappers and legal boundary contact,
  “supplement that review; they do not replace checking the mathematical definitions and
  the complete proof.”

`HalfPlaneAssemblySkeleton.lean` opens by calling itself “A checked, CONDITIONAL assembly
skeleton” with “no unconditional optimality theorem” in that file. The theorem file
does not use its conditional `feasible_iff`: it applies `plainPacking_iff_of_1563` and
`feasible_iff_of_1563` from `HalfPlaneLastCase.lean` to
`Propagation.HalfPlaneState.T1563.full_dispatch`, and neither file is retained here.

## The Release Archives

The proof’s 3,738 generated modules are not in the Git tree. `README.md` says to download
three certificate-source archives from release `v1.0.0` into `certificates/`; they hold
Lean source, not compiled proof objects. `manifest.json` gives each archive’s size and
SHA-256, and the size and SHA-256 of every one of the 4,953 source modules, with the
archive that carries it:

| Archive | Format | Bytes | SHA-256 | Modules | Module bytes |
| --- | --- | --- | --- | --- | --- |
| `generated-sources.tar.gz` | tar.gz | 718,897,665 | `5e0f823f9853b18509f2001e94dab9fea200eaa88bef2dd0b9200c97bd16f029` | 526 | 2,316,893,868 |
| `ordinary-generated-sources.tar.xz` | tar.xz | 721,405,188 | `27770a1963be6264e368463d562d49eb90b8b38f1b2fae7dcef8c56b7785c83c` | 2,832 | 3,104,229,541 |
| `tree1563-sources.tar.gz` | tar.gz | 522,564,562 | `37f0e0174eb4195798e1a0f11f8d9f20ada412b8655985e138b7931917363b5a` | 380 | 1,565,188,303 |

Together they are 1,962,867,415 bytes, about 6.99 GB of Lean source when unpacked.
Their bytes are not retained (`OR-18`); they are pinned here by name, size and SHA-256.
The import’s triage compared these digests with the SHA-256 digests GitHub reports for
the release assets and found them equal. This lane could not repeat that comparison:
GitHub’s API for the repository was not enabled in the session, and only Git reads were
served. On 13 October 2026, addressing review A of PR #588, `generated-sources.tar.gz`
was downloaded from the release and found to have the size and SHA-256 `manifest.json`
gives ([`receipts/closures.json`](receipts/closures.json)); it was then deleted. The other
two archives were not downloaded (`think-c1kz`).

## What Is Retained

The scope is what a reader needs to judge the statement and the source’s own replay
receipt: the root files and build pins, `manifest.json`, the two scripts, `verification/`,
the theorem file, the nine files whose definitions its two statements use, the two
optional control modules, and the two data files the packet’s comparisons read beside
this project’s own. Its 28 files, 3,694,177 bytes, are in the manifest
([`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256)); 27 are
retained under [`sq17-lean/`](sq17-lean/), byte-identical, 3,531,560 bytes, two of them
as deterministic gzip (below).

| Retained | Why |
| --- | --- |
| `README.md`, `CITATION.cff`, `LICENSE` | The claim, the credit, the licence |
| `lean-toolchain`, `lakefile.toml`, `lake-manifest.json` | The build pins: Lean `v4.34.1`, Mathlib `v4.34.1` at `d13f23b7` |
| `manifest.json`, stored as `manifest.json.gz` | The source’s binding of every module and archive to its SHA-256; 2,104,650 bytes, 285,911 stored |
| `scripts/unpack.py`, `scripts/reproduce.py` | The replay’s two commands: authenticate and extract the archives against `manifest.json`, then build the import closure. Read, never run |
| `verification/` | The source’s replay receipt: `clean-build-receipt.json`, the theorem’s axiom report `Square17Optimality.log` (1,115,493 bytes, 40,936 stored as `.gz`), and the two control logs |
| `Sq17Lean/Square17Optimality.lean` | The theorem |
| `PackingStatement.lean`, `HalfPlaneAssemblySkeleton.lean`, `SquareBase.lean`, `PropagationWall.lean` | `PlainPacking`, `Feasible`, unit squares, the container |
| `EndpointGeometry.lean`, `EndpointRoot.lean`, `EndpointRootData.lean`, `PolynomialNewtonRoot.lean`, `PolynomialBoxContraction.lean` | The side and the algebraic root that defines it; with `SquareBase.lean` they are the whole project-internal import closure of `EndpointGeometry.lean` |
| `HalfPlanePositiveControl.lean`, `HalfPlaneBoundaryControl.lean` | The two optional controls whose logs `verification/` keeps |
| `ExactCellCoverData.lean`, `RepresentativeCaseData.lean` | The 24 cells of the centre-box cover and the 35 excluded patterns, which [`receipts/cover-comparison.json`](receipts/cover-comparison.json) compares with this project’s cover and certified sub-pattern ledger; retained after review A of PR #588 |

**Pinned by digest only:** `.gitignore` (162,617 bytes, 3,746 lines), almost all of it
the paths of the generated modules that the archives carry, each of which
`manifest.json` lists.

**Not retained:** the other 1,201 Lean modules in the tree, 22,247,097 bytes of proofs
and certificate data, which the commit pins and `manifest.json` lists with their
digests; and the three archives above.
[`devtools.acquire_source`](../../../devtools/acquire_source.py) `--check` re-derives the
packet from its manifest.

## Receipts

- [`receipts/announcement/tweet-2109798000008597616.json`](receipts/announcement/tweet-2109798000008597616.json)
  is the announcement as X’s syndication endpoint returned it.
- [`receipts/source-consistency.json`](receipts/source-consistency.json) is the output of
  [`receipts/programs/check_source_manifest.py`](receipts/programs/check_source_manifest.py),
  run here on 13 October 2026 under Python 3.14.7 with `-I`, which reads the packet’s
  retained files and a checkout of the pin as data. It finds that the 1,215 modules
  `manifest.json` places outside the archives are exactly the tree’s 1,215 `.lean` files
  and that each has the size and SHA-256 recorded for it, as does each of the 12 root
  files it lists. For each archive it lists the member count `manifest.json` records
  beside the modules `manifest.json` assigns to that archive, and the two agree; it opens
  no archive, so both counts are the manifest’s own. In the axiom report it finds
  `Sq17.square17_optimality` depending on `propext`, `Classical.choice`, `Quot.sound` and
  13,343 distinct `native_decide` facts and on no other axiom, with no `sorryAx` anywhere
  in the log. The log’s SHA-256 equals the receipt’s `final_log_sha256`, and each control
  log equals the receipt’s digest. The root files were held to their SHA-256 alone until
  review B of PR #588 found the size missing; the program now compares both, and its
  output did not change.
- The review’s comparisons of the source with this project’s own $n = 17$ data
  ([review of 13 October](../../../../docs/project/reviews/review-2026-10-13-fitzharding-n17-lean.md),
  section 10) were scratch programs. After review A of PR #588 they are retained as
  first-party programs, `V-fitzharding-n17-premise-comparisons`, each reading the
  source’s files as text and executing nothing from it:
  - [`receipts/programs/compare_endpoint.py`](receipts/programs/compare_endpoint.py) →
    [`receipts/endpoint-comparison.json`](receipts/endpoint-comparison.json): the
    endpoint’s two polynomials, midpoint and radius equal exp-237’s certificate and
    H-255’s formulas term for term, and the side map is the record’s; the Lean’s Newton
    contraction certificate holds when recomputed; the side to 60 places,
    `4.675530093604550951634111270483146648767143855015879695416889`, lies in exp-245’s
    enclosure, is a root of the catalogue’s degree-18 polynomial by a sign change across
    $\pm 10^{-40}$, and is $1.04 \times 10^{-22}$ below the verified ceiling.
  - [`receipts/programs/compare_cover.py`](receipts/programs/compare_cover.py) →
    [`receipts/cover-comparison.json`](receipts/cover-comparison.json): the 24 cells equal
    `UNIQUE_24`’s (exp-247’s `ring-3-voronoi-8-tabbed-unique`) vertex for vertex, in the
    same order and under the same names, and none of the three other designs’; 32 of the
    35 patterns equal admitted entries of the certified sub-pattern ledger up to the
    cover’s eight symmetries (A, W7 and SW9; 18 admitted in exp-251, exp-254 and exp-256;
    11 of wand125’s, admitted in exp-317), and the other three lie strictly inside
    admitted entries.
  - [`receipts/programs/check_closures.py`](receipts/programs/check_closures.py) →
    [`receipts/closures.json`](receipts/closures.json): read on a checkout of the pin and
    `generated-sources.tar.gz`, every module of the 241-module import closure of
    `PackingStatement` (219 in the tree, 22 in that archive) and of the 18-module closure
    of `EndpointPacking` has the size and SHA-256 `manifest.json` gives, and none uses
    `native_decide` in code; the one textual match is a comment,
    `InteriorCellCapacity.lean` line 134.
- `sq17-lean/verification/` is the source’s own replay receipt, retained as it is
  published. Nothing here rebuilt any module, ran `#print axioms`, or ran the controls.

## The Second Review’s Programs

[review-2/](review-2/README.md) holds the programs of the
[second review](../../../../docs/project/reviews/review-2026-10-13-fitzharding-n17-mathematical-correctness.md),
the mathematical-correctness lane of 13 October 2026, kept as they ran, with the output
each printed. They read a checkout of the pin and members of `generated-sources.tar.gz`
as data and execute nothing of the source: an 80-digit re-derivation of the endpoint and
the frames, an exact rebuild of the census and the classifier, the cell geometry, an
exact recomputation of the 93-box dual certificate, and a Python transcription of the
compiled trace checker that re-evaluated ten of the 13,343 `native_decide` facts. Its
README says what each program read and decides, and the evidence entries that record
them; n-017’s case record cites those entries, and T-154 does not.

## Compressed Files

| Stored file | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `sq17-lean/manifest.json.gz` | upstream | `37df7bee2811cc0a627925018cfc5098d9650b64` | `ad1bf51e0bc2d05a449d30d23131cd1437312480525c38fb89a540d13ec8ac6d` |
| `sq17-lean/verification/Square17Optimality.log.gz` | upstream | `df47f876ef831efc6a2ca662c8927926cb8fa21d` | `5e74c4afe1e55f1e1c64193eb9a06aa413075a7355ad5faa108c4930da8ac241` |

`gunzip -k sq17-lean/manifest.json.gz sq17-lean/verification/Square17Optimality.log.gz`
restores the upstream bytes.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source fitzharding-n17-lean-2026-10-13 --check
uv run --frozen --all-extras --group dev python -m devtools.acquire_source fitzharding-n17-lean-2026-10-13 --checkout CLONE
.venv/bin/python3 -I resources/web/fitzharding-n17-lean-2026-10-13/receipts/programs/check_source_manifest.py resources/web/fitzharding-n17-lean-2026-10-13 CLONE
.venv/bin/python3 -I resources/web/fitzharding-n17-lean-2026-10-13/receipts/programs/compare_endpoint.py resources/web/fitzharding-n17-lean-2026-10-13 ..
.venv/bin/python3 -I resources/web/fitzharding-n17-lean-2026-10-13/receipts/programs/compare_cover.py resources/web/fitzharding-n17-lean-2026-10-13 ..
.venv/bin/python3 -I resources/web/fitzharding-n17-lean-2026-10-13/receipts/programs/check_closures.py resources/web/fitzharding-n17-lean-2026-10-13 CLONE ARCHIVE
```

`--check` re-derives the record from this packet alone; `--checkout` needs a clone at
the pin and refuses one that does not yield this record and manifest. The third command
reproduces `receipts/source-consistency.json`. The fourth and fifth need only this
packet and the repository, and reproduce `receipts/endpoint-comparison.json` and
`receipts/cover-comparison.json`; the last needs a clone at the pin and the release’s
`generated-sources.tar.gz` (`ARCHIVE`), and reproduces `receipts/closures.json`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
