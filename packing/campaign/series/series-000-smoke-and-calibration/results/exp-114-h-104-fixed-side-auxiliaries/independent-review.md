# exp-114: Independent Receipt-Checker Readiness

Status: source/toy implementation checkpoint under `think-jhs4`, 2026-09-06. No target
reconstruction, target geometry, target packet replay, or H-104 verdict has occurred.
The original commission ends at 21:14 UTC; no extension is assumed.

The reusable reader is
[`check_restricted_orientation_discriminator.py`](../../../../../devtools/check_restricted_orientation_discriminator.py).
Its CLI takes one retained packet, an explicit `--source-control` or
`--target-fixed-side` mode, and the independently retained `--producer-exit-code N`. It
installs a fixed ten-second POSIX alarm before reading the packet.
The coordinator owns the separate prospective target dispatch and exit receipt.

The checker imports no producer geometry.
It transcribes the point formulas separately and uses rational pairs for $a+b\sqrt2$,
deciding signs by rational squared comparisons.
Closed membership at 45 degrees uses $|dx+dy|\leq\sqrt2/2$ and $|dy-dx|\leq\sqrt2/2$;
containment uses the exact coordinate half-extents.
All seven witness predicates are checked separately.
The ten-set may be serialized in any order, with its masks checked in that same order;
the twelve-set and A-label order must match the frozen formulas exactly.

The reader checks the fixed side and field, point inventories, Boolean-or-null outcomes,
completed angle prefix, nonempty stratum counts, checked/unchecked inventories, exit and
completion agreement, and one independently verified witness per false clause.
Duplicate JSON keys, nonfinite numbers, noncanonical coordinates, and oversized files or
coefficients refuse.
It is not a general external proof format: positive acceptance still relies on the
reviewed exhaustive algorithm, not on the reported counts.
Timing/status prose and additional packet fields are not an independent certificate.

A checked false clause rejects the conjunction even if other angles are unfinished.
Without a checked false clause, an incomplete run remains unresolved.
Every result keeps H-036 unresolved and explicitly denies standalone exhaustive
certification. Neither a closed-unit escape nor a positive exact-angle receipt decides
H-036’s angle neighborhoods or constructs an eleven-square packing.

Nine source/toy tests passed in the first run: pytest 1.68 seconds, process wall 1.96
seconds, CPU 1.90 seconds.
They compare independently reconstructed source formulas with the producer’s source
packet, mutate the point/outcome/exit contract, exercise every escape predicate on
side-four toys, retain closed-corner membership, test near-cancelling quadratic signs,
and refuse malformed JSON and coordinates.
Target mode is not exercised.
Ruff/BasedPyright findings during development were corrected.

The focused command from `packing/` is:

```bash
UV_CACHE_DIR=/private/tmp/squares-uv-cache uv run --frozen --no-sync --all-extras --group dev python -m pytest -q tests/test_restricted_orientation_packet_review.py
```

The caller must still review the new checker and retain the separately capped target
packet replay before using it for exp-114 disposition.
The CLI’s alarm path and conjunction-with-partial-negative transition have code review
but no new dedicated end-to-end regression in this short implementation slice.
No independent exhaustive positive checker was built or implied.
The coordinator owns any remaining readiness decision and publication.

Only this report, the independent reader, and its focused test file were authored.
Experiment-loop/tbd kept source controls separate from target authority; Practical
Prose/de-slop and Flowmark guided the report.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
