# `s(11)` Exact-Endpoint Literature Audit, 2026-09-06

This is a dated public-search receipt for the exact lower-bound endpoint

```text
38100*sqrt(8100042893309449)/899996306539
  = 3.8100257236147034071933954110...
```

It records a small fresh check made before the project's 2026-09-06 promotion. An
earlier pass on the coarser rational endpoint is retained below as provenance but is
superseded for the promoted value. This receipt does not validate the proof, exhaust the
literature, or prove priority. The broader
[`s(11)` lower-bound audit](../s11-lower-bound-literature-audit-2026/README.md) remains
the substantive source and method search.

## Conclusion

The refined decimal and radicand produced no results in arXiv, Crossref, OpenAlex, or
the general web queries recorded below. Crossref tokenized the radical expression and
topic query broadly. None of the first five results from either response stated the
refined endpoint. ArXiv, OpenAlex, and general web search returned no result for any of
the four refined queries.

This is zero relevant hits in the returned exact searches and inspected leading broad
matches. It is not an exhaustive priority result. In conjunction with the 2026-09-04
audit, it supports retaining **apparently novel** for the exact endpoint.

## Refined Queries and Inspected Results

The refined searches ran from 2026-09-06 10:36:07 through 10:37:33 UTC. Each public
route received these four strings:

```text
3.810025723614703
8100042893309449
38100 sqrt(8100042893309449) / 899996306539
s(11) 3.810025 square packing
```

The arXiv route used `all:<query>` and requested at most five results. Crossref used
`query.bibliographic=<query>` with `rows=5`. OpenAlex used
`filter=fulltext.search:<query>` with `per-page=5`. General web search used exact or
close quoted variants of each expression.

| Route | Decimal | Radicand | Radical expression | Topic query | What was inspected |
| --- | --- | --- | --- | --- | --- |
| [arXiv API](https://export.arxiv.org/api/query) | `totalResults = 0` | `totalResults = 0` | `totalResults = 0` | `totalResults = 0` | Feed metadata for all four responses |
| [Crossref REST API](https://api.crossref.org/works) | `total-results = 0` | `total-results = 0` | `total-results = 3,735` | `total-results = 6,018,792` | Response counts and the first five records from each broad response |
| [OpenAlex Works API](https://api.openalex.org/works) | `meta.count = 0` | `meta.count = 0` | `meta.count = 0` | `meta.count = 0` | Response metadata for all four queries |
| General web search | No returned result | No returned result | No returned result | No returned result | Every exposed result set |

Crossref's first five radical-expression matches were unrelated token matches. The
first five topic matches included the known square-packing paper at DOI
`10.37236/1701` and four unrelated or general packing records. None stated the refined
endpoint.

## Superseded Preliminary Queries

The preliminary searches ran from 2026-09-06 10:14 through 10:16 UTC against the
coarser rational endpoint. Each route received these three strings:

```text
3429000000000/899996306539
3.810015635715733
s(11) 3.81 square packing
```

The route parameters matched the refined pass above. The general web route searched the
fraction and decimal as exact quoted strings and the topic words as
`"s(11)" "3.81" "square packing"`.

| Route | Exact fraction | Exact decimal | Topic query | What was inspected |
| --- | --- | --- | --- | --- |
| [arXiv API](https://export.arxiv.org/api/query) | `totalResults = 0` | `totalResults = 0` | `totalResults = 0` | Feed metadata for all three responses |
| [Crossref REST API](https://api.crossref.org/works) | `total-results = 0` | `total-results = 0` | `total-results = 6,927,689` | Response count for each query and the first five topic-query records |
| [OpenAlex Works API](https://api.openalex.org/works) | `meta.count = 0` | `meta.count = 0` | `meta.count = 3,069` | Response count for each query and the first five topic-query records |
| General web search | No returned result | No returned result | Seven returned results, all irrelevant | Every exposed result title, domain, and snippet |

The Crossref topic-query records inspected were *Packing Equal Circles in a Square*,
*Packing Squares in a Square*, *Packing Rectangles into the Unit Square*, *Asymptotic
square packing problems*, and *Introduction and Problem History*. The matching DOI
metadata was, respectively, `10.1201/b10670-11`,
`10.1080/0025570x.2008.11953576`, `10.1023/a:1005263703808`,
`10.24124/2024/59553`, and `10.1007/978-0-387-45676-8_1`. None of the inspected
Crossref metadata states the searched `s(11)` lower endpoint.

The five OpenAlex topic-query titles inspected were unrelated to congruent-square
packing: *Banana-shaped electron acceptors with an electron-rich core fragment and 3D
packing capability*, *Optimizing Molecular Packing via Steric Hindrance for Reducing
Non-Radiative Recombination in Organic Solar Cells*, *Motility-Driven Glass and Jamming
Transitions in Biological Tissues*, *Self-assembled coordination cages based on
banana-shaped ligands*, and *The Crystal Structure of K2TeBr6*.

The seven general-web results came from EPA NEPIS, StudyLib, Dokumen.pub, and
Electronics Finder. Their snippets matched unrelated notation or dimensions. No result
addressed congruent-unit-square packing.

## Scope and repeatability

These are live index queries, not frozen response files. Search rankings, tokenization,
and index contents can change. The topic-query totals especially must not be read as
the number of relevant works: Crossref and OpenAlex matched common tokens separately,
and only the first five records from each were inspected.

The pass did not search subscription-only MathSciNet or zbMATH full text, theses,
non-English and unindexed sources, private correspondence, or unpublished work. It did
not repeat the prior audit's catalogue, author-page, reciprocal, density, or method
lineage searches. Those limits are why this receipt supports a scoped apparent-novelty
label rather than absolute priority.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
