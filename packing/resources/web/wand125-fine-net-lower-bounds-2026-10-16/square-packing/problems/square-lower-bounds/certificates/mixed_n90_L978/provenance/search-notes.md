# Search provenance (not trusted by the checker)

Record of the search as it was run (rewritten 2026-10-16; the earlier text was a generic description). Numerical only: floating-point LP and sampling; nothing here is an input to the check.

## Source

The published certificate `mixed_n84_L9411` (n = 84, L0 = 9.411, 686 rectangles in its D4 representative), lifted to n = 90, L = 9.78 (d = L - L0 = 0.369).

## Lift

The start measure was produced by the structured-measure generator in source mode at the new side L. Its column dictionary held the full-container rectangle; every rectangle of the source certificate with positive mass, mapped to side L in three ways (uniform scaling by L/L0; insertion of a central cross of width d = L - L0, i.e. coordinates above L0/2 shifted by d in both axes; a smooth quintic stretch of the interior that keeps a wall layer fixed); and 24 phase-shifted families of rectangle bands. The source masses were not kept: an LP under the budget n with core side B re-solved every weight on sampled poses (160 rounds of sampling and refinement), giving a numerical start measure.

## Net rounds

Net rounds then followed, as for our other fine-net certificates: each round solves the LP on the retained rows, screens all 201 directions of the declared half-angle net (collecting up to 32 separated low-coverage witnesses per direction) and adds the witnesses as rows. After each round the rationalised candidate was checked exactly at all 201 directions with the verifier in check2/src (without the control); the first candidate that passed is the one in this bundle, and the check with the negative control (check2/) was run on it.

## This run

Machine: a desktop workstation (x86-64, Ubuntu under WSL2) shared with other jobs.

Generation took about 9 hours and the net rounds about 22 hours (wall clock on a shared machine). The candidate of net round 6 passed the exact check.
