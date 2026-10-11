# Review of FN-1 Original Compressed Input Custody

Reviewer: independently assigned GPT-6 Astra strong agent.
Date: 8 October 2026 UTC, 7 October in the host’s America/Los_Angeles timezone.
Reviewed source checkpoint: `cc0e5aa017834ad12bd019cefcf516c1ae90a1da`.

## Decision and Scope

**Accepted for original-input byte custody.** No source defect was found in the reviewed
acquisition extension, complete eight-input binding command or bounded negative
controls. This acceptance does not establish a new geometric result or increase any
assurance rating. Actual private-worker admission remains pending the final merged
snapshot’s unchanged storage gate and its full positive, mutation-refusal and
restoration test.

The
[source supplement](../../../packing/resources/web/wand125-fn1-input-bindings-2026-10-07/README.md)
retains eleven selected upstream files from `wand125/square-packing-bounds` at
`b73473fcf60421222b739294d3f7d9c4a8b8da07`: eight original gzip inputs, the binding
manifest, its source explanation and the MIT licence.
Their total original size is 201,666 bytes; the eight compressed inputs total 193,716
bytes. The earlier check2 source remains pinned at
`2fad66e02f54a492835dc41ac37a9184e1e7a662`. No upstream program was executed in this
review.

## Complete Binding and Acquisition Contract

The exact roster is n=19, 20, 26, 27, 28, 30, 39 and 41. The maintained
[`wand125_fn1_bindings.py`](../../../packing/devtools/wand125_fn1_bindings.py) requires
every case in the declared order, exact source paths and exact entry keys.
For each full original input, the raw compressed SHA-256 must match the new source
manifest, the previously recorded admission constant and the original check2 receipt’s
input hash.
Decompression must then equal the complete previously retained candidate byte
for byte. The decompressed file hash and mathematical candidate digest must also agree
with both the source manifest and the earlier receipt.
These are separate bindings: equivalent reserialized JSON or a recompressed gzip stream
cannot substitute for the original bytes.

The acquisition extension is explicit and opt-in.
The declaration and acquisition record enumerate `original_gzip` paths, and a separate
Original Gzip Files table binds raw compressed bytes and original Git blobs.
Ordinary Compressed Files rows retain their existing decompressed-byte meaning.
The default acquisition refusal for an undeclared upstream gzip remains in force.
The checker rejects mismatched declarations, records, source hashes, table rows,
duplicate or missing paths, and paths outside the declared scope.
Existing archive-reader behavior is preserved.

Every invocation rereads the complete inputs and old records.
The binding command refuses symlinks at any declared private path component, including
links to another location inside the same repository.
Compressed and decompressed reads are bounded.
The explicit private-worker roster carries all eight raw inputs, all eight prior full
candidates and receipts, both acquisition records, the binding manifest and supporting
packet files. No geometry or deciding receipt is replaced by a summary.
The new fast/records step checks this custody boundary; it runs no packing verifier and
changes no native scientific record, bound or rating.

## Independent Verification

From the frozen tree’s `packing/` directory with project Python 3.14.7, external
`TMPDIR`, `CARGO_TARGET_DIR` and `UV_CACHE_DIR`, the reviewer ran:

```sh
python -m pytest -q --durations=5 -p no:cacheprovider tests/test_acquire_original_gzip.py tests/test_fn1_input_bindings.py -k 'not actual_worker'
python -m devtools.wand125_fn1_bindings
```

The bounded test selection passed **21 tests, one deselected, in 11.24 seconds**. It
checks original headers, compressed bytes and Git blobs; default refusal; recompression;
receipt input/file/mathematical-digest mutations on a second invocation; semantically
equivalent but byte-different candidates; rebound missing, duplicate, reordered or
outside-path manifests; and private symlink refusal.
The complete production-source command exited zero, admitted all eight inputs and
reported `geometry_replay: false` and `bounds_changed: false`. Its command wall time was
0.126 seconds.

Receipts are `fn1-independent-binding-tests.log` and
`fn1-independent-complete-binding.json` in the external review task directory.
The writer separately reports 78 existing acquisition/decompression regression tests
passing and zero scoped type findings; those were not repeated by this reviewer.

## Remaining Integration Gate

The writer’s pre-#432 source measurement was 201,334,850 bytes against the unchanged
201,326,592-byte ceiling, exceeding it by 8,258 bytes.
That failure is retained rather than treated as admission.
The owner has an actual production-clone regression that checks every private input is
copied once as an ordinary byte-identical file, runs complete admission, changes a
copied receipt’s input hash, requires refusal, restores the original bytes and admits
again. Each subprocess retains a 45-second timeout.
This test was deliberately excluded here until the final parent merge and source-size
gate permit the real clone.
A smaller fixture is not a substitute for that remaining test.

No source-cap increase, missing input, borrowed link, geometric replay or assurance
promotion is authorized or implied by this review.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
