---
type: is
id: is-01m5rsfwjjbh5bzbrwtjtvc2xx
title: "Revise polynomial PR stack #403/#435 onto main (owner request 2026-10-25)"
kind: task
status: closed
priority: 1
version: 6
delegate: w-polystack-1025
labels:
  - project
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-25T05:45:45.809Z
updated_at: 2026-10-25T16:55:03.268Z
started_at: 2026-10-25T05:45:50.075Z
closed_at: 2026-10-25T16:55:03.267Z
close_reason: "Owner decision 2026-10-25: #403/#435 superseded; the fresh register (#818, 2f974835a) replaced them; both PRs closed."
resolution: null
duplicate_of: null
---
Owner request 2026-10-25: delegate to sub-agents to revise the open polynomial PR stack main -> #403 (claude/friendly-sagan-jk7qzy) -> #435 (codex/exact-polynomial-coverage). Goal: bring both heads current with main (bb756e19 or later) by merge commits (no rebase/force-push), CI green on both heads, descriptions accurate and short (OR-9), linking tracker #811. No new results on the stack (s(29)/T-246 and n=12/T-245 are elsewhere). Prior stack owner bead think-6vrv is delegated to claude-code@spud10.local and is not taken over here.

## Notes

## Assessment, 2026-10-25 (w-polystack-1025)

Heads read: main bb756e19; #403 claude/friendly-sagan-jk7qzy 3ee60c3e (base 34c826f0, 13 Oct);
#435 codex/exact-polynomial-coverage 7c1fe653. Main is 3,666 commits past the stack's base.
`git cherry` finds none of #403's 22 commits patch-equivalent on main.

Verdict: not a tractable merge. Stopped before pushing either layer; nothing pushed.

### Conflicts

- main into #403: 39 files. 15 case records (n = 70, 102, 123, 153, 183, 204, 207, 227,
  229, 258, 259, 260, 264, 295, 302), all re-housed on main since 13 Oct: nine with
  algebraic sides of degree 2 to 8 (T-174 PingYou #574 at 70, 153, 207; T-193 Evan #639
  at six counts) and six with later rational houses, where #403 holds its older derived
  degree-1 side; adopt_houses, upper_bound_houses, validate_schemas, cli/validate,
  release pin, composite-figure (59 hunks), chunk-components.json (modify/delete), the n=11
  research doc, suite costs, site probes and 13 test modules.
- main into #435 directly: 59 files, adding the site renderer, URL registry, overview,
  pages workflow, README/development and seven site test modules.

### What main absorbed or superseded

- House adoption moved to main on the owner's 11 Oct decision not to wait for #403
  (regularization-policy.md item 12; #518). Main has run 11 more adoption passes
  (12 Oct to 25 Oct, LATER_PASSES) with full prior-state custody
  (house-adoption-prior-state-*.json.xz), including n = 29 on 17 Oct.
- Main's house writer takes algebraic sides (think-ot5c, #756): exact_form
  `root(p, low, high)` or a quadratic closed form, minimal_polynomial in
  `exact_sides.polynomial_text` notation (`89s^5-3225s^4+...=0`), rational houses written
  `algebraic_degree: 1, minimal_polynomial: null`.
- Main's retained-JSON policy (development.md, Retained JSON Is One Record per Line)
  re-laid chunk-components.json to 49,777 lines and keeps gzip for archived third-party
  sources only.
- Main removed TREE_REUSABLE_FAST_STEPS and reworked the validation tiers (hosted CI gates
  drafts, 22 Oct); the stack's selector repairs and call-wall diagnoses (think-xb1o,
  think-w0if) were measured on the old surface.

### What is still only on the stack

- The exact-value register (exact-values.json.gz), `algebraic_source` provenance, derived
  polynomials for every record, the n = 83 degree-672 coefficients, Kingbird
  exact-side fact packets (#435), and the web catalogue and report (#435). Main publishes
  no exact-side catalogue.

### Why it stops (experimental merge, aborted, not committed)

Taking main's side for every conflict and running the stack's own
`python -m devtools.build_exact_values --check` fails at once:
`AttributeError: module 'devtools.upper_bound_houses' has no attribute 'receipt_for_source'`.
Past that API, `exact_house_sources.Inputs.admit` requires every adopted house to be degree
1 with a rational exact_form ("native side degree"), and the register needs one immutable
`house-exact-prior-{day}.json.xz` per adoption pass, which exists for 11 and 12 Oct only.
Carrying the stack forward is a port of about 4,700 lines of register tooling onto main's
rewritten adoption code, not a conflict resolution.

### Decisions for the owner

- D1 notation: main's `polynomial_text` or the stack's `2s^2 - 28s + 97 = 0`.
- D2 coverage: the stack writes degree and polynomial on 307 of 324 records (294 derived
  from the exact form, 236 of them degree 1); main writes the degree on 87, the
  polynomial on 22, and a null polynomial for a rational house. Keep the stack's derived
  fields on the records, or keep them only in the register.
- D3 `algebraic_source` for main's algebraic houses: none of catalogue,
  derived-from-exact-form or contact-system fits a replayed number-field fact.
- D4 storage: the stack's gzip of chunk-components.json and the register, or main's
  re-laid JSON.
- D5 the path: port the stack (A), rebuild the unique parts from main as a fresh PR (B),
  or hold (C).

Other beads: think-6vrv (stack owner) and think-xb1o are delegated to
claude-code@spud10.local, last touched 18 Oct; think-w0if, think-ht59, think-e7sr,
think-z3qh to codex@spud10. None were taken over.

### Done this session

- Nothing committed or pushed to either branch; heads remain 3ee60c3e and 7c1fe653.
- Rewrote both PR descriptions (2026-10-25 05:57Z) to the OR-9 template: cost first,
  current status, the decisions D1 to D5 on #403, link to #811, history pointer to the
  handoff on #435 at 7c1fe653. `devtools.check_pr_description --file` passes on both.
- Next: the owner's choice under D5. The bead stays open until then.
