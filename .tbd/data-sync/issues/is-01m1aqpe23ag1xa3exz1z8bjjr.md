---
type: is
id: is-01m1aqpe23ag1xa3exz1z8bjjr
title: "BC-091: the n=90 attempt -- H-049, the squeezable 20-in-4x6 primitive"
kind: task
status: open
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-08-31T01:42:13.826Z
updated_at: 2026-10-06T08:21:54.692Z
---
Narrowed by X-009 from 31 grid cases to one finite question: does delta((4,6),20) > 0? If yes, Arslanov's decomposition gives s(90) < 10, one step past Cantrell's Feb 2025 n=110. First step is a first-party read of the decomposition constraints for m=10 (H-049 prereq).

## Notes

2026-10-06 bead review: closed think-nh1s (Agenda 018 BC-178, never launched) as a duplicate of this bead. Its protocol carries over here:

- Before measuring, amend H-049 with the planning survey's derivation. Arslanov's inequality (2), applied twice, turns a squeezable (4,6)/20 primitive into delta((6,6),30) > 0 and so s(30) < 6. That is the m = 6 instance of s(m^2 - m) = m.
- Measure the squeeze in one of two ways: fix the ten grid squares of a 2 x 5 block inside a square of side 6 - delta, or add a delta column to fixed_cell_lp.
- Run the controls first. Arslanov's (4,8)/26 must certify at delta = 0.0177702 and refuse at 0.02. The area-impossible delta = 0.42 must refuse. The 4 x 5 grid must certify at delta = 0.

The question is still open on main: s(30) is in [47/8, 6] and s(90) is in [973/100, 10] (n-030.md, n-090.md).
