# C1092: a wider continuous mixed-sign exclusion

## 1. Statement

Let eight distinct open squares C₀,…,C₃,B₀,…,B₃ have common side a>1,
pairwise disjoint interiors, and closures in [0,4]². Use cyclic charts
R^(−i), where R(x,y)=(4−y,x). Write the actual central angles θᵢ and
boundary angles βᵢ using the normals

    u_t=(cos t,sin t),   v_t=(−sin t,cos t).

Assume |θᵢ|≤3/32 and |βᵢ|≤5/32, with angles measured in radians.
In every local chart assume the following genuine geometric conditions:

* Cᵢ strictly owns U=(1,87/50), T=(87/50,2), and excludes A=(1,1).
* Bᵢ strictly owns P=(2,1), L=(8/5,1).
* The central and boundary centers satisfy

      27/20≤Cₓ≤3/2≤Cᵧ,
      Bₓ≤9/5,  0≤Bₓ−Cₓ≤dᵢ≤1/4,
      0≤Cᵧ−Bᵧ≤3/2.

* The next central center J in the same chart satisfies

      0≤Jₓ−Cₓ≤11/10,   −eᵢ≤Jᵧ−Cᵧ≤0,
      0≤eᵢ≤1/2.

The nonnegative bounds dᵢ,eᵢ need only satisfy

    sum of the three largest dᵢ≤1/2,   Σeᵢ≤1/2.           (1)

**Theorem.** These conditions exclude every central sign pattern with
min θᵢ≤0≤max θᵢ. Thus any configuration satisfying them must have all
four central angles strictly of the same sign.

The theorem uses broad center inequalities and two aggregate gap bounds.
It does not require the old near-axis center rectangles. There is no
upper bound on the common side a.

The needed exclusions of D=(1,2) are consequences of the cyclic boundary
points: Bᵢ₋₁ owns R^(−1)(2,1)=(1,2) in sector i and is distinct from Cᵢ.

## 2. Exact elementary angular bounds

For two equal squares a separating side normal supplies projection at
least aH(t), where t is the difference of their canonical angles and

    H(t)=(1+cos t+|sin t|)/2.

For 0≤t≤r, the inequalities cos t≥1−t²/2 and sin t≥t−t³/6 give

    H(t)≥1+(t/2)(1−r/2−r²/6).

At r=1/4 the coefficient is 83/192>43/100; at r=3/16 it is
461/1024>9/20. Consequently

    H(t)≥1+(43/100)|t|   for |t|≤1/4,
    H(t)≥1+(9/20)|t|    for |t|≤3/16.                   (2)

The same first inequality applied to β shows

    cos β+|sin β|≥1+(86/100)|β|.

Also, for 0≤t≤3/32,

    cos t≥2039/2048,
    tan t≤(2048/2039)t<(101/100)t,
    tan t≤192/2039<1/10.                                (3)

These statements hold at zero; no division by an angle will be used.

## 3. The actual boundary square supplies a wall cost

Write

    Cᵢ=(3/2−Xᵢ,3/2+Yᵢ),

so Xᵢ,Yᵢ≥0. The displacement C−B has horizontal component in [−dᵢ,0]
and vertical component in [0,3/2]. A first normal from either square has
projection of absolute value at most

    1/4+(5/32)(3/2)=31/64<1.

A second normal directed upward has projection at least −5/128>−1.
Thus the only separating directions from B toward C are upward second
normals v_ψ, where ψ is either θᵢ or βᵢ.

Set Aᵢ=|βᵢ|+|θᵢ−βᵢ|. The angle bounds give
|θᵢ−βᵢ|≤1/4, and |ψ|≤Aᵢ. Actual wall containment and (2) give

    Bᵧ≥a/2+(43a/100)|βᵢ|,

while the actual pair supports give

    a+(43a/100)|θᵢ−βᵢ|
      ≤v_ψ·(C−B)≤Cᵧ−Bᵧ+dᵢ|ψ|.

Since dᵢ≤1/4<43/100, adding these inequalities and using
Aᵢ≥|θᵢ| proves

    Yᵢ≥3(a−1)/2+(43a/100−dᵢ)Aᵢ
       ≥(43/100−dᵢ)|θᵢ|.                              (4)

This estimate retains the actual boundary support and the actual wall.

## 4. Positive and nonpositive central angles have different costs

For θᵢ>0, comparisons with strict U,T force D beyond the upper second
face. Since |D−A|=1<a, A cannot be beyond the opposite second face.
U prevents its upper-face alternatives, so A is below the lower first
face. With c=cos θᵢ, s=sin θᵢ, this says

    cXᵢ−sYᵢ≤(c+s−a)/2.

Therefore

    Xᵢ−Yᵢ≤tan θᵢ/2−(sec θᵢ−1)/2−(1−tan θᵢ)Yᵢ.

Use (3), discard the nonpositive secant term, and apply (4). This gives

    Xᵢ−Yᵢ≤[101/200−(9/10)(43/100−dᵢ)]θᵢ
           =(59/500+(9/10)dᵢ)θᵢ.                       (5)

For θᵢ≤0 put t=−θᵢ, c=cos t, s=sin t, K=c+s. The forced lower first
face at D gives

    cXᵢ+sYᵢ≤(K−a)/2.                                  (6)

The local wall-strip proof of C1092-NEGATIVE-GEOMETRY.md §4 applies:
tan(t/2)<1/8; the center inequalities are identical; and |β|≤5/32
implies cos β≥49/50 and |sin β|≤19/100. It proves

    Yᵢ>(aK−1)/2≥(K−1)/2.

Combining this with (6) gives

    Xᵢ−Yᵢ≤−(K−1)²/(2c)≤0.                             (7)

In particular a nonpositive angle makes no positive contribution to the
upper bound. Formula (7) is only weakened here; its strict version is
unnecessary. At θ=0 the same forced-face conditions already contradict
Xᵢ≥0 and a>1, and the inequalities remain valid necessary conditions.

## 5. The cyclic support cost closes every mixed pattern

Suppose min θᵢ≤0≤max θᵢ, and put

    α=max θᵢ≥0,  m=max(−θᵢ)≥0,
    TV=Σ|θᵢ−θᵢ₊₁|.

There are at most three positive θᵢ. By (1), (5), and (7),

    Σ(Xᵢ−Yᵢ)
      ≤[3(59/500)+(9/10)(1/2)]α
      =(201/250)α.                                     (8)

For adjacent central squares, the absolute transverse projection is at
most (3/32)(11/10)+1/2=193/320<1. The backward first projection is
less than one because the forward projection is at least −3/64>−1.
Hence a forward first normal u_ψ of an endpoint supplies the separator.

If ψ≥0 and (x,y)=J−C, then u_ψ·(x,y)≤x, because x≥0 and y≤0.
If ψ<0, then u_ψ·(x,y)≤x+eᵢm. Thus the transport loss is charged only
to negative endpoint angles. Applying the second support bound in (2),

    Jₓ−Cₓ≥a+(9/20)|θᵢ−θᵢ₊₁|−eᵢm.

In cyclic charts Jᵢ=(5/2−Yᵢ₊₁,3/2−Xᵢ₊₁), so
Σ(Jₓ−Cₓ)=4+Σ(Xᵢ−Yᵢ). The two paths around a cycle from a minimum
angle to a maximum give TV≥2(α+m). Summing now gives

    Σ(Xᵢ−Yᵢ)≥4(a−1)+(9/20)TV−mΣeᵢ
              ≥4(a−1)+(9/10)α+(2/5)m.                  (9)

Comparing (8) and (9) yields

    0≥4(a−1)+(12/125)α+(2/5)m,

which is impossible. This proves the theorem, including every zero angle
and all tangencies of distinct square boundaries.

## 6. Exact application to positive maximal-angle ranges 1 and 2

Take the same actual central and boundary owner assignments as in
C1092-NEGATIVE-GEOMETRY.md. The preserved endpoints

    maxangle-mppm23-k1-1-segments-seed,
    maxangle-mppm23-k2-1-segments-seed

supply all their strict U,T,P,L memberships and foreign A,D ownerships.
The coarse center and adjacent displacement hypotheses above hold in
all four sectors. The exact useful dᵢ,eᵢ aggregates are:

| Range | d₀ | d₁ | d₂ | d₃ | Three-largest sum | Σeᵢ |
|---|---:|---:|---:|---:|---:|---:|
| 1 | .14528721 | .16065931 | .10649362 | .11193510 | .41788162 | .32457904 |
| 2 | .19501720 | .12189076 | .13587323 | .14685943 | .47774986 | .43830941 |

All decimals are exact rationals. Each sum is less than 1/2. The bounds
come from maxima of Bₓ−Cₓ and Cᵧ−Jᵧ over the retained exact center
polygons, using independent interval bounds to enlarge the possible
displacements. Thus correlations have not been assumed.

The actual maximal central angle has tan(α/2)≤3/64, so
|θᵢ|≤α≤3/32. All retained boundary half-angles have absolute value
at most 5/64, giving |βᵢ|≤5/32. Range 1 has α≥2 arctan(1/64)>0,
and range 2 has α≥2 arctan(2/64)>0.

The theorem therefore eliminates every mixed or zero sign configuration
in both ranges. Their remaining central angles are all strictly positive.
No claim is made here that this mixed-sign exclusion alone closes their
all-positive parts. Its input is the preserved incoming enclosure, whose
derivation from the last MPPM auxiliary assignment remains retained.

For ranges 3–6 the endpoint domains already have all central canonical
angles nonnegative; the all-positive cycle may handle zeros directly if
its own hypotheses permit them. The theorem above is the additional
mixed-sign argument specifically needed for ranges 1 and 2.
