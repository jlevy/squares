# The positive wall remainders on a wider continuous domain

## Scope

This proves the twelve wall remainder inequalities in the appendix to
`01-C1092-CYCLIC-INEQUALITIES.md` on the larger domain

    0 <= tan(alpha/2) <= 1/8,
    |tan(beta/2)| <= 1/8.

It replaces the twelve small-rectangle polynomial verifications by three
angle regions and a few factor identities. In particular, the entire
positive central target `tan(alpha/2)<=7/64` is included. The identities
are algebraic facts about the remainders; their use for actual squares
still requires the actual separator directions, coefficient signs, and
normal-transport bounds stated in the original geometric framework.

Every endpoint, including `alpha=0`, `beta=0`, and `beta=alpha`, is included.

## 1. Notation and denominators

Put

    x=tan(alpha/2),  y=tan(beta/2),
    A=1+x^2,  B=1+y^2,
    M=(1+xy)^2-(x-y)^2
     =(1+xy-x+y)(1+xy+x-y).

The hypotheses are `0<=x<=1/8` and `|y|<=1/8`. In this domain `A,B>0`,
`1+xy>0`, and `M>0`: indeed `1+xy>=63/64` whereas `|x-y|<=1/4`.
In trigonometric notation, `M/(AB)=cos(alpha-beta)>0`.

Let `f_CC,f_BC,f_CB,f_BB` be exactly the four sign-dependent remainder
formulas given in the handoff's appendix. Thus there are three formulas
for each label according to `beta<0`, `0<=beta<=alpha`, and `beta>=alpha`.

**Theorem.** Every one of those remainders is nonnegative on its entire
stated portion of the domain.

All identities below follow by substituting
`cos alpha=(1-x^2)/A`, `sin alpha=2x/A`, and the corresponding formulas
for beta. They can also be checked by multiplying by their displayed
positive denominator and collecting terms.

## 2. The region `0<=y<=x`

First,

    f_CC = 2(x-y)[x(1-x)^2+y(1+x)^2]/(A^2 B) >=0.       (1)

The other three remainders dominate this one. Their exact differences are

    f_BC-f_CC = 4(1-x^2)(x-y)^3(1+xy)/(A^2 B M),        (2)

    f_CB-f_CC = 4x(x-y)(1+xy)Q(x,y)/(A^2 B M),          (3)

    f_BB-f_CC = 4(x-y)(1+xy)R(x,y)/(A^2 B^2),           (4)

where

    Q(x,y)=3x^2y^2+2x^2y+3x^2-6xy^2-2x+y^2-2y+1,
    R(x,y)=x^2+y(1-4x-y+3x^2).

On the somewhat larger square `0<=x<=1/8`, `|y|<=1/8`,

    Q >=1-1/4-1/4-1/256-3/256=31/64>0.                 (5)

Here the four possible negative contributions are `-2x`, `-2y`,
`2x^2 y`, and `-6xy^2`; every other term was retained as nonnegative
or simply discarded. On the present region,

    1-4x-y+3x^2 >=1-1/2-1/8=3/8,

so `R>=0`. All factors in (2)--(4) therefore have the required sign.
This proves all four inequalities in this region.

## 3. The region `0<=x<=y<=1/8`

Here the two simpler remainders coincide:

    f_CB=f_BB=2(y-x)(1-x-y-xy)/(AB) >=0,                (6)

because `1-x-y-xy>=47/64>0`. Moreover

    f_CC-f_CB =4x(y-x)(1+xy)/(A^2 B) >=0,              (7)

    f_BC-f_CC =4(1-x^2)(x-y)^2(1+xy)^2/(A^2 B M)
                   >=0.                              (8)

Thus all four remainders are nonnegative here as well.

## 4. The region `y=-z<=0`

Now `0<=x,z<=1/8`. The first remainder factors as

    f_CC =2[x^2(1-x)+z(1+x)](1-x-z-xz)
             /[(1+x^2)^2(1+z^2)] >=0.                 (9)

The factor `1-x-z-xz` is at least `47/64`. Formula (3) remains an exact
identity in this region, and (5) remains valid. Since `x-y=x+z>=0`, it
gives `f_CB>=f_CC>=0`.

For the last two remainders, two short groupings suffice. Put

    M_-=(1-xz)^2-(x+z)^2>0.

Then

    f_BC=P_BC/[(1+x^2)(1+z^2)M_-],

where the following grouping is the full numerator:

    P_BC = z[2-2x-4xz-10x^3-4x^3z-6x^3z^2]
           +2x^2(1-x^2-z^4)
           +2z^4+2xz^3+6x^2z+6x^2z^3+4x^4z+6x^4z^3.

The bracket multiplying z is at least `3/2`. To see this, bound its
subtracted part by

    2x+4xz+x^3(10+4z+6z^2)
      <=5/16+339/16384=5459/16384 <1/2.

Also `1-x^2-z^4 >=1-1/64-1/4096>0`. All the remaining terms are
nonnegative. Hence `P_BC>=0`.

Finally,

    f_BB=P_BB/[(1+x^2)(1+z^2)^2],

where

    P_BB =z[2-4z-4z^2-2z^3-2x-12xz]
           +2x^2(1-2z)+2xz^3+4x^2z^2+2x^2z^3.

The first bracket is at least

    2-1/2-1/16-1/256-1/4-3/16=255/256>0,

and `1-2z>=3/4`. Thus `P_BB>=0`.

This proves all four inequalities in the negative boundary-angle region
and completes the theorem.

## 5. What the theorem supplies, and what it does not

The old positive continuation used twelve bivariate polynomial coefficient
tables on domains with central half-angle at most `1/64`. Those tables are
unnecessary for proving the wall remainder signs: the short proof above
works up to `1/8` for both angle magnitudes.

The proof does not bound the cost of replacing four unequal actual central
angles by one common angle. The complete widened positive cycle must still
retain or pay those transport costs. In particular, nonnegative remainders
alone do not justify importing the old near-axis positive theorem into its
six difficult larger-angle intervals.

## 6. The full directly derived positive-entrance domain

**Theorem 2.** All twelve remainder formulas in this chapter remain nonnegative on the larger, asymmetric domain

    0≤x=tan(alpha/2)≤1/5,
    −1/8≤y=tan(beta/2)≤1/3.                           (10)

This is the domain obtained from the actual all-positive quadrant bootstrap and its negative-boundary refinement. It is a continuous enlargement, not an angle partition or enumeration. The algebraic identities (1)–(9) remain exactly the same; only their factor bounds need checking again.

All denominators remain positive. For y≥0, 1+xy>|x−y| since x≤1/5,y≤1/3; for y=−z≤0, 1−xz≥39/40>x+z, where x+z≤13/40. Thus M>0 throughout.

If 0≤y≤x≤1/5, formula (1) is nonnegative. The factor Q in (3) satisfies

    Q≥1−2x−2y−6xy²≥1−4/5−6/125=19/125>0.

For R, the bracket 1−4x−y+3x² decreases in x and y on this region, and hence is at least its value 3/25 at x=y=1/5. Thus R≥0. Equations (2)–(4) prove all four signs in this region.

If 0≤x≤y≤1/3 with x≤1/5, the factor in (6) satisfies

    1−x−y−xy≥1−1/5−1/3−1/15=2/5>0.

Equations (6)–(8) therefore prove all four signs.

Finally let y=−z, with 0≤z≤1/8 and 0≤x≤1/5. In (9),

    1−x−z−xz≥13/20>0.

In formula (3), the negative-angle expression for Q is

    Q(x,−z)=3x²z²−2x²z+3x²−6xz²−2x+z²+2z+1,

so

    Q(x,−z)≥1−2/5−1/100−3/160=457/800>0.

This proves f_CB≥f_CC≥0. The full grouped P_BC numerator in Section 4 has its bracket multiplying z bounded below by

    2−2/5−1/10−2/25−1/250−3/4000
      =5661/4000>0.

Also 1−x²−z⁴≥1−1/25−1/4096>0. Its remaining terms are all nonnegative. The P_BB bracket is at least

    2−1/2−1/16−1/256−2/5−3/10=939/1280>0,

and 1−2z≥3/4. Its remaining grouped terms are nonnegative as well. Thus f_BC,f_BB≥0. This exhausts all signs and proves Theorem 2. ∎

As before, these are exact remainder inequalities. Their application to a cycle must still retain the actual separator sources and justify each unequal-angle transport cost.
