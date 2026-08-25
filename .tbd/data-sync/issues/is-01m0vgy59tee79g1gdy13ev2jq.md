---
type: is
id: is-01m0vgy59tee79g1gdy13ev2jq
title: Replace fragmentary packing script tests with Tryscript golden sessions
kind: task
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels:
  - engineering-maturity
  - testing
  - cli
  - golden-tests
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-25T03:55:30.489Z
updated_at: 2026-08-25T04:15:42.506Z
---
The maintained packing command surfaces are not currently tested as complete command sessions.

`tests/test_validation_cli.py` calls `sqpack.cli.validate.main()` in-process and asserts selected substrings. This bypasses the installed `packing-validate` executable boundary and does not preserve the full stdout/stderr transcript. `tests/test_command_help.py` similarly checks only `usage:` and the absence of `Traceback` for four module invocations; it does not make the complete help contract reviewable, does not exercise all three installed commands, and omits `packing-campaign`. There is no Tryscript configuration, `.tryscript.md` suite, pinned runner, or documented golden-update workflow.

Adopt the console-output golden approach from `golden-testing-guidelines` and Tryscript for maintained E2/E3 CLI and developer-tool surfaces. This is a follow-up to PR #23, not part of that PR. It covers behavioral command goldens, not the numerical basin-map problem owned by `think-lwao` or other mathematical golden semantics.

Required scope:

- Inventory the installed commands (`packing-validate`, `packing-campaign`, and `packing-ledger`) plus documented maintained module commands. Record explicit exclusions for E0/E1 one-off research scripts so the harness does not impose reusable-tool process on disposable experiments.
- Pin Tryscript in the repository toolchain and lockfile. Provide one stable run command and one explicit `--update` command; CI must not depend on `@latest`.
- Add small, end-to-end `.tryscript.md` sessions that execute the installed commands at the process boundary and capture complete stdout, stderr, exit status, and reviewable filesystem effects for canonical help, discovery/status, success, refusal, malformed-input, and partial-failure paths.
- Use isolated sandboxes, declared fixtures, `NO_COLOR`, and deterministic inputs. Normalize only genuinely unstable fields such as temporary paths or elapsed durations, preferably with named patterns. Keep stable values exact; do not use broad wildcards, `grep`, `jq`, `head`, or hashes to hide most of a result.
- Show complete written file contents when a command mutates sandbox state. Git diffs, not digests, own golden integrity.
- Keep focused pytest, property, architecture, and mutation-control tests where they verify internal invariants better than a console transcript. Remove fragmentary CLI assertions only after equivalent or stronger golden coverage exists.
- Integrate the fast sessions into `packing-validate` and Linux/macOS CI, and document the regenerate-review-diff workflow for people and agents.

Acceptance:

- Every maintained command surface is covered or explicitly classified out of scope.
- Canonical sessions are deterministic and cheap enough to run on every commit; slow or nondeterministic dependencies are mocked or replaced with stable fixtures.
- Help and error sessions compare complete output and exact exit codes, including stdout/stderr routing.
- An intentional stable-output change makes CI fail with a readable session diff; `--update` regenerates only the affected golden for review.
- No broad pattern masks a stable field, no surgical extraction substitutes for complete state, and no checksum is introduced for repository-owned goldens.

## Notes

2026-08-24: PR #23 formal review R9 independently confirms the current test smell: test_validation_cli runs a full frontier gate step inside pytest and monkeypatches the production ACTIVITY_MARKER global. Per the user's explicit scope decision, the golden-script testing migration remains a follow-up rather than a PR #23 change. R9 is deferred to this bead; implementation should replace fragment assertions and unsupported marker patching with Tryscript process-level sessions plus focused pure-function tests for internal frontier logic.
