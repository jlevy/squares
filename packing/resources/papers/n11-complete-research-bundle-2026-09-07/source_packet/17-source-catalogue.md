# Source Catalogue and Packaging Boundary

Research source revision: `4d305597a505ebfbe85f1851fa7148374661e622` (2026-09-06, merged PR 101).

Files 00-02 are editorial synthesis prepared for this review. Files 03-16 are source dossiers, and file 18 is the original SVG. This file identifies every selection. Source paths are repository-relative; no checkout or network access is needed to understand the included mathematics.

The packet contains the complete requested agenda and the complete standalone T-018 claim/certificate/verifier. Other sources are selected by relevance. The full campaign database, raw search streams, large tangent/modulus matrices, runtime dependencies, every other-n certificate, and historical operational receipts are not included. Their scoped results are explicit premises for strategic review; this folder is not an executable clone of sqpack or a standalone replay of every reported computation.

Included-source links point within this folder. Links labelled 'source archive' are optional provenance for omitted implementation or historical detail. Original external literature links are retained as citations, not required reading. An intra-source link may point to the beginning of its included source excerpt; the original section title remains searchable in that file.

Edits to source selections are limited to packet headings, local-link routing, frontmatter displayed as data, generated-banner removal and one footer per file. Executable code and certificate JSON fences are unchanged. The two receipt extracts are explicitly labelled field selections. Historical digests already inside source material are retained; this packet adds no checksum manifest.

Rebuild/check in the repository, using its Python 3.14 environment:

```sh
cd packing
uv run --frozen python -m devtools.build_agenda024_review_packet
uv run --frozen python -m devtools.build_agenda024_review_packet --check
uv run --frozen python -m devtools.build_agenda024_review_packet --zip /tmp/agenda-024-review-packet.zip
```

## Included Source Selections

| Packet file | Frozen repository source and lines |
| --- | --- |
| [03-agenda-024.md](03-agenda-024.md#source-1) | `packing/campaign/agendas/agenda-024-post-381-24h-portfolio.md:1-end` |
| [04-child-agendas.md](04-child-agendas.md#source-1) | `packing/campaign/agendas/agenda-025-adaptive-fractional-frontier.md:467-639` |
| [04-child-agendas.md](04-child-agendas.md#source-2) | `packing/campaign/agendas/agenda-025-adaptive-fractional-frontier.md:913-976` |
| [04-child-agendas.md](04-child-agendas.md#source-3) | `packing/campaign/agendas/agenda-026-density-stationarity-and-trump-capture.md:565-614` |
| [04-child-agendas.md](04-child-agendas.md#source-4) | `packing/campaign/agendas/agenda-026-density-stationarity-and-trump-capture.md:850-1009` |
| [04-child-agendas.md](04-child-agendas.md#source-5) | `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-230-adaptive-core-contract.md:1-245` |
| [04-child-agendas.md](04-child-agendas.md#source-6) | `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-231-next-phases-slice-02.md:1-end` |
| [05-current-assessment-and-review.md](05-current-assessment-and-review.md#source-1) | `docs/project/specs/active/plan-2026-09-06-post-381-research-sequence.md:1-end` |
| [05-current-assessment-and-review.md](05-current-assessment-and-review.md#source-2) | `docs/project/reviews/review-2026-09-06-agenda024-adversarial-senior-strategy.md:1-end` |
| [05-current-assessment-and-review.md](05-current-assessment-and-review.md#source-3) | `packing/campaign/explorations/X-016-after-381-two-managers-one-proof-boundary.md:102-251` |
| [06-alternative-strategies.md](06-alternative-strategies.md#source-1) | `docs/project/reviews/review-2026-09-05-strategy-gpt-56-pro-gemini-grok.md:98-469` |
| [06-alternative-strategies.md](06-alternative-strategies.md#source-2) | `docs/project/reviews/review-2026-09-05-strategy-gpt-56-pro-gemini-grok.md:470-1112` |
| [07-standalone-381-proof.md](07-standalone-381-proof.md#source-1) | `packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md:1-end` |
| [08-dilation-limit.md](08-dilation-limit.md#source-1) | `packing/cases/n11_fractional_certificate/t-022-dilation-limit-proof.md:1-end` |
| [09-trump-construction-and-local-proof.md](09-trump-construction-and-local-proof.md#source-1) | `packing/cases/trump11/packing.py:1-end` |
| [09-trump-construction-and-local-proof.md](09-trump-construction-and-local-proof.md#source-2) | `packing/cases/trump11/isolation-theorem.md:1-233` |
| [09-trump-construction-and-local-proof.md](09-trump-construction-and-local-proof.md#source-3) | `packing/cases/trump11/isolation-theorem.md:349-367` |
| [10-fractional-barriers-and-negatives.md](10-fractional-barriers-and-negatives.md#source-1) | `packing/campaign/explorations/X-014-closing-from-both-ends.md:83-430` |
| [10-fractional-barriers-and-negatives.md](10-fractional-barriers-and-negatives.md#source-2) | `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-064-h-063-two-threshold-class-program.md:148-end` |
| [10-fractional-barriers-and-negatives.md](10-fractional-barriers-and-negatives.md#source-3) | `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-070-h-064-n11-fractional-resume.md:110-end` |
| [10-fractional-barriers-and-negatives.md](10-fractional-barriers-and-negatives.md#source-4) | `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-110-h-090-core-shrink.md:71-end` |
| [10-fractional-barriers-and-negatives.md](10-fractional-barriers-and-negatives.md#source-5) | `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-111-h-091-core-shrink.md:72-end` |
| [11-density-contract-candidate-and-results.md](11-density-contract-candidate-and-results.md#source-1) | `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-242-full-size-density-proof-contract.md:1-end` |
| [11-density-contract-candidate-and-results.md](11-density-contract-candidate-and-results.md#source-2) | `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-113-h-099-trump-support-screen.md:71-end` |
| [11-density-contract-candidate-and-results.md](11-density-contract-candidate-and-results.md#source-3) | `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-115-h-105-fixed-candidate-pair-obstruction.md:70-end` |
| [11-density-contract-candidate-and-results.md](11-density-contract-candidate-and-results.md#source-4) | `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-254-post-screen-next-discriminator.md:206-end` |
| [12-restricted-orientations.md](12-restricted-orientations.md#source-1) | `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-restricted-angle-assessment.md:1-222` |
| [12-restricted-orientations.md](12-restricted-orientations.md#source-2) | `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-114-h-104-fixed-side-auxiliaries.md:67-end` |
| [12-restricted-orientations.md](12-restricted-orientations.md#source-3) | `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-angle-instrument-design.md:19-203` |
| [12-restricted-orientations.md](12-restricted-orientations.md#source-4) | `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-angle-instrument-design.md:287-end` |
| [13-typed-global-structure.md](13-typed-global-structure.md#source-1) | `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-245-typed-backbone-theorem-packet.md:1-end` |
| [14-search-and-near-tight-evidence.md](14-search-and-near-tight-evidence.md#source-1) | `TUTORIAL.md:381-571` |
| [14-search-and-near-tight-evidence.md](14-search-and-near-tight-evidence.md#source-2) | `TUTORIAL.md:907-1028` |
| [14-search-and-near-tight-evidence.md](14-search-and-near-tight-evidence.md#source-3) | `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-063-h-065-n11-near-tight-cell-census.md:123-end` |
| [14-search-and-near-tight-evidence.md](14-search-and-near-tight-evidence.md#source-4) | `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-071-h-070-n11-inset-seed-release.md:87-end` |
| [15-registered-mathematical-questions.md](15-registered-mathematical-questions.md#source-1) | `packing/campaign/hypotheses/H-036-robust-restricted-orientation.md:1-end` |
| [15-registered-mathematical-questions.md](15-registered-mathematical-questions.md#source-2) | `packing/campaign/hypotheses/H-093-n11-scalar-61-16-certificate.md:1-end` |
| [15-registered-mathematical-questions.md](15-registered-mathematical-questions.md#source-3) | `packing/campaign/hypotheses/H-094-n11-weight-and-site-redesign.md:1-end` |
| [15-registered-mathematical-questions.md](15-registered-mathematical-questions.md#source-4) | `packing/campaign/hypotheses/H-095-n11-adaptive-core-certificate.md:1-end` |
| [15-registered-mathematical-questions.md](15-registered-mathematical-questions.md#source-5) | `packing/campaign/hypotheses/H-096-n11-angle-cell-kernels.md:1-end` |
| [15-registered-mathematical-questions.md](15-registered-mathematical-questions.md#source-6) | `packing/campaign/hypotheses/H-097-n11-existential-witness-menus.md:1-end` |
| [15-registered-mathematical-questions.md](15-registered-mathematical-questions.md#source-7) | `packing/campaign/hypotheses/H-098-n11-segment-measures.md:1-end` |
| [15-registered-mathematical-questions.md](15-registered-mathematical-questions.md#source-8) | `packing/campaign/hypotheses/H-099-trump-d4-finite-support-dual.md:1-end` |
| [15-registered-mathematical-questions.md](15-registered-mathematical-questions.md#source-9) | `packing/campaign/hypotheses/H-100-below-trump-area-density.md:1-end` |
| [15-registered-mathematical-questions.md](15-registered-mathematical-questions.md#source-10) | `packing/campaign/hypotheses/H-101-trump-equality-density.md:1-end` |
| [15-registered-mathematical-questions.md](15-registered-mathematical-questions.md#source-11) | `packing/campaign/hypotheses/H-102-complete-restricted-angle-support-families.md:1-end` |
| [15-registered-mathematical-questions.md](15-registered-mathematical-questions.md#source-12) | `packing/campaign/hypotheses/H-103-complete-typed-global-capture.md:1-end` |
| [15-registered-mathematical-questions.md](15-registered-mathematical-questions.md#source-13) | `packing/campaign/hypotheses/H-104-fixed-side-point-cover-auxiliaries.md:1-end` |
| [15-registered-mathematical-questions.md](15-registered-mathematical-questions.md#source-14) | `packing/campaign/hypotheses/H-105-exp113-overweight-pair-obstruction.md:1-end` |
| [16-mathematical-background-and-literature.md](16-mathematical-background-and-literature.md#source-1) | `TUTORIAL.md:35-123` |
| [16-mathematical-background-and-literature.md](16-mathematical-background-and-literature.md#source-2) | `TUTORIAL.md:231-380` |
| [16-mathematical-background-and-literature.md](16-mathematical-background-and-literature.md#source-3) | `TUTORIAL.md:572-883` |
| [16-mathematical-background-and-literature.md](16-mathematical-background-and-literature.md#source-4) | `TUTORIAL.md:1107-1322` |
| [16-mathematical-background-and-literature.md](16-mathematical-background-and-literature.md#source-5) | `packing/resources/papers/stromquist-2003-packing-10-or-11-unit-squares.md:1-end` |
| [16-mathematical-background-and-literature.md](16-mathematical-background-and-literature.md#source-6) | `packing/resources/papers/friedman-ds7-packing-unit-squares-in-squares.md:35-86` |
| [16-mathematical-background-and-literature.md](16-mathematical-background-and-literature.md#source-7) | `packing/resources/papers/dewar-2024-contacts-oriented-squares.raw.md:1-18` |
| [16-mathematical-background-and-literature.md](16-mathematical-background-and-literature.md#source-8) | `packing/resources/papers/dewar-2024-contacts-oriented-squares.raw.md:64-70` |
| [16-mathematical-background-and-literature.md](16-mathematical-background-and-literature.md#source-9) | `packing/resources/papers/dewar-2024-contacts-oriented-squares.raw.md:979-1000` |

Two additional field-selected sources are embedded in files 09 and 11:

- `packing/campaign/series/series-000-smoke-and-calibration/results/bc-241-trump-local-theorem-review.json`
- `packing/campaign/series/series-000-smoke-and-calibration/results/exp-113-h-099-trump-support-screen/packet.json`

## File Sizes

| File | Bytes |
| --- | ---: |
| [00-READ-ME-FIRST.md](00-READ-ME-FIRST.md) | 11,245 |
| [01-research-progress.md](01-research-progress.md) | 22,619 |
| [02-tooling-and-machinery.md](02-tooling-and-machinery.md) | 30,842 |
| [03-agenda-024.md](03-agenda-024.md) | 81,766 |
| [04-child-agendas.md](04-child-agendas.md) | 44,720 |
| [05-current-assessment-and-review.md](05-current-assessment-and-review.md) | 65,486 |
| [06-alternative-strategies.md](06-alternative-strategies.md) | 38,126 |
| [07-standalone-381-proof.md](07-standalone-381-proof.md) | 95,609 |
| [08-dilation-limit.md](08-dilation-limit.md) | 7,648 |
| [09-trump-construction-and-local-proof.md](09-trump-construction-and-local-proof.md) | 18,372 |
| [10-fractional-barriers-and-negatives.md](10-fractional-barriers-and-negatives.md) | 43,194 |
| [11-density-contract-candidate-and-results.md](11-density-contract-candidate-and-results.md) | 51,157 |
| [12-restricted-orientations.md](12-restricted-orientations.md) | 35,214 |
| [13-typed-global-structure.md](13-typed-global-structure.md) | 27,303 |
| [14-search-and-near-tight-evidence.md](14-search-and-near-tight-evidence.md) | 26,293 |
| [15-registered-mathematical-questions.md](15-registered-mathematical-questions.md) | 47,521 |
| [16-mathematical-background-and-literature.md](16-mathematical-background-and-literature.md) | 89,770 |
| [18-trump-packing.svg](18-trump-packing.svg) | 34,276 |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
