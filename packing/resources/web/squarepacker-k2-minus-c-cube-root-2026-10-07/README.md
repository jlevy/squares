# Sungjoon Ryu’s Cube-Root Deficiency Preprint: Reported Intake

Retained from
[squarepacker/k2-minus-c-cube-root](https://github.com/squarepacker/k2-minus-c-cube-root)
at v1.0, `15045f9c6b74bd52f60394b9be593ebe4fb3debc`, committed on 7 October 2026.
[Issue #414](https://github.com/jlevy/squares/issues/414) reports this release; its
archive DOI is [10.5281/zenodo.23212059](https://doi.org/10.5281/zenodo.23212059).

## Scope and Status

`source/paper/paper.tex` and `source/paper/paper.pdf` are the complete, unchanged
primary text.
The source README, attribution, licences, review summary and constant-check
programs are retained alongside them.
The acquisition declaration and sources record bind every retained file to the release’s
Git tree; `acquisition/upstream-subtree.sha256` is the selected-source manifest.
Numerical analogue campaigns are outside this packet.
There is no cleaned Markdown transcription; the original TeX remains searchable.

The theorem statements were read from the primary text and are recorded as reported in
`packing/frontier/asymptotic-waste-bounds.yaml`. None of the source’s checking programs
was executed here. The theorems have no result-register entry and so no rung.
The bounds concern closed-set disjoint packings and integer sides in the stated
astronomical ranges.
They change no bound at n ≤ 324 and have no T-number.

The constants using Lemma 4.10 depend on Ryu’s k2-minus-c v1.2. The earlier project
replay reproduced its predecessor’s producer computation; it does not independently
confirm the v1.2 proof chain or these new flow arguments.
The variants using analytic Lemma 4.9 are separate reported statements.
Two reviews have read the argument:
[the 8 October review](../../../../docs/project/reviews/review-2026-10-08-quarter-cube-proof-chains.md),
at source-review scope, and
[the strongest-tier review of 2 November](../../../../docs/project/reviews/review-2026-11-02-ryu-quarter-cube-strongest-tier.md),
which accepted it. That review’s programs, which recompute this paper’s constants and
all eight cases of its Table 1, are kept in
[the quarter-power packet](../squarepacker-k2-minus-c-quarter-2026-10-07/review/quarter-cube-strongest-tier-2026-11-02/README.md).
Neither review ran the source’s programs.
The independent per-box labelling of v1.2’s Lemma 4.10 remains think-k3tk’s.

## Credit and Licence

Sungjoon Ryu authored the preprint and programs.
The source states extensive Claude (Anthropic) assistance with proofs, text and
programs, and no human peer review.
Earlier AI reviews and analogue tests are author-supplied evidence.
The original notices license the paper under CC BY 4.0 and the programs under MIT. The
source credits the Square Packing Project’s earlier producer replay; that credit is
preserved without claiming an independent replay.

## Check Retained Bytes

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source squarepacker-k2-minus-c-cube-root-2026-10-07 --check
```

This checks custody, not mathematical validity.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
