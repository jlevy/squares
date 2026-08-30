"""Efficiency rollups over coding-agent session logs.

**Systematic across harnesses:** what a rollup *is* (`model.py`), how a reader is found
and dispatched (`reader.py`), and the emit path in `devtools.log_rollup`. Every record
carries a source identified by content hash, a span, and a `semantics` block, and every
record excludes prose.

**Customised per harness:** everything between opening the file and filling in
`SessionRollup.extra`. Codex and Claude Code record genuinely different things, and one
parser over both would either discard what one knows or invent fields the other cannot
fill.

Adding a harness is one module and one line in `REGISTRY`. A reader owes three things: a
`harness` name, a `detects` that reads content rather than trusting a filename, and a
`read` returning a `SessionRollup` whose `semantics` names every figure the harness
cannot supply.

`devtools.codex_log_rollup` is not registered here, and the reason is a real difference
rather than an oversight: its unit is a *tree of Codex task sessions under a root id*,
not one file, so it answers a question this registry's one-log-in, one-record-out shape
cannot ask. Bringing it in means either exposing a public single-session parse there or
widening the protocol to take a task selector, and that is a decision with a design in it
rather than a wrapper.
"""

from __future__ import annotations

from devtools.logrollup.claude import ClaudeCodeReader
from devtools.logrollup.model import (
    Elapsed,
    SessionRollup,
    SourceLog,
    Span,
    ToolCall,
    Turn,
)
from devtools.logrollup.reader import HarnessReader, Registry, build_registry

REGISTRY: Registry = build_registry([ClaudeCodeReader()])

__all__ = [
    "REGISTRY",
    "ClaudeCodeReader",
    "Elapsed",
    "HarnessReader",
    "Registry",
    "SessionRollup",
    "SourceLog",
    "Span",
    "ToolCall",
    "Turn",
    "build_registry",
]
