---
type: is
id: is-01m4kave1ry14781fh7qhx9sgw
title: "Intake 2026-10-10 evening reads: wand125 27ed168 (8 commits), Guzhou0806 71c97d0, evand 76a529b, franciscouzo 3ef7634, squarepacker c6df2f4"
kind: task
status: open
priority: 2
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T16:38:01.528Z
updated_at: 2026-10-10T16:53:25.348Z
---
The 16:40Z sweep: wand125/square-packing has 8 commits past 22a23c8 (2026-10-10 to 10-11; newest drops the archived n = 11 density from the best-certificate table); Guzhou0806/n40-square-packing 71c97d0 (#485 follow-up); evand/square-packing 76a529b (#489); franciscouzo/square-packing 3ef7634 (#488); squarepacker/k2-minus-c-upper c6df2f4 (README DOI only). Read each: an import bead for any new result, else a read in intake-watch.yaml.

## Notes

2026-10-10 (lane report, sweep run 16:40:08 UTC at b650bc09d; exit 1, 8 items need an owner, 3 sources not checked). Read every commit past the last read in bare blob-filtered clones; no source code run.

- wand125/square-packing 22a23c8..27ed168 (8 commits, all 10 Oct UTC): three new lower-bound certificates the record lacks, no issue, no bead. a9f76c3 mixed_n122_L1126: s(122) >= 563/50 = 11.26 (linear, 201 angles, unified_linear_verify.cpp sha 0249726a, mass 12199999/100000, so s(N) >= 11.26 for N >= 122; raises reported 122-125 from Green 11.22928087555 and 126 from Nagamochi 11.24695076595; author replay 7h41m at 3 workers; asset 6443eae0, 31,784,537 B). 36b85b9 mixed_n28_L57425: s(28) >= 2297/400 (check2, 2073 dirs; +3/400 over T-107, +1/400 over #446's 287/50; asset 7d0f9107). ff9f269 mixed_n30_L58925: s(30) >= 2357/400 (check2, 2073 dirs; +9/1000 over T-109; asset 0d11fe05). Release asset digests match each ASSET.json. The other five commits are README-only; every other value in the regenerated claims table is held, below the record, or owned by think-ndvg / think-r333. Proposed: two new beads (n28+n30 check2; n122 linear) and two reads naming them.
- Guzhou0806/n40-square-packing 71c97d0 (parent e5abeb4, T-133's pin): the #485 follow-up, s(40) > 1340000/199529, release n40-continuous-1340000-199529-20261010 (ZIP 78d693ae). Owned by think-xms6; read proposed naming it.
- evand/square-packing 799be37..76a529b (9 commits): Hunt 3 (#489, pin c013f43) owned by think-xm4h. hunt3_n305.cert's side equals Couzo 3ef7634 n305.cert exactly (author dropped it for #488). Rest is packer tooling and notes. Read proposed naming think-xm4h.
- franciscouzo/square-packing 9bf90e7..3ef7634 (#488, think-6uv7): beyond the six, n303.cert drops to 17.9173656753 (7.83e-5 below #476's, above SQUISH #481's 17.9130654627; unrequested, for think-6uv7's triage), and beyond-horizon n338 (-1.48e-3) and n340 (-4.67e-5) for think-1545. Two reads proposed.
- squarepacker/k2-minus-c-upper c6df2f4: one README line (v1.1 DOI 10.5281/zenodo.23278927). Read proposed, nothing to import.
- #485 comment 6098734391: proposed result s40-continuous-pose, queued, bead think-xms6; read_through to 2026-10-10T14:50:00Z; think-xms6 added to beads.
Proposed rows validated against intake-watch.schema.yaml and the #485 change against result-requests.schema.yaml with jsonschema on scratch copies; no tracked file written.
