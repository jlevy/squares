# Drawing runs for the T-335 adoption at 109

On 21 November 2026 UTC, the adoption writer replaced T-101 with Samanyu-dev’s
[T-335](../../../frontier/RESULTS.md), the canonical rational derivation of the 7
November pinwheel. The exact side rounds up to $10.949289580946$ at 12 places.
The two strong generators used the new witness under the
[house drawing rule](../../../campaign/result-import.md#adopt-a-house-then-regularize-it).

| Run | Outcome |
| --- | --- |
| Grid-slack at 0.5°, 1° and 5° | No view. The exact re-solves were ill-conditioned or left overlapping pairs. The per-count reports record the refusal for each attempt. |
| Evan Daniel’s driver at `675a5ea` | The same-side re-solve refused on unmatched rotation. The selector held the solved-side candidate at row 3, about $2.026 \times 10^{-12}$ below the registered upper bound. |
| Selection | The axis view draws T-335 at its exact side. The new drawing is settled as `decided-no-better` and the solved-side candidate is queued separately under `think-26s0`. |

The old T-101 house drawing had no uneven or near-axis squares and 368 full shared
sides. The new T-335 axis view has four uneven and four near-axis squares, 204 full
shared sides on the house measure and 256 on the stage measure.
On the new witness the axis view improves the raw house drawing from 12 light squares to
zero, 24 uneven squares to four and 160 full shared sides to 204. The exact side is the
same in both views of T-335.

The grid-slack reports recorded 40.77 seconds in total.
Evan Daniel’s receipt recorded 12.40 CPU-seconds with one worker.
The strong runs and selection used the project interpreter and the macOS memory guard.

The three grid-slack blocks and Evan Daniel receipt sit beside their compressed
per-count reports. The selection is retained as JSON and Markdown.
The Evan Daniel run also retains the solver certificate and derived Witness/v2 for the
separate review. Their uncompressed SHA-256 digests are
`5268dfdaa9038f42588df8efbd8b177e54ac86b20a0ae45e78c00449375ff8f2` and
`f7e7eb72dc794c0c10cfe8490262aebec65fd95192a102f0c0da51b82419187e`, respectively.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
