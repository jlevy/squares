# Review of the Rung-0 Certificate Contract, 23 September 2026

A W2 factual review (Fable, extra-high thinking) of the instrument behind
[H-236](../../../packing/campaign/hypotheses/H-236-n11-fixed-angle-global-optimality-at-trump.md),
the first rung of X-046’s n11 settlement ladder: the producer
`packing/cases/trump11/fixed_angle_tree.py`, the independent reader
`fixed_angle_tree_check.py` and their tests, at frozen digests `af1179a5` (producer) and
`c4ae4e48` (reader), with Amendment 1 adding only a resume-by-subtree schedule (0 lines
removed, 99 added in `frontier_paths`, `_grow_resumed`, `run_resume` and the CLI).
[Session 156](../../../packing/campaign/agent-sessions/session-156-w3-overnight-n11-settlement.md)
commissioned it while the resumed run was still in progress, so it reviews the contract,
not the run’s outcome.

## Verdict

**The contract is sound.** If the resumed run’s reader returns `closed` with no
unresolved leaves, the declared half-tangent box, `target_is_at_least_U: true` and at
least one Trump-degenerate leaf, H-236 may be recorded as confirmed at “verified, exact,
pending BC-241”. No mathematics has to change first.

A `closed` verdict with no Trump-degenerate leaf would be a contradiction, not a result:
Trump’s pose is feasible at side $U$ and satisfies every symmetry row, so it must lie in
some leaf, and that leaf can only close through the local theorem.

## The Six Obligations

| Obligation | Verdict | Why |
| --- | --- | --- |
| Core containment | Proved, exact | Rotations are exact for rational half-tangents; the endpoint tests plus the closed-arc test equal the maximum extent over the swept window, which is below $\pi/2$. The reader refuses a core $10^{-7}$ too large. |
| Separating axes | Complete, exact | With centrally symmetric cores the Minkowski difference’s edge normals are the union of both cores’ normals, so interior-disjointness is exactly one non-strict row per pair. |
| Symmetry rows | The lemma holds | A quarter turn about the container’s centre keeps the tilted class’s orientation modulo $\pi/2$, so one of the four turns puts the tilted centroid in the closed quadrant; sorting each class afterwards is a relabelling that leaves class sums unchanged. Trump’s declared image is the unique orbit element satisfying all rows. |
| Leaf certificates | Valid for every feasible point | The dual bound holds for any nonnegative multiplier on the box $[0,4]$, which contains every relevant packing; comparison is strict against a 45-digit upper end of $U$ that the reader re-brackets independently. |
| Trump-degenerate leaves | A valid use of BC-240 | Every packing in such a leaf maps by a sup-norm isometry into BC-240’s ball, whose first clause forces equality; the reader rebuilds the image and refuses a wrong label, turn or radius. The scope inherits BC-240’s pending BC-241 review. |
| Tree completeness | Checked | Every branch’s children exhaust its disjunction, and all 256 subtree files attach to exactly the frontier paths the producer records. |

## Findings to Carry Into the Record

| Severity | Finding |
| --- | --- |
| material | The registered negative control (“side $U+10^{-3}$ does not close”) is met only at producer level: the full tree stopped at its node cap with no open leaf, and the Trump-cell control (open at $3.877081$) was produced from a non-root cell the reader does not accept. No reader-verified n11 negative control exists. |
| material | H-236’s instrument field named `sqpack.exact_lp`; the instrument uses scipy’s HiGHS binding for float proposals and exact `Fraction` arithmetic for every decision. Corrected in the record. |
| minor | The reader checks the $U$ bracket only when the target is labelled `U` and does not compare the declared box with $\pm10^{-6}$; the final record must read both fields from the reader’s output. |
| minor | A missing subtree file raises an exception rather than a `rejected` verdict; it is not a false-accept path. |
| minor | Producer and reader share `cases/trump11/packing.py` and `sqpack.field.NumberField`; the trust base should be stated with the result. |
| minor | Sixteen tampering probes were all refused for the right reason; none of them is yet a test. |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
