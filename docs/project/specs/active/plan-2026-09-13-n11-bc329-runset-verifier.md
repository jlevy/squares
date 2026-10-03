# BC329 Run-Set Verifier Contract

Date: September 13, 2026. Status: implementation contract for `think-0ylz`,
`think-n8sw`, and `think-ndlq`. The first maintained implementation landed at
`878e18d0`; its
[exact-head review](../../reviews/review-2026-09-13-n11-bc329-runset-verifier.md)
refused R2–R4 admission on six reproducible gaps.
Repair and a new review remain open.
No profile, BC329 target, or operational admission was performed for it.

The
[independent run-sheet review](../../reviews/review-2026-09-13-n11-bc329-three-profile-run-sheet.md)
identifies three missing measurements: the reader proofs are not joined to the
coordinator’s three runs (R2), the run root has no retained byte/type baseline at
coordinator return (R3), and the source freeze checks only three files (R4). The sheet’s
first-refusal stop order is R1 and is a separate Bash control; it must remain in place
even if the maintained command below launches the readers.

## Existing Binding Fields

The coordinator writes `three-profile-summary.json` with schema
`fixed-core-calibration-three-profile-summary/v1`. Its `runs` array has exactly three
entries in order. Each run carries `run_order`, `profile_directory`,
`invocation_identity`, and `calibration_receipt` (`path`, `bytes`, `sha256`). The
coordinator validates that shape and reconstructs the summary from retained records
before publishing it (`packing/devtools/run_fixed_core_calibration_profiles.py`,
`build_summary` and `validate_summary`, around lines 1280–1450 and 1867–2069).

The separate reader’s successful stdout is one JSON object with schema
`fixed-core-calibration-source-distinct-readback/v1`. It contains `status: accepted`,
`execution_revision`, `reader_revision`, `run_order`, `profile_directory`,
`invocation_identity`, and a `receipt` object with the same three binding fields
(`packing/devtools/read_fixed_core_calibration_profile.py`, `read_profile`, around lines
1973–2037). The CLI’s five flags are fixed in that module’s `_parser` near line 2040.
The reader performs the scientific and topology checks; the proposed verifier only joins
already accepted outputs.

Each profile receipt embeds `sources.manifest`, a sorted list of
`{path, git_blob, sha256}` records, and `sources.implementation_revision`. The producer
discovers local imports recursively and adds the fixture, `packing/.python-version`,
`packing/pyproject.toml`, and `packing/uv.lock`
(`packing/devtools/calibrate_fixed_core_packet.py`, `discover_implementation_paths` and
`source_manifest`, around lines 672–830). The independent reader reconstructs that path
set from Git objects at the execution revision
(`packing/devtools/read_fixed_core_calibration_profile.py`, `_execution_source_paths`
and `_validate_sources`, around lines 408–515). These paths, including package
initializers and mathematical helpers, are the R4 source closure.
The run sheet’s current three-path `git diff` at its retention block does not cover it.

## Command and API Contract

Put one reviewed module at `packing/devtools/verify_fixed_core_calibration_runset.py`.
It must be target-free and have no import from the producer or source-distinct reader.
Use Python 3.14 from `packing/.venv`; the five subcommands below are the only
operational entry points.
Each takes absolute paths, validates their real locations, refuses an existing output it
would overwrite, and exits $0$ only after its complete check.
Refusals exit $2$ with a diagnostic on stderr.

```text
python -m devtools.verify_fixed_core_calibration_runset snapshot
  --run-root RUN_ROOT --review-root REVIEW_ROOT
  --expect-execution-revision EXECUTION_REV

python -m devtools.verify_fixed_core_calibration_runset read
  --repository REPOSITORY --run-root RUN_ROOT --review-root REVIEW_ROOT
  --expect-execution-revision EXECUTION_REV
  --expect-reader-revision READER_REV --run-order {1,2,3}

python -m devtools.verify_fixed_core_calibration_runset join
  --run-root RUN_ROOT --review-root REVIEW_ROOT
  --expect-execution-revision EXECUTION_REV
  --expect-reader-revision READER_REV

python -m devtools.verify_fixed_core_calibration_runset retain
  --run-root RUN_ROOT --review-root REVIEW_ROOT
  --evidence-root EVIDENCE_ROOT
  --expect-execution-revision EXECUTION_REV

python -m devtools.verify_fixed_core_calibration_runset source-closure
  --repository REPOSITORY --run-root RUN_ROOT --review-root REVIEW_ROOT
  --expect-execution-revision EXECUTION_REV
  --candidate-tree TREE_OID
```

The corresponding public Python functions should be `snapshot_run_root(...) ->
dict`, `run_reader(...) -> int`, `join_reader_proofs(...) -> dict`,
`retain_run_root(...) -> dict`, and `verify_source_closure(...) -> dict`. No function
runs the coordinator or a calibration profile.
The run-sheet Bash calls `read` for orders 1, 2, and 3 one at a time and tests each
status before calling the next.
The wrapper constructs and launches exactly this reader argv, in the displayed order,
with the checkout’s `sys.executable`:

```text
[PYTHON, "-m", "devtools.read_fixed_core_calibration_profile",
 "--repository", REPOSITORY,
 "--expect-execution-revision", EXECUTION_REV,
 "--expect-reader-revision", READER_REV,
 "--output-dir", RUN_ROOT + "/profile-N", "--run-order", "N"]
```

The wrapper writes the exact argv *that it passes to `subprocess.run`*, its integer
status, and byte/digest bindings for stdout and stderr.
It retains the existing `profile-N-source-distinct.stdout.json`, `.stderr.log`, and
`.status` names plus a new `.command.json` under `REVIEW_ROOT`. It writes a pending
command record before launch and finalizes it atomically after return, so a crash or
launch failure leaves a refusal trace.
It returns nonzero on a reader refusal or any log/record publication failure.
The `join` command never launches a reader.

## Retained JSON Shapes

All JSON files below use UTF-8, duplicate-key rejection at every object,
`parse_constant` rejection of NaN/Infinity, exact top-level and nested key sets, exact
JSON types (`bool` must not pass as `int`), and no trailing non-JSON bytes.
`bytes` is a nonnegative integer and `sha256` is 64 lowercase hex characters.
Paths in manifests are sorted relative POSIX paths without `.` or `..`; absolute root
fields are canonical paths.
Atomic write and reread is required for each new JSON record.

`REVIEW_ROOT/run-root-inventory.json`:

```json
{
  "schema": "fixed-core-calibration-run-root-inventory/v1",
  "execution_revision": "<40 lowercase hex>",
  "run_root": "<canonical absolute path>",
  "directories": ["profile-1", "profile-1/raw-directions"],
  "files": [
    {
      "path": "profile-1/result.json",
      "type": "regular-file",
      "bytes": 123,
      "sha256": "<64 lowercase hex>"
    }
  ]
}
```

The arrays above are examples of row shape, not a permitted two-entry inventory.
The real inventory contains every directory and every regular file in the root,
including the top-level summary and coordinator run records.
The inventory excludes itself because it lives in the sibling review root.
No timestamp, inode, or archive digest substitutes for a file’s byte digest.

`REVIEW_ROOT/profile-N-source-distinct.command.json`:

```json
{
  "schema": "fixed-core-calibration-source-distinct-command/v1",
  "run_order": 1,
  "argv": ["<absolute Python executable>", "-m", "devtools.read_fixed_core_calibration_profile"],
  "exit_status": 0,
  "stdout": {
    "path": "profile-1-source-distinct.stdout.json",
    "bytes": 123,
    "sha256": "<64 lowercase hex>"
  },
  "stderr": {
    "path": "profile-1-source-distinct.stderr.log",
    "bytes": 0,
    "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  }
}
```

The real `argv` has all thirteen elements shown in the command contract above; the
shortened array shows only its initial shape.
A pending record has the same schema and argv but `exit_status: null` and both stream
bindings `null`; `join` refuses it.
The separate `.status` text must be decimal and equal to `exit_status`. The wrapper and
`join` both verify stream bindings from retained bytes.

`REVIEW_ROOT/run-set-reader-admission.json`:

```json
{
  "schema": "fixed-core-calibration-run-set-reader-admission/v1",
  "status": "accepted",
  "execution_revision": "<40 lowercase hex>",
  "reader_revision": "<40 lowercase hex>",
  "run_root_inventory_sha256": "<64 lowercase hex>",
  "summary_sha256": "<64 lowercase hex>",
  "runs": [
    {
      "run_order": 1,
      "profile_directory": "<canonical absolute path>/profile-1",
      "command_sha256": "<64 lowercase hex>",
      "proof_sha256": "<64 lowercase hex>",
      "receipt_sha256": "<64 lowercase hex>"
    }
  ]
}
```

The actual `runs` array has orders $[1, 2, 3]$ only.
`command_sha256` and `proof_sha256` cover exact retained `.command.json` and
`.stdout.json` bytes; `receipt_sha256` repeats the corresponding summary/reader receipt
binding for audit. The join must compare receipt `bytes` as well as digest even though
the small record does not repeat `bytes`. `retain` copies this record, the baseline
inventory, all reader records and logs, coordinator logs, and host observations to the
new evidence root, along with the copied summary and archive.
It emits `run-root.tar.gz`, `run-root-contents.txt`, and `run-root.tar.gz.sha256` there.
The copied summary and inventory must be byte-identical to the originals, not merely
parse to equal JSON objects.

`source-closure` is a read-only check and prints one JSON object on stdout:

```json
{
  "schema": "fixed-core-calibration-source-closure-check/v2",
  "status": "accepted",
  "execution_revision": "<40 lowercase hex>",
  "candidate_tree": "<40 lowercase hex>",
  "sources": [
    {
      "path": "packing/.python-version",
      "git_blob": "<40 lowercase hex>",
      "sha256": "<64 lowercase hex>"
    }
  ],
  "drift": ["<repository-relative path>"]
}
```

The actual `sources` array is the complete sorted manifest, not the example row.
Capture candidate and committed checks under distinct names in `REVIEW_ROOT`; neither
command writes to `RUN_ROOT` or the Git index.
The candidate check runs after the evidence files are staged and before the evidence
commit. The later check uses the actual commit OID as `TREE_OID`.

## Admission Stages and Refusals

1. **After the coordinator returns:** Call `snapshot` immediately, before any reader.
   Require coordinator status zero, a regular summary, exactly three profile directories
   and run records, and summary revision/run paths equal the caller’s root and revision.
   Scan every path without following links.
   Record sorted directory paths and each file’s type, byte count, and SHA-256 outside
   `RUN_ROOT`; atomically reread the manifest.
   Reject links, hard links, special files, duplicate normalized paths, empty or
   unexpected directories, and a file changing during its scan.
   This is the R3 baseline at the first post-return observation.
   Call the same scanner once more before reader 1.
2. **After each reader:** `read` compares the live root to the baseline before and after
   its child process. It records argv/status/streams even on refusal.
   The Bash status test stops the sequence on the first nonzero result (R1). `join`,
   reached only after three zero statuses, rescans the root and requires exactly one
   final command record, status file, stdout proof, and stderr log for each order, with
   no extra profile-labeled reader output.
   It parses each proof strictly, requires `status: accepted` and the reader schema,
   compares both revisions to the CLI expectations, compares order, canonical profile
   path, typed invocation identity, and receipt `{path,bytes,sha256}` to the matching
   summary run, and verifies the command’s exact argv and stream bindings.
   It refuses a missing, extra, malformed, duplicate, pending, or mismatched proof.
   It writes the admission record only after all three matches.
   This discharges R2; it does not independently accept reader code.
3. **At retention:** `retain` rescans before creating the archive, writes only into a
   fresh evidence root, and rescans after archiving.
   It reads every tar member as bytes, normalizes a single root prefix, and compares the
   exact file and directory path/type set, byte count, and digest to the baseline.
   Refuse duplicate names, path traversal, links, special members, extra or missing
   members, truncated members, and changed live files.
   Recheck the copied summary and inventory against baseline bytes; hash and reread the
   completed archive. Archive hashing alone is insufficient because it does not bind
   archived members to the coordinator-return baseline (R3).
4. **Before the evidence commit:** Parse all three immutable `result.json` receipts
   strictly after a fresh root/baseline comparison.
   Require their `sources.implementation_revision` and sorted manifest path/blob/SHA
   rows to agree exactly.
   For each row, verify regular Git blob mode, object ID, and SHA-256 against
   `EXECUTION_REV`. Reconstruct the producer’s local import closure from Git tree
   objects at `EXECUTION_REV`, including the fixture and three runtime declarations, and
   require exact path-set equality.
   After all intended evidence files are staged, pass the tree OID from `git write-tree`
   as `TREE_OID`; reconstruct that tree’s closure and report every path whose mode or
   blob differs from the execution tree, or that only one of the two closures holds, as
   `drift`. Re-run against the actual evidence commit OID after committing; only that
   check can name the committed tree.
   This is R4. Amended 2026-10-03 on the owner’s direction
   ([development.md](../../../../development.md#hashes-and-repository-owned-artifacts)):
   the run set is a fact about `EXECUTION_REV`, so a later code, fixture, runtime
   declaration or lockfile change is reported, never refused, and never a reason to run
   the profiles again. The working-tree comparison is dropped with it.

The new module checks evidence plumbing.
It does not turn a zero reader exit into acceptance without parsing the proof, does not
infer scientific evidence from the $n=2$ fixture, and does not lift the independent
exact-head gates in the run sheet.
The baseline shows byte/type equality at measured boundaries; it cannot prove that no
writer briefly changed and restored bytes between scans.
The external root and review root remain until the evidence commit is pushed and
admission is recorded.

## Maintained Mutation Controls

Add focused tests for the new module using a small synthetic run root and a temporary
Git repository; no positive calibration profile is needed.
Exercise one accepted three-run join and archive, then mutate one boundary at a time:

- R2: missing/extra proof, duplicate JSON key, non-finite value, accepted status with
  nonzero command status, changed argv flag or Python path, swapped order or profile
  path, changed invocation identity, and same digest with wrong receipt byte count;
- R3: added, removed, edited, or symlink-replaced run file; extra empty directory;
  archive member duplication, traversal, type change, or byte change; changed copied
  summary; and a changed top-level coordinator record;
- R4: changed nested helper, package initializer, fixture, runtime declaration, or
  lockfile blob; source deletion; and a newly added local module that enters the import
  closure at the candidate tree, each accepted and named in `drift`; and a manifest row
  that does not describe `EXECUTION_REV`, refused.

Run those tests and the normal edit/push/fast validation tiers specified in
`development.md`. The run sheet should invoke these reviewed subcommands and retain
their JSON, rather than introduce inline Python, `find`/`shasum` pipelines, or a
one-time tar inspection as an admission measurement.
Update the sheet’s review-file whitelist to include the inventory, three command
records, and reader-admission record.
Retain the two source-closure check outputs with the external originals, and cite their
hashes in the admission disposition if they are not part of the evidence commit.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
