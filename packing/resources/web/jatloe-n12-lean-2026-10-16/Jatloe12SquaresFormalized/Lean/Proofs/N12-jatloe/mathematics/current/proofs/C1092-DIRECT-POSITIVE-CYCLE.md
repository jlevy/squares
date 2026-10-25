# C1092: the complete direct all-positive cycle

All constants are exact rationals. Ownership is strict ownership by the named actual square; exclusions and separating supports may be tangent. The proof uses the four actual central squares, the four actual boundary squares, their actual paired corners, and the actual box walls. It uses no center history, angle subdivision, or enumeration of numerical angle values.

The entrance is the direct one proved in `C1092-POSITIVE-D-TRANSFER.md`, `C1092-POSITIVE-QUADRANT-BOOTSTRAP.md`, and `C1092-POSITIVE-WALL-POINTS.md`. The scalar endpoint companions are `C1092-POSITIVE-ENDPOINT-SCALARS.md` and `C1092-CB-ENDPOINT-SCALARS.md`. The BB reduction and the BC curvature scalar are proved in `C1092-POSITIVE-BB-REDUCTION.md` and `C1092-BC-CURVATURE-SCALAR.md`. Nonpositive boundary angles are handled by `C1092-NONPOSITIVE-BOUNDARY-POTENTIAL.md`.

## 1. Actual entrance and theorem

Retain the original last C1092 MPPM auxiliary assignment

    (0,0,0,0,9217,32848,590336,16424,2050,4100,262400,131200).

Use the quarter turn R(x,y)=(4−y,x). In sector chart R⁻ⁱ the central owner is C_i=Q_(4+i), and the boundary owners are

    (B₀,B₁,B₂,B₃)=(Q₉,Q₁₀,Q₁₁,Q₈).

All actual squares have common side a>1, pairwise disjoint open interiors, and closures in [0,4]². The original MPPM condition gives center(B_i)_x≤2 in each chart. Suppose that all four central canonical angles p_i are strictly positive.

The cited direct entrance theorems prove, in every sector,

    0<tan(p_i/2)<1/5,
    −1/8<tan(β_i/2)<1/3,
    center(C_i)_x<3/2<center(C_i)_y,

and the following actual strict points:

    C_i owns L₀=(1,1.6), U₀=(1,1.74), T=(1.74,2),
              H=(1,1.5), X=(1.5,2);
    B_i owns (2,.914), (1.74,1), P=(2,1).

The original paired corner owns A=(1,1). The preceding actual boundary owns D=(1,2), while the next actual central, denoted J=R(C_(i+1)) in the present chart, owns

    (2.26,1), E'=(2,1.5).

The corresponding forced faces of C, for u_p=(c,s), v_p=(−s,c), are

    u_p·(C−A)≥a/2,
    v_p·(D−C)≥a/2,
    u_p·(E'−C)≥a/2.                                (1)

Here and below C,J,B in a vector formula denote actual centers. The strict points have their original actual owners; in particular E' comes from the next central's strict X, and D from the preceding boundary's strict P.

**Theorem 1.** These actual all-positive squares do not exist. Consequently the entire all-positive canonical-angle sector of the original last C1092 assignment is excluded by a continuous proof.

## 2. Exact central projections and actual separating directions

Write C=(3/2−X₀,3/2+Y₀), with X₀,Y₀>0. The first two faces in (1) imply

    cX₀−sY₀≤(c+s−a)/2,
    sX₀+cY₀≤(c+s−a)/2.

Since c≥12/13, s≤5/13, and c+s≤17/13, they give

    X₀≤(c+s)(c+s−1)/2≤34/169,
    Y₀≤(c+s−1)/(2c)≤1/6.                           (2)

The next center is J=(5/2−Y_next,3/2−X_next). Therefore J−C has positive horizontal and negative vertical components. For every central angle r in the full allowed range,

    |v_r·(J−C)|
      ≤(5/13)(1+34/169)+34/169+1/6<1.               (3)

Every forward first-normal projection is positive: it is at least

    (12/13)(5/6)−(5/13)(34/169+1/6)>0.

Thus neither transverse normal nor either backward first normal can separate the two actual central squares. Only u_p or u_q can do so, where q is the next central angle. The first-normal projection decreases with its angle because J−C has the displayed coordinate signs. Hence the smaller actual angle always supplies the exact bound

    u_min(p,q)·(J−C)≥a H(q−p),
    H(r)=(1+cos r+|sin r|)/2.                       (4)

No original normal source is discarded by approximation in (4).

For B→C, the strict point differences T−(1.74,1)=(0,1) and L₀−(2,.914)=(−1,.686) force every oriented separator n to satisfy

    n_y>0,  n_x<.686n_y.

When β≥0, only v_p or v_β among the actual square normals can satisfy this cone. For B→J, the strict differences (2.26,1)−P=(.26,0) and E'−(2,.914)=(0,.586) force n_x>0 and n_y>0. If β≥0, only u_q or u_β remain. Thus the four positive-boundary source labels CC, CB, BC, BB are exhaustive; the first letter chooses the B→C normal and the second the B→J normal.

In its own chart define each central's two projections relative to O=(2,2):

    G_i=u_(p_i)·(O−C_i),  L_i=v_(p_i)·(O−C_i).

The first and third faces in (1) give the crucial narrow interval

    a/2+s_i/2≤G_i≤c_i+s_i−a/2.                    (5)

The left endpoint is the new E' face, not an estimate from a terminal center box. Put

    g_i=c_i+s_i−1/2,
    g_j^lo=(1+s_j)/2,  g_j^hi=c_j+s_j−1/2.

The interval in (5) is contained in [g_i^lo,g_i^hi]. Its order follows from

    g_j^hi−g_j^lo=c_j+s_j/2−1
      =y(1−2y)/(1+y²)≥0,

where y=tan(q/2).

## 3. The exact two-angle support combination

Fix one positive-boundary edge. Set

    x=tan(p/2), y=tan(q/2),
    c=cos p, s=sin p, d=cos q, t=sin q,
    h=cos β, b=sin β,
    κ=cos(q−p), σ=sin(q−p), H_delta=H(q−p),
    f(x)=(1−c)(2c−1)/c, e=y−x−f(x).

All subsequent scalar work is on the full closed ranges 0≤x,y≤1/5 and 0≤tan(β/2)≤1/3. Set

    C_p=cos(p−β), S_p=sin(p−β),
    C_q=cos(q−β), S_q=sin(q−β).

Let α be p or β according to the vertical source, and let η be q or β according to the horizontal source. Multiplication of the two actual separating inequalities by cos η and sin α eliminates the boundary's horizontal coordinate, because

    cos η v_α+sin α u_η=cos(α−η)(0,1).

The actual bottom wall gives B_y≥a(h+b)/2. Thus the two supports and the wall imply

    2D₀−A₀L_i+B₀L_j+F₀G_i+G₀G_j≥aS,

    S=cos η H(p−β)+sin α H(q−β)+D₀(h+b)/2.        (6)

All quantities in (6) are exact. Their coefficients are

| Source | A₀ | B₀ | F₀ | G₀ | D₀ |
|---|---|---|---|---|---|
| CC | d | s | 0 | 0 | κ |
| CB | h | sC_q | 0 | sS_q | C_p |
| BC | dC_p | b | −dS_p | 0 | C_q |
| BB | hC_p | bC_q | −hS_p | bS_q | 1 |

The actual central inequality (4) is

    G_i+κL_j+σG_j≥aH_delta     if q≥p,
    κG_i+σL_i+L_j≥aH_delta     if q≤p.             (7)

For q≥p set

    λ=(A₀−B₀)/κ, ω=A₀,
    I=F₀+λ, J₀=G₀+λσ;

for q≤p set

    λ=(A₀−B₀)/(1+σ), ω=B₀+λ,
    I=F₀+λκ, J₀=G₀.

Adding λ times (7) to (6) gives

    ω(L_j−L_i)+I G_i+J₀G_j
      ≥a(S+λH_delta)−2D₀.                          (8)

Every λ,ω,I is positive. For λ and ω, it suffices to check A₀−B₀>0. The respective lower bounds in the four rows are 7/13, 27/65, 9/65, and 1/25, using c,d≥12/13, h≥4/5, s,t≤5/13, b≤3/5, and C_p,C_q≥4/5. The denominators κ and 1+σ are at least 12/13 and 8/13.

For I, the CC and CB rows are immediate. In the BC and BB rows, if β≥p then F₀≥0. If β≤p, put r=cos η; then r≥12/13, A₀≥rc, B₀≤s, and F₀≥−rs. On an ascending edge

    I≥r(c−s)−s≥19/169>0;

on a descending edge

    I≥rcκ−sκ−rs≥(12/13)³−10/13=38/2197>0.

Also S+λH_delta>0. We may therefore set G_i to g_i and check either endpoint g_j∈{g_j^lo,g_j^hi}. Dropping a>1 to one in (8) is strict. Define the scalar target numerator

    F_label(β)=S+λH_delta−2D₀−I g_i−J₀g_j+ωe.    (9)

If both endpoint choices make (9) nonnegative, then (8) proves strictly

    L_j−L_i>f(x)−(y−x).                            (10)

All remaining work is to prove the signs in (9), with the exact original normal sources retained.

## 4. A common scalar parameter for both angle orders

For q≥p define

    T_*=(H_delta−g_i−σg_j)/κ;

for q≤p define

    T_*=(H_delta−κg_i−σe)/(1+σ).                   (11)

The definitions agree on p=q. The lower bound proved in `C1092-BC-CURVATURE-SCALAR.md` is

    T_*≥5/26.                                      (12)

We also need T_*≤1/2. On an ascending edge g_i,g_j≥1/2 and σ≥0, so the numerator in (11) is at most κ/2.

For a descending edge put r=x−y and τ=tan(p−q). Algebra in (11) shows that T_*≤1/2 is equivalent to

    τ[1−r−f(x)]≤c+s−1.                            (13)

For fixed x, the left side increases with r∈[0,x]. Indeed

    dτ/dr=2(1+τ²)/(1+(x−r)²)≥25/13,
    1−r−f(x)≥51/70, τ≤5/12,

so its derivative is at least (25/13)(51/70)−5/12>0. At r=x, the difference between the right side of (13) and the left side is exactly

    4x⁴(1−2x−x²)/[(1+x²)(1−x²)²]≥0.

This proves, in both angle orders and for either needed endpoint,

    5/26≤T_*≤1/2.                                  (14)

We used 0≤f(x)≤11/156<1/14. The exact maximum is immediate from f=3−2c−1/c and c≥12/13.

Expansion of (9) now yields the following single table, valid for both angle orders. It makes the boundary-angle analysis especially short:

| Source | F_label(β) |
|---|---|
| CC | dH(p−β)+sH(q−β)+κ(h+b)/2−2κ+(d−s)T_*+de |
| CB | hH(p−β)+sH(q−β)+C_p(h+b)/2−2C_p−sS_qg_j+(h−sC_q)T_*+he |
| BC | dH(p−β)+bH(q−β)+C_q(h+b)/2−2C_q+dS_pg_i+(dC_p−b)T_*+dC_pe |
| BB | hH(p−β)+bH(q−β)+(h+b)/2−2+hS_pg_i−bS_qg_j+(hC_p−bC_q)T_*+hC_pe |

This is only an exact rearrangement of (9) and (11), not a new estimate.

## 5. The CC source and its two angle endpoints

In the CC row only

    S_CC(β)=dH(p−β)+sH(q−β)+κ(h+b)/2

depends on β. On each interval cut by p and q it is concave: its second derivative is −[S_CC−(d+s)/2]<0. For β≥max(p,q) it is increasing, since each relevant cosine-minus-sine derivative is positive. Its minimum is therefore among β=0,p,q.

If q≥p, then

    S_CC(q)−S_CC(p)
      =(d−s)[H_delta−1]+κ[(d+t)−(c+s)]/2≥0.

Writing A=1+x², B=1+y², direct substitution gives

    S_CC(0)−S_CC(p)=2x²P/(A²B),

    P=1−4y−y²−x²−2xy²+2x+4xy+x²y²≥13/125>0.

The last estimate simply bounds the displayed negative terms on x,y≤1/5. Thus the ascending CC minimum is at β=p, where the endpoint theorem proves (9).

If q≤p, the corresponding exact differences are

    S_CC(0)−S_CC(q)
      =2y²(1−y)[1+y−2x+2xy−x²(1+y)]/(AB²)≥0,

    S_CC(p)−S_CC(q)
      =2(x−y)²(1+xy−x+y)(1−x−y−xy)/(A²B²)≥0.

For the first sign, its bracket is at least 1−2/5−6/125>0; every factor in the second line is positive or zero. Hence the descending CC minimum is at β=q.

That last endpoint follows directly from the proved descending BC endpoint. In the original unnormalized scalar expressions, put N_label=ω E_label. At β=q,

    λ_CC=I_BC, ω_CC=κω_BC,
    N_CC−κN_BC=dσ(κ−1)≥0.                         (15)

Here σ≤0 and κ≤1. The identities follow by using H_delta=(1+κ−σ)/2, tκ−s=dσ, and the definitions in Section 3. Therefore E_CC(q)≥E_BC(q), and the latter satisfies the target by `C1092-POSITIVE-ENDPOINT-SCALARS.md`. This completes CC throughout the positive boundary-angle domain.

## 6. A source comparison and the ascending CB endpoint

The common table in Section 4 gives the exact identity

    F_BC/d−F_BB/h
      =b/(dh){(h−d)H(q−β)
          +S_q[(h+b)/2−2−tT_*+dg_j]}.             (16)

Since

    h−d=S_q η, η=(b+t)/(1+C_q),

the right side is bS_q Z/(dh), where

    Z=ηH(q−β)+(h+b)/2−2−tT_*+dg_j.                (17)

We prove uniformly that Z<0. First dg_j≤d(d+t−1/2)≤126/169. The last function increases with q throughout its interval: its derivative is at least

    1−2t²−(3/2)t≥43/338>0.

If β≤q, then

    ηH(q−β)
      =[(b+t)/2][1+tan((q−β)/2)]≤6/13.

Together with (h+b)/2≤7/10 and T_*≥0, this already makes Z<0.

If β≥q, the same expression is

    [(b+t)/2][1+tan((β−q)/2)].

It increases with β and with q. The β derivative is positive directly. For the q derivative, put k=tan((β−q)/2)≤1/3; it is at least

    (1/2)d(1+k)−(1/4)(b+t)(1+k²)
      ≥6/13−32/117=22/117>0.

Its maximum is at β=2 arctan(1/3), q=2 arctan(1/5). There C_q=63/65, |S_q|=16/65, η=1/2, and H(q−β)=72/65. Consequently

    Z≤36/65+7/10+126/169−2=−1/1690<0.             (18)

Thus (16) gives two useful implications:

    β≥q: F_BC/d≥F_BB/h;
    β≤q: F_BC/d≤F_BB/h.                            (19)

In particular, at β=p≤q the vertical normals coincide, so BC=CC and BB=CB. Hence

    F_CB(p)/c≥F_CC(p)/d≥0.                          (20)

This proves the ascending CB endpoint from the already proved ascending CC endpoint. Its ascending multiplier J₀ at β=p is nonnegative, so decreasing g_j only raises the target numerator. Thus (20) covers both choices needed below.

## 7. The BB source

The exact BB theorem in `C1092-POSITIVE-BB-REDUCTION.md` reduces this source to two inequalities:

    min F_BB(p)≥0,
    min F_BB(q)≥(d+t)(1−κ).                         (21)

The minima range over the two g_j endpoints. At β=p these are the CB endpoint. Its ascending order is (20), and its descending order is the last estimate of the endpoint theorem. At β=q these are the BC endpoint, with exactly the quadratic slack retained in both angle orders by that theorem.

The BB proof treats the remaining two endpoints β=0 and β=2 arctan(1/3) directly. Between 0,p,q and the upper endpoint, its tangent replacement makes the entire expression a concave quadratic in tan β, for each g_j choice. Therefore (21) supplies every required inner endpoint and proves

    F_BB(β)≥0

throughout the full positive boundary range, for both angle orders and both projection endpoints. The cited BB chapter includes all coefficient signs and the exact positive outer-endpoint margins.

## 8. The CB source: one uniform concavity bound

On an interval not crossing p or q, put ε_q=sign(q−β), and set

    A_*=1/2+T_*+e, C_*=1/2−T_*.

By (14) and the exact maximum of f,

    A_*≥329/780, 0≤C_*≤1/2, A_*≤6/5.             (22)

The part of F_CB linear in h,b is

    ell=hA_*−2C_p+sC_q C_*
          +sS_q(ε_q/2−g_j).

Since C_q>0, h≥4/5, and g_j−1/2≤4/13,

    −ell≤2−329/975+100/2197.                       (23)

Indeed if β≤q the only extra loss is at most

    sS_q(g_j−1/2)≤(5/13)(5/13)(4/13)=100/2197;

if β≥q the corresponding term in ell is nonnegative and causes no loss.

The remaining, quadratic, part of F_CB has second derivative −2R, where

    R=cos(2β−p)                                  if β≤p,
    R=(c−s)cos(2β)+(c+s)sin(2β)                  if β≥p.

In the first case R≥c≥12/13. In the second, R is positive and concave on [p,2 arctan(1/3)], so its minimum is at an endpoint. Its endpoint values are c+s and (31c+17s)/25; the latter exceeds c+s because 6c−8s>0. Thus R≥12/13 in that case as well. From (23),

    F_CB''≤2−329/975+100/2197−24/13
            =−22751/164775<0.                     (24)

This proves concavity on every interval cut by β=p,q. Only β=0,p,q,2 arctan(1/3) need checking. The zero and upper boundary endpoints are supplied by `C1092-CB-ENDPOINT-SCALARS.md`. At β=p use (20) or the descending CB endpoint theorem. At β=q the CB and CC sources coincide, so Section 5 supplies the sign. Each endpoint uses the larger g_j when its multiplier J₀ is nonnegative and the smaller one when J₀ is nonpositive; the companion proves both when needed. The other endpoint choice only increases F_CB. Hence F_CB≥0 throughout.

## 9. The BC source: curvature below q and comparison above q

For β≥q, (19) and the completed BB proof immediately give F_BC≥0. It remains to consider 0≤β≤q.

Put ε_p=sign(p−β), retaining A_*,C_* from (22). The linear part of F_BC is

    ell=dC_p A_*+dS_p(g_i+ε_p/2)−2C_q+bC_*.

Its quadratic part has second derivative −2Q, where

    Q=(d−t)cos(2β)+(d+t)sin(2β).

At β=0 the exact second derivative is

    F_BC''(0)=2t−d[c(1/2+T_*+e)+s(c+s)]
                  ≤−34/845,                        (25)

by `C1092-BC-CURVATURE-SCALAR.md`.

This second derivative decreases throughout 0≤β≤q, on each side of p when p is inside that interval. To see this, first

    Q'≥2(d−t)≥14/13.

The inequality follows because (d+t)cos(2β)−(d−t)sin(2β) decreases to d−t at β=q. If β≤p, then S_p≥0 and

    −ell'≤d(g_i+1/2)+2S_q≤17/13+10/13=27/13.

If p≤β≤q, which occurs only on an ascending edge, then

    −ell'≤|S_p|A_*+d(g_i−1/2)+2S_q
                ≤6/13+4/13+10/13=20/13.

Consequently

    F_BC'''=−ell'−2Q'≤−1/13<0

in the first region, and at most −8/13 in the second. The regular second derivatives from the two sides of β=p agree because S_p=0 there. Equation (25) therefore implies strict concavity on each interval cut by p inside [0,q].

Only β=0,q, and p when p≤q remain. The first and second are the BC endpoints already proved in `C1092-POSITIVE-ENDPOINT-SCALARS.md`. At β=p≤q, BC=CC and Section 5 applies. Thus F_BC≥0 below q as well. All four positive-boundary sources have now been proved.

## 10. Closing the actual cycle

Sections 3–9 prove (10) for every positive boundary angle and every central angle order. If an actual boundary angle is nonpositive, `C1092-NONPOSITIVE-BOUNDARY-POTENTIAL.md` proves the same strict inequality directly from the actual wall and the only surviving two central-supplied normals. Thus every edge of the actual four-central cycle satisfies

    L_(i+1)−L_i>f(x_i)−(x_(i+1)−x_i),
    x_i=tan(p_i/2).

Summing around the cycle cancels both differences and gives

    0>sum_i f(x_i).

But x_i>0 and c_i≥12/13>1/2, so

    f(x_i)=(1−c_i)(2c_i−1)/c_i>0.

This is a contradiction. It proves Theorem 1 on the full continuously derived all-positive entrance, including every actual normal-source tie and every possible weak tangency. ∎

## 11. Scope in the original simplification program

The earlier direct negative and mixed-sign chapters exclude every last-assignment cycle containing a nonpositive central canonical angle. The present theorem excludes the remaining all-positive sector. Together they give a direct continuous exclusion of the entire original last C1092 assignment from its actual ownership, wall and MPPM data. No terminal angle or center history is an extra premise of this composition.

This statement concerns the identified last assignment. Any application to a larger earlier ownership family must still supply that family's actual owner reduction; the theorem does not silently substitute one assignment's owners for another's.
