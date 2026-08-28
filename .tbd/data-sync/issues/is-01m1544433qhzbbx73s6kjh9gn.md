---
type: is
id: is-01m1544433qhzbbx73s6kjh9gn
title: Merge the two READMEs and repair check_readme.py
kind: task
status: open
priority: 1
version: 2
labels: []
dependencies:
  - type: blocks
    target: is-01m15444sqtndc8k38h7bd5k6w
parent_id: is-01m15219m6eh8fww5pm9sc2sqd
created_at: 2026-08-28T21:23:58.690Z
updated_at: 2026-08-28T21:24:13.268Z
---
There are two READMEs and after the move there can be only one.

- The new front door, from PR #58: purpose first, the n=1..100 atlas above the fold, the
  inventory table, the assurance vocabulary, and where the archive falls short.
- The existing `explorations/packing/README.md`: operating principles, the seven workflow
  entry points, the layout tree, the report index and the work model. This one is
  gate-checked by `check_readme.py`, which is why it cannot simply be dropped.

Merge them into the root `README.md`, front-door material first, checked material below.

Then repair `check_readme.py`, which has two separate couplings to the old layout:

1. `layout_tree()` finds the tree by looking for a fenced block whose first line starts
   with `explorations/packing/`. README and checker change together.
2. The tree check requires every top-level entry to appear in the tree. The root brings
   six new non-dot entries the packing directory never had: `AGENTS.md`, `CLAUDE.md`,
   `Makefile`, `lefthook.yml`, `package.json`, `package-lock.json`. Either give them rows
   in the tree or extend `NOT_CONTENT`; rows are more honest, since a reader arriving at
   the root genuinely does see them.

Worth deciding here: the root README is not currently covered by `check_readme.py` at
all, which is why PR #58 deliberately carries no volatile counts. Once merged it IS the
checked README, so that constraint becomes enforced rather than voluntary.
