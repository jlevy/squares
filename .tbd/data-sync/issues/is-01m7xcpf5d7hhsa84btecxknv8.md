---
type: is
id: is-01m7xcpf5d7hhsa84btecxknv8
title: "Import JoostdeWinter: s(20) > 99/20 = 4.95, a raised lower bound by Bentz's 22 marks and Mira Cult's pose exclusion (lower_n20/ at 3a51303) (#1055)"
kind: task
status: in_progress
priority: 1
version: 5
delegate: codex-intake-1119-01a1fb
labels:
  - result-import
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-20T21:09:45.773Z
updated_at: 2026-11-21T09:21:23.695Z
started_at: 2026-11-20T22:43:14.476Z
---
Issue jlevy/squares#1055 (Joost de Winter, 2026-11-20T19:58:09Z): s(20) > 99/20 = 4.95, against the case page's 393/80 = 4.9125 (Hosono) and the 4.912808 of his own #1039 and #1042, which the issue says this supersedes at 20.

Source: lower_n20/ of JoostdeWinter/square-packing at 3a5130340b0882e72e9d04ad2419b0437cae99aa (19:37:39Z on 20 November; nine files: PROOF.md, README.md, SHA256SUMS, n20.py, n20_certificate.json, n20_orientation_intervals.json, n20_receipt.json, n20_verdicts.json, replay_log.txt). No packet retains it; intake-watch.yaml holds it for this bead (lane rec1120).

Argument as the issue states it: 22 marks of Figure 3 of Bentz (arXiv:1606.03746) scaled by 99/100 on [0, 4.95]^2; two exact sweeps show every unit square holds a mark in its concentric square of side 1 - 1/100000; nearest-mark assignment leaves two marks unassigned; 231 pairs fall into 67 classes under two reflections; Mira Cult's exact pose-exclusion program (Mira-Cult/math at 78bec6a) excludes 60 classes directly and the other 7 in 15 terminal branches, 75 terminal regions in all (4 C1, 70 F1, 1 F2; verdict SHA-256 bd1877fc...3048). `python3 n20.py` downloads the pinned upstream sources and replays; about two minutes on two cores by the author's log.

Shared premise the issue declares: the exclusion step rests on Mira Cult's code, itself under review in #1050 (import think-8x11, review think-5jr0). The cover sweeps and the reduction to 67 classes are stated independent of it.

Owed: stage 1 triage (the entry in result-requests.yaml is triage: pending), retention at the pin, replay with controls, a blind stage 4 review (a lower bound by case exclusion on borrowed software), registration at the rungs the evidence supports, and the relation to the #1039/#1042 rows at 20 (think-fv42). Credit as the issue asks: de Winter, using Bentz's marks and Mira Cult's exclusion software; AI tools named, not credited.

The issue got the `intake` label on 20 November (lane rec1120); no case label exists for n = 20.

## Notes

20 November 2026 intake triage. #1055 claims one strict lower bound, s(20) > 99/20, for unrestricted unit squares. Main at c3f4a59dc1 reports and verifies Hosono's 393/80 (T-233), with grid upper bound 5. The source's 4.912808 in #1039 and #1042 remains under review. The proposed bound exceeds the published lower endpoint by 0.0375 while leaving an interval of width 0.05 to the grid bound.

Pin JoostdeWinter/square-packing 3a5130340b0882e72e9d04ad2419b0437cae99aa, lower_n20/. The GitHub tree contains the proof, the two cover schedules, the exclusion tree, the producer replay and the receipt. The published receipt reports 67 vacancy classes, 75 terminal regions, a feasible 16-square control and verdict digest bd1877fc8a8348ed0f36a18f5827371f6ef0732828ac55dac4461aeb258f3048. These are source statements. The author reports two minutes on two cores, about four CPU-minutes for the producer replay. The independent review still needs pricing from a trial, with its own cover and case-reduction checks and an audit of the scope and premises of the shared pose-exclusion kernel at Mira-Cult/math 78bec6aacebf304d942a9225e16c2f18165778ff. Keep a producer rerun distinct from independent confirmation. No repository-maintained end-to-end checker for this exact combined argument was established during triage.

The source is pinned and the issue already carries intake. Retention and the validation environment are pending. Draft acknowledgment for after the triage PR merges: Thank you for sending the strict bound at 20. We pinned lower_n20 at 3a51303 and will check the cover, vacancy classes and terminal exclusions, including the premises shared with #1050.

21 November UTC triage: the #1055 source at 3a5130340b0882e72e9d04ad2419b0437cae99aa reports an improvement from the two lower lanes' 393/80 to a strict endpoint of 99/20, a gain of 3/80. Verified all eight listed SHA-256 entries in the nine-file lower_n20 packet. No producer or independent replay ran in this continuation. The proof uses Bentz's 22 marks and 20 Mira Cult replay files pinned at 78bec6aacebf304d942a9225e16c2f18165778ff. The pinned project tree lists no licence for that code, consistent with the independent #1050 review, whose own results are partial and do not decide the 20-square terminals. Record the separate basis for any public retention of the kernel. The producer driver accepts an offline --upstream directory. Before verified admission, review the covering reduction and closed cuts, predeclare controls, and replay all 75 terminals plus the feasible 16-square control. The pinned proof names 4.912808 as a private comparison, not the posted #1042 endpoint 4.91274373.

21 November scoped independent reduction review: direct arbitrary-rotation mark coverage at side 99/100 of the submitted square, injective nearest-mark ownership, 67 two-mark vacancy orbits (3 size 1, 14 size 2 and 50 size 4), and strictness by compactness conditional on terminal exclusions. Inspected only the submitted proof exposition and archived Bentz text. No producer code, terminal replay or controls run. Exact private draft: /Volumes/spud-ext2/agent-scratch/codex-intake-01a1fb-20261121/n20-reduction-review/n20-reduction-review.md. Its independent certificate audit and control plan still needs execution, including all 75 terminal exclusions.
