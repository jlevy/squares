---
type: is
id: is-01m28p7h39vcykq99dgjmvwv98
title: "[epic] Phase 6: the workbench stops being a prototype"
kind: epic
status: open
priority: 1
version: 13
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
child_order_hints:
  - is-01m292qr3ayhe4zxrnmcjz9vb4
  - is-01m292qrjevy600v0j0h1h5zp3
  - is-01m292qs1re33kvh0tvnm6xctd
  - is-01m292rgtadddppyrzfkjz1sn4
  - is-01m292rh6bg0nxsd2nyv4q6x99
  - is-01m2945b7wpg8ypvt3n2ttk1et
  - is-01m2945bnpzyf0jkgv9w3mcjcv
  - is-01m298nrfg4gwvw04jtpypb6b5
  - is-01m298ppyd1stv2dqe2g5b40b9
  - is-01m299tcsrh44b8n8m1c6jpgcb
created_at: 2026-09-11T16:53:49.786Z
updated_at: 2026-09-11T22:36:10.935Z
---
The page carries a banner calling itself a prototype and the banner is honest: a retained spike, excluded from the lint floor, run by hand, drawing with its own copy of the palette. It is also the thing the owner uses and the thing the video is captured from, and those two facts cannot both keep being true.

Five chunks, each landing on its own, in this order. The banner comes off LAST, because it is what makes the current state honest.

A. One source for the palette
B. The floors (ruff, BasedPyright, and a decision about the JavaScript)
C. The gates run where gates run
D. It reads the contracts
E. It lives where the code lives, and the banner comes off

## Notes

The conversion now has its own plan spec: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md, which carries the measured sizings, the five chunks with disjoint owned-file lists, the risk table and the two open questions.

The chunks gained one. The owner's rule -- 'you should not embed JavaScript or HTML inside of Python' -- is now Phase 6D (think-7f3p) rather than an option inside 6B, and it is the chunk no auto-fix touches. Order: 6D C1 (the page's script leaves the HTML), then 6D C2 (the checkers' probes leave Python) and 6B (the Python floors) and the instruments in parallel, then 6A (palette from sqpack, which edits the extracted script), then 6C and 6E last with the banner.

Not a chunk, but landed on the way: three defects the owner found on the built page, all fixed and measured -- think-lkbk (the lower numeral in the panel's serif), think-uy41 (bound arrows clipped, rail ends doubling as scale ends), think-9yzq (mode switch carried the run across). One left open: think-2m96 (the first frame of every step is an invalid packing).
