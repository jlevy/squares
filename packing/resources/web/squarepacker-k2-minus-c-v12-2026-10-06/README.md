# squarepacker: k² − c, version 1.2

This packet retains Sungjoon Ryu’s version 1.2 preprint from
[squarepacker/k2-minus-c](https://github.com/squarepacker/k2-minus-c/tree/e16a5cfa7eed489ea8d84b500e590bf6855a5f2f),
reported in
[issue #368, comment 6022000514](https://github.com/jlevy/squares/issues/368#issuecomment-6022000514).
The immutable pin is `e16a5cfa7eed489ea8d84b500e590bf6855a5f2f`, tagged `v1.2`,
committed 6 October 2026 UTC and retrieved 8 October 2026 UTC. The author archives this
version as DOI [10.5281/zenodo.23194031](https://doi.org/10.5281/zenodo.23194031).

## Retained source and credit

The complete 78-file version composition is recorded in
`acquisition/upstream-subtree.sha256` and `acquisition/sources.json`. Ten changed files
are retained byte for byte under `source/`, including the primary TeX, PDF, README,
reviews and changed constant-checking programs.
The other 68 files are byte-identical to the
[version 1.1 packet](../squarepacker-k2-minus-c-2026-10-05/README.md); explicit
`pinned_only` records name those retained copies and their digests.
The acquisition check compares the original bytes of each copy.
Archived upstream text is unchanged.

Ryu takes responsibility for the work and reports extensive Claude assistance in the
proofs, text, programs and Lemma 4.10 computation.
The source is not peer reviewed; its AI review summaries are source material.
Code and data retain the original MIT licence; the paper retains CC BY 4.0. Both licence
files are unchanged and bound to their version 1.1 copies in the manifest.

## Reported claims and review boundary

The primary Theorem 1.1 concerns unit squares pairwise disjoint **as closed sets** in
`[0,k]²`, for every integer `k >= 2`, with natural logarithms.
It reports deficiency at least `0.0353 log k` and the explicit lower bound
`1.99954 (log k − 13.06675) / 30.418`, with asymptotic coefficient `0.0657`. The
analytic variant reports `0.0319` without the computer-assisted Lemma 4.10. Corollary
1.3 reports `0.0541 log k` conditional on Daniel’s `s(k² − 3) = k` for integers
`k >= 6`.

The numerical consequences are independently checked in the maintained
`cases/asymptotic/ryu_k2_minus_c_constants.py`: 34 interval rows for nine-overlap and 30
for thirteen-overlap, with distinct all-k coefficients and a conditional
Daniel-dependent consequence confined to nine-overlap.
Negative controls reject stricter source bounds, nonpositive physical domains and a
fractional grid cutoff.
The arithmetic is conditional on the source’s geometric lemmas and coverage.
The scoped review is
[retained here](../../../../docs/project/reviews/review-2026-10-08-squarepacker-k2-minus-c-v12.md).

All thirteen original deciding leaf lists and their checking programs are byte-identical
to the earlier replay inputs.
Its Lemma 4.10 subclaim therefore retains the original runtime and outcomes; this does
not transfer the changed whole-source manifest to the new proof.
The independent per-box labelling obligation remains `think-k3tk`. The revised proof’s
remaining floating-count obligation is tracked in the scoped review under `think-gcft`.
No upstream program was executed for this acquisition, and no small-count bound,
register T-number, or global optimality claim is added.

## Rechecking custody

From `packing/`, using the project interpreter:

```bash
uv run --frozen --all-extras --group dev python -m devtools.acquire_source squarepacker-k2-minus-c-v12-2026-10-06 --check
```

This checks the full version manifest, retained bytes and all 68 referenced copies.
It does not verify the theorem.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
