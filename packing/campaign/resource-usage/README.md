# Resource Usage

One schema-validated record per agent session log, and **the record is the retained
artifact rather than a pointer to one.**

The raw JSONL a coding harness writes is large, harness-private, and full of prose this
repository has no reason to keep, so it will not always be archived.
This session’s transcript was 8.4 MB; its record is 8.3 KB, which is small enough to
live in git and detailed enough to answer the questions the efficiency work asks.

## What is here

|  |  |
| --- | --- |
| `<session-id>.yaml` | One [`ClaudeEfficiencyRollup/v1`](../schemas/claude-efficiency-rollup.schema.yaml) record, written by `devtools.claude_log_rollup` |

`devtools.codex_log_rollup` is the sibling reader for Codex transcripts and emits
`CodexEfficiencyRollup/v2`. The two are separate on purpose: the harnesses record
genuinely different things, and one shape over both would either discard what one knows
or invent fields the other cannot fill.
A unified `EfficiencyRollup` that both map into is `BC-075`’s, and it is the only thing
downstream should read.

```bash
uv run --frozen python -m devtools.claude_log_rollup LOG.jsonl --out campaign/resource-usage
```

## What survives, and what does not

**Kept:** per-tool-call identity and elapsed time, per-turn token accounting, thinking
level, model, the branch each turn ran against, and the SHA-256 of the source log so two
records can be told apart.

**Dropped, and stated because a record whose losses are undocumented gets read as
complete:** every prose body — assistant text, thinking text, user messages, tool
`stdout` and `stderr`, file contents, and diffs.
A shell command is reduced to its leading executable word, which is identity rather than
content. Nothing reconstructs a command line from these files.

## Reading the numbers

Each record carries its own `semantics` block, and it is required by the schema rather
than conventional, because a figure whose meaning is not beside it gets read as whatever
the reader assumes. Three that matter:

- **`wall_seconds` is elapsed session time**, including every interval in which nothing
  was running. It is an upper bound on work and never a measure of it.
- **`share_of_wall` can exceed one.** Concurrent tool calls are summed independently, so
  it is a load figure, not an occupancy figure.
- **`model_seconds` is unavailable for Claude Code**, which records no timed
  model-stream items and no first-token latency.
  It is absent rather than zero, and a consumer summing it with a harness that does
  report it has to carry the gap forward instead of letting a zero flatter the total.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
