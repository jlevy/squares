# The wide wall also supplies the second inward crosspoint

All terminating decimals are exact rationals. Owned points are strict, exclusions and actual supports may be tangent, and the common side satisfies 1<a≤1.001.

**Theorem.** Let C,W be disjoint open squares. Suppose C strictly owns

    O=(0,0), M=(.35,.35), P=(0,.26), Q=(.26,0),

and excludes N=(−.35,.35), D=(.35,−.35). Suppose the actual W strictly owns

    S=(1.086,0), T=(1,−.39), B=(1,.4),

excludes E=(1,−.4), has its closure in x≤2, and has center ordinate Y_W≤0. Then C strictly owns Y=(0,.5).

The center O is an explicit strict premise. The conclusion does not follow by replacing W with its three-point hull.

## 1. The canonical faces and a strict crossing point

The nonnegative canonical case of C is immediate from the face proof in Section 2 of `C1092-MMMP-CENTER-CROSSPOINTS.md`. For completeness, write u=(c,s),v=(−s,c), c≥s≥0. Excluded D has its lower u-band from O, upper u-band from M and upper v-band from O. Thus the lower transverse face satisfies V≥−.35(c+s). The target Y has its lower u-band from O, upper u-band from M, and lower v-band from P. The upper transverse projection gap is at most .85c+.35s≤sqrt(.845)<1<a. Therefore every band of Y is strict.

For the remaining case give C the negative frame u=(c,−s),v=(s,c). Strict O and the two excluded markers give

    −.35(c+s)≤U<0, −.35(c−s)≤V<0.                    (1)

Indeed N is lower u by comparison with O,M. An upper-u D would then give the width .7(c+s)<1, so D is lower v. For Y the upper u-band follows from M, the lower v-band from P, and the upper v-band from .85c−.35s≤.85<1<a. A missing Y would therefore require

    U≥−.5s.                                        (2)

At s=0 this contradicts U<0. Assume s>0 and put z=s/(1+c), rho=.5−z. The point R=(1,rho) is strict in C: its two lower projections are positive, its upper u-band follows from (2) and u(R)=1−.5s, and its upper v-band follows from (1) and

    v(R)−V≤z+.85c−.35s<1,
    1−z−.85c+.35s=Delta(z)/(1+z²),
    Delta(z)=.15−.30z+1.85z²−z³
            ≥(27/20)(z−1/9)²+2/15>0.                (3)

Here 0<z≤sqrt(2)−1<1/2. These are the exact whole-interval identities of the cited crosspoint proof.

Convexity puts the whole segment {1}×[−.39,.4] strictly in the one actual W. If z≥.1, then 0<rho≤.4 and R lies on this segment, a contradiction. We are left with

    0<z<.1, c>.98, s<.2, rho>.4.                    (4)

The rational formulas c=(1−z²)/(1+z²), s=2z/(1+z²) give these strict bounds directly.

## 2. Both actual separating normals are impossible

Theorem 1 of `MIXED-WALL-HALFANGLE-CROSSING.md` applies to this actual W; its excluded M is strict in C. Thus W has negative canonical frame w=(d,−t), w_perp=(t,d), with

    d>t>0, d+t>5/4, t>9/32>7/25,
    L<d−.4t, dL+tH≤2−a(d+t).                       (5)

The last two facts are strict ownership of B and the genuine right wall.

Orient a separator from C toward W. Strict Q,S give n_x>0 and strict R,B give n_y<0. Consequently the only actual normal sources are u and w. Set alpha=cd+st and k=ct−sd. By (4)–(5),

    k/t=c−sd/t>.98−.2/.28=93/350>13/50.             (6)

For u the same exact elimination as (12) of the crossing chapter gives

    lower_W(u)<(s/t)(d−.4t)+(k/t)[2−a(d+t)].

Meanwhile upper_C(u)=U+a≥a−.5s. Their support difference is therefore strictly greater than

    1−c−.1s+(k/t)(d+t−1)
       >−1/50+(13/50)(1/4)
       =9/200>0.                                   (7)

The coefficient of a before replacing a by 1 is positive. Thus u cannot separate.

For w, its transverse C-frame coefficient is −k<0. Since V<0 and U+a≥a−.5s,

    upper_C(w)>alpha(1−.5s).

Subtract lower_W(w)=L<d−.4t. The resulting difference is greater than

    d[c(1−.5s)−1]+t[s(1−.5s)+.4].                 (8)

The identity 1−c=sz and (4) imply

    c(1−.5s)−1=−s(z+.5c)>−.6s,
    s(1−.5s)>.9s.

Using d≤1 and t>.28, (8) is strictly greater than

    −.6s+.4t+.9st>.112−.348s
       >.112−.348(.2)=53/1250>0.                   (9)

Thus w cannot separate either. All actual separating-axis sources in the strict cone are impossible, contradicting disjoint interiors. Missing Y is therefore impossible. This proves the all-angle theorem, with every equality allowed in the original exclusions and container walls. ∎
