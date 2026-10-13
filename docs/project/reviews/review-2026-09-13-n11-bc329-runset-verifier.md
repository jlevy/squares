# Exact-Head Review: BC329 Run-Set Verifier

**Verdict: REFUSE operational admission at `878e18d0c9c68669db1e6f28bcec9c08edce98d2`.**
The verifier implements much of the proposed evidence path, and its seven focused tests
pass. Six temp-only mutations still produce five false admissions and one refusal-path
failure. R2, R3, and R4 should remain open pending repair and a new exact-head review.
This review does not authorize a positive calibration profile or BC329 target run.

## Review Boundary

- Workflow entry point: independent, read-only review of the newly committed verifier.
  No repository source, bead, PR, positive profile, or BC329 target was changed.
- Exact source head: `878e18d0c9c68669db1e6f28bcec9c08edce98d2`; verifier blob
  `85f8bbf3960de71821fc97afd0a9b47322aa83d8`; focused-test blob
  `ca4f08ee0c3fe19e28f848bfc8f487e85823b7ee`. Both files are newly added by that commit.
- Reviewed context: `AGENTS.md`, `development.md`, the independent
  [run-sheet refusal](review-2026-09-13-n11-bc329-three-profile-run-sheet.md), and the
  [proposed verifier plan](../specs/done/plan-2026-09-13-n11-bc329-runset-verifier.md).
  The two review documents were untracked working-tree files, not blobs at the source
  head. Their observed SHA-256 values were
  `02513c41f01165e6fd591a60d46a95dc2fc94cc81339c668930263b1dc3fdbab` and
  `bf2f374793d9f1c42df19935560c754ca099f67faedd2978984fd07d0a4d5d70`, respectively.
- The five public command entry points, `snapshot`, `read`, `join`, `retain`, and
  `source-closure`, contain no coordinator launch or calibration target invocation.
  I reviewed only the new verifier and its focused test file as code.
- Validation:
  `PYTHONDONTWRITEBYTECODE=1 packing/.venv/bin/python3 -m pytest -p no:cacheprovider -q packing/tests/test_verify_fixed_core_calibration_runset.py`
  passed **7/7** under Python 3.14.7. Mutation probes used
  `tempfile.TemporaryDirectory(dir="/private/tmp")` and the existing synthetic test
  helpers; they did not write to the reviewed checkout.

## Obligation Verdicts

| Obligation | Verdict | Evidence |
| --- | --- | --- |
| R2: exact external reader command, status, and proof joined to each coordinator run | **REFUSE** | The exact 13-element argv is recorded and rechecked; command status, stream hashes, proof order/path/revisions, identity equality, and receipt bytes/digest are joined. But `_same_typed` only compares matching JSON types on both sides. A boolean `requested_workers` in both summary and proof passes as an accepted run. The retained copy can also diverge from the checked proof after the admission check. |
| R3: coordinator-return run-root baseline through archive and copied summary | **REFUSE** | Per-file byte/type inventory, symlink rejection, before/after scans, tar member content checks, and copied summary/inventory byte equality are implemented. Snapshot nevertheless accepts a fourth top-level run record, contrary to the plan’s exactly-three-run-record boundary. Retention accepts changed coordinator status and can copy a proof that disagrees with the retained admission record. |
| R4: complete source closure through staged candidate and evidence commit | **REFUSE** | The verifier reconstructs local imports, fixture, runtime declarations, and compares all manifest paths, modes, blob IDs, SHA-256 values, and working files to the supplied candidate tree. It does not bind the supplied tree OID to the current Git index. A staged helper change hidden by restoring its working file passes when the caller supplies the old execution tree. No actual evidence-commit check was available to this review. |
| Strict JSON, paths, identities, and refusal status | **REFUSE** | Duplicate keys, non-finite constants, exact root/path forms, and most record key sets are checked. Specific invocation-identity field types are not. A syntactically valid 5,000-digit JSON integer raises an uncaught plain `ValueError`, so the CLI does not take its declared `REFUSED`/exit-2 path. Ordinary missing files raise `OSError`, which `main` does catch and map to exit 2. |
| Focused mutation tests | **PARTIAL** | The seven tests cover a positive synthetic join/retention, eleven proof/command mutations, five run-root mutations, four archive mutations, and several source-closure mutations. The fixtures use empty scientific payloads by design. They do not discriminate the accepted shared-invalid identity, extra run record at snapshot, stale candidate tree, changed coordinator status, inconsistent retained copy, or oversized-JSON refusal-path failure. |

## Findings

### F1 — High: Shared Invalid Identity Types Pass the Join (R2)

`_summary` checks the invocation-identity key set, revision, and run order, but it does
not validate the other identity fields’ required types
([verifier:323](../../../packing/devtools/verify_fixed_core_calibration_runset.py#L323)).
`_admission` calls `_same_typed`
([verifier:619](../../../packing/devtools/verify_fixed_core_calibration_runset.py#L619)),
which establishes equality and identical types between two records, not that either
value has the correct type.
In an isolated synthetic root, I changed the first summary identity’s
`requested_workers` from integer $4$ to boolean `true`, resnapshotted, and generated a
zero-status proof carrying the same identity.
`join_reader_proofs` returned `status: accepted`. The reader itself owns scientific
checks, but R2’s explicit typed invocation identity must reject this pair.

**Fix:** Validate every identity field against its expected JSON type and finite/range
constraints in the summary and proof before typed equality.
Add a shared-invalid mutation alongside the existing one-sided
`requested_workers = True` test.

### F2 — High: A Fourth Coordinator Run Record Enters the Baseline (R3)

`_inventory` requires the four named top-level files as a subset, not an exact set
([verifier:378](../../../packing/devtools/verify_fixed_core_calibration_runset.py#L378)).
It restricts top-level directories to `profile-1` through `profile-3`, but accepts an
additional top-level `profile-4-run.json`. I added that file before resnapshotting a
synthetic root; `snapshot_run_root` returned an inventory containing it.
Subsequent byte/type preservation can faithfully archive an inadmissible fourth run
record.

**Fix:** Validate the coordinator’s exact expected top-level run-record set at snapshot,
while documenting any permitted other top-level artifacts.
Test the added fourth record before the first inventory is made.

### F3 — High: A Stale Candidate OID Can Mask Staged Source Changes (R4)

`verify_source_closure` resolves and compares the caller’s `candidate_tree`, then checks
working source bytes
([verifier:956](../../../packing/devtools/verify_fixed_core_calibration_runset.py#L956),
[verifier:999](../../../packing/devtools/verify_fixed_core_calibration_runset.py#L999)).
It never checks that OID against the current staged index.
In a temporary Git fixture, I staged a changed `packing/devtools/helper.py`, restored
the working file to the execution bytes, and confirmed `git write-tree` produced a
different tree. Passing the old execution tree as `candidate_tree` still returned
`status: accepted`. The plan tells the run sheet to pass a fresh `git write-tree` OID;
the maintained command does not enforce that precondition, so its output alone cannot
attest the intended evidence tree.

**Fix:** Bind the precommit check to the current index tree inside the command, or
retain and independently verify a fresh `git write-tree` value as part of the exact
invocation. Distinguish that precommit check from the later committed-OID check.
Add the staged-change/restored-worktree mutation.

### F4 — High: Retention Can Copy a Proof That Its Admission Did Not Check (R2/R3)

`retain_run_root` checks `_admission` once before copying review artifacts
([verifier:786](../../../packing/devtools/verify_fixed_core_calibration_runset.py#L786));
it rereads only copied summary, inventory, and admission at the end
([verifier:817](../../../packing/devtools/verify_fixed_core_calibration_runset.py#L817)).
I injected a deterministic change to `REVIEW_ROOT/profile-1-source-distinct.stdout.json`
immediately after copying the admission record and before copying that proof.
`retain_run_root` returned `status: accepted`, while the evidence copy of the proof was
`{}\n` and its SHA-256 did **not** equal the retained admission’s `proof_sha256`. No
run-root byte changed.
The test demonstrates a concrete check/copy race, not a cryptographic forgery claim.

**Fix:** Validate the copied command, status, stream, and proof bytes against the copied
admission and original checked bytes before reporting retention success; recheck the
review-root source records after copying.
An evidence staging directory with a final publish step would also prevent a partially
built accepted-looking root from appearing early.
Add a failure-injection test at the copy boundary.

### F5 — Medium: Changed Coordinator Status Is Retained as Accepted (R3 Context)

`snapshot_run_root` requires `coordinator.status` to be `0\n`
([verifier:432](../../../packing/devtools/verify_fixed_core_calibration_runset.py#L432)).
The run-root inventory excludes that sibling review-root file, and `retain_run_root`
copies it without another content check
([verifier:790](../../../packing/devtools/verify_fixed_core_calibration_runset.py#L790)).
In a complete synthetic join, I changed it to `2\n` before `retain`; retention returned
`status: accepted` and the evidence root contained `coordinator.status = 2`. This
contradicts the retained claim that the coordinator returned successfully.

**Fix:** Recheck `coordinator.status == 0\n` at retention and after copy, or bind the
complete review-root control files to a snapshot before readers and verify that binding
at retention. Add this mutation to the focused tests.

### F6 — Medium: An Oversized JSON Integer Escapes the Refusal Path

`_json_bytes` catches decoding and JSON syntax exceptions, but Python 3.14 raises a
plain `ValueError` when a JSON integer exceeds the interpreter’s digit limit
([verifier:168](../../../packing/devtools/verify_fixed_core_calibration_runset.py#L168)).
I resealed the first proof as `b'{"n":' + b'9' * 5000 + b'}'` and called
`main(join ...)`. It raised plain `ValueError` and wrote no admission record, rather
than returning 2. `main` catches `OSError`, `EOFError`, `tarfile.TarError`, and
`RunSetRefusalError`, so this malformed retained proof/record escapes its stderr
diagnostic and exit-2 contract
([verifier:1081](../../../packing/devtools/verify_fixed_core_calibration_runset.py#L1081)).

**Fix:** Translate decoder `ValueError` and nesting `RecursionError` into
`RunSetRefusalError` in `_json_bytes`, retaining the input label.
Test through `main(join ...)` with a resealed malformed proof, asserting exact refusal
exit status and no admission record.

## Design Assessment and Next Review

The five-stage design is appropriate for the three distinct boundaries.
It keeps the run root separate from the review root, checks duplicate JSON keys, records
exact reader argv/status/streams, compares tar members to the first run-root inventory,
and reconstructs source closure without running a positive profile.
Those checks are worth retaining.
The repairs should focus on explicit type validation and on binding each later artifact
to the bytes or Git tree actually carried forward.
The next exact-head review should rerun the seven tests, the six probes above, and the
applicable edit/push/fast validation tiers before closing `think-0ylz`, `think-n8sw`, or
`think-ndlq`.

No source documentation change was assessed beyond the two reviewed plan/refusal
documents. Their existing caveat that independent reader and integrated-head acceptance
remain separate gates is correct.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
