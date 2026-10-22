---
type: is
id: is-01m5hmvcvj7xhe6sdte5fvvy0r
title: On-request prune guard matches path spellings only; a dotted-module run or import of a pruned tool passes (#721 review A1)
kind: task
status: in_progress
priority: 3
version: 4
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
delegate: c-lane-tooling-1022
labels: []
dependencies: []
parent_id: is-01m1sx5m1p5868jhwcdzfkvada
hold: null
hold_until: null
created_at: 2026-10-22T11:09:59.026Z
updated_at: 2026-10-22T19:22:31.014Z
started_at: 2026-10-22T11:14:08.734Z
---
Review A of #721, finding A1 (Low), deferred.

`test_the_on_request_prune_has_no_registered_control_consumer` (`packing/tests/test_muglich_686_import.py:122-136`) covers the ten ON_REQUEST_IMPORT_TOOLS files, five of them tools, but asserts only that no control's `run` contains the packing-relative path. A control that runs `python3 -m devtools.couzo_715_replay` (dotted module spelling), or a worker command that imports one of the tools, passes it. The audit's `registered_mentions` in `packing/devtools/run_negative_controls.py` (around lines 2565-2569 at e6a1e026) also matches path tokens only.

Reviewer found no such use at e6a1e026 (search, import closure, strace of 55 commands and the traced worker tests), so the change is sound; this is about the guard.

Fix: also assert each tool's dotted module name (`devtools.<stem>`, `sqpack.<...>`) appears in no control's `run`; optionally an AST import scan of the control programs. Apply the same to `registered_mentions`. Test: a synthetic control running `-m devtools.<pruned tool>` must be caught.

Review: https://github.com/jlevy/squares/pull/721#issuecomment-6339260683

## Notes

2026-10-22 c-lane-tooling-1022: done in jlevy/squares#723 (draft, head de5179c76), awaiting hosted CI and merge.

- `registered_mentions(candidate, records)` is now a function in `run_negative_controls.py`, called by `--audit-snapshot`. It also matches the candidate's dotted module name (`module_name`: `devtools.<stem>`, and `sqpack.<...>` for files under `src/`), on a word boundary, so `devtools.pruned_tool_two` is not a mention of `devtools.pruned_tool`.
- `test_the_on_request_prune_has_no_registered_control_consumer` asks `registered_mentions` for all ten files and shows a synthetic `-m devtools.couzo_715_replay` control caught. `test_the_audit_names_a_control_that_runs_a_candidate_by_its_module_name` drives the audit itself.
- The optional AST import-closure check is taken as `test_no_control_loads_a_pruned_tool` in `tests/test_negative_controls.py` (about 85 lines with helpers, 1.45 s). It covers every path in `PRUNE`, not only the on-request tools. It follows the load-time closure of each control's `-m` modules, pytest files with `conftest.py`, console scripts and here-document source, and it is green on main for all 50 distinct commands. Function-local imports are excluded; counting them fails 11 commands (`check_results`, `validate_schemas`, ...) through calls they never make.
- Remaining limits, stated in the PR: subprocesses that validation steps start, `importlib`, whole-suite collection, and a function-local import a control does call. Only the control's own run in a worker decides those.

2026-10-22 c-lane-tooling-1022, #723 review A1 (`edf295c41`): the load-time guard fails closed. A `python` or `pytest` invocation it cannot read raises. It reads `"PY"`, bare and redirected here-documents, `-c` source, scripts under `packing/`, and a test's bare sibling imports. The whole-suite control is named in `UNFOLLOWED_COMMANDS` with its reason. Head `09e3ba373`, with main 78dc902c1 merged in; hosted CI green (Packing validation 39837221487, Certificate page 39837221468). For the coordinator to close after merge.
