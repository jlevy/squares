# Review: The Uniqueness of Trump’s Eleven-Square Packing (T-102)

**Reviewer.** Fable, adversarial mathematical review, separately prompted.
I shared no context with the lane that registered the result (think-d1bd) beyond the
brief and the committed record.
The brief asked me to refute, or find gaps in, the claim; I worked from the pinned proof
text, the upstream notes it cites, the receipts, and my own exact computations.

**Date.** 2026-10-06.

**Subject.** T-102 in `packing/frontier/results.yaml` (lines 10133 to 10212) and
`E-n011-optimum-uniqueness` in `packing/frontier/evidence.yaml` (lines 758 to 862), at
commit `5ecb1307b` on `claude/gallant-allen-nvd2jf`, the head of PR #392; with the
commit’s edits to `README.md`, `epistemics.md`, `packing/frontier/n-011.md`,
`packing/devtools/check_results.py` and the schema, read with `git show 5ecb1307b`.

**Scope.** Whether every premise of T-060’s proof holds at side exactly $T$, so that the
endpoint argument forces Trump’s construction instead of a contradiction; whether the
symmetry bookkeeping (eight container symmetries, relabelling, the per-square quarter
turn) is exactly right; whether a rattler or a continuous family survives; whether the
registered text, rungs, kind and significance are accurate.
I checked the PR against `origin/main` (`b6f8993f3`) as well, since the PR branches from
`4148483da` and main has moved.

**What I read.** `packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md` in
full (sections 1 to 15). The four upstream notes the proof cites but the packet does not
retain, fetched over HTTPS at the pinned commit `f9e0de7`:
`src/evidence/research/candidate-capture/CANDIDATE438_CAPTURE.md`,
`src/evidence/research/global-math/FOCUSED-LOCAL-RECTANGLE.md`,
`src/evidence/docs/D4-BRIDGE-THEOREM.md`,
`src/evidence/docs/V9_CONTINUUM_SCOPE_REVIEW.md`, and the capture consumer
`audit_complete_capture438.py`. The GPT-6 Pro unified review (sections 2.4, 3.1 and S7)
and its two source reviews, the upstream-delta review’s row “Conditional uniqueness
corollary”, the paper template’s closing section,
`packing/cases/trump11/isolation-theorem.md`, T-036 and T-060 in the register,
`epistemics.md` (Verification, Confirmation, Scope and Composition, Significance, Result
Kinds), the pose-inclusion receipt, Stromquist 1984 II and 2003 in the archive, and the
Lean repository’s `README.md`, `docs/VERIFICATION_20261006.md` and
`ElevenSquare/Optimality.lean` at `cdc746ed9`.

**What I ran.** From `packing/`, with the project interpreter:
`devtools.check_n11_final_composition` to a fresh receipt path, which returned
`PASS_REVIEWED_COMPONENT_COMPOSITION` with no pending obligation and 2,180 of 2,180
exclusions in about three seconds; `devtools.check_results`, which accepts all 102
results at this commit; and an exact computation in $\mathbb{Q}(u)$ of which of the
eight container symmetries map the construction of `cases/trump11/packing.py` onto
itself (script in my scratchpad, not retained).
No geometry was rerun.

**Verdict line.** The mathematics holds.
Every statement the corollary needs is stated upstream for side $S \le T$ or for every
packing in the cap $U$, the rigid map sends a centred side-$T$ container onto $[0,T]^2$
exactly, and the local isolation lemma is a statement about every feasible packing in
the fixed $[0,T]^2$ container on all 33 coordinates, so at $S = T$ it returns the
labelled construction rather than a contradiction.
The symmetry bookkeeping is exactly right.
I found no gap. Two findings block the merge, neither mathematical: the id `T-102` is
already taken on `origin/main`, and the commit’s two Lean sentences contradict the Lean
import that main merged in PR #391. Seven non-blocking findings follow, and I propose S3
in place of S4.

## The argument at side exactly T, re-derived

Let $P$ be a packing of eleven unit squares in $[0,T]^2$. Each step below names where
the premise is stated and why it does not use $S < T$.

1. **Embedding.** `PROOF.md` section 3 (lines 143 to 151) says “Suppose a counterexample
   packing has side S<T” and centres its container in $[0,U]^2$. The operation needs
   only $S \le U$, and $T < U$ is proved exactly (line 134). The centre chart
   $z = (p - (1/2,1/2))/(U-1) \in [0,1]^2$ (line 161) needs only that each square lies
   in $[0,U]^2$. `D4-BRIDGE-THEOREM.md` line 135 states the bridge for “a packing at a
   side S<=U”.
2. **Exclusions.** Section 5 proves each of the 2,180 cases “impossible for a packing in
   the U-container” (line 235). `V9_CONTINUUM_SCOPE_REVIEW.md` line 45 shows the wall
   inequalities the certificates use are those of the field side $L$, the cap, not of
   the packing’s own container, and line 88 states the scope: “a continuum exclusion at
   rational U for its named case, allowing arbitrary independent rotations, closed cell
   boundaries”. No certificate sees the side the packing came from.
3. **D4 reduction.** Section 6 and `D4-BRIDGE-THEOREM.md` lines 132 to 168 act on “every
   D4 image of a feasible packing” in the centred $U$-frame.
   D4 about the centre of $[0,U]^2$ preserves the concentric $[0,T]^2$, which section 10
   says in so many words (line 622). Some image $g(P)$ admits exactly $J_{438}$.
4. **Capture.** Section 8 lines 500 to 513: the four branches are closed, overlap at
   equality, and are stated “at the rational cap”.
   The three far branches are contradictions for any cap-$U$ packing with that
   antecedent; the near state “contains every surviving pose”.
   `CANDIDATE438_CAPTURE.md` lines 24 to 27 states the conclusion: “Every packing of
   eleven unit squares with side $S \le T$ satisfying this antecedent is the known exact
   construction, up to the specified quarter-turn and the associated label assignment.
   Consequently it has $S = T$.” The capture consumer binds the same scope string
   (`audit_complete_capture438.py` line 281: “every packing at side S<=T is the known
   exact construction after the displayed quarter-turn”).
5. **The rigid map.** Section 8 line 529: $p_T = Q^{-1}(p_f/B - (U/2,U/2)) + (T/2,T/2)$.
   After unscaling by $B$ this is a quarter turn about the centre followed by the
   translation $(U/2,U/2) \mapsto (T/2,T/2)$, so the concentric $[(U-S)/2,(U+S)/2]^2$
   goes to $[(T-S)/2,(T+S)/2]^2$, which is $[0,T]^2$ exactly at $S = T$. The proof says
   so (lines 533 to 535: “A packing centered in a square of side S<=T is mapped by this
   rigid coordinate change into [0,T]²”), and `FOCUSED-LOCAL-RECTANGLE.md` line 15: “A
   packing in a centered container of side S <= T satisfies the T-frame wall
   inequalities.”
6. **Pose inclusion covers all 33 coordinates.** The retained receipt
   `receipts/pose-inclusion/result.json` lists eleven owners mapped bijectively to
   labels 0 to 10, 136 live rows and 1,542 vertices, each owner with its three required
   radii; `FOCUSED-LOCAL-RECTANGLE.md` lines 31 to 36 encloses every centre polygon by
   convexity and every angle interval, with the quarter-turn chart change for axis
   squares near $t = 1$ (line 25).
7. **Local isolation is a fixed-container statement.** Section 7 line 396: “with its
   container fixed as [0,T]² and with its eleven square labels fixed”, 33 coordinates.
   The conclusion (lines 485 to 487): “only the zero perturbation is feasible in the
   rectangle. This argument also excludes nonzero perturbations on its boundary.”
   Feasibility there is the necessary subsystem of the fourteen contact pairs and the
   wall rows (lines 411 to 413), which only weakens what a real packing must satisfy.
   `FOCUSED-LOCAL-RECTANGLE.md` line 95 says it directly: “the rectangle contains only
   the exact candidate packing at side T, and no packing at a smaller side.”
   So $\varphi(g(P))$ is the labelled construction $C$, and a rattler or a one-parameter
   family would be a nonzero feasible perturbation inside the rectangle, which this
   excludes.
8. **Reading back.** $P = g^{-1}\varphi^{-1}(C)$. Undoing the translation to the
   original frame, the composite is $p \mapsto (T/2,T/2) + g^{-1}Q\,(p - (T/2,T/2))$
   with $g^{-1}Q \in D_4$, the formula GPT-6’s S7 gives with the roles named.
   Section 10 uses $S < T$ only at “contrary to S<T” (line 624); at $S = T$ nothing is
   contradicted and $P$ is a container symmetry of $C$ with the capture’s label map as
   the relabelling.

**Symmetry bookkeeping.** Reflections enter through the D4 bridge’s four views and their
half-turn images (section 6 lines 332 to 337), so $g$ may be a reflection and the
claim’s “eight symmetries” is the right group.
The per-square quarter turn is handled in the chart (section 3 lines 163 to 175, section
8 lines 518 to 520). Nothing in the chain identifies two packings by anything other than
a rigid container symmetry and a relabelling.
I computed the stabiliser of the construction exactly: no non-identity element of $D_4$
maps the eleven squares onto themselves, so the optimal packings are exactly eight as
unlabelled configurations.

**T-036’s equality clause.** A packing in T-036’s family at side $T$ is $g(C)$ with
$g \in D_4$; a reflection sends the tilt $\theta^*$ to $\pi/2 - \theta^*$, whose
half-tangent 0.464 is outside T-036’s box, so $g$ is a rotation, and a rotation
preserves the axis and tilted classes, so the relabelling is within the two classes.
The supersession text is right.

## Findings

### U-1 (blocking): `T-102` is already allocated on `origin/main`

PR #392 branches from `4148483da`. Main merged lane R7 (PR #390, `ac18486aa`) afterwards
and renumbered wand125’s ten check2 certificates to `T-102` to `T-111`; on `origin/main`
(`b6f8993f3`) `packing/frontier/results.yaml` line 10116 is `T-102`, kind `lower-bound`,
“Mixed rectangle-measure lower bound verified at `n = 18`”, and the register holds 111
results.
The uniqueness result cannot merge as `T-102`; two entries would share an id and
the checker and `test_results_register.py` would refuse the file.

**Fix.** Renumber to `T-112`, the next free id on main, in every place the commit writes
`T-102`: `results.yaml` (the entry, T-036’s `superseded_by` and `notes`, T-060’s
`notes`), `evidence.yaml` (nothing cites the id there, but check), `README.md`,
`SYNOPSIS.md`, `n-011.md`, the generated `RESULTS.md`, `INVENTORY.md` and
`VERIFIERS.md`, and the five tests (`test_overview.py`, `test_recent_results.py`,
`test_result_status.py`, `test_results_register.py`, and the `Supersession` tuple).
Then regenerate and re-pin.

### U-2 (blocking on rebase): the Lean sentences contradict the import main already holds

The commit adds to `README.md` (lines 35 to 40 of the diff) and to T-060’s `notes` a
paragraph saying Queuingtheorydotcom reported a complete Lean 4 formalization and “This
project has not yet reviewed or replayed it.”
PR #391 (`claude/ecstatic-pascal-pothtx-n11lean`), merged to main at `b6f8993f3`,
retains that formalization as a packet
(`packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/`), registers
`E-n011-lean-formalization-report` and `E-n011-lean-statement-closure-build`, cites them
from T-060, and files a statement audit
(`docs/project/reviews/review-2026-10-06-n11-lean-formalization-statement-audit.md`);
main’s `README.md` line 42 and `n-011.md` lines 212 to 224 already carry the
announcement with those records.
After a rebase the PR’s sentences would be false ("not reviewed") beside main’s audit,
and the README would say the same thing twice in different words.
The PR also edits `n-011.md` line 203, which main changed in the same region, so the
rebase will conflict there and the resolver needs to know which version to keep.

The numbers in the PR’s sentences are otherwise accurate: I read the Lean repository’s
`README.md` and `docs/VERIFICATION_20261006.md` at `cdc746ed9`, which give 7,920
accepted modules, zero admissions, `propext`, `Classical.choice`, `Quot.sound` plus the
13,308 native-certificate dependencies, and the trust model
`lean_kernel_and_native_compiler`.

**Fix.** On rebase, drop the PR’s README paragraph and its T-060 `notes` paragraph and
keep main’s. In T-102’s `next_rung`, replace “once that formalization is reviewed here”
with a pointer to the statement audit, and say what I read in
`ElevenSquare/Optimality.lean`: it states `optimal_side_lower_bound` ($T \le S$ for
every packable $S$) and `optimality` only.
No Lean statement of the equality case exists, so rung 5 for this result needs a new
theorem there, not a review of the existing one.

### U-3 (non-blocking): the paper still says the project registers only optimality

`packing/devtools/templates/n11-optimality-review-article.md` lines 951 to 953: “The
Squares Project registers only the optimality statement; the uniqueness corollary rests
on the same evidence and has had no separate review.”
Both halves are stale at this commit, which lists the paper among T-102’s artifacts.
The upstream-delta review’s row 113 says the same, but that is a dated review and may
stand.

**Fix.** Point the sentence at the registered result and at this review, and bump the
paper’s version note.

### U-4 (non-blocking): the quoted case-438 note is not in the retained packet

`evidence.yaml` line 855 and `INVENTORY.md` line 450 quote
`src/evidence/research/candidate-capture/CANDIDATE438_CAPTURE.md`. The pinned packet
retains only `PROOF.md`, `README.md`, `THIRD_PARTY_NOTICES.md` and `docs/`, and the LFS
inventory does not list the note.
I fetched it at `f9e0de7` and the paraphrase is faithful (its lines 24 to 27, quoted
above). The record should not depend on a file a reader cannot open from the repository.

**Fix.** Either retain the note in the packet’s `source/` with its digest, or cite the
retained wording instead: `PROOF.md` section 9F, “accepted for every packing of side
S<=T satisfying its closed-cell antecedent in the centered U-frame” (lines 596 to 599),
which says the same thing.

### U-5 (non-blocking): significance reads as S3 under the anchors

`epistemics.md` anchors S4 at “A reusable technique, bound family, or resolved disputed
value” and S3 at “A substantive case result or machine audit”.
T-102’s own rationale says it “moves no bound and adds no method”.
A complete classification of the optimum at the central case is a substantive case
result, above T-036 (S3, restricted to one family) but of the same kind; T-052 and
T-053, the S4 entries nearest in the table, settle values.
I propose S3. If the owner reads “completes the classification at eleven squares” as a
resolved disputed value, S4 is defensible, and the choice changes no validation
behaviour.

### U-6 (non-blocking): the `uniqueness` kind is defined for one packing only

`epistemics.md` line 381 defines the kind as “each is one named packing up to the
container’s symmetries and the relabelling of the squares”.
The novelty basis itself notes that $n = 10$ has three optimal packings (Stromquist 1984
II, Figure 1), so a classification there would have three named packings and would not
fit the sentence. The four-rule chooser is otherwise coherent: the new third rule
separates a classification from a second optimality by what the claim concludes, and the
checker’s `STRUCTURE_KINDS`, the schema enum and the rubric table agree.

**Fix.** “each is one of finitely many named packings, up to ...”.

### U-7 (non-blocking): the input evidence and the verifier roles

Three bookkeeping points on `E-n011-optimum-uniqueness`:

- T-102’s `evidence` cites only the new entry; T-060’s
  `E-n011-global-optimality-independent` is cited only inside the new entry’s
  `assumptions`. `epistemics.md` says a derived claim takes the minimum rung of its
  inputs and the derivation, which the composition note states correctly (V3/C2), but
  the input is not machine-visible from the result.
  `check_results._evidence_needed` allows extra cited claims, so citing the input as
  well costs nothing.
- `VERIFIERS.md` now counts `V-n11-optimality-checkers` as deciding two claims.
  Neither program decides the step this entry adds, which is prose; both check T-060’s
  premises. The entry’s `replay` text says so; the verifier table does not.
- The entry’s `certificate` is T-060’s `final-composition.json`, whose
  `endpoint_argument` string reads “Concentric embedding of any S<T into U …
  contradicting S<T” and whose flag is `global_optimality_proved`. It certifies T-060,
  not the uniqueness step; the entry’s `limitations` concede this.
  A reader who follows the `certificate` path alone will find a receipt that says `S<T`.

**Fix.** Cite the input entry from T-102; mark both verifiers as `premises` for this
entry in the verifier register, or say in the `certificate` field’s neighbour text that
the receipt is T-060’s.

### U-8 (non-blocking): T-060’s note miscounts the native certificates

T-060’s new `notes` paragraph says “13,308 approved native_decide certificates”.
The verification report separates “Approved numerical declarations: 10,464 in 1,839
source files” from “Generated native certificate axiom dependencies: 13,308”, and its
prose says the axiom reports contain “the 13,308 approved native dependencies”.
Main’s own paragraph says “13,308 `native_decide` axioms”, which is the report’s
meaning. Moot if U-2 drops the paragraph.

### U-9 (non-blocking): two facts worth recording

- The stabiliser of the construction in $D_4$ is trivial, by exact computation in
  $\mathbb{Q}(u)$ (no rotation or reflection about the centre maps the eleven squares
  onto themselves). So there are exactly eight optimal packings as unlabelled
  configurations, one per container symmetry.
  The claim’s “one of the eight symmetries” is right; the record could say “exactly
  eight”.
- “At n = 10 Stromquist 1984 and 2003 give three optimal packings”: the count is in the
  1984 memo (`stromquist-1984-...-ii-ten-unit-squares.raw.md` line 50, “THREE PACKINGS
  OF TEN UNIT SQUARES”); the 2003 paper says “The 10-square packings in Figure 1 are
  optimal” and its figure is not in the retained transcription.
  Cite 1984 for the number.

## What held, item by item against the brief

1. Every premise of `PROOF.md` sections 3 to 10 holds at $S = T$; the only use of
   $S < T$ is the final contradiction (section 10 line 624). The exclusion certificates,
   the D4 lemma and the candidate theorem (section 9F) are stated for the cap or for
   $S \le T$. The upstream notes say the same at their own scope lines, quoted above.
2. The rigid map is onto $[0,T]^2$ at $S = T$; local isolation is stated for every
   feasible packing in the fixed container, on all 33 coordinates, closed rectangle and
   boundary included.
3. “Up to the eight symmetries of the container and relabelling” is exactly right.
   The D4 bridge chooses an image satisfying the antecedent by a rigid symmetry only;
   reflections are among the views; the per-square quarter turn is a chart change.
   The construction has no symmetry, so the orbit has eight members.
4. No rattler and no family: a nonzero feasible perturbation in the rectangle is
   excluded, and pose inclusion puts every surviving pose of every owner in the
   rectangle.
5. The claim, scope, pinpoints and assumptions are accurate: unit squares, disjoint
   interiors, boundary contact, independent rotations.
   Section numbers are right.
   Commit `1676145d5` is the v0.1.2 paper commit whose message says “states the
   uniqueness corollary conditionally”.
   The quoted case-438 statement matches the upstream note.
   The GPT-6 review’s 2.4 and S7 say what the record says they say, including that the
   review “does not transform the unexecuted parts of the global chain into a fresh
   verification of uniqueness”.
   Trump 2023 (lines 10 and 50 of the transcription), DS7 and the Kingbird catalogue
   call the packing rigid, which is local, as the novelty basis says.
   No earlier project review states the global corollary; the two pre-October mentions
   of “uniqueness” in the review directory are about $n = 17$.
6. V3 (proof-audited with a proof block) and C2 (confirming-origin, replay command
   passing, a method yielding no certificate) match the ladders; C does not exceed V.
   The checker accepts the entry.
7. T-036’s supersession text, `n-011.md`’s “Unique” paragraph and “superseded in part by
   each and in whole by the two” are correct.

## What I did not check

- The 2,180 exclusions, the D4 search, the capture branches and the focused-rectangle
  arithmetic themselves.
  They are T-060’s, replayed and reviewed there; I re-derived only that their stated
  scope admits $S = T$, which is the step T-102 adds.
- The Lean formalization’s build or axiom receipt.
  I read its README, report and the 600-byte `Optimality.lean` at the cited commit over
  the network; the repository’s own statement audit is main’s, not this PR’s.
- The generated site output, `STATUS.md`, and the DATA_REVISION pin.

## Significance

Proposed: S3, for the reason in U-5. If kept at S4, the rationale should name what S4
anchor it claims.

defect-open

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
