# Plan: Revising the Verification and Confirmation Ladders

**Date:** 2026-09-30

**Author:** Claude (agent), for the repository owner

**Status:** Proposal for the owner’s decision.
This document changes no rubric, checker or rating.
A stacked implementation of the recommended design, for the owner to review as concrete
diffs, is tracked under the same bead.

**Workflow:** W4 process review

**Beads:** `think-3zg0` (this review); `think-7khl` (does a recorded execution satisfy
V4’s replay predicate); `think-yf6t` (does a same-project review of another author’s
certificate earn C5); `think-74kl` (does a kernel check count toward C)

## Summary

The repository grades every whole result on two six-rung ladders.
`V` is meant to say how strongly a claim has been verified by anyone; `C` is meant to
say how far this repository has confirmed it.
Both ladders are derived by `devtools/check_results.py` from the evidence a result
cites, and today the derivation is purely structural: a rung is earned by the shape of
the evidence record, never by who examined the work or how adversarially.

The owner has asked for three things, in this order:

1. The top rung on both ladders is reserved for **formal verification plus human expert
   review of the formalization**. A kernel check alone is not enough.
2. Rung 4 is **mechanized or highly formal verification, plus extensive adversarial AI
   review by the best models, plus documented human oversight** of the mechanization and
   of the AI checking. The principle behind it: no rung rests on blind trust in a formal
   system or in an agent.
3. `V` measures what a result’s own source certifies (self-certification, or the
   historic certification of the literature); `C` measures how far that verification has
   been independently confirmed, by this project and by third parties.

Applied to the records as they stand, the owner’s design moves **51 of the 60 registered
results**: every `V4` result (50) lands on `V3`, and every `C4` or `C5` result (22)
lands on `C3`, because no result has a retained record of human oversight that meets the
rung-4 standard, and no result has a formal proof whose formalization a human expert has
reviewed. `C5` and `V5` are empty.
T-060, the $n = 11$ optimality result, derives `V3/C3` today and reaches the `V4/C4` the
owner expects the moment the owner’s oversight record of it is retained; a template for
that record is part of the migration.
The owner predicted this outcome (“Probably nothing here then should be at C5. Maybe
nothing at V5 too”), and the records bear it out.

The recommendation is the owner’s design (Design A below), with the following choices
made explicit for the owner to confirm or reverse: two adversarial AI reviews by
distinct reviewers as the floor for “extensive”; the project owner as an admissible
overseer at rung 4; one oversight record per checker family, enumerating the results it
covers; same-project confirmation admitted at `C3` and `C4`; a human expert who is not
the formalization’s author required at `C5`; and dated notes rather than rewritten
history for ratings published under the old ladder.

## 1. The Ladders Today, Exactly

### 1.1 What the Axes Measure

[`epistemics.md`](../../../../epistemics.md) defines the axes at lines 17–22:

> | Verification (`V`) | What is the highest verification rung supported by the cited
> evidence, regardless of who performed it?
> | Structurally derived, except `V0` and `V2`
> | | Confirmation (`C`) | What has this repository recorded, replayed, or established
> itself? | Structurally derived |

Line 146–147, in the section on results by others, restates the split: “`V` is the
strongest verification anywhere, and `C` what this repository has done.”
Line 53–54 restricts `C`: “Confirmation counts only work recorded as `audited-here` or
`replayed-here`, except `C1`, which describes a qualifying read of external evidence.”

Lines 30–33 say that the `V` rungs “are not cumulative: `V4` does not imply publication,
and `V5` means that a proof assistant has checked a formalization, not that the formal
statement matches every intended prose claim.”

### 1.2 The Verification Ladder

| Rung | Meaning (epistemics.md:37–42) | Structural predicate as written | Where enforced |
| --- | --- | --- | --- |
| `V0` | Claimed or recorded only | “No higher predicate; the result explains the classification in `notes`” | `check_results.py:435–438` requires `notes`; derivation falls through at `:346` |
| `V1` | Numerically checked | “A numerical method with recorded precision” | `:341–345`: `method` starts with `numerical` and `precision` is set |
| `V2` | Proof asserted but not publicly recoverable | “Declared with `notes` explaining the unavailable proof” | declared-only (`DECLARED_ONLY_V`, `:51`); `verification_relation` at `:349–351` accepts it over a derived `V0` or `V1` |
| `V3` | Published or audited proof | “`method: published-proof` or `proof-audited`, with a `proof` block” | `:339–340`, `PROOF_METHODS` from `sqpack/assurance.py:13` |
| `V4` | Machine-verified | “Exact-algebraic or interval-certified evidence with a certificate, replay command, and passing replay status” | `_machine_proof_shaped`, `:69–75`; `MACHINE_METHODS = {"exact-algebraic", "interval-certified"}` at `:49` |
| `V5` | Proof-assistant checked | “`method: proof-assistant-checked`” | `:335–336`: the method alone, no certificate, replay or review required |

`derive_verification` (`:334–346`) reads every cited evidence entry regardless of
`origin`, so an external machine certificate raises `V` to `V4`
(`test_results_register.py:88`). No `V` rung reads a review of any kind.

### 1.3 The Confirmation Ladder

| Rung | Meaning (epistemics.md:58–63) | Structural predicate as written | Where enforced |
| --- | --- | --- | --- |
| `C0` | Recorded | “No qualifying read or repository replay” | fall-through at `:95` |
| `C1` | Read | “An `external_review` with a qualifying state, date, reviewer, and note” | `:89–94` and `_qualifying_read`, `:98–104`: state in `{informally-verified, defect-found}` on an entry whose `origin` is `external` or `independently-external` |
| `C2` | Replayed | “Repository-origin evidence with a replay command and `replay_status: passed`” | `:87–88`, over entries with `origin` in `OURS_ORIGINS = {"audited-here", "replayed-here"}` (`:50`) |
| `C3` | Machine-confirmed | “Repository-origin exact-algebraic or interval-certified evidence with a certificate and passing replay” | `:85–86`: `_machine_proof_shaped` over repository-origin entries |
| `C4` | Confirmed by distinct methods | “At least two `C3` evidence entries with different `method` values” | `:83–84`: two distinct `method` values among the machine-shaped repository entries |
| `C5` | Review-ready | “`C3` or `C4`, plus an existing `review_artifact` mapped as a non-superseded review” | `:81–82` with `review_ready` computed at `:413–422`: the path exists and the document map lists it with `role: review` and `lifecycle` not `superseded`; `:453–462` refuses a declared `C5` without it |

Two further rules: a `C3` or higher result must name at least one existing control path
(epistemics.md:67; `check_results.py:451–452`), and “Two independently written
implementations using the same method still derive `C3`, not `C4`” (epistemics.md:71–72;
`test_results_register.py:68–70`).

### 1.4 Composition and the Minimum Rule

A classification attaches to the exact `claim` (epistemics.md:78–79). A compound claim
takes the minimum rung of its load-bearing parts; a derived claim takes the minimum of
its inputs and the derivation; an equality whose upper half is an exactly replayed
packing takes the `C` of its lower half (:81–88). The checker “derives the strongest
rung present among the cited evidence entries” (:90) and accepts a lower declaration
only when a `composition` note is present (`check_results.py:423–432` and `:445–449`);
it refuses any declaration above the derived rung.
Whether the composition note is right is a review obligation (:93–94).

### 1.5 Where the Text Is Silent or Ambiguous

1. **Does a recorded execution satisfy `V4`’s and `C3`’s “replay command, and passing
   replay status”?** (`think-7khl`.) The predicate names a command and a status; it does
   not say the command must rerun the mathematics.
   T-060’s evidence `E-n011-global-optimality-independent` (evidence.yaml:42–100) has
   `replay_status: passed` (:61), but its `replay` text says “these completed executions
   are the evidence … The composition command alone does not rerun geometry” (:53–60),
   its certificate records `geometry_rerun: false`, and the packet README says a fresh
   end-to-end replay needs state-equivalence rebinding (`think-e2ot`). The checker reads
   only the two fields, so T-060 derives `V4/C3` on them.
   The text neither admits nor excludes this reading.
2. **Does a same-project review of another author’s certificate earn `C5`?**
   (`think-yf6t`.) T-037’s `next_rung` (results.yaml:2512–2517) records that “whether a
   same-project review of another author’s certificate qualifies is the owner’s decision
   rather than missing work.”
   T-060 then took `C5` on exactly such a review
   (`review-2026-09-29-n11-optimality-census-contract.md`, Whole-Proof Acceptance,
   :2421–2459). The predicate is a document predicate (“mapped as a non-superseded
   review”) and is silent on who may write the review.
3. **Does an AI-assisted review count as a review?** The `C5` predicate names no
   reviewer at all. T-060’s review was performed by “GPT-6 Astra at max reasoning, with
   Sol implementation and coordinator integration” (evidence.yaml:83). Of the 25
   `reviewed_by` strings in evidence.yaml, every one names an AI model, an AI lane or
   “repository”; none names a person.
   Every one of the eight `review_artifact` documents was written by an AI agent (the
   inventory in §2.6). Practice has been that AI review is review; the text never says
   so.
4. **What does “independent” require?** The word appears in `performed_by:
   independent-external`, `origin: independently-external` and
   `relationship_to_generator: independent-implementation`, and no rung predicate reads
   any of them. T-060’s evidence declares `independent-implementation` (:48) beside a
   limitation that it “is not fully disjoint implementation or a second mathematical
   method” (:91–93). “Independent” currently constrains nothing.
5. **Does a proof-assistant kernel check count toward `C`?** (`think-74kl`.)
   `MACHINE_METHODS` excludes `proof-assistant-checked`, so a kernel check replayed here
   derives at most `C2` by itself.
   T-006 on jlevy/squares#249 reaches `C3` only through the separate `zmx2` replay.
   The review of that build asks the owner the question and the text does not answer it.
6. **“Review-ready” is not “reviewed”.** `C5`’s meaning is a readiness label, but every
   reader surface prints `C5` beside `V4` as the strongest rung the record holds, and
   the review documents it points at state verdicts (“support **V4/C5** for the whole
   equality”). The rung’s name understates what practice has used it for.
7. **One review suffices.** `C5` needs one mapped review; nothing asks for a second
   attempt, a different reviewer, or a confirming pass after defects are fixed.
8. **`V5` has no fidelity requirement.** `V5` is the method value alone.
   The axiom receipt, the statement’s faithfulness to the claim and the build’s
   reproducibility are left to the evidence schema’s `proof` block and to prose.
9. **`V` counts the repository’s own evidence as “anywhere”.** For this project’s
   results the `V` rung and the `C` rung are derived from the same entries, so they
   differ only in the review at `C5`. The two axes nearly coincide for first-party
   results.

### 1.6 Where the Rubric Is Copied or Rendered

| Surface | What it carries | How it is kept in step |
| --- | --- | --- |
| `epistemics.md` §Verification, §Confirmation | the two tables and the prose predicates | the source |
| `packing/devtools/check_results.py` | the derivation and refusals | `tests/test_results_register.py` pins each rung on synthetic atoms |
| `packing/frontier/results.schema.yaml:95–102` | the enums `V0`–`V5`, `C0`–`C5` and the field descriptions | schema validation |
| `packing/frontier/README.md:349–375` | a prose restatement of `C4`, `C5` and the minimum rule | hand-written |
| `packing/frontier/RESULTS.md` header (`render_results.py:46–56`) | one sentence per axis | generated |
| `README.md:148–149` | one sentence per axis | hand-written |
| `TUTORIAL.md:115–125`, `:1294`, `:1313`, `:1344` | prose explanations of `V4`, `C4`, `C5` and T-060’s rungs | hand-written |
| `SYNOPSIS.md` | the generated results-headline block (`:151–223`) and many dated prose mentions of `V4/C5` | the block is generated; the prose is historical |
| the site on jlevy/squares#255 | `overview_sections.rubric_levels` (`:306–320`) parses the `epistemics.md` tables with a regex and renders one card per axis in “Verification at a Glance”; `test_overview.py:362–370` asserts six `V`, six `C` and five `S` levels; chips print the rung letters with a `title` on the column header only | derived from `epistemics.md` |
| `packing/devtools/render_recent_results.py:598` | reads `review_artifact` for the README tables | generated |

`docs/project/paper-design.md` does not exist on either branch, so the site has no
separate written description of the rung badges.

### 1.7 What Practice Has Been

The 60 results on `origin/main` at `cbd01be8c` declare `V0` ×5, `V3` ×5, `V4` ×50; `C0`
×3, `C1` ×4, `C2` ×1, `C3` ×30, `C4` ×14, `C5` ×8 (`attic/derive_ladder.py` over
results.yaml and evidence.yaml; every declaration passes `check_results`). The eight
`C5` results are T-014, T-018, T-022, T-025, T-026, T-034, T-035 and T-060. Twenty-six
results cite two machine-shaped repository entries with distinct methods; twelve of them
declare `C3` with a composition note rather than `C4`, because a derivation step is
decided by one method.

The reviews that earn `C5` are single documents, each by one AI reviewer or by a
reviewer the document leaves unnamed: “Fable, max thinking” for T-034 and T-035, an
“Astra-max review” for T-060, an “independent reviewer for BC-153” for T-014, “a
separate agent from the implementation authors” for T-026, and a first-person author
with no name or model for T-018, T-022 and T-025 (§2.6). The repository owner has not
authored or signed a review document in `docs/project/reviews/`; the owner’s decisions
are recorded in beads and handoffs, and the owner’s review of pull requests is on
GitHub, not in the record.

## 2. The Owner’s Proposal Made Precise

### 2.1 The Owner’s Statements

All of 2026-09-30, verbatim:

1. “We need to review the confirmation and verification ladder rungs.
   The absolute highest confirmation level should be reproducible formal verification
   plus expert human review and confirmation of the proof and the formal verification.
   This should be C5 or perhaps C6. V5 would be formal verification plus human review
   that hasn’t been externally confirmed from this project or other additional sources.”
2. “We should clarify what C4, C5, C6 (if we add it) mean and what the best approach
   here is.”
3. “The current case of n=11 should not be highest levels of verification or
   confirmation since neither is formal now, though they are mechanized and confirmed.
   So I’d be inclined to say they are second-highest rung for V and C but we should
   decide what levels of the epistemics are consistent with what we’ve done so far, as
   well as consistent with what we want in the future.”
4. “I think ideally V5 and C5 would be reserved for formal verification, but not as a
   blind checklist, it must also have gone through human expert review on the
   formalization as well.
   V4 and C4 would be mechanized verification or highly formal verification of some
   form, possibly not fully human reviewed, but should have extensive AI review at a
   minimum, from multiple adversarial attempts with AI and best models confirming it.”
5. “In no case do we blindly trust any formal reasoning system or any agent.
   For V4 and C4, some human oversight of the mechanization and AI checking is needed
   with credible documentation and human review.”
6. “The differences between V and C is that one is basically self certification or
   historic certification where we haven’t readily ‘replayed’ the verification while C
   [is] confirmed, verifiable by us and other third parties.”
7. “Probably nothing here then should be at C5. Maybe nothing at V5 too depending on
   level of the records.”

Statement 1 mixes the axes: “reproducible … plus expert human review and confirmation”
describes `C5`; “formal verification plus human review that hasn’t been externally
confirmed” describes `V5`. Statement 6 separates them, and the rest of this section
follows statement 6.

### 2.2 The Two Axes

**`V`, verification, is the level of verification a result carries as certified by its
own source.** For a result of this project, the source is the producing run and its
retained certificate, reviews and oversight record; for a result by others, it is the
retained source packet at its pinned revision, plus the literature.
`V` asks what kind of verification exists and how it was examined, and does not require
this project to have replayed anything.

**`C`, confirmation, is the level to which that verification has been independently
confirmed and is verifiable:** replayed, rebuilt and reviewed by a party other than the
producing run, which is this project for others’ results, and for this project’s own
results a later replay from the repository, a second implementation, another project, or
an external reviewer.

The two ladders carry the same rung meanings; they differ in who earns each rung.
Under this definition:

- **For this project’s results,** `V` is self-certification: the producing run’s
  certificate, the adversarial AI reviews retained beside it and the owner’s oversight
  of it. `C` needs confirmation beyond that run.
  What counts, from weakest to strongest: a fresh replay of the certificate from the
  repository by a later lane (which is what `replay_status: passed` records, and what
  the gate’s certificate recomputation repeats); a second implementation or method of
  the same decision; a replay by another project; a human expert’s review; a formal
  rebuild. The proposal admits same-project confirmation at `C3` and `C4`, records
  third-party confirmation as an attribute, and requires at `C5` a human expert who is
  not the formalization’s author.
  Whether `C4` should require at least one third party is decision 9 in §6.
- **For others’ results,** `V` is what the source certifies and documents, and `C` is
  what this project (or another third party) confirmed by replaying here.
  T-060 is the test case: the source certifies a mechanized proof; this repository
  executed every exclusion and capture node in its own lanes, retained the receipts
  hash-bound, reviewed the composition with GPT-6 Astra, and reconciles the bindings
  with a composer that records `geometry_rerun: false`. Those executions were performed
  here and are retained, so they are confirmation at `C3` (machine-replayed here) under
  the reading this proposal recommends for `think-7khl`; they reach `C4` with the
  oversight record; a fresh end-to-end replay from the repository (`think-e2ot`) adds
  reproducibility, which this proposal makes a `C5` requirement, and would let the
  composer be rerun rather than reconciled.
- **Is `C` bounded above by `V`?** Every confirmation is also verification evidence, so
  when `V` counts evidence of every origin, as it does today (`:334–346`) and as this
  proposal keeps, $C \le V$ holds for atomic claims by construction.
  If this project formalizes a result whose source published only a paper proof, the
  formalization raises `V` to 4 or 5 and `C` with it.
  The one way `C` can exceed `V` is the minimum rule on a compound claim: T-014 declares
  `V3/C5` because its prose steps cap `V` while its machine parts and review earn `C5`.
  The recommended rule: $C \le V$ after composition, enforced by the checker; a compound
  claim’s `C` is also the minimum over its parts.
  T-014 is reconciled in §4.
- **What changes in how the axes are derived.** Today both axes read the same cited
  entries, `V` with any `origin` and `C` with `origin` in `{audited-here,
  replayed-here}` (plus `C1` reads).
  Under the proposal `V` still reads evidence of any origin, and additionally reads the
  result’s retained reviews; `C` reads evidence whose `origin` is `replayed-here`,
  `audited-here` or `independently-external` (the last being a third party’s own replay,
  retained here), and reads only reviews performed on the confirming side.
  The sentence at epistemics.md:53–54 (“Confirmation counts only work recorded as
  `audited-here` or `replayed-here`”) widens to admit a retained third-party replay.

### 2.3 The No-Blind-Trust Principle

To stand at the head of both ladders in `epistemics.md`:

> No rung rests on blind trust in a formal system or in an agent.
> Every rung from 4 up names the human who examined the work and states what they
> examined, in a record retained in this repository and specific enough to audit.
> A kernel check, a passing certificate replay and an AI review are evidence; a human
> reading them is what turns evidence into a rung.

### 2.4 The Terms as Checkable Predicates

Each term below is given the structural test a checker can run and the evidence that
shows it. What the checker cannot decide is stated.

**Formal verification.** An evidence entry with `method: proof-assistant-checked` whose
`proof` block names the theorem constant and its statement in the record’s own
convention, whose `pinpoints` name the files, and whose `assumptions` list the axioms;
plus a retained axiom receipt (an `artifacts` path matching `*axioms*`) printing only
the standard axioms of the system, with no `sorry`, `native_decide`, `ofReduceBool`,
`extern` or kernel-bypassing option.
Systems: Lean 4 with Mathlib is what the record holds
(`E-n013-evand-casefree-cover-lean-kernel`, evidence.yaml:3231–3267 on #249); Coq,
Isabelle, HOL and Agda would be admitted on the same terms.
*The checker verifies the fields and the receipt; whether the formal statement is
faithful to the claim is the expert reviewer’s finding (below).*

**Reproducible.** The entry’s `origin` is `replayed-here`, its `replay` is a command
runnable from the repository at a pinned toolchain (the Lean toolchain file and the
Mathlib revision named in the entry), and `replay_status: passed` was recorded by a lane
other than the one that produced the proof.
For a mechanized certificate the same reading applies to its checker.
T-060’s `replay` is a prose procedure whose geometric part cannot run from the
repository; it is reproducible at the component level (each receipt’s command is
retained) and not at the ensemble level (`think-e2ot`). This proposal requires ensemble
reproducibility only at rung 5.

**Extensive adversarial AI review by the best models.** At least $N = 2$ retained review
documents of kind `adversarial`, by at least two distinct reviewer identities (a
different model family, or a separately prompted independent lane of the same family
with no shared context), each mapped in the document map as a non-superseded `review`,
each recording the model and reasoning setting, the date, what it attacked, the defects
found and their dispositions; and a final review of kind `confirming` (or the last
adversarial review with verdict `accepted`) dated after every defect’s disposition.
*The checker counts documents and checks fields; “best models” is a dated judgment
recorded in `epistemics.md` as the reasoning tier required (a frontier model at its
maximum reasoning setting, named), and the human overseer attests that the reviews met
it.* $N = 2$ is decision 11.

**Human oversight of the mechanization and of the AI checking (rung 4).** One retained
review of kind `oversight` with `reviewer_kind: human`, naming the person, their
`relation` to the project (`owner`, `project`, `external`), the date, and `checked`
including at least `trust-boundary` (what the checker trusts and what it decides),
`certificate-meaning` (that the certificate’s accepted statement is the claim) and
`ai-findings` (that every adversarial review’s defects were dispositioned).
The record is a document under `docs/project/reviews/` mapped as a review, or a signed
section of one, and it names the result ids it covers.
*The checker verifies the fields, the mapping and the coverage; the content is the
person’s.* An owner-reviewed pull request is not such a record unless the record cites
it and says what was inspected (decision 8).

**Human expert review of the formalization (rung 5).** A retained review of kind
`formalization` with `reviewer_kind: human`, `independent_of_author: true`, naming the
person and their relation, with `checked` including `statement-fidelity`, `definitions`,
`axioms` and `build`, and verdict `accepted`. Expert means a named person who states
their competence in the proof assistant and the mathematics in the record; the owner may
serve at rung 4 and, if not the formalization’s author, at rung 5 (decisions 4 and 6).
The difference from rung 4: at 4 the human oversees the mechanization and the AI
checking of it; at 5 the human reads the formal statement and its definitions and
attests that they say what the claim says.
`V5` needs one such review (whether two, decision 15); `C5` needs two, by distinct named
experts (decided, below).

**`C5`, as the owner decided on 2026-09-30** (“replay on our project plus open source
review and at least two human experts”; “it needs to be replayed here and reviewable and
replayable by any other experts to reach that level and get expert human review at least
a couple times”). Three conditions, all structural:

1. **Replayed here.** The `proof-assistant-checked` entry has `origin: replayed-here`, a
   `replay` command runnable from the repository at a pinned toolchain, `replay_status:
   passed` and an `axioms_receipt`; the rebuild is the whole theorem, not a reduction.
2. **Open.** The proof, its formalization and everything needed to replay it are openly
   available, so that any other expert can review and replay it: an `open_review` record
   on the result names the public `sources` at a pinned revision, the `terms` under
   which they may be inspected and run, the public `replay` instructions, and the copy
   `retained` here. No particular review venue is required; the checker verifies the
   fields and that the retained copy exists.
3. **Expert-reviewed, twice.** At least two `formalization` reviews as above, by
   distinct named human experts, each with its own retained record and an accepting
   verdict.

Whether both experts must be other than the formalization’s author, and whether at least
one must be outside this project, are decisions 3 and 9. Recommended: both other than
the author (a formalization’s author reading their own statement is not a review), and
at least one outside the project that produced the formalization (the owner’s “any other
experts”).

**Externally confirmed, and independent.** A confirmation is external when performed by
a party other than the producing project: for this project’s results, another project’s
replay (`origin: independently-external`, retained) or an external human reviewer; for
others’ results, this project.
A confirmation is independent when it shares no implementation with the producing run;
the proposal records this as the existing `relationship_to_generator` and reads it only
as an attribute (§3.1), never as a rung.

### 2.5 Evidence Fields

Result-level, in `results.schema.yaml`, replacing the single `review_artifact`:

```yaml
reviews:                       # zero or more; required at rung 4 and 5
  - path: docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md
    kind: adversarial          # adversarial | confirming | oversight | formalization
    reviewer: GPT-6 Astra at max reasoning
    reviewer_kind: ai          # ai | human
    relation: project          # owner | project | external | source; required when human
    date: '2026-09-30'
    scope: >-                  # what was examined, in the reviewer's words
      Every component family, execution bindings, adverse controls, endpoint argument.
    verdict: accepted          # accepted | defects-resolved | defect-open | refuted
    checked: [trust-boundary, certificate-meaning, ai-findings]   # oversight/formalization
    independent_of_author: true                                   # formalization only
    covers: [T-060]            # result ids, for a record shared by a family
open_review:                   # required at C5: anyone can review and replay it
  sources: https://github.com/evand/square-packing/tree/6aa82ba4   # public, pinned
  terms: MIT licence           # under which the sources may be inspected and run
  replay: lean/LADDER.md at that revision                          # public instructions
  retained: packing/resources/web/evand-square-packing-2026-09-28/ # the copy here
```

At `C5` the `reviews` list holds two `formalization` entries by distinct named human
experts. Evidence-level, unchanged: `method`, `origin`, `certificate`, `replay`,
`replay_status`, `proof`, `external_review` (which keeps `C1`’s meaning).
One addition: an optional `axioms_receipt` path on a `proof-assistant-checked` entry,
required at rung 5.

### 2.6 Which Existing Review Documents Qualify

The 154 documents under `docs/project/reviews/` were inventoried for this proposal
(`attic/review-inventory.json`; the method is in §4.1).

The inventory read each document’s header, verdict section and model names, and
classified it by what it says of itself; it did not re-read the mathematics.

- **Reviewer.** 94 documents name an AI model, agent, lane or session as reviewer; 60
  state no reviewer; **none names a person** as having performed or signed a review.
  The nearest misses are an owner’s prospective “reviews this PR as a whole afterward”
  (2026-08-31) and an owner “authorized correcting the findings” (2026-09-08), neither a
  record of what was examined.
- **Adversarial.** 61 documents attack or independently re-derive a mathematical claim
  (18 call themselves adversarial; 43 are independent mathematical reviews or replays);
  93 review process, instruments, strategy or documents.
- **Mapping.** 144 retained, 9 superseded (the August set), 1 maintained; all mapped as
  `role: review`.
- **Reviewer as the eight `review_artifact` documents state it:** T-014 “independent
  reviewer for BC-153 (agenda 016)”, model unstated; T-018 no author line, and the
  document says of itself that “its author is an agent of this project working from the
  branch”; T-022 and T-025 unstated, first person; T-026 “a separate agent from the
  implementation authors”; T-034, T-035 “Fable, max thinking”; T-060 author unstated,
  “Astra-max review”. T-025’s artifact never names T-025 and its own verdict reads
  “accepted by one exact route and is not yet a retained result”; T-032 cites a review
  that “is evidence for the coordinator, not a verdict of record”.

Counting, for each result, the adversarial documents that review it (the register’s
`review_artifact`, the reviews its evidence cites, and the inventory’s judgment of
subject), 19 results have two or more: T-014, T-015, T-016, T-018, T-022, T-025, T-035,
T-036, T-037, T-038, T-041, T-043, T-044, T-045, T-047, T-049, T-051, T-059 and T-060.
Fifteen have none by subject: T-006 to T-013, T-019 to T-021, T-023, T-024, T-031 and
T-033. In most of the 19 the reviewers are the same model family in separate lanes
(three Fable reviews for T-051; two Astra documents for T-060, the second a synopsis of
the first) or unnamed, so whether they are “distinct” is decision 11; only T-018 (a
Claude Code review and a GPT-6 Pro review beside three unnamed lanes) and T-037 (Astra
and a separate implementation lane) show two named, different reviewers.
The per-result counts are in the table of §4.2.

## 3. Candidate Designs

The hard constraint for every candidate: T-060, mechanized and confirmed but not formal,
lands on the second-highest rung of both ladders once its records meet the rung’s
standard. Each candidate is judged on two counts the owner named: consistency with what
has been done so far (how many published ratings move, and why), and consistency with
what is wanted in the future (room for formal and externally confirmed results).

### 3.1 Design A: Six Rungs, Top Two Redefined (the Owner’s Design; Recommended)

Rung meanings are shared by both axes; the earner differs.

| Rung | Meaning | `V` is earned at the source by | `C` is earned on the confirming side by |
| --- | --- | --- | --- |
| 0 | Recorded | a claim with no recorded check | registration here, nothing more |
| 1 | Checked lightly | a numerical check with recorded precision | a qualifying read here (`external_review`), or a numerical replay here |
| 2 | Checked without a recoverable certificate | a proof asserted but not publicly recoverable (declared, with `notes`) | a replay here of evidence that yields no machine certificate (`replay_status: passed` on a non-machine method) |
| 3 | Checkable: a complete argument or certificate exists and was checked, without the rung-4 review record | a published or audited proof with a `proof` block, or a machine certificate (exact-algebraic, interval-certified or proof-assistant-checked) with its checker and replay command | a machine certificate replayed here, or a third party’s retained replay, with `replay_status: passed` and a control |
| 4 | Mechanized, adversarially reviewed, human-overseen | rung-3 machine evidence of any origin, plus `N` adversarial AI reviews by distinct reviewers with a confirming pass, plus a human `oversight` record | the same, where the machine evidence is a confirmation (`replayed-here`, `audited-here`, `independently-external`) and the reviews and the oversight were performed on the confirming side |
| 5 | Formal, expert-reviewed | `proof-assistant-checked` evidence with an axiom receipt, plus one human `formalization` review by someone other than the author | that evidence rebuilt and replayed here from the repository at a pinned toolchain (`origin: replayed-here`, `replay_status: passed`); an `open_review` pointer showing the proof, formalization and replay inputs are openly available for anyone to review and replay; and two `formalization` reviews by distinct named human experts |

Attributes recorded and displayed, never rungs: `methods` (the count of distinct machine
methods among the confirming entries; today’s `C4`), `third-party` (a retained replay by
another project), and `independent-implementation`.

Where each kind of evidence sits: a human expert review of the formalization is the
rung-5 condition, one at `V5` and two at `C5` beside the rebuild here and the open
pointer; AI adversarial review is a rung-4 necessary condition and never sufficient; a
replay by another project is a `C3` earner and a `third-party` attribute; a second
method is an attribute at any rung; a formal proof without the expert review is rung 3
(`V3` at the source, `C3` when rebuilt here); a formal proof whose sources are not open
cannot pass `C4` however many experts read it.

**Cost:** the full migration in §5, about 17–20 agent-hours in three lanes.
**Comparability:** 51 of 60 ratings move down on at least one axis (§4.2), with a dated
note; the register keeps the same identifiers and the same six-rung vocabulary.
**Future:** rung 5 is reserved and empty; rung 4 is reachable for the strongest existing
results by writing the oversight records; third-party confirmation has a home.

### 3.2 Design B: Add `C6`, Keep `C0`–`C5` Stable

| Rung | `V` | `C` |
| --- | --- | --- |
| 0–4 | as today | as today |
| 5 | formal proof plus a human expert review of the formalization (new) | review-ready, as today |
| 6 | — | formal proof rebuilt here reproducibly plus a human expert review (new) |

**Cost:** two to three agent-hours: a new enum value, one new predicate at each top, one
new row on each table, the site’s level count test, and no re-derivation.
**Comparability:** no published rating moves; T-060 keeps `C5`, which becomes
second-highest of seven.
**Future:** the top is reserved for formal work, but rung 4 stays “machine-verified”
with no review or oversight requirement, so the no-blind-trust principle (statement 5)
is not applied anywhere below the top, and `C5` keeps meaning “one AI review exists”.
The owner has since said the top stays at 5 (statement 4), so this design is recorded
for comparison only.

### 3.3 Design C: Formal as a `V` Property; `C` Counts Confirmations by Kind

| Rung | `V` (kind of check, any origin) | `C` (independent confirmations, counted by kind) |
| --- | --- | --- |
| 0 | recorded | none |
| 1 | numerical | read here |
| 2 | published proof | replayed here (any method) |
| 3 | machine certificate | one confirmation kind: a machine replay here |
| 4 | machine certificate with adversarial AI review | two kinds among {second method, third-party replay, human expert review, formal rebuild} |
| 5 | formal, expert-reviewed formalization | three kinds, one of them a human expert or a third party |

**Cost:** comparable to A. **Comparability:** `V` moves 50 results from `V4` to `V3`
unless AI review alone suffices; `C` moves the 26 two-method results to `C4` and T-058
(two methods plus the authors’ own verifiers replayed here) to `C5`, above T-060, which
has one method and no third party and so derives `C3`. **Verdict:** this design fails
the hard constraint unless AI review is admitted as a confirmation kind, and if it is,
an AI review alone would carry a result to `C4`, which statement 5 forbids.
Not recommended.

### 3.4 Judgment Against the Two Consistency Tests

| Design | Ratings that move | Principle at rung 4 | Room at the top | T-060 |
| --- | --- | --- | --- | --- |
| A | 51 down, by one rung each, all restorable by records the project can write | applied | `V5`/`C5` reserved, empty | `V3/C3` now; `V4/C4` on the owner’s oversight record |
| B | none | not applied | `C6`/`V5` reserved, empty | `C5` of seven |
| C | 50 down on `V`; 27 up on `C` | not applied | reserved | `V3/C3`, below T-058 |

Design A does both best: it is the only one that applies the owner’s stated principle,
and its movement is uniform (one rung, one stated reason) and reversible by the records
the owner has asked for.
Design B is the honest zero-cost fallback if the owner decides the oversight records are
not worth writing now.

## 4. The Effect on Every Registered Result

### 4.1 Method

Rungs were re-derived with `attic/derive_ladder.py`, which calls
`check_results.derive_verification` and `derive_confirmation` on the live register and
dumps the fields each candidate reads; then the candidate predicates were applied by
hand to those fields.
The human-oversight test was applied strictly, as the owner asked: a rung-4 record must
be a document in the repository written or signed by a named person, stating what they
examined.
Commit authorship, pull-request approval on GitHub, and AI-written reviews that
quote an owner’s decision were not counted.
The adversarial-review count was taken from the inventory in §2.6. The T-006 and T-058
rows for jlevy/squares#249 use that branch’s `results.yaml` and `evidence.yaml`
(`attic/pr249-derived.json`).

### 4.2 Design A

**Human oversight records.** None exists.
The 154 review documents are AI-written or name no reviewer (§2.6); the eight
`review_artifact` documents name a Fable lane, an Astra review, an unnamed agent or no
one; the owner’s decisions live in beads and handoffs as quoted directives, not as
review records naming what was inspected.

**Consequence.** Every result at `V4` lands on `V3` (50 results) and every result at
`C4` or `C5` lands on `C3` (22 results).
`V5` is empty on main, and T-006 on #249 lands on `V3` (its formalization review is
AI-written).
`C5` is empty: no formal verification here has been reproducibly rebuilt and
had its formalization reviewed by a human expert.
No result keeps a 5. The results at `V0`–`V3` and `C0`–`C3` do not move.

The new rung-3 meaning readers see for a lowered result: *Checkable: a complete argument
or certificate exists and was machine-checked; adversarial review and human oversight
not yet recorded.* The chip prints `V3`/`C3`, the attribute chips print `2 methods`
where that holds, and the dated note in `epistemics.md` says the rung was `V4`/`C4`/`C5`
under the ladder of 2026-08-31 to 2026-09-30.

| Result | Headline | Today | Design A now | What restores 4 |
| --- | --- | --- | --- | --- |
| T-001 | $s(17) \ge \frac{4426213}{1000000} = 4.426213$, from a… | `V4/C4/S3` | `V3/C3/S3` (2 methods) | oversight record; 1 adversarial on file (session-060); +1 by a named, distinct reviewer |
| T-002 | $s(18) \ge \frac{4426213}{1000000}$, by monotonicity from… | `V4/C4/S3` | `V3/C3/S3` (2 methods) | oversight record; 1 adversarial on file (session-060); +1 by a named, distinct reviewer |
| T-003 | The sixteen-point set’s unavoidability ceiling… | `V4/C3/S2` | `V3/C3/S2` (2 methods) | oversight record; 1 adversarial on file (session-060); +1 by a named, distinct reviewer |
| T-004 | Bentz 2010, Theorem 8 ($s(46) \ge 7$) is correct as… | `V4/C3/S3` | `V3/C3/S3` | oversight record; 1 adversarial on file (session-060); +1 by a named, distinct reviewer |
| T-005 | Bentz 2010, Lemma 10 is false as printed and true… | `V4/C3/S2` | `V3/C3/S2` | oversight record; 1 adversarial on file (session-060); +1 by a named, distinct reviewer |
| T-008 | $s(46) = 7$ | `V4/C3/S3` | `V3/C3/S3` | oversight record; 0 adversarial on file; +2 by named, distinct reviewers |
| T-009 | $s(29) \le 5.933833\ldots$, by a Krawczyk interval… | `V4/C3/S3` | `V3/C3/S3` | oversight record; 0 adversarial on file; +2 by named, distinct reviewers |
| T-010 | $s(11) \ge 2 + 4/\sqrt{5}$, by a repair of Stromquist… | `V4/C3/S4` | `V3/C3/S4` | oversight record; 0 adversarial on file; +2 by named, distinct reviewers |
| T-011 | Trump’s 1979 packing is exactly valid, so $s(11) \le\ldots$ | `V4/C3/S2` | `V3/C3/S2` | oversight record; 0 adversarial on file; +2 by named, distinct reviewers |
| T-012 | Goebel’s $n = 5$ packing is second-order rigid at… | `V4/C3/S3` | `V3/C3/S3` | oversight record; 0 adversarial on file; +2 by named, distinct reviewers |
| T-013 | Goebel’s $n = 40$ packing: seven verified… | `V4/C3/S3` | `V3/C3/S3` | oversight record; 0 adversarial on file; +2 by named, distinct reviewers |
| T-014 | Goebel’s $n = 5$ optimum is rigid at fixed side:… | `V3/C5/S3` | `V3/C3/S3` | oversight record; 3 adversarial on file (BC-152 lane, unnamed; BC-153 reviewer; independent Max reviewer) |
| T-015 | $s(17) \ge \frac{22529}{5000} = 4.5058$ | `V4/C3/S3` | `V3/C3/S3` | oversight record; 3 adversarial on file (BC-149 reviewer; BC-150 lane; BC-151 lane) |
| T-016 | $s(n) \ge \frac{22529}{5000}$ for $n = 18, 19$, by… | `V4/C3/S3` | `V3/C3/S3` | oversight record; 3 adversarial on file (BC-149 reviewer; BC-150 lane; BC-151 lane) |
| T-017 | $s(12) \ge \frac{99}{25} = 3.96$ | `V4/C4/S4` | `V3/C3/S4` (2 methods) | oversight record; 1 adversarial on file (an unnamed reviewer); +1 by a named, distinct reviewer |
| T-018 | $s(11) \ge \frac{381}{100} = 3.81$ | `V4/C5/S5` | `V3/C3/S5` (2 methods) | oversight record; 5 adversarial on file (Claude Code; GPT-6 Pro by filename; a project agent; an unnamed session reviewer; three agent lanes) |
| T-019 | $s(n) \ge \frac{459}{100} = 4.59$ for $n = 17, 18, 19$ | `V4/C4/S4` | `V3/C3/S4` (2 methods) | oversight record; 0 adversarial on file; +2 by named, distinct reviewers |
| T-020 | $s(n) \ge \frac{24}{5} = 4.80$ for $n = 19, 20, 21$ | `V4/C4/S4` | `V3/C3/S4` (2 methods) | oversight record; 0 adversarial on file; +2 by named, distinct reviewers |
| T-021 | $s(n) \ge \frac{97}{20} = 4.85$ for $n = 20, 21$ | `V4/C4/S3` | `V3/C3/S3` (2 methods) | oversight record; 0 adversarial on file; +2 by named, distinct reviewers |
| T-022 | $s(11) \ge 38100\sqrt{8100042893309449}/899996306539 =\ldots$ | `V4/C5/S5` | `V3/C3/S5` (2 methods) | oversight record; 2 adversarial on file (an unnamed session reviewer; unstated) |
| T-024 | $s(11) \ge 3175000\sqrt{518400042893309449}/\ldots$ | `V4/C3/S5` | `V3/C3/S5` (2 methods) | oversight record; 0 adversarial on file; +2 by named, distinct reviewers |
| T-025 | $s(11) \ge \frac{191}{50} = 3.82$, by a threshold certificate | `V4/C5/S5` | `V3/C3/S5` (2 methods) | oversight record; 2 adversarial on file (a separate agent; unstated) |
| T-026 | $s(11) \ge 955000\sqrt{518400042893309449}/\ldots$ | `V4/C5/S5` | `V3/C3/S5` (2 methods) | oversight record; 1 adversarial on file (a separate agent); +1 by a named, distinct reviewer |
| T-027 | $s(18) \ge \frac{467}{100} = 4.67$ | `V4/C4/S3` | `V3/C3/S3` (2 methods) | oversight record; 1 adversarial on file (three agent lanes); +1 by a named, distinct reviewer |
| T-028 | $s(18) \ge \frac{187}{40} = 4.675$ | `V4/C4/S3` | `V3/C3/S3` (2 methods) | oversight record; 1 adversarial on file (three agent lanes); +1 by a named, distinct reviewer |
| T-029 | $s(18) \ge \frac{1871}{400} = 4.6775$ | `V4/C4/S3` | `V3/C3/S3` (2 methods) | oversight record; 1 adversarial on file (three agent lanes); +1 by a named, distinct reviewer |
| T-030 | $s(18) \ge \frac{4679}{1000} = 4.679$ | `V4/C4/S3` | `V3/C3/S3` (2 methods) | oversight record; 1 adversarial on file (three agent lanes); +1 by a named, distinct reviewer |
| T-031 | The octagon corner class (threshold $\frac{1}{2}$) holds… | `V4/C3/S2` | `V3/C3/S2` (2 methods) | oversight record; 0 adversarial on file; +2 by named, distinct reviewers |
| T-032 | $s(17) \ge \frac{461300}{99999} = 4.61304613\ldots$, and beneath… | `V4/C4/S3` | `V3/C3/S3` (2 methods) | oversight record; 1 adversarial on file (an unnamed reviewer); +1 by a named, distinct reviewer |
| T-033 | $s(11) \ge 955000\sqrt{2073600042893309449}/\ldots$ | `V4/C3/S3` | `V3/C3/S3` (2 methods) | oversight record; 0 adversarial on file; +2 by named, distinct reviewers |
| T-034 | $s(21) \ge \frac{122}{25} = 4.88$ | `V4/C5/S3` | `V3/C3/S3` (2 methods) | oversight record; 1 adversarial on file (Fable, max thinking); +1 by a named, distinct reviewer |
| T-035 | Six-plus-five packings near Trump’s tilt with side… | `V4/C5/S3` | `V3/C3/S3` | oversight record; 2 adversarial on file (Fable, extra-high thinking; Fable, max thinking) |
| T-037 | $s(11) > \frac{31}{8} = 3.875$ | `V4/C4/S5` | `V3/C3/S5` (2 methods) | oversight record; 3 adversarial on file (Astra Max subagent; Astra, Session 152; the native implementation lane) |
| T-038 | $s(17) > \frac{461300}{99853} = 4.6197910929\ldots$ | `V4/C3/S3` | `V3/C3/S3` | oversight record; 2 adversarial on file (Astra, Session 152; an unnamed reviewer) |
| T-039 | $s(17) > \frac{231001}{50000} = 4.62002$ | `V4/C3/S3` | `V3/C3/S3` | oversight record; 1 adversarial on file (Fable max for the mathematics, Opus 5.5 for the replays); +1 by a named, distinct reviewer |
| T-040 | $s(17) > \frac{232001}{50000} = 4.64002$ | `V4/C3/S3` | `V3/C3/S3` | oversight record; 1 adversarial on file (Fable max sub-agent); +1 by a named, distinct reviewer |
| T-041 | $s(17) > \frac{466001}{100000} = 4.66001$ | `V4/C3/S3` | `V3/C3/S3` | oversight record; 2 adversarial on file (two Fable max sub-agents) |
| T-042 | $s(17) > \frac{233009}{50000} = 4.66018$ | `V4/C3/S2` | `V3/C3/S2` | oversight record; 1 adversarial on file (Fable max sub-agent); +1 by a named, distinct reviewer |
| T-043 | $s(17) > \frac{116511}{25000} = 4.66044$ | `V4/C3/S3` | `V3/C3/S3` | oversight record; 2 adversarial on file (two Fable max sub-agents) |
| T-044 | Weighted point lower bounds for ten counts in $n =\ldots$ | `V4/C3/S3` | `V3/C3/S3` | oversight record; 2 adversarial on file (Astra, Session 152; a Session 152 lane) |
| T-045 | $s(27), s(28) \ge \frac{28}{5}$, $s(31) \ge \frac{148}{25}$ and $s(32)\ldots$ | `V4/C3/S3` | `V3/C3/S3` | oversight record; 2 adversarial on file (Fable max sub-agent; a Session 152 lane) |
| T-047 | $s(11) \ge \frac{381}{100}$; $s(n) \ge \frac{1377}{250}$ for $n =\ldots$ | `V4/C3/S4` | `V3/C3/S4` | oversight record; 2 adversarial on file (Astra, Session 152; a Session 152 lane) |
| T-049 | $s(12) \ge \frac{15680}{3951} = 3.9686155\ldots$ | `V4/C4/S3` | `V3/C3/S3` (2 methods) | oversight record; 2 adversarial on file (Fable max sub-agent; the native implementation lane) |
| T-050 | $s(21) \ge \frac{5000}{1001} = 4.995004995\ldots$ | `V4/C3/S3` | `V3/C3/S3` | oversight record; 1 adversarial on file (Fable max sub-agent); +1 by a named, distinct reviewer |
| T-051 | $s(32) = 6$ | `V4/C4/S4` | `V3/C3/S4` (2 methods) | oversight record; 3 adversarial on file (three Fable max sub-agents) |
| T-052 | $s(21) = 5$, by a mixed cover of points and… | `V4/C3/S4` | `V3/C3/S4` (2 methods) | oversight record; 1 adversarial on file (Fable max sub-agent); +1 by a named, distinct reviewer |
| T-053 | $s(45) = 7$, by a mixed cover of points and… | `V4/C3/S4` | `V3/C3/S4` (2 methods) | oversight record; 1 adversarial on file (Fable max sub-agent); +1 by a named, distinct reviewer |
| T-054 | $s(45) = 7$ by a second, point-only route | `V4/C3/S2` | `V3/C3/S2` (2 methods) | oversight record; 1 adversarial on file (Fable max sub-agent); +1 by a named, distinct reviewer |
| T-056 | Smaller packings for 49 counts from $n = 68$ to… | `V4/C3/S3` | `V3/C3/S3` | oversight record; 1 adversarial on file (Fable max sub-agent); +1 by a named, distinct reviewer |
| T-057 | $s(211) \le 14.99796070496771500150 < 15$, the first… | `V4/C3/S3` | `V3/C3/S3` | oversight record; 1 adversarial on file (Fable max sub-agent); +1 by a named, distinct reviewer |
| T-060 | Trump’s eleven-square packing is globally optimal | `V4/C5/S5` | `V3/C3/S5` | oversight record; 2 adversarial on file (Astra at max reasoning, in two documents of one review stream) |

Counting the 51 rows: 17 results have two or more adversarial reviews on file and need
only the oversight record under decision 11’s lenient reading; 22 have one and need one
more; 12 have none and need two.

The named cases:

- **T-060** ($s(11) = T$): `V4/C5/S5` → `V3/C3/S5`. Mechanized at the source; every
  component executed here and retained; two Astra documents (the census and capture
  contract with its whole-proof acceptance, and the source-intake handoff that
  summarizes it), no human record.
  Restores `V4/C4` with: one `oversight` record by the owner naming the result, stating
  that the composer’s trust boundary, the composition’s meaning as the equality, and the
  Astra reviews’ dispositions were inspected; and one further adversarial review by a
  distinct reviewer if the owner sets $N = 2$ with distinct families (decision 11). Path
  to 5: a formalization of the whole argument, which no one has begun.
- **T-006** ($s(13) = 4$): on main `V3/C1/S3` → unchanged.
  On #249 `V5/C3` → `V3/C3`: the kernel check is formal, but the review of statement
  fidelity (`review-2026-09-30-lean-s13.md`) was written “by the independent adversarial
  reviewer of this session”, an AI lane.
  It is the strongest candidate for 5 on both axes: the build was reproduced here (1 h
  45 min, pinned Lean 4.33.1 and Mathlib, axiom receipt retained), so `C5` needs only
  one human expert’s `formalization` review by someone other than Evan Daniel, with
  `statement-fidelity`, `definitions`, `axioms` and `build` checked, and `V5` the same.
- **T-037** ($s(11) > 31/8$): `V4/C4/S5` → `V3/C3/S5`, attribute `2 methods`. Two mapped
  same-project reviews of 2026-09-22 exist (Kleddamag mathematics; native parent-core).
  With the owner’s oversight record it restores `V4/C4`, and `think-yf6t` is answered: a
  same-project review counts at rung 4, and the question of `C5` no longer arises for a
  non-formal result.
- **T-051** ($s(32) = 6$): `V4/C4/S4` → `V3/C3/S4`, attribute `2 methods`. Reviews:
  `review-2026-09-27-evand-s32-s12.md` (Fable max) and the point-only review of
  2026-09-28. Restores 4 with the oversight record.
  Path to 5: build the source’s hypothesis-free `s32_eq_6` here (14–28 CPU-hours; the
  conditional theorem was built on 2026-09-30) and obtain the human expert review.
- **T-052, T-053** ($s(21) = 5$, $s(45) = 7$): `V4/C3/S4` → `V3/C3/S4`. The reduction
  `s21_eq_five_of_checker` was kernel-checked here; the checker statement is not yet
  proved in Lean and $s(45)$ was not run.
  Same path as T-051.
- **T-014** ($n = 5$ rigidity): `V3/C5/S3` → `V3/C3/S3`, and with the $C \le V$ rule its
  `C` is the minimum over parts, which the composition note must restate; the prose
  steps that cap `V` at 3 also cap `C` at 3.
- **T-018, T-022, T-025, T-026, T-034, T-035** (`C5` today): → `C3`. Each has one
  adversarial Fable review and distinct methods; each restores `V4/C4` with the owner’s
  oversight record and, under $N = 2$ with distinct families, one more adversarial
  review.

### 4.3 Design B

No rating moves on main.
T-006 on #249 moves `V5` → `V4` (no human expert review), and T-060 stays `V4/C5`, now
of seven rungs. The `C6` rung is empty.

### 4.4 Design C

`V`: 50 results `V4` → `V3`, as in A, unless AI review is admitted alone, in which case
the results with one adversarial review stay at `V4`. `C`: the 26 two-method results
derive `C4`; T-058 derives `C5`; T-060 derives `C3`.

### 4.5 Paths From 4 to 5

| Result | `V` path | `C` path |
| --- | --- | --- |
| T-060 | formalize the exclusion ensemble, capture induction and local isolation; nothing exists | the same, rebuilt here; ensemble reproducibility (`think-e2ot`) first; openness of the 2.3 GB of inputs now outside Git; two experts |
| T-006 (#249) | one human expert’s formalization review of `s13_eq_4`; the build exists | the rebuild here already passed; the source is public (`evand/square-packing` at `6aa82ba4`, retained) so the open condition is met once the pointer is recorded; two human experts’ reviews remain |
| T-052 (`s(21)`) | prove the checker statement `S21CheckerCover` in Lean at the source or here; then one expert review | rebuild here; open pointer; two expert reviews |
| T-051 (`s(32)`) | build `s32_eq_6` (14–28 CPU-hours); one expert review | the same, here; open pointer; two expert reviews |
| T-053 (`s(45)`) | no Lean reduction exists for 45; write it, then as for 21 | the same |

## 5. Migration for Design A

In order, with the owner’s choices marked where the implementation takes a provisional
option:

1. **`epistemics.md`**: the principle (§2.3) at the head of the two ladders; the axis
   table rewritten in the owner’s terms (§2.2); the two rung tables with the one-line
   meanings of §3.1 and their earners; a section on review records (§2.4, §2.5); the
   attributes; the $C \le V$ rule; and a dated note: “Ratings published between
   2026-08-31 and 2026-09-30 used a ladder on which `V4` meant machine-verified, `C4`
   confirmed by distinct methods and `C5` review-ready; each result’s `notes` says what
   it held then.” The regex `overview_sections._LEVEL_ROW` reads rows of the form
   ``| `V4` | meaning |``, so the tables keep that shape.
2. **`results.schema.yaml`**: `reviews` (§2.5) replaces `review_artifact`; `attributes`
   optional; the rung enums unchanged.
   **`frontier-evidence.schema.yaml`**: `axioms_receipt` optional.
3. **`check_results.py`** and `tests/test_results_register.py`: `derive_verification`
   reads evidence of any origin plus the result’s reviews; `derive_confirmation` reads
   confirming-origin evidence plus confirming-side reviews; rung 4 needs the adversarial
   count, the distinct reviewers, the confirming pass and the human oversight record;
   rung 5 needs the formal entry, the axiom receipt and the human formalization review;
   $C \le V$; every review path mapped and non-superseded; the tests pin each predicate
   on synthetic atoms and the live register.
4. **`results.yaml`**: every result re-derived; the 51 lowered results get a dated
   `notes` line; the eight `review_artifact` fields become `reviews` entries with the
   reviewer as the document states it; `last_reviewed` advanced.
   T-060’s `next_rung` names the oversight record as the next action.
   **Owner choice marked:** $N = 2$, distinct reviewers, owner admissible as overseer.
5. **Renders**: `RESULTS.md`, `STATUS.md`, `INVENTORY.md`, the synopsis headline block,
   the README tables (`render_results`, `render_research_tables`,
   `render_evidence_inventory`, `render_results_headline`, `render_recent_results`), and
   `packing/frontier/README.md:349–375` rewritten by hand.
6. **Hand-written sentences**: `README.md:14` (`V4/C5/S5`), `README.md:148–149`,
   `TUTORIAL.md:93`, `:115–125`, `:1294`, `:1313`, `:1344`; the explainer template
   `explainer-article.md:102–108`; `overview-article.md:19`; `SYNOPSIS.md:3908` (Lay of
   the Land). Dated prose in `SYNOPSIS.md` that says “the result is now V4/C5” stays as
   written; the dated note in `epistemics.md` is how it is read.
7. **The site (jlevy/squares#255)**: the cards already derive from `epistemics.md`; add
   the count of current results at each level to each card so an empty top rung reads
   “`V5` formal, expert-reviewed: 0 results” rather than disappearing; give the `V`, `C`
   and `S` chips a `title` with the rung’s one-line meaning; the all-results filter
   keeps all six options; `test_overview` asserts the level counts, the chip titles
   against `rubric_levels`, and the `RESULTS.md` header sentences against the axis
   table. The epistemics document page renders from `epistemics.md` as it does now; check
   the tables and the `$…$` spans after the rewrite.
8. **A dedicated record template** for human oversight, `docs/project/reviews/` with the
   fields of §2.5, so the owner can write the T-060 record in one sitting.
9. **Data commit, then re-pin** (`release: re-pin DATA_REVISION to <sha> and re-stamp
   the atlas`, `build_known_best_atlas --update` with
   `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib`).
10. **Gates**: `packing-validate --records` after step 4 and again after step 5;
    `--edit` after step 6 and 7; `--push` once at the end.
    About 25 minutes of wall for the gate runs; the records tier is about 3.5 minutes
    each.

Cost: steps 1–3 about 6 agent-hours (two lanes, disjoint files); step 4 about 3; steps
5–6 about 3; step 7 about 4; steps 8–10 about 2. Seventeen to twenty agent-hours, six to
eight hours of wall with three lanes.

Old ratings need a dated note, not a rewrite: the note on each lowered result and the
one in `epistemics.md` are enough for a reader of a review from September to understand
what `V4/C5` meant when it was written.

## 6. Recommendation and Decisions

**Recommendation: Design A**, the owner’s design, with rung 3 renamed to carry the
lowered results honestly, attributes for distinct methods and third-party replay, and
the principle stated at the head of both ladders.
It is the only candidate that applies the owner’s no-blind-trust principle, and the
ratings it lowers are restored by records the project can write this week.

Decisions only the owner can make:

1. **Top rung at `C5` or `C6`?** Decided 2026-09-30: `C5`, defined as replayed here,
   open, and reviewed by at least two human experts (§2.4). (`C6` would have left rung 4
   as it is and applied the principle nowhere.)
2. **Does AI review count, and at which rung?** Recommended: it is a necessary condition
   at rung 4 on both axes and never sufficient; at rung 5 only the human formalization
   review counts. Alternative: AI review also admissible at 5 beside the human review,
   which changes nothing about who must sign.
3. **Can a same-project review reach the top rungs?** Partly decided: `C5` needs at
   least two human experts (statement of 2026-09-30). Open: must both be other than the
   formalization’s author, and must at least one be outside the project that produced
   the formalization? Recommended: yes to both.
   At `C3` and `C4`, same-project confirmation counts, with oversight on the confirming
   side. Alternative: admit the author as one of the two, or two project members, which
   makes `C5` reachable for this project’s own formalizations without an outside reader
   and weakens “reviewable by any other experts”.
4. **What does “expert” mean?** Open.
   Recommended: a named person who states, in the record, their competence in the proof
   assistant and in the mathematics; the record is what a reader can judge.
   Alternative: an allowlist in `epistemics.md`, which the owner maintains.
5. **What happens to T-060 now?** Recommended: `V3/C3/S5` on the stacked branch, with
   its `notes` stating the rung it held and the record it waits on; the owner writes the
   oversight record and the rung rises to `V4/C4` in the same pull request or the next.
   Alternative: hold the implementation until the record exists, so the published rating
   never dips; this delays the whole migration on one document.
6. **Who may serve as the human overseer at rung 4?** Recommended: the owner, or a named
   project member, or an external person; the record states the relation.
   Alternative: owner only.
7. **Can one oversight record cover a family of results sharing a checker?**
   Recommended: yes, enumerating the result ids and pinning the checker’s revision; a
   checker change re-opens the record.
   The rectangle-density certificates (T-044 to T-047), the $n = 17$ parent-angle
   certificates (T-032, T-038 to T-043) and the first-party weighted certificates (T-017
   to T-030) are the three natural families.
8. **Do existing owner-reviewed pull requests count as documentation?** Recommended: no;
   a dedicated record that may cite them.
   Alternative: a record that lists the pull requests and what was read in each, which
   is the same thing with less specificity.
9. **Must `C4`, or `C5`, include at least one third party?** Partly decided: `C5` is
   open to anyone and reviewed by two experts (statement of 2026-09-30); whether one of
   the two must be outside the project is decision 3. Open for `C4`: recommended no,
   with `third-party` as an attribute.
   Alternative: `C4` requires a third party, which lowers every first-party result to
   `C3` until another project replays it.
10. **$C \le V$ after composition?** Recommended: yes, enforced; T-014 becomes `V3/C3`.
11. **`N` and “distinct”.** Recommended: $N = 2$ adversarial AI reviews by distinct
    reviewer identities, where a separately prompted independent lane of the same model
    family counts as distinct; preferred, not required, that the families differ.
    Alternative: $N = 2$ with distinct families required, which leaves every current
    result one review short of 4 except T-060 if the source-intake review counts.
12. **Does a recorded, hash-bound execution performed here satisfy “replayed here”?**
    (`think-7khl`.) Recommended: yes at rungs 3 and 4; a fresh end-to-end replay from
    the repository is required at 5. Alternative: no, in which case T-060 is `C2` until
    `think-e2ot` lands.
13. **Does a kernel check rebuilt here count toward `C`?** (`think-74kl`.) Recommended:
    yes, as rung-3 confirmation evidence like any machine replay, and as the rung-5
    earner with the expert review; it is also a distinct method beside `zmx2`, recorded
    as the attribute.
14. **Dated note or rewritten history?** Recommended: a dated note in `epistemics.md`
    and on each lowered result; the September reviews and synopsis entries stand as
    written.
15. **One expert or two at `V5`?** Open.
    Recommended: one. `V` is the source’s own certification, and one independent expert
    attesting that the formal statement says what the claim says is what distinguishes a
    reviewed formalization from a kernel check; the second expert, the rebuild here and
    the open pointer are what `C5` counts as confirmation.
    Alternative: two at `V5` as well, which makes the two axes differ at the top only by
    the rebuild and the pointer.

## 7. Limits

- The human-oversight finding rests on the inventory of `docs/project/reviews/` and on
  `evidence.yaml`’s `reviewed_by` strings.
  Beads, handoffs, session records and pull requests on GitHub were not inventoried for
  owner review statements; by the owner’s own criterion they would not qualify, but the
  proposal did not read them.
- The adversarial-review inventory classified documents by what they say of themselves.
  It did not re-read the reviews’ mathematics or judge whether a review was in fact
  adversarial.
- No $n = 11$ geometry, Lean build or certificate was re-run for this proposal; the
  derivations use the register as it stands.
- The site branch (#255) was read, not rendered; the card and chip code was read at
  `e500e7807`.
- The cost estimates are planning figures, not measurements.

## References

- [`epistemics.md`](../../../../epistemics.md)
- [`check_results.py`](../../../../packing/devtools/check_results.py)
- [`results.schema.yaml`](../../../../packing/frontier/results.schema.yaml)
- [`frontier-evidence.schema.yaml`](../../../../packing/frontier/frontier-evidence.schema.yaml)
- [`results.yaml`](../../../../packing/frontier/results.yaml)
- [The `n = 11` census and capture contract review](../../reviews/review-2026-09-29-n11-optimality-census-contract.md)
- [The `n = 11` source intake review](../../reviews/review-2026-09-29-n11-optimality.md)
- [Plan: others’ results in the register](plan-2026-09-29-third-party-results-register.md)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
