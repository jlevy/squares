---
type: is
id: is-01m29f3zcv8kfcf70ra7fpkd1j
title: "[epic] Publish the workbench at /workbench/"
kind: epic
status: open
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
child_order_hints:
  - is-01m29f4y1r8mb8cae7ye4xv084
  - is-01m29f4yh0z5hdhnyeeqfm3dxj
  - is-01m29f4yy9ppm258n8yxd8910s
  - is-01m29f4zbw0vv3xj1xbe95narx
  - is-01m2chkrt876774phbaj1pa836
created_at: 2026-09-12T00:08:47.762Z
updated_at: 2026-09-13T04:50:05.765Z
---
The pipeline exists and is correct; what stands between it and a live page is short and worth naming rather than assuming.

Already true, and none of it needs work: `build_workbench_site.py` writes `site/workbench/`; `pages.yml` builds it with `--check` at line 326, so it must reproduce itself byte for byte and pass its own self-containment check; the upload takes `packing/site` WHOLE, so the subdirectory is a URL -- the workbench lands at `/workbench/` and the explainer keeps `/`; the path filter names every input, held there by `test_the_pages_filter_covers_every_render_input`, and it gained the two asset files when the script left the HTML.

What is not yet true is the publish itself.

- **think-l6l4 (P1)** -- the Pages build shells out to a Node nobody declared. Fix it in the same branch as the merge: a first deploy that fails on an undeclared toolchain is the worst kind.
- **think-tn6s (P2)** -- the branch has to reach main. The only strictly required step, and the only reason the page is not live now.
- **think-yuvc (P3)** -- decide what the published page says while it is still a prototype. Half the banner's text is already false.
- **think-9x0m (P4)** -- nothing checks the page after it deploys.

Measured today: the built page is sha256 84edbbf9, 4.4 MB, reproducible -- `--check` rebuilt it from scratch in 34 s and got the same bytes.
