# Finite-Case Literature Query Log, 2026-08-31

This bounded query log records the negative literature result used by
[`X-011`](../../../campaign/explorations/X-011-controls-are-not-targets.md).
The searches ran through Codex's general web-search interface with its default locale
and ranking; the underlying engine, result ids, ranking snapshot, and query URLs were
not exposed or retained. The strings can be rerun, but this record is not a repeatable
search receipt and may retrieve a different corpus. It is not a systematic-review claim
and does not prove that no unindexed paper exists.

## Scope

- **Question:** did a 2020--2026 paper establish a new finite-case record, exact value,
  or case-specific bound for `n = 17--19, 37, 39, 41, 50, 51, 53--55, 68, 69`?
- **Run:** 2026-08-31 Pacific time / 2026-09-01 UTC.
- **Surfaces:** general web search with site restrictions, direct arXiv records, and the
  Electronic Journal of Combinatorics article index.
- **Evidence rule:** a search-result snippet can route inspection but cannot establish a
  mathematical claim. Only author, preprint, journal, or retained first-party pages are
  treated as claim sources.

## Query log

The search strings were:

```text
site:arxiv.org/abs "packing unit squares" square 2020..2026 finite n 17 18 19
site:arxiv.org/abs "unit squares in a square" packing 37 39 41 50 51 53 54 55
site:arxiv.org/abs square packing unit squares 68 69 record
"packing unit squares in a square" 2026 Burns Massaccesi
site:arxiv.org/abs "unit squares" "wasted area" square packing 2025 Bui
site:arxiv.org/abs "packing unit squares in a square" McClenagan 2026
site:combinatorics.org "packing unit squares" 2020 2021 2022 2023 2024 2025 2026
site:doi.org "packing unit squares in a square" 2020 2021 2022 2023 2024 2025 2026
```

Direct URL checks then opened the known `n = 17` author post, the recent arXiv records,
and the 2021 Electronic Journal of Combinatorics construction paper.

## Retrieved relevant primary sources

| Source | Date | Scope | Effect on the prioritized finite cases |
| --- | --- | --- | --- |
| [Sam Burns, proposed `n = 17` lower bound](https://sam-burns.com/posts/proposing-better-lower-bound-for-n17-square-packing/) | 2026-08-06 | proposed fixed weighted certificate at `4.4811` | Relevant proposal, but explicitly not independently implemented or peer reviewed; retained in the adjacent `n17-lower-bounds-2026` archive |
| [Gustavo Massaccesi, proposed `n = 17` lower bound](https://gus-massa.blogspot.com/2026/08/another-better-lower-bound-for-n17.html) | 2026-08 | proposed fixed weighted certificate at `4.5058` | Relevant proposal and verifier; not a paper or adopted bound; retained and replayed locally |
| [Arslanov, Mustafin, and Shangitbayev, *Improved Packings of n(n-1) Unit Squares in a Square*](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v28i4p22) | 2021-11-05 | constructive family for `n^2-n` when the parameter is at least 12, plus three larger exceptions | Already represented in the project; it does not change any prioritized finite case below 100 |
| [Hong Duc Bui, *Square Packing with Asymptotically Smallest Waste Only Needs Good Squares*](https://arxiv.org/abs/2504.09489) | 2025-04-13 | asymptotic structural reduction | No finite-case record or exact value |
| [Hong Duc Bui, *Square packing with O(x^0.6) wasted area*](https://arxiv.org/abs/2508.04603) | 2025-08-06; revised 2026-03-15 | asymptotic construction | No finite-case record or exact value for the prioritized list |
| [Rory McClenagan, *Optimally Packing a Large Square by Unit Squares*](https://arxiv.org/abs/2602.01484) | 2026-02-01 | asymptotic `O(x^(3/5))` waste construction | No finite-case record or exact value |

The searches also returned the 2009 Friedman survey, Nagamochi's 2005 general lower
bound, older optimality papers, and unrelated online, polygon, and circle-packing work.
Those results do not supply a new 2020--2026 finite-case theorem for the target list.

## Bounded conclusion

No additional 2020--2026 paper in this retrieved corpus establishes a finite-case
record, exact value, or target-specific bound for the prioritized cases. The Arslanov
family begins above this below-100 list, while the Bui and McClenagan results are
asymptotic rather than target-specific. The recent finite-case changes remain
first-party web evidence: catalogue entries and SVGs, UnitSquare's release,
run-statistics artifacts, and the two proposed `n = 17` weighted certificates.

This conclusion is deliberately narrower than “the literature is complete.” Search
index coverage, unpublished correspondence, and uncited papers remain possible gaps.
The run did not systematically cover non-English search terms, translated titles,
author-name variants, or every spelling and transliteration of the prioritized cases.
Repeat the audit if a live catalogue adds an author, DOI, theorem citation, or method
claim not present in the retained source record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
