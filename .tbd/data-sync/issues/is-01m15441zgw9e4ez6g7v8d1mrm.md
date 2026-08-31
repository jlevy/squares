---
type: is
id: is-01m15441zgw9e4ez6g7v8d1mrm
title: "Move the tree: docs tier to the root, the rest to packing/"
kind: task
status: closed
priority: 0
version: 7
labels: []
dependencies:
  - type: blocks
    target: is-01m15442akdex5khfn7z8hrarb
  - type: blocks
    target: is-01m15442nxmwj32dq2kgrxgk4t
  - type: blocks
    target: is-01m1544315q4s96kgexe71qybx
  - type: blocks
    target: is-01m15443cdzm4pyh7nkgbwgrd8
  - type: blocks
    target: is-01m15444eff52e4tcfv8qthya7
parent_id: is-01m15219m6eh8fww5pm9sc2sqd
created_at: 2026-08-28T21:23:56.527Z
updated_at: 2026-08-28T23:27:56.774Z
closed_at: 2026-08-28T23:27:56.774Z
close_reason: Landed on refactor/hoist-packing-to-root
resolution: null
duplicate_of: null
---
One commit, `git mv` only, no content edits. The tree is knowingly broken at this commit
and repaired by the ones after it, inside a single PR.

Rename-only matters: Git records the renames, `git log --follow` keeps working on 1,160
files, and the review diff stays readable with `--find-renames`.

Steps:

1. Delete the root `README.md`. This is the one and only name collision, and the merged
   replacement is built later in the epic.
2. `git mv` the docs tier out to the root: `README.md`, `SYNOPSIS.md`, `TUTORIAL.md`,
   `conventions.md`, `development.md`, `defects.md`, `docs/`.
3. `git mv explorations/packing` to `packing/` for the rest: `atlas/`, `benchmarks/`,
   `campaign/`, `cases/`, `devtools/`, `frankensim-probe/`, `frontier/`, `golden/`,
   `resources/`, `src/`, `sqsearch/`, `tests/`, `witnesses/`, `defects.yaml`,
   `defects.schema.yaml`, `pyproject.toml`, `uv.lock`, `.python-version`.
4. Confirm `explorations/` is gone.

Watch the dotfile: `.python-version` is easy to miss with a glob and uv will silently
resolve a different interpreter without it.
