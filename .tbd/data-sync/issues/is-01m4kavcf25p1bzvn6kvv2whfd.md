---
type: is
id: is-01m4kavcf25p1bzvn6kvv2whfd
title: "Import Guzhou0806: s(40) > 1340000/199529 by a continuous-pose kernel on rect_n40_L67 (#485 follow-up)"
kind: task
status: open
priority: 1
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T16:37:59.906Z
updated_at: 2026-10-10T16:37:59.906Z
---
Comment https://github.com/jlevy/squares/issues/485#issuecomment-6098734391 (2026-10-10T14:50:00Z). s(40) > 1340000/199529 = 6.715815746…, unrestricted, raising T-133's 335427/50000 by 72586117/9976450000. New continuous-pose kernel: 43 closed slabs in t = tan(theta/2) covering [10^-6, 83/200] for squares of side B = 199529/200000 with a t-dependent legal centre domain, a separate horizontal certificate at side A = 997643/1000000 for t in [0, 10^-6], threshold tau = 4999/5000, 40 tau - 3999/100 = 1/500. Outward-rounded binary64 intervals, a concave-section integral lower bound, translation-derivative bounds; two frozen C++ kernels. Pin Guzhou0806/n40-square-packing 71c97d07553d7d5ff5c5c82f0c9d1c75a150a4e3, release n40-continuous-1340000-199529-20261010, ZIP SHA-256 78d693ae5bd08cc3065348c6593c2bec36412bebe48eb2f744786dc115bba26f; local 510.96 s at 4 workers, CI 983.95 s. wand125's review covers 6.70854 only. Needs a Fable max review of the new kernel's soundness before any replay counts.
