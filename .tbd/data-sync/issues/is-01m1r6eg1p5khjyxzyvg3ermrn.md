---
type: is
id: is-01m1r6eg1p5khjyxzyvg3ermrn
title: "New PR: a modern lint floor, Python 3.12+, on all Python code, and a review of the verification code against the tbd guidelines and Python CLI practice"
kind: feature
status: in_progress
priority: 1
version: 5
labels: []
dependencies: []
created_at: 2026-09-05T07:10:09.973Z
updated_at: 2026-09-05T15:32:24.146Z
---
Owner's direction 2026-09-05: review all of the verification and other code; it targets older Python (minimal_verify.py says CPython 3.8+, verify_claim.py 3.10+, thirdparty/ likewise). Raise the floor to Python 3.12+ everywhere (requires-python, ruff target-version and rule sets, basedpyright), follow tbd guidelines (python-rules, general-coding-rules) and best practices for Python CLI apps, and update every document that states a floor. Survey and plan first (sub-agent), then implement on a fresh branch off main after PR 79 merges. The verifier consolidation question (think-dfoc) is decided in this PR.

## Notes

PR 84 opened 2026-09-05: https://github.com/jlevy/squares/pull/84 (branch claude/python-lint-floor-v7taqx, 9 commits on main at f060b1d7). Verified before opening: floors unchanged; both n=11 verifiers' decision functions structurally identical to main (numbers, operators, comparisons, called names per function); thirdparty differences are zip->pairwise, %-format to f-strings, the random audit guarded, two new named assertions, os.path->pathlib; the 5 byte-pinned instruments identical and 72 pin tests pass; push gate on the merged tree 2012 passed. Open for the owner: PT017 global ignore, the C90 ratchet at 57, and that the 3.12 verifier floor is declared rather than enforced.
