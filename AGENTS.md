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

## Starting Research Work

The entry point for the next research loops is the synopsis’s
[current handoff](SYNOPSIS.md#current-handoff): it names the active agenda, the exact
next bounded slice, and the owning bead.
The active agenda’s session queue owns priority ordering.
`tbd ready` includes the historical backlog and is an input to a coordinator checkpoint,
not the queue itself — do not pick work from it directly when a handoff and agenda
exist.

## Build & Test

The repository is mostly prose.
The only repo-wide tooling is Markdown formatting.

```bash
make hooks-install   # once after cloning: installs the lefthook pre-commit hook
make format          # format all Markdown
make format-check    # report drift without writing
```

Python, Rust, and research validation are documented in
[`development.md`](development.md).
Run them from `packing/`, which is where the project’s `pyproject.toml` and lockfile
live: `uv run --frozen --all-extras --group dev packing-validate --fast` while editing,
and the full `packing-validate` at a research or merge checkpoint.

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
  Two exclusions qualify: the literature archive under `packing/resources/`, and the
  generated `SKILL.md` files.
  The archive is excluded for a measured reason — flowmark inserts line breaks *inside*
  `$...$` spans when it rewraps, which on 2026-08-22 broke 31 of 339 math spans in one
  transcription and 101 of 1236 in another.
  A newline mid-formula defeats `grep`, and local searchability is the entire point of
  that archive. Do not drop these exclusions without re-measuring.
- **The hook formats the whole repository, not the staged files.** Flowmark reads
  `.flowmarkignore` relative to its target argument, so passing explicit paths silently
  bypasses the exclusion list.
  That matters here: `.flowmarkignore` protects `packing/resources/`, where the
  `.raw.md` extractions are byte-level ground truth used to check the model-assisted
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

The repository is split by audience rather than by topic.

**The root holds what a reader wants**, where it is visible on arrival:
[`README.md`](README.md) as the front door, then [`TUTORIAL.md`](TUTORIAL.md),
[`SYNOPSIS.md`](SYNOPSIS.md), [`conventions.md`](conventions.md),
[`development.md`](development.md), the generated [`defects.md`](defects.md), and
`docs/project/` for reports, reviews, specs and postmortems.

**[`packing/`](packing/) holds everything that is code, data, or research record**: the
`sqpack` package and its tests, the developer tools, the Rust search engine, the
literature archive, the frontier register, the atlas, the witnesses, and the campaign.
Keeping that one level down is what stops the root from becoming unreadable, and it is
also the build root — `pyproject.toml`, `uv.lock` and `.python-version` live there.

Two rules follow from the split, and both exist because a path now has two plausible
meanings:

- **Every declared path in the record is repository-relative.** That covers
  `recorded_in` in `packing/defects.yaml`, the document map, the logbook’s
  pipeline-change paths, and the verified-upper-bound consumer contract.
  One root, one meaning, and a path that reads the same wherever it appears.
  A packing-relative path in any of those places is a bug.
- **Python path constants name which root they mean.** `ROOT` (also `PROJECT_ROOT`,
  `PACKING`) is `packing/`; `REPO` is the repository root.
  A constant pointing at a document that lives at the root resolves from `REPO`.
  `sqpack` itself finds the project by marker discovery rather than a fixed depth, so it
  does not care where the checkout sits.

The standalone research reports this repository once carried, on topics unrelated to
packing, live in [jlevy/thinking](https://github.com/jlevy/thinking).

## Conventions & Patterns

- **The project is self-contained.** Its documents, sources, and code live in this
  repository and link to each other with relative paths.
  Reader-facing prose belongs at the root; code, data, and the research record belong
  under `packing/`. Do not add a third top-level tree for either.
- **Reports separate claims by evidential status** — proved, computationally verified,
  best known, or asserted-but-unverified — and cite primary sources near the claims they
  support.
- **Independently tracked packing work declares its entry point.** The coordinating
  agent chooses W1–W7 (or `general-improvement` only for genuine repository maintenance
  outside those workflows) from [`README.md`](README.md#workflow-entry-points) before
  beginning a session or a genuine workflow phase.
  Bounded delegated work such as formatting, lint repair, extraction, or repeated checks
  inherits the parent phase unless it opens its own independently tracked session.
  Longer sessions record workflow and primary-focus changes as ordered phases;
  [`SYNOPSIS.md`](SYNOPSIS.md#workflow-entry-contracts) owns the full contracts.
- **Multi-hour packing work starts with a time-sliced plan.** Follow the
  [bounded research cycle](packing/campaign/README.md#the-bounded-research-cycle) and
  the
  [portable session guide](packing/campaign/agent-sessions/README.md#starting-a-portable-four-hour-session).
  Unless the user sets another cadence, target a coherent integration checkpoint within
  about four hours and cap each slice at 30 minutes.
  Thirty minutes is a ceiling and review point, not a quota: close a smaller process,
  review, efficiency, or implementation slice as soon as its bounded output is complete.
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
