"""The JavaScript the checkers run in the page, as files rather than Python string literals.

The checkers drive the built page through `page.evaluate`, and what they hand it is
JavaScript. Written as a Python string it is invisible to every tool either language has:
no formatter indents it, no linter parses it, no editor colours it, and an escape that is
wrong in Python is silently wrong in the browser. That is not hypothetical here -- a TeX
`\\le` written with a doubled backslash inside an f-string reached the rendered page and
broke a line of mathematics in two, because nothing between the author and the browser
could read the string as code.

So a probe is a file. `probes/<name>.js` holds one JavaScript **expression** -- almost
always an arrow function -- and `probe("<name>")` returns its text:

    from probes import probe
    box = page.evaluate(probe("panel/slots"), {"n": 26})

**Values reach a probe as its one argument, never by interpolation.** Playwright passes a
single JSON-serialisable argument, so a probe that needs `n` takes `(o) => ...` and reads
`o.n`. Building the JavaScript by formatting Python values into it is the habit this
module exists to end: it is what makes the text unparseable, and it is where the escaping
bugs come from.

Names may nest (`probes/gapbar/labels.js` is `probe("gapbar/labels")`), which is how one
checker's probes stay together.
"""

from functools import lru_cache
from pathlib import Path

PROBES = Path(__file__).resolve().parent / "probes"


@lru_cache(maxsize=None)
def probe(name: str) -> str:
    """The text of `probes/<name>.js`, read once and kept.

    Raises `FileNotFoundError` with the full path if it is missing, which is the useful
    failure: a probe named wrongly should say so at the first call rather than arrive in
    the browser as `undefined`.
    """
    path = PROBES / (name + ".js")
    if not path.is_file():
        raise FileNotFoundError(f"no probe at {path}")
    return path.read_text(encoding="utf-8")
