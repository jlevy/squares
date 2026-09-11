---
type: is
id: is-01m299vcddahjev9njwnhmcq9m
title: "J4: wire the gate, and prove the floor is live"
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m299tcsrh44b8n8m1c6jpgcb
created_at: 2026-09-11T22:36:43.308Z
updated_at: 2026-09-11T23:08:50.474Z
closed_at: 2026-09-11T23:08:50.473Z
close_reason: "lefthook fixes at commit and is sequential; npm ci with a pinned Node on the pull-request surface; make hooks-install and make lint-fix locally; 'browser floor (biome, tsc)' a step in packing-validate --fast at about a second. And test_browser_floor_contract.py proves the floor is live rather than merely written: it hands Biome a braceless if and tsc a type error and requires both to complain. Mutation-tested -- turning useBlockStatements off fails two of its tests, emptying a config's include fails a third. Landed as c803f848."
resolution: null
duplicate_of: null
---
Floor rule 6: hooks auto-fix at commit, the full verify gate runs at push and in CI.

- lefthook `pre-commit`: `biome check --write --unsafe` over staged JS/CSS with `stage_fixed: true`, sequential -- two formatters writing the index race on `.git/index.lock`. The repo's existing markdown hook is `parallel: true`; adding a second index-writing hook means that has to change.
- `npm ci` plus `biome ci --error-on-warnings .` in the pull-request surface (packing-validation.yml), and in `packing-validate --push`.
- Node is on the GitHub runner already; the repo has a package-lock.json but no `npm ci` step yet.

And the part that is easy to skip: **a config-contract check that proves the floor is live.** `ci-and-gates-rules` exists because gates go green while checking nothing. Assert that `useBlockStatements` is actually enabled and that the workbench's assets are actually in scope -- a `files.includes` typo silently exempts the only thing this is for.
