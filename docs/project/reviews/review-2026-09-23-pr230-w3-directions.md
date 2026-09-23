# Review of PR 230’s W3 Directions, 23 September 2026

Four independent reviews of [PR 230](https://github.com/jlevy/squares/pull/230) at head
`e9af4e0e2`: one mathematical review each of
[X-043](../../../packing/campaign/explorations/X-043-new-lower-bound-proof-directions.md),
[X-044](../../../packing/campaign/explorations/X-044-low-n-certificate-transfer.md) and
[X-045](../../../packing/campaign/explorations/X-045-n11-global-capture-and-exact-optimality.md)
(Fable, extra-high thinking), and one audit of the retained tools, receipts and PR status
(Opus 5.5, extra-high thinking).
[Session 156](../../../packing/campaign/agent-sessions/session-156-w3-overnight-n11-settlement.md)
commissioned them at the start of the overnight W3 continuation, and they set its
direction.

None found a fatal error.
The reviews are evidence, not verdicts: their measurements are exploratory unless a
retained tool is named, and their plausibility estimates are inferences from certificate
arithmetic rather than runs.

## Findings That Set Direction

1. **No counting certificate can prove $s(11)=U$.** Trump’s packing is feasible at
   $U=3.877083590\ldots$, so every charge certificate excludes only sides strictly below
   $U$. X-045’s cutoff composition theorem is correct, but once $s(11)>31/8$ is in hand,
   “every local minimum with side in $[L,U]$ has side $U$” is equivalent to $s(11)=U$.
   Its operational content is that first-order descent is an admissible leaf and that
   boxes whose side relaxation is below $L$ are free.

2. **Settling n11 is verified global optimization.** The task is a complete cover of
   $\{S\le U\}$ modulo the symmetry group, with every leaf closed by infeasibility, a
   side inequality, descent, or Trump’s quantified chart ball.
   Markót and Csendes proved circle packings $n=28$–$30$ this way by interval
   branch-and-bound; Montanher and coauthors did rigorous unit squares in a circle.
   At fixed angles the centre problem is an exact disjunctive LP, so **the bottleneck is
   the eleven angles**.
   The X-045 reviewer proposes a rigorous form of H-112 as the first theorem milestone:
   every packing with six axis-aligned squares and five sharing one angle has side at
   least $U$, with equality only at Trump.

3. **Kleddamag’s certificate has no side headroom.** Over its 12,028 rows the least core
   collar $A-B$ is $3.26\times10^{-9}$, so the unchanged-core ceiling is
   $31/8+10^{-8}$. The charge is pinned by the corner-flush parent pose at every angle:
   11,981 rows attain their minimum there, at $1{,}000{,}047{,}518$ units.
   Any n11 certificate gain therefore needs an **adaptive parent-core producer with
   two-of-five and three-of-five features**, which the record does not have; the
   cheapest sound next form is a corner two-band count $4g_c+7g_o>M$ (H-155’s question).

4. **Frozen-weight low-n transfers are dead at the old direction nets.** At the net
   half-step the old core $B(\cos\delta+\sin\delta)$ exceeds the shrunk parent side, so
   X-044’s row 216 as stated and row 219 cannot run.
   The live form is a re-priced LP with a direction-dependent parent-centre clip in the
   existing column generator, decided by the n-general native parent-core verifier.
   Per-target slack at a 720-step net: n12 at 3.97, 0.017%; n18 at 4.70, 0.593%; n19 at
   4.82, 0.421%; **n21 at 4.90, 5.48%**.
   A cutting-loop run at n12 with the ceiling reader is a shared kill switch: a certified
   depth-one family of value at least 12 kills every additive route at n12 from 3.97 up.

5. **The retained evidence is sound.** All seven receipts replay to identical exact
   values, every figure the three reports quote matches its receipt, and hosted
   checkpoint
   [35822748072](https://github.com/jlevy/squares/actions/runs/35822748072) passed.
   Three older receipts came from unretained tool versions; the margins, count-slack and
   corrected structural receipts are authoritative.

## Soundness Findings

| Report | Severity | Finding |
| --- | --- | --- |
| X-045 | material | The cutoff framing presents a split into two partial results; given $31/8$ it is the whole problem (finding 1). |
| X-045 | material | Mode A (excess charge forces concentration) is unpriced: it needs a non-flat, near-tight certificate at $U$, and Kleddamag’s rows spread only $8.5\times10^{-5}$. |
| X-045 | minor | The “lower minimum values” leaf is vacuous as written; the finiteness proof should cite semialgebraic path-connectedness directly. |
| X-043 | material | Rows 204–207 and 209 at n11 are blocked on the missing producer (finding 3), which the report does not name. |
| X-043 | material | Direction C’s floor reservoirs are one-body and share the threshold family’s ceiling; the gain is argued by analogy with Tokoharu’s search representation. |
| X-043 | material | Direction A at n11 is H-136/H-155 in parent-core language, and the report does not cite them. |
| X-043 | minor | Row 210 (trace-group saving) has no headroom on this certificate: the ten two-of-five orbits are dispersed and the budget $2w$ is geometrically tight. |
| X-044 | material | Rows 216 and 219 are arithmetically dead as stated (finding 4). |
| X-044 | material | Row 218 omits the registered single-shot H-228 formulation and its existing ceiling-reader kill. |
| X-044 | minor | Row 222 overlaps H-226 without linking it; certificate-to-count matching uses string equality. |
| Receipts | low | Two receipts from unretained tool versions; the superseded structural receipt carries no in-file marker; replay commands write to `/private/tmp`. |

## Ranked Discriminators

| Rank | Case | Discriminator | Exit | Instrument |
| --- | --- | --- | --- | --- |
| 1 | n11 | Scale Kleddamag’s certificate to parent sides for 3.876 and $U$; read the row minima, excess and spread | Measured $d\Gamma/dA$; if $11\cdot\text{typ}'<M$, no frozen-support repair reaches 3.876 | Native parent-core verifier through the library |
| 2 | n11 | First-order descent pruning on pose boxes | Accept/refuse fractions with Trump and the n3 sliding optimum refusing | New; exact jets and LP modules exist |
| 3 | n11 | Basin-hopping census of verified local minima in $(U,U+0.02)$ | Count and values of distinct minima near $U$ | Existing basin-hopping driver |
| 4 | n12 | Cutting loop with the ceiling reader at side 3.9609 | A certified family of value at least 12 kills additive routes at n12 | Existing |
| 5 | n12, n21 | Parent-centre clip in column generation plus a converter to the native certificate | A native-verified certificate at 3.97 or 4.9, or a refuting pose | Clip and converter to build |
| 6 | n17 | Price five-site columns against the retained exp-222 dual | Rational minimum reduced cost | New pricing tool |

## Directions the Reports Missed

- The verified-global-optimization literature and its pruning tests, symmetry
  canonicalization on the cover side, and a cheap enlargement of Trump’s radius $\rho$,
  which shrinks the annulus any cover must resolve.
- A threshold-language ceiling family near 3.876 to bound how far counting can reach.
- H-228 as the exact-four formulation at n12, net refinement with the dilation corollary
  at n18–n21, and parent-centre or threshold transfer to n26 and n29.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
