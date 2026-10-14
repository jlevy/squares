# PI reading (2026-09-10 17:40) on fast30_k5_16_interior_Y0191: the TL(1,0) meeter pair (cells 19 and 18)
"I'm not sure this meeter pair for TL10 is valid. Is the geo pre-check ensuring that there are options with enough
distance between them? These look like they'd be close to the one unit limit."

Numbers: cell-19 hull [2.163,2.226]x[2.80,3.21], cell-18 hull [2.226,2.586]x[2.244,2.597]; farthest corners
(2.163,3.21)-(2.586,2.244) at distance 1.056 -> CN passes by 0.056, A1 by dy 0.97.  Upright the pair collides
(dy < 1, x overlap 0.42); the only separation at 1.056 is both squares tilted ~23 deg (face normal along the centre
line at 66.6 deg) with 0.056 clearance, and the upper square then reaches 3.867 against the wall 3.877.

REQUEST for stage 0 (A202): run the pair table on the surviving PIECES (sub-rect x tilt bin), not the cell hulls:
 (a) CN per piece pair (max distance of the two sub-rects >= 1);
 (b) the separating-axis bound with the tilt bins: separation along a normal of piece 1 at angle phi in its bin needs
     max over the two sub-rects of |cos(phi) dx + sin(phi) dy| >= 1/2 + w2(phi - theta2) with w2 = (|cos|+|sin|)/2
     minimised over theta2 in piece 2's bin (and symmetrically); no phi in either bin => the piece pair is EXCLUDED;
 (c) a slot's demand-2 pair must be met by two PIECE-compatible options -- the count's witness must name pieces.
This is closed-form (microseconds per pair) and would settle pairs like this one without A201's bisection.
Keep A201's exact test as the fallback for pairs that survive (b).

## Coordinator grid check (17:50), witness hulls from f30_k5_16_interior_Y0191_g1_s0.json
cell 14 [2.154,2.226]x[2.80,3.23] and cell 18 [2.226,2.658]^2, poses inside the container, off the pins and MEETING
the TL(1,0) box [1.0,2.04]x[2.852,3.877], 37 tilts each: 1,034 x 2,824 admissible poses, 0 disjoint pairs.
=> the PI is right; CN on hulls passes (1.12) only because the far corners are not meeting poses.  Rule for stage 0:
a slot's two meeters are tested as a pair over their MEETING pieces (options), never over cell hulls.
