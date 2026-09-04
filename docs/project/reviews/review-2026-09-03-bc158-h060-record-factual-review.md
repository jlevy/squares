# BC-158 — factual review of the H-060 / exp-058 records against their sources

## Provenance and installation

This document is the review deliverable of BC-158, the factual review of the H-060 and
exp-058 records against their sources, written on 2026-09-03 in the agenda-016 ten-hour
run. Its author wrote only to `scratchpad/bc158-record-review/` -- a container-local
directory outside the repository, which does not survive the session -- and modified no
repository file.
It is installed here so that the evidence the records cite outlives that
directory.

The source was `583` lines with SHA-256
`35d418720e792779b8fc540e8a2abd5cca1b5ee1ccebb1b8f3c6fe157b02e7bd`, and that hash names
the scratchpad source rather than this file.
The installation added this preface and the closing guidelines footer, and reformatted
the body to house Markdown conventions; it altered no classification, verdict, finding,
number, citation, recommendation or claim boundary, and none may be altered here.
References of the form `scratchpad/...` in the body below are the reviewer’s own record
of what was read and where it was written at review time, and are left as written.

On 2026-09-04, human-facing adversarial-control labels were normalized from their legacy
compact form to **Control 1**–**Control 8**, reserving `C0`–`C5` for epistemic
confirmation levels.
The source hash retains the historical wording; no finding, verdict or claim boundary
changed.

* * *

- Reviewer: independent record reviewer.
  Authored none of the proof, the instrument, the survey, the verification, or the
  repository records under review.
- Reviewed at: 2026-09-03, 08:10Z–08:35Z, at HEAD `609e7392` (branch
  `claude/squares-pr76-overnight-run-tpc888`). No command was run inside the
  08:58Z–09:58Z quiet lease.
- Write scope honoured: nothing under `/home/user/squares` was modified, added or
  committed. All artifacts of this review are under `scratchpad/bc158-record-review/`.

## Verdict: OVERSTATEMENTS FOUND, one of them a MATERIAL MISSTATEMENT

The evidential status is right everywhere and no record claims H-060 is resolved.
The mathematics replays exactly.
What is wrong is the *account of what exists and what stands behind the citations*: the
records state as fact that the instrument, its receipt and its eight controls do not
exist, when all three were committed to this repository sixteen minutes before the
commit that says so; and the curve-selection provenance in the round records still
describes a source configuration that the artifact they point at has since withdrawn.

Findings F1–F5 would mislead a reader about what was established.
F6–F9 are omissions and bookkeeping.
F10 is X-007. F11–F12 are the checks that pass.

* * *

## F1 — MATERIAL MISSTATEMENT: “the instrument does not exist” was false when written

**The records say:**

> exp-058 `verdict.reason`: “the W7 tool, its neighbourhood receipt and the eight
> rejecting Controls 1–8 **do not exist**, which is why H-060 keeps instrument_ready
> false”

> exp-058 results JSON, `disposition.note`: “the W7 repository instrument, its receipt
> and the eight rejecting controls **do not exist**”

> exp-058 body, *Reading `assurance: verified` Correctly*: “none of it came from a
> repository instrument, **because the instrument does not exist**.”

> exp-058 body, *What This Round Does Not Establish*: “The `W7` executable instrument,
> its exact neighbourhood receipt, and the eight rejecting **Controls 1–8**. Only
> **Control 8** was pre-run here”

> X-012 preface, **Owns:** “the `W7` executable instrument, its receipt and the eight
> rejecting controls of §6 belong to a separate lane and **do not exist yet**.”

> exp-058 results JSON, `replay_scripts.reason`: “The executable form of this
> mathematics is the W7 extension of devtools.assess_n5_rigidity, which is owned by a
> separate lane and **does not exist yet**”

**The evidence says:**

`git log` on `packing/src/sqpack/local_rigidity/`:

```
609e7392 2026-09-03 08:07:06  research: Repair two tautological rigidity controls ...
2f112f4c 2026-09-03 07:40:30  research: Register the H-060 chart and proof as exp-058 and X-012
6580a9fd 2026-09-03 07:24:39  wip: add n = 5 rigidity receipt and its regression tests
```

`git ls-tree -r 2f112f4c packing/src/sqpack/local_rigidity/` — the commit that added
exp-058 and X-012 — already contains `__init__.py`, `binding.py`, `chart.py`,
`controls.py`, `instrument.py`, `polynomial.py`, `receipt.py`, `system.py`.

`git show 2f112f4c:packing/src/sqpack/local_rigidity/controls.py` defines, by name:
`changed_feature`, `zero_margin`, `omitted_constraint`, `invented_contact`,
`side_release`, `wrong_chart`, `certificate_drift`, `exp034_angle_and_slide` — a
one-to-one match, in order, with X-012 §6’s table of **Controls 1–8**. The same commit’s
`instrument.py` carries `isolation_decided: bool = False` and an `instrument_ready`
property.

The instrument review confirms the receipt was being produced at that commit:

> instrument-readiness-review §1: “the author committed `2f112f4c` ('research: Register
> the H-060 chart and proof as exp-058 and X-012') at 07:40:30Z”

> §2: “`cmp` reviewer replay vs author’s retained files: identical
> (`instrument-certificate.json` sha256 `fd221f8c…a032`, `instrument-receipt.md`
> `6324384c…443b`).”

And SYNOPSIS, edited seven minutes after `2f112f4c` (the phrase enters at `6309e1f4`,
07:47:48Z), says the opposite:

> SYNOPSIS: “A separate lane’s instrument **reports ready**, but that is its author’s
> claim, it is under independent review, and it does not decide isolation.”

**Assessment.** The repository asserts, in the same hour, both that the instrument does
not exist and that it exists and reports ready.
SYNOPSIS is the one that is right.
The JSON even names the package while denying it: `open_obligations[0].owner` reads “a
separate lane (**sqpack.local_rigidity** / devtools.assess_n5_rigidity)”.

The narrow defence available is that the agenda’s `W7` asks to *extend*
`devtools.assess_n5_rigidity` and the built article is a new package that *binds* to it
— a deviation the review records independently (§8 item 9: “The instrument is a new
package (`sqpack.local_rigidity`) binding to `devtools.assess_n5_rigidity`, not an
extension of it as the hypothesis’s instrument text says”). That defence covers the
words “the W7 extension”; it does not cover “its exact neighbourhood receipt, and the
eight rejecting Controls 1–8 do not exist”, which existed and ran.

Note also that the agenda assigns `W7` to `BC-152` itself, not to another lane —
agenda-016, BC-152 budget: “45--105 W7 extend the existing rigidity tool with a locally
injective half-angle chart”; the controls are BC-152’s 165–220 block.
“Belong to other lanes” is at best an intra-lane split, not the agenda’s allocation.

**Why this misleads.** The direction of the error is *understatement of what exists*,
but the sentence that carries it is the one that explains the disposition — “which is
why H-060 keeps `instrument_ready` false”.
A reader is told nothing has been built.
The truth is: it is built, it self-reports `instrument_ready: True` with
`isolation_decided: False`, its independent review returned **BOUNDED-CAVEAT rather than
a pass**, a repair landed at `609e7392`, and the repaired instrument has not been
re-reviewed.
Those are different epistemic situations with different next steps, and only
the second is true.

* * *

## F2 — OVERSTATEMENT: “two independent secondary sources … and they agree”, after one was withdrawn

**The records say** (six places, all still live at HEAD):

> exp-058 determination 4, question: “Given the Nash curve selection lemma **as quoted
> verbatim by two independent secondary sources**, does the order-2m coefficient
> induction close?”

> exp-058 `verdict.reason`: “its curve-selection step rests on **two independent
> secondary quotations** rather than on BCR Proposition 8.1.13 itself”

> exp-058 body: “**two independent secondary sources are quoted verbatim in the
> artifact, and they agree**, but a secondary quotation is not a reading.”

> exp-058 results JSON, `open_obligations[1]`: “Currently supported only by **two
> independent secondary sources quoted verbatim**.”

> `packing/campaign/ledger.md` lines 464 and 501 (generated from the above).

> SYNOPSIS: “the curve-selection step rests on **two secondary quotations** rather than
> on the printed BCR text.”

**The artifact they point at says:**

> X-012 §4.1: “**One citation withdrawn.** The packet also quoted Nguyen Hong Duc,
> *Curve selection lemma in arc spaces*, arXiv:2301.00128 (2022), §1, which states the
> arbitrary-semialgebraic Nash version and attributes it to Milnor.
> The statement it gives is right and agrees with the one above; the attribution is not,
> because Milnor’s own hypotheses are narrower … Keeping it would have made this
> document repeat an over-attribution, so it is withdrawn”.

**The source says:**

> curve-selection-verification §2.6: “Nguyen Hong Duc (arXiv:2301.00128) attributes the
> *arbitrary*-semialgebraic Nash version to Milnor; that is an over-attribution relative
> to Milnor’s own hypotheses, and **is one of the two secondary sources the previous
> agent relied on**. It is not wrong about the mathematics, but it is wrong about which
> theorem says it.”

> §7 recommendation 5: “**Do not cite arXiv:2301.00128 for Milnor.**”

**Assessment.** The round records describe the frozen packet’s source configuration, not
the artifact they cite.
In the installed X-012 there is now no “second independent secondary source”: what
stands behind the citation is (i) Coste’s own lecture notes — Coste is an *author* of
BCR, so author-written rather than secondary, and self-described as “still in a
provisional form”, with Theorem 1.15 introduced by “We explain the reason for this fact,
without giving a complete proof”; (ii) the printed table of contents, which locates the
proposition but gives no text; and (iii) four verbatim uses of `[BCR, Prop. 8.1.13]`,
which X-012 now correctly labels “all four by Fernando and coauthors, **which is one
author group and not four independent ones**”.

The word “independent” is doing work it cannot do in any of the six sentences above.

* * *

## F3 — MATERIAL MISSTATEMENT: the round records assert the installed artifact is unaltered

**The records say:**

> exp-058 results JSON, `frozen_packet.note`: “The installed exploration report
> reproduces this packet’s content.
> It is reformatted to house Markdown conventions and carries an installation preface
> and the common-doc footer, so its bytes differ from the frozen source; **no
> mathematical statement, number, count, citation or claim boundary was altered.**”

> exp-058 body, *Where the Artifacts Are*: “Its mathematical body is **byte-identical**
> to the frozen packet, whose SHA-256 is `28343b74…`.”

**X-012 itself says:**

> X-012 preface: “**Provenance pass, 2026-09-03.** One later pass has touched the body …
> Applying them **rewrote the citation apparatus of §4.1 (including one citation
> withdrawn)**, de-flagged the Milnor statement of §4.1 from ‘from memory’, added two
> items to that route’s reduction, added the nonconstancy clause and the hypothesis
> inventory to §4.2, and updated §8.3, the closing obligation note, the replay-artifact
> note above and this record’s brief.”

> X-012 preface, one paragraph earlier: “the body from the rule below **reproduces the
> packet’s content, reformatted** to house Markdown conventions.”

**Assessment.** Two separate errors in the same claim.
(a) “byte-identical” was already wrong at registration — X-012’s own preface says the
body was reformatted, so the bytes differ by construction.
(b) “no … citation … was altered” is now flatly contradicted by X-012’s disclosed
provenance pass. X-012 is the honest record here; the JSON — the record a reviewer would
diff the frozen hash against — denies the edit.
Neither exp-058 record was touched after `ba9d13d4` and `ad6a11f2` landed the
corrections.

The hash itself is fine:
`28343b743e689fc99968d589a542d9022d061de8ec3ae5100bf4ef4930e40b6b` is confirmed correct
for the frozen packet, and every place that cites it correctly says it names the frozen
source and not the installed file.

* * *

## F4 — OVERSTATEMENT: “equivalently Milnor 1968 Lemma 3.1”

**The records say:**

> X-012, *The single largest remaining proof obligation*: “the statement of BCR
> Proposition 8.1.13 (**equivalently Milnor 1968 Lemma 3.1**): that for an **arbitrary**
> semialgebraic `A ⊂ R^n` (not assumed open, closed, or of any dimension) and
> `x ∈ Cl(A)`, there exists a *real-analytic* arc `gamma` …”

> exp-058 body: “Primary-text confirmation of the curve-selection statement, `BCR`
> Proposition 8.1.13 **or equivalently Milnor 1968 Lemma 3.1**.”

> exp-058 results JSON, `open_obligations[1]`: “(BCR Proposition 8.1.13, **equivalently
> Milnor 1968 Lemma 3.1**).”

**The source says:**

> curve-selection-verification §0: “**Milnor’s Lemma 3.1 does not give the statement as
> written**, and the brief’s suspicion about it is correct.
> Milnor’s ‘semi-algebraic’ means *real algebraic set intersected with finitely many
> strict polynomial inequalities*, not an arbitrary semialgebraic set — now confirmed
> verbatim from a peer-reviewed source that cites Milnor p. 25 (§2.6).”

> §5.1: “The proof’s set is **not** in this class as written, for two independent
> reasons: its defining inequalities are **non-strict** (`g_j ≥ 0`), and it has a
> **point removed**.”

**Assessment.** The clause asserts, for the arbitrary-semialgebraic statement, exactly
the equivalence for which the Nguyen Hong Duc citation was withdrawn one section earlier
in the same document.
X-012 §4.1 gets it right — “the general statement is cited to BCR, and Milnor is cited
only together with the reduction that puts the set into his class” — and §8.3 gets it
right — “Alternative: Milnor 1968 Lemma 3.1 **with the finite-union reduction** of
§4.1”. The closing paragraph then drops the reduction and restores the equivalence.
Both exp-058 records repeat it uncorrected.

This is not a hair: it is the specific over-attribution the verification lane was
convened to catch, surviving in the sentence that names the round’s single largest
remaining obligation.

* * *

## F5 — OVERSTATEMENT: a survey finding carried inside the novelty CLAIM

**The records say:**

> exp-058 body, *Novelty, as Scoped*: “The admissible claim is the first exact proof
> that Goebel’s `n = 5` optimum is locally rigid at fixed side — a property Kingbird
> asserts with no method anywhere on the site, that Goebel’s 1979 paper does not state
> …, that Friedman’s survey does not annotate, and **that no stated rigidity theorem for
> polygon contacts covers**.”

> exp-058 results JSON, `novelty.claimed`: “… **and not covered by any stated rigidity
> theorem for polygon contacts**.”

> X-012 §7.4 and §8.5 carry the same sentence.

**The instrument review says, in terms:**

> instrument-readiness-review §10, qualification 1: “The clause 'not covered by any
> stated rigidity theorem for polygon contacts’ … is, by X-012’s own §7.1 and §8.3, the
> coordinator’s survey finding, unverified against the primary texts by the lane — and
> not by me. It is not needed for S3 … and **should be carried as an unverified survey
> assertion, not as part of the claim**.”

**Assessment.** The records hedge *near* the clause — X-012 §7.1 flags the “Governing
finding (coordinator’s independent prior-art survey; not verified by this lane against
the primary texts)”, §8.3 repeats it, and exp-058 adds “The scoping is this lane’s
assertion, not a reviewed finding; `BC-153` owns it”.
But in all four places the clause sits inside the sentence that states what *is*
claimed, and `novelty.claimed` is a single string a downstream consumer reads without
the neighbouring `novelty.status`. The review’s instruction was specific and is not
followed.

Two further precision losses against the survey’s own wording:

> h060-prior-art §1.6: “**no theorem stated in the structural-rigidity or jamming
> literature covers polygon contact systems**”

The records generalise this to “any stated rigidity theorem”, dropping the restriction
to the structural-rigidity and jamming literature.
The survey’s own §1.5 table records that for “McCormick 1967 / Fiacco–McCormick 1968 /
Nocedal–Wright Thm 12.6” the failing hypothesis is “**none** — hypotheses reduce to the
local 20-inequality system”, and what survives is “the whole closing inference”.
A stated theorem does cover this system once reduced; the survey’s point is narrower
than the records’ paraphrase.

The rest of the S3 scoping is correct and well carried.
The records state plainly that the statement is Kingbird’s and not novel, and exclude
the classical second-order sufficiency principle and the Connelly–Whiteley proof shape
by name, in exp-058, in `novelty.not_claimed_as_new`, and in X-012 §8.5.

* * *

## F6 — OMISSION: the instrument’s residual boundaries reach no repository record

A consequence of F1: because the records say the instrument does not exist, none of what
the instrument itself discloses reaches the record a reader consults.
Missing:

- **Four cited, not machine-checked mathematical inputs.** Instrument receipt, *Declared
  mathematical inputs*: the separating-axis theorem ("no -- a cited theorem, not a
  computation"), the rotation group’s topology ("partly … the topological statement
  itself is cited"), convexity of container and squares ("no -- standard"), continuity
  of polynomials ("no -- standard"). Confirmed accurate by the review (§8 item 2).
- **The restricted-jet limitation.** Receipt, *Claim boundary*: “the binding compares
  the second derivative along one chart ray only -- the image of T-012’s single free
  direction, e_u4 halved -- **not the full chart Hessian**.” Review §5: “the receipt
  should say ‘restricted second jet along `e_u4`’.”
- **Single-support-feature classification only.** Review §8 item 4:
  “Single-support-feature touches only; edge-flush and corner-on-corner refused by
  `DisjunctiveTouchError`.”
- **The reduction audit never samples the boundary of `U`.** Receipt: “no sampled point
  sits near the boundary by construction”; review §8 item 3: “all 244 audit points lie
  inside `U`, so the audit never samples `U`’s boundary or its complement.”
- **`isolation_decided = False` unconditionally.** In the receipt header and in
  `instrument.py`. SYNOPSIS carries it ("it does not decide isolation"); exp-058 and
  X-012 do not, because for them the instrument is not there to have a boundary.

Note that the *packet* is not subject to the restricted-jet limitation:
`verify_chart.py` verifies `H_chart == J^T H_geo J` on all twenty rows, which I re-ran
and confirmed. The limitation belongs to the instrument’s binding, and it is exactly the
kind of difference between paper proof and instrument that the record should have been
able to state.

**What the records do carry correctly, and prominently:** the second, corroborating
route is everywhere marked as not the acceptance route —

> exp-058: “It is explicitly **not** the acceptance route.
> Acceptance was preregistered on curve selection, so the second proof softens no
> obligation above.”

> X-012 §8.1: “The second proof of §5.7 is corroboration with weaker hypotheses; it is
> not a substitute, does not amend the criterion, and does not discharge any obligation
> listed below.”

> JSON `open_obligations[1].blocks`: “… is not discharged by the corroborating second
> proof”; SYNOPSIS: “discharges nothing”.

That matches h060-prior-art’s own framing ("the SOSC route proves the same claim from
weaker hypotheses, so it satisfies the criterion’s purpose, **but not its letter**"). No
finding here.

* * *

## F7 — STALENESS: SYNOPSIS says the instrument review is still running; it returned, with a caveat

> SYNOPSIS: “A separate lane’s instrument reports ready, but that is its author’s claim,
> **it is under independent review**, and it does not decide isolation.”

That sentence entered at `6309e1f4` (07:47:48Z). The review returned at 07:55Z:

> instrument-readiness-review, *Classification*: “**BOUNDED-CAVEAT** … two of the eight
> registered negative controls (`changed_feature`, `invented_contact`) are structurally
> incapable of failing and never touch the binding’s refusal path, so the receipt’s ‘all
> eight controls reject’ **overstates the evidence** for the one refusal the instrument
> exists to make … this is **not an exact PASS** and does not by itself authorize
> flipping `instrument_ready`.”

The repair landed at HEAD `609e7392` (08:07:06Z), whose own message says “H-060 remains
unresolved and instrument_ready stays false **pending re-review**”, and the receipt
digest was re-recorded as
`ba99ccccd7303f260f48c62a10fb9b6dc43ca3e8ff804646ef5de89a48967971` (the reviewed digest
was `1ab2708623cf4dd077a0f125ba81cf3777088ea8e4d750a56d1dc3f55f807978`).

No repository record carries the BOUNDED-CAVEAT classification, the tautological-control
finding, or the fact that the repaired instrument is unreviewed.

**Digest check (task item 4): clean, but empty.** `grep` over the whole repository finds
**neither** `1ab27086` **nor** `ba99cccc`. No superseded digest is cited anywhere — but
no instrument digest is cited anywhere either, so nothing in the repository pins which
build of the instrument any statement refers to.

* * *

## F8 — BOOKKEEPING: the frozen packet is 925 lines, the JSON says 926

> exp-058 results JSON, `frozen_packet`: `"bytes": 53646`, `"lines": 926`

Measured on the frozen packet
(`sha256 28343b743e689fc99968d589a542d9022d061de8ec3ae5100bf4ef4930e40b6b`, confirmed):
`wc -l` = 925, `len(text.splitlines())` = 925, newline count = 925, file ends with a
newline. `bytes` = 53646 is correct.

Every other record says 925:

> X-012 preface: “The packet is `925` lines with SHA-256 `28343b74…`”

> `session-083`: “Froze a **925-line** proof packet, sha256 `28343b74…`”

The JSON is the outlier by one.

* * *

## F9 — MINOR: X-012’s Kingbird rigid-list is uncorroborated and in tension with the survey

> X-012 §7.3: “It lists as rigid
> `n = 5, 11, 18, 28, 40, 52, 149, 296, 493, 740, 1037, 1384, 1781`”

> h060-prior-art §3.1: “The main page carries ‘Rigid.’
> on **exactly four packings at `n <= 100`: `n = 5, 11, 28, 40`** (lines 44, 80, 163,
> 224), consistent with the schema comment ‘all but four packings at n <= 100’.”

I checked the archived page: `packing/resources/web/kingbird-squares-in-squares.md`
contains exactly four `[Rigid.]` links, at lines 44, 80, 163, 224. X-012’s list adds
`n = 18` and `n = 52` below 100.

The two are reconcilable — the rigid page’s own preamble, quoted in the survey, says
“Most are the best known, but in cases where they are inoptimal, they are shown
alongside the best known”, so rigid-but-inoptimal entries need not be annotated on the
main list. Neither record says so, the rigid page is not archived, and a reader cannot
check the list of thirteen from anything in the repository.
Both records already recommend archiving the page; the JSON’s `recommendations[0]` is
exactly that, and it is the right fix.

* * *

## F10 — X-007’s correction: mathematically correct; its self-description understates its scope

**The correction is right.** Verified line by line.

> X-007 (current): “Puiseux gives that arc an expansion in fractional powers `s^(k/N)`
> for some positive integer `N`, so the substitution `s = u^N` comes first: it clears
> the fractional exponents, keeps the arc inside the set (`u > 0` exactly when `s > 0`),
> and leaves an analytic arc, whose parameter is written `s` again below, with
> `gamma(s) = p + sum_{k >= m} a_k s^k` and `a_m != 0`.”

> curve-selection-verification §4.5: “a merely continuous semialgebraic arc has only a
> *Puiseux* expansion in `s^{1/N}` and needs the reparametrisation `s = u^N` before the
> induction can start … **taking the Nash version removes the Puiseux step entirely** …
> If the Puiseux phrasing is kept, the reparametrisation to clear fractional exponents
> must be written down; it is legitimate but it is a step.”

Each step checks: a continuous semialgebraic arc into `R^n` has coordinatewise algebraic
Puiseux expansions, and a common denominator `N` may be taken; `s = u^N` maps
`(0, ε^{1/N})` onto `(0, ε)` bijectively and monotonically, so containment in the set is
preserved; `Σ a_k u^k` converges near `0` and extends analytically to `u = 0`; the
identity theorem then supplies a least `m` with `a_m ≠ 0`, which is what the induction
consumes. The alternative route named — BCR Prop.
8.1.13, whose arc is Nash hence real-analytic — does avoid the step, and X-012 §4 does
take it.

The correction also quotes the sentence it replaced.
I diffed the current file against `scratchpad/X-007.orig.md`: the quoted text —

> “the curve selection lemma gives a semi-algebraic arc into the set, and Puiseux gives
> `gamma(s) = p + sum_{k >= m} a_k s^k` with `a_m != 0`”

— is verbatim what stood at lines 301–302 of the original.
The quotation is honest.

**But “nothing else in the argument changes” understates it.** The same diff shows the
correction inserted a second repair:

> “the curve selection lemma, **applied to the feasible set *with the pose removed***,
> gives a semi-algebraic arc into it — one avoiding `p` at every positive parameter
> value, **hence nonconstant**.”

The original applied the lemma to the set itself.
The source calls that omission the central trap:

> curve-selection-verification §4.2: “**But that vacuity is precisely the trap for this
> proof.** An isolation argument needs a *nonconstant* arc.
> Under `x ∈ Ā` alone, the lemma is entitled to hand back the constant arc, and the
> coefficient induction has nothing to bite on.”

> §5.3 item 5: “**Removing the point is a separate step**, and it is the one most likely
> to be skipped.”

X-012 §4.2 treats this at length and correctly ("Applying the lemma to `F \ {0}` rather
than to `F` is load-bearing, not tidiness"). X-007’s correction repairs the same gap but
frames it as one fix — heading and opening sentence name only the reparametrisation
("The reparametrisation above was missing when this was written"), and the pose removal
appears only in a trailing subordinate clause.
A reader of the correction alone would not learn that a second, independent gap was
closed. The surrounding text is otherwise consistent with the correction.

*Cosmetic, not a finding:* the “wrong version” paragraph immediately above still writes
“Puiseux gives `gamma(s) = p + a_m s^m + …`” with integer exponents — the shorthand the
correction identifies as skipping a step.
It is describing a rejected argument, so nothing turns on it.

* * *

## F11 — Evidential status (task item 1): PASSES

Checked exhaustively; no field anywhere states or implies acceptance.

| where | field | value |
| --- | --- | --- |
| exp-058 frontmatter | `verdict.decision` | `unresolved` |
| exp-058 frontmatter | `verdict.needs_review` | `true` |
| exp-058 frontmatter | `effort.stopped_by` | `dependency` |
| exp-058 frontmatter | `subject.selftest_passed` | `false` |
| results JSON | `disposition.hypothesis_status` | `unresolved` |
| results JSON | `disposition.instrument_ready` | `false` |
| results JSON | `disposition.review_state` | `review-pending` |
| results JSON | `disposition.reviewed_by` / `frontier_change` | `null` / `null` |
| H-060 hypothesis file | `instrument_ready` | `false` |
| SYNOPSIS hypothesis table | H-060 | `needs review` |

**Roles.** The only `role: outcome` determination is the H-060 question itself, and it
carries `outcome: no_progress` with `checked_by: "nothing that the criterion accepts"`.
The four supporting determinations carry `mechanism`, `guard`, `mechanism`, `guard`. No
supporting determination is typed `outcome`.

**No promotion leaked.** `grep` over `packing/frontier/` finds no mention of H-060,
exp-058 or X-012. exp-058’s claim “No frontier property, result-register entry or
evidence record changed” is true.

**`assurance: verified` is correctly explained.** exp-058 devotes a section to saying it
describes the arithmetic and not the hypothesis ("It does **not** mean `H-060` is
verified, and the verdict is the field that says so"), which is the right disclosure for
a field that would otherwise read as a disposition.
The record lists that exact misreading in `new_failure_modes`.

**The conditional citation is kept conditional.** exp-058 determination 4: “The
hypothesis is conditional and stays conditional: the printed BCR text was not available
in this environment, so the lemma’s statement is cited rather than confirmed against a
primary source”. That is exactly what the verification’s *Primary text status, stated
plainly* paragraph supports: “I did **not** reach the printed page of BCR Prop.
8.1.13, and I did **not** reach the printed page 25 of Milnor’s Lemma 3.1.” X-012 §4.1
and §8.3 say the same in the artifact.
Apart from F2 and F4, the primary-text status is carried honestly throughout; no record
implies the printed page was consulted.

* * *

## F12 — Replay and quantities (task item 4, numbers): PASSES

I re-extracted the seven scripts from the results JSON and re-ran them at HEAD
(`scratchpad/bc158-record-review/replay/`), before the quiet lease.

- All seven `sha256` values in `replay_scripts.scripts` reproduce from the retained
  `source` text, and all seven match the frozen copies in `scratchpad/bc152/` byte for
  byte. `bytes` fields all correct.
- Elapsed for the record’s own `command` sequence: **11.05 s**, against the recorded
  `wall_seconds: 11.33`. Consistent.
- Reproduced exactly: 16 active / 64 inactive wall-corner functions, minimum inactive
  margin `1 - sqrt(2)/4`; 4 touching / 6 noncontact pairs; the 28 violated-branch
  witnesses with least value `-sqrt(2)/4`; all four active pair corners at along-edge
  parameter exactly `1/2`; `A_chart == A_geo J`; `H_chart == J^T H_geo J` on all 20 rows
  with no second-order angle correction; `q_chart == 4 q_geo`, `-2` on the four pair
  rows and `0` on the sixteen wall rows; column `t4` of `A_chart` identically zero; each
  pair polynomial restricted to the flex line exactly `-t4^2`; the 14 pinned coordinates
  and the self-stress with `w . q_chart = -2*sqrt(2)`; the SOSC pair `-2 + 2 sqrt 2 > 0`
  (chart) and `-2 + sqrt(2)/2 < 0` (`(c, theta)`) with threshold `mu > 2/(-w.q)`; and
  exp-034’s overshoot `3 sqrt(2)/4 - 1 > 0` at Goebel’s side.
- Cross-checked against two independent sources: the instrument receipt (minimum
  inactive margin `1 - 1/4*sqrt(2)`, 28 strictly negative witnesses, `100 + 28 = 128`
  strict conditions) and the reviewer’s own enumeration ("400 base margins vs
  instrument, key by key | 0 mismatches").
- The agenda’s declared counts are in agenda-016’s BC-152 budget ("the sixteen active
  and sixty-four inactive wall-corner inequalities, four touching and six noncontact
  pairs"), matching `agenda_count_confirmation` with `discrepancy: null`.

Every substantive number in the records is supported.
The problems in this review are all in the prose about provenance and about what exists.

* * *

## Ranked summary

1. **F1** — the instrument, its receipt and its eight controls existed sixteen minutes
   before the commit that says they do not; the false clause is the one that explains
   the disposition, and SYNOPSIS contradicts it seven minutes later.
   Material.
2. **F2** — “two independent secondary sources … and they agree”, after one was
   withdrawn from the artifact as an over-attribution; propagated into the ledger and
   SYNOPSIS.
3. **F3** — the JSON asserts no citation was altered, and exp-058 asserts the installed
   body is byte-identical; X-012 discloses that both are false.
4. **F4** — “equivalently Milnor 1968 Lemma 3.1” for the arbitrary-semialgebraic
   statement, in three records, including X-012’s own closing paragraph.
5. **F5** — the survey clause “not covered by any stated rigidity theorem” carried
   inside the claim, against the reviewer’s explicit instruction, and generalised beyond
   the survey’s wording.
6. **F7** — SYNOPSIS still has the instrument review in flight; BOUNDED-CAVEAT and the
   unreviewed repair reach no record.
7. **F6** — the instrument’s four cited inputs, restricted-jet binding,
   single-support-feature scope and inside-`U`-only audit reach no record.
8. **F8** — `frozen_packet.lines: 926`; the packet is 925.
9. **F9** — X-012’s thirteen-entry Kingbird rigid-list is uncorroborated and in tension
   with the survey’s four; the page is unarchived.
10. **F10** — X-007’s correction is mathematically right but describes itself as one fix
    when it made two, the second closing the constant-arc gap the source calls the trap.

Nothing found that overstates the mathematics, weakens the frozen criterion, changes an
exact quantity, or moves H-060 toward acceptance.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
