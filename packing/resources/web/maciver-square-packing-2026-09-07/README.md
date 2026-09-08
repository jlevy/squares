# David MacIver’s Square-Packing Papers, Retrieved 2026-09-07

David R. MacIver’s
[Square Packing Research](https://drmaciver.github.io/square-packing-research/) contains
three author-hosted manuscripts and Lean source.
This packet preserves the three PDFs served by that site at repository commit
[`9e2cd597047e040a63b7dcd103e79962cfc2d781`](https://github.com/DRMacIver/square-packing-research/commit/9e2cd597047e040a63b7dcd103e79962cfc2d781),
dated 2026-08-10 13:30:26 UTC. The original commit response is retained as
[source-commit.json](source-commit.json).

These are source claims awaiting independent review here.
MacIver’s claimed `s(17), s(18) > (40sqrt(2)+19)/17 + 1/200 ≈ 4.450208382054341` is
weaker than this repository’s independently verified `459/100 = 4.59`; it changes
neither verified lower bound.
The source’s AI-assistance and incomplete human-review disclosures appear in all three
abstracts and on its landing page.

The [independently reviewed method assessment](../../../../docs/project/reviews/review-2026-09-07-maciver-square-packing.md)
retains the exact comparison and concrete local-capacity controls.

## Papers and Dates

All three title pages name David R. MacIver.
They were inspected as rendered PDFs.
Dates below are the manuscripts’ printed dates, distinct from the archived commit date.
No journal venue or DOI for these manuscripts was identified in the inspected source.

| Manuscript | Printed date | Retained PDF | Faithful extraction |
| --- | --- | --- | --- |
| *The Center-Area Lemma: Three disjoint unit squares whose centers form a non-obtuse triangle span area at least 1/2* | No date printed; present at the pinned August 2026 commit | [PDF, 24 pages](maciver-2026-center-area-lemma.pdf) | [Raw text](maciver-2026-center-area-lemma.raw.md) |
| *An improved lower bound for packing seventeen unit squares in a square, via a deformation of Green’s scaffold with certified defect charging* | 8 August 2026 | [PDF, 26 pages](maciver-2026-seventeen-unit-squares-lower-bound.pdf) | [Raw text](maciver-2026-seventeen-unit-squares-lower-bound.raw.md) |
| *Counting unit squares by their centers: sharp convex bounds and exact strip laws* | August 2026 | [PDF, 24 pages](maciver-2026-counting-unit-squares-by-centers.pdf) | [Raw text](maciver-2026-counting-unit-squares-by-centers.raw.md) |

The PDFs came from these paths at the pinned commit:

- [Center-area paper](https://github.com/DRMacIver/square-packing-research/blob/9e2cd597047e040a63b7dcd103e79962cfc2d781/papers/center-area-lemma/paper.pdf)
- [Seventeen-square paper](https://github.com/DRMacIver/square-packing-research/blob/9e2cd597047e040a63b7dcd103e79962cfc2d781/papers/s17-lower-bound/paper.pdf)
- [Center-count paper](https://github.com/DRMacIver/square-packing-research/blob/9e2cd597047e040a63b7dcd103e79962cfc2d781/papers/nmax/paper.pdf)

The source
[Pages workflow](https://github.com/DRMacIver/square-packing-research/blob/9e2cd597047e040a63b7dcd103e79962cfc2d781/.github/workflows/pages.yml)
copies these files to the public site.
The neighboring `rewrite/paper.pdf` files are different drafts and are not the deployed
PDFs. Each `.raw.md` is unedited output from `pdftotext -layout`; this README is a
reading aid, not a cleaned transcription.
No license declaration was found in the inspected repository snapshot.

GitHub’s public API reports successful
[Lean build](https://github.com/DRMacIver/square-packing-research/actions/runs/31393239180)
and
[Pages deployment](https://github.com/DRMacIver/square-packing-research/actions/runs/31393239247)
runs at the pinned commit on August 10; the response is retained as
[source-ci-runs.json](source-ci-runs.json).
This corroborates upstream build and publication status.
It is not a local proof replay, and individual job logs were not inspected.

## Claims and Verification Limits

The center-area paper’s Theorem 1.1, page 1, concerns three arbitrarily oriented unit
squares with pairwise disjoint interiors.
If their center triangle is non-obtuse, its area is at least `1/2`, with equality
attainable. The non-obtuse condition is essential.
The author reports two Lean proofs.
No local Lean build or full proof audit was performed for this source-intake record.
This lemma alone supplies no new value of `s(n)`.

The seventeen-square paper states its strict lower bound in Theorem 1.1 and transfers it
to eighteen squares in Corollary 1.2, both on page 1. Its Appendix A distinguishes the
public Lean algebra from the essential computation.
The available
[`PaperProofs/S17Paper.lean`](https://github.com/DRMacIver/square-packing-research/blob/9e2cd597047e040a63b7dcd103e79962cfc2d781/PaperProofs/S17Paper.lean)
proves deformation identities, numerical inequalities, and an abstract counting
identity. It does not formalize the complete packing impossibility theorem.

The theorem also consumes fourteen interval–Farkas certificates, C1–C14, and an exact
enumeration of 634,562 compatible rows.
The complete pinned source snapshot contains none of the fourteen named `.cert.json` or
`.cert.json.gz` files, none of the cited `scripts/s17_green_*.py` replay files, and no
Makefile providing the paper’s replay targets.
Its
[audit](https://github.com/DRMacIver/square-packing-research/blob/9e2cd597047e040a63b7dcd103e79962cfc2d781/papers/s17-lower-bound/LEAN-CHECK.md)
locates those files in an author-local checkout.
A retained
[aggregate-run log](https://github.com/DRMacIver/square-packing-research/blob/9e2cd597047e040a63b7dcd103e79962cfc2d781/papers/s17-lower-bound/aggregate_replay_2026-08-08.log)
reports success, but does not provide the missing proof data or replay implementation.
This absence finding is scoped to the inspected commit, not to every possible public
branch or future release.

The center-count paper’s Theorem 1.1, page 1, claims `N ≤ area(K ⊕ [-1/2,1/2]^2)` for
centers constrained to a compact convex region `K`. The squares themselves may extend
outside `K`. Its
[Lean wrapper](https://github.com/DRMacIver/square-packing-research/blob/9e2cd597047e040a63b7dcd103e79962cfc2d781/PaperProofs/NmaxPaper.lean)
covers the rectangle bound, equality for integer rectangle sides, and the exact
very-narrow-strip law for `0 ≤ w ≤ (sqrt(2)-1)/2`. It expressly excludes the general
convex Minkowski bound.
These distinctions must accompany any use as a packing-search lemma.

## Separate Methodological Claim

The repository’s
[publication-candidate list, first methodological note](https://github.com/DRMacIver/square-packing-research/blob/9e2cd597047e040a63b7dcd103e79962cfc2d781/PUBLICATION-CANDIDATES.md)
and
[square-solver report](https://github.com/DRMacIver/square-packing-research/blob/9e2cd597047e040a63b7dcd103e79962cfc2d781/reports/square-solver.md)
assert a `4.5` ceiling for witness-measure methods while saying exact rational LP duals
still need to be obtained.
Read as a universal statement about weighted unavoidable measures, that assertion
conflicts with this repository’s verified certificate at `4.59`. Recover the precise
optimization domain and exact dual before treating it as a barrier.
It is separate from the three manuscripts’ main theorems and is unsupported at the
stated generality.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
