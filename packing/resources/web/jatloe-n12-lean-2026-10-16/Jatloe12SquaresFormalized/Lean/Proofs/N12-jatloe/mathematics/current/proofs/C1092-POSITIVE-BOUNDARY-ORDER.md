# C1092: a nonpositive boundary forces a strict rise in the central angle

All constants are exact rationals. Owned points are strict; exclusions and support separations may be tangent. This chapter uses the actual all-positive entrance already proved in `C1092-POSITIVE-QUADRANT-BOOTSTRAP.md`, together with actual P ownership. It proves a relation between consecutive actual angles, without any angular enumeration.

## 1. Retained actual geometry

Write C for the present central square, J for the next central square in the present chart, and B for the actual bottom boundary square. All have the common side a>1. Let p,q be the positive canonical angles of C,J and β the signed canonical angle of B. Put

    c=cos p, s=sin p, d=cos q, t=sin q,
    x=tan(p/2), y=tan(q/2), k=107/75, r=k−1=32/75.

The proved entrance gives

    0<x,y<1/5,
    C_x<1.5<C_y,
    J_x=4−(C_next)_y, J_y=(C_next)_x<1.5,
    −1/8<tan(β/2)<1/3.

The actual B lies above y=0 and strictly owns P=(2,1), its original marker (2,.914), and (1.74,1). The original actual central anchors supply strict T=(1.74,2) in C and E=(2,1.74),(2.26,1) in J.

The exact forced faces retained from the bootstrap and all-D theorem are

    V_C+a≤v_p·D,              D=(1,2),
    U_C+a≤u_p·E',             E'=(2,1.5),
    U_J≥u_q·P,
    U_J+a≤u_q·R'',            R''=(3,k).              (1)

Here U,V are lower face values in the displayed positive canonical frames. The third inequality is the rotated actual D exclusion; the last is the rotated lower-v face at the actual boundary point (k,1).

**Theorem 1.** Under these actual hypotheses, if β≤0, then

    q>p.                                               (2)

We first retain the exact source reductions needed to prove this assertion.

## 2. The actual B–J and C–J sources

**Lemma 2.** The actual B–J separator can be supplied only by u_B or u_q when β>0, and only by u_q when β≤0.

**Proof.** Orient the separator from B toward J. The two strict differences

    (2.26,1)−(1.74,1)=(.52,0),
    (2,1.74)−(2,.914)=(0,.826)

force n_x>0,n_y>0. If β>0, the only first-quadrant actual normals are u_B and u_q. If β=−γ≤0, put h=cos γ,b=sin γ. The only additional possible first-quadrant normal is v_B=(b,h). It already fails the strict cone when γ=0.

For γ>0 consider the actual lower-left vertex of J,

    Z=J−(a/2)(u_q+v_q).

Its y coordinate is less than one because J_y<1.5 and a(d+t)>1. The forced lower-u face at P in (1) says u_q·(Z−P)≥0, so Z_x>2 as well. Write J=(2.5−Y,1.5−X), with X,Y≥0. Directly,

    2v_B·(Z−P)
      =b[1−2Y−a(d−t)]+h[1−2X−a(d+t)]
      ≤(h+b)(1−d)−(h−b)t
       =t[(h+b)y−(h−b)]<0.                          (3)

Indeed γ<2 arctan(1/8) gives h+b≤79/65 and h−b≥47/65, while y<1/5. Thus the bracket is at most 79/325−47/65<0. Since Z lies in J's closure and P is strict in B, (3) forbids separation from B to J on v_B. This proves the lemma. ∎

**Lemma 3.** Adjacent central squares may be separated on the first normal corresponding to the smaller of p and q. In particular, if q≤p, then

    upper_C(u_q)≤lower_J(u_q).                        (4)

**Proof.** The strict points T,E allow only forward first normals and downward transverse normals, as in the adjacent-angle theorem. The downward source v_p fails because V_C≤v_pD−a<v_pE.

For v_q put κ=cos(p−q), τ=|sin(p−q)|. If q≤p, the two upper C caps in (1) imply

    lower_C(v_q)
      ≤v_qD+τ(c−.5s)−a(κ+τ)<v_qD−κ.

If q≥p, strict T and the D cap imply

    lower_C(v_q)<v_qD−κ

by the same expansion, now with the additional nonpositive term −.74cτ. In either order κ≥12/13, whereas

    v_q(D−E)=.26d+t≤.26+5/13<12/13.

Thus E prevents downward separation on v_q also.

Only the two forward first normals remain. Moreover the D cap and C_x≤1.5 give

    C_y≤1.5+(c+s−a)/(2c)<5/3.

Consequently J_x>7/3>C_x and J_y<1.5<C_y. The first-normal projection of J−C decreases with its positive angle. Its required support width, a(1+κ+τ)/2, is the same on either square's first normal. Therefore the smaller angle satisfies that support separation whenever either first normal does. This proves (4). ∎

## 3. The possible B–C sources when β≤0

Orient the separator from B toward C. The strict differences T−(1.74,1)=(0,1) and (1,1.6)−(2,.914)=(−1,.686) give n_y>0 and n_x<.686n_y. For β=−γ, its only candidates are v_p, v_B=(b,h), and −u_B=(−h,b).

The source −u_B is impossible for the whole present angle range by Section 4.2 of the quadrant bootstrap. In detail, with α=sin(p+γ), Δ=cos(p+γ), strict T and the D cap bound

    lower_C(−u_B)<−h+2b−.74cΔ−aα.

The actual boundary point (1.44,1) makes its own opposite support strictly greater than −1.44h+b. A separator would require

    h(.3+s−.74s²)+b(c−.74cs−1)<0,

which is impossible since b≤h and

    (c+s)(1−.74s)−.7>0

on c>.9,s<.42. Hence only v_p and v_B remain. At γ=0 these coincide; either of the following arguments includes that equality.

## 4. The central-supplied vertical source forces q>p

Suppose, for contradiction, that q≤p and B–C separates on v_p. By Lemma 2, B–J separates on u_q. Their actual support inequalities and (1) give

    upper_B(v_p)≤2c−s−a,
    upper_B(u_q)≤3d+kt−a.                             (5)

Write κ=cd+st, h=cos γ,b=sin γ. The real wall gives B_y≥a(h+b)/2. Also

    width_B(v_p)=a[cos(p+γ)+sin(p+γ)],
    width_B(u_q)=a[cos(q+γ)+sin(q+γ)].

Multiply the first inequality in (5) by d and the second by s. Their center-x terms cancel. Substitute the wall lower bound and then a>1. The exact necessary inequality becomes

    hA+bB+d+s<2cd+2sd+kst,
    A=dc+sd+st,    B=dc.                              (6)

The expression hA+bB increases with γ on 0≤γ≤2 arctan(1/8). Indeed

    A/B=1+tan p+tan p tan q≤229/144,
    b/h≤16/63,

so its derivative Bh−Ab is strictly positive. Thus its minimum is A at γ=0. Equation (6) would imply

    d(c+s−1)>s(1−rt).

Since c+s−1=s(1−x), this is

    x<r tan q−(sec q−1).                              (7)

The function on the right increases for 0≤q≤p₁:=2 arctan(1/5): its derivative is (r−sin q)/cos²q>0 because sin q≤5/13<32/75. For q≤p it is therefore at most

    r tan p−(sec p−1)
      =(2rx−2x²)/(1−x²)<x,

where the last sign follows from

    2r−1−2x+x²=−11/75−2x+x²<0.

This contradicts (7). The central-supplied vertical source cannot occur on a nonascending edge.

## 5. The boundary-supplied vertical source also forces q>p

Assume q≤p and B–C separates on v_B. Put

    α=sin(p+γ)=hs+bc>0,
    Δ=cos(p+γ)=hc−bs>0,
    κ=cos(p−q), τ=sin(p−q)≥0,
    D_q=cos(q+γ)=hd−bt>0.

Strict P in B and the actual separator give

    αU_C+ΔV_C>v_B(P)=2b+h.                            (8)

By Lemma 3 and the upper-u cap of J,

    κ(U_C+a)−τV_C≤3d+kt−a.                           (9)

Combine (8)–(9) with V_C≤2c−s−a. The identity κΔ+ατ=D_q gives the necessary strict inequality

    a[D_q+α(1+κ)]
      <α(3d+kt)−κ(2b+h)+D_q(2c−s).

Its coefficient of a is positive. Dropping a to one, expanding, and collecting h,b therefore requires

    h F_h+b F_b<0,                                    (10)

where

    F_h=d(cs−c−2s+1)+s+t(s²−rs),
    F_b=c+d(c²−c)+t(cs+(43/75)c+s−1).                (11)

We prove both coefficients positive on the entire triangle 0<y≤x<1/5.

First,

    F_b≥c−c(1−c)−t=c²−t≥79/169>0.                  (12)

Here d≤1, the bracket multiplying t is at least −1, c≥12/13 and t≤5/13.

For F_h, substitute the exact half-angle formulas. One obtains

    F_h/s=N(x,y)/[(1+x²)(1+y²)],                     (13)

where

    N(x,y)=(1+x²)(1+y²)
       −[1+3x²−x−x³](1−y²)
       −2y[(32/75)(1+x²)−2x].

A short continuous coefficient grouping proves its sign. Put δ=x−y≥0. The exact expansion is

    N(x,y)=y(1+y²)(11/75+4y−y²)
       +δ[1+(22/75)y²+8y³−3y⁴]
       +δ²[−2+(161/75)y+4y²−3y³]
       +δ³(1−y²).                                    (14)

On 0≤y≤x≤1/5, the coefficient of δ is at least one, that of δ² is at least −2, and that of δ³ is nonnegative. Therefore

    N(x,y)≥y(1+y²)(11/75+4y−y²)+δ(1−2δ)>0,

because x>0 and δ≤1/5. Equations (12)–(14) contradict (10). Thus the boundary-supplied vertical source also cannot occur when q≤p.

All actual separating sources have now been exhausted. A boundary with β≤0 necessarily has q>p, proving Theorem 1. All strictness comes from a>1 or the named strict owned points, so weak tangencies and equal central angles are included. ∎

## 6. Consequence for the remaining positive cycle

Every descending or equal-angle central edge has a strictly positive boundary angle. Nonpositive boundary angles can occur only on ascending edges. In particular, at a maximal central angle the following boundary is positive. This is a proved local angle-order restriction, not yet the required telescoping potential inequality on ascending edges.
