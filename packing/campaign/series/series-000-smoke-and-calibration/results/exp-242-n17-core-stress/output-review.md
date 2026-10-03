# H258 Common-Core Stress: Independent Output Review

Reviewed on 2026-10-02 after the single target run of the repaired instrument, whose
SHA-256 `88ffe6112ca49841c3eb1328723e323255fa88698748bb55b4793136599884ff` is recorded
in the receipt and equals the blob committed at
`2fbf8d2933e6a8f51268b87be111a5c03d9f95cf`. The run executed the uncommitted working
tree at `16d7975546`, as [provenance.log](run-001/provenance.log) states; the commit
that followed carries the same bytes.
The retained outputs satisfy every item of
[H258’s acceptance criterion](../../../../hypotheses/H-258-n17-common-core-stress.md)
that the instrument can decide, and this review supplies the remaining item: an
independent mathematical, code and output review finds **no blocking defect**. The
disposition `confirmed_fixed_stress` stands: all 58 normalized weights are nonnegative
on the accepted H255 box, six of them exactly zero, and the 52 stationarity identities
hold at the root. The coordinator owns the recorded verdict.

This review read the instrument, its tests, the four input receipts, both JSON outputs,
the command, provenance and timing files, and the frozen derivation documents.
It did not rerun the producer’s target command.
It reran the instrument’s eleven fast tests (all pass in 4.1 s; the slow
substituted-ring test was deselected) and it rebuilt the whole certificate independently
in [`audit/recompute_h258.py.txt`](audit/recompute_h258.py.txt), with the sympy checks
[`verify_closed_forms.py.txt`](audit/verify_closed_forms.py.txt) and
[`verify_f2_binding.py.txt`](audit/verify_f2_binding.py.txt) beside it; their outputs
are the matching `.out.txt` files and `recompute_h258.summary.json` in
[`audit/`](audit/). The scripts were written in the session scratch directory and are
retained with a `.txt` suffix, as earlier independent reviews were, because the lint
floor admits no unlinted Python under `packing/`. That code imports nothing from
`devtools`: the 58 rows come from the
[first-order review](../../../../../../docs/project/reviews/review-2026-10-01-n17-first-order-branches.md),
the loads, forces and moments from the
[core-stress review](../../../../../../docs/project/reviews/review-2026-10-01-n17-core-stress.md),
the centres from the H254 chart as H256 fixes them, and the arithmetic is `Fraction`, a
private degree-tracking type, and a private outward-rounded interval type on a
$2^{-300}$ grid rather than the producer’s $2^{-256}$ grid.

## The Frozen Allocation Is What the Code Computes

`load_scales` evaluates the closed forms $P,Q,P_\theta,Q_\theta$, $(F_1)_\theta$,
$(F_2)_\theta$, $(F_2)_\beta$, $(G_3)_\theta$, $(G_3)_\beta$ of the core-stress review
with the side passed in as an argument, and `_layout` supplies $S=(6+4t)/(1+2t-t^2)$ to
it. That is “differentiate with $S$ fixed, then substitute $S(t)$”, because the closed
forms are the fixed-$S$ partials.
Two separate facts establish that they are: `verify_closed_forms.py` differentiates
$F_1,F_2,G_3$ in trigonometric form with $S$ an independent symbol and finds each
difference from the closed form simplifies to zero; and the producer’s own
`_load_derivative_controls` proves the same five equalities in its ring with $S$ a
generator, then shows that differentiating after substitution gives a different
$(F_1)_\theta$ and $(F_2)_\theta$ (after substitution $F_1\equiv0$, which the sympy
check also reproduces).
The loads $\nu=(G_3)_\beta$, $\rho=-(F_2)_\beta$, $\mu$, $Z$, $L$, $R$ and $K$ follow
the frozen formulas line for line.

The 58 rows are emitted in the frozen order: fourteen axis walls as $W_-$ then $W_+$,
square 9’s single smooth row, then the twenty contacts in H254 order with $E_-$ before
$E_+$ on the nine parallel faces.
The row entries match the first-order review: wall rows $\pm\xi$ or $\pm\eta$ with
$\mp\omega_i/2$ and a $\sigma$ entry on right and top walls; square 9’s row
$\xi_9-\tfrac{c-s}{2}\omega_9$; parallel faces
$n\cdot(V_j-V_i)+\tfrac{\tau}{2}(\omega_i+\omega_j)\mp k(\omega_j-\omega_i)$ with $\tau$
read off as $Jn\cdot(r_j-r_i)$; smooth contacts with the owner from the review’s table,
the owner coefficient $Jn\cdot(r_j-r_i)-h'$ and the nonowner coefficient $h'$. The
nonowner supporting-corner offsets are the review’s fixed table ($(u+v)/2$ for $3\to9$,
$(e_x-e_y)/2$ for $4\to10$, $14\to7$, $15\to16$, $16\to17$, $(p+q)/2$ for $12\to16$,
$(e_x+e_y)/2$ otherwise), encoded as `CORNER_SIGNS`; the interval path refuses unless
each projection $n\cdot a$ has the strict sign the table assumes, and my run confirms
all 22 signs on the box.
The force and wall tables, $B_2,B_3,B_7$, the wall moments, the baseline residuals
$b_9,\ldots,b_{14}$ and the five tree allocations $q_{9,10}=-b_9$,
$q_{10,12}=-b_9-b_{10}$, $q_{11,12}=-b_{11}$, $q_{13,14}=-b_{13}$,
$q_{12,14}=b_{13}+b_{14}$ are the review’s, and the row-weight splits $(f\pm q/k)/2$ and
$f/2\mp m$ carry the stated signs.
The two prescribed residuals are $+\gamma\rho F_2/K$ at $\omega_{12}$ and
$-\gamma\rho F_2/K$ at $\omega_{16}$, with $F_2$ computed from $X$ and $Y$ exactly as
the chart defines it.

The ring proof is sound.
A value is $N/\prod_i f_i^{e_i}$ with $N$ a polynomial in
$\mathbb{Q}[t,b,S,\mu,\nu,\rho]$ and every $f_i$ a registered monic factor of a
polynomial the computation inverted; the registry only grows, `reduced` cancels a factor
only after `divmod` returns a zero remainder, and `register` refuses a factorization
that does not reproduce its input.
A numerator that is the zero polynomial therefore means the rational function is zero,
and evaluating at any point where every registered factor is nonzero gives zero.
`denominator_guards` evaluates each of the 11 registered factors on the H255 box by
outward interval arithmetic and refuses a factor whose enclosure contains zero; the
`foreign` check refuses a factor involving $S$, $\mu$, $\nu$ or $\rho$, which the guard
could not evaluate. Substituting the root is then valid: the identities are proved for
all $(t,b)$ off the eleven zero sets, the box avoids all eleven, the root lies in the
box, and at the root $F_2=0$ because the receipt binds $F_2\,t(1+t)(1+t^2)(1+b^2)=\Pi_2$
to the H255 polynomial, whose root the accepted H255 certificate encloses;
`verify_f2_binding.py` reproduces that binding from the exp-237 polynomial list.

## Nothing Passes Vacuously

Every refusal reaches the exit code.
`ring_residual_proofs` raises on any failed identity, `denominator_guards` raises on any
straddling factor, `interval_sign_audit` raises on a nonpositive guard, a wrong offset
branch, or a prescribed zero weight that is not the exact interval $[0,0]$, and
`criterion_passed` is the interval audit’s own `passed`. Synthetic controls run before
`_read_limited` is first called, and two tests pin that order with a reader that raises.
The nine mutations each fail in the columns one expects: the square 16 angle sign in
column 47 only, the omitted $\omega_{12}$ residual in column 35 only, the dropped
normalization term in column 51 only, the dropped `8 top` row in columns 22, 23 and 51.
The 18 row-derivative controls compare the reduced rows with exact one-sided jets of the
owner gaps, including $\tau=1$, and the interval controls include a negative operand, a
division, a zero-straddling divisor refusal and an off-grid endpoint refusal.
The $2^{-256}$ `Dyadic` type rounds every result outward with exact integer floor and
ceiling, inherits only operations whose helpers it overrides, and refuses a reciprocal
across zero. Weights are normalized by $K$ after the sign guard $K>0$, and the ten
oblique capacities $kf\pm q$ are checked unnormalized, which is equivalent since $k>0$
follows from the checked $\tau<1$.

Receipt fields are bound to their inputs.
The three receipt refs name Git blobs, `_frozen_bytes` compares each input file with
`git show` of its blob byte for byte, the H255 certificate is reverified by
`check_root`, the H256 and H257 receipts must carry the same source digest and the same
box, and `instrument_sha256` is the running file’s own digest.
I confirmed the three blobs match the files on disk and the source digest `24e296f5…`
matches the Kleddamag certificate.

Four notes, none blocking:

- The exact zero offsets of the three axis faces are a premise the instrument takes from
  the layout rather than a check it names.
  `_verify_tied_row_shapes` compares the rows’ $\tau$ with the same $\tau$, and the
  interval audit requires only $|\tau|<1$ on those faces.
  The premise is true by construction: $x_1=x_3=1/2$, $y_1=y_2=1/2$ and $x_5=x_7=S-1/2$
  in `_layout`, so each $\tau$ is the zero rational function and the ring proof carries
  it as a zero numerator; my recomputation finds the three offsets exactly zero at every
  rational point evaluated.
  A one-line `is_zero` assertion for `AXIS_FACES` would close the gap.
- `minimum_capacity_lower_bound` is reported as `0.0` because the zero-force 9/11 face
  is included. The minimum over the five oblique obligations is $0.0098987$ (the
  $11\to12$ face), which is the number the contract asks about.
- The receipt’s interval $\tau_{5,7}=[-2.07\times10^{-22},\,2.07\times10^{-22}]$ is a
  subtraction artifact, $x_7-x_5$ evaluated as intervals; my $2^{-300}$ enclosure gives
  the same width. It is harmless, since $k=1/2$ is fixed for that face and the exact
  value is zero, but a reader should not take it as a certified nonzero offset.
- The hypothesis record still says `instrument_ready: false` and carries the “Instrument
  Stop Before Target Use” section from Session 165, while the committed instrument sets
  `INSTRUMENT_READY = True`. The record needs the coordinator’s update at disposition.

## Independent Recomputation Agrees Everywhere

The exp-237 box has midpoint $(0.36204389\ldots,\,0.33094867\ldots)$ and radii
$9.86\times10^{-24}$ and $6.53\times10^{-23}$; these are the Krawczyk inclusion bounds
the receipt copies, not the $10^{-12}$ search radius.

At the midpoint, exact rational arithmetic gives $\mu=0.150929052718$,
$\nu=0.517331893718$, $\rho=0.042972149174$, $Z=0.527415499727$, $L=0.540457953988$,
$R=0.491480313447$, $K=1.72647759358$, and partials $(F_1)_\theta=0.982782975$,
$(F_2)_\theta=-0.281601516$, $(F_2)_\beta=-0.042972149$, $(G_3)_\theta=-0.061645926$,
$(G_3)_\beta=0.517331894$. These match the
[route review](../../../../../../docs/project/reviews/review-2026-10-01-n17-route-after-pr265.md)
to its printed precision and satisfy the core-stress review’s coarse bounds.
The 58 weights have exactly six zeros, the prescribed ones, no negative entry, and the
smallest positive normalized weight is $0.00607896395682$ on the $11\to12$ $E_+$ row;
the receipt reports the same key and the lower bound $0.0060789639568182355$. The
baseline residuals are $b_9=-0.033376$, $b_{10}=0.036065$, $b_{11}=-0.010366$,
$b_{12}=0.040282$, $b_{13}=0.076330$, $b_{14}=-0.108935$, and their sum equals
$\gamma\rho F_2$ exactly, $6.34\times10^{-62}$ at the midpoint.

| Oblique face | $\tau$ | $k$ | $q$ | $kf+q$ | $kf-q$ |
| --- | ---: | ---: | ---: | ---: | ---: |
| $9\to10$ | 0.056839 | 0.471581 | 0.033376 | 0.288246 | 0.221493 |
| $10\to12$ | 0.276427 | 0.361787 | −0.002689 | 0.051915 | 0.057293 |
| $11\to12$ | 0.056839 | 0.471581 | 0.010366 | 0.030631 | 0.009899 |
| $12\to14$ | 0.128052 | 0.435974 | −0.032605 | 0.033196 | 0.098407 |
| $13\to14$ | 0.080576 | 0.459712 | −0.076330 | 0.149610 | 0.302269 |

The capacities $kf-|q|$ are the route review’s $0.221$, $0.052$, $0.0099$, $0.033$,
$0.150$, and every one of the receipt’s ten capacity intervals overlaps mine.

The identity
$A^{\mathsf T}\lambda=K e_\sigma+\gamma\rho F_2(e_{\omega_{12}}-e_{\omega_{16}})$ holds
exactly, in all 52 columns, at the midpoint, at a second rational point inside the box,
and at $(1/3,1/5)$, $(37/100,33/100)$ and $(2/7,3/11)$; dividing by $K$ gives the
normalized form with the two prescribed residuals.
Beyond evidence at points, the recomputation proves the identity as a rational function
by a route independent of the ring: a degree-tracking pass through the same expression
tree bounds every residual’s numerator by degree 134 in $t$ and 10 in $b$ over a product
of 165 inverted atoms, and the 52 residuals vanish at all $135\times11=1485$ points of a
rational product grid with no zero denominator, so each numerator is the zero
polynomial. That took 3.5 s.

The interval audit on the box, with the private $2^{-300}$ type, finds all 15 guards
$c,s,d,e,\alpha,\gamma,T,(F_1)_\theta,\mu,\nu,\rho,Z,L,R,K$ strictly positive, the 22
corner-offset projections of the expected strict sign, the five oblique offsets strictly
inside $(0,1)$, 52 weights strictly positive, 6 exactly $[0,0]$, no straddle, and ten
positive capacities.
Every one of the receipt’s 58 weight, 15 guard, 9 offset and 18 capacity intervals
overlaps mine; the producer’s widest weight interval is $4.4\times10^{-21}$. Both
enclosures establish the required signs, as the contract asks of a separately
implemented auditor.
Every quantity my computation inverts keeps a strict sign on the box: $1+t^2$, $1+b^2$,
$1+2t-t^2$, $c$, $s$, $c^2$, $s^2$, $(F_1)_\theta$, $K$ and the five oblique $k$.
Factoring those numerators with sympy gives exactly eleven distinct monic irreducible
factors, and their (degree in $t$, degree in $b$, term count, sign on the box)
descriptors are the receipt’s eleven as a multiset: $t^2+1$, $b^2+1$, $t^2-2t-1$ (−),
$t-1$ (−), $t+1$, $t$, $t^2+3t-2$ (−, from $(F_1)_\theta$), $t^5-t^4+10t^3-10t^2+9t-1$
(from $k_{9,10}=k_{11,12}$), $t^3-t^2+t+1$ (from $k_{10,12}$), $t^4+10t^3-8t^2+10t-1$
(from $k_{13,14}$) and the 69-term degree-(12,6) numerator of $K$ (−);
$k_{12,14}=t(t+1)/(1+t^2)$ adds nothing new.
The registry hides no zero.

## The Certified Point and the $5\to7$ Face

Lane A2 asked whether $k=1/2$ is exact on the $5\to7$ face, since $\tau_{5,7}=-a$ when
square 5 slides a distance $a$ from the right wall.
At the point H258 certifies, $a=0$: `_layout` puts square 5 at $(S-1/2,\,1/2)$ and
square 7 at $(S-1/2,\,3/2)$, so the right-wall clearance $S-x_5-1/2$ and the offset
$x_7-x_5$ are both the zero rational function, and the H256 receipt lists `5 right`
among its 15 wall identities.
Likewise $b=0$ for square 11, whose $9\to11$ contact is one of H256’s 21 pair
identities. So $k=(1-|\tau|)/2=1/2$ exactly, and no certified number changes.
These are the two one-sided motions the first-order review catalogues; the receipt
retains their rows, `5 right` and `9/11`, with exact zero weight, which is how the
certificate covers the cone at that corner.

The documents describe this point accurately if “centroid sliders” is read as H256
defines it: the two sliders $\lambda_6$ and $\lambda_{13}$ sit at the centroid of their
feasible triangle, while every other centre, squares 5 and 11 included, sits at the H254
equality chart, in contact.
The core-stress review’s “unchanged H254 centres, centroid sliders, and root enclosure”
says exactly that. The hypothesis record’s compressed “H256 centroid/H257 feature
inventory” could be misread as placing every free coordinate at a centroid; it does not
change the geometry, and the receipt describes the point only through its three bound
receipts and the box, which is accurate.

## Receipt Binding and Execution

The target receipt is 45,895 bytes with SHA-256
`a9b1bcf0b2a5665d5eb02c18e89d200add23c993db2472df1018dcef2144e6b1`; the controls-only
receipt is 2,815 bytes with SHA-256
`271e520027ec9d8371a79034314cd4c3e6c3ad6fb9b87e26d48534eeabfb6c65`, and its five control
sections agree with the copy inside the target receipt in every field but the seconds.
The receipt’s `root_git_ref`, `endpoint_git_ref` and `feature_git_ref` name blobs
`7866e2623`, `ad7a36ed0` and `feafdae49`, whose bytes match the exp-237, exp-238 and
exp-239 certificates on disk (SHA-256 `883f51b9…`, `f052f6ae…`, `f6ba220a…`); the
[H257 output review](../exp-239-n17-endpoint-features/output-review.md) records that
inventory as accepted.
The root verification inside the receipt passed, and the receipt’s box equals the
exp-237 midpoint and inclusion bounds.

[command.txt](run-001/command.txt) retains both invocations under
`timeout --signal=TERM --kill-after=5s 300s`, `ulimit -f 10240` and the optional 1 GiB
data-segment limit, with bytecode writes disabled, the project interpreter and one
worker; [provenance.log](run-001/provenance.log) records Python 3.14.7, sympy 1.14.0,
assertions enabled, HEAD `16d7975546` with the two instrument files modified, and a load
average of 1.07.

| Process | Wall Seconds | User Seconds | Exit | JSON Bytes |
| --- | ---: | ---: | ---: | ---: |
| Controls only | 3.342 | 3.282 | 0 | 2,815 |
| Target | 30.881 | 30.167 | 0 | 45,895 |

Inside the target’s 30.19 s: controls 2.99 s, the inherited H256 chart identities 20.13
s, the ring proof 6.59 s (of which the substituted normalized stage 5.97 s), the
denominator guards 0.03 s and the interval audit 0.05 s. Every output is below the 10
MiB ceiling and both processes finished far inside the 300 s ceiling.
[before-stall-reproduction.txt](run-001/before-stall-reproduction.txt) retains the
Session 165 stall (exit 124 at 90 s) and the 21.2 s cost of the unchanged H256
foundation, so the repair’s saving is measured, not asserted.

## The Auditor Question

The frozen criterion reads: “Confirm only if all 52 normalized residuals vanish exactly
at the H255 root, all prescribed weights are nonnegative by exact identities or interval
lower bounds at least zero, every denominator and normal-force guard is strict positive,
H257 feature completeness is accepted, synthetic controls pass and independent
mathematical/code/output review finds no blocking defect.”
It names a review, not a second program.
By contrast, H255’s criterion demanded that “the producer and separately implemented
certificate checker agree”; H258’s does not.

The body adds two sentences about how interval conclusions are to be audited: “Retain
exact symbolic equalities and independently audit all interval conclusions,” and, in the
arithmetic contract, “The independent auditor implements the enclosure operations
separately and reports any differences between its bounds and the producer’s bounds;
both must establish the required signs.”
This review satisfies both as written: the enclosure operations are implemented
separately (a different grid, a different rounding routine, a different matrix builder),
every bound is compared with the producer’s and the differences are reported above, and
both establish the required signs.
A finished `audit_n17_core_stress.py` is therefore not a condition of acceptance.
The draft refuses every invocation by design and should either be completed in a later
slice or stay marked unready; what matters for the record is that the independent
arithmetic be retained.
The recomputation script and its outputs live in the session scratch directory; the
coordinator may copy them into an `audit/` directory beside `run-001/`, as exp-238 and
exp-239 did, so the evidence survives the session.

## Verdict

| Criterion item | Finding | Status |
| --- | --- | --- |
| 52 normalized residuals vanish exactly at the H255 root | Ring proof with guarded denominators; independent grid proof; $F_2=\Pi_2/(t(1+t)(1+t^2)(1+b^2))$ bound | Met |
| Prescribed weights nonnegative by exact identity or lower bound $\ge0$ | Six exact zeros, 52 strictly positive, ten positive capacities, in two enclosures | Met |
| Every denominator and normal-force guard strictly positive | 11 registered factors and 15 guards strict on the box, confirmed independently | Met |
| H257 feature completeness accepted | Bound to blob `feafdae49`, accepted in its output review | Met |
| Synthetic controls pass | Both runs, before any target read; all nine mutations refused | Met |
| Independent mathematical/code/output review, no blocking defect | This review | Met |
| Threshold: exact identity, no tolerance, strict guards | No tolerance anywhere in the identity or sign paths | Met |
| Regime: unchanged H255 box, accepted H256/H257, fixed allocation | No refinement, no alternate allocation, the box is exp-237’s | Met |
| Cost: one worker, 300 s, 10 MiB | 30.9 s, 45,895 bytes | Met |

No blocking defect. The four notes above are improvements to naming, reporting and the
hypothesis record; none changes a certified number.
What is certified is first-order stationarity of the complete 58-row common core at the
accepted endpoint under its feature premises: nonnegative side velocity on both corner
branches.
It leaves the zero-side motions, higher-order local analysis and global capture
as the separate obligations the hypothesis names, and it does not meet H027’s
quantitative class-angle threshold.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
