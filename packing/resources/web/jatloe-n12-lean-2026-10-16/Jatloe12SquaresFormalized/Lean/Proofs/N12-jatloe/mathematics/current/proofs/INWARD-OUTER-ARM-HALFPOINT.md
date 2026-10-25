# An inward square with an outer arm and a foreign short bar owns the halfpoint

All terminating decimals are exact rationals. All square ownerships are strict, and an exclusion allows a boundary point. The proof is continuous over both complete canonical signs and uses no side upper bound.

## 1. The local point-and-bar theorem

**Theorem 1.** Let C be an open square of side a>1 strictly owning

    M=(.35,.35), I=(0,.26), J=(.26,0), A=(.4,1).

Suppose it excludes O=(0,0), F=(.26,1), and every point of the segment

    {1} x [.26,.4].

Then C strictly owns H=(.5,1).

The excluded segment may in particular be the strict segment in one other actual square disjoint from C. Its two endpoint exclusions alone are not substituted for the whole segment in the proof.

### 1.1. The negative canonical sign is impossible

Give C the frame u=(c,-s), v=(s,c), where c>=s>=0 and c^2+s^2=1. Write U,V for its lower faces.

At F, the upper-u and upper-v bands follow from A, with respective projection gaps .14c and .14s. Its lower-v band follows from I. Thus F is lower u:

    U>=.26c-s.

Let E=(1,.4), the upper endpoint of the excluded bar. Its lower-u band follows from J, since .74c-.4s>=.34c>0. Its lower-v band follows from M. Its upper-v band follows from A, since the difference of their v projections is .6(c-s)>=0 and A is strict. Thus E is upper u and

    U+a<=c-.4s.

These opposed faces imply

    a<=.74c+.6s<=sqrt(.74^2+.6^2)=sqrt(.9076)<1,

which is impossible. Equal projections at the axial or diagonal endpoints still give strict bands from the strictly owned comparison point. Hence the entire negative canonical sign has been excluded.

### 1.2. Missing H would give a large positive angle

C therefore has positive frame u=(c,s), v=(-s,c), with c>=s>=0. Write e,V for the lower faces and T=V+a for the upper v face.

The two v bands of O follow from I,J and its upper-u band follows from M. Since O is excluded,

    0<=e<.26s.                                        (1)

The strict inequality follows from I. In particular s>0.

At F, the lower-u band follows from I, and its upper-u and lower-v bands follow from A. Its only possible exit is upper v:

    T<=c-.26s.                                        (2)

Suppose H were excluded from C. Its lower-u and upper-v bands follow from A; its lower-v band follows from J, with increment c-.24s>0. It would therefore be upper u:

    e+a<=.5c+s.

Together with (1) and a>1, this implies .5c+s>1. Put z=s/(1+c), so

    c+sz=1, -s+cz=-z,
    (1+z^2)(.5c+s-1)=(1-z)(3z-1)/2.

The canonical interval has 0<z<=sqrt(2)-1<1. We have proved

    z>1/3.                                           (3)

### 1.3. A strict point meets the actual bar

Define Z=(1,z). Its u projection is exactly1, so (1) and a>1 put it strictly between e and e+a. Its upper-v band follows from I, because v(Z)=-z<.26c. For its lower-v band, (2) gives

    V<c-.26s-1.

The exact identity

    c-.26s+z-1=z(.74-s-.26c)                          (4)

makes the last expression less than -z. Indeed s+.26c increases throughout the canonical positive angle interval, and at z=1/3 its value is

    .6+.26(.8)=.808>.74.

By (3), the right side of (4) is strictly negative. Hence V<-z and Z is strictly in C.

If z<=.4, then (3) places Z on the excluded segment {1}x[.26,.4], a contradiction. If z>.4, the endpoint E=(1,.4) itself is strict in C. Its lower-u band follows from J; its upper-u band follows from

    c+.4s< c+zs=1<e+a.

Its upper-v band follows from I, since s>.6 and therefore s-.14c>0. Finally, (2) gives the strict lower-v margin

    v(E)-V>1-.6c-.74s
             >=1-sqrt(.6^2+.74^2)>0.

Thus E would also be inside C, contrary to the excluded bar. Both possibilities for z have failed, so the assumed exclusion of H was impossible. This proves Theorem 1. The axial case was already excluded by (1), and the diagonal case belongs to the second bar alternative. ∎

## 2. Literal C1092 MMMP application

**Corollary 2.** In the original MMMP family, suppose actual Q5 owns F4,G6,G8 and actual Q10 owns F8. Then Q5 strictly owns (3,1.5), and actual Q9 strictly owns its bottom origin (2,1).

Use the simultaneous quarter-turn

    (X,Y)=(2-y,x-2), C=Q5.

The complete source ledger for Theorem 1 is

| Local datum | Original point or segment | Actual source |
|---|---|---|
| Strict M | (2.35,1.65) | Original Q5 marker |
| Strict I | G6=(2.26,2) | Q5 by hypothesis |
| Strict J | F4=(2,1.74) | Q5 by hypothesis |
| Strict A | G8=(3,1.6) | Q5 by hypothesis |
| Excluded O | (2,2) | Actual Q7 by the full-center theorem |
| Excluded F | F8=(3,1.74) | Actual Q10 by hypothesis |
| Excluded {1}x[.26,.4] | [2.26,2.4]x{1} | Actual Q9, by universal strict G5,F6 and convexity |

Theorem 1 therefore puts its H=(.5,1), which is original (3,1.5), strictly into actual Q5. This point is excluded from the different actual paired southeast corner Q1.

Now reflect Theorem 7 of `C1092-DIRECT-WALL-POINT.md` across x=2, with the actual corner K=Q1, boundary B=Q9, b=.914 and ell=1.6. Its strict corner anchors become (3,.914),(3,1); its excluded corner halfpoint is precisely (3,1.5), just proved in Q5. Its strict boundary anchors become (2,.914),F6=(2.4,1), both in actual Q9. The quadrant and bottom wall are the original genuine container walls. The theorem consequently puts (2,1) strictly in this same actual Q9. ∎

## 3. Exact scope

The corollary applies in particular to the right-wall alternative Q10=525056={F8,F9,G9} when Q5 owns G8: the universal F6 ownership in Q9 and F8 ownership in Q10 force F4 in Q5 by its original F-covering row. If G6 were absent from Q5, `MIXED-SPAN-FOUR-POINTS.md` would exclude its strict F4,G8 pair: its four isolated exclusions would be that actual G6 omission, F8 in Q10, and G5,F6 in Q9. Hence the displayed inward pair is literal in this branch.

If Q5 also owns F8, the foreign F premise of Theorem 1 is unavailable, and this corollary does not claim to cover that different branch. The proof retains the strict ownership of the entire bottom segment and does not treat it as an arbitrary geometric gap.
