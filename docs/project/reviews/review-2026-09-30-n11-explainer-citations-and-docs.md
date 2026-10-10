---
title: N11 Optimality Explainer Citation and Documentation Review
date: 2026-09-30
status: draft
---
# N11 Optimality Explainer Citation and Documentation Review

**Scope:** The complete T-060
[article template](../../../packing/devtools/templates/n11-optimality-review-article.md).
The opening and hero were edited separately under think-75cp; this pass changed
citations only from “The Result” onward and reviewed the opening read-only.
This is an editorial source audit, not another verification of the global proof.

## Citation Coverage

The article already distinguished the original argument from the Squares Project’s
component executions.
Its footnotes often cited the whole upstream proof or the whole long acceptance review.
The citation pass now points each major implication to the relevant original proof
section and to its particular checker or accepted receipt:

| Component | Original argument | Project confirmation at first use, caption, or footnote |
| --- | --- | --- |
| Exact endpoint and witness | [PROOF §2](../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#2-exact-construction-and-upper-bound) | [construction source](../../../packing/cases/trump11/packing.py), [exact witness checker](../../../packing/cases/trump11/verify_exact.py), and Figure 1 caption |
| Closed center cover and mask census | [PROOF §4](../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#4-closed-center-cover-and-the-2184-cases) | [D4 cover checker](../../../packing/devtools/check_n11_optimality_d4.py), [receipt](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json), [case census](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/case-census/result.json), and Figure 2 caption |
| Pose preservation and field transfer | [PROOF §5](../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#5-what-an-exact-case-exclusion-certificate-proves) | [capture-row geometry](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-transition-row0/result.json), [complete first update](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-step0/result.json), [field mask-0 result](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/shared-field-mask0/summary.json), and the relevant mathematical review sections |
| Complete exclusion set and symmetry | [PROOF §6](../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#6-the-exact-d4-reduction-to-case438) and [§9](../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#9-accepted-global-verification-obligations) | [2,180-case inventory](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/exclusion-inventory.json) and [D4 receipt](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json) |
| Capture and local endpoint | [PROOF §7](../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#7-local-contact-analysis-and-the-focused-isolation-rectangle) and [§8](../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#8-complete-case438-capture-and-the-exact-u-to-t-bridge) | [root chain](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-root-chain/result.json), [source graph](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/source-graph/result.json), [near node](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-child-near/result.json), [pose inclusion](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json), [local isolation](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/local-isolation/result.json), and Figure 3 caption |
| Deduction of $s(11)=T$ | [PROOF §10](../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#10-deduction-of-the-optimum) | [whole-proof review](review-2026-09-29-n11-optimality-census-contract.md#whole-proof-acceptance) and [final composition](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/final-composition.json) |

The captions now identify the exact witness checker, retained cover data, and source
graph where those figures first appear.
Existing footnotes carry the heavier source-to-receipt map; no new claim or equation was
added. Unused reference aliases were removed while the three used aliases remain.

Rendered-PDF inspection caught one integration defect in the citation edits: Markdown
links inside raw HTML captions appeared as literal text.
The captions now use HTML anchors, and the renderer pins those relative targets through
the same repository-boundary and file-existence checks as Markdown links.
A focused regression assertion checks that the witness citation renders as a linked
anchor.

The opening identifies the original pinned proof, driver, data and reproduction
instructions before describing this repository’s confirmation.
Its credit split agrees with the
[source third-party notices](../../../packing/resources/web/n11-optimality-2026-09-29/source/THIRD_PARTY_NOTICES.md):
Walter Trump’s construction, David Ellsworth’s reconstruction, and the incorporated
Squares Project source have distinct roles.
The [source packet](../../../packing/resources/web/n11-optimality-2026-09-29/README.md)
and [T-060 register](../../../packing/frontier/results.yaml) preserve the
Ahmed/Astra-assisted proof attribution; the article does not assign the original global
argument to this repository’s confirmation.
The retained Ellsworth SVG contains both the reconstruction diagram and exact formulas,
so that specific opening citation is supported.
No link in the generated results table was given a fabricated T-060 fragment anchor.

## Publication Integration Review

A separate read-only Sol engineering pass found no blocking integration issue in the
shared-style extraction, renderers, or Pages selection.
Both renderers supply the shared publication stylesheet, and both declare it among their
render inputs. The Pages push filter includes it; a selected optimality job must succeed
for the aggregate check to pass.
The sparse checkout includes the templates, unresolved template slots fail rendering,
and PDF output respects the shared Letter-size print rules.

Sharing the stylesheet and KPress asset loader gives both papers one source for
publication typography.
Diagram geometry remains specific to each paper.
The development guide and paper-design document now identify that ownership.
The engineering review was read-only; screen/PDF inspection and focused tests provide
the rendering evidence recorded with the draft pull request.

The SVG labels reuse the historical explainer’s measured transform compensation.
A browser regression check compares effective support and note sizes at desktop, mobile,
and print dimensions.
A separate Sol inspection of the rebuilt PDF checked transformed glyph geometry with
pdfplumber/pdfminer: Figure 3 labels measured 12.0288 pt against the 12.0333 pt support
role; notes measured 11.6483 pt against the caption’s 11.6475 pt; prose measured 12 pt.
Poppler XML’s raw font sizes differed for the SVG text, but those values did not account
for its effective transform and did not establish a visual-size discrepancy.

The first hosted publication run exposed a checkout gap (`think-dhsh`): the new
provenance paragraph cited the retained construction SVG and Kleddamag README outside
the proof packet, but the sparse checkout omitted both files.
Their exact paths are now declared as archived citation inputs and included in the
publication checkout and trigger list.
The workflow test also checks the article’s relative archive citations against the
declared inputs, so a later citation cannot silently add another omitted dependency.
The hosted browser floor also found an unchecked nullable parent in the new typography
probe. An explicit guard now reports that malformed DOM state, and the probe passes the
isolated strict TypeScript program as well as its browser regression test.

## Editorial Disposition

Two precision corrections were accepted by the mathematical reviewer and applied in the
article: the finite median-direction argument now names the square cores used here, and
the case-1383 cut identifies $y_{13}=p_y-U/2$ as centered physical height.
They change no proof obligation.

These remaining suggestions are separate from the citation pass and have not been
applied:

- Expand **S5/V4/C5** at first use in the body, with the exact distinctions in
  [epistemics.md](../../../epistemics.md); do not imply proof-assistant formalization or
  a distinct mathematical proof method.
- State explicitly that a square’s angle is modulo $\pi/2$ when introducing
  $t=\tan(\theta/2)$, while preserving both closed endpoints in the checker’s chart.
- At the local inequality’s first strict-margin statement, point the reader forward to
  the positive denominator and derivation later in the same section.
  This is a navigation improvement, not a proposed change to the inequality.

The [illustration plan](../specs/active/plan-2026-09-30-n11-optimality-illustrations.md)
separately lists the proof mechanisms the current four SVGs do not yet show.
The upstream original
[PROOF.md](../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md),
accepted receipts, and final composition remain the evidence; the article and this
review are exposition.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
