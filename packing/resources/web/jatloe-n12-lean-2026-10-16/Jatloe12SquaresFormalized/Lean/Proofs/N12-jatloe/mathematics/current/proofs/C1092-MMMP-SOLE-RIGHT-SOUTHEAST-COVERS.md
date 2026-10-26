# C1092 MMMP: literal southeast covers and the bottom origin for every positive case

All terminating decimals are exact rationals. The squares are the actual original open squares of common side a>1, with disjoint interiors. Owned points are strict and absent points may lie on faces. Every local theorem used below covers its whole stated canonical angle interval.

## 1. The literal original southeast component filter

The right square is now universally

    Q10=524800={F9,G9},

by `C1092-MMMP-PARTIAL-RIGHT-ENDING.md`. The universal actual owners relevant to the original Q5 row are

    F5,G3 in Q7;
    F6,G5 in Q9;
    F9,G9 in Q10.                                (1)

Remove from the literal original combined list M5 every component meeting one of the six foreign points in (1). This direct single-component filter, without choosing or enumerating joint ownership vectors, leaves exactly:

| Label | Strict F subset | Strict G subset |
|---|---|---|
| 65552 | F4 | G6 |
| 65792 | F8 | G6 |
| 65808 | F4,F8 | G6 |
| 69648 | F4 | G2,G6 |
| 69904 | F4,F8 | G2,G6 |
| 262160 | F4 | G8 |
| 262400 | F8 | G8 |
| 262416 | F4,F8 | G8 |
| 327696 | F4 | G6,G8 |
| 327936 | F8 | G6,G8 |
| 327952 | F4,F8 | G6,G8 |
| 331792 | F4 | G2,G6,G8 |
| 332048 | F4,F8 | G2,G6,G8 |

The source M5 is displayed in `C1092-ORIGINAL-ENTRANCE.txt`; the same filter of its original component projection V5 gives the same thirteen rows. No new geometric exclusion or assignment of an unowned auxiliary is built into this filter.

Label262160 is impossible. The actual Q5 would own F4,G8 and exclude G6,F8 by that exact label. The universal Q9 in (1) excludes its G5,F6 from Q5. These are precisely the two strict and four excluded points of the untransformed theorem `MIXED-SPAN-FOUR-POINTS.md`. Its all-angle contradiction removes this label.

The remaining twelve components can therefore be covered by three disjoint classes:

* The eight inward components, containing F4,G6:

      65552,65808,69648,69904,327696,327952,331792,332048.

* The three remaining ordinary components, containing F8,G8:

      262400,262416,327936.

* The single remaining short mixed component:

      65792={F8,G6}.

An inward component may also contain the ordinary pair. The displayed classes make the inward case first, so they are disjoint. In particular optional G2 ownership remains explicitly present in four of the inward rows; no owner has been assigned to G2 when it is absent from Q5.

## 2. An axial southeast square is impossible

Translate by (-2,-2). The actual southeast marker is M=(.35,-.35), the northwest center O=(0,0) is foreign to Q5, the actual right origin R0=(1,0) is in Q10, and the actual paired southeast corner Q1 owns K=(1,-1).

For an axis-parallel inward square, the strict points F4=(0,-.26) and G6=(.26,0) give O both strict coordinate bands, contradicting its actual foreign ownership.

For an axis-parallel ordinary square, F8=(1,-.26) gives both R0 and K their two strict horizontal bands. Their exclusions and the intervening strict F8 force R0 above the upper horizontal side and K below the lower one. The vertical side length would be at most1, contrary to a>1.

For the short mixed component, strict F8 gives R0 its horizontal band and strict G6=(.26,0) gives its vertical band. Thus R0 would be strict in Q5, again contradicting its actual owner.

These three cases cover the twelve retained components. Hence Q5 has no axial canonical representative.

## 3. The common actual consequence of a missing bottom origin

Let B=Q9, and suppose its bottom origin (2,1) were absent. Reflect Theorem7 of `C1092-DIRECT-WALL-POINT.md` across x=2, with actual corner Q1 and boundary B. Its strict corner anchors are (3,.914),(3,1), its boundary anchors are the actual B marker (2,.914) and universal F6=(2.4,1), and its corner and bottom walls are the genuine original ones. Its contrapositive gives

    (3,1.5) strictly in Q1.                     (2)

After translation by (-2,-2), write this strict foreign point as

    Y=(1,-.5).                                  (3)

Also the universal actual B pair G5,F6 supplies the whole strict segment

    [.26,.4]x{-1} in B.                          (4)

Both (2) and (4) concern the actual original corner and bottom square. They do not require an owner of F8 or G8 outside Q5.

## 4. Every positive ordinary case has the bottom origin

Suppose Q5 has positive canonical angle and owns F8,G8, allowing any additional auxiliaries in the original row. The theorem `C1092-MMMP-ORDINARY-SOUTHEAST-MISSING-ORIGIN.md` proves that a missing bottom origin would force this actual Q5 to have a strictly negative angle. Its Section2 is the complete positive-angle contradiction, using only the original marker, the ordinary pair, the actual right origin, actual northeast point (2.47,2.12), actual paired corner, and the foreign halfpoint (2).

Those actual inputs apply literally here, regardless of the other points of Q5's label. Consequently the bottom origin is strict in B for every positive ordinary case.

## 5. Every positive inward case also has the bottom origin

Suppose Q5 has positive angle and owns F4,G6. Use the common quarter-turn chart

    (X,Y)=(2-y,x-2), C=Q5, W=Q9.

A quarter turn preserves its positive canonical sign. The actual C owns M=(.35,.35), I=(0,.26), J=(.26,0), and excludes O=(0,0), which belongs to actual Q7.

Assume first that G8 is absent from C. If the bottom origin were absent, Section3 above would put its local H0=(.5,1) in the actual corner Q1. Its local A=(.4,1) is excluded because it is original G8, the stated omission. The actual W owns

    (1.086,0), (1,.26), (1,.4),

coming from its marker,G5,F6, has its genuine wall X<=2, and excludes (1,0) by the missing-origin supposition. These are exactly every input of the local Theorem1 in `C1092-MMMP-DOUBLE-RIGHT-BOTTOM-ORIGIN.md`. That theorem treats A,H0 as isolated exclusions and does not require Q10 to own either of them. Its continuous two-square contradiction applies, proving the bottom origin.

Now suppose G8 is strict in C. If F8 is also strict in Q5, this is an ordinary case and Section4 applies. If F8 is absent, use Theorem1 of `INWARD-OUTER-ARM-HALFPOINT.md`. Its complete transformed source table is

| Local input | Actual source |
|---|---|
| Strict M,I,J | Q5 marker,G6,F4 |
| Strict A=(.4,1) | G8 in Q5 |
| Excluded O | Actual Q7 center |
| Excluded F=(.26,1) | The stated absence of F8 from Q5 |
| Excluded whole {1}x[.26,.4] | Actual Q9 segment (4) |

The local theorem therefore gives H=(.5,1), namely original (3,1.5), strictly in Q5. This contradicts (2) if the bottom origin were absent. Hence the bottom origin is strict in this case as well.

The theorem just used only needs an F8 exclusion. Its use does not assert F8 ownership in the actual right square. In fact its complete negative-angle contradiction also shows that the inward labels327696 and331792, which own F4,G6,G8 and omit F8, cannot have negative canonical angle at all.

All ownership alternatives within the eight inward rows have now been covered.

## 6. The positive short mixed case owns the same halfpoint

Suppose Q5 has positive frame u=(c,s),v=(-s,c), c>=s>0, and owns F8,G6. This local argument permits additional auxiliaries, though its only class not already covered is65792. Its strict points are

    M=(.35,-.35), D=(.26,0), P=(1,-.26).

Let H,V be its upper and lower v faces. The actual northeast point

    K0=(.47,.12)

is excluded from Q5, by Theorem1 of `C1092-MMMP-NORTHEAST-LOWER-TIP.md`. Its lower u band follows from strict D. Its upper u band follows from strict P, with gap .53c-.38s>=.15c>0. Its lower v band follows from strict M, with gap .47c-.12s>=.35c>0. Thus its sole exit is upper v:

    H<=.12c-.47s.                               (5)

Suppose Y=(1,-.5) were absent from this actual Q5. Its lower u band follows from M, since .65c-.15s>=.5c>0. Its two upper bands follow from P, with gaps .24s and .24c. Therefore Y could leave only through the lower v face, giving

    V>=-s-.5c.

Together with (5), this would imply

    a=H-V<=.62c+.53s<=sqrt(.6653)<1.

This is impossible. Hence Y is strictly in Q5. If the actual bottom origin were absent, (2) would put the same point in the different actual Q1. Therefore the bottom origin is strict for the positive short mixed case too.

## 7. Universal conclusion for the positive southeast sign

Combining the twelve-cover classification with Sections4--6 proves:

**Theorem.** Whenever the actual southeast Q5 has positive canonical angle in the remaining original MMMP family, the actual Q9 strictly owns its bottom origin (2,1). Consequently

    [2,2.4]x{1} is strictly in the same actual Q9.

No southeastern angle bound or floor has been inferred merely from this conclusion. Those remain additional actual-square obligations for the positive cases. Negative ordinary and negative inward cases retain their own scope; only the explicit negative exclusion for labels327696,331792 was added above.

Every transferred theorem was applied to its original actual strict points, weak absences, genuine wall or corner, and actual whole foreign segment. In particular no missing auxiliary was given another owner just to complete a local input table.
