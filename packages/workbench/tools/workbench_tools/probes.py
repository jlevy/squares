"""The JavaScript the checkers run in the page, as files rather than Python string literals.

This is the repository's one probe loader, `sqpack.probes`, bound to this package's own
`probes/` directory. The contract is written there: a probe is a `.js` file holding one
JavaScript expression, and values reach it as its one argument, never by interpolation.

    from workbench_tools.probes import probe
    box = page.evaluate(probe("panel/slots"), {"n": 26})

Names may nest (`probes/gapbar/labels.js` is `probe("gapbar/labels")`), which is how one
checker's probes stay together.

A binding rather than a second copy: the package already imports `sqpack` at runtime, so
there is nothing that would justify two implementations of one convention.
"""

from pathlib import Path

from sqpack.probes import probe as load_probe

PROBES = Path(__file__).resolve().parents[2] / "probes"


def probe(name: str) -> str:
    """The text of `probes/<name>.js`, read once and kept.

    Raises `FileNotFoundError` with the full path if it is missing, which is the useful
    failure: a probe named wrongly should say so at the first call rather than arrive in
    the browser as `undefined`.
    """
    return load_probe(PROBES, name)
