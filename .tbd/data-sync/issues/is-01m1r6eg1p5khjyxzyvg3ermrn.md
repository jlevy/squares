---
type: is
id: is-01m1r6eg1p5khjyxzyvg3ermrn
title: "New PR: a modern lint floor, Python 3.12+, on all Python code, and a review of the verification code against the tbd guidelines and Python CLI practice"
kind: feature
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-09-05T07:10:09.973Z
updated_at: 2026-09-05T07:10:09.973Z
---
Owner's direction 2026-09-05: review all of the verification and other code; it targets older Python (minimal_verify.py says CPython 3.8+, verify_claim.py 3.10+, thirdparty/ likewise). Raise the floor to Python 3.12+ everywhere (requires-python, ruff target-version and rule sets, basedpyright), follow tbd guidelines (python-rules, general-coding-rules) and best practices for Python CLI apps, and update every document that states a floor. Survey and plan first (sub-agent), then implement on a fresh branch off main after PR 79 merges. The verifier consolidation question (think-dfoc) is decided in this PR.
