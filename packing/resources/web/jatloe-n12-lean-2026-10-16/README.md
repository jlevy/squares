# Jatloe’s Lean Proof That s(12) = 4, Pinned 2026-10-16

This packet retains
[Queuingtheorydotcom/Jatloe12SquaresFormalized](https://github.com/Queuingtheorydotcom/Jatloe12SquaresFormalized)
at the commit its release `n12-verified-2026-10-16` tags: a Lean 4 proof that the least
side of a square holding twelve unit squares is 4, the side of the $4 \times 3$ grid.
Its one public theorem is `N12Compact.Final.optimality : S12.packingConstant12 = 4`, in
the project `Lean/Proofs/N12-jatloe`. The record held $s(12) \ge 7943/2000$ (T-095) and
the grid’s $s(12) \le 4$ before it, and no claim of the value.

Its Frontier key is **[Jatloe n12 Lean 2026-10-16]**. It reached the project through an
announcement on X, not an issue: the owner opened
[jlevy/squares#810](https://github.com/jlevy/squares/issues/810) on 25 October 2026 to
track it, and bead `think-4l14` owns its import.
The record registers it as `T-245` at `V0`/`C0`, as reported.
The claim below is stated as the source states it; nothing here has built the proof, and
no review has read it yet.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/Queuingtheorydotcom/Jatloe12SquaresFormalized> |
| Revision | [`d0caf4532a7ead68be1389ef87387b126fc2e0ab`](https://github.com/Queuingtheorydotcom/Jatloe12SquaresFormalized/tree/d0caf4532a7ead68be1389ef87387b126fc2e0ab), tree `0d50ba6e7d60b15fc62a0b2a83cfb4d014bd9574`, “Publish audited N12 proof and compiled-artifact provenance”, the sixth and last commit on `main`, which the tag `n12-verified-2026-10-16` names |
| Committed | 2026-10-16T05:12:49Z (01:12:49 in the commit’s −04:00), by Queuingtheorydotcom; the first commit, `e294e45`, is of 2026-10-15T16:26:13Z |
| Retrieved | 2026-10-25T05:34Z, a full clone; `git ls-remote` at 05:53Z gave `main`, `HEAD` and the tag all at this commit |
| Licence | No licence file anywhere in the tree, and none stated in `README.md`, `AGENTS.md` or `SOURCE-PROVENANCE.json`. What is retained rests on the owner’s decision of 9 October 2026 to keep upstream material that matters for the record and track its licence (epic `think-gtmb`); the follow-up for this source is `think-c9ec` |
| Pinned subtree | 426 files, 5,984,062 bytes, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) |
| Retained here | 423 files, 5,968,679 bytes as published, byte-identical under [`Jatloe12SquaresFormalized/`](Jatloe12SquaresFormalized/), five of them stored as deterministic gzip ([Compressed Files](#compressed-files)) |
| Announcement | Manasseh Ahmed as @ManassehA06 (display name “Square Packing Fan”, account 1499452114313129988, the account of the $n = 11$ announcements), 2026-10-22T02:36:07Z, retained as [`receipts/announcement/tweet-2113097037306569124.json`](receipts/announcement/tweet-2113097037306569124.json), the post as X’s syndication endpoint returned it at 2026-10-25T05:45:44Z (2,575 bytes, SHA-256 `ecd7b4a0b35dc95109fd231624e0b88faded812e991c7687fb72102694d7c00f`) |
| Reply naming the repository | The same account, 2026-10-22T02:36:20Z, in reply to the announcement, retained as [`receipts/announcement/tweet-2113097091580932578.json`](receipts/announcement/tweet-2113097091580932578.json), fetched at the same time (8,758 bytes, SHA-256 `e963dbe8f3b408699c61d2bcca44a571723216c23c01e6cfc1fdcac3a21181ba`) |
| Request | None from the authors. [jlevy/squares#810](https://github.com/jlevy/squares/issues/810), opened by the owner on 2026-10-25T05:38:24Z, labels `intake` and `n-12`; bead `think-4l14` |

**The upstream repository is not public.** `README.md` and `SOURCE-PROVENANCE.json` say
the proof sources are copied byte for byte from `EvolvingPrograms/SquaresLean`, branch
`main`, commit `1f60d412707aae824b76fbaf11d4e708695451fa`, whose Actions run 38849916588
(job 116808701733) accepted the theorem.
That repository asks for credentials, so neither the commit nor the run can be read from
here. What is public is this commit, the run’s evidence it carries under
`verification/run-38849916588/`, and the release’s assets.

**The release**
[`n12-verified-2026-10-16`](https://github.com/Queuingtheorydotcom/Jatloe12SquaresFormalized/releases/tag/n12-verified-2026-10-16)
carries three assets, none retained here:

| Asset | Bytes | SHA-256 | Read here |
| --- | ---: | --- | --- |
| `N12-jatloe-final-evidence-1.zip` | 2,934,549 | `db3447b212544e83028fdabd73cf3acd14b796e7ff977cbb899b6e7164b5d9f8` | Downloaded at 2026-10-25T05:46:14Z; its SHA-256 is this one |
| `N12-jatloe-compiled-checkpoint-38847898861.zip` | 1,033,472,991 | `7a20bbdfc76a6f066dc6795e3c50b38c81641c5e99d4dff47536cc6fc1772496` | Its size only, from the download’s headers; bulk under OR-18, not fetched |
| `SHA256SUMS` | 404 | `18d9fa813d995e9bd26c5d19bb511de5758410f53b2d449cfb00a3698a7c844b` | Downloaded; it lists the two archives above, and `SOURCE-PROVENANCE.json` and `compiled-checkpoint-verification.json` at the SHA-256 the retained copies have |

The evidence archive holds the run’s compiler logs, its receipt index, the per-module
receipts (`checked-modules.json`), the final report and the audits; the files the commit
keeps under `verification/run-38849916588/` are its own copies of the last of these.
The checkpoint archive holds a tar of 3,072,215,040 bytes: 5,377 `.olean` objects
(3,043,639,848 bytes), 5,377 compiler logs and the receipt index, saved by the earlier
run 38847898861 at `437041a0`, which failed later.
A replay here would rebuild the objects rather than fetch them.

## Credit and AI Assistance, as the Source States Them

`README.md`: “Jatloe provided the full mathematical proof and partial Lean
formalization. Ben Gurevitch aided in formalization.
**CTJLewis refactored and compiled the formalization.**” `SOURCE-PROVENANCE.json`
repeats the three as `credits`, and `AGENTS.md` tells agents working on the project to
“Preserve Jatloe’s, Ben Gurevitch’s and CTJLewis’s credits.”
Every commit is by Queuingtheorydotcom, Manasseh Ahmed’s GitHub account, as the record
has held since the owner’s confirmation of 6 October 2026; `SOURCE-PROVENANCE.json` says
the publication changed only “Documentation, pinned runtime/bootstrap and public replay
workflow” and preserved the proof’s Lean sources.

The announcement reads, in full: “The optimal packing of 12 squares is much nicer!
Thank you to @jatloe for sending me a full proof of the result alongside a partial
formalization, and thanks to all of the square packers who helped finish the
formalization”, then “Image source: https://jlevy.github.io/squares/atlas.html” and a
picture. @jatloe is X account 1339674174239944705, display name “jatloe”, as the post’s
`user_mentions` gives it.
The reply reads “@jatloe Lean repo:” and links the repository.
The source gives Jatloe no other name, so the record credits Jatloe by that name.
CTJLewis is the person the record holds as Lewis (GitHub and X ctjlewis), whom the
$n = 11$ formalization credits with its verification infrastructure.
Whether “Ben Gurevitch” is the Benjamin Gurevitch that formalization credits is not
stated here; the record does not join the two without that evidence.

**AI assistance, in the source’s own terms.** The repository makes no statement of AI
assistance, and the announcement names none.
`AGENTS.md` is a set of rules addressed to agents working on the formalization;
`Lean/Proofs/N12-jatloe/audit/BRANCHES.md` lists upstream working branches named
`codex/…` and `n12/worker-…-codex-…`;
`Compact/Completion/C981/SHORT-CERTIFICATE-ROUTE.md` describes “The coordinating root
agent” and “The child agent”; and `mathematics/README.txt` is written to “the user”, as
in “Compilation was explicitly deferred by the user.”
No commit at the pin carries an AI co-author trailer.

## What the Source Claims

From `README.md`, `SOURCE-PROVENANCE.json`, `verification/run-38849916588/README.txt`
and the run’s `github-replay.json` and `global-type-axiom-audit.log`:

- **The theorem.** `Compact/Assembly/Final.lean`:

  ```lean
  theorem optimality : S12.packingConstant12 = 4 :=
    SourceAssembly.optimality SourceAssembly.pending_closed
  ```

  in namespace `N12Compact.Final`, with no hypothesis.
  `source/S12/PackingConstant.lean` defines
  `feasibleSides : Set ℝ := {L | 0<L ∧ Nonempty (UnitPacking L)}` and
  `packingConstant12 : ℝ := sInf feasibleSides`, and proves `four_feasible` from
  `gridPacking : UnitPacking 4`, the $4 \times 3$ grid of axis-parallel unit squares.
  `source/S12/Normalization.lean` defines `UnitPacking L` as twelve `OpenSquare`s, each
  of `side = 1`, every point `Inside` one lying in $[0, L]^2$, and no point `Inside`
  two. `source/S12/Diagonal.lean` (namespace `S12Pilot`) defines an `OpenSquare` by `c`,
  `s` with `c ^ 2 + s ^ 2 = 1`, `loU`, `loV` and `side > 0`, and `Inside x y` as
  `loU < c * x + s * y < loU + side` and `loV < -s * x + c * y < loV + side`: an open
  square at any rotation and translation.

- **The proof’s shape.** The lower half normalizes a packing below side 4 into a
  `NormalizedPacking` of twelve congruent squares of a common side in $(1, 1001/1000]$
  inside $[0, 4]^2$ (`source/S12/Packing.lean`), and excludes every one through marker
  ownership and a classification into 117 original cases, each closed by a proof term
  (`Compact/Assembly/SourceAssembly.lean` and the 19 other modules of
  `Compact/Assembly/`). The written mathematics, 255 Markdown chapters and notes, 14
  text files and an index, is under `mathematics/`.

- **The run.** Run 38849916588 accepted all 5,377 project modules of the theorem’s
  closure at Lean `v4.35.0` and Mathlib `56a005855ea17e0b0958f73ec801ae140b0a1679`
  (4,049 external modules; 9,583 in all with setup and the audit), then elaborated
  `GlobalTypeAudit.lean`, which checks `example : S12.packingConstant12 = 4 :=
  N12Compact.Final.optimality` and prints its axioms; `global_optimality_proved` is
  `true` in `github-replay.json`.

- **The trust model.** The axiom list is `propext`, `Classical.choice`, `Quot.sound` and
  1,624 auxiliary axioms that `native_decide` generated
  (`…_checked._native.native_decide.ax_1`), with no `sorryAx` and no other axiom;
  `inherited_native_compiler_trust` is `true`. The README: “verification retains the
  documented native compiler trust of `native_decide`, in addition to Lean’s kernel.”

- **What the run did not do.** “All 5,377 module objects were reused from cache; this
  particular job was not a fresh compilation of every module.”
  The objects were compiled in earlier runs, and the checkpoint that preserves them
  comes from run 38847898861, which failed later; the successful run checked each reused
  object against its source, dependency, compiler, object and log receipts.
  `SOURCE-PROVENANCE.json` records `modules_freshly_compiled_in_this_run: 0` and
  `local_independent_full_rebuild_performed: false`.

## What Is Retained

The scope is what a reader needs to judge the statement and the run, and what the
mathematical review reads: the four root files, the two workflow files, the accepted
run’s evidence, the project’s build pins, README, profile, toolchain lock and replay
instructions, the 109-module import closure of `S12.PackingConstant` (every definition
the statement uses, and the grid), the 20 modules of `Compact/Assembly/` (the final
theorem and the assembly above it, 19 of them in its closure), and the written
mathematics under `mathematics/` (270 files).
Of the 426 files in the manifest, 423 are retained byte-identical at their upstream
paths under [`Jatloe12SquaresFormalized/`](Jatloe12SquaresFormalized/). Three are
**pinned by digest only**:

| Upstream path | Bytes | Why not retained |
| --- | ---: | --- |
| `ci/__init__.py`, `ci/scheduler.py` | 48 and 3,736 | The replay workflow’s job scheduler, a program that decides nothing about the theorem; fetched at the pin for a replay with the producer’s workflow |
| `verification/run-38849916588/check_compiled_checkpoint.py` | 11,599 | The source’s preservation checker for the checkpoint archive, which checks custody and not the proof |

The rest of the tree, 6,225 files, is pinned by the commit; 5,249 of them are modules of
the theorem’s closure, each also by its Git blob in the closure receipt below.
[`acquisition/sources.json`](acquisition/sources.json) records the pin and every file,
and from `packing/`,
`uv run --frozen --all-extras --group dev python -m devtools.acquire_source jatloe-n12-lean-2026-10-16 --checkout CHECKOUT`
rebuilds the packet from a checkout at the pin; `--check` re-derives it without one.

## Receipts

The two closure receipts were written here on 25 October 2026 by
[`devtools.lean_closure`](../../../devtools/lean_closure.py), which reads Git objects at
the pin and runs nothing from the source.
A token count is not a parse and not a build: it says what the text holds, and the axiom
set stays the source’s report until a build here prints it.

- [`receipts/lean-closure.json.gz`](receipts/lean-closure.json.gz), the closure of
  `Compact.Assembly.Final`: 5,377 project modules, 32,385,124 bytes, none missing,
  across the libraries `Compact`, `Completion` and `S12`. In their code, comments
  removed, there is no `sorry`, `axiom` declaration, `implemented_by`, `extern`,
  `unsafe`, `debug.skipKernelTC`, `ofReduceBool`, `+native`, `native := true`,
  `reduceBool`, `reduceNat` or `trustCompiler`; `native_decide` appears 2,572 times in
  42 modules. Outside the project it imports `Mathlib` (255 import lines), `Lean` (22)
  and `Std` (1). The manifest’s packages are `path` dependencies under
  `.lake/packages/`, so it pins no revision; the Lean and Mathlib pins are
  `lean-toolchain` and `verification/toolchain-lock.json`.
- [`receipts/statement-closure.json.gz`](receipts/statement-closure.json.gz), the
  closure of `S12.PackingConstant`: 109 modules, 1,138,482 bytes, all retained here.
  Its only kernel escape is `native_decide`, 723 times in 39 modules:
  `Normalization.lean` imports the case reduction (`S12.To117`), so its data modules
  come with the definitions.

From `packing/`, with a clone of the source as `CHECKOUT`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.lean_closure CHECKOUT \
  --commit d0caf4532a7ead68be1389ef87387b126fc2e0ab --root Lean/Proofs/N12-jatloe \
  Compact.Assembly.Final \
  --source-url https://github.com/Queuingtheorydotcom/Jatloe12SquaresFormalized --json OUT
```

and the same with `S12.PackingConstant` for the statement closure.

- [`receipts/statement-audit.json`](receipts/statement-audit.json), written the same day
  by [`devtools.audit_n12_lean`](../../../devtools/audit_n12_lean.py) for the
  [statement audit](../../../../docs/project/reviews/review-2026-10-25-n12-lean-formalization-statement-audit.md),
  which cites its counts. It reads every module of the closure receipt by its Git blob
  and counts, in code and in the raw text, the eleven-square audit’s escape tokens and a
  few more (`set_option` names, instance classes, `decide +kernel`, `noncomputable`), over
  the whole closure and over the statement closure; it lists every declaration of the
  statement’s names; it matches each of the 1,624 `native_decide` axioms of
  `global-type-axiom-audit.log` to the calls of its owner, 1,525 declarations, and lists
  by module the 948 calls in 749 declarations that no axiom of the final theorem
  reaches; and it holds every module’s bytes to the SHA-256 the run’s
  `verified-source-manifest.json` states, and the log and the manifest to the digests
  `SOURCE-PROVENANCE.json` records. None differs.

From `packing/`, with the same checkout, and then from the packet alone, which recomputes
the statement closure’s part and the run evidence:

```sh
uv run --frozen --all-extras --group dev python -m devtools.audit_n12_lean scan CHECKOUT
uv run --frozen --all-extras --group dev python -m devtools.audit_n12_lean check
```

## The Build Plan, Priced

A replay here is a fresh build of the theorem’s closure from the pin, accepted only with
the axiom list of `global-type-axiom-audit.log`: stage the project from a checkout at
the pin, put Mathlib `56a00585` at `.lake/packages/mathlib` with its official cache for
Lean `v4.35.0`, build `Compact.Assembly.Final`, and elaborate
`verification/run-38849916588/GlobalTypeAudit.lean`. The producer’s own route is its
public workflow (`.github/workflows/verify.yml` and `n12.yml`), which builds the modules
one at a time with two to four Lean threads each.

The source’s per-module receipts price it.
Every one of the 5,377 receipts in the evidence archive’s `checked-modules.json` has
exit status 0 and no rejected admission, and records its module’s compile time and Lean
threads:

```sh
unzip -p N12-jatloe-final-evidence-1.zip checked-modules.json | jq '[.[] | .record] |
  {modules: length, wall_s: (map(.elapsed_seconds) | add),
   thread_s: (map(.elapsed_seconds * .lean_threads) | add), max_s: (map(.elapsed_seconds) | max)}'
```

prints 5,377 modules, 59,586.74 wall-seconds and 138,504.10 thread-seconds, the longest
module 248.25 seconds.

| Item | Estimate |
| --- | --- |
| Toolchain | `leanprover/lean4:v4.35.0` and Mathlib `56a00585`’s cache for the 4,049 external modules, about 7 to 10 GB with the toolchain by the Mathlib caches fetched here before; the producer’s run held 6.76 GB of project files, and the objects alone are 3.04 GB |
| CPU | about 17 to 39 CPU-hours: 16.6 wall-hours of serial module builds, 38.5 if every Lean thread was busy throughout, by the source’s receipts; setup and the final audit add minutes |
| Memory | not recorded per module; the producer’s runner had 88 CPUs and 170 GB free, and ran the build under a resident-memory bound of 157,113 MiB |
| Subset | the 109-module statement closure, 9.4 wall-minutes and 37.5 thread-minutes by the same receipts, with a probe written for it, as the $n = 11$ statement audit’s was, printing the definitions and the axioms of `gridPacking` and `packingConstant12_le_four`; it decides the statement and the grid in Lean and moves no rung |

By the receipts the complete build fits the owner’s 40 CPU-hour item cap at its high
reading, just: it waits on a machine whose memory is known to hold the largest modules,
and on the pass’s decision to start it (`T-245`’s `unfinished_confirmations` names its
bead). This host, with 4 cores, 15 GB of memory and 20 GB of free disk on 25 October,
would take 17 wall-hours or more and might not hold it.

## Limitations

- **Nothing was built or run here.** The axiom list, the run and the receipts are the
  source’s, from a private repository whose commit and run cannot be read from here; the
  accepting run reused every compiled object, so no single run compiled the closure.
- **The written proof and the formal one are different objects.** The mathematics under
  `mathematics/` is the proof the formalization follows; whether every chapter is
  formalized, and whether the 117 cases exhaust the normalization, is for the review.
- **Comments and dated notes in the tree are historical.** Modules such as
  `SourceAssembly.lean` still say the assembly “awaits the final ordinary Lean replay”;
  the README says the run-specific evidence supersedes such text, and the files were
  kept unchanged.
- **No review has read it.** The statement audit and the mathematical review of stage 4
  start from this packet.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `Jatloe12SquaresFormalized/Lean/Proofs/N12-jatloe/mathematics/SOURCE-INDEX.json.gz` | upstream | `bc62066f80605a1ddc5b3d3001b8ef28ab947ac7` | `064383245921773cc72aafe4900e64bc6ad47b8b740c74df9902ca8f684ff10b` |
| `Jatloe12SquaresFormalized/verification/run-38849916588/github-replay.json.gz` | upstream | `3d6d8d123602bc600233d78170d0ece3e6a63f38` | `483e85130a7b4b31f22241c9d7725fbfc018809c158f23ea250f3c1546458798` |
| `Jatloe12SquaresFormalized/verification/run-38849916588/global-native-axiom-audit.json.gz` | upstream | `c2508c8f177c8a27d9f493b49041903e0f9cf731` | `3766dec1b81a61173703df53ca3cac88cee57636894d976c44f3b28ba8a585a1` |
| `Jatloe12SquaresFormalized/verification/run-38849916588/global-type-axiom-audit.log.gz` | upstream | `c908a5779bde67e7d8fd78376b29e8895037da3d` | `e76041bcaffad1adec4b43489a6352a700746281f7acdf4808c5ed990fb14b15` |
| `Jatloe12SquaresFormalized/verification/run-38849916588/verified-source-manifest.json.gz` | upstream | `00ed75dfd800938fec928a1b5f460b23748fa942` | `95fe302fa7a180af5b495656c08846d9c7a8bbd820df71d6608e0d66bb1409e0` |
| `receipts/lean-closure.json.gz` | receipt | `7624e84426b5896e03cc5abbd51b96821260a4b9` | `1c579c07c6027c73e28e56baef954fb590ec0473831a54b8c3b981d8d29a9400` |
| `receipts/statement-closure.json.gz` | receipt | `e1fed470c9fa4c1991e8723f65e039c637925692` | `65ee7a2004eefaf8acf760f09b4da9edfd0f0f7b9b04974ea18477c2f2659853` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
