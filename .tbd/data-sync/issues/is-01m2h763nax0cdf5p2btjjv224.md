---
type: is
id: is-01m2h763nax0cdf5p2btjjv224
title: "Guard: JavaScript in a Python string fails the build"
kind: feature
status: closed
priority: 1
version: 8
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
updated_at: 2026-09-15T01:17:56.613Z
closed_at: 2026-09-15T01:17:56.612Z
close_reason: "Delivered in PR #175: the AST guard, the ratchet allowlist, the edit-tier and PR-surface wiring, the contract test, controls and docs."
resolution: null
duplicate_of: null
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

## Notes

Delivered in PR #175 (head 1ec9ea7b).

- Guard: packing/devtools/check_no_embedded_js.py parses every tracked or untracked-unignored *.py file (git ls-files; it walks the tree in gitless snapshots). It counts three kinds of site:
  (1) a built script argument to evaluate, evaluate_handle, evaluate_all, eval_on_selector, eval_on_selector_all, wait_for_function or add_init_script, positional or keyword: a literal, f-string, concatenation, % or .format result, a string method applied to text or to a probe, or a name bound to one;
  (2) a string matching a JavaScript signature, with concatenations read as one string;
  (3) code after a <script> tag. Docstrings are exempt.
- Policy and ratchet: packing/devtools/embedded-javascript.yaml holds the signatures, the script-tag and script-code patterns, and the allowlist. The check fails on an unlisted offender, a grown count, an unrecorded shrink, and a clean file that is still listed.
- Initial allowlist: 477 sites in 48 files (312 JavaScript string, 155 script argument, 10 script body). By bead: think-3pox 324 sites in 25 files; think-53dt 123 in 13; think-xvjf 30 in 10. This is larger than the epic's 36-file estimate, mainly because of Node scripts inside packing/tests.
- Wiring: the step 'browser code lives in files (embedded JavaScript, probes)' runs in --edit and --checks, taking about 2.5s.
- Liveness: packing/tests/test_no_embedded_js_contract.py (50 tests) and three negative controls in devtools/controls.yaml.
- Docs: AGENTS.md (JavaScript floor section) and development.md ('Browser Code Lives in Files').
