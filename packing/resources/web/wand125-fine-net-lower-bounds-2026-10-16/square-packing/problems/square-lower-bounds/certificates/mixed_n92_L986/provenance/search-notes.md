# Search provenance (not trusted by the checker)

Record of the search as it was run (rewritten 2026-10-16; the earlier text was a generic description). Numerical only: floating-point LP and sampling; nothing here is an input to the check.

## Source

The published certificate `mixed_n73_L8813` (n = 73, L0 = 8.813, 462 rectangles in its D4 representative), lifted to n = 92, L = 9.86 (d = L - L0 = 1.047).

## Lift

The start measure was produced by the structured-measure generator in source mode at the new side L. Its column dictionary held the full-container rectangle; every rectangle of the source certificate with positive mass, mapped to side L in three ways (uniform scaling by L/L0; insertion of a central cross of width d = L - L0, i.e. coordinates above L0/2 shifted by d in both axes; a smooth quintic stretch of the interior that keeps a wall layer fixed); and 24 phase-shifted families of rectangle bands. The source masses were not kept: an LP under the budget n with core side B re-solved every weight on sampled poses (160 rounds of sampling and refinement), giving a numerical start measure.

## Net rounds

Net rounds then followed, as for our other fine-net certificates: each round solves the LP on the retained rows, screens all 201 directions of the declared half-angle net (collecting up to 32 separated low-coverage witnesses per direction) and adds the witnesses as rows. After each round the rationalised candidate was checked exactly at all 201 directions with the verifier in check2/src (without the control); the first candidate that passed is the one in this bundle, and the check with the negative control (check2/) was run on it.

## This run

Generation (about 70 minutes) and the first 12 net rounds (about 13 hours) ran on a 16-vCPU x86-64 cloud virtual machine. The run was then moved: the saved state of round 12 was copied to a desktop workstation (x86-64, Ubuntu under WSL2) shared with other jobs, where it continued after one restart; the candidate of the 5th round there (17th overall, about 3.3 hours) passed the exact check. Our earlier certificate n92 L=9.813 was lifted from the same source with d = 1; it was not used as a source here.
