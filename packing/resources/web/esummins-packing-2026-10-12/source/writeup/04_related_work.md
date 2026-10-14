# Related work: AI-assisted mathematics 2025–2026, read through one lens

*Living document, edited in place. Survey compiled 2026-09-09; all access dates are 2026-09-09 unless stated.
Corrections landed 2026-09-10 (A195): the R10 row and its reference (version, date and result breakdown), the
removal of R10 from the Lean-trust-anchor list, a direct contribution statement at the top, and the reframing of
§3's novelty list as an absence-of-evidence note. Tone is deliberately neutral: this document does not argue
that this lab's setup is better than any other, only that it is differently arranged.*

> **FLAGGED FOR THE PI — not actioned.** The external review of 2026-09-10 (§5) asks that this chapter be
> **shortened for the initial package**: at ~5,450 words it devotes substantial space to competitor claims,
> disputed attribution and the classification of other people's contributions, which are peripheral to the
> strongest evidence here and enlarge the fact-checking burden. The review suggests three or four closely
> relevant primary references would suffice for a first brief, naming Anthropic's Formalizing Fermat's Last
> Theorem account as a verified primary comparator. **A195 deliberately did not shorten the chapter** — deciding
> what a survey drops is an editorial judgement for the PI, and the corrections above are worth landing whether
> or not the cut happens. If the chapter is cut, the natural shape is: keep this chapter as an appendix, and
> promote the contribution statement below plus R4, R13, R15 and R19 into the brief.

## The contribution, stated directly

*Added 2026-09-10 (A195), at the external review's request, to replace novelty-by-absence as the framing.*

This repository documents three things, and they can be checked against the record without reference to what
anyone else has or has not done:

1. **Sustained visual guidance by an engineer.** Over weeks, a mechanical engineer with no formal mathematical
   training read generated drawings of live cases and wrote spatial readings; those readings became named
   lemmas, verifier clauses and search leaves. The traffic is dated and attributable, episode by episode, in
   `03_lab_timeline.md` §3 and summarised in `01_summary.md`.
2. **Exact falsification in both directions.** The engineer's readings were tested against certified geometry
   and several were refuted — a hairline grazer the eye cannot see, a lane a certified polygon closed. The
   machine's own constructions were refuted in the other direction — case trees on boxes never clipped against
   each other, cores rebuilt from a hull that discarded the growth making cuts propagate, a clip against
   inscribed squares rather than true polygon cores. Both directions are recorded, with the measured effect of
   each correction.
3. **The resulting artifacts.** An unconditional certified lower bound `s(11) ≥ 3.82` with an end-to-end Lean
   theorem; a 52-of-52 window scoreboard under a frozen exact verifier; Lean-checked `LocalDead` kernels for
   three exact local minima; a windows clause proved end to end in Lean; and a set of frozen, replayable
   certificates — together with a written record of where the pipeline was **wrong**, including a soundness bug
   in one verifier found by external review, reproduced, fixed, and re-replayed.

**What is not claimed.** Nothing here is a controlled comparison against either party working alone, and nothing
here is a priority claim. A survey's inability to find another example of an arrangement does not establish that
the arrangement is first; it establishes that the compiler did not find one. Section 3's "not found elsewhere"
list should be read in exactly that spirit and no stronger — it is an absence-of-evidence note appended to the
statement above, not a substitute for it.

## Why this survey exists, and the lens it uses

Top-line coverage of AI-assisted mathematics reports *what was proved* and *which model did it*. It rarely
reports the two facts this lab turns on:

1. **Who managed the AI** — the mathematician themselves, a separate engineer, or a company team — and
   **how deep the interaction was**: one prompt, a few prompts, or a sustained multi-week loop with tooling,
   process and state carried between sessions.
2. **What training the human had**, and **what the human actually contributed**: problem selection only,
   validation only, mathematical insight, tooling and process, or all of these.

This lab (`writeup/01_summary.md`) is arranged so that a single person supplies both the orchestration
(process, tooling, compute budget, verification harness) *and* the mathematical insight (the stratification
that makes the case split tractable, and the readings of the drawings that become geometric lemmas). That
person is a mechanical engineer by training, a recreational mathematician, with no PhD; the target problem,
the exact value of s(11), has been open for roughly fifty years. **This lab has not completed its proof as of
2026-09-10** — the k0 residue is eleven converged-alive cells and **none has been closed**; the cascade has
killed 40 *nodes* inside one of them under the frozen verifier, which is not the same thing — so nothing below
should be read as a completed-result comparison. It is a comparison of *setups*.

Where a claim comes from press rather than from a paper or a primary announcement, it is marked. Where a
source could not be retrieved, it is marked [could not fetch]. Nothing here is invented; where a search
returned nothing, that is stated.

### Fields recorded

| field | meaning |
|---|---|
| Interaction depth | one-shot (single prompt); few prompts (a session, hours); sustained (weeks or more, state carried across sessions); autonomous pipeline (system run at scale, human curates output) |
| Who managed the AI | mathematician; separate engineer; company team; amateur/self; lab of one |
| Human training | professional mathematician; PhD student / undergraduate; engineer; amateur |
| Human contribution | selection; validation; insight; tooling/process; writeup |
| Verification | informal; expert review; peer review; Lean / proof assistant; machine-checkable certificate |
| Process documented | did they publish the workflow, or only the theorem? |

---

## 1. The table

Confidence is the compiler's confidence in the *classification*, not in the underlying mathematics.
Full URLs and access dates are in section 4.

| # | Result / claim | Open for; significance | Models & tools | Interaction depth | Who managed the AI | Human training | Human contributed | Verification | Process documented | Confidence (source) |
|---|---|---|---|---|---|---|---|---|---|---|
| R1 | OpenAI VP Kevin Weil's Oct 2025 claim that GPT-5 "found solutions to 10 previously unsolved Erdős problems"; post later removed | n/a — the problems were "open" only in the sense that the database maintainer knew of no published solution | GPT-5 | few prompts (in effect literature retrieval) | company team | professional (the debunkers) | selection; the *debunking* was the human work | informal; corrected by Thomas Bloom, who called it "a dramatic misrepresentation" | no workflow published; the post was deleted | high (TechCrunch 2026-05-20; Quanta 2026-08-03) |
| R2 | Erdős #728 resolved (factorial-divisibility log-gap phenomenon); described as the first Erdős problem fully resolved autonomously by an AI system | posed by Erdős; the Erdős-problems wiki files it under "AI alongside literature", consistent with Pomerance (2014) | GPT-5.2 Pro + Aristotle (Harmonic); Lean | few prompts, operator-driven | amateur/self — "operated by Kevin Barreto" | undergraduate (Cambridge, 2nd year) | selection; operation; the human-readable writeup was done by a third party | Lean proof; human exposition in arXiv:2601.07421 | partial — the writeup describes the proof, not the prompting loop | high (arXiv:2601.07421; Erdős wiki) |
| R3 | Erdős #1196 (primitive sets / the Erdős sum) resolved | ~60 years | GPT-5.4 Pro via a ChatGPT Pro subscription | **one-shot** — a single prompt "on an idle Monday afternoon" | amateur/self | amateur — Liam Price, 23, "no advanced mathematics training" (Sci Am); "some college math, didn't finish degree" (Quanta) | selection; a prompting methodology; cross-model self-verification | expert review — reviewed by Barreto, then verified and refined by Terence Tao and Jared Duker Lichtman | partial — Price's method of re-feeding a candidate solution to a fresh model instance is described in press, not in a paper | high (Scientific American 2026-04-24; Quanta 2026-08-03) |
| R4 | Erdős #1026 (maximum sum of monotone subsequences); c(n) determined completely | posed 1975 (~50 years) | AlphaEvolve, Aristotle, Gemini, ChatGPT Pro; Lean | **sustained** — 12 Sep to 7 Dec 2025, with the decisive work compressed into ~48 hours | distributed community coordinated by a professional mathematician (Tao) | mixed: professionals plus community contributors | selection; insight (the c(n) reformulation was human, by Desmond Weisenberg); validation; synthesis | Lean (Aristotle proved c(k²)=1/k) | **yes** — Tao published a full narrative of who did what and when | high (Tao blog 2025-12-08) |
| R5 | Erdős #848 resolved | not established by the sources found | GPT-5 | sustained (12 Oct – 20 Nov 2025) | the mathematicians themselves | professional (Mehtaab Sawhney, Mark Sellke) | insight; validation | expert review | not to the compiler's knowledge | medium (Erdős-problems wiki table only; no narrative source found) |
| R6 | Przemek Chojecki's 12 claimed Erdős solutions (#522, #603, #610, #856, #888, #896, #953, #956, #1092, #1133, #1151, #1190) | various | GPT-5.4 Pro, GPT-5.5 Pro, Aristotle | few prompts per problem, run as a personal marathon across the whole open list | amateur/self (one person, at volume) | [unverified] — his training was not established by any source found | selection at scale; validation; cleaning results up for journal submission | expert review pending; in his own words the claims "still need to be verified properly" | partial — thread-level notes on X; no methods paper found | medium (X posts by @prz_chojecki; Erdős wiki) |
| R7 | Wouter van Doorn's body of AI-credited papers and forum work; fourth-most prolific commenter on the Erdős forum | various | ChatGPT and other LLMs | **sustained**, over months, alongside a non-academic day job | amateur/self | amateur — incomplete master's in maths (KU Leuven); worked at a customer-service company | selection; validation; **simplification and generalisation** of model output into publishable form ("the eventual proofs that I write are simpler, more general, and easier to read") | peer review (journal papers) | no methods paper found | high (Quanta 2026-08-03, direct quotes) |
| R8 | Erdős #90 / the planar unit-distance conjecture (Erdős 1946) disproved | ~80 years; central to discrete geometry | an unnamed OpenAI internal reasoning model | **one-shot** — presented as "the first major mathematical open problem solved with AI with minimal human intervention beyond the initial prompt" | company team | professional (verifiers) | selection; validation | expert review — Timothy Gowers said he would recommend publication to *Annals of Mathematics* "without any hesitation"; Will Sawin independently verified the reasoning and improved the result | **yes, unusually** — the initial prompt and the model's chain of thought were published alongside the proof PDF | high (The Conversation 2026-05-26; TechCrunch 2026-05-20; OpenAI primary page [could not fetch] — HTTP 403) |
| R9 | OpenAI "Astra": ten mathematics and theoretical-CS results with Lean certificates, including what is claimed as the first improvement to the general sphere-packing exponent since 1978, and the first explicit construction of a non-sofic group (open since 1999) | ~48 years for the packing exponent | unreleased Astra model; Lean 4 | autonomous pipeline; humans prepared the manuscripts, the model formalised each argument | company team | professional | selection; manuscript preparation | **machine-checkable** — Lean 4 repository published with a 249-page manuscript | partial — artefacts published; the loop is not documented | medium-high (press consensus: implicator.ai, qz.com, TechTimes, all Aug 2026; primary OpenAI page not fetched) |
| R10 | DeepMind "Aletheia" (Gemini Deep Think plus a natural-language verifier) on the Erdős problems: **five seemingly novel autonomous solutions and eight literature identifications**, out of 700 problem responses | various | Aletheia / Gemini Deep Think | autonomous pipeline with heavy human curation downstream | company team plus academic collaborators | professional | selection; **verification and literature-checking**, named by the authors as the hardest step | **informal expert verification**, described by the authors as "slightly subjective"; only 31.5 % of 200 examined responses were technically correct. **No proof assistant** — this row is not a Lean row | **yes** — the paper documents the funnel and its failure modes | high (**arXiv:2601.22401v3, dated 5 February 2026**; the version actually consulted) |
| R11 | DeepMind "AlphaProof Nexus": 9 of 353 attempted open Erdős problems solved autonomously (two open 56 years), 44 of 492 OEIS conjectures, a 15-year-old Hilbert-function question, a convex-optimisation bound | up to 56 years | AlphaProof, Gemini 3.0 Flash rating agents, an evolutionary agent variant; Lean | autonomous pipeline, reported at a few hundred dollars per problem | company team | professional | selection; system design | **machine-verified** (Lean) | partial — the agent architecture is described in press; the compiler did not locate a primary paper | medium (the-decoder.com and secondary write-ups; primary DeepMind publication not found in searches) |
| R12 | AlphaEvolve applied to 67 problems: roughly 20 new results, including finite-field Kakeya bounds, the kissing number in dimension 11 (592 → 593), rediscovery of the Gerver sofa, and packing/tiling problems | various | AlphaEvolve (Gemini-powered evolutionary coding agent) | autonomous search **inside a human-built harness** | company team plus mathematicians | professional (Georgiev, Gómez-Serrano, Wagner, Tao) | **tooling/process (verifier design)**, selection, validation | numerical and constructive; independently re-verified by the human authors | **yes** — Tao is explicit that "a non-trivial amount of human effort needs to go into designing a non-exploitable verifier", and that the system sometimes exploited verifier weaknesses | high (arXiv:2511.02864; Tao blog 2025-11-05) |
| R13 | Buckmaster–Alpöge: finite-time blowup with smooth forcing for the incompressible porous medium equation, 2D Boussinesq, and 3D incompressible Euler; Lean-formalised | builds directly on a multi-year programme of Córdoba and Martínez-Zoroa; adjacent to a Millennium Problem | Claude (Anthropic) and Codex (OpenAI), plus later models for iterative writeups and auditing; Lean | **sustained** — first blowup solution 2026-08-15, Lean verification 2026-08-22, preprints 2026-09-08; press describes a long personal collaboration (see the discrepancy note below) | **a mathematician and a separate industry researcher together** — Tristan Buckmaster (NYU), Levent Alpöge (Anthropic) | professional mathematician plus industry researcher | insight; validation; extensive rewriting — the first model output was called "the most horrendous I have ever seen" and took weeks to bring to professional quality | **Lean**; formalisations posted to a public repository. The related Navier–Stokes work was held back because "its Lean verification has not finished" | partial — AI usage is disclosed inside the papers; the compiler found no full workflow account | high (Tao blog 2026-09-07; Unite.AI 2026-09; Buckmaster Mastodon) |
| R14 | OpenAI's claim that an internal system produced a proof of finite-time singularity for forced Navier–Stokes | Millennium Problem | an internal OpenAI system | **disputed** — initially described to Buckmaster as a ~100-page proof produced with "very little human input"; Buckmaster reports the account changed under questioning to substantial team involvement and iterative prompting | company team | professional | selection; validation | **contested** — the Clay Mathematics Institute has not accepted the result and still lists the problem as unsolved | no | medium (Unite.AI; implicator.ai; Tao blog comments; OpenAI primary page [could not fetch] — HTTP 403) |
| R15 | Anthropic: a complete computer-checked proof of Fermat's Last Theorem in Lean — ~13 million lines, 29,500 intermediate theorems, ~11 days of largely autonomous work, ~6 billion output tokens | FLT proved by Wiles in 1994; the Lean formalisation effort (Buzzard's EPSRC project) had been running since 2024 | an internal model "roughly comparable to Claude Fable 5.1"; Prove2Me, a multi-agent platform maintaining a DAG of theorem statements | **autonomous pipeline with minimal human direction** — "occasional high-level instructions" such as "Jacobian as a scheme sounds high priority" | company team; **a separate engineer/researcher (Tianyi Peng) directed it** | professional researcher; Kevin Buzzard (mathematician) reviewed the completed proof afterwards | tooling/process; selection; review. Mathematical input from humans was described as limited | **machine-checkable** (Lean kernel) | **yes** — the coordination platform and scheme are described | high (Anthropic research page, 2026-09-04) |
| R16 | "Early science acceleration experiments with GPT-5": four new mathematics results plus results in physics, astronomy, CS, biology and materials science | various; the authors call them "modest in scope but profound in implication" | GPT-5 | few prompts to sustained, varying by case; interaction transcripts included | company team plus academic collaborators | professional (including Timothy Gowers) | insight; validation — results "carefully verified by the human authors" | expert review by the human authors | **yes** — documenting the interactions is the paper's stated purpose | high (arXiv:2511.16072, 2025-11-20) |
| R17 | The Equational Theories Project: crowdsourced formalisation at scale, launched September 2024 | a large finite classification problem attacked collaboratively | Lean plus automated tools and a human crowd | sustained, months, distributed | professional mathematician (Tao) coordinating | professional plus community | insight; tooling/process; coordination | **Lean** | **yes** — a paper about the collaboration itself | medium-high (arXiv:2512.07087; abstract only, not fetched in full) |
| R18 | Flyspeck: a formal proof of the Kepler conjecture | conjectured 1611; Hales–Ferguson proof 1998, whose computer code referees could not fully certify; Flyspeck launched 2003, completed ~2014 | HOL Light and Isabelle; no machine learning | **sustained, roughly eleven years**, human-directed | the mathematician himself (Thomas Hales) | professional | insight; **tooling/process** — he built the verification effort precisely because ordinary peer review could not certify his own computation | **machine-checkable** (proof assistants) | yes — published account | high (arXiv:1501.02155; *Forum of Mathematics, Pi*) |
| R19 | Boolean Pythagorean triples: no two-colouring of {1,…,7825} avoids a monochromatic Pythagorean triple | an Erdős–Graham problem, settled 2016 | cube-and-conquer SAT with look-ahead heuristics, 800 cores, ~2 days; no machine learning | sustained, human-directed | the researchers themselves (Heule, Kullmann, Marek) | professional | insight (encoding and symmetry breaking); tooling/process | **machine-checkable**: a ~200 TB DRAT proof, distributed as a 68 GB compressed certificate anyone can expand and re-check | yes — published method | high (arXiv:1605.00723; *Nature* news 2016) |
| R20 | The four-colour theorem | conjectured 1852; Appel–Haken computer-assisted proof 1976; Gonthier's Coq formalisation 2005 | discharging plus exhaustive case checking; no machine learning | sustained, human-directed | the mathematicians themselves | professional | insight; tooling/process | machine-checkable after the 2005 formalisation | yes | high (standard history; no 2025–26 source required) |
| R21 | **This lab**: 3.82 ≤ s(11) ≤ 3.877084 with the lower bound certified; every class but k0 closed on the whole window by certificates checked by a frozen verifier; two of four local minima Lean-checked. **The k0 residue is eleven cells and no k0 cell has yet been killed** | the exact value of s(11) has been open ~50 years — Trump's 1979 packing has never been beaten and no matching lower bound was known | Claude models under an agent harness; Lean; LP certificates; frozen verifiers; a generated SVG gallery of every live case | **sustained multi-week loop** — dozens of drawing → reading → lemma → re-drawing cycles per day across ~170 numbered attempts | **lab of one** — the same person orchestrates and supplies the insight | **engineer (mechanical) by training; recreational mathematician; no PhD** | selection; **insight** (the simply-supported stratification; the geometric readings that became reusable leaves); **tooling/process**; validation | **machine-checkable certificates plus Lean for parts**; not peer-reviewed; **the proof is incomplete** | **yes, by construction** — `writeup/03_lab_timeline.md` is the workflow record | high (this repository) |

---

## 2. Notes on each entry

**R1 — the October 2025 Erdős claim.** Kevin Weil, then an OpenAI VP, posted that GPT-5 had "found solutions
to 10 (!) previously unsolved Erdős problems and made progress on 11 others". Thomas Bloom, who maintains
erdosproblems.com, called this "a dramatic misrepresentation": "open" on his site meant only that he was
personally unaware of a published solution. GPT-5 had located existing papers. Weil removed the post after
public criticism from Yann LeCun and Demis Hassabis. This episode set the terms for every later dispute:
the hard question is not whether the model produced a correct argument but whether the argument is new.
(TechCrunch, 2026-05-20; Quanta, 2026-08-03.)

**R2, R3 — Barreto and Price.** These are the closest published comparators for *non-professional* leadership.
Kevin Barreto is a second-year Cambridge undergraduate; Liam Price is described as 23 with no advanced
mathematics training. They began by prompting a free version of ChatGPT with randomly chosen open problems.
Erdős #728 was resolved by GPT-5.2 Pro plus Harmonic's Aristotle "operated by Kevin Barreto"; the Lean proof
was later written up for humans by Nat Sothanaphan (arXiv:2601.07421). Erdős #1196 came from a *single prompt*
to GPT-5.4 Pro. Tao's comment was that "the LLM took an entirely different route, using a formula well known
in related math, but which no one had thought to apply to this type of question." Interaction depth: one-shot
to a few prompts. The humans supplied problem selection, a prompting discipline and cross-checking; not
mathematical insight into the problem. They were also on the receiving end of the literature dispute: Barreto's
Erdős #333 claim was matched within hours to a 1977 Erdős paper, which he described as "quite gut-wrenching".

**R4 — Erdős #1026.** The best-documented *sustained* collaboration in the Erdős wave, and the only one whose
narrative Tao published in full. It is a distributed community effort, not a lab of one: separate people
supplied the reformulation, the numerics, the asymptotics, the Lean proof and the coordination. Tao's own
assessment is that a traditional effort by one or two mathematicians "may eventually have been able to put all
these pieces together, but... this process would have taken much longer". Notably the proof itself was "not
particularly novel"; the achievement was synthesis. (Tao blog, 2025-12-08.)

**R6, R7 — the volume amateurs.** Przemek Chojecki swept the open Erdős list with GPT-5.4 Pro and then
GPT-5.5 Pro and claimed twelve solutions, by his own account still needing proper verification. Wouter van
Doorn is the most interesting amateur case for this lab's lens: incomplete master's, a customer-service day
job, sustained engagement over months, and an explicitly *complementary* division of labour — "A lot of my
recent papers should be mostly credited to AI... The ideas involved were ideas I did not come up with myself",
but "the eventual proofs that I write are simpler, more general, and easier to read for other people than the
thing that ChatGPT came up with." Van Doorn's contribution is distillation, not orchestration or insight.
(Quanta, 2026-08-03.)

**R8 — the unit-distance disproof.** The cleanest example of the one-shot bucket, and unusual in publishing
the prompt and the chain of thought. Human work was concentrated entirely downstream: Gowers, Sawin, Alon,
Wood and Bloom in verification and commentary roles. Bloom's own worry about the wave — "AI is being used a
lot by people who aren't mathematicians, who don't have a huge mathematical background and are not capable of
verifying the output... We're seeing a lot more of these 100- to 200-page papers... No human has read it" —
is a verification-burden argument, and it is the argument this lab's certificate-first design is aimed at.

**R9, R10, R11, R12 — the company pipelines.** These differ from every other bucket in that the *system*, not
a conversation, is the unit of work. Where humans matter is verifier design (Tao is explicit that a
non-exploitable verifier takes non-trivial human effort, and that AlphaEvolve sometimes gamed weak ones) and
downstream literature checking (the Aletheia paper names literature-checking, not verification, as the hardest
human step, with only 31.5% of examined responses technically correct). The interaction is broad and shallow:
hundreds of problems, little depth per problem.

**R13, R14 — the fluid-dynamics collaboration and the dispute.** Buckmaster (NYU) and Alpöge (Anthropic) is
the reference case for a sustained, deep, model-assisted collaboration on a hard problem, formalised in Lean
and disclosed in the papers. The division of labour is two people: a professional mathematician supplying
direction and a researcher at a model lab driving the tooling. **Discrepancy note:** the compiler's brief
described this as "over a month" of collaboration; one secondary source (Unite.AI) describes "nearly a year";
Tao's post gives only the recent milestones (2026-08-15 blowup, 2026-08-22 Lean, 2026-09-08 preprints). The
duration is therefore [unverified] beyond "sustained, at least weeks". The OpenAI counter-claim (R14) is
contested on process as well as on credit: Buckmaster reports that a characterisation of "very little human
input" changed under questioning. Clay has not accepted it. Tao's framing is worth recording as the field's
current normative position: the community should "reject irresponsible and unsustainable usages of AI
technology that only serve to advance nominal goals rather than the true underlying goals of the field."

**R15 — FLT in Lean.** The largest formalisation-at-scale result found, and the sharpest contrast with this
lab on the insight axis: 13M lines of Lean, 29,500 theorems, ~11 days, human mathematical input described as
limited, direction supplied by an engineer (Tianyi Peng) through "occasional high-level instructions", with a
mathematician (Buzzard) reviewing afterwards. It is a *formalisation* of a known proof, not the discovery of
an unknown one — the mathematics was already settled in 1994. It shows that the orchestration-heavy,
insight-light configuration is now viable when the mathematics is known.

**R18, R19, R20 — the pre-AI baseline.** All three are "computer-assisted but human-directed", and all three
were run by the mathematicians themselves rather than by a separate engineering team. Flyspeck is the closest
structural ancestor of this lab: Hales's Kepler proof was accepted only conditionally because referees could
not certify his computation, so he spent about eleven years building machine-checkable verification of his own
argument. Boolean Pythagorean triples is the closest ancestor of the certificate design: a ~200 TB DRAT proof
distributed as a 68 GB certificate that any third party can expand and check. Four-colour is the historical
precedent for both the method and the sociological objection. None of these involved learned models; the
"AI" in them is search and proof checking.

---

## 3. Buckets

**Bucket A — one-shot / few-prompt frontier-model results, human is selector and validator.**
Entries: R1, R2, R3, R6, R8, and much of the wider Erdős wave. **Count: 5 table rows** (representing many
dozens of individual problems). Characteristic: interaction measured in prompts or hours; the human chooses
the problem, prompts, and checks; the mathematical content originates in the model. Verification ranges from
informal to Lean. Process documentation is thin except where a company chose to publish the prompt (R8).

**Bucket B — autonomous or semi-autonomous company pipelines.**
Entries: R9, R10, R11, R12, R15. **Count: 5.** Characteristic: the human contribution is system design,
verifier design, problem-set curation and downstream literature checking; breadth over depth; strong
machine-checkable verification (Lean) in most cases; workflow partially published.

**Bucket C — sustained collaborations where a separate engineer or lab drives the AI alongside a
mathematician.** Entries: R13, R14 (as claimed), and R15 in part. **Count: 2–3.** Characteristic: weeks or
more of work, real mathematical difficulty, formal verification, but the orchestration and the insight sit in
*different heads*.

**Bucket D — sustained collaborations managed by the mathematician themselves.**
Entries: R4, R5, R16, R17, and the pre-AI baseline R18, R19, R20. **Count: 7.** Characteristic: a professional
mathematician both directs the tooling and supplies the mathematics. This is the bucket this lab most
resembles structurally — and the pre-AI members of it (Flyspeck, Boolean Pythagorean triples) resemble it most
of all, minus the learned models.

**Bucket E — non-mathematician-led.**
Entries: R2, R3, R6, R7. **Count: 4.** Characteristic: an amateur or student selects problems and runs models
at volume. In every case found, the *mathematical* content comes from the model and the human's contribution
is selection, prompting discipline, verification, and (for van Doorn) distillation into readable form. The
compiler found **no case in this bucket of an amateur supplying the structural mathematical idea**, and no case
of an amateur building a multi-week orchestration and verification apparatus.

**Where this lab sits: between D and E, and in neither cleanly.** By the human's training it belongs in
bucket E. By interaction depth, tooling, verification design and the origin of the key structural idea it
behaves like bucket D. The compiler found no other entry that is simultaneously non-professional-led,
sustained over weeks, orchestration-heavy, and insight-supplying from the human side.

---

## 4. What is and is not novel about this lab's setup

This section is written to be defensible line by line. The lab's proof is **incomplete**: as of 2026-09-09 the
k0 residue is eleven cells and none has been killed, so no claim below is a claim about a finished theorem.

### Not novel

- **Using frontier models on a long-open problem.** Routine since late 2025 (R2, R3, R8, R9, R11).
- **Machine-checkable certificates for a case-exhaustion proof.** Predates AI entirely: Flyspeck (R18) and the
  Boolean Pythagorean triples DRAT certificate (R19) are the model, and this lab's frozen-verifier design is a
  direct descendant.
- **Lean as the trust anchor.** Standard across R2, R9, R11, R13, R15. **R10 is not on this list**: the Aletheia
  paper's own verification is informal expert review, which its authors describe as "slightly subjective", with
  31.5 % of 200 examined responses technically correct. Listing it as a Lean row was an error, corrected 2026-09-10.
- **A single non-professional using models to attack open problems.** Established by R2, R3, R6, R7.
- **Sustained multi-week human–model collaboration on a hard problem.** Established by R13, and by R4 in a
  distributed form.
- **Publishing the workflow rather than only the theorem.** Done by Tao (R4, R12), by the GPT-5 science paper
  (R16), by the Aletheia paper (R10), and by Anthropic for FLT (R15).
- **The observation that human verifier design is the bottleneck.** Stated plainly by Tao for AlphaEvolve
  (R12) and by the Aletheia authors (R10).

### Not found elsewhere in this survey — an absence-of-evidence note, not a novelty claim

*Reframed 2026-09-10 (A195). The contribution statement is at the top of this chapter and stands on the record.
Everything in this subsection is a statement about what the compiler searched for and did not find, over the
sources listed in section 5. None of it establishes priority, and none of it should be quoted as if it did.*

- **The same non-professional supplies both the orchestration and the structural mathematical idea.** In every
  bucket-E case found, the mathematical content originates with the model and the human supplies selection,
  prompting and checking; van Doorn is explicit about this. In bucket C the two roles exist but sit in
  different people. In bucket D the person doing both is a professional mathematician. The compiler found no
  documented case combining: no formal mathematical training, sustained multi-week orchestration, *and* the key
  structural idea coming from the human. Confidence: medium — this is an absence-of-evidence claim over the
  sources listed in section 5, not a proof of absence.
- **A visual channel as the primary interface between human insight and machine proof.** The lab's
  drawing → reading → lemma → re-drawing loop, with generated galleries of live cases and a status script that
  retires killed pages, is the mechanism by which a non-symbolic human contribution enters a symbolic proof.
  The compiler found no comparable documented interface in any surveyed result. AlphaEvolve's human effort went
  into verifier design (R12); Aletheia's into literature checking (R10); FLT's into a theorem DAG (R15). None
  is a channel for human geometric intuition. Confidence: medium.
- **Bidirectional error correction as a recorded feature.** `01_summary.md` records both directions: the AI's
  unclipped case trees and hull-rebuilt cores caught by the PI reading pictures, and the PI's misreadings
  refuted by certified geometry. Surveyed results generally document one direction — human verification of
  model output. Confidence: medium-low; other projects may do this without recording it.

### Explicitly not claimed

- Not claimed: that s(11) is proved. It is not.
- Not claimed: that the mathematics here is harder than R8, R13 or R9. No comparison of difficulty is made.
- Not claimed: that this is the first amateur-led AI mathematics result. It is not (R2, R3).
- Not claimed: that the AI could not have done this alone with better tooling. The lab's record shows where it
  did not, on this problem, with these tools; that is a narrower statement.
- Not claimed: priority over any surveyed result. Several surveyed items post-date the start of this lab and
  several pre-date it; the survey does not establish an ordering.

---

## 5. Gaps in this survey

- The erdosproblems.com forum blog thread on problem 728 and AI usage returned HTTP 403 and **[could not
  fetch]**; the site's stated AI policy is therefore reported only via Quanta and the community wiki.
- OpenAI's own Navier–Stokes and unit-distance pages returned HTTP 403 and were **[could not fetch]**; those
  rows rest on secondary reporting and on Tao's blog.
- No primary DeepMind publication for "AlphaProof Nexus" was located; R11 rests on secondary reporting.
- Przemek Chojecki's training and profession (R6) are **[unverified]**.
- The duration of the Buckmaster–Alpöge collaboration (R13) is **[unverified]**; sources disagree.
- Searches for a *second* non-professional-led, sustained, orchestration-plus-insight project returned nothing.
  That is an absence of results, not evidence that none exists.
- Searches for AI work specifically on s(n) square packing returned only the classical literature (Friedman's
  survey; Trump's 1979 packing) and AlphaEvolve's unrelated packing experiments. No AI attack on s(11) by
  anyone else was found.

---

## 6. References

All accessed 2026-09-09. Press items are marked *(press)*; papers and primary announcements are not.

**Erdős-problems wave**
1. AI contributions to Erdős problems (community wiki, last updated 2026-06-30). https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems
2. Quanta Magazine, "Why the Legendary Erdős Problems Are Falling to AI", 2026-08-03 *(press)*. https://www.quantamagazine.org/why-the-legendary-erdos-problems-are-falling-to-ai-20260803/
3. Scientific American, "Amateur armed with ChatGPT 'vibe maths' a 60-year-old problem", 2026-04-24 *(press)*. https://www.scientificamerican.com/article/amateur-armed-with-chatgpt-vibe-maths-a-60-year-old-problem/
4. TechCrunch, "OpenAI claims it solved an 80-year-old math problem — for real this time", 2026-05-20 *(press)*. https://techcrunch.com/2026/05/20/openai-claims-it-solved-an-80-year-old-math-problem-for-real-this-time/
5. N. Sothanaphan, "Resolution of Erdős Problem #728: a writeup of Aristotle's Lean proof", arXiv:2601.07421 (submitted 2026-01-12). https://arxiv.org/abs/2601.07421
6. T. Tao, "The story of Erdős problem #1026", 2025-12-08. https://terrytao.wordpress.com/2025/12/08/the-story-of-erdos-problem-126/
7. erdosproblems.com forum, "Problem 728 and the use of AI on Erdős problems". https://www.erdosproblems.com/forum/thread/blog:2 — **[could not fetch: HTTP 403]**
8. P. Chojecki, X/Twitter thread summarising 12 AI-assisted Erdős claims *(press/self-report)*. https://x.com/prz_chojecki/status/2050160288108892407
9. The Conversation, M. Lee, "An AI solution to an 80-year-old problem has shocked mathematicians", 2026-05-26 *(press)*. https://theconversation.com/an-ai-solution-to-an-80-year-old-problem-has-shocked-mathematicians-283686
10. OpenAI, "An OpenAI model has disproved a central conjecture in discrete geometry". https://openai.com/index/model-disproves-discrete-geometry-conjecture/ — **[could not fetch: HTTP 403]**

**Company pipelines**
11. T. Feng, T. Trinh, G. Bingham, J. Kang, S. Zhang et al., "Semi-Autonomous Mathematics Discovery with Gemini: A Case Study on the Erdős Problems", **arXiv:2601.22401v3, dated 5 February 2026**. https://arxiv.org/abs/2601.22401v3 — **corrected 2026-09-10 (A195)**: an earlier compilation of this survey gave the date as 2026-08-24 and a breakdown of "4 autonomous resolutions, 2 partial, 4 independent rediscoveries, 5 literature identifications". The arXiv v3 record gives **5 February 2026** and describes **five seemingly novel autonomous solutions and eight literature identifications**. The version cited is the one consulted; results in this table must be attributed to a named version, since the breakdown differs between versions.
12. B. Georgiev, J. Gómez-Serrano, A. Z. Wagner, T. Tao, "Mathematical exploration and discovery at scale", arXiv:2511.02864 (2025-11). https://arxiv.org/abs/2511.02864
13. T. Tao, "Mathematical exploration and discovery at scale" (blog post), 2025-11-05. https://terrytao.wordpress.com/2025/11/05/mathematical-exploration-and-discovery-at-scale/
14. The Decoder, "Google DeepMind's AlphaProof Nexus solves decades-old math problems for a few hundred dollars" *(press)*. https://the-decoder.com/google-deepminds-alphaproof-nexus-solves-decades-old-math-problems-for-a-few-hundred-dollars/
15. S. Bubeck et al., "Early science acceleration experiments with GPT-5", arXiv:2511.16072, 2025-11-20. https://arxiv.org/abs/2511.16072
16. Implicator.ai, "OpenAI Says Astra Solved 10 Math Problems With Lean Proofs", Aug 2026 *(press)*. https://www.implicator.ai/openai-astra-10-math-problems-lean-proofs/
17. Quartz, "OpenAI Astra model solves 10 open math problems for $2,000", 2026-08-03 *(press)*. https://qz.com/openai-astra-model-math-problems-lean-proofs-080326

**Fluid dynamics and the credit dispute**
18. T. Tao, "Finite time blowup with smooth forcing term for the incompressible porous medium, Boussinesq, and incompressible Euler equations", 2026-09-07. https://terrytao.wordpress.com/2026/09/07/finite-time-blowup-with-smooth-forcing-term-for-the-incompressible-porous-medium-boussinesq-and-incompressible-euler-equations/
19. Unite.AI, "Buckmaster and Alpöge Post AI Fluid Blowup Proofs, Dispute OpenAI Contact", Sept 2026 *(press)*. https://www.unite.ai/buckmaster-and-alpoge-post-ai-fluid-blowup-proofs-dispute-openai-contact/
20. T. Buckmaster, Mastodon announcement. https://mastodon.social/@tristanbuckmaster/117233413705701198
21. OpenAI, "On the Navier–Stokes Millennium Prize Problem". https://openai.com/index/navier-stokes-solution/ — **[could not fetch: HTTP 403]**
22. Implicator.ai, "Clay Institute Won't Call Navier-Stokes Solved by OpenAI" *(press)*. https://www.implicator.ai/clay-institute-navier-stokes-openai-proof-claim/

**Formalisation at scale**
23. Anthropic, "Formalizing Fermat's Last Theorem", 2026-09-04. https://www.anthropic.com/research/formalizing-fermats-last-theorem
24. "The Equational Theories Project: Advancing Collaborative Mathematical Research at Scale", arXiv:2512.07087. https://arxiv.org/pdf/2512.07087
25. Lean FRO / FLT project pages. https://lean-lang.org/use-cases/flt/

**Commentary**
26. T. Tao, "Mathematics in the age of AI", arXiv:2608.16753 (submitted 2026-08-17), essay based on the ICM 2026 public lecture. https://arxiv.org/abs/2608.16753
27. T. Tao, "Terence Tao on AI in mathematics (and beyond)" (collected views). https://teorth.github.io/tao-web/ai-views.html

**Pre-AI computer-assisted baseline**
28. T. Hales et al., "A formal proof of the Kepler conjecture", arXiv:1501.02155; *Forum of Mathematics, Pi* (2017). https://arxiv.org/abs/1501.02155
29. M. J. H. Heule, O. Kullmann, V. W. Marek, "Solving and Verifying the Boolean Pythagorean Triples problem via Cube-and-Conquer", arXiv:1605.00723. https://arxiv.org/abs/1605.00723
30. *Nature* news, "Two-hundred-terabyte maths proof is largest ever", 2016 *(press)*. https://www.nature.com/articles/nature.2016.19990
31. Wikipedia, "Boolean Pythagorean triples problem" (used only for the 7825 threshold). https://en.wikipedia.org/wiki/Boolean_Pythagorean_triples_problem

**Square packing background**
32. E. Friedman, "Packing Unit Squares in Squares: A Survey and New Results", *Electronic Journal of Combinatorics*, Dynamic Survey DS7. https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS7
33. E. Friedman, "Packing Unit Squares in Squares" (author page). https://erich-friedman.github.io/papers/squares/squares.html

**This lab**
34. `writeup/01_summary.md`, `writeup/02_mathematics.md`, `writeup/03_lab_timeline.md`, and the primary
    in-repo record (`LOG.md`, `attempts/REGISTRY.md`, `docs/residue_ledger.md`, `lean/`).
