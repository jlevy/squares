---
type: is
id: is-01m29f4y1r8mb8cae7ye4xv084
title: "P1: the Pages build depends on a Node nobody declared"
kind: bug
status: open
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
  - workbench-phase-2
dependencies:
  - type: blocks
    target: is-01m2cm03rtrjcg98ejb9y56jn6
  - type: blocks
    target: is-01m28p88qyq83eek30pja3np54
parent_id: is-01m29f3zcv8kfcf70ra7fpkd1j
created_at: 2026-09-12T00:09:19.153Z
updated_at: 2026-09-13T05:43:46.878Z
---
`pages.yml`'s build job pins Python to 3.14.7 and uv to 0.12.8, and says nothing about Node. But the workbench's build shells out to it: `build_candidate.py:1152` runs `["node", entry]` to render about a thousand KaTeX expressions in one call, and `build_workbench_site.py` is what invokes that.

It works today only because `ubuntu-latest` happens to ship a Node. That is a runner-image detail, not a declaration: a change to the image, or a KaTeX upgrade wanting a newer runtime, breaks the publish with no warning and an error that will read as a KaTeX problem rather than a toolchain one.

Fix: `actions/setup-node@48b55a011bda9f5d6aeb4c2d9c7362e8dae4041e # v6.4.0` with `node-version: "24.18.0"` in the build job of `pages.yml`, matching what `packing-validation.yml` and the vendored kpress already pin, so the repository has one answer to 'which Node'.

No `npm ci` is needed there: the Pages build needs the Node runtime, not the pinned tools. Biome and tsc run in `packing-validation.yml`, which is the right separation -- Pages builds, validation checks.
