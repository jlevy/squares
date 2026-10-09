# Sungjoon Ryu’s Quarter-Power Deficiency Preprint: Reported Intake

Retained from
[squarepacker/k2-minus-c-quarter](https://github.com/squarepacker/k2-minus-c-quarter) at
v1.0, `abbedcf4bba2e4053f0278e669d84966a89c8b73`, committed on 7 October 2026.
[Issue #414](https://github.com/jlevy/squares/issues/414) reports this release; its
archive DOI is [10.5281/zenodo.23211207](https://doi.org/10.5281/zenodo.23211207).

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
`packing/frontier/asymptotic-waste-bounds.yaml`. No checking program was executed here,
and no proof or constant has gained project confirmation.
The bounds concern closed-set disjoint packings and integer sides in the stated
astronomical ranges.
They change no bound at n ≤ 324 and have no T-number.

The constants using Lemma 4.10 depend on Ryu’s k2-minus-c v1.2. The earlier project
replay reproduced its predecessor’s producer computation; it does not independently
confirm the v1.2 proof chain or these new flow arguments.
The variants using analytic Lemma 4.9 are separate reported statements.
Review `think-6ptr` must check the complete dependency chain and theorem-to-checker
bindings before any promotion.

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
uv run --frozen --all-extras --group dev python -m devtools.acquire_source squarepacker-k2-minus-c-quarter-2026-10-07 --check
```

This checks custody, not mathematical validity.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
