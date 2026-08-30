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
| `<session-id>.yaml` | One [`ClaudeEfficiencyRollup/v1`](../schemas/claude-efficiency-rollup.schema.yaml) record, written by `devtools.logrollup.claude` |

The harness is detected from the log’s content, so one command serves every reader.

[`devtools/logrollup/`](../../devtools/logrollup/) is where the split between systematic
and per-agent lives.
`model.py` holds what a rollup *is* for any harness — a content-identified source, a
span, turns, tool calls, and a required `semantics` block — and `reader.py` holds the
protocol and registry that find a reader by reading the file rather than trusting its
name. Everything else is per-harness: adding one is a module and a line in `REGISTRY`.

`devtools.codex_log_rollup` emits `CodexEfficiencyRollup/v2` and is deliberately **not**
registered, for a real difference rather than an oversight: its unit is a tree of Codex
task sessions under a root id, not one file, so it answers a question this registry’s
one-log-in, one-record-out shape cannot ask.
A unified `EfficiencyRollup` that both map into is `BC-075`’s, and it is the only thing
downstream should read.

```bash
uv run --frozen python -m devtools.log_rollup LOG.jsonl --out campaign/resource-usage
```

## What survives, and what does not

**Kept:** per-tool-call identity and elapsed time, per-turn token accounting, thinking
level, model, the branch each turn ran against, and the SHA-256 of the source log so two
records can be told apart.

**Dropped, and stated because a record whose losses are undocumented gets read as
complete:** every prose body — assistant text, thinking text, user messages, tool
`stdout` and `stderr`, file contents, and diffs.
A shell command is reduced to the tool it runs and a structural shape, both identity
rather than content.
Nothing reconstructs a command line from these files.

**One record per log, named by the log’s own stem.** A subagent transcript carries its
parent’s `session_id`, so keying the filename on that would overwrite the parent’s
record with the last subagent’s.

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
