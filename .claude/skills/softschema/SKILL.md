---
name: softschema
description: >-
  Validate YAML and Markdown artifacts with gradual contracts. Use for Markdown
  with YAML frontmatter or pure YAML records, soft/permissive/enforced schema
  maturity, record enhancement, agent and software pipelines, import staging,
  or running the `softschema` CLI.
allowed-tools: ["Bash(softschema:*)"]
---
<!-- DO NOT EDIT format=f02: written by `softschema skill --install`.
Re-run that command to update.
-->

# softschema Skill

`softschema` adds gradual contracts to YAML data.
The standard profile is Markdown with YAML frontmatter and an optional body.
Pure YAML is also supported when the structured record stands on its own.
This skill is a routing layer.
The CLI documents itself, so load only the command output you actually need.

## When to Use

A workflow needs reliable YAML values before the final record shape is known, or a
record needs prose context beside its structured payload.
Use the contract-status progression to refine records for agent steps, software
consumers, or a later strict database or API boundary.

## Pick One Runner First

Pick one command prefix, then use it for every command in this skill.
In examples, `$SS ...` means “run the selected prefix with these arguments.”

1. If `softschema --version` works, use `SS='softschema'`.
2. Else if `uvx --version` works, use `SS='uvx softschema@latest'`.
3. Else if `npx --version` works, use `SS='npx -y softschema@latest'`.
4. Else install uv (`curl -LsSf https://astral.sh/uv/install.sh | sh` or
   `brew install uv`) or Node (`brew install node`), then retry.

The zero-install fallback resolves the latest published release.
Prefer an installed project command when one is available; use a lockfile-backed project
dependency when the version must be repeatable (see `$SS docs installation`).

`$SS doctor` reports the installed version, available runners, and recommended command
prefix.

## Bootstrap

Each command prints material the agent should read and follow:

```bash
$SS --help                  # command listing + entry-point pointers
$SS skill --brief           # compact operating brief
$SS docs guide              # mental model and adoption path
$SS docs spec               # exact artifact format
$SS docs example-artifact   # a copyable example
$SS docs --list             # full topic index
```

## Operating Brief

<!-- BEGIN SOFTSCHEMA BRIEF -->
Use soft schemas when humans, agents, or software produce YAML records whose consumed
structure should stabilize over time.

- Choose the artifact profile independently of the contract status.
  Use the standard `frontmatter-md` profile when the YAML payload benefits from a
  Markdown body carrying context; use `pure-yaml` when the whole artifact is structured.
- YAML is authoritative for any consumed value.
  In `frontmatter-md`, the Markdown body is reader-facing.
  Do not parse Markdown body prose or tables for structured fields.
- Treat `soft`, `permissive`, and `enforced` as boundary maturity.
  Start with a named convention, validate the stable fields under authored rules, and
  enforce a bound structural schema when undeclared fields should fail.
- Evolve the schema as records and consumers reveal stable fields and constraints.
  Changing the schema or status does not require changing a Markdown body.
- Date- and timestamp-shaped YAML scalars are portable strings, quoted or unquoted.
  JSON Schema `format` is annotation-only; use a semantic model or an explicit
  structural assertion when date validity matters.
- The `softschema:` block is the self-description quartet: `contract` (the payload
  contract ID), `schema` (relative path to the compiled schema), `envelope` (the payload
  key), `status` (strictness).
  A fully self-describing artifact validates with `$SS validate <artifact>`, no flags.
- Add a field to the contract when a consumer relies on its name and meaning.
  Leave uncertain YAML extensions outside the contract until they stabilize.
- Use the optional Markdown body for provenance, reasoning, and caveats that do not fit
  fixed fields.
- Read `$SS docs guide` for the mental model.
- Read `$SS docs spec` for the exact artifact format.
- Inspect `$SS docs example` and `$SS docs example-artifact` for the copyable movie
  example; `$SS docs example-schema` prints its compiled schema.
- Validate at the boundary with `$SS validate`: no flags for a self-describing artifact;
  `--schema` to override with a compiled schema; `--model` for a Pydantic/Zod model
  (imports and runs local code; trusted models only; `--schema` is the safe path for
  untrusted input). Run `$SS validate --help` for exact syntax.
- **Check your own artifact before you finish, with `$SS repair`.** After writing a
  contract-bearing artifact, run it on that file.
  It fixes the two mistakes a model makes writing YAML by hand — an unquoted `: ` inside
  a value, and a scalar like `1850` that reads as a number where the contract wants a
  string — writes the file, and reports the verdict.
  Anything it does not fix, such as a missing field or a key that is a near-miss for the
  declared one, is yours to correct: it reports those and never guesses at them.
  A document it cannot read at all comes back as a record naming why, which is what a
  truncated write leaves behind.
  Add `--dry-run` to see what would change without writing, or `--check` to fail
  whenever anything would change, which is what a gate wants.
  `$SS validate` never writes; it is what a consumer runs, and it refuses an artifact it
  cannot read rather than reporting one.
- Keep examples copyable; do not scaffold or mutate a target project unless the user
  explicitly asks for that workflow.

<!-- END SOFTSCHEMA BRIEF -->

## Install

softschema ships two interchangeable implementations with the same CLI surface; pick the
runtime you already have.
Use a zero-install runner:

```bash
# Python (Pydantic):
uvx softschema@latest --help            # ephemeral, latest published release
uv tool install softschema             # persistent

# TypeScript (Zod):
npx -y softschema@latest --help         # ephemeral, latest published release
```

Both expose the same commands and flags and validate against the same canonical schema;
the only difference is whether models are written as Pydantic or Zod.

## Self-Install (Optional)

Run once per project to install discoverable mirrors of this skill, so any agent working
in the repo finds it natively:

```bash
$SS skill --install --scope project --agent portable --agent claude
# writes:
#   .agents/skills/softschema/SKILL.md   (Codex, Gemini CLI, cross-agent installers)
#   .claude/skills/softschema/SKILL.md   (Claude Code mirror)
```

The mirrors carry a `DO NOT EDIT` marker.
Re-run the same explicit install command to refresh after upgrading.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
