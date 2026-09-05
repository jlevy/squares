---
type: is
id: is-01m1r6eg1p5khjyxzyvg3ermrn
title: "New PR: a modern lint floor, Python 3.12+, on all Python code, and a review of the verification code against the tbd guidelines and Python CLI practice"
kind: feature
status: open
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T07:10:09.973Z
updated_at: 2026-09-05T07:20:48.522Z
---
Owner's direction 2026-09-05: review all of the verification and other code; it targets older Python (minimal_verify.py says CPython 3.8+, verify_claim.py 3.10+, thirdparty/ likewise). Raise the floor to Python 3.12+ everywhere (requires-python, ruff target-version and rule sets, basedpyright), follow tbd guidelines (python-rules, general-coding-rules) and best practices for Python CLI apps, and update every document that states a floor. Survey and plan first (sub-agent), then implement on a fresh branch off main after PR 79 merges. The verifier consolidation question (think-dfoc) is decided in this PR.

## Notes

Survey 2026-09-05 (sub-agent): the tree is already Python 3.14 with requires-python >=3.14, ruff target py314, basedpyright 3.14, and ruff/format/basedpyright all at zero findings; UP/FA/PTH at py312 measure 0. Pre-3.12 code is confined to the standalone verifiers (minimal_verify.py 3.8+, verify_claim.py 3.10+, thirdparty/ 3.8+, all excluded or noqa'd on purpose so any system python3 can run them) plus one dt.timezone.utc in the ungated .agents skill asset. Plan: close the two coverage holes (.agents skill assets, frankensim-probe), enable FURB/FLY/PYI/BLE/ERA/ARG/PT and a C90 ratchet (~427 findings, 72 auto-fixable), turn the global T201 waiver into per-directory ignores (4 library prints), raise the verifiers to 3.12+ as the owner directed and pay the cost (233 findings, docstrings, templates, thirdparty README transcript re-run), keep independent_verify.py and resources/web excluded as retained review and archive artifacts, harmonize CLI entry points (main(argv) -> int, raise SystemExit(main()), --version on the four scripts), add config- and coverage-contract tests, update AGENTS.md/development.md/conventions.md. Implementation in worktree /home/user/squares-lint on branch claude/python-lint-floor-v7taqx off f5d4b854, to be rebased onto main after PR 79 merges.
