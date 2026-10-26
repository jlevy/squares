# C1092 MPPM: simultaneous positive caps and conditional crosspoint seeds

All decimals are exact rational numbers. Retain the original no-omission OOOO entrance, its twelve actual open square owners, the common side 1<a<=1.001, and all established actual wall advances. Exclusion includes a possible boundary point and never assigns an auxiliary to another square.

Normalize a strictly positive ordinary central as C=Q4, translate by (-2,-2), and write

    u=(c,s), v=(-s,c), c>=s>0, c^2+s^2=1,
    U<u·Z<U+a, V<v·Z<V+a,
    A=U+a, K=V+a, x=s/(1+c).

The strict ordinary points are

    M=(-.35,-.35), P=(-1,-.26), G=(-1,-.4).

Its forward point is T=(-.26,0), its backward inner point is I=(0,-.26), and its local crosspoint is X=(-.5,0).

## 1. An upper-u cap without a membership assumption

**Theorem 1.** Every such strictly positive ordinary C satisfies

    U>=-c-s, V>=.4s-c, A<=0, K<=1.086s.             (1)

There are the following stronger alternatives, for the same actual faces:

| Forward membership in C | Additional simultaneous bounds |
|---|---|
| T omitted | A<=-.26c, V>=.56s-c |
| T strict | K<=s |
| T strict and I omitted | A<=-.26s |

**Proof.** When T is omitted, all four conclusions and the two stronger bounds are the unconditional profile in Lemma 1 of C1092-MPPM-MISSING-POSITIVE-WALL-ORDER.md. Its whole bottom bar has one actual owner Q9; no preceding-origin hypothesis is needed.

When T is strict, Theorem 1 and Corollary 2 of C1092-MPPM-FORWARD-OWNED-POSITIVE-D.md give U>=-c-s, V>=.4s-c and K<=s. If I is omitted, their additional cap A<=-.26s supplies A<=0.

It remains the actual ordinary/inward overlap where both T and I are strict. The independently proved C1092-MPPM-CENTERED-POSITIVE-OVERLAP.md excludes O=(0,0) from C, using only its genuine ordinary neighbors and walls. At O the lower-u band follows from T, with increment .26c>0; the lower-v band follows from I, with increment .26c>0; and the upper-v band follows from T, whose v-projection is .26s>0. Thus the omitted O can only exit through upper u, giving A<=0. This does not assign O another owner. All alternatives have been exhausted. ∎

## 2. Unconditional owned-forward seeds and a conditional missing-forward seed

**Theorem 2.** If T is strict, then X=(-.5,0) is strict in C for every strictly positive canonical angle. If T is omitted, the same conclusion follows under the additional closed-interval hypothesis

    0<x<=1/3.                                      (2)

No next-forward ownership, preceding-wall origin or assumed central center is needed.

**Proof.** The lower-u band follows directly from G:

    u(X)-u(G)=.5c+.4s>0.

When T is strict, its upper-u comparison supplies the required band at once:

    u(T)-u(X)=.24c>0.

When T is omitted, assume (2). For this upper-u band, (1) and a>1 give

    A>=a-c-s>-.5c,

because

    1-s-c/2=(1-x)(1-3x)/(2(1+x^2))>=0             (3)

on (2). Thus even the endpoint x=1/3 gives a strict band. For the lower-v band, K<=1.086s gives

    v(X)-V>=a-.586s>0.                             (4)

To establish the final upper-v band, first suppose T is omitted. Then V>=.56s-c, so

    K-v(X)>=a-c+.06s>0.

Now suppose T is strict. If x>=1/10, the weaker V>=.4s-c is sufficient:

    K-v(X)>=a-c-.1s
             >1-c-.1s=s(x-.1)>=0.                 (5)

If 0<x<=1/10, use instead the genuine far bottom point F=(-.56,-1), or original (1.44,1), strict in actual Q9 and hence excluded from C. It has three strict bands:

    u(F)-u(G)=.44c-.6s>0,
    u(M)-u(F)=.21c+.65s>0,
    v(P)-v(F)=.44s+.74c>0.

For the first sign, s/c=2x/(1-x^2)<=20/99<11/15. Consequently F must be lower v, giving V>=.56s-c and again K-v(X)>=a-c+.06s>0. The two owned-forward intervals cover its complete canonical range, and their shared endpoint is retained. All four bands of X are strict, proving Theorem 2. ∎

## 3. A forward-owned sector with a foreign next crosspoint

**Theorem 3.** Retain (2), suppose T is strict in C, and suppose E'=(0,-.5) is excluded from C. Then

    A<=-.5s,                                      (6)

C excludes I=(0,-.26), and H=(-1,-.5) is strict in C.

The premise that E' is excluded must come from an explicit owner or another proved exclusion. Theorem 2 can supply it unconditionally from a positive forward-owned next actual central, or from a positive missing-forward next central satisfying (2).

**Proof.** At E', the lower-u band follows from M since .35c-.15s>=.20c>0. Its upper-v band follows from M, since v(M)-v(E')=.35s+.15c>0. If E' were lower v, the forward-owned cap K<=s would imply

    a<=s+.5c<=1

by (3), an impossibility. Thus its only exit is upper u, proving (6). Since u(I)=-.26s>-.5s>=A, the backward point I is indeed excluded; this conclusion is proved, not presumed.

We give the complete remaining H argument, including its possible lower-v exit. Both upper bands of H are strict: compare its u-projection with M and its v-projection with G. If H exited through lower v, comparison with strict M would force

    -.35c+.35s > -.5c+s,
    s/c<3/13.                                    (7)

The genuine foreign northwest marker N=(-.35,.35) has both lower bands strict, from P and M. An upper-u exit of N, compared with strict T, would require

    -.09c+.35s>0,

or s/c>9/35, contrary to 3/13<9/35. Thus N would have to be upper v. The opposed v-faces at H and N would then give

    a<=v(N)-v(H)=.85c-.65s<1,

again impossible. Consequently an omitted H must instead be lower u, so U>=-c-.5s. Combining this with (6) gives a=A-U<=c<=1, a final contradiction. Hence H is strict. ∎

## 4. Literal original-sector outputs and current scope

Apply simultaneous quarter turns R(x,y)=(4-y,x) to each complete local proof. The relevant points are

| Actual central | Forward point | Local crosspoint X | Next crosspoint E' | Outer halfpoint H |
|---|---|---|---|---|
| Q4 | G3=(1.74,2) | (1.5,2) | (2,1.5) | (1,1.5) |
| Q5 | F4=(2,1.74) | (2,1.5) | (2.5,2) | (2.5,1) |
| Q6 | G6=(2.26,2) | (2.5,2) | (2,2.5) | (3,2.5) |
| Q7 | F5=(2,2.26) | (2,2.5) | (1.5,2) | (1.5,3) |

Each far point F used in Section 2 rotates with its actual wall owner. The resulting strict H in Theorem 3 yields the corresponding next actual wall origin by the already audited paired-corner transfer: Q9(2,1), Q10(3,2), Q11(2,3), or Q8(1,2), respectively.

Theorem 1 is unconditional for positive ordinary sectors, and Theorem 2 gives an unconditional crosspoint for every positive forward-owned sector. Its missing-forward alternative and Theorem 3 explicitly retain the half-angle ceiling (2); this chapter does not yet prove that ceiling for a mixed-forward cycle. In particular no next-forward point is treated as foreign merely because its designated owner omits it.
