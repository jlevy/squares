# Fix Check: The Uniqueness of Trump’s Eleven-Square Packing (T-112)

**Reviewer.** Fable, the reviewer who wrote
`review-2026-10-06-n11-uniqueness-adversarial.md`, prompted separately to check the
fixes. I share no context with the lane that registered the result and made the fixes
(think-d1bd) beyond the brief, `AGENTS.md` and the committed record.
My earlier review names the result `T-102`; it is `T-112` now, and this document uses
`T-112` throughout.

**Date.** 2026-10-06.

**Subject.** `T-112` in `packing/frontier/results.yaml` (lines 11462 to 11581) and
`E-n011-optimum-uniqueness` in `packing/frontier/evidence.yaml` (lines 881 to 987), at
commit `0df76fc26`, the head of `claude/gallant-allen-nvd2jf-followups` (PR #394), which
contains PR #392’s head `98f3fdff2`; compared against the reviewed commit `5ecb1307b`
and against `origin/main` as fetched during this check, `4261f6809`. The branch forks
from `b6f8993f3`, the main I compared against on the first review.

**Scope.** Each of U-1 to U-9: resolved, partially resolved or not, with the file and
line that shows it. Then a second adversarial read of the whole of `T-112`’s claim,
composition, `next_rung` and notes, the evidence entry, `epistemics.md`’s Result Kinds,
`n-011.md`, `README.md`, and the paper’s new text in PR #394, for any new mathematical
or factual error: the eight-configurations statement, the Stromquist and Trump
quotations against the archive, and the sentence about the Lean theorem.

**What I read.** `git diff origin/main..HEAD` in full for the 25 files the stack
changes, and `git log origin/main..HEAD` (fifteen commits, two of them merges of main).
`T-036`’s `superseded_by` and notes (lines 3226 to 3255) and `T-060`’s notes (lines 5303
to 5321). `devtools/render_recent_results.py` `standing()` (lines 477 to 496) with
`BOUND_CLAIMS` (line 134), `held()` and `_lower_holders()` (lines 435 to 474), and
`devtools/build_bound_citations.py` `results_carrying()` (lines 466 to 478).
`devtools/result_status.py` `open_issues()` and `latest_review()` (lines 87 to 133).
`ElevenSquare/Optimality.lean` in the retained Lean packet, the statement audit’s
coverage table, and `docs/VERIFICATION_20261006.md` lines 10 to 25 in the same packet.
`PROOF.md` lines 498 to 540. The transcriptions
`trump-2023-packing-11-unit-squares.raw.md`,
`stromquist-1984-...-ii-ten-unit-squares.raw.md` and
`stromquist-2003-packing-10-or-11-unit-squares.md` under `packing/resources/papers/`.
`packing/cases/trump11/packing.py`.

**What I ran.** With the project’s Python 3.14.7 interpreter
(`/home/user/squares/packing/.venv/bin/python3`, with `PYTHONPATH` pointed at this
worktree’s `packing/src` and `packing/`, since the worktree has no venv of its own and I
did not want the main checkout’s data read in its place):

- `devtools.check_results`: 112 registered results, every check passes; by status 1
  recorded, 3 reviewed, 106 confirmed, 2 incomplete.
- `pytest tests/test_results_register.py tests/test_result_status.py
  tests/test_recent_results.py tests/test_n11_composition_joins.py`: 129 passed, 1
  failed. The failure is FC-1 below.
  `tests/test_overview.py` could not set up in this worktree, because the `kpress`
  submodule is not checked out here (`devtools/sans_instances.py:136`), which is my
  environment and not the branch.
- An exact computation in $\mathbb{Q}(u)$ of the $D_4$ stabiliser of the construction in
  `cases/trump11/packing.py` about the container’s centre, with a numeric distance from
  each image to the packing (script in my scratchpad, not retained).
  Its result is under U-9 and FC-2.
- `git fetch origin main`, which moved `origin/main` from `b6f8993f3` to `4261f6809`.

No geometry was rerun.

## Verdict

The two blocking findings are resolved: the result is `T-112`, the register holds 112
entries and the checker accepts it, and the PR’s two Lean sentences are gone in favour
of main’s import.
Of the seven non-blocking findings, U-3, U-4, U-5, U-6, U-8 and U-9 are
resolved; U-7 is resolved in two of its three parts, and the third part was declined for
a reason I checked in the code and that holds.
The mathematics is unchanged and still holds; the one new mathematical statement, that
there are exactly eight optimal configurations, I re-derived exactly.

I raise four new findings.
One blocks the merge as the branch stands:

- **FC-1 (blocking):** `test_result_status.py` fails at `0df76fc26` because `T-112` is a
  project result whose latest review ends `defect-open`. Recording this check closes it.
- **FC-2:** the stabiliser check is retained only in prose, and its number, 0.84, is not
  the nearest non-identity image under either natural metric.
- **FC-3:** the paper’s `[^lean]` footnote still says the project has reviewed neither
  formalization, beside the body’s statement audit.
- **FC-4:** the stack is one merge of main behind, and the merge will conflict in four
  files the branch does not mean to change.

## Findings, One by One

| Finding | Was | Disposition | Where |
| --- | --- | --- | --- |
| U-1 | blocking: `T-102` taken on main | resolved | `results.yaml:11462`, `:11566`; `check_results` passes at 112 |
| U-2 | blocking on rebase: Lean sentences contradict main’s import | resolved | `README.md:38-41` adds only the T-112 sentence; `T-060` notes carry main’s text; `next_rung` at `:11552-11559` |
| U-3 | paper says the project registers only optimality | resolved | paper `:952-954`; `release.py:361-371`, `:455` |
| U-4 | quoted case-438 note not in the packet | resolved | `evidence.yaml:979-981` cites `PROOF.md` section 8; no `CANDIDATE438` citation remains |
| U-5 | S4 reads as S3 | resolved | `results.yaml:11491-11498`, score 3, `by:` names U-5 |
| U-6 | kind defined for one packing | resolved | `epistemics.md:381`, `:399-401` |
| U-7 | input evidence, verifier roles, the certificate | partially | `:11515-11517` (declined, reason holds); `evidence.yaml:959-961` (done); `VERIFIERS.md:105`, `RESULTS.md:703` (not done) |
| U-8 | 13,308 miscounted as certificates | resolved | moot with U-2; the paper’s `[^lean-done]` at `:1305-1311` counts axioms |
| U-9 | state “exactly eight”; cite 1984 for three | resolved | `results.yaml:11472-11475`; `evidence.yaml:986-987`; paper `:1293-1304` |

### U-1 (blocking): the id

**Resolved.** The entry is `T-112` (`results.yaml:11462`). Its notes say it was
registered as `T-102` and renumbered when the branch merged main, where `T-102` to
`T-111` had been taken the same day, and that the stored review’s `T-102` means this
entry (`:11566-11568`). `T-036`’s `superseded_by` names `T-112` (`:3245`), the SYNOPSIS
row, the generated `RESULTS.md` (line 67) and the five tests use `T-112`
(`test_results_register.py:1142`, `test_result_status.py:320`,
`test_recent_results.py:117`, `test_overview.py:3059`, `:3177`). `check_results` accepts
the file with 112 results, and the register tests other than FC-1 pass.

### U-2 (blocking on rebase): the Lean sentences

**Resolved.** Against `origin/main`, `README.md` gains only the four-line T-112 sentence
(lines 38 to 41); the PR’s “not yet reviewed or replayed” paragraph is gone.
`T-060`’s notes hold main’s import paragraph and no second one (lines 5303 to 5321; the
only difference from current main there is FC-4). `T-112`’s `next_rung` now says what I
asked it to: the theorem `ElevenSquare.optimality`, which the statement audit reads as
$s(11) = T$, “states the lower bound and the construction and no equality case”, and a
Lean statement of the equality case would be the route to rung 5 (`:11552-11559`). That
is what the retained `Optimality.lean` states: `optimal_side_lower_bound` ($T \le S$ for
every packable $S$) and `optimality` as the pair of `construction_packable` with it, and
nothing about which packings attain $T$. The statement audit’s coverage table has the
row “No uniqueness of the packing | None stated”.

### U-3 (non-blocking): the paper’s stale sentence

**Resolved.** The closing section now reads “The Squares Project registers this
corollary separately as T-112. It rests on T-060’s evidence and adds no computation; its
one new step, that each premise is stated for a side at most $T$, is prose” (paper lines
952 to 954). `OPTIMALITY_REVIEW_HISTORY` gains v0.1.6, “registered as T-112 and no
longer called unreviewed” (`release.py:361-371`), and `OPTIMALITY_REVIEW_REVISED` is
October 6 (`:455`). The upstream-delta review’s row stands as a dated review.

### U-4 (non-blocking): the unretained upstream note

**Resolved.** The novelty basis now cites the retained text: “The upstream proof states
uniqueness only for the near branch of its case 438, at side S <= T (PROOF.md section 8:
the local theorem forces the near-branch packing to be the exact construction)”
(`evidence.yaml:979-981`). That is `PROOF.md` line 538, in section 8, and the paragraph
before it (lines 533 to 536) is the $S \le T$ statement.
`grep` finds no `CANDIDATE438` in `results.yaml`, `evidence.yaml` or `INVENTORY.md`.

### U-5 (non-blocking): significance

**Resolved.** Score 3, with a rationale that names the S3 anchor and says what an S4
would need (`results.yaml:11491-11498`); `by:` cites the review and records that the
registration proposed S4.

### U-6 (non-blocking): the kind’s definition

**Resolved.** “each is one of finitely many named packings, up to the container’s
symmetries and the relabelling of the squares, and moves no bound”
(`epistemics.md:381`), and the chooser’s new fourth rule separates a classification from
a second optimality (`:399-401`). The schema enum, `check_results.KINDS` and
`STRUCTURE_KINDS` agree.

### U-7 (non-blocking): the input evidence, the verifier roles, the certificate

**Partially resolved; the declined part was declined for a reason that holds.**

- *Cite `E-n011-global-optimality-independent` from `T-112`.* Declined, and the
  composition note says why: it “claims the exact value, which would give this result a
  bound’s standing that it does not have” (`:11515-11517`). I checked.
  `standing()` returns `NO_STANDING` only when none of a result’s cited evidence claims
  a bound (`render_recent_results.py:486-489`), and `exact-value` is in `BOUND_CLAIMS`
  (line 134; the entry’s claim is `exact-value`, `evidence.yaml:697`). Worse than the
  note says: `held()` credits a case’s lower bound to every in-scope result carrying any
  of the bound’s own evidence (`_lower_holders`, lines 435 to 449, through
  `results_carrying`, `build_bound_citations.py:466-478`), so `T-112` would read
  “current best” for $s(11)$ beside `T-060`, and `check_standing` compares that against
  the stated bound. The reason holds, and my suggestion was wrong for this register.
- *The verifier roles.* Not done.
  A verifier’s role is one value per program (`verifiers.yaml:1130`, `role: decides`),
  so `VERIFIERS.md` line 105 now counts `V-n11-optimality-checkers` as deciding two
  claims, and `RESULTS.md` line 703 lists it for `E-n011-optimum-uniqueness` without the
  `premises` mark that `V-check-n11-final-composition` carries.
- *The certificate.* Done in the entry’s `limitations`: “The certificate is T-060’s
  composition receipt, whose endpoint_argument is written for S < T, and the verifiers
  decide T-060’s premises, not the step at S = T” (`evidence.yaml:959-961`).

The remaining part is bookkeeping in a generated table.
If the verifier register ever gains a per-evidence role, this entry is the case for it;
until then the `limitations` sentence is where a reader learns it, and I do not reopen
the finding.

### U-8 (non-blocking): the native-certificate count

**Resolved.** The paragraph it was in is gone (U-2). The paper’s new `[^lean-done]`
counts “13,308 axioms from approved `native_decide` certificate checks” (lines 1305 to
1311), which is the report’s “Generated native certificate axiom dependencies: 13,308”
(`VERIFICATION_20261006.md` line 17), beside “Approved numerical declarations: 10,464”
(line 16). The paper’s body says “7,920 Lean modules with no admitted goal” (line 1012),
which is the report’s lines 13 and 14.

### U-9 (non-blocking): exactly eight, and the 1984 count

**Resolved.** The claim now says “No symmetry of the container maps Trump’s packing to
itself, so there are exactly eight optimal packings as unlabelled configurations, the
images of one another” (`results.yaml:11472-11475`). I re-derived this exactly, in
$\mathbb{Q}(u)$ from `cases/trump11/packing.py`, for all eight elements of $D_4$ about
$(T/2, T/2)$: the identity maps all eleven corner sets onto themselves, and no other
element maps more than four (the anti-diagonal reflection, four; the diagonal, three;
the rest, two). So the stabiliser is trivial and the orbit has eight members, as
unlabelled configurations and modulo the per-square quarter turn, since corner sets
ignore both. The three-packings count is cited to the 1984 memorandum in the evidence
entry (`evidence.yaml:986-987`), the paper (lines 1293 to 1304) and `n-011.md` (line
213).

## The Second Adversarial Read

**The claim** (`results.yaml:11467-11485`). $T = 3.8770835900228141773\ldots$ agrees
with the construction’s side to the digits printed (my run:
`3.87708359002281417730789…`). “The least side T-060 proves possible”, the 1979 date,
independent rotations, boundary contact, the quarter-turn reparametrisation and the
three-sentence summary of the argument match my first review’s derivation; “a D4 element
composed with the case-438 quarter turn” is the alignment.
The last paragraph on T-036 is right: reflections leave that family, as T-036’s own
notes say.

**Composition** (`:11506-11517`). V3 from proof-audited with a proof block, C2 for a
prose step, “as for T-036’s composing step”: unchanged from what I accepted.
The second paragraph is U-7 above.

**`next_rung`** (`:11552-11559`). Accurate about the Lean theorem, as under U-2. “Rungs
4 need what T-060’s need” is consistent with T-060’s own `next_rung`.

**Notes** (`:11560-11581`). The history is right: the paper stated the corollary from
v0.1.2, the register registered only optimality, the renumbering, the two blocking
findings “about the registration, not the mathematics”, and “U-8 fell away with U-2”.
One number in the dispositions is not right as stated; that is FC-2.

**The evidence entry.** Unchanged from the reviewed commit except the novelty basis
(U-4) and `limitations` (U-7); both read correctly.
The entry’s `replay` runs only `check_n11_final_composition`, and names
`V-n11-optimality-checkers` beside it as T-060’s entry does.

**`epistemics.md`.** The new row and rule are consistent with the schema’s description
(`results.schema.yaml:121`, `:131-134`) and the checker (`check_results.py:126`,
`:143-148`).

**`n-011.md`.** The “Unique, 2026-10-06” paragraph (lines 206 to 214) and the T-036
paragraph (lines 459 to 462, “superseded in part by each and in whole by the two”) agree
with the register. The `evidence` list gains the entry (line 143).

**The quotations.** Trump: “The geometrical object is absolutely rigid, no unit square
can be rotated or translated” is line 50 of the transcription, after the page-2 marker
at line 24, so “p. 2” is right.
Stromquist 1984 II: “Three different packings of ten unit squares in a square of side s
= 3 + √2/2” is line 47 of the raw extraction, which is p. 1 by the transcription’s page
map; the extraction garbles the radical as `3 + #V2`, and the paper’s `\sqrt{2}/2`
restores it from the memo’s own abstract three lines earlier, “s = 3 + 2/2 = 3.707”,
which is the same number.
The quotation is faithful to the memo; a reader checking it against the archive should
know the raw line is damaged there.
Stromquist 2003: “The 10-square packings in Figure 1 are optimal” is line 28 of the
transcription, and its Theorem 1 makes any packing at $3 + \sqrt{1/2}$ optimal, so
“which Stromquist 2003 proves optimal” holds whatever its Figure 1 shows.

**The Lean sentence.** The paper’s body (lines 1011 to 1017) and `T-112`’s `next_rung`
agree with the retained `Optimality.lean` and the statement audit, as under U-2. The
footnote beside them does not; that is FC-3.

**The paper’s section references.** “§8” links the anchor
`#8-complete-case438-capture-and-the-exact-u-to-t-bridge`, which is the slug of
`PROOF.md` line 498, “## 8. Complete case438 capture and the exact U-to-T bridge”; “its
§10” is “Deduction of the optimum” (line 616). The three archive paths and the audit
path in the new footnotes resolve.

## New Findings

### FC-1 (blocking): `test_result_status.py` fails at `0df76fc26`

`test_every_registered_result_has_exactly_one_status_from_the_record` asserts that every
result without an `attribution` is `confirmed` from the day it is registered
(`packing/tests/test_result_status.py:175-178`). `T-112` has no `attribution`, and its
latest review is my adversarial review with verdict `defect-open`, so `open_issues`
reports it (`devtools/result_status.py:107-112`) and the status is `incomplete`, as
`RESULTS.md` line 67 shows.
The assertion fails with `T-112`: `assert 'incomplete' == 'confirmed'`. `check_results`
does not see this; the test does, and it is in the register tests the push tier runs.

This is the state the record is designed to pass through, and the fix is to finish
passing through it. **Fix.** Add this document to `T-112`’s `reviews` after the
adversarial review, with `kind: confirming`, `verdict: defects-resolved` and
`covers: [T-112]`, in the form T-101’s fix check takes (`results.yaml:10082-10094`), and
to its `artifacts` and the document map.
`latest_review` keeps the last-listed of two reviews dated the same day
(`result_status.py:121-133`), so the order matters.
Regenerate `RESULTS.md` and `INVENTORY.md`, re-pin, and run the test.
If the owner prefers the result to stay `incomplete` until FC-2 and FC-3 are done, this
document’s verdict is still `defects-resolved` on the findings it checks, and the test
needs the record changed, not the test.

### FC-2 (non-blocking): the stabiliser check lives in prose, and its number is off

`T-112`’s notes say the trivial stabiliser was “checked here numerically, the nearest
non-identity image 0.84 away” (`results.yaml:11576-11577`). Nothing retained performs
the check: no test under `packing/tests/` and no tool under `packing/devtools/` computes
a container symmetry of `cases/trump11/packing.py`, and the claim’s “exactly eight”
rests on my first review’s unretained computation and the lane’s unretained one.
`OR-1` says a measurement never stays in one-off code.

The number is also not what I find.
Measuring an image by the best bijection of its centres onto the packing’s, by the
largest displacement, the nearest non-identity image is the diagonal reflection at
$0.756$; the half-turn, the two axis reflections and the anti-diagonal reflection are at
$0.845$, and the quarter turns at $0.877$. Measuring by the largest distance from an
image centre to the nearest original centre gives the same order.
So 0.84 is the half-turn’s distance, or the nearest image if only rotations were tried;
it is not the nearest of the seven.
The exact fact, that no non-identity element maps the corner set onto itself, is
unaffected.

**Fix.** Retain the check as a test, exact in $\mathbb{Q}(u)$: for each non-identity
element of $D_4$ about the centre, the set of eleven corner sets is not mapped onto
itself (the largest coincidence is four squares, under the anti-diagonal reflection).
Then either drop the number from the notes or state its metric and correct it.

### FC-3 (non-blocking): the paper’s `[^lean]` footnote contradicts its body

Line 1291 of the paper still ends `[^lean]` with “The Squares Project has neither
reviewed nor replayed either formalization.”
The body it annotates now says the project’s statement audit of October 6 reads
`ElevenSquare.optimality` as exactly $s(11) = T$ (lines 1014 to 1017), and `T-060`’s
notes record that the statement closure and the upper half were built here
(`E-n011-lean-statement-closure-build`, `results.yaml:5317-5318`). That is a review of
the statement and a partial replay.
The sentence was true in v0.1.5 and is the same shape of staleness as U-2.

**Fix.** “The Squares Project has audited the statement of 11SquaresFormalized’s theorem
and built its statement closure and upper half, and has replayed neither proof in full.”

### FC-4 (non-blocking): the stack is one merge of main behind

`origin/main` moved to `4261f6809` after the branch’s last merge of main (`3cffade43`,
from `b6f8993f3`). The difference is PR #393 (`29fef4e20`), which rewrites the X
attribution of the Lean announcement in `n-011.md`’s Lean paragraph, `T-060`’s notes,
`bibliography.yaml` and the Lean packet’s `README.md`, and adds two tweet receipts.
The branch changes none of those passages: `git diff b6f8993f3..HEAD` on the
bibliography and the packet is empty, and its `n-011.md` Lean paragraph is
`b6f8993f3`’s. So `git diff origin/main..HEAD` shows the branch deleting two receipts
and un-naming the announcer, which it does not intend.
The branch edits `n-011.md` lines 206 to 214 and `T-060`’s notes region, both near what
#393 changed, so the next merge will conflict there.

**Fix.** Merge main once more and take main’s side in all four files.
The paper’s new sentence, “On October 6 Queuingtheorydotcom reported the formalization
in 11SquaresFormalized complete” (line 1011), is consistent with #393’s attribution and
with the repository’s own verification report, and needs no change.

## Not Checked

- The 2,180 exclusions, the D4 search, the capture branches and the focused-rectangle
  arithmetic, which are T-060’s and were not the subject of either review.
- `test_overview.py` and the generated site, which my worktree cannot build without the
  `kpress` submodule; I read the `RESULTS.md`, `INVENTORY.md`, `VERIFIERS.md` and
  `SYNOPSIS.md` rows in the diff instead.
- The Lean formalization’s build; I read `Optimality.lean` and the verification report
  from the retained packet, not over the network.
- Whether the stored adversarial review is byte-identical to what I wrote.
  The register says it is stored as written; `.flowmarkignore` does not exclude it, so
  the commit hook may have reflowed it, which changes no finding.
- The `DATA_REVISION` pin and `STATUS.md`.

defects-resolved

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
