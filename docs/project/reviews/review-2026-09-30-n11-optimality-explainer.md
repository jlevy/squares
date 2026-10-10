# Eleven-Square Optimality Explainer: Mathematical Review

**Date:** September 30, 2026\
**Reviewer:** Codex, Astra at max reasoning\
**Tracking:** `think-diy1`, under `think-08pw`

**Disposition:** The mathematical prose in
[Why Eleven Squares Need This Much Room][article] correctly explains the accepted T-060
argument. The prose clarifications identified during review are incorporated.
The reviewed article has SHA-256
`88622f7942248b1a7ec561b0fbd735cf675ba30c408778641ec4b751aa4088c5`. The figures,
rendered mathematics and repaired citations are approved.
No blocking finding remains.

This is an exposition review of the completed proof, not a new proof execution or a
stronger theorem. Its premises are the [whole-proof acceptance][acceptance], the
[final composition][composition] with SHA-256
`eaad8f14cf3404e8abe1bfee18cbd7f12a2fed2094f46f021d4e3bfb3088b141`, and the
[simplification disposition][simplification]. No accepted source, receipt, or
mathematical result was changed for this review.

## Mathematical Coverage

| Article argument | Review finding |
| --- | --- |
| Exact theorem and upper bound | The root interval, degree-eight polynomial and expression for $T$ match T-060. Appendix A reproduces the six axis-aligned squares and five rigidly rotated squares in the exact construction. The 44 vertex checks, 55 weak separating-axis checks and opposite-wall spans have the stated scope. Display decimals and SVG coordinates do not define the exact endpoint. |
| Exhaustive center cover | The open radius-`1/2` disks justify center separation at least one. The sixteen closed Voronoi cells cover the normalized center domain and have physical diameter strictly below one. Distinct labels, arbitrary boundary ties, 4,368 masks and 2,184 half-turn representatives follow. The article does not replace these cells with a uniform grid or assume common orientations. |
| Pose preservation | Strict whole-angle cores and owned hulls justify rejecting closed Minkowski collision regions, including their boundaries. Necessary cuts, complete residual coverage, closed angular endpoints and degenerate domains retain every feasible pose. New ownership is used only after its complete supporting check; parent states and parallel common priors remain explicit. |
| Field counting | The mask-transfer rule requires the owner support and a strict charge excess. The five-site charge is defined by median projections, not by containing three sites. Its capacity-one proof uses strict separation of compact cores inside disjoint physical square interiors. Collision alternatives contribute no physical charge. |
| Exclusions and symmetry | The exact exclusion set contains 1,904 field cases and 276 others. The separate $1931+76+173$ grouping describes provenance. The early D4 cuts depend on the complete 1,931-case baseline; they do not borrow the final four-survivor conclusion. Both case-1383 branches remain required. The final D4 overlay argument handles closed ties and uses strict distance bans. |
| Capture and inclusion | The three complementary closed splits, ten nodes, nine parent edges and four leaves match the accepted ancestry. The near state has 136 live angular rows and 1,542 center vertices. Vertex bounds extend by convexity, while full angular intervals require the stated half-angle conversion and quarter-turn chart. Owner-cell labels and local square labels have separate roles. |
| Local isolation | The fourteen contact pairs, 112 features, 88 negative-feature exclusions, 512 raw selections, 128 derivative branches and 8,448 signed-coordinate certificates match the complete local obligation. The proof retains nonlinear remainder bounds and the positive dual margins. It establishes isolation in the finite closed rectangle, rather than only infinitesimal rigidity. |
| Endpoint passage | The field scale is undone before the fixed rotation and translation. A side-`S` container concentric with the cap becomes $[(T-S)/2,(T+S)/2]^2$ in the fixed-`T` frame. For $S<T$, local isolation forces the spanning witness and gives a contradiction. The article neither claims infeasibility at $U$ nor rescales the small squares during this deduction. |

The local inequality has the correct sign.
For a nonzero displacement, set $\tau=\max_j|h_j|/r_j$ and choose a saturated coordinate
and a dual sign opposite its displacement.
Nonnegative dual weights preserve the necessary inequalities $A_i h\ge-\tau^2K_i/2$. The
residual estimate then gives

$$
\tau r_j\le\epsilon_j\tau R+\tau^2M_j/2,
\qquad R=\max_k r_k.
$$

The checked margin $M_j<2(r_j-\epsilon_jR)$ supplies a positive denominator and
$\tau\le c_j\tau^2$ with $c_j<1$, contradicting $0<\tau\le1$. Appendix B preserves the
pair-gap, wall-gap and unavailable-feature Taylor bounds, including the maximum
curvature over elementary gaps sharing a gradient.
This agrees with the [accepted local derivation][local-proof] and
[independent checker][local-check].

## Findings and Resolutions

**Coverage target clarified.** The first draft described coverage of the old domain
without identifying the independently necessary wall and self-containment cuts.
The accepted checker may cover a smaller required domain than the source’s proposed
input domain, provided those cuts have been proved necessary.
The article now states this distinction in “Keeping everything else.”
It preserves the proof obligation that no feasible center is removed by an unsupported
shrink.

**Finite projection directions explained.** The first draft stated that the majority
condition reduces to finitely many directions without giving the reduction.
The article now identifies square-axis directions and normals to site-pair lines.
Between adjacent directions, the median site and support signs remain fixed; each
inequality is linear in the normal.
Every normal in a sector is a nonnegative combination of its bounding rays, so checking
the bounding directions proves the full sector.
This supplies the continuum implication used by the
[reviewed field consumer][field-review].

**Quarter-turn direction clarified.** The displayed frame map correctly uses $Q^{-1}$ to
undo the checked quarter-turn.
The prose now says so explicitly, avoiding an ambiguous description of $Q$ as the map
from captured centers to the construction.

These clarifications do not change the accepted proof or require a geometric replay.
No unresolved mathematical-prose finding remains at the reviewed revision.

**Witness illustration bound to its exact source.** The initial figure helper reused the
known-best atlas illustration, whose provenance supports a numerical drawing rather than
an exact certificate.
The corrected helper regenerates the Trump illustration through `frame_from_trump11()`
and the deterministic SVG renderer, and requires equality with the retained
[exact-construction rendering][witness]. Its pixel coordinates remain rounded display
values.
Accessible prose states that distinction without treating the renderer as a proof
assistant.

**Capture leaf labeled by what it establishes.** The near leaf now reads “local
enclosure.” The separate inclusion and fixed-`T` local theorem discharge that enclosure;
the near capture receipt alone does not prove isolation.
The source-parent graph has the accepted ten nodes and nine edges, and its three far
leaves remain contradictions.

**Radicals restored in the PDF.** The first full PDF inspection found that Appendix B’s
three square-root signs were missing, visibly changing the curvature formulas even
though the Markdown was correct.
The paper’s broad SVG sizing rule also matched KaTeX’s radical SVGs.
Scoping that rule to the authored figure children restored the mathematical glyphs.
The corrected page was rechecked: the translation term has its radical and both the pair
and wall bounds have the required $\sqrt2$ denominators.
This was a publication defect; no proof input or accepted inequality changed.

**Footnote links restored.** A formatting pass had replaced 39 footnote-link targets
with private-use placeholders.
The final article uses direct relative links for those citations.
The source and rendered HTML contain no remaining placeholders; the article’s links and
the PDF’s source URLs were checked.
This repair changes citation targets, not mathematical prose or the proof’s
dependencies.

## Attribution and Evidence Scope

The article credits the global argument to Ahmed’s Astra-assisted work, building on the
Squares Project and Kleddamag, and credits the attaining construction to Walter Trump.
It separately acknowledges David Ellsworth’s reconstruction diagram.
The historical T-018, T-025 and T-026 methods are antecedents; T-037’s strict lower
bound, T-059’s reported row-minimum equality and rectangle-density tools are not used as
substitutes for T-060’s additional premises.

The S5/V4/C5 wording agrees with the [epistemic policy][levels] and current
[T-060 registration][register]. The article discloses shared construction, derivative
and arithmetic primitives, same-method confirmation, and the absence of C4
distinct-method confirmation or V5 proof-assistant verification.
It claims neither new global mathematics nor global uniqueness of all optimal packings.

The final composer reconciles reviewed executions and records `geometry_rerun: false`.
The article correctly separates that operation from the actual observed geometric runs.
It preserves the publisher’s four stale final-state digest defects and the remaining
automation work needed to bind newly generated parent receipts.
These are reproduction limitations of the stated workflows, not missing mathematical
obligations in the accepted ensemble.
The final accepted review, rather than its earlier provisional checkpoints, supports the
article’s conclusion.

## Figure and Rendered-Output Review

The figure source has been checked against its stated roles: the witness depicts a
rounded exact construction, the Voronoi and mask drawings depict center membership, and
the capture tree depicts proof dependencies.
The inspected mask and capture previews match those meanings.
No figure replaces a full angle interval with a sampled angle, erases a closed branch
boundary, or portrays an owned hull as an occupied center cell.

All sixteen pages of the browser-produced PDF were inspected, followed by a separate
inspection of the corrected Appendix B after the scoped CSS fix.
The witness shows all eleven square boundaries and the container clearly.
The center-cell and capture diagrams, closed branch table, local dual inequalities,
endpoint map, placement formulas and evidence table are legible.
No clipped equation, hidden branch condition or mathematical omission was found.
An intermediate ImageMagick preview had dropped the witness’s strokes; the browser/PDF
output preserves them.

The reviewed [figure source][figures] has SHA-256
`e0346647fa7d8aabfe84db452eaf1c4abadfacd5ea75cc33642055ba40e11d63`, and the corrected
[stylesheet][style] has SHA-256
`fe2d9254aa5d94fb13813ea354e7919fdd8d4f98ebf65c617b379237d9a1e48b`. The inspected
sixteen-page preview PDF has SHA-256
`070be9fbbe206f40fb3bd9f652e46a35988647c44c2fb3c253dce0780f1a06d9`. The final rebuild
repairs the footnote links without changing the reviewed mathematical layout.
This identifies the review preview, not a separate proof certificate or a guarantee that
a later build has identical PDF metadata.
The [maintained renderer][renderer] produces the publishable outputs from the reviewed
source and figures.

The publishable PDF should be regenerated after the source commit so its immutable
repository links include the newly added review documents.
This is the normal publication step, not an unresolved mathematical obligation.
The review does not promote T-060 beyond its existing S5/V4/C5 classification.

[article]: ../../../packing/devtools/templates/n11-optimality-article.md
[acceptance]: review-2026-09-29-n11-optimality-census-contract.md#whole-proof-acceptance
[composition]: ../../../packing/resources/web/n11-optimality-2026-09-29/receipts/final-composition.json
[simplification]: review-2026-09-30-n11-expository-simplification.md
[local-proof]: ../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#7-local-contact-analysis-and-the-focused-isolation-rectangle
[local-check]: ../../../packing/devtools/check_n11_optimality_local_isolation.py
[field-review]: review-2026-09-29-n11-optimality-census-contract.md#first-independent-field-exclusion-mask-0
[levels]: ../../../epistemics.md
[register]: ../../../packing/frontier/results.yaml
[witness]: ../../../packing/atlas/rendering/trump11-overview.svg
[figures]: ../../../packing/devtools/n11_optimality_figures.py
[style]: ../../../packing/devtools/templates/n11-optimality.css
[renderer]: ../../../packing/devtools/render_n11_optimality_explainer.py

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
