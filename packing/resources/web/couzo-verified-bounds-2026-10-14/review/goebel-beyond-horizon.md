# Beyond-Horizon Rows Against Göbel’s Classical Constructions

Beyond the case corpus the record’s standing side at a count is its beyond-horizon row or
the grid, ⌈√n⌉; it holds no Göbel construction there. This review measures, exactly,
which beyond-horizon rows lie above Göbel’s classical construction at their count, for
four sets: this packet’s 487b058 certificates, #607’s 43ac7d2 rows, the 4e4c8ce index’s
341 rows below both of those, and the record’s current beyond-horizon rows on `main`
(`6964362b5`).

## How Göbel’s Side Is Computed

[goebel_beyond_horizon.py](goebel_beyond_horizon.py) builds every member of the three
closed-form families the Kingbird catalogue states, archived here as
**[Kingbird-Göbel-squares]** (`packing/resources/web/kingbird-squares-in-squares-gobel-squares.md`,
archived 2026-09-07) and **[Kingbird-Göbel-strips]**
(`packing/resources/web/kingbird-squares-in-squares-gobel-strips.md`, archived
2026-09-07), which generalize Frits Göbel’s constructions (**[Göbel 1979]**):

| Family | Count | Side | Condition |
| --- | --- | --- | --- |
| Göbel square | n = 2(a+1)a + b² | a + 1 + (b/2)√2 | a, b positive integers, a − 1 < (b/2)√2 < a + 1 |
| Göbel strip | n = (a+1)a + 2 + b | a + 1 + (1/2)√2 | b = 1 + ⌊(a−1)√2⌋ |
| Corner-touching strip | n = (a+1)a + 3 + b | 2 + (b+1)(1/2)√2 | the same b; the strip page states it “starting at s(18)” |

Göbel’s side at a count m is the least side of any member at a count n ≥ m: removing
n − m squares from a packing of n packs m. Every side is held exactly as p + q√2 with
p and q rational; a rational row side S is compared by the exact sign of S − p against
q√2, squaring only when both are non-negative, and ⌊(a−1)√2⌋ is `isqrt(2(a−1)²)`. So
every relation below is exact; the margins are printed from √2 to 60 places. No
construction is re-verified here: the catalogue states them, and the author’s `58a7833`
reports an exact check over ℚ(√2) of each one it uses up to 1,024
(`gobel_bounds.json`, members up to 975). Its least closed form at or above each count
equals this one at all 661 table rows it reaches; the rows above 975 rely on these
formulas alone.

A rational side cannot equal p + q√2 with q ≠ 0, so no row is equal.

## The Question for the Owner

The rule records a beyond-horizon row when it is below the record’s row or the grid and
every earlier report. If Göbel’s published constructions count as earlier reports, and
as the baseline beyond 324, the rows above them are not recorded. Until the owner
decides, the comparison marks such a row `undecided-goebel`
([beyond-horizon-comparison.json](beyond-horizon-comparison.json)), the claims record
leaves it out, and the register plan lists it separately.

## Tables

[goebel-beyond-horizon.json](goebel-beyond-horizon.json) holds every row of every set;
the rows above Göbel’s construction follow.

### franciscouzo@487b058 (this packet)

296 rows: 42 above, 0 equal, 254 below.
Below by 2.87e-03 to 8.28e-01.

| n | Side, rounded up | Göbel's construction | Family | From count | Above by | Row |
| --- | --- | --- | --- | --- | --- | --- |
| 408 | 20.707106781214260 | 20 + 1/2 sqrt(2) | Göbel strip | 408 | 2.77e-11 | undecided-goebel |
| 415 | 20.899494936674099 | 11 + 7 sqrt(2) | Göbel square | 416 | 6.24e-11 | undecided-goebel |
| 416 | 20.899494936654200 | 11 + 7 sqrt(2) | Göbel square | 416 | 4.25e-11 | undecided-goebel |
| 445 | 21.606601717830411 | 11 + 15/2 sqrt(2) | Göbel square | 445 | 3.22e-11 | undecided-goebel |
| 449 | 21.707106781215686 | 21 + 1/2 sqrt(2) | Göbel strip | 449 | 2.91e-11 | undecided-goebel |
| 488 | 22.606601717852951 | 12 + 15/2 sqrt(2) | Göbel square | 489 | 5.47e-11 | undecided-goebel |
| 489 | 22.606601717848642 | 12 + 15/2 sqrt(2) | Göbel square | 489 | 5.04e-11 | undecided-goebel |
| 492 | 22.707106781252576 | 22 + 1/2 sqrt(2) | Göbel strip | 493 | 6.60e-11 | undecided-goebel |
| 493 | 22.707106781230865 | 22 + 1/2 sqrt(2) | Göbel strip | 493 | 4.43e-11 | undecided-goebel |
| 537 | 23.707106781272295 | 23 + 1/2 sqrt(2) | Göbel strip | 538 | 8.57e-11 | undecided-goebel |
| 538 | 23.707106781249586 | 23 + 1/2 sqrt(2) | Göbel strip | 538 | 6.30e-11 | undecided-goebel |
| 585 | 24.707106781266224 | 24 + 1/2 sqrt(2) | Göbel strip | 586 | 7.97e-11 | undecided-goebel |
| 586 | 24.707106781234812 | 24 + 1/2 sqrt(2) | Göbel strip | 586 | 4.83e-11 | undecided-goebel |
| 634 | 25.707106781229354 | 25 + 1/2 sqrt(2) | Göbel strip | 635 | 4.28e-11 | undecided-goebel |
| 635 | 25.707106781236456 | 25 + 1/2 sqrt(2) | Göbel strip | 635 | 4.99e-11 | undecided-goebel |
| 636 | 25.727922061394232 | 13 + 9 sqrt(2) | Göbel square | 636 | 3.64e-11 | undecided-goebel |
| 685 | 26.707106781224178 | 26 + 1/2 sqrt(2) | Göbel strip | 686 | 3.76e-11 | undecided-goebel |
| 686 | 26.707106781239832 | 26 + 1/2 sqrt(2) | Göbel strip | 686 | 5.33e-11 | undecided-goebel |
| 687 | 26.727922061414540 | 14 + 9 sqrt(2) | Göbel square | 688 | 5.67e-11 | undecided-goebel |
| 688 | 26.727922061424186 | 14 + 9 sqrt(2) | Göbel square | 688 | 6.63e-11 | undecided-goebel |
| 738 | 27.707106781225937 | 27 + 1/2 sqrt(2) | Göbel strip | 740 | 3.94e-11 | undecided-goebel |
| 739 | 27.707106781239729 | 27 + 1/2 sqrt(2) | Göbel strip | 740 | 5.32e-11 | undecided-goebel |
| 740 | 27.707106781243436 | 27 + 1/2 sqrt(2) | Göbel strip | 740 | 5.69e-11 | undecided-goebel |
| 793 | 28.707106781230976 | 28 + 1/2 sqrt(2) | Göbel strip | 795 | 4.44e-11 | undecided-goebel |
| 794 | 28.707106781243630 | 28 + 1/2 sqrt(2) | Göbel strip | 795 | 5.71e-11 | undecided-goebel |
| 795 | 28.707106781257545 | 28 + 1/2 sqrt(2) | Göbel strip | 795 | 7.10e-11 | undecided-goebel |
| 851 | 29.707106781241575 | 29 + 1/2 sqrt(2) | Göbel strip | 853 | 5.50e-11 | undecided-goebel |
| 852 | 29.707106781255264 | 29 + 1/2 sqrt(2) | Göbel strip | 853 | 6.87e-11 | undecided-goebel |
| 853 | 29.707106781240030 | 29 + 1/2 sqrt(2) | Göbel strip | 853 | 5.35e-11 | undecided-goebel |
| 860 | 29.849242405011954 | 15 + 21/2 sqrt(2) | Göbel square | 861 | 9.45e-11 | undecided-goebel |
| 861 | 29.849242404958972 | 15 + 21/2 sqrt(2) | Göbel square | 861 | 4.15e-11 | undecided-goebel |
| 910 | 30.707106781230479 | 30 + 1/2 sqrt(2) | Göbel strip | 912 | 4.39e-11 | undecided-goebel |
| 911 | 30.707106781256350 | 30 + 1/2 sqrt(2) | Göbel strip | 912 | 6.98e-11 | undecided-goebel |
| 912 | 30.707106781261461 | 30 + 1/2 sqrt(2) | Göbel strip | 912 | 7.49e-11 | undecided-goebel |
| 919 | 30.849242405483649 | 16 + 21/2 sqrt(2) | Göbel square | 921 | 5.66e-10 | undecided-goebel |
| 920 | 30.849242404969408 | 16 + 21/2 sqrt(2) | Göbel square | 921 | 5.19e-11 | undecided-goebel |
| 921 | 30.849242405009142 | 16 + 21/2 sqrt(2) | Göbel square | 921 | 9.16e-11 | undecided-goebel |
| 964 | 31.556349186148873 | 16 + 11 sqrt(2) | Göbel square | 964 | 4.48e-11 | undecided-goebel |
| 971 | 31.707106781253358 | 31 + 1/2 sqrt(2) | Göbel strip | 974 | 6.68e-11 | undecided-goebel |
| 972 | 31.707106781253645 | 31 + 1/2 sqrt(2) | Göbel strip | 974 | 6.71e-11 | undecided-goebel |
| 973 | 31.707106781287656 | 31 + 1/2 sqrt(2) | Göbel strip | 974 | 1.01e-10 | undecided-goebel |
| 974 | 31.707106781232863 | 31 + 1/2 sqrt(2) | Göbel strip | 974 | 4.63e-11 | undecided-goebel |

### #607 at 43ac7d2

22 rows: 0 above, 0 equal, 22 below.
Below by 3.16e-02 to 6.47e-01.

### 4e4c8ce index, below 487b058 and #607

341 rows: 47 above, 0 equal, 294 below.
Below by 2.87e-03 to 8.28e-01.

| n | Side, rounded up | Göbel's construction | Family | From count | Above by | Row |
| --- | --- | --- | --- | --- | --- | --- |
| 331 | 18.707106781186548 | 18 + 1/2 sqrt(2) | Göbel strip | 331 | 1.87e-23 | PingYou Ltd (BuddenPing); derived exact |
| 368 | 19.707106781210123 | 19 + 1/2 sqrt(2) | Göbel strip | 369 | 2.36e-11 | Francisco Couzo; local |
| 407 | 20.707106781186548 | 20 + 1/2 sqrt(2) | Göbel strip | 408 | 2.07e-23 | PingYou Ltd (BuddenPing); derived exact |
| 408 | 20.707106781186548 | 20 + 1/2 sqrt(2) | Göbel strip | 408 | 2.07e-23 | Francisco Couzo; derived exact |
| 415 | 20.899494936611666 | 11 + 7 sqrt(2) | Göbel square | 416 | 2.09e-23 | Francisco Couzo; derived exact |
| 416 | 20.899494936650217 | 11 + 7 sqrt(2) | Göbel square | 416 | 3.86e-11 | Francisco Couzo; ct105 task |
| 445 | 21.606601717826290 | 11 + 15/2 sqrt(2) | Göbel square | 445 | 2.81e-11 | Francisco Couzo; local |
| 448 | 21.707106781186548 | 21 + 1/2 sqrt(2) | Göbel strip | 449 | 2.17e-23 | PingYou Ltd (BuddenPing); derived exact |
| 449 | 21.707106781186548 | 21 + 1/2 sqrt(2) | Göbel strip | 449 | 2.17e-23 | Francisco Couzo; derived exact |
| 488 | 22.606601717826290 | 12 + 15/2 sqrt(2) | Göbel square | 489 | 2.81e-11 | Francisco Couzo; derived exact |
| 489 | 22.606601717844322 | 12 + 15/2 sqrt(2) | Göbel square | 489 | 4.61e-11 | Francisco Couzo; local |
| 491 | 22.707106781186548 | 22 + 1/2 sqrt(2) | Göbel strip | 493 | 2.27e-23 | PingYou Ltd (BuddenPing); derived exact |
| 492 | 22.707106781186548 | 22 + 1/2 sqrt(2) | Göbel strip | 493 | 2.27e-23 | Francisco Couzo; derived exact |
| 493 | 22.707106781226524 | 22 + 1/2 sqrt(2) | Göbel strip | 493 | 4.00e-11 | Francisco Couzo; ct105 task |
| 537 | 23.707106781186548 | 23 + 1/2 sqrt(2) | Göbel strip | 538 | 2.37e-23 | Francisco Couzo; derived exact |
| 538 | 23.707106781226524 | 23 + 1/2 sqrt(2) | Göbel strip | 538 | 4.00e-11 | Francisco Couzo; derived exact |
| 585 | 24.707106781226524 | 24 + 1/2 sqrt(2) | Göbel strip | 586 | 4.00e-11 | Francisco Couzo; derived exact |
| 586 | 24.707106781230069 | 24 + 1/2 sqrt(2) | Göbel strip | 586 | 4.35e-11 | Francisco Couzo; ct105 task |
| 634 | 25.707106781224408 | 25 + 1/2 sqrt(2) | Göbel strip | 635 | 3.79e-11 | Francisco Couzo; ct105 task |
| 635 | 25.707106781230069 | 25 + 1/2 sqrt(2) | Göbel strip | 635 | 4.35e-11 | Francisco Couzo; derived exact |
| 636 | 25.727922061389287 | 13 + 9 sqrt(2) | Göbel square | 636 | 3.14e-11 | Francisco Couzo; local |
| 685 | 26.707106781219034 | 26 + 1/2 sqrt(2) | Göbel strip | 686 | 3.25e-11 | Francisco Couzo; ct105 task |
| 686 | 26.707106781230069 | 26 + 1/2 sqrt(2) | Göbel strip | 686 | 4.35e-11 | Francisco Couzo; derived exact |
| 687 | 26.727922061389287 | 14 + 9 sqrt(2) | Göbel square | 688 | 3.14e-11 | Francisco Couzo; derived exact |
| 688 | 26.727922061419038 | 14 + 9 sqrt(2) | Göbel square | 688 | 6.12e-11 | Francisco Couzo; ct105 task |
| 738 | 27.707106781219034 | 27 + 1/2 sqrt(2) | Göbel strip | 740 | 3.25e-11 | Francisco Couzo; derived exact |
| 739 | 27.707106781230069 | 27 + 1/2 sqrt(2) | Göbel strip | 740 | 4.35e-11 | Francisco Couzo; derived exact |
| 740 | 27.707106781238093 | 27 + 1/2 sqrt(2) | Göbel strip | 740 | 5.15e-11 | Francisco Couzo; ct105 task |
| 793 | 28.707106781219034 | 28 + 1/2 sqrt(2) | Göbel strip | 795 | 3.25e-11 | Francisco Couzo; derived exact |
| 794 | 28.707106781230069 | 28 + 1/2 sqrt(2) | Göbel strip | 795 | 4.35e-11 | Francisco Couzo; derived exact |
| 795 | 28.707106781238093 | 28 + 1/2 sqrt(2) | Göbel strip | 795 | 5.15e-11 | Francisco Couzo; derived exact |
| 851 | 29.707106781230069 | 29 + 1/2 sqrt(2) | Göbel strip | 853 | 4.35e-11 | Francisco Couzo; derived exact |
| 852 | 29.707106781249520 | 29 + 1/2 sqrt(2) | Göbel strip | 853 | 6.30e-11 | Francisco Couzo; ct105 task |
| 853 | 29.707106781234289 | 29 + 1/2 sqrt(2) | Göbel strip | 853 | 4.77e-11 | Francisco Couzo; ct105 task |
| 860 | 29.849242405006181 | 15 + 21/2 sqrt(2) | Göbel square | 861 | 8.87e-11 | Francisco Couzo; ct105 task |
| 861 | 29.849242404953195 | 15 + 21/2 sqrt(2) | Göbel square | 861 | 3.57e-11 | Francisco Couzo; local |
| 910 | 30.707106781224535 | 30 + 1/2 sqrt(2) | Göbel strip | 912 | 3.80e-11 | Francisco Couzo; ct105 task |
| 911 | 30.707106781238093 | 30 + 1/2 sqrt(2) | Göbel strip | 912 | 5.15e-11 | Francisco Couzo; derived exact |
| 912 | 30.707106781234289 | 30 + 1/2 sqrt(2) | Göbel strip | 912 | 4.77e-11 | Francisco Couzo; derived exact |
| 919 | 30.849242405477680 | 16 + 21/2 sqrt(2) | Göbel square | 921 | 5.60e-10 | Francisco Couzo; ct105 task |
| 920 | 30.849242404953195 | 16 + 21/2 sqrt(2) | Göbel square | 921 | 3.57e-11 | Francisco Couzo; derived exact |
| 921 | 30.849242405003170 | 16 + 21/2 sqrt(2) | Göbel square | 921 | 8.57e-11 | Francisco Couzo; ct105 task |
| 964 | 31.556349186142756 | 16 + 11 sqrt(2) | Göbel square | 964 | 3.87e-11 | Francisco Couzo; local |
| 971 | 31.707106781224535 | 31 + 1/2 sqrt(2) | Göbel strip | 974 | 3.80e-11 | Francisco Couzo; derived exact |
| 972 | 31.707106781247502 | 31 + 1/2 sqrt(2) | Göbel strip | 974 | 6.10e-11 | Francisco Couzo; ct105 task |
| 973 | 31.707106781281510 | 31 + 1/2 sqrt(2) | Göbel strip | 974 | 9.50e-11 | Francisco Couzo; ct105 task |
| 974 | 31.707106781226721 | 31 + 1/2 sqrt(2) | Göbel strip | 974 | 4.02e-11 | Francisco Couzo; ct105 task |

### record's current beyond-horizon rows (main)

40 rows: 2 above, 0 equal, 38 below.
Below by 1.70e-02 to 6.47e-01.

| n | Side, rounded up | Göbel's construction | Family | From count | Above by | Row |
| --- | --- | --- | --- | --- | --- | --- |
| 369 | 19.740417287556077 | 19 + 1/2 sqrt(2) | Göbel strip | 369 | 3.33e-02 | couzo-extended-range-reports-2026-10-08 (print) |
| 376 | 19.904068025746006 | 10 + 7 sqrt(2) | Göbel square | 376 | 4.57e-03 | couzo-certificates-2026-10-13 |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
