# Feature: Basic and Advanced Square-Packing Tutorials

**Date:** 2026-10-14

**Author:** Codex, Astra strong tier at xhigh, on the owner’s revision brief

**Status:** Delivered in [PR #604](https://github.com/jlevy/squares/pull/604), merged as
`16ea3bd0606c` and published on 14 October 2026. Shared headings and original
publication dates followed in [PR #617](https://github.com/jlevy/squares/pull/617),
merged as `f97bc0b199e2` and published on 15 October 2026.

**Tracking:** `think-n8md`, under `think-jpto`; the coordinator owns bead changes.

## Purpose and Scope

Split the long tutorial into a short first introduction and a technical companion,
preserving the relevant explanations, definitions, sources and earlier links.
The owner explicitly requested an Astra revision based on the latest results, a much
shorter initial tutorial, and preservation of the original information.

The basic paper is for a reader new to square packing: objects, the definition of
$s(n)$, bounds, examples, rotations and contacts, exact versus numerical evidence, and
how to read the current record.
The advanced paper is for a reader following how the research works: separation cells
and LPs, refinement and terminal families, exact reconstruction, certificates,
regularization, search design, lower-bound mechanisms, global optimality, and the
complete vocabulary and notation cards.

The initial content lane owned the two manuscripts, this plan and the editorial record.
The coordinator then delegated tutorial-specific page integration and its tests to the
same writer.
Scientific registers, witnesses, policies, dependencies and release versions
remain unchanged. The source claims were checked against the admitted record on 14
October 2026; intake packets and reported formalizations retain their recorded limits.

## Manuscripts and Reading Order

| Manuscript | Published page | Role |
| --- | --- | --- |
| [TUTORIAL.md](../../../../TUTORIAL.md) | `tutorial.html`, unchanged | Short beginner paper, prominently featured at the top of Explanations |
| [TUTORIAL-ADVANCED.md](../../../../TUTORIAL-ADVANCED.md) | `tutorial-advanced.html` | Advanced companion after the basic paper in the prominent Tutorial section |

The advanced paper teaches configuration space and linear programming before the
weighted-cover proof that previously interrupted the first section.
It places the certificate, evidence and regularization distinctions together before the
search and proof case studies.
Its retained technical depth is deliberate: shortening the basic paper does not discard
the advanced derivations.

The basic paper keeps the original H1 and `tutorial.html` URL. Its earlier-fragment
landings are explicit HTML anchors beside ordinary links to the advanced paper.
They work in Markdown without a script; the site’s existing document mapper should
rewrite only the document target, keeping the fragment.

## Preservation Map

Every original numbered section is accounted for below.
The subsection map that follows lists every moved heading.
The original document had 20,269 whitespace-delimited words; final counts and source
checks are in the
[editorial review](../../reviews/review-2026-10-14-tutorial-split-editorial.md).

| Original section | Basic destination | Advanced destination and preservation |
| --- | --- | --- |
| Opening and Contents | New opening and reading links | New methods-first outline; audience/ownership boilerplate condensed |
| 1. The Problem | §§1–5: definition, minimum, area/grid bounds, touching, rotation, Trump figure, current status | §6: full lower-bound progression, Stromquist falsification and repair, T-018 proof, finite covering LP, conditional corner-owner example; threshold/dilation explanation expanded |
| 2. The Configuration Space | §§1 and 4: pose/configuration and scope of a fixed-angle solve | §1: every variable, separating-axis choice, LP constraint, numerical reconstruction, angle classes, one-parameter reduction, Kingbird figure |
| 3. Cells, Basins, and Two Traps | §§3–4: sliders, local versus global and refinement | §2: full quench algorithm, both traps, n=3 quotient figure, n=5 sheet with its correct side and distinct rigidity result |
| 4. The Corner | Link from §4 | §2, The corner: basis switch, signed derivatives, measured method comparison and its limitations |
| 5. Algebra Versus Numerics | §4: finite precision, exact and interval evidence | §3: numerical tolerance limits, benchmark table, number fields, primitive elements, semialgebraic argument, all assurance/method definitions, typed contacts, Fritz–John/KKT, rattlers and reconstruction |
| 6. What Is Built, and What Is Not | §§4–5: what a construction and a complete proof establish | §4: capability boundaries retained; certificate/replay, independence, regularization and intake distinctions added |
| 7. How the Search Is Approached, and Why | §4: exploration versus refinement | §5: strategy families, rarity hypothesis, objective/retention distinction, relaxation ladders, calibration and negative measurements, scoped to their historical experiments |
| 8. What Is Known, and What Is Not | §5: selected current cases and the two gaps | §8: full established/open inventory, with current uniqueness, formalization and construction examples |
| 9. How an Optimality Proof Is Built | §5: short explanation of the global proof | §7: all local/global/capture steps, caps, cover cells, capacity, orbits, sub-patterns, admissibility, dual/stress argument, sliders, arithmetic costs |
| 10. A Vocabulary Card | Definitions introduced at first use | §9: every original glossary row retained, refined where needed, with new evidence and regularization terms |
| 11. A Notation Card | Elementary notation introduced at use | §10: every original symbol row retained; regularization side symbols added |
| 12. Further Reading | §7: short route by reader need | §11: complete mathematical reading list and arithmetic/tooling notes, with superseded-status wording corrected |
| 13. Where to Go Next | §7: selected entry points | §12: complete specialist route table retained |

No proof step, formula in a worked derivation, bibliography entry or figure is
intentionally removed.
Repeated framing, promotional absolutes and stale status wording are revised; the
editorial record names those substantive changes.
The source tree retains the detailed original experiments and cited proofs.

### Earlier-fragment destinations

| Earlier fragment on `tutorial.html` | Destination |
| --- | --- |
| `#contents` | [Contents](../../../../TUTORIAL-ADVANCED.md#1-configuration-space-and-linear-programs) |
| `#the-state-of-n--11-in-one-table` | [The state of `n = 11`, in one table](../../../../TUTORIAL-ADVANCED.md#the-state-of-n--11-in-one-table) |
| `#how-a-weighted-atomic-lower-bound-proof-works` | [How a weighted atomic lower-bound proof works](../../../../TUTORIAL-ADVANCED.md#how-a-weighted-atomic-lower-bound-proof-works) |
| `#how-the-finite-covering-lp-searches-for-atoms` | [How the finite covering LP searches for atoms](../../../../TUTORIAL-ADVANCED.md#how-the-finite-covering-lp-searches-for-atoms) |
| `#why-condition-on-corner-squares` | [Why condition on corner squares?](../../../../TUTORIAL-ADVANCED.md#why-condition-on-corner-squares) |
| `#2-the-configuration-space` | [2. The Configuration Space](../../../../TUTORIAL-ADVANCED.md#1-configuration-space-and-linear-programs) |
| `#the-cell-decomposition` | [The cell decomposition](../../../../TUTORIAL-ADVANCED.md#the-cell-decomposition) |
| `#thirty-four-dimensions-become-one` | [Thirty-four dimensions become one](../../../../TUTORIAL-ADVANCED.md#thirty-four-dimensions-become-one) |
| `#3-cells-basins-and-two-traps` | [3. Cells, Basins, and Two Traps](../../../../TUTORIAL-ADVANCED.md#2-refinement-corners-and-connected-families) |
| `#the-quench-map` | [The quench map](../../../../TUTORIAL-ADVANCED.md#the-quench-map) |
| `#trap-1a-fixed-angle-cell-solve-is-not-a-basin` | [Trap 1—a fixed-angle cell solve is not a basin](../../../../TUTORIAL-ADVANCED.md#trap-1a-fixed-angle-cell-solve-is-not-a-basin) |
| `#trap-2a-point-basin-need-not-be-a-terminal-component` | [Trap 2—a point-basin need not be a terminal component](../../../../TUTORIAL-ADVANCED.md#trap-2a-point-basin-need-not-be-a-terminal-component) |
| `#the-generalized-lesson-learned-twice` | [The generalized lesson, learned twice](../../../../TUTORIAL-ADVANCED.md#the-generalized-lesson-learned-twice) |
| `#4-the-corner` | [4. The Corner](../../../../TUTORIAL-ADVANCED.md#the-corner) |
| `#5-algebra-versus-numerics` | [5. Algebra Versus Numerics](../../../../TUTORIAL-ADVANCED.md#3-exact-arithmetic-and-reconstruction) |
| `#why-exactness-is-not-optional` | [Why exactness is not optional](../../../../TUTORIAL-ADVANCED.md#why-exactness-is-not-optional) |
| `#the-number-field` | [The number field](../../../../TUTORIAL-ADVANCED.md#the-number-field) |
| `#how-many-roots-does-a-packing-need` | [How many roots does a packing need?](../../../../TUTORIAL-ADVANCED.md#how-many-roots-does-a-packing-need) |
| `#assurance-method-and-precision` | [Assurance, method, and precision](../../../../TUTORIAL-ADVANCED.md#assurance-method-and-precision) |
| `#contact-graphs-stationary-branches-and-rattlers` | [Contact graphs, stationary branches, and rattlers](../../../../TUTORIAL-ADVANCED.md#contact-graphs-stationary-branches-and-rattlers) |
| `#from-a-numeric-solution-to-an-exact-one` | [From a numeric solution to an exact one](../../../../TUTORIAL-ADVANCED.md#from-a-numeric-solution-to-an-exact-one) |
| `#6-what-is-built-and-what-is-not` | [6. What Is Built, and What Is Not](../../../../TUTORIAL-ADVANCED.md#4-certificates-regularization-and-evidence) |
| `#7-how-the-search-is-approached-and-why` | [7. How the Search Is Approached, and Why](../../../../TUTORIAL-ADVANCED.md#5-search-design-and-its-limits) |
| `#the-catalogue` | [The catalogue](../../../../TUTORIAL-ADVANCED.md#the-catalogue) |
| `#the-strategy-why-pointing-should-beat-scaling` | [The strategy: why pointing should beat scaling](../../../../TUTORIAL-ADVANCED.md#the-strategy-why-pointing-should-beat-scaling) |
| `#steering-keep-the-loss-change-what-you-keep` | [Steering: keep the loss, change what you keep](../../../../TUTORIAL-ADVANCED.md#steering-keep-the-loss-change-what-you-keep) |
| `#relaxation-ladders-turn-rare-event-search-into-path-following` | [Relaxation ladders: turn rare-event search into path-following](../../../../TUTORIAL-ADVANCED.md#relaxation-ladders-turn-rare-event-search-into-path-following) |
| `#calibration-must-match-mechanism-not-just-difficulty` | [Calibration must match mechanism, not just difficulty](../../../../TUTORIAL-ADVANCED.md#calibration-must-match-mechanism-not-just-difficulty) |
| `#near-misses-are-the-data` | [Near-misses are the data](../../../../TUTORIAL-ADVANCED.md#near-misses-are-the-data) |
| `#8-what-is-known-and-what-is-not` | [8. What Is Known, and What Is Not](../../../../TUTORIAL-ADVANCED.md#8-results-and-open-questions) |
| `#established` | [Established](../../../../TUTORIAL-ADVANCED.md#established) |
| `#open` | [Open](../../../../TUTORIAL-ADVANCED.md#open) |
| `#9-how-an-optimality-proof-is-built` | [9. How an Optimality Proof Is Built](../../../../TUTORIAL-ADVANCED.md#7-global-optimality-by-exclusion-and-capture) |
| `#three-parts` | [Three parts](../../../../TUTORIAL-ADVANCED.md#three-parts) |
| `#the-cap-above-the-optimum` | [The cap above the optimum](../../../../TUTORIAL-ADVANCED.md#the-cap-above-the-optimum) |
| `#the-centre-box-and-capacity-one-covers` | [The centre box and capacity-one covers](../../../../TUTORIAL-ADVANCED.md#the-centre-box-and-capacity-one-covers) |
| `#symmetry-and-orbits` | [Symmetry and orbits](../../../../TUTORIAL-ADVANCED.md#symmetry-and-orbits) |
| `#sub-pattern-exclusion-by-containment` | [Sub-pattern exclusion by containment](../../../../TUTORIAL-ADVANCED.md#sub-pattern-exclusion-by-containment) |
| `#selection-versus-certification` | [Selection versus certification](../../../../TUTORIAL-ADVANCED.md#selection-versus-certification) |
| `#what-makes-a-certificate-admissible` | [What makes a certificate admissible](../../../../TUTORIAL-ADVANCED.md#what-makes-a-certificate-admissible) |
| `#a-local-minimum-modulo-sliders` | [A local minimum modulo sliders](../../../../TUTORIAL-ADVANCED.md#a-local-minimum-modulo-sliders) |
| `#capture` | [Capture](../../../../TUTORIAL-ADVANCED.md#capture) |
| `#why-exact-arithmetic-dominates-the-cost` | [Why exact arithmetic dominates the cost](../../../../TUTORIAL-ADVANCED.md#why-exact-arithmetic-dominates-the-cost) |
| `#10-a-vocabulary-card` | [10. A Vocabulary Card](../../../../TUTORIAL-ADVANCED.md#9-vocabulary) |
| `#11-a-notation-card` | [11. A Notation Card](../../../../TUTORIAL-ADVANCED.md#10-notation) |
| `#12-further-reading` | [12. Further Reading](../../../../TUTORIAL-ADVANCED.md#11-further-reading) |
| `#what-does-the-arithmetic-here` | [What does the arithmetic here](../../../../TUTORIAL-ADVANCED.md#what-does-the-arithmetic-here) |
| `#13-where-to-go-next` | [13. Where to Go Next](../../../../TUTORIAL-ADVANCED.md#12-research-and-implementation-guides) |

The original H1 fragment and `#1-the-problem` remain direct headings in the basic paper.
The old `#contents` landing leads to the first advanced section because the site removes
handwritten Contents lists in favor of its contents rail.

## Integration Contract

The writer implemented the following tutorial-specific integration after the initial
manuscript commit. The coordinator retains release and publication ownership.

1. **Page registration and discovery.** Add `TUTORIAL-ADVANCED.md` through
   `packing/devtools/repo_links.py` and `site_documents.py`, with target
   `tutorial-advanced.html`, article metadata and the Explanations current-navigation
   alias. Add it to `render_overview.py`’s page inventory, renderer dispatch and source
   inputs, and to `packing/site-urls.yaml` through its normal registry workflow.
2. **Document and math policy.** Map the new maintained tutorial in
   `docs/project/document-map.yaml`; include its mathematical source in
   `packing/devtools/math-markup.yaml` and the applicable reader-source checks.
   The root-document convention and its test currently list `TUTORIAL.md` explicitly;
   add the advanced companion deliberately in `check_documentation.py` and
   `test_document_layout.py`. Do not bypass the documentation checker.
3. **Reader placement.** Feature both papers in the Tutorial section at the top of
   Explanations, with the basic paper first.
   Keep Papers/PDFs and Film/Workbench presentation under the coordinator’s latest UI
   brief. Suggested basic note: “The problem, bounds, small examples, and how to read a
   packing result.” Suggested advanced note: “Linear programs, exact certificates,
   search, regularization, and global optimality proofs.”
4. **Links and old fragments.** Render both documents and let the central mapper rewrite
   their relative Markdown links.
   Verify all 50 original heading fragments on the basic paper: its original H1 and
   problem heading plus 48 explicit landings.
   Check the sanitized output preserves the explicit anchors.
   Existing methods-survey links to old tutorial fragments can keep working; optionally
   update their source targets to the advanced sections for a direct landing.
   No JavaScript forwarding is required.
5. **Build inputs.** Include the new source in Pages scope and any dependent paper
   inputs, so changing either tutorial rebuilds its consumers.
   Check `test_pages_scope.py`, the explainer’s source-input contracts and change-scoped
   validation selection.
6. **Preserve existing checks at their new owner.** Move the explainer-version reference
   assertion in `test_n11_lower_bounds_explainer.py` to the advanced source, which keeps
   the versioned reference.
   In `check_svg_rendering.py`, retain the Trump figure expectation in the basic paper
   and move the n=3 and n=29 expectations to the advanced paper.
   Update the old long-tutorial card-note assertions in `test_overview.py` to the two
   actual descriptions, preserving title and link checks.
   Exercise `test_site_documents.py` on both pages: math rendering, contents rails,
   source-target rewriting and fragment existence.
   Its old assertion that `tutorial.html` has no `contents` id needs to account for the
   intentional legacy landing; the test that strips a handwritten Contents block remains
   valid.
7. **Publication surfaces.** Both tutorials use the existing reader-document pipeline:
   `tutorial.html`, `tutorial-advanced.html` and their GitHub manuscripts.
   Article metadata, glyph/page measurement lists, URL budgets and publication checks
   cover the new page. The advanced page inherits the original tutorial’s 800 kB
   allowance after measuring 771,603 bytes; the basic page returns to the ordinary page
   limit. The four standalone papers retain their independent editions and PDF producers.
   No tutorial PDF or separate component-version architecture is introduced.
8. **Moved audit coverage.** The negative-control checkout includes the advanced
   manuscript. The T-007 consumer inventory scans both tutorials, its change-scoped
   trigger names the advanced source, and its derived 324-case inventory is refreshed.
   The gallery checks retain all three original tutorial figures at their new owners.

## Implementation and Validation

- [x] Read the original tutorial and its earlier pedagogy/soundness reviews.
- [x] Check material status claims against the current register and primary packets.
- [x] Write the short basic paper and restructure/revise the advanced companion.
- [x] Preserve and inventory definitions, notation, figures, citations and fragments.
- [x] Apply the common-doc, copy-edit, de-slop and substantive editorial passes.
- [x] Format the authored Markdown and perform lightweight source checks.
- [x] Independent mathematical and editorial review; all three findings corrected and
  the repairs verified by that reviewer.
- [x] Integrate page, registry, card and test changes under the contract above.
- [x] Render both papers and check browser typography and clipping at desktop and phone
  widths; verify source/website links and all legacy landings.
- [x] Run focused publication, documentation, source-scope and static checks.
- [x] Complete the coordinator’s combined release disposition, PR review and hosted CI.

Validation reuses the installed Python environment and the pinned local kpress checkout.
There is no dependency installation, PDF build or scientific replay.
The focused source and browser receipts are recorded in the editorial review.
PR #604’s reviewed head passed
[Packing](https://github.com/jlevy/squares/actions/runs/38634417915) and
[Pages](https://github.com/jlevy/squares/actions/runs/38634417893); the
[merged deployment](https://github.com/jlevy/squares/actions/runs/38636016372) published
both tutorials and passed the
[4,243-check live audit](https://github.com/jlevy/squares/actions/runs/38636016372/job/116103959611).
The later original-date and heading refinements passed
[main Packing](https://github.com/jlevy/squares/actions/runs/38722914629) and
[Pages with deployed-site verification](https://github.com/jlevy/squares/actions/runs/38722914631)
at PR #617’s merge. The basic tutorial retains its 1 October first-publication date; the
advanced tutorial’s first publication is 14 October.
The separate CI iteration-cost follow-up, `think-h96x`, remains open.
External scratch is the dedicated `tutorial-basic-advanced` directory; unique source and
editorial evidence live in this worktree.
The writer made local source commits and tutorial registry updates.
The coordinator owned pushes, PRs, release metadata and bead synchronization.

## References

- [Basic manuscript](../../../../TUTORIAL.md)
- [Advanced manuscript](../../../../TUTORIAL-ADVANCED.md)
- [Editorial review and claim-change record](../../reviews/review-2026-10-14-tutorial-split-editorial.md)
- [Epistemics](../../../../epistemics.md)
- [Results register](../../../../packing/frontier/RESULTS.md)
- [Regularization policy](../../policies/regularization-policy.md)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
