---
type: is
id: is-01m1b297ydh4ahazqwk4mx6hqq
title: "Lane A1: machine-check Bentz 2010 m=4 -- s(13)=4 as the first machine-verified published proof"
kind: task
status: in_progress
priority: 1
version: 7
spec_path: packing/campaign/explorations/X-010-two-lanes-two-ladders.md
labels:
  - x-010
  - lane-a
dependencies:
  - type: blocks
    target: is-01m1b29rfxaxq8g3nbt23wwgre
created_at: 2026-08-31T04:47:15.916Z
updated_at: 2026-08-31T09:22:53.365Z
---
Section 3 of bentz-2010-optimal-packings-13-and-46.md (~126 transcript lines, two subsections: non-adjacent and adjacent corner-restricted boxes) is the smallest published proof on the m^2-3 line. Encode its resources and forcing steps in the A0 instrument; every failed step gets the escaping-pose falsifier (think-yrvm) before any repair is invented -- H-033's discipline. Either outcome is a result: the first machine-verified proof of a published s(n) value, or a printed gap found and repaired (T-4 precedent; the audit record is one exact gap in Stromquist, four defects in El Moumni). Exit: replayable certificate, or a typed gap report with the escaping pose. X-010 Lane A rung 1.

## Notes

agenda-010 BC-099 (block 3, after the checkpoint).

2026-08-31 session-053: Theorem 8 (s(46)=7) machine-certified as printed — cases/bentz46, 92 exact cells over Q(sqrt2,sqrt3), Lemma 5 threshold bound 0.955390, 45/45 points charged, 3.17s wall — held unresolved+needs_review per the unattended rules. The m=4 remainder, typed from the completed extraction delegation: (1) encode Section 3.1's 3x4-rectangle lemma layer first; (2) the sliding point Z is the one moving-family step and needs a new certifier premise type (a parameterized point family, not a fixed transversal); (3) Figures 2-10 are unextractable, so every m=4 tiling is reconstructed from prose the way Theorem 8's Figure 1 was; (4) candidate printed-proof gap at SA's (1.74,1) configuration where the Lemma 11 case split names no covering case — replay before believing; (5) Corollary 7 carries the known transcription hazard: derive it from Lemma 6 mechanically (H-041 discipline).

2026-08-31 session-056 (block 5): Figure 2's base configuration is machine-certified — cases/bentz13, 30 exact rational cells (4 Lemma 1 corner pentagons, 8 Lemma 4 wall rectangles, 18 Lemma 2 triangles), 16/16 charged, 0.04s — and the Lemma 10 audit found a candidate printed defect: the replacement point '(1, 1.74)' is refuted by an exact escape certificate (box side 1001/1000 at (1.46, 0.7) avoids the whole printed replacement set), while (1.74, 1) — corroborated by S_A, by 3.1's alternatives, and by being the y=x mirror the B-version delivers — is contained by the same box. Both held unresolved+needs_review; transcription annotated at Lemma 10; raw carries the same reading so paper-vs-extraction is undecidable here. Remainder: the three corrected replacement certificates (P1 (1.12,1), P2 (1.74,1), P3 (1.87,0.76)) need the margin-cell kind (cells within 1/2 of a wall are box-centre-infeasible since boxes of side > 1 sit inside the container) plus per-replacement retilings near old A; then Section 3.1's staged sets.

2026-08-31 session-056 phase 2: Lemma 10 machine-settled both ways — all three CORRECTED replacement sets certify (r1 (1.12,1): Lemma 5 quad a=22/25 b=457/500 bound 0.936340; r2 (1.74,1): margin+near cells; r3 (1.87,0.76): quad a=239/250 b=19/25 bound 0.780032), and both quads sit in exactly the Lemma-5 parameter families Bentz's Section 1 lists — strong corroboration of the corrected reading. Certifier gained subset semantics, margin cells, near cells, rational-a threshold. With the escape certificate against the printed point: refuted as printed, certified as corrected, held unresolved+needs_review. Remaining m=4 ladder: Section 3.1's staged sets (14-point/4-pair Figure 3 partial cover over 16 alternative choices, then Figure 4's 15-point sets), then Lemma 11 and 3.2's R1-R4 with the sliding point Z.
