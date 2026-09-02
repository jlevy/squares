# Finite-Case Literature Query Log, 2026-08-31

This bounded query log records the negative literature result used by
[`X-011`](../../../campaign/explorations/X-011-controls-are-not-targets.md).
The searches ran through Codex’s general web-search interface with its default locale
and ranking; the underlying engine, result ids, ranking snapshot, and query URLs were
not exposed or retained.
The strings can be rerun, but this record is not a repeatable search receipt and may
retrieve a different corpus.
It is not a systematic-review claim and does not prove that no unindexed paper exists.

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

The searches also returned the 2009 Friedman survey, Nagamochi’s 2005 general lower
bound, older optimality papers, and unrelated online, polygon, and circle-packing work.
Those results do not supply a new 2020--2026 finite-case theorem for the target list.

## Bounded conclusion

No additional 2020--2026 paper in this retrieved corpus establishes a finite-case
record, exact value, or target-specific bound for the prioritized cases.
The Arslanov family begins above this below-100 list, while the Bui and McClenagan
results are asymptotic rather than target-specific.
The recent finite-case changes remain first-party web evidence: catalogue entries and
SVGs, UnitSquare’s release, run-statistics artifacts, and the two proposed `n = 17`
weighted certificates.

This conclusion is deliberately narrower than “the literature is complete.”
Search index coverage, unpublished correspondence, and uncited papers remain possible
gaps. The run did not systematically cover non-English search terms, translated titles,
author-name variants, or every spelling and transliteration of the prioritized cases.
Repeat the audit if a live catalogue adds an author, DOI, theorem citation, or method
claim not present in the retained source record.

## Multilingual follow-up — 2026-09-01

A second bounded search used German, French, Russian, and Japanese phrases for packing
unit squares in a square, first with `17 18 19` and then with
`37 39 41 50 51 53 54 55 68 69`:

```text
"Einheitsquadrate" Quadrat Packung 17 18 19 2020 2026
"carrés unité" carré empaquetage 17 18 19 2020 2026
упаковка единичных квадратов в квадрат 17 18 19 2020 2026
正方形 単位正方形 パッキング 17 18 19 2020 2026
"Einheitsquadrate" Quadrat Packung 37 39 41 50 51 53 54 55 68 69
"carrés unité" carré empaquetage 37 39 41 50 51 53 54 55 68 69
упаковка единичных квадратов квадрат 37 39 41 50 51 53 54 55 68 69
単位正方形 正方形 パッキング 37 39 41 50 51 53 54 55 68 69
```

The relevant returns were mirrors or translations of sources already represented here: a
Japanese bibliographic record for McClenagan’s 2026 asymptotic preprint, a Chinese
repost of Massaccesi’s `n = 17` author post, and Russian secondary overview pages.
No new primary finite-case paper appeared.
The remaining results were unrelated uses of unit squares or numeric coincidence.
Mirrors and secondary pages were not archived because they add no claim or provenance
beyond the retained primaries.

This follow-up narrows one limitation of the first query pass but does not make the
audit systematic. Four language phrases, one search interface, index coverage, and the
absence of author-name transliteration sweeps still leave unsearched surfaces.

## Exact-number primary-source follow-up — 2026-09-01

A third pass forced the prioritized numbers into journal- and preprint-restricted
queries instead of relying on generic topic terms:

```text
site:arxiv.org square packing "unit squares" (17 OR 18 OR 19 OR 37 OR 39 OR 41) finite packing
site:arxiv.org square packing "unit squares" (50 OR 51 OR 53 OR 54 OR 55 OR 68 OR 69)
site:combinatorics.org "unit squares" packing square finite cases
"unit square packing" "68" "69" square record
```

No additional 2020--2026 primary finite-case paper appeared.
The relevant recent hit was again the Arslanov--Mustafin--Shangitbayev family, whose
below-100 consequences do not include the prioritized cases.
The other recent returns were Bui and McClenagan’s already-recorded asymptotic work or
papers about different packing problems.

The pass did recover useful historical mechanism context from the primary
[Friedman dynamic survey](https://www.combinatorics.org/files/Surveys/ds7/ds7v4-2005/ds7-2005.html):

- the `n = 18` construction supplies a component reused in the survey’s `n = 68`
  packing;
- the `n = 53` and `n = 68` records were reported as related constructions;
- the `n = 54` packing grew from the `n = 19` diagonal-strip mechanism, and `n = 69`
  from a width-four diagonal strip;
- the survey describes `n = 50` as an L-extension of `n = 37`; and
- its `n = 37`, `n = 41`, and `n = 55` discussion attributes the then-current
  improvements to diagonal-strip or case-specific constructions.

These are historical routing links, not evidence that the old numerical bounds remain
current. They strengthen the case for mechanism-linked controls—`18 -> 68`, `19 ->
54`, and `37 -> 50`—and for treating `68` and `69` as structured extensions rather than
arbitrary large targets.
They do not remove the present source-semantics and exact verification gates.

A formula-specific follow-up for the current `n = 54` side
`7 - sqrt(2)/2 + sqrt(1 + sqrt(2))` returned the existing catalogue and Friedman’s
historical account, but no primary derivation assigning all 54 exact poses.
The survey says Cantrell improved a construction based on an `n = 19` diagonal strip;
that is enough to motivate a source/formula audit, not enough to synthesize exact
coordinates from the retained decimals.
The registered H-055 source-cell and correspondence gates therefore remain necessary.

Agenda 014's later
[`BC-126` source/formula receipt](../n54-source-formula-audit-2026/README.md) inspected
the linked SVG source rather than only its rendered catalogue entry. That source does
carry exact defining equations, exact side and angle formulas, symbolic placement
expressions, and a generative half-turn layout. This narrows the absence above: there is
still no paper or 54-row labeled pose derivation, but the current construction is not
available only as unexplained decimals. The remaining gap is an exact source parser,
labeled correspondence, and independent geometry replay.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
