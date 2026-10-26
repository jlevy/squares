# C1092: every genuinely mixed central-sign cycle is impossible

All decimals are exact rationals. Strict ownership refers throughout
to the actual open squares, and all exclusions and separating faces
allow equality. The common side satisfies a>1. There is no assumed
angle-magnitude bound, boundary-angle bound, center enclosure, or
upper bound on a.

## 1. Statement and already proved actual support inputs

Use the original last C1092 auxiliary assignment, the actual owners
C_i=Q_(4+i), and the four local charts R^(−i), where

    R(x,y)=(4−y,x),
    (B_0,B_1,B_2,B_3)=(Q_9,Q_10,Q_11,Q_8).

Every local central strictly owns

    M=(1.65,1.65), U₀=(1,1.74),
    L₀=(1,1.6),   T=(1.74,2).

The original paired corner strictly owns A=(1,1); the actual bottom
boundary owns (1.6,1), and the next actual central owns E=(2,1.74).
The universal wall extension puts L'=(1.44,1) strictly in each
actual boundary. Write P=(2,1), D=(1,2), H=(1,1.5).

**Main theorem.** A configuration in this original last assignment
cannot have both a strictly positive and a nonpositive canonical
central angle.

The following previously proved conclusions hold in arbitrary sign
cycles and are used with their exact stated dependencies:

1. Every nonpositive sector owns H and has its actual boundary own
   P, by the two predecessor-sign H theorems.
2. Every nonpositive sector excludes D, even if its preceding P is
   missing, by
   [C1092-MIXED-NEGATIVE-DISK.md](C1092-MIXED-NEGATIVE-DISK.md).
3. A nonpositive predecessor forces H, and consequently the actual
   boundary P, in a positive successor, by
   [C1092-NEGATIVE-TO-POSITIVE-H.md](C1092-NEGATIVE-TO-POSITIVE-H.md).

In particular a nonpositive C, in its negative canonical frame

    u=(c,−s), v=(s,c), c≥s≥0, c²+s²=1,
    q=s/(1+c),

has the actual support conclusions from Sections 3–4 of
[C1092-NEGATIVE-OWNED-POINTS.md](C1092-NEGATIVE-OWNED-POINTS.md):

    0<q<13/50,        c>.87,        s<.49,
    U≥c−2s,          V+a≤2s+2.26c=:f,               (1)

and its actual center satisfies

    Cₓ>X*,           Cᵧ>Y*,
    Y*=1+(c+s)/2,
    X*=[c−2s+1/2+sY*]/c.                            (2)

The zero-angle endpoint is already impossible in that local argument.
The derived q bound gives c>2331/2669>.87 and s<1300/2669<.49.
The geometric input to (2) is the actual boundary's strict segment
[1.44,2]×{1}, the container wall, and the lower-u face at D.

We prove two short edge lemmas before composing the cycle.

## 2. A negative predecessor forbids a bounded positive successor

**Lemma 1.** Let C be a nonpositive central with the actual support
facts (1),(2), and suppose its next actual central C⁺ is positive,
excludes its local D and A, and has positive half-angle

    0<r≤7/32.                                       (3)

Then the two actual central squares cannot be disjoint.

The actual L' exclusion at C⁺ and its four original strict anchors
are also understood as part of the original owner hypotheses. No H
ownership or H exclusion in C⁺ is assumed in this lemma.

### 2.1. The positive faces and physical frame

Write the local positive frame of C⁺ as

    u⁺=(d,t), v⁺=(−t,d),
    d≥t>0, d²+t²=1, r=t/(1+d).

The D exclusion is upper-v: its lower-u, upper-u and lower-v bands
are strict by U₀,T,L₀. At A both upper bands are strict by M,L₀.
If A were lower-v, its face and the D cap would give a≤d≤1.
Thus A must be lower-u:

    U⁺≥d+t.                                        (4)

The bound (3) gives

    d≥975/1073,       t≤448/1073<.42,
    t/d≤448/975<11/15.                              (5)

At L'=(1.44,1), the lower-u, upper-u and upper-v bands are strict,
using respectively L₀,M,L₀:

    u⁺(L')−u⁺(L₀)=.44d−.6t>0,
    u⁺(M)−u⁺(L')=.21d+.65t>0,
    v⁺(L₀)−v⁺(L')=.6d+.44t>0.

Hence the actual L' exclusion is lower-v:

    V⁺≥d−1.44t.                                    (6)

In C's chart the next square is J=R(C⁺). Reindex its physical
frame as u_J=(d,t), v_J=(−t,d), with lower bands 𝒰,𝒱. Equations
(4),(6) become

    𝒱≥d−3t,       𝒰+a≤3d+1.44t.                   (7)

Its strict points include T_J=(2,1.74) and M_J=(2.35,1.65).
Strict M,M_J and T,T_J force any separating normal from C to J
to have n_x>0 and n_x−n_y>0. Only three actual sources remain:

    u=(c,−s),       u_J=(d,t),       −v_J=(t,−d).     (8)

Put K=cd−st>0 and L=ct+sd>0. Both ordinary angle magnitudes are
strictly below π/4, so K>0, and K²+L²=1. The projection relations
are

    u=K u_J−L v_J,
    u_J=K u+L v,
    −v_J=L u−K v.

### 2.2. Source u_J

From (2) and a>1,

    upper_C(u_J)
      =dCₓ+tCᵧ+(a/2)(K+L)
      >dX*+tY*+(K+L)/2.

Set κ=(1−q)/(1+q). The exact identity already used in the
negative-to-positive H theorem is

    dX*+tY*+(K+L)/2
      =2(d+t)+(1−c)(dκ−t).                         (9)

Here κ>37/63 and t/d≤448/975<37/63. Therefore

    upper_C(u_J)>2(d+t)>u_J·T_J.

Since T_J is strict in J, this rules out separation on u_J.

### 2.3. Source u

From (7),

    lower_J(u)=K𝒰−L(𝒱+a)
      ≤K(3d+1.44t−a)−L(d−3t+a).

The first inequality in (1) gives upper_C(u)≥c−2s+a. Thus
separation would imply

    a(1+K+L)
      ≤K(3d+1.44t)−L(d−3t)−c+2s.                 (10)

Subtract the right side of (10) from 1+K+L. The exact result is

    1−Ac−Bs,
    A=2−d−t+.44dt,
    B=1−d+t−.44t².                                 (11)

In the positive half-angle r,

    1−A²−B²
      =−4r[1875r³−1450r²+1446r−350]
         /[625(1+r²)²].                            (12)

For 0<r≤7/32, the bracket is bounded above by

    1875(7/32)³+1446(7/32)−350
      =−460747/32768<0.

Hence A²+B²<1, so Ac+Bs<1 by Cauchy–Schwarz. The margin in
(11) is positive, contradicting (10) and a>1.

### 2.4. Source −v_J

The C supports in (1) give

    upper_C(−v_J)=L(U+a)−KV
      ≥L(c−2s)−Kf+a(K+L).

Equation (7) gives lower_J(−v_J)≤−d+3t−a. Separation would
therefore imply

    a(1+K+L)≤−d+3t−L(c−2s)+K(2s+2.26c).           (13)

The margin between 1+K+L and its right side is

    1−A₁d−B₁t,
    A₁=1.26−c−s+cs−.26s²,
    B₁=2−c+s−.26cs−s².                            (14)

The bounds c>.87,s<.49 in (1) yield A₁≤1.26−c<.39. Also

    B₁=1+s(1−.26c)−cs²/(1+c)
       ≤1+.78s<1.4.

Using (5),

    A₁d+B₁t<.39+1.4(.42)=489/500<1.

This excludes (13). All three actual sources in (8) are impossible,
proving Lemma 1. ∎

## 3. A positive square followed by a negative square is bounded

**Lemma 2.** In the original setting, suppose a positive central C
excludes D and is followed by a nonpositive central. Then

    tan(p/2)<7/32,                                  (15)

where p is C's positive ordinary angle.

Write u_C=(c,s),v_C=(−s,c), c≥s>0. Its D exclusion forces

    V_C+a≤2c−s.                                    (16)

Let the next negative central, rotated into the present chart, be
J with frame u_J=(d,−t),v_J=(t,d). The already proved negative
local support facts apply to that actual square. In particular,

    d>.87, t<.49,
    𝒰+a≤3d−1.44t,       𝒱+a≤2d+2.26t.             (17)

The first cap is the rotation of its genuine local lower-v face
at L'; the second is the rotation of its genuine upper-u face at
E=(2,1.74). J strictly owns E=(2,1.74) in the present chart,
the image of its local T. C strictly owns T=(1.74,2).

Suppose p≥p₀=2 arctan(7/32). Then

    c₀=975/1073, s₀=448/1073,
    s≥s₀>13/37,       s/c≥448/975>.45.             (18)

Strict M,M_J and T,E leave only the actual normal sources
u_C,−v_C,u_J from C toward J. Put K=cd−st>0,L=ct+sd>0.
The negative successor has ordinary angle magnitude below π/4,
so p+|angle(J)|<π/2 and K>0.

### 3.1. The transverse source −v_C

By (16), upper_C(−v_C)≥a−2c+s. Strict E in J gives
lower_J(−v_C)<2s−1.74c. The difference is at least

    a−.26c−s>0,

because .26c+s≤1.26/sqrt(2)<1<a. This source is impossible.

### 3.2. The source u_C

Here u_C=K u_J+L v_J. Using both caps (17), and the strict
point T in C, separation would require

    a(K+L)
      <K(3d−1.44t)+L(2d+2.26t)−(1.74c+2s).       (19)

The difference between K+L and the right side is exactly

    cA₂+sB₂,
    A₂=d+t−1.26+.74t²−.56dt,
    B₂=d−t+.74dt+.56t².                            (20)

Since d≥1−t² and d≤1,

    A₂≥−.26+.44t−.26t²≥−.26.

Also (17) gives

    B₂≥d−t(1−.74d)
       >.87−.49[1−.74(.87)]>.69.

Consequently, by (18),

    cA₂+sB₂>−.26c+.69s
       >c[−.26+.69(.45)]>0.

This contradicts (19) and a>1.

### 3.3. The source u_J

The relation u_J=K u_C−L v_C, strict T, and (16) give

    upper_C(u_J)
      >u_J·T+L(a−.74s).

The first cap in (17) gives lower_J(u_J)≤3d−1.44t−a.
Separation would therefore require

    a(1+L)<1.26d+.56t+.74sL.                       (21)

Subtract the right side from 1+L. This equals

    1−A₃d−B₃t,
    A₃=1.26−s+.74s²,
    B₃=.56−c+.74cs.                               (22)

On the interval (18), 0<A₃<1, since

    A₃−1=.74(s−1)(s−13/37)<0.

If B₃≤0, then A₃d+B₃t≤A₃<1 immediately. Suppose B₃>0.
The function

    B₃(s)=.56−sqrt(1−s²)(1−.74s)

is strictly increasing, because its derivative is
s(1−.74s)/sqrt(1−s²)+.74sqrt(1−s²)>0. At s=.45, its
value is negative: sqrt(1−.45²)>.89 and .89(.667)>.56.
Hence B₃>0 implies s>.45.

The function A₃ is convex, so its maximum on [.45,1/sqrt(2)]
is at an endpoint. Those endpoint values satisfy

    A₃(.45)=.95985<.96,
    A₃(1/sqrt(2))=1.63−1/sqrt(2)<.93<.96.

Also, by monotonicity,

    B₃≤.93−1/sqrt(2)<.23.

Therefore A₃²+B₃²<.96²+.23²=.9745<1. Cauchy–Schwarz gives
A₃d+B₃t<1, contradicting (21). All actual normal sources have
been excluded under (18), proving Lemma 2. ∎

## 4. Composition at the first positive sector

Assume a genuinely mixed sign cycle exists. Choose an edge from a
nonpositive central C_i to a strictly positive central C_(i+1).
Such an edge exists in every cyclic list containing both signs.

The nonpositive-sector theorems give strict P_i in the actual B_i,
and the mixed negative disk theorem gives D_i excluded from C_i.
Thus C_i has all the actual support facts (1),(2).

The negative-to-positive H theorem gives strict H_(i+1) in the
positive successor and strict P_(i+1) in its actual B_(i+1).
In particular:

    C_(i+1) excludes D_(i+1), supplied by actual B_i;
    C_(i+2) excludes D_(i+2), supplied by actual B_(i+1).

There are two possibilities for C_(i+2).

* If it is positive, apply the proved adjacent-positive angle
  theorem in
  [C1092-POSITIVE-ADJACENT-ANGLE.md](C1092-POSITIVE-ADJACENT-ANGLE.md)
  to C_(i+1),C_(i+2). Its first pair of caps uses P_i; its second
  pair uses P_(i+1). Both points have just been supplied by their
  actual boundary owners. It does not require P_(i+2). The result
  is positive half-angle less than 7/32 at C_(i+1).
* If it is nonpositive, its actual negative support faces are
  already available in every mixed cycle. Lemma 2, applied to
  C_(i+1),C_(i+2), gives the same strict bound at C_(i+1).

Thus in either case C_(i+1) has positive half-angle below 7/32.
Lemma 1 now contradicts separation from its nonpositive predecessor
C_i. This proves the main theorem. ∎

Together with the already proved full all-nonpositive theorem, this
removes every sign pattern of the original last C1092 assignment
that contains a nonpositive central angle. Any remaining configuration
would have all four central canonical angles strictly positive. The
present proof does not claim completion of that all-positive sector.
