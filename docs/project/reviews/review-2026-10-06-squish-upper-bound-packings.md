# Mathematics Review: Eleven SQUISH Upper-Bound Packings

Reviewed 2026-10-06 (America/Los_Angeles) by **GPT-6 Astra, high reasoning**, in a
separately prompted W2 mathematics lane.
The reviewer read the source certificates and the geometry checkers before inspecting
the importing lane’s implementation and receipts.
This is a project AI adversarial review.
It is not human oversight.

**Accepted:** all eleven exact rational certificates establish their stated upper
bounds. Both first-party exact routes decide all 177,440 pairs, and both reject each
negative control. The review findings were fixed and checked.
No mathematical defect remains open.

## Claim and Source

Nate Chaoweeraprasit’s [submission #401](https://github.com/jlevy/squares/issues/401)
provides rational certificates for packings of
$n=108,126,129,130,154,155,180,209,238,303$ unit squares.
The
[supplemental comment](https://github.com/jlevy/squares/issues/401#issuecomment-6031977107)
adds $n=153$. These are **T-113** (the ten-count release) and **T-114** (the
supplement). For each certificate’s rational side $S$, the claim under review is
$s(n)\le S$, where $s(n)$ is the least side of a square that contains $n$ freely rotated
unit squares with pairwise disjoint interiors.

The ten original files were read from
[`itsnaka/squish-certs`](https://github.com/itsnaka/squish-certs) at revision
`07fe6dde1e5b67405a3076719b90e58e2882b677`, under `squish-submission-2026-10-06/`; the
eleventh came from the linked comment.
The certificate contains `n`, `s_exact`, `s_decimal` and a list of rational triples
`[x,y,t]`, with $(x,y)$ the centre and $t=\tan(\theta/2)$. The source’s printed checker
output is a reported result.
No published producer checker was available to reproduce here.

The exact certificates establish feasible packings.
Neither a stationary numerical solution nor a feasible packing proves local or global
optimality. No optimality claim is admitted by this review.

The source folder uses 6 October in its name; the pinned commit and supplemental comment
were published on 7 October UTC. The retained
[acquisition record](../../../packing/resources/web/squish-401-2026-10-07/acquisition/sources.json)
identifies each source by URL and digest.
This review compared those eleven digests, the counts, both side fields and all **1,885
rational triples** with the retained normalized facts: all agree exactly.
The packet keeps derived geometry facts because the source publishes no licence.
No upstream success log enters the deciding path.

## From Rational Triples to Unit Squares

For one source triple let

$$
a=\frac{1-t^2}{1+t^2},\qquad b=\frac{2t}{1+t^2},\qquad
u=(a,b),\qquad v=(-b,a).
$$

All entries are rational, and $1+t^2>0$ for every rational $t$. Thus no exceptional
denominator or trigonometric evaluation is hidden in the conversion.
The identity

$$
a^2+b^2=\frac{(1-t^2)^2+4t^2}{(1+t^2)^2}=1
$$

gives $u\cdot u=v\cdot v=1$, $u\cdot v=0$ and $\det(u,v)=1$. With centre $c=(x,y)$, the
cyclically ordered corners are

$$
c-\frac{u+v}{2},\quad c+\frac{u-v}{2},\quad
c+\frac{u+v}{2},\quad c+\frac{-u+v}{2}.
$$

Their successive edges are $u,v,-u,-v$. They therefore describe a nondegenerate unit
square, with exact rational coordinates and counterclockwise order.
Positive and negative $t$, as well as $t=0$, obey the same identities.
The parametrization’s omitted rotation by $\pi$ creates no soundness issue: every
supplied finite $t$ gives a square, and rotating a square by $\pi$ leaves its shape
unchanged.

This conversion uses the supplied rational numbers directly.
It neither rounds the centres nor estimates an angle.
It introduces no dilation, translation or enlargement of the container.
The imported corner witness must carry exactly the same $S$ as `s_exact`, and one square
for each of the `n` source triples.

## The Verification Theorem

The certificate-to-bound argument has four hypotheses, all of which must be checked.

1. The roster contains exactly the declared positive integer $n$ squares, each with four
   rational corners. Parsing must preserve all source triples and must reject a count
   mismatch.
2. The corners of every piece form a unit square in cyclic order.
   Rational arithmetic checks unit edge lengths, right angles and, in the independent
   checker, opposite edges.
   The conversion above establishes these properties as well; the geometric checks
   defend against a faulty conversion.
3. Every corner coordinate belongs to $[0,S]$. The container and each square are convex,
   so corner containment implies containment of the entire square.
4. For each of the $n(n-1)/2$ unordered pairs, at least one edge-normal axis from either
   square separates their projection intervals, allowing endpoint contact.

For the last hypothesis, project the two squares onto a nonzero axis $w$ to obtain
intervals $[L_A,H_A]$ and $[L_B,H_B]$. Define

$$
g_w=\max(L_B-H_A,L_A-H_B).
$$

If $g_w\ge0$, a line perpendicular to $w$ separates the interiors.
Equality allows boundary contact: a point in a two-dimensional square’s interior
projects strictly between its extrema, so it cannot be in both interiors when the
intervals only touch.
The separating-axis theorem supplies the converse for convex polygons: disjoint
interiors have a separating axis normal to an edge of one polygon.
Opposite square edges are parallel, so the two distinct normals from each square
suffice. No axis is zero, because the shape check establishes unit edges.
Normalizing the axes is unnecessary for a sign decision.

Consequently the maximum of the eight directed gaps over these four axes is nonnegative
exactly when the two square interiors are disjoint.
All comparisons are over $\mathbb Q$, including equality.
There is no epsilon or floating-point tolerance.
With all four hypotheses established, the listed squares are a feasible packing in
$[0,S]^2$, which proves $s(n)\le S$. The proof requires neither a lower bound nor an
assumption about which square pairs are in contact.

## Exact Sides and Displayed Bounds

The proof uses `s_exact`. A finite decimal printed beside it is an upper bound only when
that decimal is at least the rational side.
Comparing the eleven source decimals with their rational sides gives four downward
roundings: $n=130,154,238,303$. Their verified decimal displays require one unit in the
sixteenth decimal place added to the source’s display.
The other seven source decimals are above the exact side; at $n=126,129,155,180,209$
they exceed its least sixteen-place decimal ceiling by eight or nine units in the last
place. The verified display is computed from the rational side by integer ceiling
division, so it can improve those source displays as well.

| $n$ | Verified decimal ceiling | Unordered pairs |
| --- | --- | --- |
| 108 | 10.9206589394033085 | 5,778 |
| 126 | 11.7735852916961071 | 7,875 |
| 129 | 11.8808935876459918 | 8,256 |
| 130 | 11.9044830325168772 | 8,385 |
| 153 | 12.8796793733329640 | 11,628 |
| 154 | 12.9282936576777577 | 11,781 |
| 155 | 12.9536770693532733 | 11,935 |
| 180 | 13.9236350042524224 | 16,110 |
| 209 | 14.9496179522017921 | 21,736 |
| 238 | 15.9294090272583145 | 28,203 |
| 303 | 17.9203123729203498 | 45,753 |

The total is **177,440 pairs per deciding route**. Rounding a proven upper bound upward
weakens it safely. A displayed decimal below $S$ would need a different certificate or
argument. The certification receipt’s `certified_side` and `exact_form` both retain the
source rational $S$; `verified_value` is the least sixteen-place decimal $V$ satisfying
$V\ge S$.

The confirmation records use **`exact_form: S` in both bound lanes**, and $V$ as both
reader displays.
The schema makes `exact_form` authoritative, so these records retain the
strongest exact bound proved by the certificate, $s(n)\le S$, while displaying a safe
ceiling. The reviewer checked all eleven records: both exact identities equal the
certificate side, and $S\le V<S+10^{-16}$. The existing bound-agreement check accepts
each pair without modification.

The post-rebase integration audit also checked every generated bound citation and atlas
entry. All eleven citations use the same safe ceiling and correctly attribute T-113 or
T-114. Each atlas witness has exactly the mathematical input retained in its
certification receipt, including the rational side, coordinate frame, unit size and
complete ordered corner roster.
The atlas display does not replace the exact side used for verification.

The later translation screen supplies a separate numerical motion observation for each
retained configuration.
The reviewer checked that all eleven case records label this `not-rigid` with
`numerically-checked` assurance, keep the optimization problem open and restrict the
claim to the retained configuration.
All 311 stored positive motions name square identifiers in the current certified
witnesses. These observations do not strengthen the exact upper-bound theorem into an
optimality or rigidity proof.

The original `s_decimal` strings remain in the source facts, acquisition, receipts and
attributed case prose.
The
[normalized release claims](../../../packing/resources/web/squish-401-2026-10-07/acquisition/release-normalized-claims.json)
and
[normalized supplement claim](../../../packing/resources/web/squish-401-2026-10-07/acquisition/supplement-normalized-claims.json)
explicitly distinguish that source display from the safe decimal used by the case
records. This is a normalization of how the source’s exact rational claim is displayed;
the source geometry and certified side are unchanged.

## Checker Boundaries

The adapter
[`squish_upper_bound_packets`](../../../packing/devtools/squish_upper_bound_packets.py)
requires a positive rational side, integer count and complete roster, with rational
strings rather than JSON floating-point numbers.
It refuses duplicate JSON keys, unknown fields, more than 324 pieces, sources larger
than one million bytes and rational literals longer than 256 characters.
The new 324-piece bound is its own admission limit; it reuses the existing half-angle
conversion without changing the older import command’s 64-piece limit.
The conversion agrees term by term with the derivation above.

`decide` serializes the generated Witness/v2 file before running either checker.
The first-party
[`check_rational_witness_independent`](../../../packing/devtools/check_rational_witness_independent.py)
checks rational corners using its own shape tests, projection intervals and all-pair
loop. Its `check(path)` entry point, which the adapter uses, validates the Witness/v2
envelope, exact scalar strings, unit piece size, coordinate convention, positive count,
complete roster, unique identifiers and four corners per piece before the geometry
checks. The lower-level `check_squares` function alone would assume some of that
structure, but the submitted route does not call it directly.

The second route,
[`sqpack.witness.exact_verify`](../../../packing/src/sqpack/witness.py), materializes
rational corners and calls
[`sqpack.verify.verify_packing`](../../../packing/src/sqpack/verify.py) with exact
fraction signs, after `load_witness` has validated the serialized witness against the
schema. `check_shapes=True` and `bucket=False` are the defaults, and `exact_verify` does
not override them. The geometry loop therefore tests every unordered pair; it does not
rely on the optional floating-point centre buckets.
Its separate margin calculation also visits every pair.
A margin summary is diagnostic; the verification verdict comes from the shape,
containment and separation checks.

These routes have separate geometry implementations.
They share the source adapter, its exact corner output, Python, `fractions.Fraction` and
the project’s YAML loader; they also use project witness infrastructure.
Running both does not independently validate source acquisition or conversion.
This review’s algebra, roster audit and inspection of the adapter address that shared
boundary.

The confirmation relationship is **independent implementation relative to the producer’s
SQUISH code**: the deciding programs use first-party rational geometry, and the importer
reads the published certificate format.
It is not a reproduction of the producer’s checker.
The two first-party routes use the same separating-axis theorem; they are not different
mathematical methods.
Neither is a proof-assistant kernel.

## Significance

**Keep S3 for both T-113 and T-114.** The
[retained frontier comparison](../../../packing/resources/web/squish-401-2026-10-07/acquisition/frontier-comparison.json)
shows a strictly smaller rational side than each prior verified upper bound.
The ten original improvements range from about $0.000413$ at $n=129$ to $0.00670$ at
$n=130$; the supplemental improvement at $n=153$ is about $0.00199$. These are
substantive case results, comparable to Couzo’s T-056 and T-092, both S3. Daniel’s
T-098, S2, refines previously known packings by about $10^{-13}$ to $10^{-11}$. The
current claims provide new smaller packings, while the source’s unpublished search
procedure supports no reviewed claim of a reusable method.
Priority is scoped to the retained source search; the comparison with this register is
not a proof of global novelty.

## Replay, Controls and Disposition

The retained
[certification receipt](../../../packing/resources/web/squish-401-2026-10-07/receipts/certification.json.gz)
records acceptance of all eleven certificates by both exact routes, with the complete
pair counts in the table above.
Both routes report zero minimum container clearance for every certificate.
That establishes a boundary contact, not optimality or rigidity.
The importer writes the rational witness only after both routes accept and both report
the expected pair count.
It records zero side inflation: the certified side is the source’s exact fraction.

The
[negative-control receipt](../../../packing/resources/web/squish-401-2026-10-07/receipts/negative-controls.json)
uses the 108-square certificate.
Both mutations preserve the number and shapes of the pieces; they test geometric refusal
rather than malformed-input refusal.

| Mutation | Independent corner checker | `exact_verify` |
| --- | --- | --- |
| Replace square 2’s corners with square 1’s corners | Refuses one overlapping pair, with best gap $-1$ | Refuses overlap of squares 0 and 1 |
| Translate square 1 by $(-2S,0)$ | Refuses negative container clearance $-2S$ | Refuses all four corners crossing the left wall |

Each control run still examines all 5,778 pairs.
Duplicating a contained unit square forces an interior overlap while preserving
containment; translating one beyond the left wall forces a container violation.
The observed reasons match those intended failures.

The reviewer ran
[`test_squish_upper_bound_packets.py`](../../../packing/tests/test_squish_upper_bound_packets.py)
with
[`test_squish_upper_bound_receipts.py`](../../../packing/tests/test_squish_upper_bound_receipts.py)
and
[`test_squish_receipt_binding.py`](../../../packing/tests/test_squish_receipt_binding.py)
on the final semantic receipt format: **42 tests passed**. Besides the two mutation
types, these exercise a 108-piece roster above the old admission cap, malformed or
incomplete source data, duplicate JSON keys, input bounds, the nonzero rotation $t=1/2$,
exact boundary contact and an overlap of $10^{-30}$. Both deciders accept the touching
two-square fixture and reject the same fixture moved inward by that exact amount.
This test would expose a permissive epsilon in the deciding path.
Tests also reject duplicate receipt rosters, altered retained certificates, invalid
source metadata and replacing both facts and their rebuilt certificate while reusing an
earlier successful receipt.
The stale-success test exercises the binding between the complete checker input and the
receipt rather than relying on source attribution or file formatting.

The semantic receipt tests also accept changed nongeometric metadata and equivalent
rational spellings, reject changed geometry, units, coordinate frames or method
dispatch, and reject stale control inputs and normalized claim displays.
The reviewer also ran the two atlas normalization tests at $n=126,130$, which passed.
The atlas accepts either the original source display or its prescribed safe ceiling
while preserving the exact side $S$; an arbitrary changed bound is refused.

The adapter’s offline `check` rebuilds each witness from its normalized facts and
compares the complete mathematical input with both the retained certificate and the
input recorded in the receipt.
It checks the count, positive rational side, unit piece size, rational corner
representation, coordinate frame and every ordered corner and identifier.
Rational literals are reduced before comparison.
The native verifier’s `exact-algebraic` method dispatch is required before extracting
this input.

The same comparison applies to both control inputs.
Changes to nongeometric prose or formatting do not alter the mathematical input; changes
to a side, corner, piece size or roster cannot reuse an earlier successful receipt.
This is direct comparison of the retained values, with no digest of a repository-owned
artifact deciding acceptance.
Source revision, URL, retrieval metadata, retention status and named checker routes are
also checked; none can silently turn into a claim of producer-checker reproduction.
`check --replay` additionally repeats both decisions on every requested certificate and
regenerates both controls; it compares the new results with the retained receipts.
Omitting `--n` requests all eleven.

The reviewer independently repeated both geometric decisions for all eleven retained
certificates. That run exposed MR-2 at the final control comparison.
After its fix, the reviewer repeated the 108-square case and both controls successfully.
The final v2 receipt stores the complete mathematical input for each decision.
After recertification in the confirmation checkout, the engineering lane completed a
fresh all-eleven deterministic replay, including both controls with their recorded
inputs, in **75.594 seconds**. The exact corner geometry and source rational sides were
unchanged. These are complete certificate checks; no sample stands in for the full
roster.

From `packing/`:

```bash
uv run --frozen python -m devtools.squish_upper_bound_packets check --replay
uv run --frozen --all-extras --group dev python -m pytest tests/test_squish_upper_bound_packets.py tests/test_squish_upper_bound_receipts.py tests/test_squish_receipt_binding.py -q
```

| Finding | Severity and disposition |
| --- | --- |
| MR-1: `check` collapsed duplicate receipt counts into a dictionary before checking the roster, and accepted repeated control names | **Medium, fixed.** It now checks raw list length and the exact set of counts, and requires the two distinct control names with complete checker coverage and recorded failures. All three duplicate-roster mutations are covered by passing tests. |
| MR-2: full replay reached the controls and failed its receipt comparison because fresh failure tuples differed from JSON-loaded lists | **Blocker, fixed.** `decide` normalizes its results at the JSON receipt boundary. The new control round-trip test passes, and the reviewer repeated the 108-square replay with both controls successfully. The defect affected replay equality, not the geometric verdicts. |
| MR-3: normalizing the reported display to its safe decimal ceiling made the atlas reject nine source records | **Blocker, fixed.** The atlas accepts the prescribed ceiling as well as the original source display, with exact geometry still checked at $S$. The reviewer reproduced the failure at $n=126,130$ and ran the passing acceptance and arbitrary-bound refusal tests after the fix. |
| Finite source displays can lie below their exact side | **Handled; no open defect.** Verified decimals use exact integer ceiling division. The source’s displays remain separately attributed. |

The two exact geometry implementations and the source conversion have no unresolved
mathematical finding.
Their claim is independently re-implemented upper-bound feasibility.
This review supplies one accepting project AI review; it neither supplies the second
distinct review nor the human oversight required for rung 4 by
[`epistemics.md`](../../../epistemics.md).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
