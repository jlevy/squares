# Two fixed wall bars select the northeast upper auxiliary

This is the new shared selection argument used in C1090. It replaces a
wall-center case split by necessary ownership of a single point.
All decimals are exact; strict ownership and weak exclusion are distinguished.

The local point lemmas cited below are included unchanged in
[the recovered geometric library](../../C1089/reference/recovered-lemmas/)
The library links resolve relative to this proof chapter.

## Theorem

Let S,E be disjoint open squares of side a>1. Their sides need not have the
same orientation. Suppose S strictly owns

    M_S=(2.35,1.65), F8=(3,1.74), G8=(3,1.6),

and excludes the three points

    K=(3,1), K'=(3.086,1), R=(3.086,2)

and the whole segment

    I=[2.26,2.8] x {1}.

Suppose E strictly owns M_E=(2.35,2.35), excludes

    M_N=(1.65,2.35), F9=(3,2.26), G9=(3,2.4),

and satisfies these two actual-ownership alternatives:

    E owns F5=(2,2.26) or F7=(2.4,3);
    E owns G6=(2.26,2) or G7=(2.26,3).                  (C)

Then

    G7 is strictly in E;
    if G6 is strictly in E, F7 is strictly in E.        (S)

No top square, top-wall sign, left-wall sign, propagated center enclosure,
angle sampling, or assertion that an omitted point has another owner is
required by this theorem. The excluded segment I must be a genuine excluded
whole segment, not a join of endpoints belonging to different squares.

## Proof

### 1. Whenever E owns G6, the actual S has negative canonical angle

Disjointness makes G6 excluded from S. Apply the outward sign-lock theorem
[C981-WALL-CYCLES, Theorem 6](../../C1089/reference/recovered-lemmas/C981-WALL-CYCLES.md)
to S, with its strict M_S,G8 and its excluded K,R,G6,I. It proves that S has
a strictly negative canonical frame. Reflection of the ENTIRE local
configuration in y=2 therefore puts S in the nonnegative frame required by
the two outward-point lemmas below. The axial alternative has been excluded
by the sign-lock theorem itself.

Both reflected outward-point lemmas use exactly the same S inputs:

| Their input before reflection | Actual input after y -> 4-y |
|---|---|
| strict (2.35,2.35), (3,2.26) | M_S, F8 in S |
| excluded (2.26,2), (3.086,2) | G6 in E, and R |
| excluded (2.26,3), (2.8,3) | the two endpoints of I |
| excluded (3,3), (3.086,3) | K,K' |

### 2. E owning G6 but excluding F7 is impossible

The first alternative in (C) forces F5 in E. Reflect the inward-point
[C1084-DUPLICATE-POINT, Theorem 1](../../C1089/reference/recovered-lemmas/C1084-DUPLICATE-POINT.md)
in y=2. Its strict points become M_E,F5,G6; its exclusions become M_N,
M_S,F7. The first two are genuinely excluded, M_S by disjointness, and F7
is the current omitted point. The lemma proves

    (2.46,2.01) strictly in E.

Theorem 2 of the same chapter, reflected in y=2 and applied to the S inputs
in the preceding table, puts the identical point strictly in S. This
contradicts disjoint interiors. We have proved G6 in E implies F7 in E.
The case where F7 lies on E's boundary is an omitted-point case here.

### 3. E cannot omit G7

Suppose G7 is excluded from E. The second alternative in (C) forces G6 in E;
Section 2 forces F7 in E.

If F5 is excluded, the quarter-turn (x,y)->(4-y,x) of the
[MIXED-SPAN-FOUR-POINTS theorem](../../C1089/reference/recovered-lemmas/MIXED-SPAN-FOUR-POINTS.md)
applies. Its two strict inputs are G6,F7; its four exclusions are
F5,G7,F9,G9. These are precisely the hypotheses just established. This
is impossible for every square orientation.

If F5 is strictly in E, then
[C974-C976-DUPLICATE-POINT, Theorem 2](../../C1089/reference/recovered-lemmas/C974-C976-DUPLICATE-POINT.md)
applies to E with strict M_E,F5,G6,F7 and excluded G7,M_N,M_S. It gives

    (2.50,2.04) strictly in E.

Theorem 1 of that chapter, reflected in y=2, applies to S with the exact
input table in Section 1. It gives the identical strict point in S,
again impossible.

Every point is either strictly interior or excluded from the open square,
so the two alternatives for F5 are exhaustive, including boundary contact.
Both conclusions (S) are proved. ∎

## Literal C1090 owner map

S=Q5 and E=Q6. The excluded M_N belongs strictly to Q7. The two points F9,G9
belong strictly to actual Q10. The corner points K,K' belong to actual Q1,
R to actual Q10, and the entire I to actual Q9. All these owners are
distinct from S,E as required. No property of marker 1 is used.

The alternatives (C) follow from the actual NE component lists, after
excluding F9,G9 by their Q10 ownership. They are not extra hypotheses on
the original packing.

## What is new and what is reused

The selection theorem and its use BEFORE any top-wall split are new in this
handoff. The local sign lock, two duplicate-point pairs, and mixed-span
inequality are recovered continuous proofs, not new discoveries or newly
compiled theorems. This proof makes their logical combination and literal
inputs explicit. In particular, it never applies the C1089 family theorem
to C1090's different marker family.
