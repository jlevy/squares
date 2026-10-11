---
type: is
id: is-01m4mdbe5pjzjb684fqbedg5p0
title: "Check out evand/square-packing in full into attic/ and examine search/regularize: the code, the process and how it differs from regularize_axis_components/2"
kind: task
status: in_progress
priority: 1
version: 4
labels:
  - regularization
dependencies:
  - type: blocks
    target: is-01m4mdbq6bhkv71fxeeckawsbt
parent_id: is-01m4mdb1j4atn6yvmtcf93eqmt
created_at: 2026-10-11T02:40:57.526Z
updated_at: 2026-10-11T02:42:11.244Z
---
Owner request 2026-10-11 (epic think-cdud, item 4): clone https://github.com/evand/square-packing in full into attic/evand-square-packing (tbd shortcut checkout-third-party-repo; read-only), at main's head, and record the commit. Examine search/regularize (https://github.com/evand/square-packing/tree/main/search/regularize) and what it calls (exactsolve, the path test samepacking.py, reg.py, atlas.py, verify_cert.py and verify_cert2.py, the lists and REGULARIZE.md): inputs, the LP translation, symmetry and coincident-face imposition, angle grouping, the conservative and fewest variants, the level classification and its path test, the exact certificate it writes, its dependencies and licence (MIT at ea1a2f2), and its run cost per count. Compare with this project's regularize_axis_components/2 (devtools/regularize_axis_components.py, atlas/known-best/regularized/): what each guarantees (same side, exact verification, non-regression), what each refuses, and which drawings each would change. Output: a written assessment in docs/project/ (research brief or review) with a recommended adaptation plan for the stacked regularization PR, the soundness obligations the adaptation must meet (exact feasibility at the stated side; same-packing identity basis recorded in the register's regularizations field), and the open owner questions.

## Notes

2026-10-11: cloned https://github.com/evand/square-packing in full into attic/evand-square-packing at 060c1a1 (main's head, 'Merge PR #6 (wand125): ValidTilt7 / Valid7 in the kernel'), 377 MB, gitignored; search/regularize holds REGULARIZE.md, atlas.py, census.py, gallery.py, lists/, lists.py, refresh.py, reg.py, register_cert.py, samepacking.py. An examination lane (stage: research, read-only on the checkout) is writing the assessment to the coordinator's scratch; it goes into the stacked regularization PR (think-ux1v).
