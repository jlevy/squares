---
type: is
id: is-01m5hmvcvj7xhe6sdte5fvvy0r
title: On-request prune guard matches path spellings only; a dotted-module run or import of a pruned tool passes (#721 review A1)
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies: []
parent_id: is-01m1sx5m1p5868jhwcdzfkvada
created_at: 2026-10-22T11:09:59.026Z
updated_at: 2026-10-22T11:09:59.026Z
---
Review A of #721, finding A1 (Low), deferred.

`test_the_on_request_prune_has_no_registered_control_consumer` (`packing/tests/test_muglich_686_import.py:122-136`) covers the ten ON_REQUEST_IMPORT_TOOLS files, five of them tools, but asserts only that no control's `run` contains the packing-relative path. A control that runs `python3 -m devtools.couzo_715_replay` (dotted module spelling), or a worker command that imports one of the tools, passes it. The audit's `registered_mentions` in `packing/devtools/run_negative_controls.py` (around lines 2565-2569 at e6a1e026) also matches path tokens only.

Reviewer found no such use at e6a1e026 (search, import closure, strace of 55 commands and the traced worker tests), so the change is sound; this is about the guard.

Fix: also assert each tool's dotted module name (`devtools.<stem>`, `sqpack.<...>`) appears in no control's `run`; optionally an AST import scan of the control programs. Apply the same to `registered_mentions`. Test: a synthetic control running `-m devtools.<pruned tool>` must be caught.

Review: https://github.com/jlevy/squares/pull/721#issuecomment-6339260683
