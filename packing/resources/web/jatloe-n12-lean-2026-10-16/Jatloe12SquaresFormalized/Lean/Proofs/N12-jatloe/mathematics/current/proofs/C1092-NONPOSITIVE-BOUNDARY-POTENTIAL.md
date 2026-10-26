# C1092: the exact potential on every nonpositive-boundary edge

All constants are exact. This chapter retains the actual all-positive last assignment, the complete entrance in `C1092-POSITIVE-QUADRANT-BOOTSTRAP.md`, and the resulting strict ownership of every P=(2,1). All squares have a common side a>1. The central half-angles lie in (0,1/5), and a nonpositive boundary half-angle lies in (−1/8,0]. No angle sampling or finite subdivision is used.

For consecutive actual central angles p,q, write

    x=tan(p/2), y=tan(q/2),
    c=cos p, s=sin p, d=cos q, t=sin q,
    κ=cos(q−p)=cd+st, σ=sin(q−p)=ct−sd,
    H_p=c+s, H_q=d+t, H_delta=(1+κ+σ)/2.

In each central square's own sector chart, define the actual center projections

    G_i=u_p·((2,2)−C_i), L_i=v_p·((2,2)−C_i),
    G_j=u_q·((2,2)−C_j), L_j=v_q·((2,2)−C_j).

The corner's forced lower-u face gives G_i≤H_p−a/2 and G_j≤H_q−a/2. The stronger lower bounds from the new E' are not needed in this chapter.

**Theorem 1.** If the intervening actual boundary has canonical angle β≤0, then

    L_j−L_i>f(x)−(y−x),
    f(x)=(1−c)(2c−1)/c.                               (1)

In particular the same weak inequality may be used in a closed-cycle sum. The function f is strictly positive for every actual x>0.

## 1. Only the two central-supplied normals survive

The audited boundary-order theorem gives q>p, so 0<x<y<1/5. Its B–J source lemma gives only the actual first normal u_q for that pair. We show that, more strongly than required in that chapter, the boundary cannot supply its own vertical normal for B–C either.

Write β=−γ, h=cos γ,b=sin γ. Thus h≥b≥0 and γ<2 arctan(1/8). The B–C cone and the earlier exclusion of −u_B leave only v_p and v_B=(b,h). Suppose v_B separates from B toward C. Let

    α=sin(p+γ)=hs+bc>0,
    Δ=cos(p+γ)=hc−bs>0.

The actual upper faces at E'=(2,1.5) and D=(1,2) give

    lower_C(v_B)=αU_C+ΔV_C
      ≤α(2c+1.5s−a)+Δ(2c−s−a).

But the actual P=(2,1) is strict in B, so upper_B(v_B)>2b+h. Dropping a to one in the necessary separation inequality requires

    hF+bG>0,
    F=(1−c)(1−s)−.5s²,
    G=−c+s−s²−.5cs.                                  (2)

Both coefficients are strictly negative. Indeed

    F=s²(1−c−2s)/[2(1+c)]<0

because (1−c)/s=tan(p/2)<1/5<2, while G<−c+s<0. This contradicts (2). The equality γ=0 is included; its strict sign still follows from p>0.

Consequently B–C separates on v_p and B–J on u_q. These are the actual source directions. There is no negative horizontal multiplier to estimate.

## 2. An exact wall combination without angular transport

For any angle z set H(z)=(1+cos z+|sin z|)/2. The actual two support inequalities are

    v_p·(C−B)≥aH(p+γ),
    u_q·(J−B)≥aH(q+γ),                                (3)

where J is the next actual central center in the present chart. Multiply the first inequality by d and the second by s. Since d v_p+s u_q=(0,κ), the boundary x coordinate cancels exactly. The genuine wall gives B_y≥a(h+b)/2. Thus

    d v_p·C+s u_q·J≥a F(p,q,γ),
    F=dH(p+γ)+sH(q+γ)+κ(h+b)/2.                       (4)

The angles p+γ and q+γ are below π/4, so their sines and cosines are positive. Expanding (4) gives the particularly simple identity

    F=(d+s)/2+hA+bB,
    A=dc+sd+st,    B=dc.                              (5)

It follows that F increases with γ on the entire negative-boundary range: indeed

    A/B=1+tan p+tan p tan q≤229/144,
    b/h≤16/63,

so the derivative Bh−Ab is positive. Therefore

    F(p,q,γ)≥F₀:=(d+s)/2+dc+sd+st.                  (6)

The actual quarter-turn relation yields

    d v_p·C+s u_q·J=2κ−dL_i+sL_j.                   (7)

Because p<q, the audited smaller-angle central separation gives

    G_i+κL_j+σG_j≥aH_delta.                          (8)

Set

    λ=(d−s)/κ>0.

Add λ times (8) to (4), and use (7). The coefficients of L_j and −L_i are both d. Apply the actual upper bounds G_i≤H_p−a/2 and G_j≤H_q−a/2; all their multipliers are nonnegative. After (6) and dropping the positive coefficient of a−1, one obtains strictly

    L_j−L_i>B₀(x,y),                                 (9)

where

    B₀=[F₀+λH_delta−2κ
          −λ(H_p−1/2)−λσ(H_q−1/2)]/d.              (10)

For clarity, the coefficient of a before this last drop is

    [F+λH_delta+λ(1+σ)/2]/d>0.

No comparison angle, support transport error, or independent support enclosure has entered (9).

## 3. One scalar inequality on the whole ascending triangle

**Lemma 2.** For every 0≤x≤y≤1/5, expression (10) satisfies

    B₀(x,y)≥f(x)−(y−x).                              (11)

Every denominator in (10) is positive: d≥12/13, κ≥12/13, and d−s≥7/13. Substitute

    c=(1−x²)/(1+x²), s=2x/(1+x²),
    d=(1−y²)/(1+y²), t=2y/(1+y²).

Put δ=y−x. The following exact rational identity results:

    B₀−f(x)+(y−x)=N(x,y)/D(x,y),                     (12)

with positive denominator

    D=(1−x²)(1+x²)(1−y²)(1+y²)(1+x−y+xy)>0.

The numerator is conveniently given as the following seven coefficients of δ:

    N(x,x+δ)=C₀+C₁δ+C₂δ²+C₃δ³+C₄δ⁴+C₅δ⁵+C₆δ⁶,

where

    C₀=2x²(1−x)³(1+x)(1+x²)²,

    C₁=1−8x+11x²+6x³−28x⁴+2x⁵−12x⁶
          −22x⁷+27x⁸−10x⁹+x¹⁰,

    C₂=−5+21x−12x²−20x³+18x⁴−58x⁵−44x⁶
          +68x⁷−21x⁸+5x⁹,

    C₃=8−16x−2x²+24x³−74x⁴−40x⁵+82x⁶
          −24x⁷+10x⁸,

    C₄=−4+12x²−42x³−16x⁴+48x⁵−16x⁶+10x⁷,

    C₅=(x−1)(5x⁵−x⁴+10x³+8x²−3x+1),

    C₆=(x−1)²(x+1)(1+x²).

These equalities can be verified by substitution and multiplication by D; they do not require an inequality certificate or angle sampling.

On 0≤x≤1/5 the coefficient bounds

    C₀≥(128/125)x²,
    C₁≥1−8x+11x²,
    C₂≥−5+17x,
    C₃≥8−18x,
    C₄≥−4, C₅≥−1, C₆≥0                            (13)

follow directly by grouping the displayed coefficients. Here are explicit checks for the nontrivial groups.

For C₁, discard its remaining positive terms after x³ and bound

    C₁−(1−8x+11x²)
      ≥x³[6−28x−12x³−22x⁴−10x⁶]≥0.

The bracket decreases and is positive at x=1/5. For C₂ and C₃ respectively,

    C₂−(−5+17x)
      ≥x[4−12x−20x²−58x⁴−44x⁵−21x⁷]≥0,

    C₃−(8−18x)
      ≥x[2−2x−74x³−40x⁴−24x⁶]≥0.

Again each bracket decreases and remains positive at 1/5. Similarly

    C₄+4≥x²[12−42x−16x²−16x⁴]≥0.

Finally, if P₅=5x⁵−x⁴+10x³+8x²−3x+1, then

    P₅≥1−3x−x⁴>0,
    P₅−1≤x[5x⁴+10x²+8x−3]≤0.

Thus 0<P₅≤1 and C₅=(x−1)P₅≥−1. The C₀ and C₆ bounds are immediate.

Because 0≤δ≤1/5,

    −4δ⁴−δ⁵≥−(21/25)δ³.

Consequently (13) implies

    N(x,y)≥Q(x,δ),                                   (14)

where the single polynomial lower bound is

    Q=(128/125)x²+δ(1−8x+11x²)
         +δ²(−5+17x)+δ³(179/25−18x).

To see its sign on the whole triangle without subdivision, put

    u=5x, v=5δ, w=1−u−v.

All three are nonnegative because x+δ=y≤1/5. The following compact homogeneous identity is exact when u+v+w=1:

    3125Q
      =128u²(u+w)²
       +v[156u³+406u²w+875uw²+625w³]
       +v²[78u²+925uw+1250w²]
       +v³[139u+804w]
       +179v⁴.                                       (15)

Every term is nonnegative. In fact Q>0 unless x=δ=0: if v>0 its final term is positive, and if v=0,u>0 its first term is positive. Equations (12)–(15) prove (11), strictly away from the origin. The closed endpoints and equal-angle line have all been included. ∎

Combining Lemma 2 with (9) proves Theorem 1. This supplies the precise nonpositive-boundary edge inequality needed to match the direct positive-boundary potential. ∎

## 4. How the result joins the cycle

The audited boundary-order theorem ensures every nonpositive boundary occurs on an ascending central edge. This chapter proves the same uniform bound (1) which the direct positive-boundary theorem seeks on its other edges. Once that counterpart is supplied, the increments y−x telescope exactly around the four actual sectors:

    0=sum_i(L_(i+1)−L_i)
      ≥sum_i f(x_i)−sum_i(x_(i+1)−x_i)
       =sum_i f(x_i)>0.

The present chapter proves the entire nonpositive-boundary contribution. It does not claim the complementary positive-boundary theorem before that theorem has been independently established.
