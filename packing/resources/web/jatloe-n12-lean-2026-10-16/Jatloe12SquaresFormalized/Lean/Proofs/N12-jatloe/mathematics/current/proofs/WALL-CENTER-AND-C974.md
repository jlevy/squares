# A direct wall-center theorem and its uniform C974 application

All decimal numbers here are exact rationals. Strict ownership means
interior membership in the actual square; an excluded point may be on a
face. No upper bound on the side length is used.

## 1. The wall-center theorem

**Theorem.** Let W be an open square of side a>1 with its closure in x≥0.
Suppose W strictly owns

    P=(.914,2),  Q=(1,2.4),

and excludes

    F=(1,1.74),  M=(1.65,2.35).

Then its center ordinate satisfies

    Y_W>51/25=2.04.

This conclusion is valid for every square orientation. In particular no
singleton-corner point such as (.76,1.87) is needed.

### Proof

Relabel the square's two face axes so that its first unit normal is
(l,h), with l>0, h≥0, l²+h²=1. Its second normal is (−h,l).
Such a choice covers every square orientation: a negative canonical
angle is handled by exchanging the two axes and reversing one normal.
An axis-aligned square uses l=1,h=0. Write the strict bands as

    U<lx+hy<U+a,   V<−hx+ly<V+a.

The leftmost closed vertex has abscissa lU−h(V+a), so the actual wall
imposes

    lU≥h(V+a).                                          (1)

The center ordinate is

    Y_W=hU+lV+(a/2)(l+h).                               (2)

Both upper bands of F follow strictly from Q. Its exclusion therefore
implies one of the two closed lower-face bounds

    U≥l+1.74h,   or   V≥−h+1.74l.                       (3)

Put K=l+h. Throughout this quadrant,

    K≥1+(4/5)lh,                                        (4)

because K−1=2lh/(K+1), K≤sqrt(2)<3/2. Also h²≤1 and lh≤1/2.

**First alternative in (3).** The lower first band of M follows from P:
its projection increment is .736l+.35h>0. Its upper second band follows
from Q, with difference −.65h−.05l<0. Finally its upper first band
follows from U≥l+1.74h and

    (1.65l+2.35h)−(l+1.74h)
       =.65l+.61h≤sqrt(.7946)<1<a.

Thus M must exit through the lower second face:

    V≥−1.65h+2.35l.

Substitution in (2), followed by a>1 and (4), yields

    Y_W≥2.35−.61h²−.65lh+(a/2)K
        >2.85−.61h²−.25lh
        ≥2.85−.61−.125=2.115>2.04.                     (5)

**Second alternative in (3).** Eliminate U by the actual wall (1).
Since l>0 and h²+l²=1,

    Y_W≥V/l+a h²/l+(a/2)K
        ≥1.74−h/l+a h²/l+(a/2)K
        >1.74+(h²−h)/l+K/2.

The identity (h²−h)/l=−lh/(1+h) and (4) give

    Y_W>2.24−[1/(1+h)−2/5]lh.                          (6)

For 0≤h≤1/4, the bracket is at most 3/5 and lh≤h≤1/4;
the right side in (6) is at least 2.24−.15=2.09.
For 1/4≤h<1, the bracket is at most 2/5 and lh≤1/2;
the right side is at least 2.24−.20=2.04.
Both alternatives in (3) therefore prove the theorem. The strict
inequality comes from a>1 with a positive coefficient, so every weak
exterior contact and the zero-sine endpoint are included. ∎

## 2. The third C974 wall-center comparison now follows directly

In the original C974 owner order, Q10 is the actual right wall square.
The fixed common auxiliary facts give its strict points

    (3.086,2), (3,2.4).

The southeast central square Q6 owns F8=(3,1.74), in every one of its
listed auxiliary alternatives. The northeast central square Q7 owns
the original marker (2.35,2.35). Both squares are distinct from Q10,
so Q10 excludes these two points.

Reflect the entire local configuration in x=2. Its points become
P=(.914,2), Q=(1,2.4), F=(1,1.74), M=(1.65,2.35), and the right
container wall becomes x=0. The theorem therefore gives

    Y_10>51/25>2.                                       (7)

No assumption about which square owns the missing southwest inner
corner, and no extra auxiliary choice, occurs in this argument. It is
uniform over both missing-corner alternatives and all 85 members of
the supplied C974 cover.

Together with Theorem 2 of OTHER-GEOMETRY.md, the following three
center comparisons are now direct continuous consequences of the
original C974 physical entrance:

    Y_8>423/200,   X_9>423/200,   Y_10>51/25.

These establish, with strict margins, three of the four center-sign
comparisons requested in Chapter 04. The top comparison X11≤2 and
the final contradiction within that center region remain separate
obligations; they are not claimed from the three inequalities above.

## 3. A useful partial top-wall application

If a C974 alternative gives Q11 strict ownership of (1.6,3) and
exclusion of (2.26,3), apply the same theorem under

    (x,y)↦(4−y,4−x).

Its marker (2,3.086) and strict point (1.6,3) become P,Q, and the
excluded point (2.26,3) becomes F. The remaining excluded point M
corresponds to the absent northwest original marker (1.65,2.35),
which is outside every square in C974. Thus this genuine additional
auxiliary condition gives

    4−X_11>51/25,   or   X_11<49/25<2.                  (8)

Among the supplied possible top labels, this condition includes 16392
and 16424. Labels that own (2.26,3), or lack (1.6,3), cannot be put
under this application. The exact exclusion is retained explicitly.
