n17 sub-pattern branch-and-bound certificate (schema n17-subpattern-bb-certificate/v1)
Written by packing/devtools/pilot_n17_subpattern_bb.py --save-certificate.

FILES
Every *.json.gz file is gzip of canonical JSON (keys sorted, separators "," and ":",
ASCII) and is named by the SHA-256 of its uncompressed bytes. The manifest names the
enclosure table ("trig") and the node chunks ("chunks", in processing order); its
"summary" gives the verdict, whether the tree is complete, and the node and leaf counts.
Every number a check uses exactly is a string "p/q" in lowest terms. A value written from
a binary64 float is that float's exact value. Integers (indices, signs) are JSON ints.

CLAIM
U = header.cap. Cell s is header.cells[s], a closed convex polygon with vertices listed
counterclockwise; edge e runs from vertex e to vertex e+1 (cyclically). The claim: no k
unit squares, square s centred in cell s, at any angles, all inside [0,U]^2, have
pairwise disjoint interiors. Angles are taken modulo pi/2 in header.root_angles, a closed
interval of width greater than pi/2. M_k = header.half_pi_multiples[k] is an enclosure
[lo, hi] of k pi/2; "pi/2-lower" is M_1 lo.

For a pair p, (i, j) = header.pairs[p] and d = c_j - c_i. The squares are disjoint iff
n(phi) . d >= g for some phi in {theta_i + k pi/2, theta_j + k pi/2 : k = 0..3}, with
n(phi) = (cos phi, sin phi), g = 1/2 + h(theta_j - theta_i), h(a) = (|cos a| + |sin a|)/2.

ENCLOSURES
trig[t] = [cos_lo, cos_hi, sin_lo, sin_hi, nx, ny] for each angle t (a key "p/q"):
cos t and sin t lie in the two intervals (mpmath.iv at 120 bits, rounded outward to
binary64); (nx, ny) is the float normal the planes at t use (any vector would do: the
check charges its distance to the enclosure). A reader can confirm the enclosures with
any rigorous sin and cos.

TREE
A node record: id, parent (null at the root), angles (per square [lo, hi]), windows
([p, lo, hi]: pair p is separated along a normal whose angle, modulo 2 pi, is in
[lo, hi]), rounds, closed (a reason, or null), and for an open node "split" and "final".
The node's region: angles in its intervals, each windowed pair separated in its window,
centres in its inherited boxes (header.root_boxes at the root, else the parent's final).
  T1 The root has header.root_angles and no windows.
  T2 A node with closed null has a split, and its children (records with parent = id):
     "angle" [s, a]: two children equal to the node except square s's interval, which is
     [lo, a] and [a, hi], with lo <= a <= hi.
     "pair" [p, W]: one child per window in W, equal to the node except pair p's window,
     which is that window; covering is checked by P4.
  T3 A node with closed not null has no children; summary.complete is true and every
     record is closed or split. Then every pose of the root lies in a closed leaf.

ROUNDS (a node's rounds in order; round r relaxes over boxes B_r = "boxes")
Boxes are [xl, xh, yl, yh] per square. A reader may keep its own exact boxes and only
check that each recorded box contains them; every check below gets easier on smaller
boxes, and every recomputed quantity below is at least as tight in exact arithmetic as
the outward float it replaces.
  B1 Round 0: from the inherited boxes, for square s with angle [a, b]: h_lo = 1/2 if
     b - a >= pi/2-lower or [a, b] meets some M_k; otherwise the larger of 1/2 and
     min over t in {a, b} of (|cos t| lower + |sin t| lower)/2 from trig (h is concave
     between multiples of pi/2). Intersect with [h_lo, U - h_lo]^2, then with the cell
     (exact clipping), take the bounding box; B_0 contains it. closed "cell" with no
     rounds means this is empty for some square.
  B2 "next" is B_{r+1}: the box after the round's "bounds", clipped to the cells as in B1.

PAIRS IN A ROUND (for each pair listed in the round's "pairs")
Dx = [xj_lo - xi_hi, xj_hi - xi_lo] and Dy likewise from B_r. With angle intervals
[ai, bi] and [aj, bj]:
  P1 g_lo = 1 if aj <= bi and ai <= bj, or bj - ai - (aj - bi) >= pi/2-lower, or
     [aj - bi, bj - ai] meets some M_k. Otherwise g_lo = max(1, 1/2 + min of h at
     aj - bi and at bj - ai), each h bounded below as in B1 from enclosures of cos and
     sin of the difference: cos(p - q) = cos p cos q + sin p sin q and
     sin(p - q) = sin p cos q - cos p sin q in interval arithmetic on trig.
  P2 "pairs"[p] lists pieces [lo, hi, m] with lo <= m <= hi. For each family [a, b] in
     {[ai, bi], [aj, bj]} and k = 0..3, the set {t + k pi/2 : t in [a, b]} meet the
     pair's window (modulo 2 pi; no window means all angles) lies in the union of the
     pieces' [lo, hi] (modulo 2 pi).
  P3 Planes. eps(t) = max(cos_hi - cos_lo, sin_hi - sin_lo) and
     E = max|Dx| + max|Dy|. A plane is nbar . d >= r with nbar = (nx, ny) of trig at its
     angle. If hi - lo < pi/2-lower the piece has three planes, at lo, hi and m, with
     base right sides g_lo, g_lo and g_lo (1 - x^2/2), x = max(m - lo, hi - m), and
     r = base - eps(angle) E. Lemma (module docstring): every d with n(phi) . d >= g for
     some phi in [lo, hi] satisfies one of n(lo) . d >= g, n(hi) . d >= g,
     n(m) . d >= g cos x. Otherwise the piece has one plane at m with
     r = g_lo - 2 tau (S + tau D) - eps(m) E, tau = max(m - lo, hi - m)/2,
     S >= max over the d-box and the enclosure at m of |-sin(m) dx + cos(m) dy|,
     D >= max |d| over the d-box. A plane is impossible when max over the d-box of
     nbar . d < r, or (three-plane case) when max over the d-box and the enclosure at
     its angle of n . d < base.
  P4 For a "pair" split [p, W] (made on the last round): every piece of pair p lies in a
     window of W (modulo 2 pi) or has every plane impossible.

CLOSURES AND ROWS
  C1 "closed_pair" [p, "disc"]: max |d|^2 over the d-box < 1. [p, "pair"]: every plane
     of every piece of p is impossible.
  C2 Row ["c", s, e]: a x_s + b y_s <= c for edge e of cell s from (x0, y0) to (x1, y1),
     a = y1 - y0, b = x0 - x1, c = a x0 + b y0. Row ["u", t]: cuts[t] = [p, ux, uy, v]
     reads ux (x_j - x_i) + uy (y_j - y_i) >= v, that is
     ux x_i + uy y_i - ux x_j - uy y_j <= -v. It is valid when v <= min over every
     possible plane of p (P3) of min over the d-box meet the plane of u . d.
  C3 closed "lp": the last round's "farkas" [[row, y], ...] with y >= 0 satisfies
     min over z in B_r of sum y (a_row . z - b_row) > 0, so the round's region is empty.
  C4 "bounds", in order: [col, sign, value, [[row, y], ...]], col = 2 s + axis (axis 0
     is x). sign z_col >= value holds when value <= min over the current box of
     (sign e_col + sum y a_row) . z - sum y b_row. Then the current box's lower bound
     (sign 1) becomes value, or its upper bound (sign -1) becomes -value. The current box
     starts as B_r.
  C5 closed "obbt": "emptied" is "bounds" (some lower bound exceeds its upper bound) or
     "cell" (a tightened box misses its cell).

This certificate's manifest: 340492bddf2674b70e4403e15c13793c224a5dfa4d428a5e1834da546ee6a9dc.json.gz
