---
type: is
id: is-01m68g3f8bda4are97wk6tf31k
title: Hold a project copy of 11SquaresOptimal's verification supplement before think-3i74's --full run (#850 review A2)
kind: task
status: open
priority: 3
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-10-31T08:09:32.683Z
updated_at: 2026-10-31T08:09:32.683Z
---
Review A2 of #850 (31 October 2026): the packet n11-optimality-paper-2026-10-09 pins Queuingtheorydotcom/11SquaresOptimal's verification supplement paper/eleven-squares-publication.zip at 4262f07c7723428c1725bb757ed06d0c4d28be1a by size and SHA-256 only (5,426,101 bytes, 9ece0254a4c08cb3d68bd2332f4250b935cf5b6e02ce4c1bccabbff2914fba03; 387 files, 26,360,481 bytes unpacked), as OR-18 allows. No copy the project controls holds those bytes. think-3i74's next step, the supplement's `verify.py --full` run, needs them, and an upstream history rewrite or the removal of paper/ would leave the pin naming bytes nobody holds.

Do one of: publish the zip as a hosted object with a manifest (development.md, Publishing Hosted Data) when think-3i74 schedules the run; or, at the latest when it runs, re-fetch the zip at 4262f07, compare it with the pinned digest before extracting anything, and record the comparison in the run's receipt.

Done when: a project-held copy exists with its manifest, or the run's receipt records the re-fetch and the digest match.
blocked_on: think-3i74
