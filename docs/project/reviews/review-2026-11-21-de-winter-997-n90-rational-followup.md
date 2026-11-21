# De Winter’s n = 90 Follow-Up: Stage 4 Mathematical Review

Date: 21 November 2026.\
Reviewer: Codex, strong tier (`tbd-strong-max`), maximum reasoning.\
Kind: adversarial mathematical review, correctness scope.\
Verdict: accepted for finite exact feasibility; no blocking, major, or minor finding.\
Covered submission:
[the author’s follow-up to #997](https://github.com/jlevy/squares/issues/997#issuecomment-7058975230),
candidate member `90/candidate.json.gz`.

## Summary for the Author

The submitted rational coordinates place 90 unit squares in the square of side

$$
L=9.994038766582870551562992268196496807097969609726923622\ldots,
$$

where the exact value is the `side` fraction in the retained candidate.
An independently written program checked all 90 shapes, all 1,440 vertex–wall
inequalities, and all 4,005 unordered pairs.
Every required inequality passed.
Thus the stated upward rounding gives $s(90)\le 9.994038766583$.

The candidate has exact contacts: 64 zero vertex–wall inequalities and one pair with
zero best separation, squares 8 and 49 using zero-based indices.
Boundary contact is allowed.
The result establishes feasibility without a positive clearance guarantee.

All 13 predeclared controls passed.
The enclosed input is also feasible.
The final common scale of its centers changes the side by approximately
$8.9940387678\times10^{-73}$ and preserves every orientation.
Against the supplied registered reference $99940387666098521323/10^{19}$, the
candidate’s gain is approximately $2.6981580737\times10^{-11}$. These are separate
comparisons.

The
[frozen result](../../../packing/campaign/issue-intake/2026-11-21-de-winter-997-n90-followup/review/result-frozen.json)
and
[packet README](../../../packing/campaign/issue-intake/2026-11-21-de-winter-997-n90-followup/review/README.md)
retain the decisions and exact program that made them.
No producer program was read or run.

## Claim, Inputs, and Independence

The claim is existence of 90 closed Euclidean unit squares contained in $[0,L]^2$ with
pairwise disjoint interiors.
There is no lower-bound or optimality claim.

The author defines a triple as $(c_x,c_y,t)$ with $t=\tan(\theta/2)$ for a signed
counterclockwise angle.
The candidate uses lists; the enclosed input uses dictionaries with `cx`, `cy`, and `t`.
The verifier requires 90 entries, strict rational strings, a positive side, and valid
triple shapes. It rejects duplicate JSON keys, floating coordinates, nonfinite values,
and zero denominators.
See the
[frozen parser, lines 35–88](../../../packing/campaign/issue-intake/2026-11-21-de-winter-997-n90-followup/review/verify_independent.py.txt#L35).

The compressed candidate’s SHA-256 is
`3a8e8913d0b87ac0b68c3fc4ac24d6ad042074c9696a2cdbfae3682b2e0b96c7`. The input’s is
`c519aa1822709897d541e7b83efdb027054ad636059bfb340acdb3e9c4a5fb9b`. The
[source manifest](../../../packing/campaign/issue-intake/2026-11-21-de-winter-997-n90-followup/review/evidence/source-manifest.json)
identifies all four factual members and the author comment.

The independent plan froze at 17:44:46.218786 UTC; the result froze at 17:48:28.842350
UTC on 21 November. Before that result, this lane read only the assignment, specified
author comment, four factual members, host memory-guard instructions, and its own files.
Source comparison files and candidate metadata contain producer-reported arithmetic;
those claims were read and recomputed.
No producer verification code, maintained project geometry code, adjacent derived
results, or earlier review was read.

After the freeze, this lane read workflow/configuration documents, the earlier #997
review sections identified below, and the pinned archive’s member list.
The four factual files match their archive members byte-for-byte.
The
[custody receipt](../../../packing/campaign/issue-intake/2026-11-21-de-winter-997-n90-followup/review/archive-custody.json)
records the 39,377-byte ZIP, SHA-256
`c04a0a60ca91f15922f6077c878c50b654e759ee659c14d43096cadaae574afa`. Its certificate path
is `90/candidate.json.gz` at the archive root.

This is an independent implementation with separate prompt and code and no shared
producer components.
The author disclosed an OpenAI AI tool, and this reviewer is Codex; no independence of
model family is claimed.
The trust boundary includes CPython 3.14.7, its integer and `Fraction` arithmetic, the
JSON/gzip readers, the supplied bytes, and the author’s coordinate convention.
Exact feasibility does not authenticate historical provenance or priority.

## From the Certificate to Feasibility

For each rational $t$, put $q=1+t^2$ and define

$$
u=\left(\frac{1-t^2}{q},\frac{2t}{q}\right),
\qquad
v=\left(-\frac{2t}{q},\frac{1-t^2}{q}\right).
$$

Since $q>0$ and $(1-t^2)^2+4t^2=(1+t^2)^2$, these are perpendicular unit vectors with
positive orientation.
The points $c+(\epsilon u+\delta v)/2$, for $\epsilon,\delta\in\{-1,1\}$ in cyclic
order, bound a unit square.
The program also checks the constructed vertices: four squared edge lengths equal to
one, four adjacent dot products equal to zero, signed area equal to one, and centroid
equal to the supplied center.
All 90 squares pass.
See the
[frozen construction](../../../packing/campaign/issue-intake/2026-11-21-de-winter-997-n90-followup/review/verify_independent.py.txt#L121).

For every vertex $(x,y)$ it checks $x\ge0$, $L-x\ge0$, $y\ge0$, and $L-y\ge0$. Convexity
makes these 1,440 exact inequalities sufficient for containment of every square.

For squares $A,B$ and a nonzero normal $a$, let $[m_A,M_A]$ and $[m_B,M_B]$ be the
extrema of their vertex projections.
Either $m_B-M_A\ge0$ or $m_A-M_B\ge0$ puts the polygons on opposite sides of a line,
with only boundary contact possible at equality.
The program tries both directions for the two edge normals reconstructed from each
square’s vertices. It evaluates all four axes for every unordered pair and retains the
largest signed separation.

Every accepted pair therefore carries an explicit separating line.
Acceptance uses that sufficient condition; it never infers separation from a numerical
tolerance. The
[frozen pair routine](../../../packing/campaign/issue-intake/2026-11-21-de-winter-997-n90-followup/review/verify_independent.py.txt#L174)
forms projection differences by integer cross multiplication over positive denominators.
No trigonometric or floating-point decision occurs.
The
[complete loop](../../../packing/campaign/issue-intake/2026-11-21-de-winter-997-n90-followup/review/verify_independent.py.txt#L194)
checks the pair count against $90\cdot89/2=4,005$ and the axis count against 16,020. The
retained pair ledgers give a separating axis, direction, and exact margin for every
pair.

## Invariants and Controls Checked

| Invariant | Evidence |
| --- | --- |
| Exactly 90 unit squares are interpreted | Count validation; 360 unit-edge checks, 360 right-angle checks, 90 area checks, and 90 center checks |
| Containment includes every corner and wall | 1,440 inequalities, no failure |
| Every unordered pair is separated | 4,005 pairs, 16,020 axis tests, no failed pair |
| Equality is accepted as boundary contact | Axis-aligned touching, rotated wall touching, and rotated pair touching controls |
| Tiny penetrations survive exact arithmetic | An overlap and a wall excursion of $10^{-100}$ are refused |
| Tilted separating axes are used | Rotated pair control passes while horizontal and vertical bounding intervals overlap |
| Duplicate geometry is refused | Coincident synthetic squares fail; replacing candidate square 89 by square 0 fails pair $(0,89)$ after all 4,005 pairs are tested |
| Malformed inputs cannot count as proof | Wrong count, zero denominator, floating coordinate, nonfinite coordinate, short triple, and duplicate-key controls are refused |

The 13 controls were declared before checking the candidate.
Their fixtures and outcomes are retained in the
[plan](../../../packing/campaign/issue-intake/2026-11-21-de-winter-997-n90-followup/review/plan-frozen.json)
and result. The candidate duplication and count-mismatch controls mutate the supplied
certificate; the other geometric controls use small rational fixtures.
The enclosed input’s minimum wall margin is $1.5\times10^{-82}$ and its minimum selected
pair margin is approximately $1.00000000013\times10^{-73}$.

## Comparisons and Their Scope

All nine rows of `comparisons.csv` reproduce as exact reference minus candidate side.
The metadata’s input digest, original side, and gain match.
One positive scale and translation maps all 90 input centers to candidate centers, while
all 90 half-angle tangents remain identical.
The square sides stay one; only centers change.

The supplied leaderboard decimal has 50 digits after the decimal point.
It equals the candidate truncated to that precision, while its exact scalar is about
$3.6220346293\times10^{-51}$ *below* the candidate.
Displayed agreement supports the author’s wording but establishes no improvement over
that scalar. The underlying leaderboard run and provenance were not authenticated here.

The four old points in `previous-comparisons.json` support a conditional obstruction to
obtaining the candidate through uniform scaling of old centers with orientations fixed.
For pair $(1,39)$, separation on an axis requires

$$
\lambda\lvert(c_{39}-c_1)\cdot a\rvert
\ge r_1(a)+r_{39}(a),
$$

where each $r$ is the square’s projection radius.
The least threshold over the four edge normals gives
$\lambda\ge0.9999999999979778448617\ldots$. The horizontal width of the supplied squares
57 and 10 then requires an enclosure at least $9.9940387665916647905938\ldots$,
approximately $8.7942390308\times10^{-12}$ above the candidate.

For necessity in this conditional argument, the difference body of two centered squares
is their Minkowski sum.
Its edges are parallel to edges of the squares, so its bounding inequalities use these
four normal directions.
A center difference strictly inside all those inequalities gives interior overlap.
Thus separation requires reaching at least one of the four thresholds.

All supplied exact thresholds and gain claims reproduce.
This argument assumes those four triples belong to the stated old witness, fixes their
orientations, and allows positive uniform scaling of centers plus translation in an
axis-aligned enclosure.
It does not authenticate the complete old witness or exclude arbitrary rotation,
deformation, or reoptimization.
See the
[frozen arithmetic routine](../../../packing/campaign/issue-intake/2026-11-21-de-winter-997-n90-followup/review/verify_independent.py.txt#L351).

## Findings and Questions

No blocking, major, or minor defect was found in finite feasibility.

| ID | Grade | Location | Finding and disposition |
| --- | --- | --- | --- |
| N1 | Note | Candidate `side` and `squares`, decoded line 1 | Exact wall and pair contact is valid. Record the zero margins and preserve exact arithmetic. |
| N2 | Note | `90/previous-comparisons.json`, lines 20–29 and 49 | The 50-place display agrees, but its exact scalar is smaller. Keep agreement separate from a strict leaderboard improvement. |
| N3 | Note | `90/previous-comparisons.json`, lines 50–88 | The four-point obstruction needs its stated fixed-orientation assumptions. Preserve that conditional scope. |

No further information is needed for finite feasibility.
The author’s clarification identifies the registration text to retain for the earlier
leaning-square account.
The origin of the earlier tiny rotation and historical linear-program output remain
unresolved as the author states.

## Relation to the Earlier Review

Only after the independent result froze did this reviewer read the
[15 November #997 addendum](review-2026-11-15-de-winter-996.md#addendum-15-november-2026-the-replacement-certificate-of-997-lane-l182),
specifically its opening, custody/comparison sections, padding discussion, findings, and
author questions. No earlier program or receipt was used.

That review accepted the old exact side $99940387666098521323/10^{19}$ and reported
positive pair gaps. This certificate has a smaller side and an exact pair contact; the
changed margins are consistent with the different rational input.
Its four-point obstruction agrees in scale with the earlier review’s roughly
$1.818734\times10^{-11}$ center-contraction allowance.
The candidate is below the corresponding conditional enclosure bound.

The current comment expressly answers the earlier question about which registration
narrative to retain.
This review makes no new attribution or historical-search claim.

For a separately registered numerical follow-up, the recommended significance is **S2**,
a citable refinement of an already reported local solution.
The earlier arrangement’s S3 assessment covers its larger case contribution and remains
unchanged.
If the follow-up is incorporated into that result, retain its cumulative claim
scope when recording significance.

## Execution and Retained Versions

The first run used the exact
[frozen program](../../../packing/campaign/issue-intake/2026-11-21-de-winter-997-n90-followup/review/verify_independent.py.txt),
SHA-256 `608c4ce81d4750df551ba64c5353a68112bbd6c9f3fb623ea4e5b8d32283cafe`. Its
[result](../../../packing/campaign/issue-intake/2026-11-21-de-winter-997-n90-followup/review/result-frozen.json)
has SHA-256 `2e135584054b2c3b9a680f91394e4f825826b3638fb5c130aa087e7787ea2da4`.
Historical line references point to that exact source.

The command in `execution.json` ran the dedicated worker with CPython 3.14.7 and
`-I -B`, after an observe-only memory guard sampled it.
Worker and guard exited zero.
The guard observed one process, normal pressure throughout, approximately 0.02 GiB
maximum tree cost, and no interventions.

After the mathematical freeze, a separate working copy received import, layout, naming,
and boolean-argument style changes.
It passed the full project Ruff configuration and targeted BasedPyright.
A second observed run passed.
The retained comparison checks every result field except run times and the intentionally
changed program digest; all geometry, source identities, controls, comparisons, and
verdicts match. Its negative control detects an altered candidate verdict.

The frozen source and receipt remain authoritative for the independent finding.
The working source is a separately identified replay version.
Standard-library exact arithmetic avoids dependencies on a producer or maintained
geometry implementation; that separation is the design requirement of this review.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
