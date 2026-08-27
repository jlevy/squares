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

The repository is mostly prose.
The only repo-wide tooling is Markdown formatting.

```bash
make hooks-install   # once after cloning: installs the lefthook pre-commit hook
make format          # format all Markdown
make format-check    # report drift without writing
```

Packing-specific Python, Rust, and research validation is documented in
[`explorations/packing/development.md`](explorations/packing/development.md).
From that directory, use
`uv run --frozen --all-extras --group dev packing-validate --fast` while editing and the
full `packing-validate` command at a research or merge checkpoint.

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

- **Exclusions are evidence-based, not precautionary.** The policy is to format the
  whole repository and exclude only what we have a tested reason to leave raw.
  Two exclusions qualify: the literature archive under
  `explorations/packing/resources/`, and the generated `SKILL.md` files.
  The archive is excluded for a measured reason — flowmark inserts line breaks *inside*
  `$...$` spans when it rewraps, which on 2026-08-22 broke 31 of 339 math spans in one
  transcription and 101 of 1236 in another.
  A newline mid-formula defeats `grep`, and local searchability is the entire point of
  that archive. Do not drop these exclusions without re-measuring.
- **The hook formats the whole repository, not the staged files.** Flowmark reads
  `.flowmarkignore` relative to its target argument, so passing explicit paths silently
  bypasses the exclusion list.
  That matters here: `.flowmarkignore` protects `explorations/packing/resources/`, where
  the `.raw.md` extractions are byte-level ground truth used to check the model-assisted
  transcriptions against.
  Reflowing them would void that guarantee.
  Do not “optimise” the hook to `{staged_files}`.
- **The flowmark version is pinned** in the `Makefile` (currently the latest Rust build,
  `flowmark-rs==0.3.2` — the Rust port is the fast one).
  Pinned rather than floating so it is not an unpinned zero-install runner, which
  `tbd guidelines supply-chain-hardening` rule 6 warns against.
  Bumping the pin is a deliberate, reviewable change.

Emergency bypass: `git commit --no-verify` (avoid in PRs).

## Architecture Overview

Two top-level trees hold the content.

- **`docs/project/research/`** — standalone research reports that need nothing but
  themselves. [Its README](docs/project/research/README.md) is the index.
- **`explorations/`** — self-contained project directories.
  Each one owns *everything* for its topic: its own reports under
  `docs/project/research/`, its own literature archive under `resources/`, and its own
  code and tests. [`explorations/packing/`](explorations/packing/README.md) is the worked
  example and the pattern to follow.

The split is by self-containment, not by subject.
A report that stands alone lives in `docs/`; a report that comes with sources and code
moves into an `explorations/` directory alongside them, so the whole line of work can be
read, run, and moved as one unit.

## Conventions & Patterns

- **An exploration directory is self-contained.** Its reports, sources, and code live
  under it and link to each other with relative paths that stay valid if the directory
  is moved or copied out.
  Do not scatter one project’s material across top-level trees.
- **Reports separate claims by evidential status** — proved, computationally verified,
  best known, or asserted-but-unverified — and cite primary sources near the claims they
  support.
- **Independently tracked packing work declares its entry point.** The coordinating
  agent chooses W1–W7 (or `general-improvement` only for genuine repository maintenance
  outside those workflows) from
  [`explorations/packing/README.md`](explorations/packing/README.md#workflow-entry-points)
  before beginning a session or a genuine workflow phase.
  Bounded delegated work such as formatting, lint repair, extraction, or repeated checks
  inherits the parent phase unless it opens its own independently tracked session.
  Longer sessions record workflow and primary-focus changes as ordered phases;
  [`explorations/packing/SYNOPSIS.md`](explorations/packing/SYNOPSIS.md#workflow-entry-contracts)
  owns the full contracts.
- **Multi-hour packing work starts with a time-sliced plan.** Follow the
  [bounded research cycle](explorations/packing/campaign/README.md#the-bounded-research-cycle)
  and the
  [portable session guide](explorations/packing/campaign/agent-sessions/README.md#starting-a-portable-four-hour-session).
  Unless the user sets another cadence, target a coherent integration checkpoint within
  about four hours and cap each slice at 30 minutes.
  At every boundary, compare measured command, coordinator, and sub-agent time with the
  remaining plan and replan only future slices.
  Use available sub-agents for independent read-only or disjoint-write work; the
  coordinating agent owns shared records, integration, commits, and external updates.
- **Archived source material is never edited to look tidy.** Where a transcription
  reconstructs damaged text, it is flagged inline and counted in the archive README.

<!-- BEGIN FLOWMARK INTEGRATION format=f03 surface=agents-md -->
## flowmark

Auto-format Markdown with `flowmark` for clean, semantic git diffs.

- Run `flowmark --auto <files>` on Markdown you create or edit.
- Run `flowmark --docs` for full usage and `flowmark --skill` for the skill.
- If `flowmark` is not on `PATH`, use a pinned `uvx` runner (never `@latest`).
- Fast Rust port (recommended): `uvx --from flowmark-rs==0.3.2 flowmark`.
- Python build (library / newest patch): `uvx --from flowmark==0.7.2 flowmark`.

<!-- END FLOWMARK INTEGRATION -->

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->

<!-- BEGIN PPROSE INTEGRATION format=f02 -->
## Practical Prose (pprose)

Practical Prose: an evaluation toolkit and editorial workflows for practical documents.
Use when the user asks to improve, audit, score, or compare practical documents.

For durable Markdown documentation, use `pprose-common-edit` whenever creating, editing,
reviewing, or reorganizing it, unless the task is explicitly read-only.
Keep the required guideline footer intact.

Apply AI-slop reduction whenever drafting or editing prose, not only on request: use
`pprose-de-slop` to remove AI-writing tells and formulaic LLM prose, applying its
bundled catalog contextually and preserving meaning and voice.

Discover the tool from the CLI itself: `pprose --help` for commands, `pprose about` for
the project narrative, `pprose skill` for the workflow skills, and `pprose list` for
every on-demand guideline, shortcut, and runbook
(`pprose guidelines|shortcut|runbook <name>` prints one).

Run pprose as `pprose <command>` if on PATH, else `uvx pprose@0.4.0 <command>`
(zero-install via uv).

<!-- END PPROSE INTEGRATION -->
