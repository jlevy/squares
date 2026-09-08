| kind | pairs | mean of max displacement | max of max displacement | pairs with any rotation | mean crossings |
| --- | ---: | ---: | ---: | ---: | ---: |
| prefix | 160 | 0.000 | 0.000 | 0 | 0.0 |
| shared-picture | 5 | 0.000 | 0.000 | 0 | 0.0 |
| matched | 158 | 2.206 | 4.500 | 156 | 12.9 |

Pairs with max displacement under 1 unit: 174 of 323 Pairs with max displacement under 3
units: 290 of 323 Pairs with max displacement over 5 units: 0 of 323 Pairs with max
displacement over 10 units: 0 of 323

Histogram of maximum matched displacement (unit-square units), all 323 pairs:

```
   exactly 0 | 165 ########################################
    (0, 0.5) |   1 
    [0.5, 1) |   8 ##
      [1, 2) |  68 ################
      [2, 3) |  48 ############
      [3, 5) |  33 ########
      [5, 8) |   0 
     [8, 12) |   0 
 12 and over |   0 
```

Most chaotic pairs (by maximum displacement):

| pair | side | max disp | mean disp | moved >1 | rotated | crossings | blocks | moving in blocks | alone |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 256→257 | 16.000→16.536 | 4.50 | 0.56 | 25 | 84 | 20 | 6 | 177 | 1 |
| 233→234 | 15.778→15.823 | 4.49 | 0.84 | 69 | 135 | 45 | 13 | 189 | 43 |
| 227→228 | 15.571→15.609 | 4.33 | 0.69 | 61 | 121 | 34 | 15 | 199 | 25 |
| 265→266 | 16.778→16.823 | 4.21 | 0.77 | 67 | 136 | 54 | 15 | 223 | 40 |
| 237→238 | 15.914→15.940 | 3.96 | 0.76 | 27 | 108 | 24 | 16 | 224 | 12 |
| 125→126 | 11.707→11.776 | 3.95 | 0.72 | 5 | 29 | 11 | 9 | 109 | 15 |
| 302→303 | 17.887→17.931 | 3.92 | 0.79 | 46 | 134 | 32 | 17 | 275 | 26 |
| 230→231 | 15.683→15.707 | 3.86 | 0.88 | 71 | 115 | 33 | 12 | 198 | 31 |
| 231→232 | 15.707→15.778 | 3.81 | 0.91 | 70 | 115 | 38 | 13 | 223 | 7 |
| 174→175 | 13.707→13.778 | 3.77 | 0.94 | 68 | 102 | 34 | 13 | 159 | 14 |
| 170→171 | 13.536→13.571 | 3.74 | 0.70 | 42 | 90 | 13 | 14 | 130 | 30 |
| 173→174 | 13.657→13.707 | 3.72 | 0.71 | 41 | 63 | 23 | 13 | 159 | 13 |
| 269→270 | 16.906→16.941 | 3.70 | 0.92 | 111 | 120 | 63 | 16 | 227 | 41 |
| 202→203 | 14.728→14.778 | 3.70 | 0.88 | 67 | 104 | 49 | 13 | 189 | 12 |
| 203→204 | 14.778→14.823 | 3.67 | 0.90 | 68 | 119 | 42 | 15 | 159 | 42 |

Most graceful matched pairs (by maximum displacement):

| pair | side | max disp | mean disp | moved >1 | rotated | crossings | blocks | moving in blocks | alone |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 201→202 | 14.707→14.728 | 0.49 | 0.06 | 0 | 0 | 0 | 3 | 199 | 1 |
| 206→207 | 14.873→14.894 | 0.53 | 0.04 | 0 | 35 | 0 | 7 | 203 | 2 |
| 151→152 | 12.823→12.831 | 0.53 | 0.04 | 0 | 27 | 0 | 5 | 26 | 2 |
| 176→177 | 13.823→13.823 | 0.55 | 0.01 | 0 | 29 | 0 | 4 | 28 | 1 |
| 236→237 | 15.876→15.914 | 0.58 | 0.08 | 0 | 28 | 0 | 13 | 234 | 1 |
| 5→6 | 2.707→3.000 | 0.77 | 0.39 | 0 | 1 | 0 | 0 | 0 | 4 |
| 181→182 | 13.957→13.974 | 0.79 | 0.06 | 0 | 72 | 0 | 9 | 154 | 4 |
| 107→108 | 10.847→10.926 | 0.81 | 0.13 | 0 | 24 | 0 | 4 | 105 | 1 |
| 204→205 | 14.823→14.824 | 0.83 | 0.08 | 0 | 33 | 0 | 4 | 32 | 2 |
| 4→5 | 2.000→2.707 | 1.00 | 0.60 | 0 | 0 | 0 | 0 | 0 | 3 |
| 9→10 | 3.000→3.707 | 1.00 | 0.58 | 0 | 1 | 0 | 2 | 8 | 0 |
| 55→56 | 7.946→8.000 | 1.01 | 0.44 | 1 | 18 | 0 | 7 | 44 | 8 |

Largest matched rotation count: 260→261 (159 squares rotate) Largest maximum
displacement: 256→257 (4.50 units)

Block matching over the 158 assignment pairs (clusters within 4 degrees and a gap of
0.2, residual tolerance 0.35, discount 0.1):

- Moving squares carried by a block: 20582 of 22757 (90.4%)
- Pairs whose moving squares are at least half in blocks: 155 of 158; at least nine in
  ten: 83; all of them: 13
- Pairs where some moving square fell back to a square-level move: 145 of 158
- Blocks per pair: mean 9.3, max 18; clusters per frame (from, to): mean 5.7, 5.7
- Residual after the block transform, over block members: mean 0.020 units, max 0.350;
  pairs with a max residual over 0.2: 76

New-square rule: lowest total matching cost after removal from n+1, then fewest
full-side contacts, then highest position (y, then x).

- decided by lowest cost: 157 pairs
- decided by lowest cost, fewest contacts, highest position: 1 pairs
- choice differs from revision 4’s leftover: 134 of 158 pairs
- tie sets larger than one: 1 pairs, the largest 2 candidates

Arrival overlap census (the new square at its final pose against the squares of n before
they move): 158 of 323 pairs, 588 squares covered in all; max 6 in one pair; mean over
the overlapping pairs 3.72

Full 1..324 run at dwell 1.0 s, move 1.4 s, settle 0.4 s: 905.4 s = 15.1 min (323
transitions plus a closing dwell) Per-kind schedule, static appends at dwell 0.5 s, move
0.0 s, settle 0.4 s (no move): 158 × 2.8 + 165 × 0.9 + 1.0 = 591.9 s = 9.9 min Per-kind
schedule, static appends at dwell 0.5 s, move 0.4 s, settle 0.3 s (short move): 158 ×
2.8 + 165 × 1.2 + 1.0 = 641.4 s = 10.7 min

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
