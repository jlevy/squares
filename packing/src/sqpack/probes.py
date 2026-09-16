"""Browser code as files: the one loader for every Python tool that drives a page.

A Python tool that drives a browser hands it JavaScript -- through Playwright's `evaluate`,
`wait_for_function` or `add_init_script`. Written as a Python string, that JavaScript is
invisible to every tool either language has: no formatter lays it out, no linter parses it,
no type checker reads it, and an escape that is wrong in Python is silently wrong in the
browser. That is not hypothetical here: a TeX `\\le` doubled inside an f-string reached a
rendered page and broke a line of mathematics in two, because nothing between the author
and the browser could read the string as code.

So JavaScript in a Python string is not allowed anywhere in this repository, and
`devtools.check_no_embedded_js` fails the gate on it. A **probe** is what replaces it:

- a `.js` file under a directory named `probes`, holding one JavaScript **expression** --
  almost always an arrow function -- which Biome formats and lints and `tsc` type-checks;
- named by its path under that directory without the suffix, so
  `packing/devtools/probes/check_published_site/startup.js` is
  `probe(PROBES, "check_published_site/startup")` from a module whose `PROBES` is
  `packing/devtools/probes`;
- grouped one directory per tool, beside the tools that use it: `packing/devtools/probes/`,
  `packing/tests/probes/`, a spike's own `probes/`.

**Values reach a probe as its one argument, never by interpolation.** Playwright passes a
single JSON-serialisable argument, so a probe that needs `n` takes `(o) => ...` and reads
`o.n`:

    PROBES = Path(__file__).resolve().parent / "probes"
    box = page.evaluate(probe(PROBES, "check_layout/slots"), {"n": 26})

`add_init_script` is the one entry point that takes no argument; `applied` gives it the
probe already called, with no argument or with one serialised as JSON rather than
formatted.

`devtools.check_probes` keeps every probe tree honest: each file parses as a function, each
is named by a Python file beside its directory, and each name a Python file uses has a
file. It finds names by reading string literals, so a probe name is always written out
whole, never assembled.

The workbench package's `workbench_tools.probes` is this loader bound to the package's own
`probes/` directory, so its checkers keep calling `probe("<name>")` with one argument.
"""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path, PurePosixPath

SUFFIX = ".js"


@cache
def probe(root: Path, name: str) -> str:
    """The text of `<root>/<name>.js`, read once per process and kept.

    Raises `FileNotFoundError` with the full path when the file is missing, which is the
    useful failure: a probe named wrongly says so at the first call rather than arriving
    in the browser as `undefined`. Raises `ValueError` for a name that is not a plain
    relative path under `root`. Neither is cached, so a probe written after a failed call
    is found by the next one.
    """
    parts = PurePosixPath(name).parts
    if not parts or name.startswith("/") or ".." in parts or name.endswith(SUFFIX):
        raise ValueError(f"not a probe name: {name!r}")
    path = root.resolve().joinpath(*parts[:-1], parts[-1] + SUFFIX)
    if not path.is_file():
        raise FileNotFoundError(f"no probe at {path}")
    return path.read_text(encoding="utf-8")


#: Stands for "no argument", which is not the same call as an argument of `None`: a probe
#: with a default parameter sees `undefined` in the first case and `null` in the second.
_NO_ARGUMENT = object()


def applied(source: str, argument: object = _NO_ARGUMENT) -> str:
    """A probe's source called once, as one script for `add_init_script`.

    With `argument`, the call passes it serialised by `json.dumps`, which escapes every
    character JavaScript could misread; JSON is a JavaScript expression. That is the
    boundary Playwright itself draws for `evaluate`, drawn once here instead of at each call
    site. Without one, the probe is called with no argument at all.
    """
    expression = source.strip().removesuffix(";")
    passed = "" if argument is _NO_ARGUMENT else json.dumps(argument, allow_nan=False)
    return f"({expression}\n)({passed});\n"
