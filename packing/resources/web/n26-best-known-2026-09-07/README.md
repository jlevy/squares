# Sources for the Twenty-Six-Square Record Review

Retrieved September 7, 2026 PDT, extending into September 8 UTC, for the
[n = 26 best-known audit](../../../../docs/project/research/research-2026-09-07-n26-best-known-audit.md).
The reviewed problem allows arbitrary orientations of 26 congruent unit squares in a
square container. The search identified no reported upper packing below Friedman’s
$U=(7+3\sqrt2)/2$.

## Retained Artifacts

| File | Primary source and revision | Preservation |
| --- | --- | --- |
| [tilted-squares-in-square.json](tilted-squares-in-square.json) | [MinMax Arena data](https://minmaxarena.com/data/tilted-squares-in-square.json), `generatedAt: 2026-09-08T00:34:07.581Z` | Complete retrieved JSON. The n = 26 record is `p18-n26-v1`, dated `2026-09-02T18:06:21.856Z`. |
| [chelokot-manifest-n26.extract.json](chelokot-manifest-n26.extract.json) | [Manifest at 753079eb](https://github.com/chelokot/square-packing-archive/blob/753079eb37d8d16225a5dc1f56e493a3c3b243f4/archive/manifest.json) | JSON selection of objects with `n == 26`, serialized by `gh api --jq`; whitespace normalized. |
| [chelokot-square-26-tracker.json](chelokot-square-26-tracker.json) | [Exact configuration at 753079eb](https://github.com/chelokot/square-packing-archive/blob/753079eb37d8d16225a5dc1f56e493a3c3b243f4/archive/configurations/square-26-tracker.json) | Complete source bytes. Git blob `201372a0e3a4b8539ff51f5f44e9c99a4d43dab2` matches the upstream content identifier. |
| [chelokot-square26tracker.lean.txt](chelokot-square26tracker.lean.txt) | [Lean theorem at 753079eb](https://github.com/chelokot/square-packing-archive/blob/753079eb37d8d16225a5dc1f56e493a3c3b243f4/formal/SquarePackingArchive/Records/Square26Tracker.lean) | Complete source bytes, stored as text for inspection. Git blob `07a5d035d0c9c0600e79379041ba79bf9b02ebaf` matches the upstream content identifier. |
| [evanoman-squares-n26.extract.json](evanoman-squares-n26.extract.json) | [Square data at 1004f62c](https://github.com/EvanOman/squares-in-squares/blob/1004f62cdb2a283ab386c7da54f11871e3bd71d7/site/data/squares.json) | JSON selection of objects with `n == 26`, serialized by `gh api --jq`. This preserves the exact-expression text; decimal formatting is the API query renderer’s output, not a preservation of every original numeric token. |
| [forloopcodes-best-packings-n26.extract.json](forloopcodes-best-packings-n26.extract.json) | [Cached packings at 6a5646de](https://github.com/forloopcodes/least-space-squares/blob/6a5646dec9d89a5f750adcf488c769b60fe5ccf9/data/best_packings.json) | The complete outer `"26"` value, sliced from the raw 81,200-byte response without reserializing its numeric tokens. The retained `s` token is `5.621320343794426`. |

The chelokot commit is dated September 5, 2026, 21:42:12 UTC; the EvanOman commit,
September 3, 2026, 01:49:39 UTC; and the forloopcodes commit, September 3, 2026,
04:25:56 UTC. Commit dates identify the fetched snapshots; each project’s individual
record and verification dates have their own meanings.

The two full chelokot files were checked against the GitHub content API’s blob
identifiers using `git hash-object`. The extracts are intentionally smaller than their
upstream files and cannot match those full-file identifiers.
Preserve these archived sources as source material rather than formatting them.

## Claim Status

The chelokot manifest reports exact $U$, discovery by Friedman in 1997, and a Lean check
dated September 6, 2026. The retained module states `HasPacking 26 U`; its imported
soundness theorem and Lean build were not independently replayed here.
The configuration records import from Ellsworth’s
[square-26b.svg](https://kingbird.myphotos.cc/packing/square-26b.svg).
EvanOman’s record imports the same SVG, preserves the same exact expression, and marks
the optimum unproved.
Neither source supplies a smaller side.

The forloopcodes cached side is above $U$. Its README demonstration prints
`5.621320343560`, which is a rounded display of the reference neighborhood and cannot
rank a distinct construction at that precision.
The project’s stated geometry tolerance is $10^{-9}$; its numerical check is not adopted
as an exact feasibility certificate.

MinMax Arena maximizes the smallest square side inside a unit container.
Its stored score `31646327699330128` corresponds to the squared side
$R=1977895481208133/62500000000000000$. The
[scalar comparison results](../../../cases/stromquist/n26-source-scores.json) give
$R<1/U^2$, so the submitted score implies a normalized container side of approximately
$5.6213203992203053755>U$. The source’s n = 26 geometry has not received an independent
all-pair replay in this review.
Ranking its stated smallest side against $U$ does not require accepting its feasibility
assurance.

The
[research report](../../../../docs/project/research/research-2026-09-07-n26-best-known-audit.md)
retains the broader source coverage, query families, exclusions, and conditions for
reopening the record review.
None of the newly archived external verification claims changes the mathematical
frontier.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
