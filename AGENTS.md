# Project Instructions for AI Agents

This file provides instructions and context for AI coding agents working on this
project.

<!-- BEGIN TBD INTEGRATION format=f08 surface=agents-md -->
## tbd

This repository uses **tbd** for git-native issue tracking (beads), spec-driven
planning, and on-demand engineering guidelines.
As the agent, you operate tbd on the user’s behalf: translate their requests into tbd
actions rather than telling them to run commands.

- Run `tbd prime` to load current project state and the full tbd workflow.
- Run `tbd skill` for the complete reusable tbd skill instructions.
- Run `tbd shortcut --list` and `tbd guidelines --list` for on-demand resources.
- Track all work as beads: `tbd create`, `tbd ready`, `tbd close`, and `tbd sync`.

<!-- END TBD INTEGRATION -->

## Build & Test

This repository ships no code.
The only tooling is Markdown formatting.

```bash
make hooks-install   # once after cloning: installs the lefthook pre-commit hook
make format          # format all Markdown
make format-check    # report drift without writing
```

### Markdown formatting

**Flowmark owns all Markdown here.** Do not add Prettier, Biome, or dprint Markdown
handling alongside it — two Markdown formatters churn each other’s output and make hooks
nondeterministic.

Formatting is applied **automatically on commit** by a lefthook `pre-commit` hook, which
formats and re-stages the result (`stage_fixed: true`). You should never need to format
by hand, and unformatted Markdown is not something you can commit by accident.

Formatting drift deliberately **does not fail CI**. It is fixed at commit time instead,
so style never blocks a build.
`make format-check` exists for ad-hoc checking, not as a gate.

Two rules worth knowing before changing any of this:

- **The hook formats the whole repository, not the staged files.** Flowmark reads
  `.flowmarkignore` relative to its target argument, so passing explicit paths silently
  bypasses the exclusion list.
  That matters here: `.flowmarkignore` protects `resources/papers/` and
  `resources/web/`, where the `.raw.md` extractions are byte-level ground truth used to
  check the model-assisted transcriptions against.
  Reflowing them would void that guarantee.
  Do not “optimise” the hook to `{staged_files}`.
- **The flowmark version is pinned** in the `Makefile` (currently the latest Rust build,
  `flowmark-rs==0.3.2` — the Rust port is the fast one).
  Pinned rather than floating so it is not an unpinned zero-install runner, which
  `tbd guidelines supply-chain-hardening` rule 6 warns against.
  Bumping the pin is a deliberate, reviewable change.

Emergency bypass: `git commit --no-verify` (avoid in PRs).

## Architecture Overview

*Add a brief overview of your project architecture*

## Conventions & Patterns

*Add your project-specific conventions here*

<!-- BEGIN FLOWMARK INTEGRATION format=f03 surface=agents-md -->
## flowmark

Auto-format Markdown with `flowmark` for clean, semantic git diffs.

- Run `flowmark --auto <files>` on Markdown you create or edit.
- Run `flowmark --docs` for full usage and `flowmark --skill` for the skill.
- If `flowmark` is not on `PATH`, use a pinned `uvx` runner (never `@latest`).
- Fast Rust port (recommended): `uvx --from flowmark-rs==0.3.2 flowmark`.
- Python build (library / newest patch): `uvx --from flowmark==0.7.2 flowmark`.

<!-- END FLOWMARK INTEGRATION -->
