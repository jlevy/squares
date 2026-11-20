---
type: is
id: is-01m7xcpf5d7hhsa84btecxknv8
title: "Import JoostdeWinter: s(20) > 99/20 = 4.95, a raised lower bound by Bentz's 22 marks and Mira Cult's pose exclusion (lower_n20/ at 3a51303) (#1055)"
kind: task
status: open
priority: 1
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
created_at: 2026-11-20T21:09:45.773Z
updated_at: 2026-11-20T21:09:45.773Z
---
Issue jlevy/squares#1055 (Joost de Winter, 2026-11-20T19:58:09Z): s(20) > 99/20 = 4.95, against the case page's 393/80 = 4.9125 (Hosono) and the 4.912808 of his own #1039 and #1042, which the issue says this supersedes at 20.

Source: lower_n20/ of JoostdeWinter/square-packing at 3a5130340b0882e72e9d04ad2419b0437cae99aa (19:37:39Z on 20 November; nine files: PROOF.md, README.md, SHA256SUMS, n20.py, n20_certificate.json, n20_orientation_intervals.json, n20_receipt.json, n20_verdicts.json, replay_log.txt). No packet retains it; intake-watch.yaml holds it for this bead (lane rec1120).

Argument as the issue states it: 22 marks of Figure 3 of Bentz (arXiv:1606.03746) scaled by 99/100 on [0, 4.95]^2; two exact sweeps show every unit square holds a mark in its concentric square of side 1 - 1/100000; nearest-mark assignment leaves two marks unassigned; 231 pairs fall into 67 classes under two reflections; Mira Cult's exact pose-exclusion program (Mira-Cult/math at 78bec6a) excludes 60 classes directly and the other 7 in 15 terminal branches, 75 terminal regions in all (4 C1, 70 F1, 1 F2; verdict SHA-256 bd1877fc...3048). `python3 n20.py` downloads the pinned upstream sources and replays; about two minutes on two cores by the author's log.

Shared premise the issue declares: the exclusion step rests on Mira Cult's code, itself under review in #1050 (import think-8x11, review think-5jr0). The cover sweeps and the reduction to 67 classes are stated independent of it.

Owed: stage 1 triage (the entry in result-requests.yaml is triage: pending), retention at the pin, replay with controls, a blind stage 4 review (a lower bound by case exclusion on borrowed software), registration at the rungs the evidence supports, and the relation to the #1039/#1042 rows at 20 (think-fv42). Credit as the issue asks: de Winter, using Bentz's marks and Mira Cult's exclusion software; AI tools named, not credited.

The issue got the `intake` label on 20 November (lane rec1120); no case label exists for n = 20.
