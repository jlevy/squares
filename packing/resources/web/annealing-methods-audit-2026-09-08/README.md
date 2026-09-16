# Annealing and search-method source audit, 2026-09-08

This directory is the frozen discovery packet for
[the annealing research report](../../../../docs/project/research/research-2026-09-08-annealing-for-square-packing.md).
It retains the actual arXiv, Crossref and OpenAlex responses used to locate that
report's method sources, so a later agent can inspect the same corpus without repeating
the searches. It is a bounded query receipt, not a claim that every publication surface
was exhausted.

The report's argument is about *search methods* rather than about square packing
results, so the corpus it needs is the circle-, disk- and sphere-packing method
literature plus the experimental-annealing literature, none of which the earlier
square-packing refreshes were looking for. That is the gap this pass closes.

## Search receipts

Every query below was issued from this checkout with `curl` on 2026-09-08. Times are
UTC. `totalResults` is the count the index reported, not the number retained.

| Receipt | Retrieved | Result count | Query |
| --- | --- | ---: | --- |
| `arxiv-query-annealing-packing.xml` | 2026-09-08 16:41:12Z | 35 | `all:"simulated annealing" AND all:packing` |
| `arxiv-query-annealing-square-packing.xml` | 2026-09-08 16:41:17Z | 0 | `all:"simulated annealing" AND all:"square packing"` |
| `arxiv-query-replica-exchange-packing-fraction.xml` | 2026-09-08 16:41:21Z | 0 | `all:"replica exchange" AND all:"packing fraction"` |
| `arxiv-query-basin-hopping-packing.xml` | 2026-09-08 16:41:24Z | 7 | `all:"basin hopping" AND all:packing` |
| `arxiv-query-move-set-local-search-packing.xml` | 2026-09-08 16:41:27Z | 3 | `all:packing AND all:perturbation AND all:"local search"` |

Each arXiv feed was requested at
`https://export.arxiv.org/api/query?search_query=<query>&start=0&max_results=60&sortBy=submittedDate&sortOrder=descending`
and each retains its own query URL, retrieval timestamp and result count in its
`<opensearch:*>` and `<link rel="self">` elements.

The two index queries:

| Receipt | Retrieved | Request |
| --- | --- | --- |
| `crossref-query-replica-exchange-maximal-packing.json` | 2026-09-08 16:41:43Z | `https://api.crossref.org/works?query.bibliographic=replica+exchange+maximal+packing+fraction+hard+disks+circular+cavity&rows=20&select=DOI,title,author,container-title,issued,URL,link` |
| `crossref-query-cpc-out-of-equilibrium.json` | 2026-09-08 16:45:28Z | `https://api.crossref.org/works?query.bibliographic=out+of+equilibrium+replica+exchange+maximal+packing+hard+disks&filter=from-pub-date:2025-06-01,container-title:Computer+Physics+Communications&rows=10&select=DOI,title,container-title,issued,volume,page` |
| `openalex-query-annealing-packing-methods.json` | 2026-09-08 16:41:46Z | `https://api.openalex.org/works?search=simulated+annealing+packing+congruent+squares&per-page=50&filter=from_publication_date:2000-01-01` (236 matched, first 50 retained) |
| `openalex-work-basurto-2024.json` | 2026-09-08 16:39Z | `https://api.openalex.org/works/doi:10.1063/5.0219006` |
| `openalex-paywall-probe.json` | 2026-09-08 16:42:08Z | `https://api.openalex.org/works?filter=doi:<seven DOIs>&per-page=50&select=id,doi,title,publication_year,primary_location,open_access,best_oa_location,locations` |

The seven DOIs in the paywall probe are `10.1063/5.0219006`,
`10.1103/PhysRevE.79.021102`, `10.1039/c3cp44332a`, `10.1063/1.3244562`,
`10.1016/j.ejor.2004.09.008`, `10.1007/978-1-4613-0295-7_15` and
`10.1007/s00454-004-1129-z`. That query exists to record open-access status for the
sources the report cites but could not read, so the next agent inherits a checked
verdict rather than a guess.

| Receipt | SHA-256 |
| --- | --- |
| `arxiv-query-annealing-packing.xml` | `a58009f6bf33406450e0c8c1d6e1c32be6f4b98b56190cb065f542a3494b6c11` |
| `arxiv-query-annealing-square-packing.xml` | `25670f4e11a6b2ac8196dbafe2a7fc2050532352b0bf4364052102876764e5a4` |
| `arxiv-query-basin-hopping-packing.xml` | `7523062260ffd9b4472811f4036d069cd291900a44093d18b22cb0905bdb385a` |
| `arxiv-query-move-set-local-search-packing.xml` | `1d245aa838dd038224e1834500c30d0d18b8ea7867254b5574ae675faa2e4fec` |
| `arxiv-query-replica-exchange-packing-fraction.xml` | `3bb3e9760240b702d208d4e24096cb273f1e5049a55a06ff50f94b7a965cb006` |
| `crossref-query-cpc-out-of-equilibrium.json` | `6aac48dd41505b05f64f89beb61c830099e9e7eed148946fa434cddd99bf1812` |
| `crossref-query-replica-exchange-maximal-packing.json` | `3a3d7568711f470345e42039c6bcf52e68a13fe67b6a7ee9bf1cb9aa9fe49872` |
| `openalex-paywall-probe.json` | `367b5ebc2517281b7075c93422340a70c2bba08e997b7afc4743dd2cbf50308a` |
| `openalex-query-annealing-packing-methods.json` | `e13a49fa31e66603c384c79d93707d7ebaf1d932ef32b08f7fd1668f02d04e5a` |
| `openalex-work-basurto-2024.json` | `bd280537dd77e7c02a47c62195565153023d640b38295d4f74e77f1b2c34add8` |

## What the zero counts mean

Two feeds are empty, and both are worth keeping as negative receipts.

`all:"simulated annealing" AND all:"square packing"` returns **nothing on arXiv**. The
method literature for this exact problem does not live there; it lives in
[the Kingbird catalogue's](../kingbird-squares-in-squares.md) provenance comments,
[Ellsworth's run statistics](../kingbird-run-statistics-2026/README.md),
[Schadt's `n = 29` repository](../schadt-s29-2025/README.md) and
[Squarl's documentation](../squarl-n17-2026/README.md), all of which this archive
retains and none of which is an indexed publication. That is a fact about the subject,
not a failure of the query.

`all:"replica exchange" AND all:"packing fraction"` also returns nothing, and the reason
is the same in a different direction: the replica-exchange packing line publishes in the
Journal of Chemical Physics and Computer Physics Communications, not on arXiv. Crossref
found it immediately.

## Acquisition manifest

Fifteen papers were retained as PDF plus a faithful `pdftotext -layout` extraction, the
extraction method this archive already uses. None carries a cleaned transcription; they
are **raw-only** entries under
[the archive index's](../../README.md) stated convention. Paths are repository relative
and all live under `packing/resources/papers/`.

| Source | File stem | Acquisition URL | PDF SHA-256 | Raw SHA-256 |
| --- | --- | --- | --- | --- |
| Ye, Huang and Lü 2013 | `ye-huang-lu-2013-iterated-tabu-search-unequal-circles` | <https://arxiv.org/pdf/1306.0694v1> | `cc302b29d7d1513dee2cadedb73d3603268b057aab175b4d63393de509a6a8d6` | `61253de36a9809254c7606339ecf59a9b58bf9ca5ea4ed998ce4d2f452f23cfe` |
| Gensane 2004 | `gensane-2004-dense-packings-equal-spheres-cube` | <https://www.combinatorics.org/ojs/index.php/eljc/article/download/v11i1r33/pdf/> | `4ec149d41085845f4aca38f168b684d0d1a35dfb2e4819fada2c6c87e5c71a86` | `eb3facd28e3fa665a882042c4a17a7014e298235f3543ccae13655df466bd1ac` |
| Addis, Locatelli and Schoen 2008 | `addis-locatelli-schoen-2008-disk-packing-square` | <https://optimization-online.org/wp-content/uploads/2005/10/1229.pdf> | `1c8c2934aeb75776bd9a96685bb2fa5b006502738d69e8674e936d225774bf77` | `1d2eb7d777af1e057c17924c2e35d2ce3a0b7ae91f15d54ad1ad71c990687029` |
| Grosso, Jamali, Locatelli and Schoen 2010 | `grosso-jamali-locatelli-schoen-2010-packing-equal-unequal-circles` | <https://optimization-online.org/wp-content/uploads/2008/06/1999.pdf> | `1a63f3d1a4d411336684a8e29e4144b3fd1197a3e308e45fa659502a2cd424c9` | `cfcb05726065101ac40f741e89f5364ec6a7806f3cd59a4f168223a883651e75` |
| Lai, Hao, Xiao and Glover 2023 | `lai-hao-xiao-glover-2023-perturbation-thresholding-search` | <https://leria-info.univ-angers.fr/~jinkao.hao/papers/LaietalJOC2023.pdf> | `ce91a16950826e8f686e416fac3741ad84326640c0ce78fad3d737fbcab06519` | `bf0c2078a5bb32e56fd0ae41d611d71f1872404d180b51405cacd22e4869e14d` |
| Odriozola 2009 | `odriozola-2009-replica-exchange-hard-spheres` | <https://arxiv.org/pdf/1010.2923v1> | `562e22f02a408b6e408c21fa6588c577506ae03e566846c84ca43918450b524d` | `7581081a3ad322bc2cc8f36bd4b7d4920a4cd7eeedcc15a08e3b360ceecc4431` |
| Johnson et al. 1989, Part I | `johnson-aragon-mcgeoch-schevon-1989-annealing-part-i` | <https://faculty.washington.edu/aragon/pubs/annealing-pt1.pdf> | `0ddcc5db2474891b3374f5c413b473be98b22d7e0d7b15542db7e7fd81080898` | `5cce15dd1d60472b671b8e954646285a0193a0885ccd8e4091cdd53ed7d5d841` |
| Johnson et al. 1991, Part II | `johnson-aragon-mcgeoch-schevon-1991-annealing-part-ii` | <https://faculty.washington.edu/aragon/pubs/annealing-pt2.pdf> | `9cb38bbcaa0dd1c6d5ef1a67c0bf794a7889693e3b610ec5320a5727d4e8f3ba` | `c486e289aaa69279b6410687a21d10de27fbee3310f1ecc2644d242211db7938` |
| Blair, Santangelo and Machta 2012 | `blair-santangelo-machta-2012-packing-squares-in-a-torus` | <https://arxiv.org/pdf/1110.5348v2> | `e33da80a2428dfecbad2bfca9e62865cbd20edc22df67cfc81f332848619d935` | `20ab74762d5d8b30d0f5114e1ffb7db0bee40a1fb480a98c22d73e0a48f6d573` |
| Berthold et al. 2026, January | `berthold-kamp-mexi-pokutta-polik-2026-global-optimization-combinatorial-geometry` | <https://arxiv.org/pdf/2601.05943v1> | `60c4f3db2bcc742c9131fc3946095ce26ea1f26496c434665285134a85cf8be8` | `d96af043950f1db179f45f443bdec14922bd80c7a84973fd9325bc166d891a50` |
| Berthold et al. 2026, May | `berthold-kamp-mexi-pokutta-polik-2026-out-of-the-box-packing-problems` | <https://arxiv.org/pdf/2605.04850v1> | `c9be799bd98605287b909841dab1bf2e272923aba709851690246d3f7c6d4862` | `dd59769d1fbffa20ce39adbbe6a90bbb6ff3a0b5daeba826b0ff72c9116d6031` |
| Ninarello, Berthier and Coslovich 2017 | `ninarello-berthier-coslovich-2017-next-generation-glass-transition` | <https://arxiv.org/pdf/1704.08864v1> | `55a30ffaed6da8208f0ad266f919edd5437b8c1840f076bbd7fb73339cf9c40d` | `d52b67bd19ab17376eba034b6e935e519cc71d9bce50773faad5209d6d58b7b2` |
| Xu, Xiao and Amos 2008 | `xu-xiao-amos-2008-simulated-annealing-weighted-polygon-packing` | <https://arxiv.org/pdf/0809.5005v1> | `25b4abbe48fca9dc9364b541ad4a3f3d23682dee79137953650512b0526de9e5` | `9f28f6c43af4e65e7518e3cf23c0d7dc374f48018fa81f948f013006b1aa163e` |
| Anderson, Irrgang and Glotzer 2016 | `anderson-irrgang-glotzer-2016-scalable-metropolis-hard-shapes` | <https://arxiv.org/pdf/1509.04692v1> | `8fd96785e428472e59e23bf954084a15fa3d1e1cf6c1fbc5eecb26bd1b051f03` | `ef7790e482290afcc2a2bfe5af9f09f31946d6bbb0b691aa83fdb992c624a70d` |
| Gardeyn, Vanden Berghe and Wauters 2025 | `gardeyn-vandenberghe-wauters-2025-sparrow-2d-nesting` | <https://arxiv.org/pdf/2509.13329v1> | `ac6d0437f6ec4cfbbc3b8449f9259ba72e945d42c17cf2bffef91ef4f077004e` | `0f556f6456b1da6a8222c3e975677aaf4a6db8a73f7a5aa28781b38e56ce471d` |

The `anderson-irrgang-glotzer-2016` extraction printed
`Internal Error: xref num 271 not found but needed, try to reconstruct` and then
completed. The extraction is usable and the PDF is the retained ground truth, as it is
for every entry here.

One repository, not a paper, was retained in the same pass:
[`../squarl-n17-2026/`](../squarl-n17-2026/README.md), Sam Burns's open `n = 17`
pipeline, pinned at commit `016dff982938c69f0b7b2d63edd90d2e7e839dcc`. Its own README
carries the file list and hashes.

## Three claims checked against the retained bytes

The report's most load-bearing readings were verified against these files rather than
against abstracts.

- **Ye, Huang and Lü, Table 3.** Read on page 15 of the retained PDF. Against population
  basin hopping the row is better 27, equal 3, worse 0; against the contest record 25,
  4, 1; against simulated annealing (Müller, Schneider and Schömer) 20, 7, 3; against
  the best known at the time 14, 13, 3. The report's correction — that population basin
  hopping lost every non-tie while the annealer tied 7 and won 3 — is exactly this
  table.
- **Gensane's four procedures.** `Random Walking`, `Stochastic Billiard`, the
  simultaneous perturbation of all spheres, and `With Perturbations` appear as
  Algorithms 1 to 4 in the retained PDF, with the `ε/factor = 1e-12` ratio the report
  quotes. His own summary is in Section 1: contrary to the two-dimensional case, the
  billiard algorithm and probably the earlier ones cannot produce all optimal packings
  to good accuracy without perturbations.
- **Johnson et al., Part I.** Observations 4 and 5, the two negative results about
  adaptive and non-geometric cooling schedules, are in the retained Part I PDF; the
  91-versus-89-colour neighbourhood comparison is in Part II.

## Screened out, and why

The broad feeds returned a great deal that is not this problem. The dispositions:

| Source | Actual problem | Disposition |
| --- | --- | --- |
| `arXiv:1611.02323`, quasi-physical quasi-human packing of equal circles in a circle; `arXiv:1701.00541`, unequal circles in a square by narrow action spaces | Circle packing solvers from the same school as Ye, Huang and Lü | Query receipt only. Adjacent-problem method with no distinct claim the report rests on |
| `arXiv:2108.03203`, `arXiv:2001.07709`, circle *bin* packing | A different objective: many bins, not one minimal container | Query receipt only |
| `arXiv:2406.08430`, `arXiv:2309.12678`, `arXiv:2602.07913`, quantum and QUBO annealers | Discrete bin-packing and routing benchmarks | Query receipt only. Not continuous packing under free rotation |
| `arXiv:2602.10233`, ImprovEvolve: basin hopping meets LLM-guided evolutionary search | LLM-guided program search, not a packing method | Query receipt only |
| `arXiv:1701.00263`, population annealing of a binary hard-sphere mixture; `arXiv:1203.3373`, dense sphere packings in cylinders | Equilibrium statistical mechanics of spheres | Query receipt only. Sibling physics, but neither reports a record-setting packing search |
| Cluster and molecular-conformation hits across all feeds (`physics/0407106`, `chem-ph/9502007`, and others) | Lennard-Jones and metal-cluster global optimisation | Query receipt only. The funnelling-landscape idea the report borrows is cited through Addis et al., who state it for disks |
| `arXiv:2606.16333`, differentiable packing of irregular 3D objects | Gradient-based irregular 3D packing | Query receipt only |

Two feed hits were *not* screened out and are retained above: `arXiv:1110.5348` and
`arXiv:0809.5005` surfaced independently in the broad annealing feed, and
`arXiv:1306.0694` surfaced in the move-set feed. That the queries rediscovered three
sources the report had already cited is the only positive evidence here that the query
set overlaps the report's corpus at all.

## Attempted and not retrieved

Nothing below was faked, paraphrased into the archive, or reconstructed. Each was
attempted on 2026-09-08 and each failed for a stated reason.

| Source | Why the report needs it | Attempt and result |
| --- | --- | --- |
| Basurto, Gurin, Specht and Odriozola, *Searching for the maximal packing fraction of hard disks confined by a circular cavity through replica exchange / event-chain Monte Carlo*, J. Chem. Phys. 161(4):044110, 2024, [doi:10.1063/5.0219006](https://doi.org/10.1063/5.0219006) | The 108 new maximal disk packings, and the replica count, pressure ladder and cost per record the report says it does not have | OpenAlex reports `is_oa: true`, `oa_status: hybrid`, with the DOI itself as the only OA location and **no PDF URL**. Both `https://doi.org/10.1063/5.0219006` and the AIP article-PDF path returned **HTTP 403** to `curl`. No arXiv preprint: `au:Odriozola AND all:"circular cavity"` and `all:"replica exchange" AND all:"hard disks" AND all:"circular cavity"` both returned 0 |
| Basurto, Gurin, Varga and Odriozola, *Densest packings and accelerated equilibration of hard body systems via out-of-equilibrium replica exchange Monte Carlo method*, Comput. Phys. Commun. 320:109990, 2026 | The out-of-equilibrium successor and its `N <= 1000` records | Located by Crossref (`crossref-query-cpc-out-of-equilibrium.json`), which fixes the DOI as `10.1016/j.cpc.2025.109990`, volume 320, article 109990, issued 2026-03. OpenAlex reports `is_oa: false`, `oa_status: closed`, no repository full text. Elsevier; not retrieved |
| André Müller, Johannes J. Schneider and Elmar Schömer, *Packing a multidisperse system of hard disks in a circular environment*, Phys. Rev. E 79:021102, 2009 | The annealer whose results Ye, Huang and Lü's Table 3 compares against | `oa_status: closed` in the paywall probe. No arXiv preprint: `all:"multidisperse" AND all:"hard disks"` returned 0. Not retrieved. The report's use of it is confined to what Ye et al.'s retained table reports about it |
| Oakley, Johnston and Wales, *Symmetrisation schemes for global optimisation of atomic clusters*, Phys. Chem. Chem. Phys. 15(11):3965-3976, 2013, [doi:10.1039/c3cp44332a](https://doi.org/10.1039/c3cp44332a) | The two-orders-of-magnitude symmetrisation speedup | `oa_status: hybrid` with a direct RSC PDF URL in the probe, but `https://pubs.rsc.org/en/content/articlepdf/2013/cp/c3cp44332a` returned **HTTP 403**. Not retrieved |
| Gomes and Oliveira, *Solving irregular strip packing problems by hybridising simulated annealing and linear programming*, Eur. J. Oper. Res. 171(3):811-829, 2006, [doi:10.1016/j.ejor.2004.09.008](https://doi.org/10.1016/j.ejor.2004.09.008) | The annealing-plus-LP-compaction pairing and its 8.84% average improvement | `oa_status: closed`. Elsevier. Not retrieved; the report already lists it among the two sources it could not read directly |
| *Packing Equal Circles in a Square II* (TAMSASS-PECS), [doi:10.1007/978-1-4613-0295-7_15](https://doi.org/10.1007/978-1-4613-0295-7_15) | Threshold accepting's track record on the sibling problem | `oa_status: closed`. Springer book chapter. Not retrieved |
| Li and Milenkovic 1995; Milenkovic 1998 | The all-piece LP compaction and separation operators | Elsevier, both. Not attempted beyond the OA probe's scope; recorded here so the next pass does not rediscover the obstacle |

Gensane and Ryckelynck 2005 appears in the paywall probe with `oa_status: bronze` and a
working Springer `/content/pdf/` URL. That is not news: the archive
[has retained it since 2026-08-22](../../papers/gensane-ryckelynck-2005-improved-dense-packings.pdf),
and the probe is retained as a re-confirmation rather than as a new find. The report's
statement that it is paywalled describes the article landing page, and the archive's
"Not Retrievable" section already records the correction.

## What this pass did not cover

- **No search for square-packing *results*.** This pass looked for search *methods*.
  Currentness of the record tables and of the `n = 17` certificate line belongs to
  [`literature-refresh-2026-09-05`](../literature-refresh-2026-09-05/README.md) and the
  audits beside it, and none of those was re-run here.
- **No Google Scholar, Semantic Scholar, DBLP or publisher-site browsing.** Three
  indexes were queried. A method paper that is in none of them and not on an author's
  own page would not have been found.
- **No citation-chain expansion.** The papers citing Gensane and Ryckelynck, or citing
  Addis et al., were not enumerated. The report's own Limits section says no
  matched-budget head-to-head of annealing against basin hopping on a continuous packing
  problem was found; this pass did not close that, and a citation-chain pass is the
  obvious next attempt.
- **No replay of anything retained.** The fifteen PDFs are sources. Their numbers were
  read, not recomputed.
- **No coverage of the pre-2000 experimental-annealing literature** beyond Johnson et
  al., and no attempt at the physics literature on event-chain Monte Carlo, which the
  replica-exchange line depends on and which the report mentions only in passing.
