# C1092: a nonpositive sector forces H in its positive successor

All terminating decimals denote exact rationals. Owned points are
strict in their actual open squares. Exclusions and actual separating
faces may have equality. The common side satisfies a>1, with no upper
bound or incoming angle-magnitude restriction.

## 1. Statement and the previously proved negative support

Use the original last C1092 assignment and the local charts
R^(−i), where R(x,y)=(4−y,x). Each local central C_i strictly owns

    M=(1.65,1.65), U₀=(1,1.74),
    L₀=(1,1.6),   T=(1.74,2).

**Theorem.** If C_i has nonpositive canonical angle, then the next
central C_(i+1) strictly owns its local point H=(1,1.5), regardless
of the sign of that next central angle. Consequently the next actual
boundary B_(i+1) strictly owns its local P=(2,1).

For a nonpositive successor this is already the two-central theorem
in [C1092-NEGATIVE-H-PROPAGATION.md](C1092-NEGATIVE-H-PROPAGATION.md).
We prove the assertion when the successor is positive.

Work in C_i's chart, and write C=C_i, J=R(C_(i+1) in its own chart).
The full mixed-sign result
[C1092-MIXED-NEGATIVE-DISK.md](C1092-MIXED-NEGATIVE-DISK.md)
proves that C's actual boundary owns P and C excludes D=(1,2),
even when the preceding boundary P is missing. Therefore the local
argument in Sections 3–4 of
[C1092-NEGATIVE-OWNED-POINTS.md](C1092-NEGATIVE-OWNED-POINTS.md)
applies to this actual C and its actual boundary. It gives the
following support facts, not merely the center-radius conclusion.

Write

    u=(c,−s), v=(s,c), c≥s≥0, c²+s²=1,
    q=s/(1+c),
    U<u·X<U+a, V<v·X<V+a.

Then

    0<q<13/50,       c>.87,       s<.49,
    U≥c−2s,         V+a≤2s+2.26c=:f,               (1)

and for the actual center (Cₓ,Cᵧ),

    Cₓ>X*,          Cᵧ>Y*,
    Y*=1+(c+s)/2,
    X*=[c−2s+1/2+sY*]/c.                           (2)

The zero-angle endpoint is already impossible by the original D
and U₀ faces. The simple numerical bounds in (1) follow from
q<13/50:

    c>2331/2669>.87,       s<1300/2669<.49.

The geometric source of (2) is actual wall clearance above the
strict segment [1.44,2]×{1} in C's own boundary square, combined
with the actual lower-u face at D. No condition on the boundary
angle or a center history is used.

## 2. The positive successor's missing-H faces

Write the next square in its own chart as C⁺, with positive frame

    u⁺=(d,t), v⁺=(−t,d), d≥t≥0, d²+t²=1.

The preceding actual boundary is C's boundary, whose P is already
strictly owned. Hence C⁺ excludes D=(1,2). It also excludes its
original foreign central points N=(1.65,2.35), E=(2,1.74).

Suppose for contradiction that H is outside C⁺. The positive H
face proof in Section 2 of
[C1092-MIXED-NEGATIVE-DISK.md](C1092-MIXED-NEGATIVE-DISK.md)
uses only H,N and the four strict local anchors, and gives

    U⁺≥d+1.5t.                                     (3)

For completeness, H is lower-u or lower-v. A lower-v exit would
give t/d<3/13 by M. Then N has its other three bands strict and
is upper-v, giving a≤.85d−.65t<1. Thus only (3) is possible.

The lower-u, upper-u and lower-v bands at D are strict by U₀,T,L₀,
respectively. Therefore

    V⁺+a≤2d−t.                                     (4)

At E the lower-u and upper-v bands are strict by U₀,T, so E is
upper-u or lower-v. A lower-v exit would give

    a≤(2d−t)−(1.74d−2t)=.26d+t
       ≤1.26/sqrt(2)<1,

contradicting (4). Consequently

    U⁺+a≤2d+1.74t.                                 (5)

Combining (3),(5) gives a≤d+.24t. With r=t/(1+d),

    d+.24t−1=2r(.24−r)/(1+r²),

so a>1 forces

    0<r<6/25,       t<.46,
    t/d<300/589<37/63.                              (6)

These successor angle bounds are consequences of the assumed
missing H and actual foreign points. They are not extra premises.

## 3. The physical successor and its actual normal sources

Reindex the physical frame of J=R(C⁺) as

    u_J=(d,t),       v_J=(−t,d),
    𝒰<u_J·X<𝒰+a,   𝒱<v_J·X<𝒱+a.

The missing-H floor (3) becomes

    𝒱≥d−2.5t.                                      (7)

The actual strict points in J include

    T_J=(2,1.74),       M_J=(2.35,1.65).

As before, strict M,M_J and strict T,T_J force every separating
normal from C toward J to have n_x>0 and n_x−n_y>0. Among the
actual face normals of the two squares only the following remain:

    u=(c,−s),       u_J=(d,t),       −v_J=(t,−d).     (8)

Put

    K=cd−st,       L=ct+sd.

The bounds (1),(6) make both ordinary angles strictly less than
π/4. Their sum is therefore less than π/2, so K>0. Also L>0 and
K²+L²=1. The exact projection relations are

    u=K u_J−L v_J,
    u_J=K u+L v,
    −v_J=L u−K v.

We now exclude the three sources separately, over their full
continuous angle domains.

## 4. Source u_J: the actual wall-clearance support

The center bound (2) and a>1 give

    upper_C(u_J)
       =dCₓ+tCᵧ+(a/2)(K+L)
       >dX*+tY*+(K+L)/2.

Set κ=(1−q)/(1+q). Direct substitution in the right side gives
the exact identity

    dX*+tY*+(K+L)/2
       =2(d+t)+(1−c)(dκ−t).                        (9)

Because q<13/50, κ>37/63. By (6), t/d<300/589<37/63, so
dκ−t>0. Thus

    upper_C(u_J)>2(d+t)>2d+1.74t=u_J·T_J.

The strict point T_J gives lower_J(u_J)<u_J·T_J, so separation
on u_J is impossible.

## 5. Source u: one exact norm inequality

The strict T_J gives 𝒰<2d+1.74t. Together with (7),

    lower_J(u)=K𝒰−L(𝒱+a)
       <K(2d+1.74t)−L(d−2.5t+a).

On the other hand upper_C(u)=U+a≥c−2s+a. Separation would
therefore require

    a(1+L)<K(2d+1.74t)−L(d−2.5t)−c+2s.           (10)

Subtract the right side from 1+L. The exact result is

    1−Ac−Bs,
    A=1−t+.5t²+.74dt,
    B=1−d+.5dt−.74t².                              (11)

In terms of r=t/(1+d), direct simplification yields

    1−A²−B²
      =2r[325−1647r+3425r²−1250r³]
         /[625(1+r²)²].                            (12)

For 0<r<6/25, the cubic bracket satisfies

    325−1647r+3425r²−1250r³
       ≥325−1647r+3125r²
       =3125(r−1647/6250)²+1349891/12500>0.

Thus A²+B²<1. By Cauchy–Schwarz, Ac+Bs<1, so the margin in
(11) is strictly positive. Equation (10) is impossible for a>1.

## 6. Source −v_J: a fixed rational margin

The exact support of C and (1) give

    upper_C(−v_J)=L(U+a)−KV
       ≥L(c−2s)−Kf+a(K+L).

Equation (7) gives lower_J(−v_J)=−(𝒱+a)≤−d+2.5t−a.
Therefore separation would imply

    a(1+K+L)≤−d+2.5t−L(c−2s)+K(2s+2.26c).        (13)

The difference between 1+K+L and the right side equals

    1−A₁d−B₁t,
    A₁=1.26−c−s+cs−.26s²,
    B₁=1.5−c+s−.26cs−s².                          (14)

By (1), c>.87 and s<.49. Hence

    A₁≤1.26−c<.39,
    B₁≤1.5−c+s<1.12.

Using d≤1 and t<.46 from (6),

    A₁d+B₁t<.39+1.12(.46)=2263/2500<1.

This contradicts (13). There is no possible actual separating
source in (8), contradicting disjointness. Therefore the positive
successor strictly owns H. ∎

## 7. The exact ownership consequence and remaining scope

Every point used above is supplied by the original last assignment
or by an already proved actual-owner transfer. In particular the
successor's D comes from its preceding actual boundary P, which is
forced because the predecessor central is nonpositive. The first
central's own D may have been furnished by the two-central exclusion
of [C1092-MIXED-NEGATIVE-DISK.md](C1092-MIXED-NEGATIVE-DISK.md);
the wall-clearance proof requires only that D be excluded.

Strict H in the successor central excludes H from its actual paired
corner. The all-angle corner-to-boundary Theorem 7 of
[C1092-DIRECT-WALL-POINT.md](C1092-DIRECT-WALL-POINT.md)
therefore gives strict P in that successor's actual boundary.

Combining the present theorem with the two predecessor-sign theorems
for a nonpositive recipient yields this precise cyclic restriction:

    a missing P can occur only at a strictly positive central
    whose preceding central is also strictly positive.

All nonpositive centers and all missing-P positive centers are
already inside the small disk. The current theorem does not assert
the disk conclusion for a positive central whose own P is owned,
and does not by itself complete the arbitrary-sign cycle.
