# Independent Review of the T-022 Exact-Containment Limit

**Verdict: accept integrated promotion commit
`6b4cde0a905d5165fe1f841870d1081c9c915e0e`.** The sharpened theorem and its retained
replay boundary are sound.
The unchanged `T-018` source certificate and a new exact Euclidean containment lemma
prove the weak lower bound

$$
s(11)\ge S_*:=
\frac{38100\sqrt{8100042893309449}}{899996306539}
=3.810025723614703407\ldots.
$$

This is not the coarse Condition 4 dilation argument.
That argument stops at $3.8100156357\ldots$. The new result follows only after replacing
the coarse shrink estimate at each rational scale by the exact support-function estimate
proved here. The integrated promotion preserves that distinction.

I reviewed the final integrated
[`T-022` proof](../../../packing/cases/n11_fractional_certificate/t-022-dilation-limit-proof.md),
the
[`T-022` machine record](../../../packing/cases/n11_fractional_certificate/t-022-dilation-limit-corollary.json),
the changes to
[`dilation_corollary.py`](../../../packing/devtools/dilation_corollary.py), and the
[`dilation_corollary` tests](../../../packing/tests/test_dilation_corollary.py).
I checked the theorem against the retained
[`T-018` claim](../../../packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md)
rather than treating the derived record as a premise.

## Frozen Source and Replay Boundary

The frozen source is
[`certificate.json`](../../../packing/cases/n11_fractional_certificate/certificate.json),
SHA-256 `b121edbd044b6f326022d8783551efd947c95eec2738269857d039358ac6ae6a`. I
independently ran its standard-library verifier.
It accepted **Conditions 1–5** and reported:

| Check | Exact result |
| --- | --- |
| Condition 1 | 1,121 distinct atoms inside the container, with nonnegative weights and the declared $D_4$ symmetry |
| Condition 2 | total mass $434547/40000 < 11$ |
| Condition 3 | final-net slack $309449/250000000000 \ge 0$ |
| Condition 4 | $D=207107/90000000$ and $B(1+D)=899996306539/900000000000<1$ |
| Condition 5 | least cell mass $4001/4000\ge1$ over 181 directions and 567,130,649 cells |

That replay establishes the source data.
It does not by itself establish the sharpened limit.
The additional theorem layer uses the replayed Conditions 1, 2, 3, and 5, recomputes $B$
and $D$ from the same bytes, and replaces the scaled use of Condition 4 with the exact
lemma below. Source Condition 4 remains true and is part of the complete `T-018` replay,
but its coarse inequality is not true throughout the new scaled family.

For durable evidence, `--check-limit-record` runs the full source verifier, binds the
derived record to the source SHA-256, compares the declared source totals with the exact
decision, recomputes the sharpened arithmetic, and refuses record drift.
A record, a hand-constructed `Verdict`, or the legacy explicit-factor output is not a
substitute for that path.

## Exact Arithmetic

The source values are

$$
L=\frac{381}{100},\qquad
B=\frac{9977}{10000},\qquad
D=\frac{207107}{90000000}<1.
$$

Set

$$
R=90000000^2+207107^2=8100042893309449.
$$

Then

$$
\sqrt{1+D^2}=\frac{\sqrt R}{90000000},
\qquad
1+D=\frac{90207107}{90000000}.
$$

The uniform fixed-$B$, single-core factor ceiling and side are

$$
c_*=
\frac{\sqrt{1+D^2}}{B(1+D)}
=\frac{10000\sqrt R}{899996306539},
$$

and

$$
S_*=Lc_*
=\frac{38100\sqrt R}{899996306539}.
$$

Squaring gives the entirely rational identity

$$
S_*^2=
\frac{11758103264356929262890000}
     {809993351783841654158521}.
$$

The fraction is reduced.
The factorization

$$
R=61\cdot421\cdot4133\cdot76315013
$$

has four distinct prime factors, so $R$ is squarefree.
Thus $S_*$ is irrational, and its primitive minimal polynomial over the integers is

$$
809993351783841654158521X^2
-11758103264356929262890000.
$$

The rational squared form, not a decimal or floating-point square root, is the decision
surface for every strict comparison.

## Exact Containment Lemma

Let $d$ be the angular difference between a unit square and its nearer net direction,
and put $t=\tan d$. The net construction gives $0\le t\le D$. A concentric square of
side $qB$ at the net direction lies strictly inside the unit square whenever

$$
qB(\cos d+\sin d)<1.
$$

For $t\ge0$,

$$
\cos d+\sin d=f(t):=\frac{1+t}{\sqrt{1+t^2}}.
$$

Monotonicity on the needed interval has the exact algebraic proof

$$
(1+D)^2(1+t^2)-(1+t)^2(1+D^2)
=2(D-t)(1-Dt)\ge0.
$$

Indeed, $D-t\ge0$ and $1-Dt>0$ for $0\le t\le D<1$. Dividing by the positive product
$(1+t^2)(1+D^2)$ and taking nonnegative square roots gives

$$
\cos d+\sin d=f(t)\le f(D)
=\frac{1+D}{\sqrt{1+D^2}}.
$$

For rational $q>0$, the needed strict containment follows from

$$
qBf(D)<1.
$$

All quantities are positive, so this is equivalent to the exact rational test

$$
\bigl(qB(1+D)\bigr)^2<1+D^2.
$$

The inequality holds exactly when $0<q<c_*$. This proves strict interior containment
without invoking the scaled coarse Condition 4.

Writing $h=D$ for the net’s constant half-tangent increment, the $k$th gap has tangent

$$
\frac{h}{1+k(k+1)h^2}.
$$

It is uniquely largest at $k=0$, where it equals $D$; the midpoint of that angular gap
realizes the corresponding error.
Thus $f(D)$ is the actual maximum support factor for this net.
Consequently, $c_*$ is the strict-containment supremum for this particular method: one
uniform $B$, one concentric inner square per packed square, and the fixed net.
It is not proved to be the strongest consequence of the atoms or their coverage
geometry. Direction-dependent core sizes, multiple cores, and other uses of the coverage
margin remain outside `T-022`.

## Dilation-Limit Theorem

Fix a rational $q$ with $0<q<c_*$. Multiply every atom coordinate, the container side
$L$, and the covered-square side $B$ by $q$. Leave the weights and direction net
unchanged.

| Replayed property | Effect of scaling by $q$ |
| --- | --- |
| Condition 1 | Positive common scaling preserves distinctness and container inclusion; unchanged nonnegative weights and scaled atom orbits retain the declared symmetry in $[0,qL]^2$. |
| Condition 2 | The weights and their total do not change. |
| Condition 3 | The rational direction net and $D$ do not change. |
| Condition 5 | Inverse dilation bijects admissible closed $qB$-squares in $[0,qL]^2$ with admissible closed $B$-squares in $[0,L]^2$, preserving boundary incidence and covered mass. |
| Exact containment | The squared test above puts every selected $qB$-square strictly inside its corresponding unit square. |

The rest of the retained theorem proof is unchanged: reflection handles orientations
past $\pi/4$, Condition 5 gives mass at least one to the selected inner square,
Condition 1 preserves that mass on pullback, strict interior containment prevents an
atom from being counted in two packed squares, and Condition 2 gives the contradiction.
Hence

$$
s(11)\ge qL
\quad\text{for every rational }q\text{ with }0<q<c_*.
$$

Now let $x$ be any real number with $0<x<S_*=c_*L$. Rational density supplies a rational
$q$ with

$$
\frac{x}{L}<q<c_*.
$$

A packing in side $x$ embeds in the larger container of side $qL$, contradicting the
result at that rational scale.
Thus no positive side below $S_*$ is packable.
Every element of the set whose infimum defines $s(11)$ is at least $S_*$, so

$$
s(11)\ge S_*.
$$

This is a direct density and embedding argument.
It does not take a limit of packings, certificates, or verifier outputs.

## Rejection of the Superseded Scaling Proof

The review transport `4b7bce5f` is superseded and must not be used to justify $S_*$. It
scaled $B$ and applied frozen Condition 4, which allows only

$$
qB(1+D)<1
\quad\Longleftrightarrow\quad
q<c_0:=\frac1{B(1+D)}.
$$

That family has the smaller supremum

$$
Lc_0=
\frac{3429000000000}{899996306539}
=3.810015635715733\ldots.
$$

The number is sound as an intermediate finding.
At $q=c_0$, the exact containment test is still strict because

$$
qBf(D)=\frac1{\sqrt{1+D^2}}<1.
$$

It is not the sharpened result.
For $c_0<q<c_*$, frozen coarse Condition 4 fails while the exact squared test passes.
Any implementation or document saying that scaled Conditions 1–5 hold throughout this
interval is wrong. `T-022` is a sharpened-containment corollary of the fully replayed
source, not a family accepted by the frozen coarse checker.

The rational control

$$
q_+=\frac{500003}{500000}
$$

lies in that distinguishing interval.
Its coarse containment exceeds one by

$$
q_+B(1+D)-1
=\frac{853258419617}{450000000000000000}>0,
$$

while its exact squared-containment slack is

$$
1+D^2-\bigl(q_+B(1+D)\bigr)^2
=\frac{33822158946641039188838841479}
       {22500000000000000000000000000000000}>0.
$$

It therefore proves

$$
s(11)\ge q_+L
=\frac{190501143}{50000000}
=3.81002286,
$$

even though the frozen coarse checker rejects it.
This is the required positive control for the new theorem layer.

The earlier finite rational scale remains valid:

$$
a=\frac{250001}{250000},\qquad
aB(1+D)=
\frac{224999976631056539}{225000000000000000}<1,
$$

so

$$
s(11)\ge aL=\frac{95250381}{25000000}=3.81001524.
$$

It too is strictly weaker than $S_*$. Its role is a regression check, not the promoted
headline.

## Attempted Falsifications

### Equality at the Sharpened Endpoint

At $q=c_*$,

$$
\bigl(qB(1+D)\bigr)^2=1+D^2,
$$

so the sharp containment test reaches equality.
The proof requires strict interior containment and supplies no certificate at $q=c_*$.
This does not affect the weak bound: the density step uses a distinct rational $q<c_*$
above each hypothetical $x<S_*$. The record states that the endpoint is not certified.

### Strict `>`

The argument excludes every side below $S_*$ and is compatible with $s(11)=S_*$. It
cannot prove $s(11)>S_*$. Even proving no fit exactly at $S_*$ would not by itself rule
out packings at arbitrarily close larger sides.
The promoted relation is `>=`.

### Compactness or Attainment

No step assumes that the infimum defining $s(11)$ is attained.
A hypothetical packing below $S_*$ is contradicted at one larger rationally scaled
container. Compactness and a limiting configuration are unnecessary.

### Arbitrary Unverified Source

The new theorem depends on the exact `T-018` data.
An arbitrary source file, retained-status declaration, or plausible-looking `Verdict`
object does not prove the numerical result.
The durable path replays Conditions 1–5 on the frozen source bytes, binds the derived
record to their SHA-256, and then applies the separately recorded exact-containment
lemma. The public limit derivation does not accept a supplied verdict.

I attempted two concrete substitution attacks on the retained path.
First, comparing only condition names, total mass, and a reported minimum lets a verdict
from one certificate be attached to another; changing `n` is one simple negative control
when the closed-form reports are not recomputed.
Recomputing Conditions 1–4 narrows that attack but does not authenticate Condition 5 for
changed atom geometry.
Second, hashing one read of a path and parsing a later read can bind the record to bytes
other than the ones verified.
The integrated implementation closes both attacks.
`build_limit_record` parses one bounded byte snapshot with the retention gate’s strict
loader, verifies that in-memory certificate through Condition 5, hashes that snapshot,
and rereads the path before publication.
The shared raw JSON loader rejects duplicate keys.
Negative controls cover the changed-`n` verdict substitution, path substitution, and
duplicate-key cases.

The convenience explicit-factor mode still inherits Condition 5 from a retained source
instead of replaying it, and says `not replayed here` in its output.
It is a diagnostic, not the retention or promotion path, and its output alone is not
durable evidence.

### The $L/B$ Mistake

The sharp ceiling is

$$
c_*=\frac{\sqrt{1+D^2}}{B(1+D)},
$$

not $1/B$. Since $D>0$,

$$
\sqrt{1+D^2}<1+D,
$$

and therefore $c_*<1/B$. At the erroneous factor $1/B$, the squared test would require
$(1+D)^2<1+D^2$, or $2D<0$, which is false.

## Implementation Checks and Promotion Recommendation

The integrated implementation matches the reviewed theorem:

- the full `T-018` source replay and SHA-256 binding precede derivation of the record;
- the verifier decision, including Condition 5, is bound to the same in-memory
  certificate parsed from the exact bytes whose digest is recorded;
- duplicate JSON keys are refused on that raw-byte path, and negative controls exercise
  certificate/verdict substitution and file-read substitution;
- the new family is labeled as a sharpened exact-containment corollary, not as scaled
  data satisfying frozen Condition 4;
- every decision uses the rational squared inequality, while radicals and decimals are
  presentation fields;
- $q_+=500003/500000$ is accepted by the exact squared test while failing frozen coarse
  Condition 4, with the exact slack recorded above;
- the generated record and reader documents state `>=`, no endpoint certificate, and no
  compactness requirement; and
- the retained Conditions 3 and 5 are reused only through the frozen full replay and the
  proved invariance steps above.

The integration conflict resolution also keeps the source review dates distinct: `T-018`
remains reviewed through `2026-09-05`, while the new `T-022` evidence records
`2026-09-06`.

On the exact integrated tree, all 20 focused dilation-corollary tests pass.
An independent rational-arithmetic check reproduces the source digest, $D$, $R$,
$S_*^2$, and the record’s weak relation and endpoint flag.
The review’s eight local links resolve, and the one-file review diff has no whitespace
errors.

I recommend accepting `T-022` and, once this independent review is retained and mapped
as non-superseded, promoting its confirmation from C3 to C5. The review supports C5’s
review-ready rung, not C4’s requirement for a second method-distinct derivation.
Conditions 3 and 5 enter the promoted result only through the same-source replay and the
invariance proof, not through declarations copied into the result record.

## Literature and Priority Scope

The refreshed public-search receipt records searches for the refined decimal, radicand,
radical expression, and topic.
arXiv, OpenAlex full text, and general-web searches returned no result on the recorded
routes. Crossref returned no exact endpoint hit; its radicand and topic searches had
broad tokenized matches, with no refined endpoint in the first five inspected results on
either route.

The
[`exact-endpoint literature receipt`](../../../packing/resources/web/s11-exact-endpoint-literature-audit-2026-09-06/README.md)
and the broader
[`s(11)` lower-bound audit](../../../packing/resources/web/s11-lower-bound-literature-audit-2026/README.md)
are supporting searches, not priority proofs.
They do not exhaust subscription-only full text, theses, non-English or unindexed
sources, private correspondence, or unpublished work.
I did not independently repeat the live queries.
The evidence supports only the scoped label **apparently novel**; mathematical
acceptance does not depend on that label.

## Residual Risks

- The sharpened containment argument is a human proof, not a proof-assistant
  formalization. It inherits the retained theorem and source verifier’s correctness
  assumptions, mitigated by the independent standard-library replay.
- The source digest identifies the certificate bytes, not the verifier implementation.
  A portable proof package must carry or identify both; the repository commit and
  validation gate bind the verifier version operationally.
- The explicit-factor command is a convenience calculation over a retained premise; it
  does not replay Condition 5 and must not replace `--check-limit-record` in an evidence
  or promotion workflow.
- An algebraic endpoint is easier to mistranscribe than a rational one.
  The reduced value of $S_*^2$, the squarefree radicand, and the primitive quadratic
  above provide independent exact cross-checks.
- This result is the uniform fixed-$B$, single-core strict-containment supremum.
  It does not close direction-specific or multi-core improvements, including possible
  equality arguments outside the present theorem.
- Fit at $S_*$, any strict improvement beyond it, and absolute literature priority
  remain unresolved.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
