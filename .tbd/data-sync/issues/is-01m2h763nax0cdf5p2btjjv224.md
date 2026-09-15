---
type: is
id: is-01m2h763nax0cdf5p2btjjv224
title: "Guard: JavaScript in a Python string fails the build"
kind: feature
status: open
priority: 1
version: 6
labels: []
dependencies:
  - type: blocks
    target: is-01m2h764pcbfwx0btxez85zdsq
  - type: blocks
    target: is-01m2h765488h9hcy6c3zpp4abx
  - type: blocks
    target: is-01m2h765jws1b00yav58n7wzaq
  - type: blocks
    target: is-01m2h7667fbtgmwgtwpq0hdtmw
parent_id: is-01m2h76347zn3abcahzd3642ac
created_at: 2026-09-15T00:24:04.521Z
updated_at: 2026-09-15T00:25:26.690Z
---
A check that makes JavaScript in Python impossible to merge.

- **AST-based, not grep.** It fails on:
  - a string literal, f-string or concatenation passed as the script argument to Playwright's `evaluate`, `evaluate_handle`, `evaluate_all`, `eval_on_selector`, `eval_on_selector_all`, `wait_for_function` or `add_init_script` (keyword or positional);
  - a module or class string constant that parses as JavaScript by the same heuristics the inventory used;
  - any `<script>` body built inside Python.
  The only accepted script argument is a probe loaded from a `.js` file (`probe("<name>")`) or a variable bound to one.
- **A ratchet allowlist** in a data file names each remaining offender with its tracking bead and current site count. The check fails if a count grows, if a file not on the list offends, or if a listed file has reached zero and not been removed. The list must be empty when the epic closes.
- **Wired into the edit tier and CI** (`packing-validate`), with a contract test that plants each offending form in a temporary Python file and requires the check to fail, per the liveness rule in `ci-and-gates-rules`.
- **Documented** in `development.md` and in `AGENTS.md`'s JavaScript floor paragraph as a rule with no exceptions.
