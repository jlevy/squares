# Further continuous wall and top reductions for C974 and C976

All decimal numbers denote exact rationals. An owned point is strict; an excluded point may touch a face. The statements below retain the actual owner of each whole foreign segment. These are the structural reductions preceding the later complete C976 ending, identified in Section 6. C974 still requires its final contradiction.

## 1. A wall advance that does not exclude the inward auxiliary

**Theorem 1.** Let Q be an open square of side a>1, with closure in x≥0. Suppose it owns

    P=(.914,2), A=(1,2.4),

and excludes

    F=(1,1.74), M=(1.65,2.35).

Then Q strictly owns T=(1,2.56).

Unlike the older wall advance, this statement does not exclude (1.74,2). It is valid whether that auxiliary is owned, foreign or absent.

**Proof.** Choose a positive-quadrant face normal (l,h), with l>0, h≥0 and l²+h²=1; the perpendicular normal is (−h,l). This relabeling covers every square orientation. Let U,V be the lower face coordinates. The actual wall gives

    lU≥h(V+a).                                          (1)

Both upper bands of F follow strictly from A. Thus F is lower u or lower v.

If U≥l+1.74h, then at M its lower u band follows from P, its upper v band follows from A, and its upper u band follows from

    u(M)−U≤.65l+.61h≤sqrt(.7946)<1<a.

Hence M is lower v: V≥−1.65h+2.35l. The target T has both lower bands from A, and both upper bands follow from

    u(T)−U≤.82h<1<a,
    v(T)−V≤.65h+.21l≤sqrt(.4666)<1<a.

Otherwise V≥−h+1.74l. Again T has both lower bands from A, and its upper v band follows from v(T)−V≤.82l<1<a. If its upper u band failed, U+a≤l+2.56h. Multiplying this inequality by l and using (1) and the lower bound for V would give

    a(l+h)≤1+.82lh.

But K=l+h satisfies

    K−1=2lh/(K+1)≥(2sqrt(2)−2)lh≥.82lh.

Therefore aK≤K, contradicting a>1 and K>0. This also handles h=0, and every weak exterior contact. ∎

### Exact applications

In both C974 and C976, actual Q10 owns (3.086,2),(3,2.4). Actual southeast Q6 owns F8=(3,1.74), and actual northeast Q7 owns (2.35,2.35). Reflect all these data through x=2. Theorem 1 applies, uniformly over the supplied auxiliary families, and gives

    (3,2.56)∈Q10 strictly.                              (2)

This includes Q10's label590336, which owns G6 and therefore cannot use the older G6-excluding wall theorem.

## 2. Owning the inward auxiliary gives a larger advance without a wall

**Theorem 2.** Let Q be any open square of side a>1. Suppose it owns

    (.914,2), (1.74,2), (1,2.4),

and excludes (1,1.74),(1.65,2.35). Then it has a strictly positive canonical angle, and

    9/35<s/c<13/37,
    (1,2.74)∈Q strictly.                               (3)

No container hypothesis or upper bound on a is required.

**Proof.** Translate by (−1,−2). Denote the owned points by

    P=(−.086,0), D=(.74,0), A=(0,.4),

and the excluded points by F=(0,−.26), M=(.65,.35).

In a nonpositive canonical frame u=(c,−s), v=(s,c), c≥s≥0, the lower u band of F follows from A; its upper u and upper v bands follow from D and A. Thus F is lower v. At M the lower u band follows from P, the upper u band follows from D, and the lower v band follows from D, since .35c−.09s>0. Hence M is upper v. These two faces imply

    a≤v(M)−v(F)=.65s+.61c≤sqrt(.7946)<1,

which is impossible. This includes the axial case.

Use the positive frame u=(c,s), v=(−s,c), c≥s≥0. The point F has both upper bands from D,A, so it is lower u or lower v. If it is lower u, then M has its lower u band from P, its upper v band from A, and its upper u band from u(M)−u(F)=.65c+.61s<1<a. Thus M would be lower v; but v(D)−v(M)=−.09s−.35c<0 contradicts strict ownership of D. Therefore F is lower v.

Now M has the lower u band from P, the lower v band from D and the upper v band from A. It must be upper u. The strict upper u and lower v bands of D give

    .74c<.65c+.35s,
    −.74s>−.26c,

which are exactly the angle bounds in (3).

For T=(0,.74), both lower bands follow from A. Its upper u band follows from D, since .74(c−s)>0. Its upper v band follows from the lower-v face at F:

    v(T)−V≤c≤1<a.

Thus T is strict in Q, proving the theorem after translating back. ∎

In either original family, Q10 owning G6=(2.26,2) has exactly these hypotheses after reflection through x=2. Hence

    Q10 owns G6  ⇒  (3,2.74)∈Q10 strictly.              (4)

This is an additional actual-owner consequence, not permission to apply the same reach when G6 belongs to a different square.

## 3. A top origin from the actual corner and left wall

### 3.1. A direct proof valid in both C974 and C976

Suppose Q11 owns F3=(1.6,3). In both families actual Q8 owns (.914,2),(1,2.4), and excludes (1,1.74) in Q1 and (1.74,2) in Q5. The older all-angle wall-reach theorem therefore gives (1,2.56) strictly in Q8; ownership of the northwest marker is not one of that theorem's excluded premises. Together with (1,2.4), this puts (1,2.5) strictly in that same Q8.

Apply Theorem 7 of `C1092-DIRECT-WALL-POINT.md` to actual K=Q4 and B=Q11 after the simultaneous reflection (x,y)↦(x,4−y). Its parameters are b=.914 and ell=1.6. The exact data are:

| Local theorem datum | Original strict point or condition |
|---|---|
| K owns (1,b) | Q4's original marker (1,3.086) |
| K owns (1,1) | Q4's compulsory paired-corner point (1,3) |
| K excludes (1,1.5) | (1,2.5) strictly in actual Q8, just proved |
| B owns (2,b) | Q11's original marker (2,3.086) |
| B owns (ell,1) | Q11's F3=(1.6,3) |
| K is in the first quadrant, B is above y=0 | The reflected genuine container walls |

These are distinct actual disjoint squares of the same side a>1, as that two-square theorem requires. Its all-angle conclusion puts (2,1) strictly in the reflected Q11, or

    (2,3)∈Q11 strictly, in both original families.       (5)

This proof uses no stronger reach of the merged C976 left owner and no surrogate corner owner.

### 3.2. An alternative C974 proof by two strict segment completions

Suppose a C974 alternative gives Q11 ownership of F3=(1.6,3). The actual left wall Q8 owns (1,2.8) by Theorem 4 of `C981-WALL-CYCLES.md`: its foreign marker (1.65,2.35) is the globally absent northwest marker in C974, and its other two required exclusions are supplied by actual Q1. The paired northwest corner Q4 owns (1,3).

Apply the corner theorem, Theorem 5 of `OTHER-GEOMETRY.md`, to Q4 in coordinates

    (ξ,η)=(y−3,1−x).

The owned origin is (1,3), the two foreign points are Q8's (1,2.8) and Q11's (1.6,3), and the actual left wall gives η≤1. Its parameters are q=.2,p=.6,r=.6, with

    p²+q²=.4<1,
    p²+r²=.72<1,
    q+r=.8<2sqrt(2)−2.

Therefore Q4 strictly owns (1,3.6), and its whole vertical segment {1}×[3,3.6] is strict.

Now apply Theorem 9 of `OTHER-GEOMETRY.md` to Q11 in coordinates

    (ξ,η)=(2−x,y−3).

Its strict marker (2,3.086) and F3=(1.6,3) become (0,.086),(.4,0); its real top wall gives η≤1. The actual Q4 segment becomes {1}×[0,.6], exactly the foreign segment required by that theorem. It follows that

    (2,3)∈Q11 strictly.

All ownership statements in this alternative chain refer to one fixed physical configuration. In C976 the northwest marker belongs to Q8, so the first use of the stronger wall theorem in this particular chain is unavailable. Section 3.1 supplies the top origin there by a different actual two-square theorem.

## 4. One inward–outward contradiction excludes every rightward top alternative

**Theorem 3.** In either C974 or C976, suppose the actual northeast owner Q7 owns F5=(2,2.26) and G6=(2.26,2), and excludes F7=(2.4,3). Then the configuration is impossible.

**Proof.** The original southeast label family is

    {65792,262400,327936,65824,327968}.

Every member except262400 owns G6. Since G6 is strictly in the different square Q7, pairwise disjointness forces the southeast owner Q6 to have label262400, that is, to own F8=(3,1.74) and G8=(3,1.6) and to exclude G6.

The inward strict-point theorem, Theorem 1 of `C1084-DUPLICATE-POINT.md`, applies to Q7 after reflection through y=2. Its strict anchors are the northeast marker, F5,G6. Its three required excluded points are the southeast marker in Q6, the northwest marker (absent from every square in C974, owned by Q8 in C976), and F7 by this theorem's hypothesis. Thus

    (2.46,2.01)∈Q7 strictly.                            (6)

The actual bottom wall Q9 owns (2,.914),(2.4,1), and the actual Q0 owns (1.87,.76). Its required other exclusions for the strong wall theorem are G2=(1.74,1) in Q0 and the southeast marker in Q6. Theorem 4 of `C981-WALL-CYCLES.md`, transposed, therefore gives (2.8,1)∈Q9. Since Q9 also owns G5=(2.26,1), the entire segment [2.26,2.8]×{1} is strictly in that one owner.

Apply the outward sign theorem, Theorem 6 of `C981-WALL-CYCLES.md`, to Q6. Its owned points are the southeast marker and G8. Its required excluded points are G6 in Q7, (3,1) in the paired southeast corner Q2, (3.086,2) in the right wall Q10, and the complete bottom segment in Q9 just proved. It has a strictly negative canonical angle.

Now reflect the outward strict-point theorem, Theorem 2 of `C1084-DUPLICATE-POINT.md`, through y=2. Its owned marker and F8 are in Q6; its excluded inner point G6 is in Q7, its right marker (3.086,2) is in Q10, its two bottom-segment points (2.26,1),(2.8,1) are in Q9, and its corner points (3,1),(3.086,1) are in Q2. The reflected sign premise has just been established. Consequently

    (2.46,2.01)∈Q6 strictly.                            (7)

The duplicate strict point in (6)–(7) contradicts disjoint open interiors. ∎

**Corollary 4.** In both original families the top owner Q11 cannot own F7=(2.4,3).

Every listed Q11 label owning F7 also owns G7=(2.26,3). Every listed Q7 label owns F5 or F7, and G6 or G7. If Q11 owned F7, disjointness would therefore force Q7 to own F5 and G6 and to exclude F7. Theorem 3 applies. This is a structural disjunction on the complete retained families; no enumeration of individual twelve-owner vectors is used.

It follows that only these four top labels remain in either family:

    16392,147464,16424,147496,

namely F3,G4 with optional F5 and/or G7. In particular Q11 always owns F3=(1.6,3) after this reduction. Section 3.1 therefore establishes (2,3)∈Q11 throughout every remaining alternative of both families, using the actual left wall and northwest corner. Section 3.2 retains the stronger C974-only segment completion as an additional reusable consequence.

## 5. Consolidated consequences of the later point lemmas

The later complete local proofs sharpen the earlier four-label top reduction as follows. The final outward-pair support theorem is in `C974-C976-OUTWARD-PAIR.md`:

| Actual owner | Retained possibilities after the new reductions | Complete proof source |
|---|---|---|
| Top Q11, both families | Exactly16392, owning F3,G4 | `C974-C976-DUPLICATE-POINT.md`, Section 4 |
| Southeast Q6, both families | Exactly327936, owning F8,G6,G8 | `ELBOW-CROSSPOINT.md` |
| Northeast Q7, both families | 131200,131232; both own F7,G7 | The preceding top reduction, Section 4 above, `MIXED-SPAN-FOUR-POINTS.md`, `ELBOW-CROSSPOINT.md`, and `OUTWARD-BAR-AND-UPPER-SPAN.md` |

The southeast label owns F8,G6,G8. The two common northeast labels mean, respectively,

    F7,G7;  F5,F7,G7.

The complete two-square support theorem in `C974-C976-OUTWARD-PAIR.md` excludes every southeast outward label262400, after the top-only common-point branch is removed. Pairwise disjointness then excludes northeast196768 because southeast327936 owns G6. Exactly two central label pairs remain as necessary possibilities at this stage:

    (327936,131200), (327936,131232).

In both pairs actual southeast Q6 owns (2.5,2) and (3,1.5), and the actual corner-to-wall transfer gives (2,1) strictly in Q9. For northeast131232, actual Q7 owns (2,2.5) and (2.42,2.16). For northeast131200, it owns (2.525,2.125) and (2.5,3), the latter transferring (3,2) strictly to actual Q10. The complete point proofs and owner mappings are in `C974-C976-CENTRAL-CROSSPOINTS.md`.

These are structural consequences of the retained label families and the indicated continuous contradictions. No enumeration of full twelve-owner vectors is needed. Further pairwise disjointness forces all three paired corners Q2,Q3,Q4 to label0 and the bottom wall Q9 to label32832. In C974 the left wall Q8 has label2050. In C976 it has label2050 or2082, the latter additionally owning F5. The right wall Q10 has exactly label524800: its G6 alternative is excluded because southeast Q6 owns G6, and its F7 alternative is excluded because northeast Q7 now always owns F7.

The uniform top label also finishes the fourth requested wall-center comparison in C974. Apply the direct wall-center theorem in `WALL-CENTER-AND-C974.md` under (x,y)↦(4−y,4−x). Its strict anchors are the top marker and F3; its excluded points are G7, now strict in northeast Q7, and the northwest marker. The latter is absent in C974 and belongs to distinct Q8 in C976, so this comparison is valid in both families:

    X11<49/25<2.                                        (8)

In C974 the other three wall-center comparisons were already established, giving the complete requested sign reduction with strict margins:

    Y8>423/200,  X9>423/200,  Y10>51/25,  X11<49/25.

The direct actual-corner theorem in Section 3.1 gives (2,3) strictly in Q11 throughout both surviving families. It uses the weaker, legitimate left-wall advance (1,2.56), which remains available when C976 merges the northwest marker into Q8. The larger C974 advance (1,2.8) and the C974-only corner segment in Section 3.2 remain distinct additional consequences.

## 6. Source and present scope

The retained original entrances are `C974/01_entrance_and_85_vectors.txt` and `root_next/special_cases/C976-01-entrance-and-catalogue.txt` in the earlier completed source. The former has exact mask

    (1,2,12,48,192,256,512,1024,4096,8192,16384,32768),

and the latter replaces mask4096 by6144, merging the northwest central marker into actual Q8. Their displayed local ownership families and strict corner hulls supply all inputs explicitly used above. No claim is made to replace their finite local ownership entrance by these lemmas.

The wall advances, all four C974 center signs, the top origin in both families, the branch exclusions, and the consolidated necessary configurations in Section 5 are continuous geometric reductions. The subsequent chapters now complete the entire C976 family: `C976-MERGED-LEFT-ENDING.md` excludes both nonnegative northeast alternatives; `C976-LEFT-UPPER-POINTS.md` gives the strict actual left points; and the complementary actual two-square theorems in `C976-LEFT-TOP-ANGLE.md` and `C976-NEGATIVE-NE-TOP-ENDING.md` exclude all top-square orientations when the northeast angle is negative. Their exact ownership maps retain both final northeast labels and all optional earlier assignments.

C974's complete contradiction remains to be supplied after the two-pair reduction in Section 5. Its northwest marker is absent, whereas C976's belongs to the actual left square; the completed C976 ending uses that merged-marker premise and is not transferred across this ownership change.
