# Review of the Eleven-Square Optimality Paper, v0.1.6

**Date:** 2026-10-07\
**Submission:** Guzhou0806\
**Lead reviewer and adjudicator:** GPT-6 Astra Pro\
**Tracking:** `think-e4a1`\
**Workflow:** W2 factual review and authorized bounded exposition corrections.

## Verdict and Scope

The reviewed proof interfaces remain supported by the inspected evidence and the
selected fresh component checks below.
This review found seven bounded exposition issues, including one incompletely resolved
October 3 finding. All seven are addressed in the accompanying v0.1.7 article revision.
None requires changing the accepted certificate ensemble or the registered optimality or
uniqueness claim.

The baseline is [main at ef79288a4][baseline], and the subject is the complete
[v0.1.6 article][article], its figures and references.
The review follows the [paper design rules][design], especially the n = 11 series’
distinction between masks and cases, definitions before use, and evidence-based figure
text. Earlier findings were checked against the October 3 reviews and
[integration dispositions][integration], the [v0.1.4 change record][v014], and the
October 6 [uniqueness][] and [Lean statement][lean-audit] audits.

Three separately prompted GPT-6 Astra reviewers examined the global argument, local
algebra and endpoint, and exposition and assurance statements.
They received the pinned sources and task boundaries without the coordinator’s candidate
findings. All three used `xhigh`; the harness rejected the repository’s requested `max`
setting before those reviews started.
Their reports were evidence for the lead reviewer’s adjudication, not automatic
findings. This is AI review, with no new human oversight record and no change to T-060’s
S5/V3/C3 or T-112’s registered assurance.

This review does not claim a fresh execution of all 2,180 exclusions and ten capture
nodes. In particular, retained-receipt composition, fresh component geometry and a full
Lean build are different checks; the table below records which occurred.

## Findings and Dispositions

Locations refer to the baseline article, before the accompanying edits.
Severity uses the repository’s Blocker/High/Medium/Low vocabulary.
No Blocker or High finding was established in this bounded review.

| ID | Severity | Location | Disposition |
| --- | --- | --- | --- |
| F1 | Medium | Construction, lines 197–199 | Correct the inference from zero projection gap to contact; completes October 3 finding 9 |
| F2 | Low | Contact polynomial, lines 215–221 | Restrict the explanatory deformation to a neighborhood of the selected root |
| F3 | Medium | Symmetry introduction, lines 615–619 | Distinguish a raw mask from its numbered half-turn case |
| F4 | Medium | Shorter symmetry proof, lines 679–683 | Correct the intermediate counts and state both propagation rules |
| F5 | Low | Figures 6 and 8, lines 388–399 and 551–562 | Put the existing figures after their symbols are defined; identify the sum denoted by $K-Q$ |
| F6 | Medium | Independence limitation, lines 987–990 | Name the shared global geometric primitives already listed in the registers |
| F7 | Low | Lean status transition, lines 1000–1017 | Separate this project’s full-replay status from the dated source completion report |

### F1: A Zero Projection Gap Does Not Establish Contact

The construction’s squares 0 and 4 already refute the baseline implication.
They are $A(0,0)$ and $A(1,T-1)$. Their horizontal projections, $[0,1]$ and $[1,2]$,
have gap zero, while their vertical projections have gap $T-2>0$. The squares are
strictly separated. The [local theorem][local-theorem] also identifies this incidental
zero projection, and the exact witness checker correctly counts the pair among the 41
strictly separated pairs.

The valid separating-axis criterion accepts a nonnegative gap in any edge-normal
direction. Actual contact is characterized by the *largest* gap over the edge normals of
both polygons being zero.
The revision states those two facts separately.

This is [October 3 paper review][oct3] finding 9, whose wording changed without removing
the false implication.
It is recorded here as an incomplete earlier correction, not as a new defect in the
witness or local-isolation computation.

### F2: The Contact Deformation Is Local

The baseline treats $u$ as a free parameter and concludes that smaller values make
squares 2 and 10 overlap.
Substituting $u=1/10$ into Appendix A gives $T(u)=460/119$, and the two squares have
vertical projection gap $57039/48076>0$. This refutes the unrestricted pair-overlap
assertion. It does not describe a feasible eleven-square packing, and it says nothing
against the optimum.

The intended local statement is supported.
At the selected algebraic root, seven of the pair’s eight separation features each have
a strictly negative corner inequality.
The remaining feature, supplied by square 10, has corner signs $(+,0,+,+)$; its tied
corner is exactly the displayed function

$$
\frac{p(u)}{2u(1-u^4)(1+2u-u^2)}.
$$

Continuity keeps the other seven features unavailable in a neighborhood of the root.
The denominator is positive there, and the already stated $p'>4$ makes the tied gap
negative just below the root.
Thus no feature separates the pair there.
The revision says that $u$ is varied near its selected root and that overlap occurs just
below it. It preserves the contact identity without asserting a global parameter range.

These checks used the displayed Appendix A formulas with rational arithmetic and exact
algebraic signs. Symbolic cancellation verifies the contact identity.
As a separate check on the derivative, bounding each monomial on the rational isolating
interval gives

$$
p'(u)-4\ge\frac{398878171521}{2500000000000}>0
\quad\text{on }[9/25,37/100].
$$

### F3: A Half-Turn Preserves the Case, Not the Raw Mask

The article defines a mask as an eleven-element subset of the sixteen cells and proves
that no such subset is fixed by the half-turn.
Its later claim that the identity and half-turn give the same mask therefore conflicts
with its own definitions.

For example, case 1462’s representative and its half-turn are

$$
\begin{aligned}
J&=\{0,1,3,5,6,8,9,11,12,13,14\},\\
H(J)&=\{1,2,3,4,6,7,9,10,12,14,15\}.
\end{aligned}
$$

They are different masks in the same numbered case.
The [cover checker][d4-checker] computes that distinction explicitly.
The revision calls the four numbered outcomes *cases*. Later uses of actual masks and
their half-turns remain appropriate; a global word replacement would obscure the
enumeration’s six raw non-438 masks.

### F4: The Shorter Symmetry Proof Needs the Correct Census and Both Rules

The [retained incidence receipt][incidence-receipt] and a fresh execution of its
[checker][incidence-checker] give the following census:

| Identity case | Triples | Immediate contradictions | Entering propagation | Further contradictions | Final survivors |
| --- | ---: | ---: | ---: | ---: | ---: |
| 999 | 216 | 168 | 48 | 47 | 1 |
| 1462 | 216 | 198 | 18 | 17 | 1 |
| 1659 | 216 | 196 | 20 | 20 | 0 |

The article used the further-contradiction counts, 47, 17 and 20, for the preceding
survivor counts. The revision gives 48, 18 and 20.

Its description also gave only the singleton-owner rule.
The checker’s `propagate` function repeats two sound rules: an owner confined to one
region reserves that region’s labels, and a view label available from only one owner
forces that owner to keep only regions carrying that label.
Either an empty owner domain or an unsupported required label is a contradiction.
The revised paragraph states both rules and their iteration before reporting one, one
and no survivors.

This is the supplementary shorter proof.
The accepted composition uses the [exhaustive D4 check][d4-receipt], which also passed
afresh in this review.
Neither the correction nor the supplementary incidence check replaces that accepted
premise or removes the earlier baseline-dependent cuts for cases 2175 and 2176.

### F5: Figures Must Follow Their Definitions

Figure 6 previously introduced $x$, $K$, $Q$ and $K-Q$ before the body explained the
center, owned hull, strict core and forbidden-center sum.
Figure 8’s drawing used $O$, $P$ and $J$ before the subsequent transfer paragraph
defined them. The series’ reading-order rule applies to the whole figure, including its
drawing.

The revision moves Figure 6 after the collision derivation and writes $K-Q=K+(-Q)$
explicitly there. Its caption uses the already established “current assumptions.”
Figure 8 follows the transfer rule and its definitions.
Their data, numbering and geometric drawings are preserved.

The term checker skips SVG labels, and the baseline term registry does not cover these
particular symbols. A passing term check alone therefore cannot establish this part of
the reading-order audit.
The source ordering and rendered figure positions must also be inspected.

### F6: State Which Global Geometry Is Shared

The baseline limitation names shared local construction, derivatives and exact
arithmetic. The [evidence register][evidence] and [verifier record][verifiers] also
explicitly name shared exact clipping, closed-cover and collision kernels, which the
publisher bundles. These are part of global exclusion and capture checking.

The revision names those routines alongside the local primitives.
Independently written consumers remain distinct from independently implemented deciding
primitives; the description of the former is preserved.
This completes the scope clarification sought by October 3 finding C8 without reopening
its deferred independent-kernel work or reclassifying the existing confirmation.

### F7: Reconcile the Lean Transition with the Dated Report

The undated statement that both formalizations are “in progress” precedes the report
that Queuingtheorydotcom completed one on October 6. The revision introduces the two
projects neutrally and identifies this project’s limitation as the absence of a full
proof-assistant replay.

The [October 6 statement audit][lean-audit] supports the existing distinctions: the
theorem matches $s(11)=T$, the statement closure and upper half were built here, the
full run is reported by the source, and the numerical certificates trust Lean’s compiler
as well as its kernel.
The dated reports, private-run limitation, native-certificate trust base and unchanged
rungs remain explicit.
The already corrected footnote is not raised again as a defect.

## Proof Coverage and Verification

All project Python checks used the pinned Python 3.14.7 environment.
The fresh component checks used the retained inputs and existing consumers; they are not
new independent implementations of all arithmetic or geometric primitives.

| Obligation | Work performed and result | Scope of that evidence |
| --- | --- | --- |
| Algebra and attaining construction | Exact witness passed: 11 unit squares, 55 pairs, 14 touching and 41 strictly separated pairs, 20 wall coordinates; exact algebra confirmed one positive root, irreducibility and degree eight | Upper bound and the displayed construction; separate rational substitution supports F2 |
| Closed cover and symmetry | Accepted D4 consumer passed: 4,368 masks, 2,184 cases, 220 closed regions and 1,572 strict bans; all three assignment problems infeasible | Fresh geometry for this conditional D4 implication, with earlier exclusions still premises |
| Supplementary incidence bridge | `PASS_D4_INCIDENCE_BRIDGE`; the census in F4 was reproduced | Fresh cover/overlay reconstruction and propagation; supplementary, not a composed premise |
| Five-site field certificate | Full mask-0 consumer passed: 55 owned points, all 136 rows and 459 transferred cases, no pending rows | One complete certificate; the other field certificates were not all rerun |
| Local isolation | `PASS_INDEPENDENT_FIXED_T_LOCAL_ISOLATION`; 112 features, 24 available and 88 unavailable, 512 feature selections, 128 systems, all 8,448 signed-coordinate margins | Full fixed-$T$ local component; worst ratio agrees with the retained approximately 0.676505208 |
| Pose inclusion | Recomputed inclusion from the hash-verified retained compact extraction: 136 rows and 1,542 vertices | Conditional on that extraction; the unretained original near-state file was not fetched and re-extracted |
| Global state joins | Final composer returned `PASS_REVIEWED_COMPONENT_COMPOSITION`, all 2,180 exclusions present, no pending obligations, `geometry_rerun: false` | Retained execution identities and reviewed joins; no fresh global exclusion/capture run |
| Endpoint and uniqueness | Reviewed the rigid cap-to-$T$ map, role bijection, angular charts, opposite-wall span and the same deduction at $L_0=T$ | The stated complete exclusion/capture premises support both deductions; no new theorem is registered |

The [validation guide][validation] gives portable commands and decoded input locations
for these existing consumers.
Representative commands, from `packing/`, are:

```sh
uv run --frozen --all-extras --group dev python -m cases.trump11.verify_exact
uv run --frozen --all-extras --group dev python -m devtools.check_n11_optimality_d4_incidence --output "$OUT/d4-incidence.json"
uv run --frozen --all-extras --group dev python -m devtools.check_n11_optimality_local_isolation --weighted "$OUT/local-weighted.json" --focused "$OUT/local-focused.json" --branch-limit 128 --max-seconds 60 --output "$OUT/local-isolation.json"
uv run --frozen --all-extras --group dev python -m devtools.check_n11_final_composition --out "$OUT/composition.json"
```

Use a fresh output directory and decode the local input objects as the validation guide
specifies. A full PASS status and complete coverage matter in addition to process exit.
For example, a one-branch local run is not the 128-branch result above.

## Earlier Concerns Checked Without Reopening Them

| Concern | Current disposition and reason |
| --- | --- |
| Frozen singleton interval helper | The defect is disclosed. Accepted positive-area callers use complete interior slices and closure; degenerate domains are separately checked or refused. No newly reachable unsound use was established |
| Angular seams and loose outer poses | The invariant is rowwise at shared endpoints and ownership is quantified over valid packings. The earlier C1 and C7 distinctions are present |
| Field charge versus holding three sites | The median, half-plane and three-site-hull forms and the no-site example distinguish these predicates; capacity and strict transfer are stated |
| Capture counts | Four terminal branches, ten dependency nodes, fourteen root rounds and thirteen complete root-node updates are different objects. The partial fourteenth update is disclosed |
| Baseline and final D4 dependency | The 1,931-case premise belongs to the accepted cuts for 2175 and 2176; their use precedes the final four-survivor reduction. The baseline-free Lean claim is separately attributed |
| Full replay and formalization | The article already separates retained composition from fresh geometry and source-reported Lean completion from an observed full build |
| Assurance and uniqueness | The current records govern the rungs. Neither this AI review nor an ordinary PR approval substitutes for the required human oversight or independent expert formalization review |

## Revision and Submission Checks

The patch changes the article, its own version and revision date, this review’s
documentation-map entry and generated synopsis row.
It also preserves the task record through the supported outbox recovery.
The theorem, proof consumers, frozen input objects and accepted receipts keep their
existing meanings. A wider rewrite or replacement proof is not needed to address these
findings.

The review and paper changes receive the existing renderer, figure, term, structure,
release and artifact-date tests.
The artifact-date checks must run after the article’s commit, because their authority is
Git’s last change date.
Repository and hosted validation, rendered artifact inspection, and the exact submitted
revision are recorded in the pull request’s Validation section; a proposed or running
check is not a pass.

This host initially blocked two unchanged record checks when Python’s forkserver tried
to create a Unix socket, and the pinned Chromium download returned an unavailable-site
page. Those environmental failures are not mathematical failures.
They remain explicit until equivalent checks on the submitted revision have completed on
a supported host.
Native Git push also lacks command-line credentials here, so submission
uses the authenticated GitHub connection; any unsynced bead record is preserved through
tbd’s documented outbox recovery rather than a hand-edited sync branch.

[baseline]: https://github.com/jlevy/squares/tree/ef79288a498b5469e6b944f7b150d83aeeab5f94
[article]: https://github.com/jlevy/squares/blob/ef79288a498b5469e6b944f7b150d83aeeab5f94/packing/devtools/templates/n11-optimality-review-article.md
[design]: ../../../packing/devtools/templates/paper-design.md
[integration]: review-2026-10-03-n11-gpt6-pro-review-integration.md
[v014]: review-2026-10-04-n11-optimality-paper-v0.1.4-changes.md
[uniqueness]: review-2026-10-06-n11-uniqueness-fix-check.md
[lean-audit]: review-2026-10-06-n11-lean-formalization-statement-audit.md
[oct3]: review-2026-10-03-n11-optimality-paper-adversarial.md
[local-theorem]: ../../../packing/cases/trump11/isolation-theorem.md
[d4-checker]: ../../../packing/devtools/check_n11_optimality_d4.py
[d4-receipt]: ../../../packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json
[incidence-checker]: ../../../packing/devtools/check_n11_optimality_d4_incidence.py
[incidence-receipt]: ../../../packing/resources/web/n11-optimality-2026-09-29/receipts/d4-incidence/result.json
[evidence]: ../../../packing/frontier/evidence.yaml
[verifiers]: ../../../packing/frontier/verifiers.yaml
[validation]: ../../../packing/resources/web/n11-optimality-2026-09-29/VALIDATION.md

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
