---
type: is
id: is-01m15444eff52e4tcfv8qthya7
title: Repoint repo-name URLs from thinking-scratchpad to squares
kind: chore
status: closed
priority: 2
version: 3
labels: []
dependencies:
  - type: blocks
    target: is-01m15444sqtndc8k38h7bd5k6w
parent_id: is-01m15219m6eh8fww5pm9sc2sqd
created_at: 2026-08-28T21:23:59.054Z
updated_at: 2026-08-28T23:27:56.825Z
closed_at: 2026-08-28T23:27:56.825Z
close_reason: Landed on refactor/hoist-packing-to-root
resolution: null
duplicate_of: null
---
The repository is now `jlevy/squares`. Four frontier schemas carry `$id:` URLs built on
the old name, for example:

    $id: https://github.com/jlevy/thinking-scratchpad/explorations/packing/frontier/strategy-catalogue.schema.yaml

Both halves are stale: the repository name and the path. Files:
`strategy-catalogue.schema.yaml`, `source-availability.schema.yaml`,
`asymptotic-waste-bounds.schema.yaml`, and the prospective atlas seed schema.

Nothing dereferences these today, so this is correctness of metadata rather than a
runtime break. Doing it inside this epic means the URLs are rewritten once instead of
twice.

Also here: `packing/frontier/source-availability.yaml:22` `archive:` field, and the
`Run from explorations/packing` text in `packing/src/sqpack/project.py:51`.

Separately worth raising with the user: `.tbd/config.yml` still has `id_prefix: think`,
so beads read `think-xxxx` in a repository called `squares`. Changing it is not part of
this epic and would not renumber existing beads.
