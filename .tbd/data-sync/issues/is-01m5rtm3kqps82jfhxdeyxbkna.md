---
type: is
id: is-01m5rtm3kqps82jfhxdeyxbkna
title: "New exact-side polynomial PR from current main, building on T-246; supersedes #403/#435 (#811)"
kind: task
status: in_progress
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-10-25-exact-side-register.md
delegate: w-exact-sides-1025
labels:
  - project
dependencies: []
parent_id: is-01m5sv3xcxr02a4019fz9bbmn9
hold: null
hold_until: null
created_at: 2026-10-25T06:05:32.663Z
updated_at: 2026-10-25T16:37:32.702Z
started_at: 2026-10-25T14:30:51.378Z
---
Owner decision 2026-10-25: #403/#435 are out of date (assessment in think-vt31). Start a fresh PR on current code and practice: main's polynomial notation (exact_sides.polynomial_text, root(p, low, high)), main's record coverage (derived facts in a register or view, not written onto records), one-record-per-line retained JSON; algebraic_source only if it still earns its place. Builds on Evan Daniel's s(29) registration (T-244, think-6gti). Lower priority: start only after the current result landings (T-243 n=12, T-244 s(29)) and the other outstanding intake items have merged. Run by its own sub-agent; the coordinator owns sequencing.

## Notes

## Slice 1, 2026-10-25 (w-exact-sides-1025)

Branch claude/friendly-einstein-gf9z0h-exact-sides from origin/main 272b411b4, main 0785626cc merged in (one release.py conflict, both records kept); draft PR https://github.com/jlevy/squares/pull/818 (feat(exact-sides), labels project and S2). Spec docs/project/specs/active/plan-2026-10-25-exact-side-register.md; epic think-gbr2 with later slices think-fz2w (2, stated polynomials), think-sg7h (3, every count; owner Q1), think-bvxv (4, n = 83 completed; owner Q2; think-chsu owned elsewhere), think-9n0p (5, s(29) from its archive), think-ylad (6, site catalogue).

Delivered: packing/frontier/exact-side-register.json (24 facts at 24 counts: 10 houses, 9 staged T-193 houses, 5 configurations at 29, 83, 172, 204, 263), its schema, devtools.exact_side_register (SymPy irreducibility over Z, Descartes isolation in GMP integers, writer held to exact_sides.form, --update/--check), the records-tier step "exact-side register is current", devtools.kingbird_root_polynomial and n = 83's receipt (square-83.svg fetched live, held to the 5 October pin; 673 coefficients, primitive, height 724 digits, one root within 1e-99 of the printed side, 9.635e-20 below the rational house), tests, READMEs, the integrity-ceremony allowlist entry, DATA_REVISION re-pinned, and the four papers' no-change record (69 files byte-identical, twice from the tree and once with main's three candidate inputs swapped in).

Coordination: when think-ot5c adopts a staged T-193 count, `exact-side register is current` fails and names `python -m devtools.exact_side_register --update`; the adopting PR regenerates the register.

## Validation and hosted CI, 2026-10-25 (w-exact-sides-1025)

Head 045d8c89a, with main 0785626cc merged at a2a5748ef: the edit tier without its type floor passed all 69 selected steps in 491 s, and the records tier all 54 in 191 s. The type floor hits this host's 900 s cap; hosted typecheck passes. The papers were rendered again at a2a5748e: 69 files byte-identical three ways, and identical to the 57f70c3e measurement apart from the link revision. The no-change record says so (045d8c89a). Hosted CI is green at 045d8c89a: of 59 check runs, 31 passed (packing-required, pages-required and merges-into-base among them) and 28 were skipped by scope, none failed; a2a5748e was green the same way. The PR body was updated with these results and carries the session footer (verified against the published body; check_pr_description ok). PR state: open, draft, mergeable_state clean, labels S2 and project.

Open owner decisions, under "Decisions for the Owner" in the PR body: Q1 (slice 3, whether the register lists every count) and Q2 (slice 4, whether n = 83's 673 coefficients are retained). The PR stays a draft. Ready-for-review, merge and closing #403/#435 are the coordinator's calls; this bead closes when the PR lands.
