---
type: is
id: is-01m15b68m8zw92zf42gy1xvjv0
title: Merge the two READMEs and repoint check_readme
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m15219m6eh8fww5pm9sc2sqd
created_at: 2026-08-28T23:27:28.903Z
updated_at: 2026-08-28T23:27:31.365Z
closed_at: 2026-08-28T23:27:31.364Z
close_reason: Landed in the reorg branch
resolution: null
duplicate_of: null
---
The root README becomes the front door (purpose, atlas graphic, inventory table, Start Here) followed by the gate-checked content it already had.

check_readme follows it: README/SYNOPSIS/RESEARCH resolve from REPO, the layout tree is found by a branch marker instead of the directory name it opens with (the thing that made it fragile under exactly this move), and the tree now draws the repository -- including the six new root entries AGENTS.md, CLAUDE.md, Makefile, lefthook.yml, package.json and package-lock.json.
