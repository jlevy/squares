# Editorial Review: Top-Level Reader Documents and Site Pages

## Scope and Context

Review date: 2026-10-11. Reviewer: GPT-6 Astra, strong-tier editorial lane, xhigh
reasoning. Work is coordinated under `think-mfvg`.

The readers are newcomers learning square packing, researchers checking the project’s
claims, and contributors following its engineering and record conventions.
The review uses the Practical Prose full-edit procedure and its 20 dimensions, with the
common documentation guidelines, AI-prose corrections, and the applicable guidance for
long practical guides.

Safe wording, navigation, and formatting corrections were applied directly.
Scientific claims, evidence classifications, policy choices, and generated research
records were not rewritten to resolve substantive findings.
Ten findings remain for disposition below; the first three affect mathematical scope,
implementation status, or the validation instructions a contributor follows.

### Documents and Coverage

| Source | Coverage |
| --- | --- |
| [TUTORIAL.md](../../../TUTORIAL.md) | All section headings and whole-file lexical/structural checks; close reading of the introduction, bounds, weighted-proof setup, fixed-angle LP argument, exactness and field discussion, capability limits, search strategy, current/open claims, and optimality-proof framework. Detailed later proof steps, notation tables, and references were inspected selectively. |
| [SYNOPSIS.md](../../../SYNOPSIS.md) | Whole-file metrics and lexical checks; every section’s heading and opening assessed for structure and claim calibration. Close reading concentrated on current results, freshness labels, capability declarations, and the promotion pipeline. Long historical handoffs, generated tables, experiment histories, and individual proof claims received selective checks. |
| [conventions.md](../../../conventions.md) | Close reading throughout, including evidence vocabulary, ownership, identifiers, provenance, and validation instructions. |
| [development.md](../../../development.md) | All section headings and openings, whole-file checks, and close reading of setup, code placement, command semantics, validation tiers, and published-site guidance. Long timing histories, release procedures, and individual command recipes were inspected selectively. |
| [operating-rules.md](../../../operating-rules.md) | Close reading of the rules and their evidence, with emphasis on current instructions versus dated measurements. Individual historical timings were not independently replayed. |
| [epistemics.md](../../../epistemics.md) | Close reading throughout, including the V/C definitions, review requirements, composition, status, significance, novelty, and external credit. |
| Site templates | Complete prose read of `atlas-article.md`, `all-results-article.md`, `visualize-article.md`, `papers-article.md`, `frontier-article.md`, and `report-results.md` under `packing/devtools/templates/`. The shared report-results block was audit-only because the front-door lane owns its overview/about context. |
| Generated views | Representative audit of the introductions, classifications, and selected rows in [defects.md](../../../defects.md), [RESULTS.md](../../../packing/frontier/RESULTS.md), and [STATUS.md](../../../packing/frontier/STATUS.md). Generated blocks inside the synopsis were also audit-only. |

The source inventory was traced through `site_documents.DOCUMENTS` and the authored
templates used by `render_overview` and the frontier renderer.
README, the homepage/about templates, navigation, styles, headers, and renderer code
belong to other lanes.

This is a full-dimension editorial audit with selective claim checking, not a
line-by-line certification of the research corpus.
The six root documents measured 148,511 words before editing, including 88,741 in the
synopsis.
Their size limits how much mathematical and historical evidence this review can
independently establish.

## Strengths

- **Definitions support later reasoning (P4, E2, R2).** The tutorial derives the
  fixed-angle linear program from constant corner offsets, linear containment, fixed
  separation, and a linear objective.
  Its weighted-certificate example states the nonnegativity and strict-containment
  premises before using them.
- **Claims usually carry useful boundaries (R3, G1, J1).** The tutorial distinguishes a
  feasible witness, local isolation, and global optimality; its established-results
  table states what each result does not prove.
  The synopsis explains the unexposed arbitrary-witness promotion path despite available
  library components.
- **Credit and confirmation are separated (J2, G3).** Epistemics gives the source’s
  authors credit for a result while separately recording what this project replayed,
  which code it used, and what review remains.
- **The record supports correction (G1, J3).** Known defects, failed searches, and
  unresolved experiments remain visible.
  Operating rules distinguish measured runner variation from an inferred explanation and
  preserve the correction to an earlier regression interpretation.
- **The short site pages orient readers efficiently (P1, F1).** The papers page
  identifies the three n = 11 papers and the methods survey.
  The film page warns that its displayed lower bound predates T-060 and provides a
  direct workbench link.

## Coverage of All 20 Dimensions

| Dimension | Assessment and disposition |
| --- | --- |
| P1 Suitability | The tutorial, conventions, epistemics, and site pages have distinct reader tasks. The synopsis combines current guidance with extensive history; TP-02 and TP-04 identify the resulting burden. |
| P2 Scope | Most introductions state their boundaries. The generic optimality-proof claim exceeds the n = 11 reasoning cited for it (TP-01); the historical upper-bound claims also exceed their stated evidence scope (TP-05). |
| P3 Breadth | The tutorial covers geometry, numerical search, exact verification, and proof. The broad exclusion of counting-based optimality omits recorded alternatives (TP-01). The site inventory includes all authored pages assigned to this lane. |
| P4 Depth | Worked geometric and certificate arguments provide detail proportional to their teaching role. Current capability summaries need reconciliation more than additional exposition (TP-02). |
| E1 Clarity | Removed vague introductory phrasing and clarified the supersession subject. Remaining terminology ambiguity concerns what “formal” means (TP-06). |
| E2 Coherence | The tutorial’s definitions generally precede their use. Mixed historical and current declarations interrupt the synopsis’s current-state account (TP-02, TP-04). |
| E3 Concision | Removed redundant promotion commentary and introductory padding. The synopsis’s scale and duplicate historical state require an author-directed structural decision (TP-04). |
| F1 Organization | Replaced stale numbered tutorial references with links to the vocabulary and notation cards. Site section-level H1 usage was retained as the existing rendering convention. |
| F2 Consistency | Corrected the General Principles heading and punctuation in conventions. Scoped terminology and residual typography remain in TP-06, TP-08, and TP-10. |
| F3 Formatting | Added missing guideline footers to the film and frontier templates. Source formatting was checked with Flowmark; rendered layout remains the coordinator’s integration responsibility. |
| R1 Discipline | Observations, scoped numerical outcomes, and mathematical implications are usually distinguished. Generated defect prose makes a predictive claim without displaying the analysis supporting it (TP-09). |
| R2 Soundness | The sampled fixed-angle and weighted-counting arguments expose their premises. A local method limitation is presented as a general proof limitation (TP-01). This review does not certify every proof step. |
| R3 Precision | Bound gaps, search gaps, assurance, and method are distinguished. Current versus historical capability, “formal,” and the actor earning C need more consistent scope (TP-02, TP-06, TP-08). |
| R4 Parsimony | The tutorial’s derivations serve teaching and inspection rather than duplicate a cited theorem without purpose. The optimality framework needs a scoped premise, not a longer argument (TP-01). |
| G1 Verifiability | Result IDs, retained evidence, and replay commands make sampled claims traceable. Historical universals, legal universals, and the recurrence prediction lack proportionate support (TP-05, TP-07, TP-09). |
| G2 Factuality | T-060’s V3/C3 and the n = 11 bound closure agree with the retained register. Current capability and validation instructions conflict internally (TP-02, TP-03). External history and legal assertions remain unverified. |
| G3 Relevance | Citations generally support nearby claims or provide useful depth. Long historical material belongs to the project record, but its placement within a current synopsis needs review (TP-04). |
| J1 Calibration | The assurance vocabulary usually prevents numerical evidence being promoted into proof. Blanket limitations and “best predictor” language exceed the displayed evidence (TP-01, TP-05, TP-09). |
| J2 Fairness | External contributors retain credit, including when work is superseded. Counting methods that attain an optimum deserve explicit recognition alongside the local/global/capture approach (TP-01). |
| J3 Robustness | Numerical tolerances, implementation independence, alternative checker methods, and historical corrections expose competing interpretations. TP-08 concerns maintaining those distinctions in short summaries. |

## Weaknesses and Suggested Fixes

### Purpose and Reasoning

**TP-01 — High: scope the claimed limitation of counting certificates.** Dimensions: P2,
P3, R2, J1, J2. Location:
[TUTORIAL.md, “Three parts”](../../../TUTORIAL.md#three-parts).
The section says that a counting certificate “cannot reach the known side itself” and
that proving optimality needs a different kind of argument.
It introduces this as a general statement about s(n), citing the n = 11 account.
But the retained register describes T-051’s weighted closed cover proving s(32) = 6 and
T-052/T-053’s mixed covers proving s(21) = 5 and s(45) = 7. Those counterexamples are
already summarized near the start of the synopsis.
Scope the limitation to the particular strict-core certificate family and explain that
local/global/capture is the approach used for the oblique cases discussed here.
Do not present it as necessary for every optimality proof.

**TP-02 — High: reconcile current capability declarations.** Dimensions: P1, E2, R3, G2.
Location: [SYNOPSIS.md, “What Is Built”](../../../SYNOPSIS.md#what-is-built), especially
“Verification Capability Ladder,” “The proof lane,” and “Compiled acceleration.”
The capability ladder says native point and threshold gates have complete distinct
coverage methods. The following proof-lane list still says the interval branch-and-bound
hook, LP duals as unavoidable-set generators, and any Lean formalization are unbuilt.
Elsewhere, the same document describes the weighted-certificate generator and the
confirmed certificate methods.
T-060’s current register entry also retains an October 6 Lean statement audit, with the
full replay still outstanding.
Some old “unbuilt” statements may concern narrower components, but their current wording
does not state that boundary.
Reconcile each against its owning module or record, preserving genuine unexposed
interfaces and incomplete replay work; date historical declarations explicitly.

**TP-04 — Medium: separate current state from dated history.** Dimensions: P1, E2, E3,
F1, G2, G3. Location: the [synopsis opening](../../../SYNOPSIS.md), “Current Handoff,”
“Handoff Record,” and “Where This Stands.”
The opening says Date 2026-10-01 and names an October 1 evidence cutoff, while the
opening results account includes an October 5 replay and the current handoff links an
October 10 plan. The closing “Where This Stands” opens with a September 22 state.
Explicitly dated historical sections are useful evidence; the problem is treating one
date as the freshness signal for a document with independently updated layers.
Replace the ambiguous overall cutoff with clearly scoped freshness information and
consider moving long handoff histories into linked dated records while retaining the
current research summary, definitions, and direct evidence links.
That structural change needs the document owner’s decision.

### Grounding and Judgment

**TP-03 — High: reconcile validation instructions across the guides.** Dimensions: P1,
F2, G2. Location:
[conventions §11](../../../conventions.md#11-what-the-gate-actually-enforces),
[operating rule OR-3](../../../operating-rules.md#or-3-never-wait-on-a-gate-with-nothing-else-in-flight-run-ci-beside-the-research),
and [development’s validation tiers](../../../development.md#validation-tiers).
Conventions says CI runs the full gate on every push.
Development distinguishes the fast PR surface from full/deferred checkpoints.
OR-3 still names a seven-part surface and instructs a records-only pre-push check;
development lists ten partitions and requires the change-reachable push tier.
The nine-versus-ten typo within development itself was corrected, but these wider
instructions determine behavior and need a coordinated policy reconciliation.
Keep the tier definition in development and link the other rules to it.

**TP-05 — Medium: support or narrow claims about the entire history of the field.**
Dimensions: P2, G1, J1. Location: [TUTORIAL.md §1](../../../TUTORIAL.md#1-the-problem)
and [“The catalogue”](../../../TUTORIAL.md#the-catalogue).
“Every upper bound in the history of the subject is a construction,” “No
non-constructive upper bound has ever been obtained,” and “Every record before 2000 came
from here” are universal historical assertions without a nearby source establishing that
coverage. The distinction between checking a construction and excluding all packings is
useful without an unsupported claim about all prior work.
Cite an identified survey with an explicit search boundary, or scope the statements to
the retained corpus.
This review did not establish that the universal claims are false.

**TP-06 — Medium: distinguish formal assurance from proof-assistant verification.**
Dimensions: E1, F2, R3, G2. Location:
[TUTORIAL.md, “Established”](../../../TUTORIAL.md#established), the T-060 row.
It says the result “is not formal,” while the project’s assurance definitions call an
exact machine check formal verification.
The current [T-060 entry](../../../packing/frontier/results.yaml) retains a Lean
formalization report and statement audit but does not yet have a complete retained build
supporting a higher rung.
Say precisely which proof-assistant build and expert review remain outstanding.
Preserve V3/C3: it agrees with the register and should not be promoted from the
existence of a formalization alone.

**TP-07 — Medium: distinguish a source-retention policy from a universal legal claim.**
Dimensions: P2, G1, G2. Location:
[conventions §6](../../../conventions.md#6-provenance), the paragraphs claiming
coordinate facts carry no license forward “regardless of source.”
The owner decision establishes project policy, but the passage supplies no legal
authority or jurisdictional scope for its unconditional legal conclusion.
Have the owner separate the operational policy from any legal proposition it depends on
and provide appropriate authority for the latter.
This review did not perform a legal-source audit or decide the legal claim.

**TP-08 — Medium: keep the confirming party consistent in short definitions.**
Dimensions: F2, R3, J3. Location:
[epistemics, “The Four Classifications”](../../../epistemics.md#the-four-classifications),
[“Results by Others”](../../../epistemics.md#results-by-others), and
[the results-page introduction](../../../packing/devtools/templates/all-results-article.md).
The detailed C definition includes a third party’s retained replay and distinguishes
confirmation from independent implementation.
Later summaries reduce C to “what this repository has done” or “what this repository has
confirmed independently.”
A reader can interpret these as stronger actor or code independence guarantees than the
detailed rules make.
Use a shared short definition that includes retained third-party confirmation and
reserve implementation independence for the explicit relationship field.

**TP-09 — Low: remove engagement rhetoric and substantiate the recurrence prediction.**
Dimensions: E1, R1, G1, J1. Location: [generated defects.md](../../../defects.md), “The
short version” and “What caught them.”
“The line worth reading twice” directs attention instead of stating the finding.
The claim that fixes without a regression check are “the best predictor of what comes
back” is stronger than the displayed recurrence examples establish.
The counts are useful; retain them and distinguish observed recurrences from a
prediction of future ones.
Apply any correction in `devtools.render_defects`, then regenerate the view.
No generator edit was made in this lane.

### Form

**TP-10 — Low: complete a source-aware typography pass on the long documents.**
Dimensions: F2, F3. Whole-file metrics found spaced-em-dash flags in the synopsis,
development, and operating rules.
Examples include
[OR-3](../../../operating-rules.md#or-3-never-wait-on-a-gate-with-nothing-else-in-flight-run-ci-beside-the-research)
around the timing-receipt explanation and development’s cost-history prose.
The common guidelines call for unspaced em dashes or more suitable punctuation.
The raw counts also include table placeholders and retained material, so they are
attention flags rather than a count of confirmed defects.
Conventions’ authored punctuation was corrected directly.
Handle generated blocks at their sources and preserve literal historical quotations.

## Disposition

The coordinator recorded the ten unresolved findings under follow-up epic `think-jb41`.
These follow-ups preserve the scientific and policy questions for their owners; the safe
edits below are complete.

| Finding | Priority | Follow-up bead |
| --- | --- | --- |
| TP-01: Counting-certificate scope | High | `think-3kk4` |
| TP-02: Current capability declarations | High | `think-ygf9` |
| TP-03: Validation instructions | High | `think-az2c` |
| TP-04: Current state and dated history | Medium | `think-fp0c` |
| TP-05: Universal historical claims | Medium | `think-8b3f` |
| TP-06: Formal assurance terminology | Medium | `think-rd7a` |
| TP-07: Source-retention legal claim | Medium | `think-957e` |
| TP-08: Confirming-party definitions | Medium | `think-i168` |
| TP-09: Defect recurrence prediction | Low | `think-76zl` |
| TP-10: Remaining typography | Low | `think-k58j` |

## Edits Applied

- **Tutorial:** shortened introductory framing, removed the instruction to learn ideas
  “properly,” stated the elementary bounds directly, and tightened the near-miss and
  established/open introductions.
- **Synopsis:** removed a redundant explanation of the reported-value promotion
  distinction and the obsolete narration about when its components were missing.
- **Conventions:** repaired the opening grammar, replaced two stale tutorial section
  numbers with direct anchor links, removed redundant commentary, and normalized
  authored punctuation.
- **Development:** clarified a phrase about navigation, corrected nine partitions to ten
  where the following list already has ten, and added submodule initialization before uv
  sync. `.gitmodules` and the local kpress source in `pyproject.toml` support that setup
  dependency.
- **Operating rules:** title-cased General Principles and removed its stale reference to
  “three” principles when OR-14 through OR-18 are listed.
- **Site templates:** clarified that recorded bounds, rather than cases themselves,
  match or beat a superseded bound; added the guideline footer to the film and frontier
  templates.

## Verification and Limits

- Ran `pprose shortcut shortcut-full-edit` and read the Practical Prose, AI-prose,
  common-documentation, and practical-guide guidelines.
- Ran `pprose metrics` on all six root documents and all six listed site templates; the
  default banned-register scan returned zero hits for each.
  Additional lexical searches and section-by-section structural inspection found the
  context-dependent issues described above.
- Ran `python -B -m devtools.check_synopsis` with the project’s Python 3.14 environment:
  passed, reporting agreement with the artifacts, ledger, and defect log.
  This validates the checker’s enumerated contracts, not every natural-language claim;
  TP-02 and TP-04 remain despite the pass.
- Ran `python -B -m devtools.render_operating_rules --check`: passed, reporting that
  `AGENTS.md` mirrors all 18 rules.
- Ran `python -B -m devtools.check_math_markup`: passed, checking 1,526 migrated files
  and retaining 145 spans as code.
- Ran the pinned Flowmark 0.4.0 on the eight edited sources and this review, then
  `flowmark --auto --check --no-cache --force-exclude` on the same paths: passed.
  `git diff --check` also passed.
- Compared the selected T-060, T-051, T-052, and T-053 claims against
  `packing/frontier/results.yaml`; compared the n = 11 and n = 17 frontier rows against
  the generated status view.
  No mathematical certificate was replayed for this editorial review.
- Inspected the owned diff for changed mathematics, identifiers, citations, and claim
  strength. The direct edits preserve them; the setup addition is a documented
  prerequisite correction.
- Build, browser rendering, integrated link checks, and final repository gates are
  coordinated separately.
  This review makes no claim that the published site was deployed or that its rendered
  layout passed from this lane alone.

No external source was independently researched for this review.
Historical, legal, and uncited universal claims therefore remain explicit verification
limits, not implied endorsements.
Numerical benchmark histories, all experiment outcomes, and the full proof corpus were
not independently remeasured or recertified.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
