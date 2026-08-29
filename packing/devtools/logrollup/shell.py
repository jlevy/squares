"""Resolving a shell command to the tool it actually runs.

Part of the systematic half of the rollup, not the Claude half: any harness that records
shell commands can key on this, and Codex records them too.

**The leading word of a command is a poor identity.** In one measured session `cd` led
524 of 882 commands, because nearly every one opened with `cd /repo && ...`, and `uv`
accounted for much of the rest because the real tool sat behind `uv run --frozen --group
dev`. A rollup keyed on that answers no question.

So a command is split into segments, each is peeled of assignments, flags and redirects,
and what remains is named as it was invoked: the runner prefix is kept because
`uv run foo.py` is a different thing from `foo.py`, and a Python call is named by the
module or script it runs because `python` alone says nothing.

A name carries identity and never an argument value, a path beyond a script's own
basename, or a literal.
"""

from __future__ import annotations

import re
import shlex
from dataclasses import dataclass
from enum import StrEnum

SEGMENT = re.compile(r"&&|\|\||;|(?<!\|)\|(?!\|)")
PIPE_JOIN = re.compile(r"(?<!\|)\|(?!\|)")
REDIRECTS = frozenset({">", ">>", "<", "<<", "2>", "2>&1", "&>", "|&"})
DURATION = re.compile(r"\d+(\.\d+)?[smhd]?")

# Wrappers that stand in front of the real tool. Kept in the name rather than discarded:
# how a tool was invoked is part of what it cost.
RUNNERS = frozenset({"uv", "uvx", "time", "timeout", "env", "nohup", "sudo", "command", "exec"})
# Shell syntax, not tools. Splitting a loop on `;` leaves `do`, `done` and `break` looking
# like commands, and counting them as invocations buries the tools underneath noise.
KEYWORDS = frozenset(
    {
        "do",
        "done",
        "for",
        "while",
        "until",
        "if",
        "then",
        "fi",
        "else",
        "elif",
        "case",
        "esac",
        "break",
        "continue",
        "function",
        "return",
        "in",
        "select",
    }
)
# Runner flags that consume the next token, which would otherwise read as the tool.
VALUE_FLAGS = frozenset(
    {"--from", "--with", "--group", "--python", "--project", "--directory", "-p"}
)
# Tools whose subcommand is the interesting half: `git commit` and `git status` are not
# the same activity, and collapsing them to `git` loses what the session was doing.
SUBCOMMANDED = frozenset(
    {"git", "gh", "tbd", "cargo", "npm", "make", "ruff", "pip", "docker", "pprose"}
)
# Text munging that is the point of a command when it leads one and incidental when it
# follows a pipe. Position decides: `grep -rn x .` is the work, `... | grep x` filters
# someone else's.
FILTERS = frozenset(
    {
        "head",
        "tail",
        "wc",
        "sort",
        "uniq",
        "cut",
        "tr",
        "sed",
        "awk",
        "grep",
        "rg",
        "jq",
        "xargs",
        "tee",
        "column",
        "less",
        "cat",
        "sponge",
    }
)


class Family(StrEnum):
    """What kind of tool an invocation is.

    The distinction the efficiency work needs is our own instruments against everything
    else: time in `packing-validate` is the gate, and time in `grep` is orientation.
    """

    project = "project"
    toolchain = "toolchain"
    vcs = "vcs"
    inspection = "inspection"
    filesystem = "filesystem"
    shell = "shell"
    other = "other"


PROJECT_PREFIXES = ("packing-", "sqpack", "sqsearch", "devtools.", "cases.", "benchmarks.")
FAMILIES: dict[str, Family] = {
    name: family
    for family, names in (
        (
            Family.toolchain,
            (
                "uv uvx python python3 pytest ruff basedpyright pyright make node npm"
                " cargo rustc flowmark tbd pprose softschema jq curl docker"
            ),
        ),
        (Family.vcs, "git gh lefthook"),
        (
            Family.inspection,
            "grep rg sed awk cat head tail wc find ls tree diff sort uniq du df ps file",
        ),
        (Family.filesystem, "mkdir rm cp mv touch chmod rmdir ln tar unzip"),
        (Family.shell, "cd echo true false test export date sleep printf which type set"),
    )
    for name in names.split()
}


@dataclass(frozen=True, slots=True)
class Invocation:
    """One resolved tool call: how it was invoked, and what kind of tool it is."""

    name: str
    family: Family

    @property
    def is_shell_bookkeeping(self) -> bool:
        return self.family is Family.shell


PIPELINE = Invocation(name="(pipeline)", family=Family.other)
"""The name for a command no single tool owns. Parenthesised so it cannot be mistaken
for an executable that exists."""


def basename(token: str) -> str:
    """The last path element of a token, never empty.

    Trailing slashes are stripped first: `packing/` would otherwise reduce to the empty
    string and leave an unnameable invocation, which is how a real transcript crashed
    this resolver.
    """
    trimmed = token.rstrip("/")
    return trimmed.rsplit("/", 1)[-1] or token


def family_of(name: str) -> Family:
    """The family a bare tool or module name belongs to."""
    if name.startswith(PROJECT_PREFIXES):
        return Family.project
    return FAMILIES.get(name, Family.other)


def _meaningful(tokens: list[str]) -> list[str]:
    """Tokens with assignments, flags, and everything after a redirect removed."""
    kept: list[str] = []
    skip_next = False
    for token in tokens:
        if skip_next:
            skip_next = False
            continue
        if token in REDIRECTS:
            break
        if token.startswith("-"):
            skip_next = token in VALUE_FLAGS
            continue
        if "=" in token and not token.startswith("/") and not kept:
            continue  # a leading VAR=value assignment
        kept.append(token)
    return kept


def _python_target(tokens: list[str], words: list[str]) -> str | None:
    """The module or script a Python invocation runs, or None for `-c` and heredocs."""
    if "-m" in tokens:
        after = tokens[tokens.index("-m") + 1 :]
        return next((t for t in after if not t.startswith("-")), None)
    return next((basename(w) for w in words if w.endswith(".py")), None)


def resolve(segment: str) -> Invocation | None:
    """One command segment, named as it was invoked.

    `uv run --frozen packing-validate --records` is `uv run packing-validate`;
    `python3 foo.py > out.txt` is `python3 foo.py`; `git commit -q` is `git commit`.
    The runner prefix stays because it is part of how the time was spent, and the family
    comes from the tool rather than from the runner in front of it.
    """
    try:
        tokens = shlex.split(segment)
    except ValueError:
        return None
    words = [w for w in _meaningful(tokens) if basename(w) not in KEYWORDS]
    if not words:
        return None

    prefix: list[str] = []
    index = 0
    while index < len(words) and basename(words[index]) in RUNNERS:
        runner = basename(words[index])
        prefix.append(runner)
        index += 1
        if index < len(words) and words[index] == "run":
            prefix.append("run")
            index += 1
        elif index < len(words) and runner == "timeout" and DURATION.fullmatch(words[index]):
            # `timeout 600 cmd` would otherwise name the call after its duration.
            index += 1
    if index >= len(words):
        # A bare runner with nothing after it, such as `time` alone.
        return Invocation(name=" ".join(prefix), family=Family.toolchain)

    head = basename(words[index])
    rest = words[index + 1 :]
    if head.startswith("python"):
        target = _python_target(tokens, rest)
        parts = [*prefix, head, *(["-m", target] if "-m" in tokens and target else [])]
        if target and "-m" not in tokens:
            parts.append(target)
        return Invocation(name=" ".join(parts), family=family_of(target or head))
    family = family_of(head)
    # Our own CLIs carry subcommands too, and `packing-ledger check` is not
    # `packing-ledger render`. Keyed off the family rather than a second list, so a new
    # project CLI is distinguished without anyone remembering to enumerate it.
    if rest and (head in SUBCOMMANDED or family is Family.project):
        return Invocation(name=" ".join([*prefix, head, basename(rest[0])]), family=family)
    return Invocation(name=" ".join([*prefix, head]), family=family)


def invocations(command: object) -> tuple[Invocation, ...]:
    """Every tool one shell command invokes, in order.

    A segment that will not lex yields nothing rather than a guess: a rollup that
    silently mis-attributes is worse than one reporting fewer calls than were made.
    """
    if not isinstance(command, str) or not command.strip():
        return ()
    found = (resolve(segment) for segment in SEGMENT.split(command) if segment.strip())
    return tuple(call for call in found if call is not None)


def primary(command: object) -> Invocation | None:
    """The one name a command's elapsed time is attributed to.

    A command with a single major tool is named by it, so `cd /repo && packing-validate`
    is a validation call and `grep -rn x . | head` is a search. A command with several is
    `(pipeline)`, whether joined by a pipe or by `&&`: the two differ in how output moves,
    not in whether one tool owns the time, and giving a whole chain's time to whichever
    ran first is how the previous keying went wrong.

    Shell bookkeeping is never major, and a text-munging tool is major only when it leads
    the command rather than filtering something else's output.
    """
    found = invocations(command)
    if not found:
        return None
    major = [
        call
        for position, call in enumerate(found)
        if not call.is_shell_bookkeeping
        and (position == 0 or call.name.rsplit(" ", 1)[-1] not in FILTERS)
    ]
    if len(major) == 1:
        return major[0]
    if len(major) > 1:
        return PIPELINE
    return found[0]
