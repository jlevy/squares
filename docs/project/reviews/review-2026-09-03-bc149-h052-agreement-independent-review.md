# BC-149 — Independent Review of the H-052 Complete Agreement (exp-059)

## Provenance and installation

This document is the review deliverable of BC-149, the independent review of the H-052 complete agreement (exp-059), written on 2026-09-03 in the
agenda-016 ten-hour run. Its author wrote only to `scratchpad/bc149/`
-- a container-local directory outside the repository, which does not survive the
session -- and modified no repository file. It is installed here so that the evidence the
records cite outlives that directory.

The source was `316` lines with SHA-256
`dc1548ff7227171c1770cfaacc88e8420ffb6944827d7b1c1991a2fc5d702d78`, and that hash names the scratchpad
source rather than this file. The installation added this preface, and reformatted the body to
house Markdown conventions; it altered no classification, verdict, finding, number,
citation, recommendation or claim boundary, and none may be altered here. References of
the form `scratchpad/...` in the body below are the reviewer's own record of what was
read and where it was written at review time, and are left as written.

* * *

Independent reviewer, Agenda 016 block BC-149, hypothesis H-052. I authored none of the
successor package, the run, or its records.

- Repository `/home/user/squares`, branch `claude/squares-pr76-overnight-run-tpc888`.
  The review began at HEAD `2796174b` with the two exp-059 result files untracked;
  during the review the coordinator committed them unchanged as `ceff4400` (the
  committed result blob hashes to `438dfc1f…`), so the packet is now bound at one
  revision. The engine commit `2f112f4c` is an ancestor, and the four driver and test
  files hash identically at `2f112f4c`, at HEAD and in the working tree.
- Interpreter `/home/user/squares/packing/.venv/bin/python3` (Python 3.14.7). Bare
  `python3` was never invoked.
- Writes went only to `scratchpad/bc149/` and its `replay-root/`. No repository file was
  created, modified or deleted; no `git add`, `commit` or `push`; the `needs_review`
  flag on exp-059 was left as it was.
- Pre/post digests of the result, checkpoint and four ancestor artifacts are identical
  across every replay (`logs/refusals.log`).

## Classification: Pass

Every reported figure reproduces exactly, the whole admission boundary replays, the
decision derives from the emitted evidence, and a third implementation of my own
reproduces all 181 rows.
Under the repository’s decision rule (exact decision, replay, mutation and claim
boundary reproduce) this is a **pass**. It authorizes the coordinator to clear
`needs_review` on exp-059 and to open BC-150.

Three instrument limitations are recorded below.
None bears on the 181-cell agreement or fired on this round; each names its repair.
One of them is a record-accuracy correction that should travel with the flag clear.

**Scope.** Agreement decides implementation agreement only: two accumulations of one
retained certificate agree on every direction cell.
It is assurance evidence.
It is not new mathematics, not an independent proof method, and not adoption of the
4.5058 bound; BC-150 audits the mathematical implication separately, and no frontier or
result-registry file changes on this determination.

## Independence Assessment (Obligation 5)

This is the finding to read first, because the word “fresh successor implementation”
invites a stronger reading than the code supports.

**The successor adds no arithmetic.** Its module docstring says so (`run.py` line 3),
and its `SuccessorChainDriver` defaults are the unchanged exp-049 accumulators imported
through the resume driver (`run.py` lines 92–93 and 924–925). What is fresh is the
chain, checkpoint, ancestry and assembly layer.
The agreement exp-059 completes is therefore the exp-049 pair’s agreement, carried to
all 181 directions; the independence to assess is exp-049’s.

**What the two paths share.** Both `accumulate_source_faithful` and
`accumulate_target_independent` import the same `reduce_event_cells` from `geometry.py`
(`source_faithful.py` line 7, `target_independent.py` line 7). That one function fixes
everything up to the per-cell mass: the projection convention, the atom rectangles, the
u and v event sets, the center-domain polygon, its clipping, and the list of candidate
cells. It is a close transcription of the retained source’s own `verify_orientation`
scaffolding (`clip_u`, `center_domain`, the slab loop).
Both paths also share `fixture.py` (orbit expansion, grid coordinates, weight
normalization through `_normalized_atoms`), `model.py`, and a single implementation of
`_preconditions` and `_mutation_guards`.

**What the two paths compute differently.** Only the mass at each candidate cell.
The source-faithful path fills a two-dimensional difference array and takes two
cumulative-sum passes, mirroring the source’s `diff.cumsum(axis=0).cumsum(axis=1)`. The
independent path, for each cell center, builds a one-point `Fixture` and calls the
clean-room `accumulate_direction`, which sums the weights of the atoms whose projections
fall in the closed window (`target_independent.py` lines 32–44). That is direct
membership summation, O(cells × atoms), against range addition, O(cells).

**What the comparison can and cannot see.** A `DirectionManifest` has ten fields.
Eight of them (`label`, `direction`, `x_events`, `y_events`, both event hashes,
`event_cell_count`, `evaluated_state_count`) are outputs of the shared reduction and are
equal by construction.
Only `minimum` and `witness` are produced by different code.
I checked that this residual comparison is real rather than tautological by injecting
defects into a copy of the sweep and comparing with the frozen independent path on the
real direction 0 (`logs/defect_injection.log`):

| Injected defect in the sweep | Detected | Sweep minimum |
| --- | --- | --- |
| second cumulative pass dropped | yes, `minimum` and `witness` differ | `-215/192` |
| wrong sign on one difference-array corner | yes | `-113/6` |
| every rectangle’s top edge extended by one event | no | `1` |

The third row is inherent to comparing minima: a defect that only raises masses at
non-minimizing cells is invisible.
The registered criterion is on minima, so this is a scope statement, not a flaw.

**Verdict on independence.** The agreement establishes accumulation-level independence
over a shared reduction: for all 181 directions and all 16,562,293 candidate cells, the
range-addition accumulation reproduces the direct membership sums at the minimizing
cells, and the two select the same witness.
It does not independently establish the cell reduction, the fixture reconstruction, the
projection convention, the preconditions or the mutation guards, all of which are
single-sourced; an error in any of them would appear in both paths identically.
H-052’s regime permits sharing “the fixed certificate, mathematical definitions, and
invariant manifest but not the published accumulation control flow”, and the shared
reduction sits inside that permission.
The record’s wording that the paths agree on “event-cell reductions” should be read as
“use the same reduction”.

**A third path closes most of that gap at the implementation level.** `my_eval.py`
imports nothing from the repository.
It parses the hash-verified retained source, builds the 168 atoms and 181 directions
itself (its atom hash is `37d35da0…` and its direction hash `cc789e1a…`, matching the
summaries), forms its own event lists and domain clipping, and computes every cell mass
as an integer matrix product `U · diag(w) · Vᵀ` of membership matrices, a different
control flow from either repository path.
It reproduces all 181 rows: `x_events`, `y_events`, `event_cell_count`, `minimum` and
`witness`, in 7.5 s (`my_eval_summary.json`). That covers the reduction and the fixture
reconstruction as implementations.
It does not cover the mathematics: whether checking cell centers of this reduction
suffices, whether the shrink-and-scaling step is sound, and whether the source’s reading
of the certificate is the one intended are BC-150 questions.

## Replay Register (Obligation 1)

Every check below ran from my scratch scripts; the driver itself cannot be pointed at a
temporary root (`_production_paths` refuses any path but the preregistered three, and
`run_target` refuses because the result exists), so the replay is by re-derivation from
the published bytes plus the synthetic suites.

| Check | Result |
| --- | --- |
| Result bytes: SHA-256 `438dfc1f…`, 10,923,451 bytes | reproduced |
| Checkpoint bytes: SHA-256 `bb45ed2a…`, 10,947,228 bytes; `checkpoint_sha256` in the record matches | reproduced |
| Canonical under `model.py:101` (`canonical_json` + newline) and under my own `json.dumps(sort_keys=True, separators=(",", ":"))` | both files, byte-exact |
| `validate_result` on the published record | passes |
| `verify-ancestry` CLI: both ancestries verified, 0 target directions evaluated, 1.9 s | reproduced |
| Frozen package manifest by the resume driver’s recipe and by a shell equivalent | `309ec241…` |
| Four frozen sources (`README`, two HTML pages, retained verifier `04531a54…`) | digests match |
| Driver hashes: successor `ab4dd8fe…`, resume `3e5284fd…`, child `f4522750…`, test `dbe1032f…`, clean room `55d36239…` | match binding and record |
| `preconditions`, `shrink_and_scaling`, `mutation_guards`, `fixture`, `frozen_expectations` blocks recomputed through the frozen code | byte-identical to the record |
| The same preconditions recomputed by my own arithmetic from `L, M, B, T, KMAX` | 181 unit directions, 180 gap bounds, quarter-turn bracket, `B(1+T/K) = 899635478111/900000000000 < 1`, `L = (L−M) + M` |
| `atom_hash`, `direction_hash`, `fixture_hash` | reproduced |
| Both 181-row summaries: 168 atoms, `37d35da0…`, `cc789e1a…`, `203/12`, global minimum `1/1` | byte-identical to each other and to the checkpoint rows |
| Rows 170–180 recomputed through the frozen accumulators on this host (3 workers, 155–188 s per independent call, 0.6–1.0 s per source call) | all 11 source and independent manifests byte-identical to the checkpoint rows; all 11 row hashes reproduce, ordinal 180 to `60e58a70…` |
| Self-test, normal and `-O`: 115 guards, 0 skipped, receipt `0109332a…`, stdout `875722ce…` | byte-identical |
| `pytest` successor, child and base n17 suites under a scratch `basetemp` | 39 passed in 4.9 s |
| Interruption control (`test_interrupted_then_resumed_matches_uninterrupted`, guards `interrupted-resume-equivalence`, `no-partial-row-promotion`) | pass |
| Overwrite refusal: `run_target` on the preregistered paths | refused, “result path already exists”, nothing written |
| Fresh-path refusals: exp-056 checkpoint and progress, exp-052 checkpoint, the three frozen packages, lexical `..`, absolute outside path, any path carrying `exp-056` | all refused; a fresh slug inside the root is accepted |
| Progress marker absent after the run; `--status` reports 181 rows, 11 new, complete, all agree | reproduced |
| Run window 08:59:33Z–09:32:44Z is 1991 s; result and checkpoint mtimes 09:32 | consistent with the session record |

## The Decision Is Derived (Obligation 2)

`assemble_result` (`run.py` lines 1878–1940) builds the body without the six
decision-bearing fields, round-trips it through `canonical_json`, and only then sets
`preconditions_pass`, `all_mutations_rejected`, `frozen_invariants`,
`frozen_invariants_pass`, `instrument_valid` and `decision`, each from the emitted
fields. It returns `validate_result(record)`, and `run_target` (line 2166) publishes
nothing but that return value, through `_write_exclusive` (line 2222). `validate_result`
(lines 1590–1664) re-derives all six and refuses on any mismatch; `derive_decision`
(lines 1214–1230) reads only `instrument_valid`, `terminal_schema`,
`exact_manifest_agreement` and `first_disagreement`, and `_validate_agreement_body`
recomputes `exact_manifest_agreement` from the two parsed summaries.
The derivation chain is closed: there is no path that copies a stored decision through.
Re-running `derive_decision`, `derive_instrument_valid`, `derive_preconditions_pass` and
`derive_shrink_and_scaling_pass` on the published bytes returns `accepted`, `True`,
`True`, `True`.

Two qualifications, both confirmed by direct check rather than by the validator:

- The leaf booleans (`direction_unit`, the gap bounds, the five mutation outcomes) are
  computed once, at assembly, by `production_evidence`; the validator trusts them.
  I recomputed them through the frozen code and by my own arithmetic (above).
- `validate_result` is a self-consistency check that reads nothing but the record, so
  three anchors that tie the record to the world are not pinned by it: the
  `frozen_expectations` block is taken from the record rather than compared with
  `PRODUCTION_EXPECTATIONS`; the binding’s ancestor digests are not compared with disk;
  and the spine rebuilt from the summaries is not compared with `carried_boundary` (see
  limitation 1). All three hold here: `frozen_expectations` equals the production
  constants, the digests match disk, and `spine[169]` is `8947b38e…`.

## Chain Rebuilt From the Summaries Alone (Obligation 3)

`my_chain_rebuild.py` imports nothing from the repository.
With my own serializer and my own reimplementation of the row hash (domain
`n17-resume-paired-row-v1` over ordinal, direction, both manifests, agreement and the
previous hash) it rebuilds all 181 links from the two `CertificateManifest` summaries,
anchored at the exp-052 binding hash `2446fa39…`, and the rebuilt spine equals the
record’s `chain_spine` byte for byte.
It passes through `9badcc57…` at ordinal 32 (the exp-052 boundary) and `8947b38e…` at
ordinal 169 (the exp-056 boundary) and terminates on
`60e58a70c49fe6be879230c6305e59695364016ecdf1ba5ac3a305c12f5cb9a6`, the reported last
row hash. The same code rebuilds the checkpoint’s 181 rows with every
`previous_row_hash`, `row_hash` and `agreement` flag reproduced, and the summary rows
are byte-equal to the checkpoint rows.

## Ancestry: Immediate Parent and Carried Genesis (Obligation 4)

| Item | exp-056 (immediate parent) | exp-052 (carried genesis) |
| --- | --- | --- |
| checkpoint SHA-256 on disk | `0d39a7e7…` | `db5c1569…` |
| progress SHA-256 on disk | `0875f31f…` | `08e301b0…` |
| binding hash, recomputed by my own recipe from the checkpoint’s binding block | `18ec64b4…` (domain `n17-child-binding-v1`) | `2446fa39…` (domain `n17-resume-binding-v1`) |
| progress marker | ordinal 170, `independent_started`, bound to `18ec64b4…`, chained to row 169 | ordinal 33, `independent_started`, bound to `2446fa39…`, chained to row 32 |
| rows | 170; rows `[:33]` byte-equal to exp-052’s | 33 |
| result file | absent | absent |

The distinction is structural, not nominal: exp-056’s own row 0 chains to the exp-052
binding hash, not to its own, and exp-056’s binding block names exp-052 as its parent
with the matching digests, binding hash, last row hash and row count.
The exp-059 checkpoint’s rows `[:170]` are byte-equal to exp-056’s rows, its row 0
chains to `2446fa39…`, and the exp-059 binding hash `f7c93f05…` reproduces from the
binding block under domain `n17-successor-binding-v1`.

Non-substitutability was replayed on the real artifacts, read-only: exp-052 in the
parent slot, exp-056 in the genesis slot, swapped identities, a parent declared at
ordinal 169 or at stage `source_complete`, a genesis declared at `source_started`, a
wrong genesis anchor and a wrong genesis row count are all refused, while the genuine
specifications verify (`logs/refusals.log`). Git corroborates that the four ancestor
digests are unchanged since the last commit that touched them (`313624cc`).

## The Row Minima Are a Property of the Certificate (Obligation 6)

All 181 row minima being exactly `1/1` is what a tight linear-programming certificate
looks like, and the source’s own assertion is `global_min >= WEIGHT_SCALE`, that is,
minimum ≥ `576/576`. It is not an artifact of a comparison that cannot fail:

- The mass function is far from constant.
  By my third path, the per-direction maximum ranges from `187/96` to `131/48`, and the
  cells attaining the minimum number 172 to 7,272 of 2,025 to 94,293 per direction (1.0
  % to 8.5 %). The 181 witnesses are pairwise distinct.
- Two of three injected arithmetic defects change the minimum and are refused (table
  above).
- The self-test’s disagreement guards perturb a manifest by `+1` and confirm the stop,
  the retained row and the typed schema.
- `frozen_expectations.global_minimum` is `1/1`, the reduced form of the registered
  `576/576`, and `_summary_invariants` checks both summaries’ global minimum against it
  and against the minimum of their own rows.

## The Disclosed Limitation (Obligation 7)

Confirmed as stated.
`build_parser` (`run.py` lines 3277–3287) offers `--record`, `--selftest`, `--status`,
`--verify-ancestry` and `--calibrate`; nothing assembles a terminal schema from an
existing checkpoint.
On a `SuccessorDisagreementStopError`, `main` prints a status block and returns 3
without reaching `assemble_result` (lines 3308–3321). Schema (b) itself is sound: on a
synthetic chain it assembles from the retained checkpoint with all six absences declared
(`logs/adversarial.log`).

The statement is accurate but understates the trap.
Relaunching the identical command after a retained disagreement does not refuse: the
driver reloads the checkpoint, whose `_validate_rows` accepts a disagreeing row, and
continues from the next ordinal.
On the synthetic chain the relaunch appended the remaining direction, and the chain then
failed assembly with “the chain continued past its first disagreement”.
So after an exit 3 the operator must assemble schema (b) by a separate step before any
relaunch, and the readiness report’s “re-issue the identical command” applies to
interruptions only. It did not fire on this round.

## Limitations and Named Repairs

None of these prevents clearance; each names its repair and is a candidate for BC-155.

1. **The validator does not tie the rebuilt spine to the carried boundary.** I altered a
   carried row (ordinal 5) identically in both summaries, rebuilt the spine and
   `last_row_hash`, and left `carried_boundary` untouched; `validate_result` accepted
   the record although `spine[169]` no longer equalled `8947b38e…`. The exp-059 record
   and the readiness report say the validator “requires it to reproduce … the carried
   boundary 8947b38e… at ordinal 169” and that “an altered manifest therefore cannot
   survive”; that is true of the executed admission boundary (`_validate_rows` ties the
   prefix to exp-056 on disk before assembly) but not of `validate_result` alone.
   The published record satisfies the tie; I checked it directly.
   Repair: one comparison in `_validate_agreement_body` of
   `spine[binding.first_new_ordinal - 1]["row_hash"]` against
   `binding.immediate_parent.last_row_hash`, one guard, and a one-clause correction to
   the two documents. The same function could also pin `frozen_expectations` to the
   production constants when the binding names exp-059.
2. **No assembly path from a retained disagreement, and a relaunch spoils it** (above).
   Repair: an `--assemble` action that reads a checkpoint whose last row disagrees, and
   a refusal in `open_chain` when the loaded chain already carries a disagreement.
3. **Independence is at the accumulation level over a shared reduction.** This is within
   H-052’s registered regime and is a scope statement rather than a defect; the record’s
   “agrees on … event-cell reductions” should say “over the same event-cell reduction”.
   My third path is scratch evidence, not a repository artifact; if BC-150 wants an
   implementation-independent reduction on the record, `my_eval.py` is a starting point.

## Disposition

- Classification: **pass**.
- Authorized transition: exp-059 `needs_review` may be cleared by the coordinator; the
  decision `accepted`, its reason and the claim boundary stand unchanged.
  I did not edit the record.
- BC-150 opens on this pass.
  Its entry should carry limitation 1’s correction and read the independence assessment
  above before treating `validate_result` as sufficient evidence of anything beyond
  record self-consistency.
- H-052 is accepted at its registered scope: implementation agreement for this fixed
  certificate. Nothing here moves a bound.

## Replay Artifacts

All under `scratchpad/bc149/`. Scripts marked *own* import nothing from the repository.
Digests are the first sixteen hex characters of SHA-256.

| Path | Purpose | Digests (script, output) |
| --- | --- | --- |
| `check_result.py`, `logs/check_result.log` | canonical bytes, `validate_result`, field dump, derivations | `a1f1b7f60dd548b6`, `04422cd9e97c593b` |
| `my_chain_rebuild.py` (own), `logs/my_chain_rebuild.log` | chain rebuild, binding hashes, ancestry cross-checks | `177df6ca01752fb5`, `6cc8f7253003aebc` |
| `my_eval.py` (own), `my_eval_summary.json` | third-path evaluation of all 181 rows | `32911b97fca8d3ff`, `41d6994fc69dfb72` |
| `recompute_rows.py`, `rows/summary.json` | rows 170–180 through the frozen accumulators | `4b26fd018f202d11`, `92aa297dc080a83a` |
| `replay_evidence.py`, `logs/replay_evidence.log` | preconditions, mutations, fixture block, hashes | `2b451ac07fdecf53`, `55244be42fc55ff6` |
| `adversarial.py`, `logs/adversarial.log` | probe 1 (validator anchor), probe 2 (relaunch after disagreement) | `7acfccf7ffff55a0`, `baaccea8893cfb93` |
| `refusals.py`, `logs/refusals.log` | overwrite, fresh-path and swapped-ancestry refusals on the real artifacts | `c1d10fcb3b65604a`, `79365c05e491cbc7` |
| `defect_injection.py`, `logs/defect_injection.log` | discriminating power of the row comparison | `1622701de8f329d1`, `1ed5bb0f7918d335` |
| `logs/selftest_normal.json`, `logs/selftest_optimized.json` | byte-identical receipts | `875722ceea9ce17d`, `875722ceea9ce17d` |
| `logs/pytest.log`, `logs/verify_ancestry.log` | 39 passed; ancestry report | `b2215eddefb4fa11`, `93666ee10784432e` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
