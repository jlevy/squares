---
type: is
id: is-01m28p7h39vcykq99dgjmvwv98
title: Ship a clean standalone packing workbench
kind: epic
status: open
priority: 1
version: 39
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
  - is-01m29f3zcv8kfcf70ra7fpkd1j
  - is-01m29fmp137m9trd5gbc1x1ryg
  - is-01m29fnn377jv7kmkek75ekkt3
  - is-01m29g1hhddhwsqfr0fz4r175e
  - is-01m29gkhfkt1sv50caesct8q0x
  - is-01m29gs5z48h1ztmc5h659hd6b
  - is-01m29hy2bcnwej20dfv7c9ydrp
  - is-01m2chae7ahgc8nf7vb33wkhj7
  - is-01m2chag118qjnczfj2zbrtx3b
  - is-01m2chahf57z4w9tj5gehbs0td
  - is-01m2chakgrn8keadss1jcs401b
  - is-01m2chkpvbrqv1h9nttp8rrtqb
  - is-01m2chr5bvzvbmzhsph4jcnrf9
  - is-01m2chr65cx0jhfd1gsmx3r31y
  - is-01m2chvkkmv158bkmqg9444jn8
  - is-01m2cj9hf5v77se0yyzbr5jqd6
  - is-01m2ckve44dr18jrbqajj3tjpw
  - is-01m2ckzsvafkecaad6hh20gbvz
  - is-01m2ckztpy58ydg71fkvwz7f0v
  - is-01m2ckzvnsawqg79z9ybspc3yt
  - is-01m2cm03rtrjcg98ejb9y56jn6
  - is-01m2b7n9tyq13n0zw4tkq4rfss
  - is-01m2b7na7psnnn1j62g1yjdtta
  - is-01m2cmf6vy26q99h0pa25g518w
created_at: 2026-09-11T16:53:49.786Z
updated_at: 2026-09-13T05:40:02.043Z
---
Governing source of truth: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md. Deliver a single top-level packages/workbench containing all application, core simulation, illustration timeline, IO, tests/probes and workbench-specific tools, with Pack, Animate and later Search using the same typed run/receipt contracts. The architecture review is evidence and resolution tracking, not a second roadmap. Supporting annealing, shared-contract and video plans supply detail.

Phases 0-2 refresh and inventory, establish an immediately strict package shell, repair evidence/strategy/benchmark/seed semantics and quality gates. Phase 3 consolidates data, browser/Node kernel, timeline, app and build/capture tools. Phase 4 completes arbitrary-n Pack, cleans obsolete consumers, documents operation, and validates a safe Pack/Animate release. Phase 5 completes experimental strategies, Search and calibration, with an end-to-end acceptance checkpoint. Search is deferred by dependencies, not dropped. Optional Python/Rust services and new mathematical campaigns are separate work. Existing palette/source separation and initial browser-floor adoption are retained accomplishments; legacy bead status is reconciled under think-a9gt.

## Notes

The conversion now has its own plan spec: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md, which carries the measured sizings, the five chunks with disjoint owned-file lists, the risk table and the two open questions.

The chunks gained one. The owner's rule -- 'you should not embed JavaScript or HTML inside of Python' -- is now Phase 6D (think-7f3p) rather than an option inside 6B, and it is the chunk no auto-fix touches. Order: 6D C1 (the page's script leaves the HTML), then 6D C2 (the checkers' probes leave Python) and 6B (the Python floors) and the instruments in parallel, then 6A (palette from sqpack, which edits the extracted script), then 6C and 6E last with the banner.

Not a chunk, but landed on the way: three defects the owner found on the built page, all fixed and measured -- think-lkbk (the lower numeral in the panel's serif), think-uy41 (bound arrows clipped, rail ends doubling as scale ends), think-9yzq (mode switch carried the run across). One left open: think-2m96 (the first frame of every step is an invalid packing).
