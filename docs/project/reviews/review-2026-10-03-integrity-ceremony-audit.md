---
title: Integrity Ceremony Audit
date: 2026-10-03
status: planning-review
---
# Integrity Ceremony Audit

**Session:** 168, lane R7 (reviewer; read-only on code).
**Question:** which mechanisms in this repository hash, freeze, seal or digest-gate its
own files, what each one costs, and which of them cross a trust boundary that justifies
the cost. **Baseline:** `db370d14a`, the revert of the gmpy2 dependency that
`audit_kleddamag_n11_native` refused.
**Method:** every `hashlib` import and every 64-hex literal under `packing/` and
`packages/` read in context (106 `devtools` files, 10 `sqpack` modules, 62 test files,
29 case modules, 13 benchmarks, 8 workbench tools); every `git cat-file`, `git
show` and `rev-parse` comparison; the gate’s 89 steps; the four workflows; the budget
register and `suite-file-costs.json` for measured cost; the defect register, the bead
store and the Session 168 records for incidents.
Two gate steps were timed locally (`--only`). Nothing in the repository was edited
except this document and the document map.

The owner’s direction, 2026-10-03, which this review applies verbatim:

> why should changing any dependency cost 1.7 hours?
> what is the purpose of the ‘sealing’ at all?
> we want to use checks to validate correctness, but this is not an adversarial
> environment.

> It should never cost hours of verification time for internal bookkeeping.
> That’s needless ceremony.
> It makes no sense. In our project, we are not validating across a trust boundary.
> We’re worrying about correctness.

> We need determinism for sure, but determinism should not cost rerunning code.

## Verdicts

- **Forty-two items in ten families.** Twenty keep a named boundary, thirteen are
  replaced by Git revision, a semantic comparison or a small determinism test, six are
  removed, two families (the n11 proof chain and the retained cases) are frozen as-is
  with a ban on extension, and one family only records digests and gates nothing.
- **The three biggest taxes are all internal bookkeeping.** The n11 native audit freezes
  `pyproject.toml`, `uv.lock` and `.python-version` to blobs at `c183cc9a`, so any
  dependency change demands the 6,197 s native run again (the owner’s 1.7 hours; lane E1
  is removing it). The capture pilot refuses its own checkpoint whenever any byte of
  `sqpack/hull_kernel/` changes, which on 2026-10-03 sent a 256-row run back to round 0
  after a speedup whose output a test proves identical.
  The n17 ledger pins verifiers, receipts and verification receipts by SHA-256, so every
  verifier edit needs a review verdict on a digest, a ledger edit and a 242 to 4,258 s
  full re-verification to carry the new digest, and it needed that twice in one day.
- **The fixed-core calibration family is the largest standing cost in the suite**: 94.7
  s of the 1,213.6 s cohort (7.8 per cent) for tools that can only run at one commit,
  because `calibrate_fixed_core_packet` refuses unless `HEAD` equals the frozen revision
  and `read_fixed_core_calibration_profile` refuses unless `HEAD` equals the reader
  revision. The bead that would use them (`think-vy5i`) is paused.
- **The pattern already bit the public record.** `think-gzju` (P0, open) is a digest
  binding in the published n11 case-438 near-audit that fails while the geometry
  replays; the arity-8 selector receipts named bytes the run had not imported, because
  `module_sha256` was hashed at write time rather than import (`1d8577bca`); and `D-226`
  is CI discarding the history its own provenance gate needed.
  Each is a check catching a bug in the check.
- **What stays is short and nameable.** Downloaded packets against pinned values
  (Kleddamag, Kingbird, wand125, Tokoharu, Guzhou, Wang and Li, Evan D), the external
  `general_pose_tree` checker at a revision, Git ancestry checks (provenance, session
  gate), cache identities of generated artifacts (workbench page and video, the engine
  self-test binary), and dedupe ids.
- **OR-16 needs one more paragraph**, stated in section 5, so that “no SHA-256 manifests
  beside Git files” is read as also forbidding digest-gated refusals, frozen-blob
  comparisons and re-run obligations, which it was not: the ledger added
  `receipt_sha256` and `verification.sha256` a month after OR-16 was written.

## 1. The Test Applied

`tbd guidelines general-coding-rules` gives the test: a comparison adds assurance only
when the two values are computed independently with the data outside our control in
between. When one trusted process computes both sides, the check can only catch bugs in
itself. [development.md](../../../development.md#hashes-and-repository-owned-artifacts)
and OR-16 add the repository’s form of it: Git is the integrity boundary for
repository-owned files, so identify them by revision and path.

Three distinctions decide the verdicts below:

- **Naming is not checking.** A file named by the digest of its content is a reference,
  like a Git blob id. Refusing to read it because its bytes no longer hash to its name is
  the save-then-read round trip the guideline names as ceremony.
- **Determinism is proved by a small instance, never by a re-run.** A fast-tier test
  that produces a fixture and compares bytes is the proof.
  Refusing a retained result until a long computation runs again under the current bytes
  is not determinism; it is the cost the owner is objecting to.
- **A verifier’s independence is a design property; a digest is bookkeeping.** The
  kernel and branch-and-bound verifiers were written separately from the producers, and
  that stays. Which bytes a review admitted is a Git revision and a review document, not
  a 64-hex allowlist.

## 2. Inventory

Columns: where; what it gates; the failure it claims to detect; whether that failure
crosses a boundary we do not control; what already catches the real failure; measured or
estimated cost; verdict.
Costs are per gate run unless stated.
Test-file seconds are from `devtools/suite-file-costs.json`.

### 2.1 Family A: Environment Sealing

| # | Where | Gates | Claimed failure | Boundary | Caught otherwise by | Cost | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | `packing/devtools/audit_kleddamag_n11_native.py:41-92` (`PROOF_INPUTS`, `check_proof_code`): 16 source files plus `pyproject.toml`, `uv.lock`, `.python-version` must equal their blobs at `c183cc9a` | `tests/test_native_parent_core_receipt.py` in the quick lane (8.5 s) | the retained 6,197 s native run reused with changed code or dependencies | none: our tree against our history | the same test’s 19 semantic refusals on the receipt (claim, rows, bounds, budget); replay of a few rows | any dependency change costs the 6,197 s run again; gmpy2 (`c401c81d6`) was reverted in `db370d14a` for this | REPLACE: record revision and paths; drift informational (E1) |
| A2 | `packing/devtools/fixed_core_packet.py:86-90, 567-600, 1931-1953`: interpreter identity, `uv.lock` bytes, source manifest rows carry `git_blob` and `sha256` and must bind | `tests/test_fixed_core_packet.py` (23.1 s) | a packet run under another runtime or source | none | the packet’s own exact replay of the T-025 and T-026 sources | 23.1 s per suite; 98 tests with 38 digest references | REPLACE (E1) |
| A3 | `packing/devtools/calibrate_fixed_core_packet.py:819-842`: `HEAD` must equal the frozen revision, checkout clean, fixture digest fixed | `tests/test_fixed_core_packet_calibration.py` (24.0 s) | a calibration at another commit | none | the fixture’s reviewed answers (`test_frozen_cross_fixture_and_normalization_have_the_reviewed_answers`) | 24.0 s per suite; the tool cannot run at any other commit | REPLACE (E1) |
| A4 | `packing/devtools/verify_fixed_core_calibration_runset.py:51, 998-1125`: three profiles’ source manifests compared blob for blob | `tests/test_verify_fixed_core_calibration_runset.py` (2.1 s) | profiles from different sources | none | manifest paths equal; the profile contents agree | 2.1 s | REPLACE (E1) |
| A5 | `packing/devtools/read_fixed_core_calibration_profile.py:395-397, 509-513`: `HEAD` must equal the reader revision; every manifest row must hash to its execution blob | `tests/test_read_fixed_core_calibration_profile.py` (44.8 s) | a profile read by other reader bytes | none | the reader’s semantic checks of the profile | 44.8 s per suite, the costliest file of the family | REPLACE (E1) |

Family A together is 103.2 s of every suite run, and its real cost is the re-run it
demands of a 1.7-hour computation whenever `uv.lock` moves.
Lane E1 owns the implementation (`think-lhyk`); this review records the family for
completeness and agrees with its scope.

### 2.2 Family B: The n17 Digest Chain

| # | Where | Gates | Claimed failure | Boundary | Caught otherwise by | Cost | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B1 | `packing/devtools/pilot_n17_capture.py:131-136, 1497-1498`: `TOOL_SHA256` and `KERNEL_SHA256` (every `sqpack/hull_kernel/*.py`) must equal the checkpoint’s | `load_checkpoint`, so every resume | a checkpoint certified by other code | none | `pilot.replay` (`PASS_REPLAYED`, `final_state_agrees`), and every step was certified by the checker when written | the 256-row run started 04:54 UTC from round 0 because `841e368dd` (cached collision facets, proved equal to the reference by `test_hull_kernel_caches`) changed three kernel files; 42 min per round at the 128-row cap, 3-hour ceiling; the same run then refused its round-10 checkpoint (“the kernel changed since the checkpoint”) after an opt-in kernel change that is byte-identical by default | REMOVE the digest refusals; keep schema and settings; record revision |
| B2 | `packing/campaign/explorations/X048-session-168-pilots/certified-sub-patterns.yaml` `verifiers:` and `packing/devtools/census_n17_certified.py:244-246` | an admitted entry counts only with a receipt whose `verifier_sha256` is listed | a receipt from an unreviewed verifier | none: verifier, review and receipt are all in Git | the review document and the commit that lists it | per verifier edit: a review verdict on a digest (the whole question of `review-2026-10-03-n17-verifier-rewrites.md`), a ledger edit, and 242 to 4,258 s of full re-verification to carry the digest; listed twice in 24 h | REPLACE with verifier path, revision and review reference |
| B3 | same ledger, `receipt_sha256` and `verification.sha256`; `census_n17_certified.py:230-232, 301-303` | an entry is refused when a committed receipt’s digest differs | a receipt edited after admission | none: a manifest beside files Git already tracks | Git | ledger edit on every receipt regeneration | REMOVE |
| B4 | `census_n17_certified.py:249`: the verification receipt’s certificate digests must equal the producer receipt’s | the census | an entry whose verification checked other objects | none | the certificate path named by the entry | ms | REPLACE with the path |
| B5 | `packing/devtools/check_n17_subpattern.py:110-127`, `verify_n17_kernel_certificate.py:641-649`, `verify_n17_bb_certificate.py:380-384`: `seed-<sha256>.json.gz` and `node-<sha256>.json.gz` refused unless bytes hash to the name and are canonical JSON | every load | a certificate file edited after save | none | the verifier’s own obligations (`check_frame`, `check_seed`, the row cover) | ms per load; any re-serialization breaks the name | REMOVE the refusals; digest names may stay as names |
| B6 | `MODULE_SHA256` at import: `select_n17_sub_patterns.py:144`, `verify_n17_kernel_certificate.py:68`, `verify_n17_bb_certificate.py:53`, `survey_n17_residue.py:92`, `sweep_n17_residue_universe.py:53`, `census_n17_certified.py:104`; `tool_sha256` and `kernel_sha256` in `check_n17_subpattern.py:414, 454-455`; `instrument_sha256` in `check_n17_core_stress.py:1527` | nothing; recorded in receipts | a receipt naming bytes that were edited during a long run | none | Git revision plus a dirty flag answers the same question | the write-time-versus-import defect (`1d8577bca`); tests pin the mechanism (`test_select_n17_sub_patterns.py:395-403`, `test_verify_n17_certificates.py:105, 599`, `test_pilot_n17_capture.py:49-63, 182`) | REPLACE when touched: record `git hash-object` of the imported bytes, the revision and whether the tree was dirty |
| B7 | `sweep_n17_residue_universe.py:236, 454`: a resumed sweep refuses a plan or flags file whose digest moved | resume | resuming under other flags | none | compare the flag lists | ms | REPLACE with semantic equality |
| B8 | `packing/src/sqpack/hull_kernel/node.py:214` and `producer.py:849, 987`: a node names its seed by content digest | `admit_header` | a node paired with another seed | none | `check_frame` compares the seed’s groups with the node’s initial state | none | KEEP as a reference (content addressing used as naming); say so in the docstring |

### 2.3 Family C: Frozen-Blob Comparisons

| # | Where | Gates | Claimed failure | Boundary | Caught otherwise by | Cost | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | `packing/devtools/audit_bc303_parent_union.py:18-24, 44-67`: the source must equal its blob at `SOURCE_REVISION`, and `read_bc303_parent_union.py` must equal its blob at the execution revision | on demand; no test imports the audit (`test_read_bc303_parent_union.py` imports the reader) | the reader edited since the run | none | the audit imports no reader and recomputes the masses itself | any edit to the reader (typing, formatting) breaks the audit | REPLACE: record the revision, drop the byte comparison |
| C2 | `packing/devtools/audit_n17_endpoint_receipt.py:521-526`, `check_n17_endpoint_feasibility.py:598-606`: a retained root certificate must equal a frozen Git blob | `tests/test_n17_endpoint_*` (0.4 s) | a retained result edited in place | none | Git | ms; a re-serialization of the result breaks it | REPLACE with path and revision |
| C3 | `packing/devtools/check_general_pose_tree_census.py:31, 176-190`: an external `general_pose_tree` checkout pinned to a revision and its files to blobs | `tests/test_general_pose_tree_census.py` (1.6 s) | running against another checker | **yes**: another repository, passed by `--checker` | nothing else | 1.6 s | KEEP; the boundary is named in the docstring |
| C4 | `packing/devtools/admit_threshold_compression.py:108-118, 268` and `compress_threshold_certificate.py:77-86, 134`: reviewed bytes read with `git show REV:PATH` | admission | reading other bytes than the review admitted | none | this is the Git-identity pattern itself | ms | KEEP the pattern; drop the duplicate `sha256` fields when touched |
| C5 | `packing/devtools/check_n17_local_minimum.py:1404-1441, 3119`: Git blob ids of the sources recorded; the feature certificate’s digest match recorded as a boolean, not refused | nothing | none | none | n/a | none | KEEP as the model pattern |

### 2.4 Family D: The n11 Proof Chain

| # | Where | Gates | Claimed failure | Boundary | Caught otherwise by | Cost | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D1 | 170 distinct 64-hex literals across `packing/devtools/check_n11_*.py`, `n11_*.py`, `inventory_n11_*.py`, `prepare_n11_*.py`, `check_hull_kernel_*.py` (204 across `devtools`); the mask-0 checker’s digest `75fc0238…` pinned by `check_n11_optimality_field_runner.py:27, 197`, `field_mask202.py:25, 46`, `check_n11_capture_root_pilot.py:33, 322-428`, `check_hull_kernel_mask0.py:46, 150` and `check_n11_baseline_d4_cuts.py:38`; checkers re-hash themselves at the end of a run ("audit code changed", `check_n11_capture_root_chain.py:250`, `root_continue.py:368-413`, `branch_r1.py:242`, `child_node.py:865`) | the n11 family’s 52 test files, every suite run | a retained receipt reused with a different checker or input | the published packet `packing/resources/web/n11-optimality-2026-09-29/` is distributed for independent checking, but these pins are between repository files, not between the packet and a reader | Git; the packet’s LFS pointers (`*_LFS_SHA`) are Git LFS’s own content ids | 49.4 s per suite for the family, the chain’s own checker tests a minority of that; the pinned modules cannot be edited; `think-gzju` (P0, open) is a `final_state_sha256` binding in the public case-438 near-audit that fails while the geometry replays | FREEZE: retained and published evidence stays intact (OR-16); no new pins; fix `think-gzju` by rebinding, never by adding a layer; any new n11 tool identifies inputs by path and revision |

### 2.5 Family E: Gate Steps That Read Git History

| # | Where | Gates | Claimed failure | Boundary | Caught otherwise by | Cost | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | `packing/src/sqpack/cli/validate.py:3397-3461, 4806` “provenance: recorded commits are reachable” | the fast tier, every pull request | an experiment’s `engine_commit` orphaned or lost by a history rewrite | **yes**: history rewriting is outside any one tree; Git is the right instrument (OR-16) | nothing else; `D-138` and `D-226` are both failures it was built from | 12.0 s per run (measured locally); requires full history on the `validate` job | KEEP |
| E2 | `packing/devtools/check_session_gate.py`, `validate.py:3309` “terminal sessions name the gate that certified them” | records tier | a session certifying a tree nobody can identify, or a commit off the mainline | **yes**: ancestry, by Git | nothing else | 14.0 s per run; `test_session_gate.py` 6.1 s | KEEP |
| E3 | `fetch-depth: 0` on 11 jobs in `packing-validation.yml`, 5 in `deep-gate.yml`, 1 in `branch-mergeability.yml` | every CI job | tests that read historical objects fail on a shallow clone (66 tests, per the shard comment at `packing-validation.yml:681-690`) | the provenance and session-gate steps need history on one job; the other reasons are families A, C and D | n/a | one measured pair: 174 s full against 7 s sparse checkout on the workbench job (runs 35052785989 and 35056004552, 2026-09-16); the quick lane’s own trial found blobless saves about 100 MB of a 520 MB fetch | REPLACE on remeasure: after slices 1 and 4, run the shards blobless and keep full history where E1 and E2 run |

### 2.6 Family F: Library Round Trips

| # | Where | Gates | Claimed failure | Boundary | Caught otherwise by | Cost | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | `packing/src/sqpack/rust_rectangle_geometry.py:98, 121`: the engine binary is copied to a temp dir and re-hashed ("snapshot changed during copy") | every exact verifier session | a copy that differs from its source | none: the guideline’s own example of ceremony | the OS | ms | REMOVE |
| F2 | `packing/src/sqpack/campaign/runner.py:1286-1291`: an archive’s digest must equal its stored verification receipt’s, after the archive has just been re-verified in a separate process | `record` | an archive moved under its certificate | none | the re-verification that precedes it, every time | ms; a refusal path that can only misfire | REMOVE the digest comparison; keep the re-verification |
| F3 | `runner.py:861, 876`: the engine self-test receipt names the binary by digest | reuse of a self-test | a self-test cached for a different build | the binary is a build product, not in Git | n/a | ms | KEEP as a cache identity; name it as one |
| F4 | `packing/src/sqpack/fractional/threshold_compression.py:788-790`: a selection manifest names its catalog by a digest of the semantic model | manifest load | a manifest applied to another catalog | none | semantic (it hashes the model, not bytes) | ms | KEEP as a named content identity, or path and revision when touched |
| F5 | `packing/devtools/core_shrink.py:75`: a replay refuses a source whose digest differs from the receipt’s | replay | a receipt replayed against other source | none | the replay recomputes the whole event spectrum | ms | REMOVE the comparison; keep the record |
| F6 | `packing/devtools/checkpoint_manifest.py` `check` | on demand | legacy manifest drift | none | Git | none now | KEEP for the two retained legacy manifests only; `pack` already writes no sidecars |
| F7 | `packing/devtools/audit_grid_symmetry.py:157`: the H259 identity receipt pinned by digest | audit | an identity receipt replaced | none | Git | ms | REPLACE when touched |

### 2.7 Family G: Workbench Identities

| # | Where | Gates | Claimed failure | Boundary | Caught otherwise by | Cost | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| G1 | `packages/workbench/tools/workbench_tools/cadence.py:762`, `capture_video.py:786-947`, `poster.py:151`, `benchmark.py:480`, `check_animate_view.py:573`, `build_candidate.py:1332`, `src/data/corpus.ts:378`: a video receipt names the built page, a poster names its video, a page names the citation file it was built from | `--verify`, poster cutting, trial grouping, the animate-view check | drawing a finding from a page other than the one captured; a page built from stale citations | the page and video are generated artifacts, not in Git, so no revision names them | n/a | none | KEEP as cache identities (the guideline’s “cache correctness” case); say so in each docstring |

### 2.8 Family H: External Sources Against Pinned Values

| # | Where | Gates | Boundary | Verdict |
| --- | --- | --- | --- | --- |
| H1 | `packing/src/sqpack/fractional/parent_core.py:287-301` `REVIEWED_SHA256`; `packing/devtools/audit_kleddamag_n11.py:52-73` certificate and source-manifest digests | reading Kleddamag’s n11 release | **yes**: a third party’s release, pinned at review | KEEP |
| H2 | `packing/src/sqpack/research/unitsquare_precision.py:240-271`, `cases/unitsquare_precision/production/run.py:45-46` | `https://kingbird.myphotos.cc/packing/square-68.svg` against a pinned digest | **yes**: a download | KEEP |
| H3 | `packing/devtools/audit_wand125_point_and_mixed.py`, `audit_wand125_rectangles.py`, `audit_wand125_tools.py` | upstream subtree listings, bundle `files-sha256.json`, the reviewed upstream checker files | **yes**: acquired packets | KEEP, including the pins on our retained copies of upstream’s checker, whose expected value is upstream’s |
| H4 | `packing/devtools/audit_tokoharu_density.py:105-155` | `tokoharu-density.sha256` file manifest | **yes** | KEEP |
| H5 | `packing/devtools/audit_guzhou_r068.py:117-121, 320` | release certificate against its pin | **yes** | KEEP |
| H6 | `packing/devtools/audit_wang_li_n11.py:427` | the s(11) certificate taken in at `62eb45966` | **yes** | KEEP |
| H7 | `packing/devtools/audit_evand_mixed_covers.py:510-571` | upstream run headers’ digests against the retained files | **yes** | KEEP |
| H8 | `packing/cases/n54_source_contract/contract.py`, `verify.py` | the retained n54 source and its clean-room copy | **yes** (BC-141’s source contract) | KEEP, frozen |
| H9 | `packing/devtools/build_known_best_atlas.py:438` `upstream_declared_sha256`; the Kingbird catalogue capture (`1d4020e9f`) | upstream’s declared digest | **yes** | KEEP |
| H10 | `.github/workflows/packing-validation.yml:159, 194` `rustc -vV` digest as a cache key; `pages.yml:1697` size-and-digest listing of the publication | nothing; a key and a diff aid | n/a | KEEP; neither is a check |

### 2.9 Family I: Recording-Only Digests

`audit_cell_occupancies.py:154`, `verify_rectangle_density.py:136-181`,
`refine_rectangle_density_frontier.py:317-322`, `compare_rectangle_density_bounds.py`,
`compare_evand_s32_sweep.py`, `bench_n11_*.py`, `bench_rectangle_clip_ab.py`,
`checker_modules()` in `check_n17_subpattern.py:130-137`, and
`sqpack/research/canonical.py:141, 260` (blake2b dedupe ids) record digests and gate
nothing.
They cost nothing and need no slice; the only change is that new receipts record
Git blob ids and the revision instead, and `canonical.py` keeps its ids with the
“deduplication” function named, which it already does.

### 2.10 Family J: Retained Cases

`packing/cases/unitsquare_precision/` (`proof_sha256` envelopes, `SealedParent`),
`cases/n17_weighted_certificate_*` (checkpoint ancestry by digest, 145 references in the
successor alone), `cases/n11_threshold_certificate/`, `cases/trump11/` are closed
experiments whose receipts are retained evidence.
OR-16 keeps frozen evidence intact.
FREEZE; nothing new is built on their pattern; `test_unitsquare_precision*.py` and the
weighted-certificate tests (about 7 s together) stay as they are.

## 3. What the Ceremony Has Cost

Measured where a record exists, estimated where it does not.

| Tax | Measure | Source |
| --- | --- | --- |
| A dependency change | the 6,197.4 s n11 native run, demanded again before `test_native_parent_core_receipt` passes | `session-153-native-full.json`; `think-lhyk`; `c401c81d6` reverted in `db370d14a` |
| A kernel speedup with identical output | the 256-row capture run restarted from round 0; at the 128-row cap a round is about 42 min and an update about 155 CPU-s, under a 3-hour ceiling; later the same day the run refused its round-10 checkpoint after an opt-in kernel change that is byte-identical by default | `think-g2qn` note of 05:00 UTC; `receipts/capture-pilot2-box1024-128.json`; the coordinator’s note after the 14:37 UTC restart |
| A verifier edit | a review verdict on whether a digest may be listed, a ledger edit, and a full verification to carry it: W7 4,258 s under the reviewed verifier and 242 s under the rewrite, A 1,550 s, N1 315 s; two digests per verifier after 24 h | `certificates/*/verification*.json`; the ledger header; `0c56fb627`, `1c870efe2` |
| The suite, every run | 103.2 s for family A and 49.4 s for the n11 family’s 52 test files, of 1,213.6 s; the provenance step 12.0 s and the session gate 14.0 s per gate run | `suite-file-costs.json`; local `--only` timings |
| CI checkout | 17 jobs clone full history; the one measured pair is 174 s against 7 s | `gate-budgets.yaml:1496-1499`; the workflows |
| Defects in the checks themselves | `D-138` (quoted versus unquoted commit hashes skipped), `D-226` (shallow CI against its own provenance gate), `D-158` (unattached extraction hashes), the selector hashing at write time, `think-gzju` open at P0 | `defects.yaml`; `1d8577bca`; the bead |
| Reviewer and agent attention | the verifier-rewrites review’s framing question is a digest listing; the capture lane lost a resume; the arity-8 selector lane retained a diff so that its receipts’ digest could be reproduced | the review documents; `receipts/selector-arity8-ran-to-committed.diff` |

The first three rows are the ones the owner named.
None of them crosses a boundary: in each, the repository checked itself against itself
and charged a long computation for the privilege.

## 4. Removal Plan

Seven slices, ranked by tax removed per hour of work, each with disjoint files so lanes
can run in parallel.
Effort is agent time including tests and a push-tier run.

### Slice 1: Environment Sealing (Lane E1, in Flight)

Owner `think-lhyk`. Files: A1 to A5. Effort: one lane-day.

- `audit_kleddamag_n11_native`: `check_proof_code` records `{path, git_blob}` at the
  recorded proof commit and reports, without failing, which paths differ at `HEAD`.
  `PROOF_INPUTS` loses `pyproject.toml`, `uv.lock` and `.python-version`.
- The fixed-core family drops `HEAD` equality, clean-checkout and runtime-identity
  refusals and the blob-for-blob manifest comparison; receipts keep revision and paths.
- **Tests to keep:** the 19 semantic refusals in `test_native_parent_core_receipt.py`
  and `test_frozen_cross_fixture_and_normalization_have_the_reviewed_answers`. **Drop:**
  `test_git_reuse_boundary_binds_transitive_code_and_lock_not_unrelated_docs`,
  `test_source_manifest_refuses_a_stale_revision`,
  `test_source_and_reader_revisions_are_separate_exact_bindings`,
  `test_runtime_binding_validates_the_project_environment_and_lock`,
  `test_executed_source_bytes_must_match_the_prevalidated_manifest` and their kin.
  **Add:** one test that a receipt at an older proof commit is accepted at `HEAD` with
  its drift listed.
- Then gmpy2 returns as a plain dependency.

### Slice 2: The n17 Checkpoint, Ledger and Verifiers

Files: B1 to B7. Effort: three to four hours.
Removes the restart tax and the digest-admission review step.

- `load_checkpoint` checks schema and settings only, records `{revision, dirty}` and the
  checkpoint’s own revision, and relies on `replay` for the semantic guarantee it
  already provides.
- The ledger’s `verifiers:` becomes a list of `{path, revision, review}`;
  `receipt_sha256` and `verification.sha256` are deleted; the census requires a
  verification receipt that is `PASS`, `full`, of the entry’s certifier kind, naming the
  entry’s certificate path, produced by a listed verifier path at or after its listed
  revision.
- `load_certificate`, `load_object` and `read_named` stop refusing on name or canonical
  form; digest names stay as names until the next producer change renames them
  `seed.json.gz` and `node.json.gz`.
- `MODULE_SHA256` and `TOOL_SHA256` become a `provenance()` helper returning the blob id
  of the imported bytes (`hashlib.sha1(b"blob %d\0" ...)`, as `check_n17_local_minimum`
  already does), the revision and a dirty flag; nothing compares them.
- The residue sweep compares flag lists, not file digests.
- **Tests to keep:** the W7 bins-8 production test
  (`test_verify_n17_certificates.py:242-260`), which is the small-instance determinism
  proof: the producer’s bytes equal the committed fixture.
  `test_hull_kernel_caches` stays as the proof that the speedup is the reference.
  **Rewrite:** the census tests that fabricate digests
  (`test_census_n17_certified.py:136, 212-232`). **Drop:**
  `test_the_kernel_verifier_refuses_bytes_that_do_not_match_their_name`,
  `test_digests_are_read_at_import`, the `module_sha256` assertions at
  `test_select_n17_sub_patterns.py:395-403`. **Add:** a resume test: write a checkpoint,
  append a comment to `hull_kernel/__init__.py`, reload, assert accepted and replayed.

### Slice 3: Library Round Trips

Files: F1, F2, F5, F7. Effort: one to two hours.

- Delete the copy re-hash in `rust_rectangle_geometry`, the archive digest comparison in
  `runner.record`, the source digest refusal in `core_shrink.replay`, and the identity
  receipt pin in `audit_grid_symmetry`.
- **Tests to keep:** the separate-process re-verification test for the runner and the
  engine self-test cache test.
  **Drop:** any test that asserts the removed refusal messages.

### Slice 4: Frozen-Blob Audits

Files: C1, C2. Effort: two hours.

- `audit_bc303_parent_union` records `SOURCE_REVISION` and the execution revision and
  stops comparing the reader to its blob; `audit_n17_endpoint_receipt` and
  `check_n17_endpoint_feasibility` name the root certificate by path and revision.
- **Tests to keep:** the arithmetic replays.
  **Drop:** the “differs from frozen Git blob” cases.

### Slice 5: CI History

Effort: one hour plus two CI runs.
After slices 1 and 4, rerun the quick lane blobless at one commit, list the tests that
still fetch historical objects, and leave full history only on the job that runs the
provenance and session-gate steps.
The saving is one checkout per job: the measured pair (7 s sparse and blobless against
174 s full) bounds it from above, and the quick lane’s blobless-only trial, which saved
about 100 MB of a 520 MB fetch, bounds it from below.
`gate-budgets.yaml` records the before and after, and nothing is claimed until it does.

### Slice 6: The n11 Chain

Effort: none now. Freeze D1 and J. Close `think-gzju` by regenerating the one binding
from the verified source, and record in the packet’s `README.md` that the chain is
closed: new n11 tools identify inputs by path and revision.

### Slice 7: The Rule and Its Ratchet

Effort: one hour. Section 5’s text goes into `operating-rules.md` and `development.md`,
and `AGENTS.md` is regenerated.
A ratchet in the style of the TypeScript floor, `devtools/check_integrity_ceremony.py`,
counts two patterns outside an allowlist of family H and C3:
`hashlib.sha256(Path(__file__)` self-digests, and `== *_SHA*` comparisons against
literals or recorded fields.
It fails when the count grows.
It is cheap (one `ast` pass, under a second), and it catches the thing that has been
re-added on four separate dates since OR-16 was written on 2026-09-06: the bc303 audit
on 09-13, the n11 chain on 09-29, the endpoint audits on 10-01, and five n17 tools with
the ledger on 10-02. OR-1 says a measurement belongs in a tool.

## 5. Proposed Amendment

### 5.1 OR-16, One Paragraph Added After the Second

> **Internal bookkeeping never costs a re-run, and the repository is not a trust
> boundary with itself.** Identify a retained result, a tool, a kernel or a verifier by
> the Git revision and repository-relative paths that produced it, never by a digest of
> its bytes. Reuse a checkpoint, receipt, cache or certificate whenever its content still
> checks; nothing refuses it because a file, a dependency, a lock or an interpreter has
> changed since it was written.
> Record that drift beside the result as information.
> Prove determinism with a small-instance test in the fast tier (same input, identical
> bytes), never by re-running a retained computation.
> A checksum earns its place only where three answers are written beside it: the
> boundary it crosses, where the independently supplied expected value comes from, and
> the failure it detects; a downloaded packet, an external checker at a revision, and
> Git ancestry qualify, and a file the repository wrote does not.
> The owner set this on 2026-10-03, after a dependency change was priced at the 6,197 s
> n11 native run and a kernel speedup with identical output sent a capture run back to
> round 0.

### 5.2 development.md, Under Hashes and Repository-Owned Artifacts

> Four shapes are ceremony here and are refused in review: a tool that hashes its own
> source or its kernel’s and refuses a checkpoint or receipt whose digest differs; a
> ledger or registry that lists verifiers, receipts or receipts-of-receipts by SHA-256;
> an audit that compares a working file to its historical Git blob and fails on
> difference; and a frozen copy of code kept so that bytes can be compared.
> The shape that replaces all four is a `provenance()` record: the blob id of the bytes
> the process imported (`git hash-object`, or `hashlib.sha1(b"blob %d\0" + data)` as
> `check_n17_local_minimum` does), the revision, and whether the tree was dirty; it is
> recorded and never compared.
> Determinism is a fixture test: produce a small instance and compare its bytes with the
> committed fixture (`test_verify_n17_certificates`’s W7 at bins 8 is the model).
> Content addressing may name files and deduplicate; a name is not a check, and a loader
> does not refuse a file for not hashing to its name.
> `devtools/check_integrity_ceremony.py` holds the count of self-digests and digest
> comparisons outside the named boundaries and fails when it grows.

## 6. What Stays, and the Boundary Each Names

- **Downloaded or acquired sources against values pinned at review** (H1 to H9): another
  party’s bytes, checked against what the review saw.
- **The external `general_pose_tree` checker at a revision** (C3): another repository.
- **Git ancestry** (E1, E2): history rewriting, which no single tree can see.
- **Cache identities of generated artifacts** (F3, G1): a page, a video or a built
  binary has no revision, so a digest is its name, and each docstring says that is the
  function.
- **Content ids for deduplication** (`canonical.py`, B8’s seed reference): naming, never
  refusal.
- **Legacy checkpoint manifests** (F6): retained evidence, not extended.

Everything else in the inventory compares the repository with itself.

## Evidence Status

- **Measured:** the 6,197.4 s run; the per-file suite costs; the 12.0 s and 14.0 s gate
  steps; the 174 s against 7 s checkout pair; the verification receipt durations; the
  per-update and per-round capture costs; the digest-literal counts.
- **Recorded, not re-measured:** the 256-row restart and its cause (the lane’s bead
  note); the gmpy2 revert’s reason (the E1 bead).
- **Estimated:** the slice efforts, and the CI saving, which slice 5 measures before it
  is claimed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
