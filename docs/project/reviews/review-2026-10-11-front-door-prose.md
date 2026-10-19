# Editorial Review: README, Homepage, and About

## Scope and Context

This W8 documentation pass reviews the project’s public introduction for a reader who
knows little about square packing, a contributor reporting a result, and a developer
arriving at the repository.
The mathematical claims and contributor credits require more care than ordinary
promotional copy: a wording change can imply a stronger proof, broader coverage, or a
different attribution.

The review covers [README](../../../README.md), the
[homepage template](../../../packing/devtools/templates/overview-article.md), the
[About template](../../../packing/devtools/templates/about-article.md), and their
generated prose in
[overview_sections.py](../../../packing/devtools/overview_sections.py): the hero
caption, paper descriptions, documentation cards, resource cards, and media labels.
The shared result invitation was read for context; another editorial lane owns its
source and the other top-level pages.
Navigation, typography, browser behavior, and the bodies of linked papers are outside
this lane.

The Practical Prose full-edit playbook was applied as separate lint, expression,
reasoning, claim, and purpose passes.
The review uses all 20 dimensions without assigning numeric scores.
Safe wording and navigation fixes were applied directly.
Six substantive findings remain for author judgment; the edits preserve numerical
bounds, result IDs, citations, verification ratings, and contributor credits.

## Strengths

- **Readers can reach the evidence.** README’s result summaries name result IDs and link
  the case records and reviews.
  The generated cards distinguish exact finite feasibility from optimality, and several
  explicitly identify what a replay excluded (G1, R3, J1).
- **The principal numerical claims agree with the record.** The eleven-square result,
  Daniel’s infinite family, and the seventeen-square bracket match the retained result
  register. README correctly labels the Lean formalization as its source’s report rather
  than transferring the machine-check rating to it (G2, J1).
- **The site gives unfamiliar readers concrete objects.** The packing illustration,
  definition of $s(n)$, atlas, and linked first-principles tutorial provide a usable
  route into the problem.
  The revised paper introduction now accounts for both tutorials and the three-part
  eleven-square series (P1, P3, E2).
- **Credit and assurance survive compression.** The About page names contributors, the
  resource cards name authors, and the README explains why a feasible witness does not
  establish optimality.
  These distinctions should survive any later shortening (J2, R2, R4).

## Weaknesses by Dimension

The finding IDs in this table refer to the concrete recommendations below.
A dimension with no separate finding was reviewed; it is not a certification of every
linked source.

| Group | Dimension | Assessment and location |
| --- | --- | --- |
| Purpose | P1. Suitability | README’s opening, website links, and result invitation serve the public reader. Its later workflow reference competes with that task; FD-6 proposes a clearer boundary. |
| Purpose | P2. Scope | The opening’s “every known result” and About’s “all known new results” exceed the dated, named-source coverage contract; see FD-1. |
| Purpose | P3. Breadth | The front door covers the problem, atlas, results, papers, reporting, sources, and developer entry points. The homepage’s description of its paper cards omitted the methods tutorial; corrected. Exhaustive coverage of outside work remains unverified under FD-1. |
| Purpose | P4. Depth | Mathematical details are appropriately linked to papers and case records. README’s Core Commands needed a link to environment prerequisites; added. The large process reference receives more space than initial contributor setup; see FD-6. |
| Expression | E1. Clarity | Split the opening’s long inventory, removed decorative size/completeness adjectives from that inventory, shortened the repeated “question is simple” sentence, and named the actor in About’s project history. The magnitude claim “exploded” needs evidence, not just a synonym; FD-2. |
| Expression | E2. Coherence | The progression from problem to atlas and results works. About introduces its contributor list as work building on this project, then labels Daniel’s work independent; FD-3. |
| Expression | E3. Concision | Small repetitions were removed. README still repeats substantial workflow material whose owners it links; FD-6. The contrast between feasibility and optimality is necessary and should remain. |
| Form | F1. Organization | Website links and the repository guide support scanning. Core Commands now points to setup. README’s process section and report catalogue make the front door long; FD-6. Template heading structure is delegated to the site-layout lane. |
| Form | F2. Consistency | The same problem-introduction wording was applied to README and the homepage template. Mathematical notation, result IDs, names, and source-report qualifiers were preserved. |
| Form | F3. Formatting | Flowmark and the README link/structure check cover the edited Markdown. Template metrics do not measure rendered HTML headings or generated card content. Browser layout and final rendered-page verification belong to the integrated check. |
| Reasoning | R1. Discipline | About’s first sentence fuses a claimed increase in activity with an explanation for it. The increase and its cause need separate support; FD-2. |
| Reasoning | R2. Soundness | The feasible-witness/optimality distinction is sound. The AI-causation statement needs a warrant, and the generic definition of an upper bound is too narrow; FD-2 and FD-5. |
| Reasoning | R3. Precision | Exact bounds and result IDs are useful. “Third-party validation,” “cannot overlap,” and “upper bound” need more precise scope for a first-time reader; FD-4 and FD-5. |
| Reasoning | R4. Parsimony | The result summaries cite their proof records rather than attempting condensed reproofs. That is the right argument shape here. No separate issue beyond the unsupported causal step in FD-2. |
| Grounding | G1. Verifiability | Numerical highlights have traceable result IDs. “Every known,” “every other major resource,” and “exploded” lack a defined comparison or coverage test; FD-1 and FD-2. |
| Grounding | G2. Factuality | The checked headline values and assurance distinctions agree with the retained records. Universal current coverage and the claimed cause of the 2026 activity were not established; FD-1 and FD-2. Verification limits are stated below. |
| Grounding | G3. Relevance | The paper and resource links bear directly on the problem and its evidence. README’s detailed work-object and workflow reference is useful to operators but could be linked from this introductory document; FD-6. |
| Judgment | J1. Calibration | The Lean report qualifier and case-review links are well calibrated. Coverage claims and the broad validation label need the same discipline; FD-1 and FD-4. |
| Judgment | J2. Fairness | Named credits are a strength. About’s introductory dependency claim can still imply that the independent contribution derives from this project; FD-3. |
| Judgment | J3. Robustness | Read from a newcomer’s perspective, “third-party” may imply a different degree of independence from the one the record establishes. Read from an outside contributor’s perspective, “all known” may imply their unimported result is absent from the field. FD-1 and FD-4 test those alternative readings. |

## Suggested Fixes for Authors and Editors

### FD-1: Bound the Coverage Promise

**Priority: high. Dimensions: P2, G1, G2, J1, J3.** Locations: README’s first paragraph
(“a full archive of every known result” and “every other major resource”); About’s
paragraph beginning “This project now independently tabulates.”

The [source-coverage register](../../../packing/frontier/source-coverage.yaml) was last
reviewed on 10 October 2026. It defines a corpus of $n = 1\ldots324$ and explicitly
limits coverage to current catalogues and first-party releases known to the project.
It disclaims an exhaustive search of all possible sources.
That supports the concrete corpus statement; it does not establish the unqualified
universal wording.

Choose a coverage statement tied to the maintained record, such as “an archive of
published square-packing results, with a case-by-case atlas for $n = 1\ldots324$,” and
link the coverage policy where useful.
Keep the invitation to report missing work.
Changing this promise is substantive, so the universal wording was left for the author.

### FD-2: Separate Growth in Activity from Its Claimed Cause

**Priority: medium.
Dimensions: E1, R1, R2, G1, G2.** Location: About’s opening sentence,
“Work … has exploded in the summer of 2026 thanks to AI-powered research efforts.”

The result register supplies dated results, and particular source records disclose AI
assistance. Neither fact alone establishes the magnitude “exploded,” the full seasonal
comparison, or the causal claim about the field as a whole.
This review did not perform a historical activity study or a causal analysis.

The author can either cite a defined comparison of activity and explain the contribution
of AI assistance, or replace the opening with a narrower dated observation linked to the
result register. Preserve the source-specific AI credits.
A mechanical replacement of “exploded” with “grown” would leave the underlying
evidentiary problem unresolved.

### FD-3: Separate Independent Results in the About Introduction

**Priority: medium. Dimensions: E2, J2.** Location: “Now several others have obtained
results building on this work, including,” followed by the three contributor bullets.

The Daniel bullet explicitly says “Independently,” and the source comment preserves that
distinction.
The preceding umbrella still says the list consists of work building on this
project.
A reader scanning the introduction can retain that dependency claim and miss its
qualification.

Introduce the list as recent contributions, then state the dependency in the two
eleven-square entries where the record supports it.
Alternatively, separate Daniel’s independent work into its own paragraph.
Preserve all names, links, and mathematical claims.
This is an attribution decision, so it was flagged instead of silently revised.

### FD-4: State What Independence the Validation Claim Means

**Priority: medium. Dimensions: R3, J1, J3.** Location: README’s opening phrase
“agent-based third-party validation.”

The result register separates verification, confirmation, and review.
For example, T-060 stands at V3/C3 and discloses that its reimplementation shares
components with the source.
Its retained adversarial review is an AI review, and its next-rung record names further
review obligations. This does not invalidate the proof or make a third party’s replay
useless; it defines what the assurance claim establishes.

Clarify whether “third-party” means the project checks other authors’ results, or
whether it means an independently implemented method or review of every result.
A short opening description linked to the verification ladders can state the intended
meaning without repeating the ladders.
The stronger interpretations are not established by that label alone.

### FD-5: Distinguish a Bound from the Best Known Bound

**Priority: medium.
Dimensions: R2, R3.** Locations: README’s shared problem introduction
and the matching homepage paragraphs.

An upper bound follows from any valid packing.
The text defines it as the enclosing side for “the tightest packing ever discovered,”
which instead describes the best known upper bound.
A reader learning the concept could infer that a valid, less efficient packing
establishes no bound.
“Cannot overlap” also leaves boundary contact implicit, although the accepted claims
explicitly allow it.

Define an upper bound using a valid construction, then identify the displayed bound as
the best known one if that is the intended claim.
Consider specifying that interiors cannot overlap and boundary contact is allowed.
Retain the existing numbers and the lower-bound source qualifier.
These are changes to mathematical exposition, so this pass leaves them for author
review.

### FD-6: Keep the README’s Process Detail Proportional to Its Entry-Point Role

**Priority: low.
Dimensions: P1, P4, E3, F1, G3.** Locations: Repository Guide, Essential
Conventions, Reports, Autonomous Research Process, and Where the Contracts Live.

The baseline README has 4,246 words by `pprose metrics`, a 40-row report index, and a
long process section that repeats definitions and workflow contracts from linked owner
documents. This is useful reference material, but a new reader must pass through much of
it to understand the repository’s operating model.

Keep the public overview, selected results, setup route, repository map, and a short
assurance explanation.
Consider moving the full workflow table and work-unit reference to their existing owner
documents, leaving a concise link and relationship summary.
Before doing so, update the README checker deliberately: it currently requires the
workflow entries to appear in README. This is a structural and contract decision, not a
copy edit; no sections were removed.

## Disposition

The six substantive findings are tracked under parent epic `think-jb41` for author
judgment. Their proposed changes have not been applied.

| Finding | Bead |
| --- | --- |
| FD-1: Coverage promise | `think-2fxr` |
| FD-2: Growth and AI causation | `think-tnwb` |
| FD-3: Independent contributor credit | `think-l6hy` |
| FD-4: Validation independence | `think-w22u` |
| FD-5: Bound definition and boundary contact | `think-us9y` |
| FD-6: README process detail | `think-wnbn` |

## Edits Applied

- Split README’s long opening inventory into shorter sentences and removed vague
  promotional adjectives from that inventory while retaining the coverage claim for
  explicit review under FD-1.
- Simplified the credit-name request, paper-page description, repository-record
  description, dependency-location sentence, and transition to the two verification
  examples.
- Removed the repeated description of the problem as simple, keeping identical text in
  README and the homepage template.
- Linked environment setup before README’s Core Commands.
- Distinguished the first-principles and methods tutorials in the homepage paper
  introduction.
- Replaced About’s passive project-history sentence with one naming Joshua Levy as the
  actor. Dates, links, and stated mathematical scope were preserved.

## Verification and Limits

The claim audit compared the prominent result summaries against
[results.yaml](../../../packing/frontier/results.yaml), the
[$n = 17$](../../../packing/frontier/n-017.md) and
[$n = 29$](../../../packing/frontier/n-029.md) case records, the source-coverage record,
and the retained
[Lean formalization packet](../../../packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/README.md).
This verifies agreement with the retained evidence and its stated assurance; it is not a
fresh mathematical review or execution of those proofs.

| Check | Result |
| --- | --- |
| Result IDs T-011, T-037, T-051, T-052, T-053, T-060, T-064, T-065, T-093, and T-112 | Headline values agree with README/About. The register has V3/C3 for the first nine and V3/C2 for the uniqueness corollary T-112. |
| Seventeen-square decimal | Recomputed `18641771 / 4000000 = 4.66044275`; it agrees with T-093 and the case record. |
| Daniel’s family scope | T-064 states the theorem for every integer $k \ge 6$ and separately explains the $k = 6\ldots18$ projection onto the retained case corpus. |
| Lean status | T-060 and the retained packet distinguish the reported full verification run from the locally built statement closure and upper half; README preserves the reported qualifier. |
| Report catalogue | Counted 40 Markdown table rows, matching the introductory count. |
| README checker | `uv run --frozen --all-extras --group dev python -m devtools.check_readme` passed: directory, reports, defect sources, work model, and links agree. |
| Formatting | `flowmark --no-cache --auto` on the four owned Markdown files and `git diff --check` passed. The no-cache option avoids writing Flowmark’s default cache to the internal disk. |
| Prose metrics | README 4,246 → 4,236 words; homepage template 216 → 215; About template 281 → 278. Generated blocks and rendered HTML headings are not represented by those template counts. |

All project-Python checks used the task’s external environment, with `TMPDIR`,
`UV_CACHE_DIR`, and `CARGO_TARGET_DIR` assigned under the designated external scratch
directory. Initial sandboxed `uv` invocations could not initialize that external cache;
the focused checks passed after permission review allowed the required location.

The pass did not independently replay proofs, re-audit the contents of all 40 research
reports, fetch every live external resource card target, or establish exhaustive
coverage of outside results.
Their current external state remains unverified by this review.
The card descriptions were reviewed for exposition and assurance language; the selected
numerical highlights received the explicit record checks above.
Final site assembly, rendering, and browser checks are recorded by the coordinating
lane.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
