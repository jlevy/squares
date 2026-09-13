# N11 Strategy Audit for the BC329 Closeout

Source-distinct mathematical review for think-7kwu, September 12, 2026. Reviewed at Git
revision `5fa83cc723579c7fa469e81fed354773bd85d6d6`, including the PR148 and PR149
stack. No scientific target, certificate replay, or validation was run.
This report does not assume a BC329 outcome and does not reclassify retained evidence.

The T-025/T-026 counting and dilation arguments have no soundness defect identified in
this reading. The current plan and X-027/X-028 generally preserve their scope.
The next decision should depend on BC329’s terminal evidence, with a small
direct-certificate discriminator and a structural lane that explicitly carries its
selection obligations.
Neither a pass nor a rejection justifies a method-wide ranking.

## Definitions and Exact Fact Ladder

Let $K_L=[0,L]^2$. A physical packing has eleven contained closed unit squares whose
interiors are pairwise disjoint; touching is legal.
The least feasible side $s(11)$ is attained by compactness of the bounded
centre/orientation space and closedness of containment/non-overlap.

A selected **strict core** is a smaller closed square inside one parent’s interior.
Cores from different parents are therefore disjoint as closed sets.
A finite direction net is sound only with a proved selection rule covering every
physical orientation.
A **pose domain** specifies both orientations and all allowed centres.

A point atom charges $w$ on membership of one site.
A threshold atom $(S,k,w)$ charges $w$ when a core contains at least $k$ distinct sites;
its budget is $w\lfloor |S|/k\rfloor$. This follows because disjoint core traces consume
disjoint sites. A complete certificate has charge at least one throughout its domain and
total budget below eleven.

A **fractional family** gives nonnegative weights to potentially overlapping cores.
It obstructs a certificate language only when its placements belong to the declared
domain and it satisfies every capacity of that language.
Point depth at most one everywhere suffices for arbitrary point measures, but not for
threshold charges.

An **owner** is a selected core containing an admitted near-corner mark; its parent is
not thereby flush with a wall or seated in a literal corner.
A **conditional certificate** excludes a stated owner/contact branch.
Its conclusion becomes global only through complete physical transfer and sufficient
selection coverage.

The proof ladder is:

1. **Analytic theorem.** Symmetry, angular coverage, strict core containment, complete
   pose coverage, and budget $M<11$ give
   $11\le\sum_i\operatorname{charge}(C_i)\le M<11$. For mismatch $d$ with $\tan d\le D$,
   the coarse containment test is $B(1+D)<1$. The exact support factor is
   $(1+D)/\sqrt{1+D^2}$. See
   packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md:33–91.
2. **Finite reduction.** At a fixed direction, point-membership events partition the
   centre plane. Traces are constant on open cells; closed-boundary membership can only
   increase nonnegative charge.
   The retained verifier requires nonempty interior of the admissible centre domain.
   Its inclusion-exclusion sweep is an evaluation device, not permission for negative
   certificate weights.
   See that claim:93–118.
3. **T-025 computational fact.** At $L=191/50$, $B=9977/10000$, and 181 folded
   directions, 584 point atoms and 320 two-of-three atoms have budget
   $685457679/62500000$ and least charge $100000203/100000000$. The exact and interval
   routes retain complete decisions.
   Together with the theorem, this excludes packing at $L$ and yields the registered
   $s(11)\ge3.82$. See that claim:120–155.
4. **T-026 computational fact.** Its own 1441-direction certificate has
   $B_0=249507/250000$ and $D_0=207107/720000000$. Relative weights are unchanged from
   T-025; the multiplier is $500000000/498684619$. Its least charge is one and budget
   $5483661432/498684619<11$. T-026 re-establishes this source certificate directly;
   T-025’s numerical bound is not a logical premise.
   See
   packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md:121–145.
5. **T-026 analytic composition.** Common rational dilation $q$ preserves traces and
   budgets. Every $q^2B_0^2(1+D_0)^2<1+D_0^2$ excludes side $qL$. Rational density and
   upward embedding then exclude every real side below
   $C=955000\sqrt{518400042893309449}/179696714646249=3.826447410572939744\ldots$. Thus
   $s(11)\ge C$ is an ordinary exact lower bound.
   The argument does not decide packing at $C$ or establish $s(11)>C$. See that
   claim:142–202.
6. **Assurance.** V4/C5 describes the retained exact/interval evidence and mapped
   review, not a formalized proof-assistant theorem or independent rediscovery of every
   premise. The event sweep and interval route share bytes and analytic premises.
   The standalone verifier adds a separate implementation of the exact method.
   See epistemics.md:27–89 and TUTORIAL.md:111–133.
7. **BC329 preflight.** The new constants and exact geometric improvement are checked
   arithmetic conditional on unmeasured coverage.
   Runner controls and easy full-shape calibration are instrument evidence.
   They supply no lower bound and no estimate that the scientific target must finish in
   the same time. See
   docs/project/reviews/review-2026-09-10-n11-bc329-packet-preflight.md:88–154,261–300.

## What Each BC329 Outcome Means

BC329 fixes $L=191/50$, the original sites, thresholds and relative weights,
$B_c=9981/10000$, and the 2880-step net with $D_c=207107/1440000000$. Let $m_c$ be its
exact least raw charge and $M=685457679/62500000$.

The scaling criterion is exactly $\exists\alpha>0:\alpha m_c\ge1,\ \alpha M<11$ if and
only if $m_c>M/11$. The frozen choice $\alpha=1/m_c$ is normalization, not
re-optimization. Charge below one is not by itself a rejection.

| Terminal evidence | Mathematical consequence | Remaining questions |
| --- | --- | --- |
| Exact $m_c>M/11$, all declared coverage routes agree on the normalized bytes, and dilation-source replay passes | $s(11)\ge S_c=38200\sqrt{2073600042893309449}/14374707134967=3.826721480476156460\ldots$ | Strictness at $S_c$, best core/net choice, other weights, larger improvements, and all structural routes |
| Independently checked admissible core of raw charge $\le M/11$ | No common scaling makes this exact packet meet both inequalities; equality also refutes it | Re-optimization, other core sizes/nets/sites/atoms, and conditional domains |
| Timeout, incomplete directions, nonzero-width interval enclosure, stalls or exhausted box budgets without a valid refuter | Packet unresolved; completed direction evidence retains its narrower scope | Whether the packet is feasible and whether a different instrument would decide it |
| Source mismatch, malformed geometry, method disagreement or invalid witness | Invocation/instrument invalid; no scientific verdict | Repair and separately justified continuation |

These are the preflight’s own distinctions at lines 304–327. The plan’s statement that
disagreement is merely “unresolved” should preserve the more informative invalid
classification.

Two deductions make the closeout more informative:

- At fixed direction, increasing $B$ increases charge at every surviving centre and
  shrinks the admissible-centre domain.
  BC329 includes T-026’s old directions, and $B_c>B_0$, so new coverage uncertainty lies
  in the inserted directions.
  Complete final replay is still required.
  An alleged old-direction refuter would conflict with retained evidence and should
  trigger source/geometry investigation.
- For this net, improvement over T-026 requires $B<0.998171489070944698\ldots$ by an
  exact squared comparison.
  A rejection at $0.9981$ leaves a real interval of larger candidates.
  Conversely, a retained low-charge core also refutes smaller core sides, and any other
  net containing its direction, while its membership/admissibility conditions persist.
  A maintained exact analysis of those breakpoints can sometimes cover the remaining
  improving interval without another full sweep.
  This is a proposed derived-witness instrument, not an already obtained BC329 result.

Source: preflight:144–154,172–176,203–216.

## Whole-Square Weighting and the Missing Conditional Theorems

The retained 88-core family has mass eleven and depth at most one everywhere at side
$191/50$. Scaling by $10000/9977$ gives **full unit squares** of fractional mass eleven
in $L_*=38200/9977$, below 3.83. Integrating any unconditional point cover against this
family forces mass at least eleven.
Selecting any individually defined core inside each unit square preserves the depth
inequality. This excludes all such unconditional point-core methods at $L_*$ and above,
regardless of asymmetry, net or individually chosen core size.
It does not exclude threshold charges, restrictions depending on other packed squares,
or point methods below $L_*$.

The full-unit obstruction does not require strong duality.
X-027’s interior-incidence duality and density result supplies a separate
value-equivalence theorem with a stated boundary convention.
Pairing arbitrary singular closed-square cover measures with only almost-everywhere
capacities is unsound.
Neither result proves a physical integrality gap at $L_*$; a physical exclusion there
remains missing. Both T-026 and the proposed BC329 bound lie below $L_*$. See
X-027:266–378 and
docs/project/research/research-2026-09-10-x027-fractional-duality.md:104–197.

The independent-parent translation obstruction is narrower: with $B=9977/10000$ and the
retained nodes, the translated 88 cores have explicit individual parents from side
3.82345. This removes a particular redundant point-only test, but the parents have not
been shown mutually compatible.
A6 adds capacity checks for its fixed 2,566 atom orbits at its stated domain; it does
not obstruct the whole threshold language.
Cutting A6’s fixed support does not control replacement supports.
See the active plan:114–157 and the evidence account:769–890.

For conditional exclusion, the missing obligations are precise:

- **Domain transfer:** every relevant physical residual must produce a selected core in
  the certified domain, including all centre, angle, sign, boundary and feature cases.
- **Shared variables:** the same owner must satisfy all residual constraints, and the
  selected owners must coexist.
  Separately chosen unary witnesses do not supply this.
- **Selection:** for a physical packing $P$, if $\Gamma(P)$ is its set of valid
  selections and $G$ the excluded selections, prove $\Gamma(P)\cap G\ne\varnothing$. A
  normalized-family version suffices if every feasible packing has an admitted
  normalized representative and every normalized packing has such a selection.
- **Resources:** use distinct owners; account for the union when banking point mass;
  prove any conditional threshold budget.
  A parent-contained region is not automatically bankable selected-core mass.

Raw-label exhaustion is sufficient but stronger than required.
A neutral label may coexist with an excluded selection, and a fractional survivor need
not extend to any physical packing.
A finite list of contact types still has continuous geometric obligations.
Sources: X-028:244–291; structural-normal-forms review:351–423.

## Structural Lemmas Worth Using

The easiest useful top-level lemmas are already available as reviewed analytic
deductions:

1. **Fixed-side normal form S1:** in each labelled fixed-angle feasible component,
   lexicographic minimization yields a representative whose physical contact components
   all touch the left and bottom walls and whose active genuine-contact rows have rank
   $2n$. This works at the trial side and retains all angles.
   It supplies the complete alternative “one snug parent, or a contact path of 2–11
   parents,” not a short-path theorem.
   See
   docs/project/reviews/review-2026-09-10-n11-structural-normal-forms.md:119–207,351–382.
2. **Seven of eight marks:** at $q=96/25$, the admitted point measure leaves allowance
   $\varepsilon=524199/2000000$, while two marks weigh more by $441/125000$. At most one
   mark is unowned. If $\sigma$ fully owned pairs split between two cores, there are
   $4+\sigma$ distinct owners and $7-\sigma$ residuals.
   The 80 incidence patterns are a complete abstract alternative before geometry.
   See the structural-helper report:245–335.
3. **One shared surplus:** with the same measure,
   $U_\mu+\sum_i(\mu(C_i)-1)=\varepsilon$. For $u$ missing marks and independently
   proved lower surplus bounds on disjoint owner groups,
   $uw+\sum_c\gamma_c\le\varepsilon$. A strict reverse inequality on a complete role
   domain would exclude that pattern.
   All useful $\gamma_c$ could still be zero; this has not been measured.
   See that report:345–420.
4. **At most three wall contacts:** the incircle separation calculation at 3.84 bounds
   each wall to three touching parents.
   With S1 there are at most three contact components, so some component has at least
   four parents and some path joins owners from different corners.
   These need not be the same component.
   Select owners after normalization.
   See X-027:563–595.

A literal-corner normalization is not currently supported.
A tilted snug square misses the literal corner; literal occupancy forces axis alignment.
The exact two-square fixture at $74/35$ is individually bottom-left stable and isolated
at fixed angles but has no parent touching both chosen walls.
It refutes a translation/quench shortcut, not existence of some free-rotation n11 corner
optimum. The n6 rotational rattler and n3 sliding optimum also prevent replacing
continuous terminal families with isolated angle/pose lists.
An arbitrary active SAT equality can be a projection coincidence without physical
contact. Sources: structural-normal-forms review:215–349; TUTORIAL.md:600–740.

A defensible next structural lemma should therefore constrain an admitted
snug/contact-path or ownership branch, with its complementary branches retained.
Compactness, numerical descent, a contact count or a stationary stress does not supply
the missing literal-corner statement.

## Issues in the Current Text

| Priority and issue | Exact source evidence | Recommended correction |
| --- | --- | --- |
| P2: surviving exhaustion claim | packing/frontier/results.yaml:1465–1468 says the small budget margin shows “where this route ends” and “near exhausted.” Lines 1514–1521 and the BC329 preflight correctly say the finite measurements do not establish that. | Replace the claimed conclusion with the measured margin and the open fixed-packet/re-optimization questions. A BC329 rejection still does not validate the original inference. |
| P2: incorrect denial of T-025 strictness | packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md:155 denies a strict inequality at 191/50, although its proof excludes that side and TUTORIAL.md:37–40 states attainment. The wording originates at packing/devtools/render_verifiable_claim.py:461. | Say what the registered claim asserts without denying its elementary compactness corollary: an attained minimum cannot equal an excluded feasible side. This distinction is different from T-026’s limiting endpoint. No numerical headline or registration needs to change for this wording repair. |
| P2: selection quantifier ambiguous in tutorial | TUTORIAL.md:438–440 requires cases covering “every permitted combination.” X-028:246–259 and the account:257–264 give the correct existential selection condition. | State “every hypothetical packing admits at least one valid excluded selection.” Avoid presenting all raw-label closure as necessary. |
| P2: invalid versus unresolved disagreement | docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md:305–309 says disagreement is unresolved; the preflight:309 classifies method disagreement as invalid. | Keep scientific undecidability separate from evidence inconsistency in the terminal disposition. |
| P2: latest evidence addenda omit exp156 | docs/project/reviews/review-2026-09-09-n11-evidence-interpretation.md:333 and docs/project/research/research-2026-09-09-n11-evidence-and-inference.md:1024–1034 still place the saved-escape target in the future. The active plan:188–195 and X-028:218–225 record its completed TR B-only incompatibility and untested other owners. | Add a current disposition or explicit historical cutoff and superseding pointer. Preserve the original receipts and criteria. Update similarly stale runner-readiness prose only from the matching admitted source. |
| P2: local dimension overstated | TUTORIAL.md:733–740 identifies local dimension with Jacobian nullity. At a singular constraint, nullity is only linearized information; $x^2=0$ already has nullity one and local dimension zero. | State the regularity/constant-rank hypothesis, or call nullity a linearized dimension and require integrability/stratum analysis. Do not use this sentence as a rigidity or finite-branch premise. |
| P3: tutorial’s point-dual endpoint is historical | TUTORIAL.md:382–385 highlights an inconclusive mass-10.3842 baseline without the later 88-core mass-eleven witness. | Add the current obstruction and its domain; keep the old state only if needed to explain H135’s particular input. |
| Planning precision: H131 does not give exact (9,2) counts | packing/campaign/hypotheses/H-131-near-axis-counts-at-q.md:12–18 gives upper counts. X-027:681–691 and X-028:311–318 propose a (9,2) comparison; the companion certificate report:662–663 correctly requires remaining profiles. | Register it as one conditional exact-count branch, or minimize demand over every allowed count vector. For the simple $n_0\le9$ case, $d_0\le d_1$ makes $9d_0+2d_1$ the worst allowed demand. Without that order, the single normalization is insufficient for the whole count theorem. |

The report and review aliases in the preceding sections refer to the exact paths listed
in this table or to the source map below.
Historical “unrun” statements with explicit earlier cutoffs are not themselves errors.

## Ranked Hypotheses and Discriminating Tests

These are readiness and information judgments, not measured comparative productivity.
Every new target must freeze source, domain, proposal rule, exact witnesses, controls,
deadlines and terminal meanings before measuring.

| Rank | Hypothesis and test | Accept, reject and scope |
| --- | --- | --- |
| 1, conditional on BC329 | **One nearby core/net change remains worthwhile.** After rejection, analyze exact low-charge witness breakpoints against the entire improving B interval; after acceptance, inspect the least-charge directions and budget margin to choose one smaller-core or locally refined candidate. Freeze only one successor packet if justified. | A retained witness interval can refute that declared B range for the fixed weights/net. A gap in interval coverage is unresolved. A new all-pose certificate plus transfer proves its own bound. Do not treat a uniform-core rejection as rejection of direction-dependent core sizes. |
| 2, direct alternative | **Re-optimizing existing atoms removes the packet bottleneck.** Keep BC329 geometry and a common source-bound row set; compare frozen ratios against optimized coefficients. Add omitted rows through a fixed rule before full retention. | Exact finite primal/dual bounds can prove a finite gain. An exact dual of mass at least eleven on admissible rows obstructs the same fixed atom catalog, even though other placements are omitted. Allowing arbitrary new point sites additionally requires full point-depth feasibility; allowing new thresholds requires their capacities. Complete positive coverage and dilation are still needed for a new bound. |
| 3, small language test | **The weighted five-site motif has geometric expressive advantage.** Admit exact traces for one motif on a frozen core domain; compare with all 80 ordinary threshold types on the same sites before expanding production coverage machinery. | A realizable trace subset with exact domination cost above one proves local advantage. An ordinary mixture of cost at most one covering the complete realizable trace universe removes that advantage on this domain. Neither determines the global cover; ordinary replacement columns may still help. |
| 4, structural | **A full co-owner parent or shared surplus removes a retained neutral obstruction.** Freeze one complete owner cell, use the same measure and source family, and compare with the weaker core/patch model. Prefer the exact surplus minimum if its instrument has the smaller admission burden. | Full-domain strict surplus contradiction excludes the named pattern. Lower surviving fractional mass only removes that witness; it is not a cover. A feasible survivor at the residual mass blocks only the declared point domain. A fixed pose requires a separate positive-width continuation. |
| 5, profile using existing language | **Proved angle counts improve demands or thresholds improve the same profile.** Compare uniform versus optimized demands with language fixed, then points versus thresholds with identical optimized demands and count constraints. | Exact finite gain isolates the changed mechanism. All-pose class coverage plus the minimum demand over all allowed count vectors gives the conditional/global consequence actually covered. One failed profile is not a failure of angle conditioning. |
| 6, conditional reserve | **Unary geometry or shared-owner consistency gives a genuine new restriction.** BC337 already owns the TR unary obstacle. For a joint test, first obtain disjoint residuals with positive unary controls, then decide whether one owner can coexist with both. | Complete common-owner impossibility proves the named relation; a compatible common owner rejects that pair hypothesis. A pointwise relation requires a complete pose-event definition and budget before becoming a charge/capacity certificate. Exp149/151 are not valid substitutes for this pair test. |

Richer multilevel floor compositions, nonuniform nets, direction-dependent core sides,
changed sites, and a rows-complete loop at a larger side remain open direct-certificate
changes. Direction-dependent point weights alone with a budget based on their sitewise
supremum have a retained domination argument and should not be confused with changed
class demands or changed core geometry.
See the certificate-mechanisms report:603–681.

Full-support pricing remains a mechanism reserve, not a route to a point-only
certificate at its frozen 3.84 side, where the transported unit-family obstruction
applies. Constructive search in another contact class remains a distinct upper-bound
option; its failure under a finite budget has no global lower-bound consequence.

## Recommended Plan Changes

1. Close BC329 with the terminal table above and preserve its actual evidence; keep the
   bracket at T-026 unless the complete acceptance chain passes.
   If accepted, update the bound gap and assurance only from the new registered claim.
2. Replace the static “next route” entry with one outcome-dependent direct
   discriminator. A rejected packet should first supply its exact witness and B-range
   implications; a timeout should supply the unfinished stage and evidence needed to
   decide whether continuation is operationally worthwhile.
3. Put the small realizable-trace discriminator ahead of full multiplicity-format
   expansion. Retain the matched row/column comparison and whole-optimal-dual-face test
   after that gate.
4. Make the structural lane consume S1, seven-mark ownership and one shared resource
   account. Record a complete branch/selection map alongside each proposed conditional
   cover, including the unclosed complementary branches.
   Do not add a literal-corner, finite-angle, short-path or quench-completeness premise.
5. Reconcile the current evidence account, tutorial and latest review addenda with
   exp156 and the actual runner admission, while retaining dated historical scopes.
   Correct the surviving exhaustion claim and the two mathematical wording problems
   before they are reused as premises.

Source map for abbreviated citations:

- Active plan:
  docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
- Evidence account:
  docs/project/research/research-2026-09-09-n11-evidence-and-inference.md
- Preflight: docs/project/reviews/review-2026-09-10-n11-bc329-packet-preflight.md
- X-027:
  packing/campaign/explorations/X-027-stromquist-fractional-and-structural-strategy.md
- X-028: packing/campaign/explorations/X-028-n11-strategy-portfolio-draft.md
- Structural-normal-forms review:
  docs/project/reviews/review-2026-09-10-n11-structural-normal-forms.md
- Structural-helper report:
  docs/project/research/research-2026-09-10-x027-structural-helpers.md
- Certificate-mechanisms report:
  docs/project/research/research-2026-09-10-x027-certificate-mechanisms.md

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
