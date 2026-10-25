---
type: is
id: is-01m5rtm3kqps82jfhxdeyxbkna
title: "New exact-side polynomial PR from current main, building on T-246; supersedes #403/#435 (#811)"
kind: task
status: in_progress
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-25-exact-side-register.md
delegate: w-exact-sides-1025
labels:
  - project
dependencies: []
parent_id: is-01m5sv3xcxr02a4019fz9bbmn9
hold: null
hold_until: null
created_at: 2026-10-25T06:05:32.663Z
updated_at: 2026-10-25T16:04:10.491Z
started_at: 2026-10-25T14:30:51.378Z
---
Owner decision 2026-10-25: #403/#435 are out of date (assessment in think-vt31). Start a fresh PR on current code and practice: main's polynomial notation (exact_sides.polynomial_text, root(p, low, high)), main's record coverage (derived facts in a register or view, not written onto records), one-record-per-line retained JSON; algebraic_source only if it still earns its place. Builds on Evan Daniel's s(29) registration (T-244, think-6gti). Lower priority: start only after the current result landings (T-243 n=12, T-244 s(29)) and the other outstanding intake items have merged. Run by its own sub-agent; the coordinator owns sequencing.

## Notes

## Slice 1, 2026-10-25 (w-exact-sides-1025)

Branch claude/friendly-einstein-gf9z0h-exact-sides from origin/main 272b411b4, main 0785626cc merged in (one release.py conflict, both records kept); draft PR https://github.com/jlevy/squares/pull/818 (feat(exact-sides), labels project and S2). Spec docs/project/specs/active/plan-2026-10-25-exact-side-register.md; epic think-gbr2 with later slices think-fz2w (2, stated polynomials), think-sg7h (3, every count; owner Q1), think-bvxv (4, n = 83 completed; owner Q2; think-chsu owned elsewhere), think-9n0p (5, s(29) from its archive), think-ylad (6, site catalogue).

Delivered: packing/frontier/exact-side-register.json (24 facts at 24 counts: 10 houses, 9 staged T-193 houses, 5 configurations at 29, 83, 172, 204, 263), its schema, devtools.exact_side_register (SymPy irreducibility over Z, Descartes isolation in GMP integers, writer held to exact_sides.form, --update/--check), the records-tier step "exact-side register is current", devtools.kingbird_root_polynomial and n = 83's receipt (square-83.svg fetched live, held to the 5 October pin; 673 coefficients, primitive, height 724 digits, one root within 1e-99 of the printed side, 9.635e-20 below the rational house), tests, READMEs, the integrity-ceremony allowlist entry, DATA_REVISION re-pinned, and the four papers' no-change record (69 files byte-identical, twice from the tree and once with main's three candidate inputs swapped in).

Coordination: when think-ot5c adopts a staged T-193 count, `exact-side register is current` fails and names `python -m devtools.exact_side_register --update`; the adopting PR regenerates the register.
