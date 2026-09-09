# Research Resources: Square Packing

This directory is a local, greppable archive of the primary literature behind
[research-2026-08-22-packing-11-unit-squares.md](../../docs/project/research/research-2026-08-22-packing-11-unit-squares.md).
It keeps the literature searchable without refetching, re-extracting, or fighting
paywalls and bot blocks.

## Layout

```
packing/resources/
├── papers/   Academic papers: original .pdf, cleaned .md, and faithful .raw.md
└── web/      Web sources: original .html and maintained .md capture
```

The archive’s normal form stores a paper three ways; the documented exceptions follow:

| File | What it is | Use it for |
| --- | --- | --- |
| `<name>.pdf` | The original, byte-for-byte as retrieved | Authority; figures; anything the text loses |
| `<name>.md` | Cleaned Markdown, headings and LaTeX restored | Reading and quoting |
| `<name>.raw.md` | Unedited extraction or OCR output | Check the clean copy against this; for image-only scans, the PDF remains the ground truth |

The `.raw.md` files are deliberately retained.
Cleanup was done by language models, so the raw extraction is the fallback whenever a
formula in a `.md` looks suspicious.

**Transcription status, stated exactly.** The archive normally stores an original
source, a cleaned `.md` transcription, and a faithful `.raw.md` extraction.
One hundred and nine entries currently fall short in ways worth naming rather than
hiding:

- `gensane-ryckelynck-2005-improved-dense-packings`,
  `nagamochi-2005-packing-unit-squares-in-a-rectangle`,
  `wang-dong-li-2016-new-result-packing-unit-squares` and
  `basic-slivkova-2018-optimal-piercing-square`,
  `alpert-bauer-kahle-macpherson-spendlove-2023-hard-squares-configuration-spaces`,
  `alvarado-garduno-gonzalez-2025-square-section-braid-groups`,
  `el-moumni-1999-optimal-packings-unit-squares`, and
  `trump-2023-packing-11-unit-squares`, plus `bal-2026-64-rectangle-wegner-lp-gaps`,
  `dewar-2024-contacts-oriented-squares`,
  `connelly-whiteley-1996-second-order-rigidity`,
  `donev-torquato-stillinger-connelly-2004-jamming-lp`,
  `donev-connelly-stillinger-torquato-2007-underconstrained-jammed-packings`, and
  `connelly-packings-of-circles-and-spheres-lecture-notes` are **raw-only**: PDF and
  faithful extraction, no cleaned transcription yet.
  All fourteen were read directly from the PDF, and the claims resting on them were
  checked there.
- The fifteen search-method sources retained on 2026-09-08 for
  [the annealing report](../../docs/project/research/research-2026-09-08-annealing-for-square-packing.md)
  are **raw-only** on the same terms:
  `ye-huang-lu-2013-iterated-tabu-search-unequal-circles`,
  `gensane-2004-dense-packings-equal-spheres-cube`,
  `addis-locatelli-schoen-2008-disk-packing-square`,
  `grosso-jamali-locatelli-schoen-2010-packing-equal-unequal-circles`,
  `lai-hao-xiao-glover-2023-perturbation-thresholding-search`,
  `odriozola-2009-replica-exchange-hard-spheres`,
  `johnson-aragon-mcgeoch-schevon-1989-annealing-part-i`,
  `johnson-aragon-mcgeoch-schevon-1991-annealing-part-ii`,
  `blair-santangelo-machta-2012-packing-squares-in-a-torus`,
  `berthold-kamp-mexi-pokutta-polik-2026-global-optimization-combinatorial-geometry`,
  `berthold-kamp-mexi-pokutta-polik-2026-out-of-the-box-packing-problems`,
  `ninarello-berthier-coslovich-2017-next-generation-glass-transition`,
  `xu-xiao-amos-2008-simulated-annealing-weighted-polygon-packing`,
  `anderson-irrgang-glotzer-2016-scalable-metropolis-hard-shapes`, and
  `gardeyn-vandenberghe-wauters-2025-sparrow-2d-nesting`. These are method sources
  rather than results about congruent squares, and a cleaned transcription would buy
  little: the report’s readings from them are specific numbered observations and tables.
  Three of those readings were checked against the retained bytes and the check is
  recorded in
  [the acquisition packet](web/annealing-methods-audit-2026-09-08/README.md); the rest
  are cited from abstracts, tables, or the report’s own reading, and the packet says
  which.
- The **seventy-two** simulation- and physics-method sources retained on 2026-09-09 for
  [the simulation mechanisms report](../../docs/project/research/research-2026-09-09-simulation-mechanisms-for-packing.md)
  are **raw-only** on the same terms, and are listed in
  [their own table](#simulation-and-physics-method-sources) below.
  Like the 2026-09-08 batch these are method sources rather than results about congruent
  squares, and a cleaned transcription would buy little: the report’s readings from them
  are specific numbered parameters, quoted sentences and tables.
  Eight of those readings were checked against the retained bytes and the check is
  recorded in
  [the acquisition packet](web/simulation-methods-audit-2026-09-09/README.md), which
  also names every source the pass could not obtain and says what the report does and
  does not claim from it.
  One of the seventy-two, `more-wu-1997-global-continuation-distance-geometry`, is an
  **image-only raster scan**: its faithful extraction is 28 bytes of form feeds and
  `pdftotext` reported no warning at all, so an `.ocr.md` sidecar is retained beside it
  on the same terms as the Stromquist memoranda, and the formulas the report quotes were
  read off rendered page images rather than off the OCR.
- `gobel-1979-geometrical-packing-and-covering-problems` is **PDF-only**: the source is
  retained, but neither a cleaned transcription nor a faithful extraction has been
  produced. Claims resting on it must be checked against the page images.
- `roth-vaughan-1978-inefficiency-packing-squares` carries a **partial** cleaned
  transcription: abstract, introduction and Theorem, read from the rendered page image
  and reproduced verbatim; Sections 2–7 are not transcribed.
  The 1978 scan’s OCR loses subscripts, superscripts and interval notation, and
  transcribing it would mean reconstructing mathematics rather than reformatting it.
  The file opens with a banner saying so.
- The three `stromquist-1984-packing-unit-squares-inside-squares-*` memoranda are
  **image-only scans with concise reading aids**, not cleaned transcriptions.
  Their `.raw.md` files are unedited page-ordered Tesseract OCR for search, not source
  ground truth; formulas and figures must be checked against the PDFs.
- The three [MacIver 2026 manuscripts](web/maciver-square-packing-2026-09-07/README.md)
  have original PDFs, faithful `pdftotext -layout` extractions, and one shared reading
  aid. They have no cleaned transcriptions.
  The packet records their source claims, incomplete local verification, and the missing
  computational artifacts for the seventeen-square proof.

Writing the missing transcriptions is deferred deliberately rather than done hastily—
model-assisted cleanup is exactly what produced the reconstruction hazards tabulated in
the next section, and Roth–Vaughan is the argument for that caution: two independent
secondary sources reported a constant the paper does not contain.

## Reconstructed Passages: Read This Before Quoting a Formula

Cleanup was model-assisted, and on badly-extracted PDFs the models sometimes
**reconstructed** damaged mathematics rather than only reformatting it.
Every such passage is annotated inline with `GARBLED` or `NOTE`, and any file containing
them opens with a ⚠️ banner giving the count.

| File stem | Annotated | Notes |
| --- | --- | --- |
| `stromquist-2003-packing-10-or-11-unit-squares` | 3 | Figure 13’s four defining coordinates were interleaved by the raw multi-column extraction and then reconstructed incorrectly. The lists are now read directly from rendered PDF page 9. A second annotation preserves but corrects the paper’s own extraneous-root error in the middle Lemma 4 table. A third gives an explicit box escaping the printed Figure 14 set and distinguishes that proof gap from the separately proposed one-coordinate repair. |
| `erdos-graham-1975-on-packing-squares-with-equal-squares` | 17 | **Heavily damaged** 1975 typescript scan. The central theorem was *not extracted at all*—raw shows only `Theorem.` then `(1)`—and the transcription supplies the known `w(α) = Θ(α^{7/11})` as a flagged reconstruction. A reading aid, not a source. |
| `compound-perfect-squared-squares-1303.0599` | 10 | Ten passages, nearly all **tables and matrices** scrambled by multi-column extraction. Do not cite its tables. |
| `bentz-2016-optimal-packings-22-and-33` | 3 | Probable “Stromberg” → “Stromquist” correction and a reconstructed distance bound in Lemma 7. |
| `friedman-ds7-packing-unit-squares-in-squares` | 3 | **The “Optimal?” column of Table 1 was INFERRED, not read**—the column exists in the original but its per-row values were lost, and the transcriber deduced them from the survey’s own theorems. Both appendix tables (53 and 29 rows) were likewise reassembled from interleaved extractions. The survey predates later results, so a blank means “not proved as of that revision”. **The research doc’s proof-status claims do not rest on this file**—they use Kingbird’s explicit “Proved by” attributions and the individual papers. |
| `square-packing-x06-wasted-area-2508.04603` | 6 | Three cells of the Section 5 comparison table; two Section 5 repairs (the omitted $\nu$ condition in Proposition 7 and the lost division bar in the reduction waste term); and the omitted upper bound on Section 3.1’s replacement index. Do not cite that table. |
| `arslanov-improved-packings-n-n-1` | 1 | One orientation-constraint formula unrecoverable; its numeric value is preserved. |
| `bentz-2010-optimal-packings-13-and-46` | 1 | Corollary 7: segments reconstructed **and an inequality direction changed** (`2√2−2 > b` in raw vs `b > 2√2−2` here). Direction UNVERIFIED. The leading claim—intersection length ≥ `2√2−2 ≈ 0.828`—is unambiguous in the raw and unaffected. |
| `kearney-shiu-2002-efficient-packing-unit-squares` | 1 | One chain of inequalities in Theorem 2’s proof not reconstructed; the conclusion is stated. |
| `mcclenagan-2026-optimally-packing-large-square` | 2 | One exponent `(3−√3)/2` reconstructed from fragments, flagged as possibly wrong; plus a source-level contradictory chain in Section 3. H-037 gives an independent local repair of the chain; it does not certify the full theorem. |

Files not listed carry no annotations.
Resolving `(cid:NN)` ligature artifacts, running headers, and page numbers is ordinary
cleanup, not reconstruction, and is not flagged.

**The rule:** if a formula sits near an annotation, check it against the `.raw.md`
before relying on it.
The research document cites only claims that are unambiguous in the raw extractions.

## Why This Archive Is Not Auto-Formatted

The repository auto-formats maintained Markdown with Flowmark on commit.
The paper and web archives are excluded for two independent reasons.
First, `.raw.md` files are byte-level ground truth, so reflowing them would void the
comparison with the model-assisted transcriptions.
Second, the cleaned `.md` files are archival transcriptions: formatting would retype
source characters such as straight quotes and ellipses merely to make them look tidy.

Inline mathematics is no longer the reason for the exclusion.
The pinned `flowmark-rs==0.4.0` keeps every `$...$` span whole, and
`devtools.check_math_spans` remeasures that property on copies.
The archive remains excluded because source and transcription fidelity still require it.

The same byte-level rule applies to whitespace.
Some faithful `pdfminer` output contains spaces on blank lines, so the root
`.gitattributes` disables Git whitespace diagnostics only for `resources/**/*.raw.md`.
Hand-written Markdown keeps the normal check; raw extraction bytes are never normalized
to satisfy a presentation rule.

`packing/resources/README.md` is formatted normally.

## Searching

Paths below are written from the repository root.

```bash
# Find every mention of a bound across the whole archive
grep -rn "unavoidable" packing/resources/ --include=*.md

# Search only cleaned papers, not raw extractions or HTML
grep -rn "3.877" packing/resources/papers/*.md

# Check a formula in a cleaned paper against the raw extraction
grep -n "sqrt" packing/resources/papers/stromquist-2003-*.raw.md
```

## Papers

Citation keys match those used in the research document.
This table holds sources about packing congruent squares.
Two further tables below hold method analogues from adjacent problems:
[rigidity and verification](#rigidity-and-verification-method-sources), and
[search and annealing](#search-and-annealing-method-sources).

| Key | Title | Authors | Year | Venue | File stem |
| --- | --- | --- | --- | --- | --- |
| **[Stromquist Memo I]** | Packing Unit Squares Inside Squares, I (Six Unit Squares) | W. Stromquist | 1984 | Daniel H. Wagner, Associates internal memorandum, September 11 | `stromquist-1984-packing-unit-squares-inside-squares-i-six-unit-squares` |
| **[Stromquist Memo II]** | Packing Unit Squares Inside Squares, II (Ten Unit Squares) | W. Stromquist | 1984 | Daniel H. Wagner, Associates internal memorandum, October 15 | `stromquist-1984-packing-unit-squares-inside-squares-ii-ten-unit-squares` |
| **[Stromquist Memo III]** | Packing Unit Squares Inside Squares, III (Cases with n ≤ 65 and Martin Gardner’s Conjecture for n = 11) | W. Stromquist | 1984 | Daniel H. Wagner, Associates internal memorandum, November 15 | `stromquist-1984-packing-unit-squares-inside-squares-iii-cases-through-65-and-gardner-conjecture` |
| **[Stromquist 2003]** | Packing 10 or 11 Unit Squares in a Square | W. Stromquist | 2003 | Electron. J. Combin. 10, #R8 | `stromquist-2003-packing-10-or-11-unit-squares` |
| **[Friedman DS7]** | Packing Unit Squares in Squares: A Survey and New Results | E. Friedman | 1998– | Electron. J. Combin., Dynamic Survey DS7 | `friedman-ds7-packing-unit-squares-in-squares` |
| **[Kearney–Shiu 2002]** | Efficient packing of unit squares in a square | M. J. Kearney, P. Shiu | 2002 | Electron. J. Combin. 9, #R14 | `kearney-shiu-2002-efficient-packing-unit-squares` |
| **[Göbel 1979]** | Geometrical Packing and Covering Problems | F. Göbel | 1979 | *Packing and Covering in Combinatorics*, Math. Centre Tracts 106, 179–199 | `gobel-1979-geometrical-packing-and-covering-problems` |
| **[Bentz 2010]** | Optimal Packings of 13 and 46 Unit Squares in a Square | W. Bentz | 2010 | Electron. J. Combin. 17, #R126 | `bentz-2010-optimal-packings-13-and-46` |
| **[Bentz 2016]** | Optimal Packings of 22 and 33 Unit Squares in a Square | W. Bentz | 2016 | arXiv:1606.03746 | `bentz-2016-optimal-packings-22-and-33` |
| **[Erdős–Graham 1975]** | On packing squares with equal squares | P. Erdős, R. L. Graham | 1975 | JCTA 19, 119–123 (Stanford CS-TR-75-483) | `erdos-graham-1975-on-packing-squares-with-equal-squares` |
| **[Caoduro–Sebő]** | Packing, Hitting, and Colouring Squares | M. Caoduro, A. Sebő | 2022/24 | arXiv:2206.02185 | `caoduro-sebo-packing-hitting-colouring-squares` |
| **[Wegner-CE 2026]** | Counterexamples to Wegner’s Conjecture for Rectangles | see file | 2026 | arXiv:2606.17854 | `wegner-counterexamples-rectangles` |
| **[Martin 2000]** | Compactness Theorems for Geometric Packings | G. Martin | 2000 | arXiv:math/0005054 | `martin-2000-compactness-theorems-geometric-packings` |
| **[McClenagan 2026]** | Optimally Packing a Large Square by Unit Squares | R. McClenagan | 2026 | arXiv:2602.01484 | `mcclenagan-2026-optimally-packing-large-square` |
| **[Good-Squares 2025]** | Square Packing with Asymptotically Smallest Waste Only Needs Good Squares | see file | 2025 | arXiv:2504.09489 | `square-packing-good-squares-2504.09489` |
| **[Waste-0.6 2025]** | Square packing with O(x^0.6) wasted area | see file | 2025 | arXiv:2508.04603 | `square-packing-x06-wasted-area-2508.04603` |
| **[Arslanov et al.]** | Improved packings of n(n−1) unit squares in a square | M. Z. Arslanov et al. | 2021 | Electron. J. Combin. 28(4) | `arslanov-improved-packings-n-n-1` |
| **[CPSS 2013]** | Compound Perfect Squared Squares of the Order Twenties | see file | 2013 | arXiv:1303.0599 | `compound-perfect-squared-squares-1303.0599` |
| **[Gensane–Ryckelynck 2005]** | Improved Dense Packings of Congruent Squares in a Square | T. Gensane, P. Ryckelynck | 2005 | Discrete Comput. Geom. 34, 97–109 | `gensane-ryckelynck-2005-improved-dense-packings` |
| **[Nagamochi 2005]** | Packing Unit Squares in a Rectangle | H. Nagamochi | 2005 | Electron. J. Combin. 12, #R37 | `nagamochi-2005-packing-unit-squares-in-a-rectangle` |
| **[Wang–Dong–Li 2016]** | A New Result on Packing Unit Squares into a Large Square | S. Wang, T. Dong, J. Li | 2016 | arXiv:1603.02368 | `wang-dong-li-2016-new-result-packing-unit-squares` |
| **[Basic-Slivkova 2018]** | On optimal piercing of a square | B. Bašić, A. Slivková | 2018 | Discrete Applied Mathematics 247 | `basic-slivkova-2018-optimal-piercing-square` |
| **[Alpert et al. 2023]** | Homology of configuration spaces of hard squares in a rectangle | H. Alpert, U. Bauer, M. Kahle, R. MacPherson, K. Spendlove | 2023 | Algebraic & Geometric Topology 23, 2593–2626; arXiv:2010.14480 | `alpert-bauer-kahle-macpherson-spendlove-2023-hard-squares-configuration-spaces` |
| **[Alvarado-Garduño–González 2025]** | Square-section braid groups and Higman–Neumann–Neumann extensions | O. Alvarado-Garduño, J. González | 2025 | arXiv:2510.17707 | `alvarado-garduno-gonzalez-2025-square-section-braid-groups` |
| **[Roth–Vaughan 1978]** | Inefficiency in Packing Squares with Unit Squares | K. F. Roth, R. C. Vaughan | 1978 | JCTA 24, 170–186 | `roth-vaughan-1978-inefficiency-packing-squares` |
| **[El Moumni 1999]** | Optimal Packings of Unit Squares in a Square | S. El Moumni | 1999 | Studia Sci. Math. Hungar. 35, 281–290 | `el-moumni-1999-optimal-packings-unit-squares` |
| **[Trump 2023]** | Packing of 11 unit squares in a square with minimum size | W. Trump | 2023 | Author preprint | `trump-2023-packing-11-unit-squares` |
| **[Bal 2026]** | A 64-Rectangle Counterexample to Wegner’s Conjecture and LP Gaps up to 5/2 | A. K. Bal | 2026 | arXiv:2607.11318v2 | `bal-2026-64-rectangle-wegner-lp-gaps` |
| **[Dewar 2024]** | How many contacts can exist between oriented squares of various sizes? | S. Dewar | 2024 | Discrete Math. 347(4), 113879; arXiv:2210.10422v2 | `dewar-2024-contacts-oriented-squares` |

## Contributed Research Packets

The owner-supplied
[complete n=11 research bundle](papers/n11-complete-research-bundle-2026-09-07/INTAKE.md)
was received on 2026-09-07 UTC; its complete 57-file distribution remains in the local
`attic/`. The tracked archive retains its research reports, source snapshot, figures,
checkers, replay outputs and delivered PDFs.
PDF publishing helpers and original distribution-integrity files stay in the attic.
The intake note records this selection, the adapted packaging documentation and the
scope of the replayed controls.
This is a contributed analysis packet; its proposals and supplied checks are not
automatically accepted campaign results.

[X-017](../campaign/explorations/X-017-compatibility-and-complete-case-covers.md) owns
the critical adaptation and complete source-to-record map.
[Agenda 027](../campaign/agendas/agenda-027-compatibility-and-restricted-families.md)
organizes the proposed work as a separate agenda.

## Rigidity and Verification Method Sources

These papers and notes support the local-rigidity and certified-search program.
They are method analogues, not direct theorems about the global optimum for eleven
congruent squares. In particular, smooth-particle or tensegrity results require their
hypotheses to be matched to the square pose chart and its nonsmooth feature changes.

| Key | Title | Authors | Year | Venue | File stem |
| --- | --- | --- | --- | --- | --- |
| **[Connelly–Whiteley 1996]** | Second-Order Rigidity and Prestress Stability for Tensegrity Frameworks | R. Connelly, W. Whiteley | 1996 | SIAM J. Discrete Math. 9(3), 453–491 | `connelly-whiteley-1996-second-order-rigidity` |
| **[Donev et al. 2004]** | A Linear Programming Algorithm to Test for Jamming in Hard-Sphere Packings | A. Donev, S. Torquato, F. H. Stillinger, R. Connelly | 2004 | J. Comput. Phys. 197, 139–166 | `donev-torquato-stillinger-connelly-2004-jamming-lp` |
| **[Donev et al. 2007]** | Underconstrained Jammed Packings of Nonspherical Hard Particles: Ellipses and Ellipsoids | A. Donev, R. Connelly, F. H. Stillinger, S. Torquato | 2007 | Phys. Rev. E 75, 051304 | `donev-connelly-stillinger-torquato-2007-underconstrained-jammed-packings` |
| **[Connelly notes]** | Packings of Circles and Spheres, Lectures III and IV | R. Connelly | undated | Institut Henri Poincaré lecture slides | `connelly-packings-of-circles-and-spheres-lecture-notes` |

## Search and Annealing Method Sources

Retained on 2026-09-08 for
[Annealing for Square Packing](../../docs/project/research/research-2026-09-08-annealing-for-square-packing.md).
Only two of them are about squares at all, and neither sets a record for `s(n)`. They
are here because the report’s argument is about **search methods**, and the methods that
set packing records were developed on circles, disks and spheres, or measured on graph
problems. Every entry is raw-only.
The retrieval receipts, the checked readings, and the sources that could not be
retrieved are in
[`web/annealing-methods-audit-2026-09-08`](web/annealing-methods-audit-2026-09-08/README.md).

| Key | Title | Authors | Year | Venue | File stem |
| --- | --- | --- | --- | --- | --- |
| **[Gensane 2004]** | Dense Packings of Equal Spheres in a Cube | T. Gensane | 2004 | Electron. J. Combin. 11, #R33 | `gensane-2004-dense-packings-equal-spheres-cube` |
| **[Addis–Locatelli–Schoen 2008]** | Disk Packing in a Square: A New Global Optimization Approach | B. Addis, M. Locatelli, F. Schoen | 2008 | INFORMS J. Comput. 20(4), 516–524 (preprint) | `addis-locatelli-schoen-2008-disk-packing-square` |
| **[Grosso et al. 2010]** | Solving the problem of packing equal and unequal circles in a circular container | A. Grosso, A. R. M. J. U. Jamali, M. Locatelli, F. Schoen | 2010 | J. Global Optim. 47, 63–81 (preprint) | `grosso-jamali-locatelli-schoen-2010-packing-equal-unequal-circles` |
| **[Ye–Huang–Lü 2013]** | Iterated Tabu Search Algorithm for Packing Unequal Circles in a Circle | F. Ye, W. Huang, Z. Lü | 2013 | arXiv:1306.0694 | `ye-huang-lu-2013-iterated-tabu-search-unequal-circles` |
| **[Lai et al. 2023]** | Perturbation-based thresholding search for packing equal circles and spheres | X. Lai, J.-K. Hao, R. Xiao, F. Glover | 2023 | INFORMS J. Comput. (accepted manuscript) | `lai-hao-xiao-glover-2023-perturbation-thresholding-search` |
| **[Odriozola 2009]** | Replica Exchange Monte Carlo applied to Hard Spheres | G. Odriozola | 2009 | J. Chem. Phys. 131, 144107; arXiv:1010.2923 | `odriozola-2009-replica-exchange-hard-spheres` |
| **[Johnson et al. Part I]** | Optimization by Simulated Annealing: An Experimental Evaluation; Part I, Graph Partitioning | D. S. Johnson, C. R. Aragon, L. A. McGeoch, C. Schevon | 1989 | Oper. Res. 37(6), 865–892 | `johnson-aragon-mcgeoch-schevon-1989-annealing-part-i` |
| **[Johnson et al. Part II]** | Optimization by Simulated Annealing: An Experimental Evaluation; Part II, Graph Coloring and Number Partitioning | D. S. Johnson, C. R. Aragon, L. A. McGeoch, C. Schevon | 1991 | Oper. Res. 39(3), 378–406 | `johnson-aragon-mcgeoch-schevon-1991-annealing-part-ii` |
| **[Blair et al. 2012]** | Packing Squares in a Torus | D. W. Blair, C. Santangelo, J. Machta | 2012 | arXiv:1110.5348; J. Stat. Mech. | `blair-santangelo-machta-2012-packing-squares-in-a-torus` |
| **[Xu–Xiao–Amos 2008]** | Simulated Annealing for Weighted Polygon Packing | Y.-C. Xu, R.-B. Xiao, M. Amos | 2008 | arXiv:0809.5005 | `xu-xiao-amos-2008-simulated-annealing-weighted-polygon-packing` |
| **[Anderson et al. 2016]** | Scalable Metropolis Monte Carlo for simulation of hard shapes (HOOMD-blue HPMC) | J. A. Anderson, M. E. Irrgang, S. C. Glotzer | 2016 | Comput. Phys. Commun. 204, 21–30; arXiv:1509.04692 | `anderson-irrgang-glotzer-2016-scalable-metropolis-hard-shapes` |
| **[Ninarello et al. 2017]** | Models and algorithms for the next generation of glass transition studies | A. Ninarello, L. Berthier, D. Coslovich | 2017 | Phys. Rev. X 7, 021039; arXiv:1704.08864 | `ninarello-berthier-coslovich-2017-next-generation-glass-transition` |
| **[Berthold et al. 2026a]** | Global Optimization for Combinatorial Geometry Problems Revisited in the Era of LLMs | T. Berthold, D. Kamp, G. Mexi, S. Pokutta, I. Pólik | 2026 | arXiv:2601.05943 | `berthold-kamp-mexi-pokutta-polik-2026-global-optimization-combinatorial-geometry` |
| **[Berthold et al. 2026b]** | Out-of-the-Box Global Optimization for Packing Problems: New Models and Improved Solutions | T. Berthold, D. Kamp, G. Mexi, S. Pokutta, I. Pólik | 2026 | arXiv:2605.04850 | `berthold-kamp-mexi-pokutta-polik-2026-out-of-the-box-packing-problems` |
| **[Sparrow 2025]** | An open-source heuristic to reboot 2D nesting research | J. Gardeyn, G. Vanden Berghe, T. Wauters | 2025 | arXiv:2509.13329 | `gardeyn-vandenberghe-wauters-2025-sparrow-2d-nesting` |

## Simulation and Physics Method Sources

Retained on 2026-09-09 for
[Physics and Simulation Mechanisms for Square Packing](../../docs/project/research/research-2026-09-09-simulation-mechanisms-for-packing.md).
None of them is about congruent squares in a square, and none sets a record for `s(n)`.
They are here because that report’s argument is about **mechanisms that move bodies
under a simulated physical or geometric rule**, and those mechanisms were developed on
disks, spheres, ellipses, polyhedra and, in the graphics half, on nothing in particular.
Every entry is raw-only, with the one image-only exception named above.
The acquisition URLs, retrieval timestamps, per-file SHA-256 hashes, the eight readings
checked against the retained bytes, the screened-out material, and every source that
could not be retrieved are in
[`web/simulation-methods-audit-2026-09-09`](web/simulation-methods-audit-2026-09-09/README.md).

### Inflation, event-driven dynamics and billiards

| Source | File stem |
| --- | --- |
| Lubachevsky, *How to Simulate Billiards and Similar Systems*, J. Comput. Phys. 94, 1991 | `lubachevsky-1991-how-to-simulate-billiards` |
| Donev, Torquato & Stillinger, *Neighbor list collision-driven molecular dynamics for nonspherical hard particles*, 2005 | `donev-torquato-stillinger-2005-neighbor-list-collision-driven-nonspherical` |
| Skoge, Donev, Stillinger & Torquato, *Packing hyperspheres in high-dimensional Euclidean spaces*, 2006 | `skoge-donev-stillinger-torquato-2006-packing-hyperspheres-high-dimensional-euclidean-spaces` |
| Torquato & Stillinger, *Jammed hard-particle packings: from Kepler to Bernal and beyond*, Rev. Mod. Phys. 82, 2010 | `torquato-stillinger-2010-jammed-hard-particle-packings-kepler-bernal` |
| Jiao, Stillinger & Torquato, *Optimal packings of superdisks*, 2008 | `jiao-stillinger-torquato-2008-dense-packings-superdisks` |
| Jiao, Stillinger & Torquato, *Maximally random jammed packings of superballs*, 2010 | `jiao-stillinger-torquato-2010-mrj-packings-superballs` |
| Klement, Lee, Anderson & Engel, *Newtonian event-chain Monte Carlo and collision prediction with polyhedral particles*, 2021 | `klement-engel-2021-newtonian-event-chain-monte-carlo-collision-prediction-polyhedra` |
| Hoover, Hoover & Bannerman, *Single-speed molecular dynamics of hard parallel squares and cubes*, 2009 | `hoover-hoover-bannerman-2009-single-speed-md-hard-parallel-squares-cubes` |
| Hoy, *Ultradense jammed ellipse packings via biased SWAP*, 2024 | `hoy-2024-ultradense-jammed-ellipse-packings-biased-swap` |
| Bannerman, Sargant & Lue, *DynamO: a free O(N) general event-driven molecular dynamics simulator*, 2011 | `bannerman-sargant-lue-2011-dynamo-free-event-driven-md-simulator` |
| Boll, Donovan, Graham & Lubachevsky, *Improving dense packings of equal disks in a square*, 2000 | `boll-donovan-graham-lubachevsky-2000-improving-dense-packings-disks-square` |
| Graham & Lubachevsky, *Repeated patterns of dense packings of equal disks in a square*, 1996 | `graham-lubachevsky-1996-repeated-patterns-dense-packings-disks-square` |
| Graham & Lubachevsky, *Dense packings of equal disks in an equilateral triangle*, 1995 | `graham-lubachevsky-1995-dense-packings-disks-equilateral-triangle` |
| Lubachevsky & Graham, *Curved hexagonal packings of equal disks in a circle*, 1997 | `lubachevsky-graham-1997-curved-hexagonal-packings-disks-circle` |

### Adaptive shrinking cell, and contact dynamics

| Source | File stem |
| --- | --- |
| Torquato & Jiao, *Dense packings of the Platonic and Archimedean solids*, Nature 460, 2009 | `torquato-jiao-2009-dense-packings-platonic-archimedean-solids` |
| Torquato & Jiao, *Dense packings of polyhedra: Platonic and Archimedean solids*, Phys. Rev. E 80, 2009 | `torquato-jiao-2009-dense-packings-polyhedra-platonic-archimedean` |
| Torquato & Jiao, *Robust algorithm to generate a diverse class of dense sphere packings via linear programming*, Phys. Rev. E 82, 2010 | `torquato-jiao-2010-robust-algorithm-sphere-packings-linear-programming` |
| Jiao, Stillinger & Torquato, *Optimal packings of superballs*, 2009 | `jiao-stillinger-torquato-2009-optimal-packings-superballs` |
| Atkinson, Jiao & Torquato, *Maximally dense packings of two-dimensional convex and concave noncircular particles*, 2012 | `atkinson-jiao-torquato-2012-maximally-dense-packings-2d-noncircular` |
| Maher, Stillinger & Torquato, *Kinetic frustration effects on dense two-dimensional packings of convex particles*, 2021 | `maher-stillinger-torquato-2021-kinetic-frustration-2d-convex-packings` |
| Fu, Steinhardt, Zhao, Socolar & Charbonneau, *Hard sphere packings within cylinders*, 2016 | `fu-steinhardt-zhao-socolar-charbonneau-2016-hard-sphere-packings-within-cylinders` |
| Fayen, Jagannathan & Foffi, *Infinite-pressure phase diagram of binary mixtures of hard disks*, 2020 | `fayen-jagannathan-foffi-2020-infinite-pressure-phase-diagram-binary-hard-disks` |
| Unger & Kertesz, *The contact dynamics method for granular media*, 2003 | `unger-kertesz-2003-contact-dynamics-method-granular-media` |
| Unger, Kertesz & Wolf, *Force indeterminacy in the jammed state of hard disks*, 2005 | `unger-kertesz-wolf-2005-force-indeterminacy-jammed-hard-disks` |
| Dubois, Acary & Jean, *The Contact Dynamics method: a nonsmooth story*, C. R. Mecanique 346, 2018 | `dubois-acary-jean-2018-contact-dynamics-method-nonsmooth-story` |
| Shaebani, Unger & Kertesz, *Generation of homogeneous granular packings: contact dynamics at constant pressure*, 2008 | `shaebani-unger-kertesz-2008-homogeneous-granular-packings-contact-dynamics-pressure-bath` |
| Shojaaee, Shaebani, Brendel, Torok & Wolf, *Parallel contact dynamics by adaptive hierarchical domain decomposition*, 2012 | `shojaaee-shaebani-brendel-torok-wolf-2012-parallel-contact-dynamics-domain-decomposition` |
| Olsen & Kamrin, *Resolving force indeterminacy in contact dynamics using compatibility conditions*, 2018 | `olsen-kamrin-2018-force-indeterminacy-contact-dynamics` |
| Preclik & Rude, *Ultrascale simulations of non-smooth granular dynamics*, 2015 | `preclik-rude-2015-ultrascale-simulations-nonsmooth-granular-dynamics` |
| Mazhar, Heyn & Pazouki et al., *Chrono: a parallel multi-physics library*, 2013 | `mazhar-heyn-pazouki-2013-chrono-parallel-multiphysics-library` |
| Azema, Estrada & Radjai, *Particle shape dependence in 2D granular media*, 2012 | `azema-estrada-radjai-2012-particle-shape-dependence-2d-granular` |
| Azema, Radjai & Saussine, *Quasistatic rheology of irregular polyhedral particles*, 2009 | `azema-radjai-saussine-2009-quasistatic-rheology-irregular-polyhedral-particles` |

### Constraint projection, position-based dynamics and differentiable simulation

| Source | File stem |
| --- | --- |
| Gravel & Elser, *Divide and concur: a general approach to constraint satisfaction*, Phys. Rev. E 78, 2008 | `gravel-elser-2008-divide-and-concur` |
| Kallus, Elser & Gravel, *A method for dense packing discovery*, 2010 | `kallus-elser-gravel-2010-method-dense-packing-discovery` |
| Kallus, Elser & Gravel, *Dense periodic packings of tetrahedra with small repeating units*, 2010 | `kallus-elser-gravel-2010-dense-periodic-packings-tetrahedra` |
| Kallus, *Solving geometric puzzles with divide and concur*, Cornell thesis, 2011 | `kallus-2011-solving-geometric-puzzles-with-divide-and-concur` |
| Elser, *How densely can spheres be packed with moderate effort in high dimensions?*, 2023 | `elser-2023-how-densely-can-spheres-be-packed-moderate-effort` |
| Elser, *The complexity of bit retrieval*, 2016 | `elser-2016-complexity-of-bit-retrieval` |
| Elser, *Learning without loss*, 2019 | `elser-2019-learning-without-loss` |
| Lal, *The flow limit of reflect-reflect-relax*, 2025 | `lal-2025-flow-limit-reflect-reflect-relax` |
| Mueller, Heidelberger, Hennix & Ratcliff, *Position based dynamics*, 2007 | `muller-heidelberger-hennix-2007-position-based-dynamics` |
| Macklin, Mueller & Chentanez, *XPBD: position-based simulation of compliant constrained dynamics*, 2016 | `macklin-muller-chentanez-2016-xpbd` |
| Macklin, Storey, Lu et al., *Small steps in physics simulation*, 2019 | `macklin-storey-lu-2019-small-steps-physics-simulation` |
| Mueller, Macklin, Chentanez et al., *Detailed rigid body simulation with extended position based dynamics*, 2020 | `muller-macklin-chentanez-2020-detailed-rigid-body-xpbd` |
| Bender, Mueller & Macklin, *A survey on position based dynamics*, 2017 | `bender-muller-macklin-2017-survey-position-based-dynamics` |
| Stuyck & Chen, *DiffXPBD: differentiable position-based simulation of compliant constraint dynamics*, 2023 | `stuyck-chen-2023-diffxpbd` |
| Hu, Anderson, Li et al., *DiffTaichi: differentiable programming for physical simulation*, 2020 | `hu-anderson-li-2020-difftaichi` |
| Freeman, Frey, Raichuk et al., *Brax: a differentiable physics engine for large scale rigid body simulation*, 2021 | `freeman-frey-raichuk-2021-brax` |
| Werling, Omens, Lee et al., *Fast and feature-complete differentiable physics*, 2021 | `werling-omens-lee-2021-fast-feature-complete-differentiable-physics` |
| Howell, Le Cleac’h, Kolter et al., *Dojo: a differentiable physics engine for robotics*, 2022 | `howell-le-cleach-kolter-2022-dojo-differentiable-physics-engine` |
| Suh, Simchowitz, Zhang et al., *Do differentiable simulators give better policy gradients?*, ICML 2022 | `suh-simchowitz-zhang-2022-do-differentiable-simulators-give-better-policy-gradients` |
| Metz, Freeman, Schoenholz & Kachman, *Gradients are not all you need*, 2021 | `metz-freeman-schoenholz-2021-gradients-are-not-all-you-need` |
| Zhong, Han & Brikis, *Differentiable physics simulations with contacts: do they have correct gradients?*, 2022 | `zhong-han-brikis-2022-differentiable-physics-contacts-correct-gradients` |
| Antonova, Yang, Jatavallabhula et al., *Rethinking optimization with differentiable simulation*, 2022 | `antonova-yang-jatavallabhula-2022-rethinking-optimization-differentiable-simulation` |
| Gupta & Raman, *Differentiable packing of irregular 3D objects with adaptive container estimation*, 2026 | `gupta-raman-2026-differentiable-packing-irregular-3d-objects` |
| Wang & Lu, *Image-space collage and packing with differentiable rendering*, 2024 (screened) | `wang-lu-2024-image-space-collage-and-packing-differentiable-rendering` |
| Debnath, Tiwari, Sadekar & Raman, *RASP: shadow-guided packing*, 2025 (screened) | `debnath-tiwari-sadekar-2025-rasp-shadow-guided-packing` |
| Zhang, Lyu, Rudra et al., *Sequential object placement with convex decomposition*, 2026 (screened) | `zhang-lyu-rudra-2026-sequential-object-placement-convex-decomposition` |

### Smoothed penalties, continuation, and nonlinear-programming packing

| Source | File stem |
| --- | --- |
| Nurmela & Ostergard, *Packing up to 50 equal circles in a square*, DCG 18, 1997 | `nurmela-ostergard-1997-packing-up-to-50-equal-circles-in-a-square` |
| Nurmela & Ostergard, *More optimal packings of equal circles in a square*, DCG 22, 1999 | `nurmela-ostergard-1999-more-optimal-packings-of-equal-circles-in-a-square` |
| More & Wu, *Global continuation for distance geometry problems*, Argonne MCS-P505-0395, 1995 | `more-wu-1997-global-continuation-distance-geometry` |
| Birgin & Sobral, *Minimizing the object dimensions in circle and sphere packing problems*, 2008 | `birgin-sobral-2008-minimizing-object-dimensions-circle-sphere-packing` |
| Birgin & Gentil, *New and improved results for packing identical unitary radius circles*, 2010 | `birgin-gentil-2010-packing-unitary-radius-circles-triangles-rectangles-strips` |
| Birgin, Martinez & Nishihara, *Orthogonal packing of rectangular items within arbitrary convex regions*, 2006 | `birgin-martinez-nishihara-2006-orthogonal-packing-arbitrary-convex-regions` |
| Birgin, *Applications of nonlinear programming to packing problems*, 2016 | `birgin-2016-applications-nonlinear-programming-packing` |
| Romanova, Bennell, Stoyan & Pankratov, *Packing of concave polyhedra with continuous rotations*, EJOR, 2018 | `romanova-bennell-stoyan-2018-packing-concave-polyhedra-continuous-rotations` |
| Peralta, Andretta & Oliveira, *Solving irregular strip packing problems with free rotations using separation lines*, 2018 | `peralta-andretta-oliveira-2018-irregular-strip-packing-free-rotations-separation-lines` |
| Yaskov & Chugay, *Packing equal spheres by block coordinate descent*, 2020 | `yaskov-chugay-2020-packing-equal-spheres-block-coordinate-descent` |
| Lopez & Beasley, *Packing unequal rectangles and squares using formulation space search*, 2018 | `lopez-beasley-2018-packing-unequal-rectangles-squares-formulation-space-search` |
| He, Ye & Wang, *An efficient quasi-physical quasi-human algorithm for packing equal circles in a circular container*, 2018 | `he-ye-wang-2018-quasi-physical-quasi-human-equal-circles` |
| Zhou, He & Zheng, *Geometric batch optimization for packing equal circles*, 2023 | `zhou-he-zheng-2023-geometric-batch-optimization-equal-circles` |
| Hansmann & Wille, *Global optimization by energy landscape paving*, 2002 | `hansmann-wille-2002-global-optimization-energy-landscape-paving` |

## Web Sources

| Key | What | Source | File stem (in `web/`) |
| --- | --- | --- | --- |
| **[Friedman Center]** | Packing Center record tables and diagrams | erich-friedman.github.io | `friedman-packing-center-squares` |
| **[Friedman DS7 html]** | 2009 HTML edition of the DS7 survey | combinatorics.org | `friedman-ds7-survey-2009-html` |
| **[Kingbird]** | Squares-in-Squares catalogue: exact minimal polynomials, rigidity flags | kingbird.myphotos.cc | `kingbird-squares-in-squares` |
| **[Kingbird-compared]** | Supersession history: which record fell to which method, when | kingbird.myphotos.cc | `kingbird-squares-in-squares-compared` |
| **[Kingbird-rigid]** | Author-maintained rigid-packing classification | kingbird.myphotos.cc | `kingbird-squares-in-squares-rigid` |
| **[Kingbird-Göbel-squares]** | The Göbel-square family in closed form, `n = 2(a+1)a + b²` at side `a + 1 + (b/2)√2`, with its rendered members: 32 picture panels over 18 distinct `n`, from 5 to 9465; retrieved 2026-09-07 | kingbird.myphotos.cc | `kingbird-squares-in-squares-gobel-squares` |
| **[Kingbird-Göbel-strips]** | The Göbel-strip family in closed form, `n = (a+1)a + 2 + b` with `b = 1 + ⌊(a−1)√2⌋`, at side `a + 1 + (1/2)√2`, with its rendered members: 152 picture panels over 58 distinct `n`, from 5 to 2135; retrieved 2026-09-07 | kingbird.myphotos.cc | `kingbird-squares-in-squares-gobel-strips` |
| **[Kingbird analytic minimization]** | Author notes on stationary equations for underdetermined packing systems | kingbird.myphotos.cc | `kingbird-squares-in-squares-analytic-minimization` |
| **[Kingbird run statistics]** | First-party simulated-annealing basin frequencies and setup-specific search costs for `n = 51, 55` | kingbird.myphotos.cc | `kingbird-run-statistics-2026/` |
| **[UnitSquare 2026]** | Results Release 1: six reported construction-only improvements and its public structured record | hmbelvedere.com | `unitsquare-release1-2026/` |
| **[Burns–Massaccesi n17]** | Exact-rational weighted lower-bound sources at 4.4811 and 4.5058, their public verifiers, and a distinct near-record topology; retained as method provenance and controls after later project bounds | sam-burns.com; gus-massa.blogspot.com | `n17-lower-bounds-2026/` |
| **[Brandwijk n17 capsule]** | Exact 16-point certificate capsule for `s(17) > 89/20`, offline checker, metadata, local audit, and later supersession context | zenodo.org | `literature-refresh-2026-09-05/` |
| **[Burns n17 addendum 2026-09-07]** | The rest of Burns’s series: the introduction post, the near-record arrangement’s coordinates file and five figures, the two post images, a replay receipt for the retained `4.4811` verifier, and a Squarl repository pointer; extends `[Burns–Massaccesi n17]` without editing its frozen README | sam-burns.com; github.com/sam-bee/squarl | `burns-n17-series-addendum-2026-09-07/` |
| **[GitHub n17 certificates 2026]** | Three August 2026 GitHub certificate repositories for `s(17)` found outside the indexed corpus: Mira’s exact 16-point pose-space certificates (`4.450837`, then `4.468292` with triangle-piercing leaves), Fort’s `4.456575` on the same architecture, and anabologyco-maker’s weighted-measure candidate `9141/2000 = 4.5705` with an exact orientation partition and a Lean layer; retained with their checkers, replay scripts and receipts | github.com | `n17-github-certificates-2026/` |
| **[MacIver 2026 papers]** | Three author-hosted manuscripts: a reported `s(17), s(18) > 4.450208382…`, the center-area lemma, and center-count bounds; original PDFs, faithful extractions, source revision, upstream CI receipt, and a reading aid with verification limits | github.com/DRMacIver; drmaciver.github.io | `maciver-square-packing-2026-09-07/` |
| **[n26 current-source audit 2026]** | Current n26 catalogues, recent solver and proof projects, and an exact comparison of MinMax Arena’s reciprocal score; no smaller public upper bound found in the scoped search | primary catalogues; GitHub; minmaxarena.com | `n26-best-known-2026-09-07/` |
| **[De Winter 2026]** | Mutable author report of proposed construction improvements at `n = 68, 126, 206`; coordinates unavailable and values unreplayed | researchgate.net | `de-winter-improved-packings-2026/` |
| **[Schadt n29 2025]** | Thomas Schadt’s `n = 29` record repository: the packing, its Python verifier, the rendered SVG, and his four-sentence methodology note | github.com/BalthasarStrauss | `schadt-s29-2025/` |
| **[Squarl n17 2026]** | Sam Burns’s open `n = 17` pipeline documentation at a pinned commit: the formulation and move set, the deep-polish architecture and its tolerances, the final nine-hour production search’s own accounting, and the earlier topology drain | github.com/sam-bee/squarl | `squarl-n17-2026/` |
| **[Literature refresh 2026-09-05]** | Frozen arXiv, Crossref, OpenAlex, and Zenodo receipts; additions, currentness checks, and nearby-problem exclusions | primary sources and scholarly indexes | `literature-refresh-2026-09-05/` |
| **[Annealing methods audit 2026-09-08]** | Frozen arXiv, Crossref and OpenAlex receipts for the search-method corpus; the fifteen-paper acquisition manifest, three readings checked against the retained bytes, the screened-out adjacent problems, and the open-access verdict on every source that could not be retrieved | primary sources and scholarly indexes | `annealing-methods-audit-2026-09-08/` |
| **[Simulation methods audit 2026-09-09]** | Frozen arXiv, Crossref, OpenAlex, Semantic Scholar, GitHub and publisher receipts for the physics- and simulation-mechanism corpus, in four disjoint lanes; 101 responses, the seventy-two-paper acquisition manifest with per-file hashes, eight readings checked against the retained bytes, four searches whose zero counts are themselves findings, the screened-out adjacent problems, and every source that could not be retrieved with its obstacle | primary sources and scholarly indexes | `simulation-methods-audit-2026-09-09/` |
| **[`s(11)` lower-bound audit 2026]** | Exact-value, reciprocal, catalogue, citation-chain, and method-lineage search supporting the scoped novelty claim for `381/100` | primary papers; author pages; scholarly indexes; public catalogues | `s11-lower-bound-literature-audit-2026/` |
| **[`s(11)` exact-endpoint audit 2026-09-06]** | Dated exact-value and topic-query receipt for `38100*sqrt(8100042893309449)/899996306539`; a bounded currentness check, not absolute-priority proof | arXiv; Crossref; OpenAlex; general web index | `s11-exact-endpoint-literature-audit-2026-09-06/` |
| **[Finite-case literature audit 2026]** | Repeatable queries and bounded negative result for recent papers on the prioritized cases | arxiv.org; combinatorics.org; author pages | `finite-case-literature-audit-2026/` |
| **[`n = 54` source/formula audit 2026]** | Revision-keyed genealogy, live-SVG formula receipt, quartic-field replay, and typed pose-correspondence gap | combinatorics.org; kingbird.myphotos.cc | `n54-source-formula-audit-2026/` |
| **[Montanher et al. 2018]** | Rigorous packing of unit squares into a circle (full text via PMC) | pmc.ncbi.nlm.nih.gov | `montanher-2018-rigorous-packing-unit-squares-circle` |
| **[Markót 2021]** | Improved interval methods for circle packing in the unit square (full text via PMC) | pmc.ncbi.nlm.nih.gov | `markot-2021-improved-interval-methods-circle-packing` |
| **[squaring.net BSST]** | The Smith-diagram / Kirchhoff correspondence, in detail | squaring.net | `squaring-net-brooks-smith-stone-tutte-II` |
| **[squaring.net Sprague]** | Priority for the first published perfect squared square | squaring.net | `squaring-net-sprague` |
| **[Wikipedia]** | Square packing overview | en.wikipedia.org | `wikipedia-square-packing` |
| **[`n = 19–21` lower-bound audit 2026]** | Versioned DS7 history, evidential status, and bounded priority check for the `24/5` certificate | combinatorics.org; retained papers and web captures | `n19-n21-lower-bound-literature-audit-2026/` |

The MacIver packet preserves three separate citation identities at commit
`9e2cd597047e040a63b7dcd103e79962cfc2d781` (10 August 2026). Its
[reading aid](web/maciver-square-packing-2026-09-07/README.md) distinguishes the
manuscripts’ printed dates from that source revision and the September retrieval date.
No journal venue or DOI for them was identified in the inspected source.

| Key | Manuscript | Printed date | Retained source |
| --- | --- | --- | --- |
| **[MacIver 2026 n17]** | *An improved lower bound for packing seventeen unit squares in a square, via a deformation of Green’s scaffold with certified defect charging* | 8 August 2026 | [PDF](web/maciver-square-packing-2026-09-07/maciver-2026-seventeen-unit-squares-lower-bound.pdf) |
| **[MacIver 2026 center-area]** | *The Center-Area Lemma: Three disjoint unit squares whose centers form a non-obtuse triangle span area at least 1/2* | No date printed; present at the pinned August commit | [PDF](web/maciver-square-packing-2026-09-07/maciver-2026-center-area-lemma.pdf) |
| **[MacIver 2026 nmax]** | *Counting unit squares by their centers: sharp convex bounds and exact strip laws* | August 2026 | [PDF](web/maciver-square-packing-2026-09-07/maciver-2026-counting-unit-squares-by-centers.pdf) |

## Special Kingbird SVG Witnesses

These are not papers, but they carry the source geometry rather than a rendered picture.

- `papers/kingbird-square-11-provenance.svg` is the single most information-dense source
  found on `n = 11`. Its XML comments carry David Ellsworth’s provenance notes, the two
  contact equations, the derived placement constants, and the full exact-solution
  history (Gensane–Ryckelynck 2004 → Ellsworth 2023 → Alexeev’s independent
  confirmation). It is preserved verbatim.
- `papers/kingbird-square-29-provenance.svg` carries Thomas Schadt and David Ellsworth’s
  `n = 29` construction, 100-digit placement constants, the six defining equations, and
  the full SVG transform tree.
  The upstream response was retrieved on 2026-08-24. The retained text differs only by
  CRLF-to-LF normalization and a terminal newline.
  The H-024 experiment records the URL, retrieval date, normalization, and retained
  path; Git retains the source bytes.

## Not Retrievable

The archive records these sources to avoid duplicate searches.
**Re-test this list rather than inheriting it.** On 2026-08-22 three entries were
removed because they turned out to be freely available: Gensane–Ryckelynck (Springer
serves the PDF openly at its `/content/pdf/` URL—the earlier attempt had fetched the
article landing page), Nagamochi (open access in the *Electronic Journal of
Combinatorics*, and cited by its exact title in the archived DS7 reference list all
along), and Wang–Dong–Li (arXiv).
A “not retrievable” verdict is a negative search result, and this archive has now been
wrong about it **eight** times.
On 2026-08-27 the full El Moumni article was found inside the Hungarian Academy’s public
volume scan and Trump’s 2023 note on the author’s own site.
Earlier corrections include Markót 2021 at PMC, Roth & Vaughan (1978) supplied on
request, and Stromquist’s three memoranda on the author’s publication page.
Reading Roth–Vaughan produced two corrections to the published secondary literature.

[`../frontier/source-availability.yaml`](../frontier/source-availability.yaml) records
the maintained list, each obstacle, its dependants, and a route to obtaining the source;
the research document renders it as a table.
The short version below is kept for readers of this archive.

| Source | Obstacle |
| --- | --- |
| Arslanov & Bui, *Note on “efficient packings of unit squares in a large square”*, DCG (2025) | Springer; not open access. |
| Brooks, Smith, Stone & Tutte, *The dissection of rectangles into squares*, Duke Math. J. 7 (1940) | Project Euclid; not open access |
| Gustafsson & Thulin (1980), *Ronden* | Swedish company periodical; Ellsworth notes he has not read it directly either |
| MacIver (2026), supporting C1-C14 certificates and exact ledger/replay scripts | Absent from the inspected public commit of 10 August 2026; checked 7 September. The manuscript itself is archived. |

Six search-method sources were attempted on **2026-09-08** and not retrieved.
[The annealing audit packet](web/annealing-methods-audit-2026-09-08/README.md) records
each attempt, its HTTP result, and its open-access verdict from the retained OpenAlex
probe; the short version is that Basurto et al.
2024 (J. Chem. Phys.
161:044110) and Oakley et al.
2013 (Phys. Chem. Chem.
Phys. 15:3965) are nominally hybrid open access but returned HTTP 403, and that Basurto
et al. 2026 (Comput.
Phys. Commun. 320:109990), Müller et al.
2009 (Phys. Rev. E 79:021102), Gomes & Oliveira 2006 (Eur.
J. Oper. Res. 171:811) and the TAMSASS-PECS chapter are closed.
These are not in
[`../frontier/source-availability.yaml`](../frontier/source-availability.yaml), which
tracks sources bearing on square-packing bounds; these bear on search method.

Twenty further simulation-method sources or groups of them were attempted on
**2026-09-09** and not retrieved.
[The simulation methods audit packet](web/simulation-methods-audit-2026-09-09/README.md)
records each attempt, its HTTP result and its open-access verdict; these too bear on
method rather than on bounds and are not in `source-availability.yaml`. Three patterns
are worth carrying forward rather than rediscovering.
**HAL is gated from this host by an Anubis proof-of-work challenge that returns HTTP 200
with a challenge page**, which is what hides the open copies of the four foundational
contact-dynamics papers (Moreau 1994, Jean 1999, Radjai and Richefeu 2009, Radjai et al.
1996). **The American Physical Society refuses plain `curl` with HTTP 403** even on
bronze open-access articles.
And **a Cloudflare interstitial returns HTTP 200**, so a fetch can appear to succeed and
write an HTML file to a `.pdf` path; one such file was written and deleted in this pass,
and the packet says so.

## Provenance and Licence

The original archive was retrieved on **2026-08-22** from the URLs recorded in each
file’s metadata header.
The El Moumni volume scan was retrieved on **2026-08-27** from the Hungarian Academy’s
REAL-J repository; its article occupies PDF pages 287–296. Trump’s 2023 preprint was
retrieved the same day from his public author page.
The three Stromquist memoranda were retrieved on **2026-08-24** from the author’s
[official publication page](https://www.walterstromquist.com/publications.html), which
links the exact archived PDFs as `squares1.pdf`, `squares2.pdf`, and `squares3.pdf`. All
three PDFs are image-only scans; their raw aids are unedited Tesseract 5.5.0 English OCR
from 300 dpi Poppler-rendered page images, concatenated in page order with form-feed and
newline separators. All 47 pages were visually reviewed on **2026-09-07**, and the
author’s [publication page](https://walterstromquist.com/publications.html) still links
the three notes under Geometry and Topology.
The expanded reading aids describe
[Memo I’s six-square helper argument](papers/stromquist-1984-packing-unit-squares-inside-squares-i-six-unit-squares.md),
[Memo II’s forced incidences](papers/stromquist-1984-packing-unit-squares-inside-squares-ii-ten-unit-squares.md),
and
[Memo III’s historical claims and restricted proof](papers/stromquist-1984-packing-unit-squares-inside-squares-iii-cases-through-65-and-gardner-conjecture.md).
[Stromquist’s Memos and Helper Arguments](../../docs/project/research/research-2026-09-07-stromquist-memos-and-helper-arguments.md)
records their implications for the research program.
The review retains source-level formula slips as explicit reading notes and leaves the
PDFs and raw OCR unchanged.
The fifteen search-method papers and the Squarl documentation were retrieved on
**2026-09-08**; every URL, timestamp and SHA-256 is in
[the audit packet](web/annealing-methods-audit-2026-09-08/README.md), and each `.raw.md`
is `pdftotext -layout` on its retained PDF. The seventy-two simulation- and
physics-method papers were retrieved on **2026-09-09** on the same terms, from arXiv,
from open-access journal and repository mirrors, from author and institutional pages,
and in three cases from the Internet Archive’s copy of a publisher PDF; every URL,
timestamp and SHA-256 is in
[the simulation methods packet](web/simulation-methods-audit-2026-09-09/README.md).
The single OCR sidecar in that batch was produced with `pdftoppm -r 300 -gray -png` and
Tesseract at `--psm 6`, the same method as the Stromquist aids.
Archive PDFs are marked binary in the repository’s `.gitattributes`; this prevents Git
from interpreting compressed scan streams as text without changing any source bytes.
The arXiv and Electronic Journal of Combinatorics items are open access; the Stanford
technical report and PMC item are publicly posted.
Retained for private research use.
Consult the original publisher before redistributing.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
