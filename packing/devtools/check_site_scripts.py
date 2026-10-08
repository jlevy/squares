"""Inventory every published script against reviewed startup and interaction families.

Names deliberately omit asset hashes: the reviewed program family, rather than a
specific byte digest, owns the declaration. Unknown programs fail the build. Browser
load checks separately verify that declared enhancements preserve readable initial HTML.
"""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

# The only exceptions to static primary content are the interactive workbench and
# allowlisted old-address forwarding. Every other program enhances existing HTML.
FAMILIES = {
    "theme": (
        "input-response",
        "Reader theme choice; persisted attributes are set before paint.",
    ),
    "table": (
        "input-response",
        "Sort/filter complete static rows; query presets select existing rows.",
    ),
    "popover": ("input-response", "Enhance native popovers containing prepared content."),
    "row-popover": (
        "input-response",
        "Open a canonical result article after a row is pressed.",
    ),
    "case-popover": (
        "input-response",
        "Open a canonical case record after a case link is pressed.",
    ),
    "case-page": (
        "registered-forwarder",
        "Resolve known legacy case-index query/fragment aliases to canonical records.",
    ),
    "film": ("non-layout", "Play within a poster's reserved media rectangle."),
    "atlas-grid": ("non-layout", "Enhance existing tiles inside a reserved grid."),
    "atlas-view": ("input-response", "Apply requested atlas layout to existing static tiles."),
    "kpress-behaviors": (
        "non-layout",
        "TOC, navigation and overlay wiring over static document content.",
    ),
    "katex-math": (
        "input-response",
        "Math engine for interactive paper controls and reader font choices.",
    ),
    "forward": (
        "registered-forwarder",
        "Preserve only registered moved addresses and frozen historical fragments.",
    ),
    "not-found": (
        "registered-forwarder",
        "Resolve only allowlisted case/result aliases under the project root.",
    ),
    "published": (
        "workbench-application",
        "Load and validate the interactive workbench corpus; failure remains visible.",
    ),
    "workbench": (
        "workbench-application",
        "Interactive packing application; primary document headings/help are static.",
    ),
}
# Paper publication links pre-existing inline programs as page.<hash>.js. These
# stable source markers give each retained program its own reviewed declaration.
PAPER_PROGRAMS = (
    (
        "Typesets a kpress page's formulas",
        "non-layout",
        "Readiness wiring skips already prepared primary mathematics.",
    ),
    ("The reader's colour theme:", "input-response", "Reader theme controls."),
    (
        "shared: certificate picker and queued static math",
        "input-response",
        "Certificate picker over prepared math; dynamic readouts follow input.",
    ),
    (
        "Certificate C-n011-fractional-",
        "input-response",
        "Interactive certificate diagrams in reserved SVG rectangles.",
    ),
    (
        "kpress client behaviors, flattened from",
        "non-layout",
        "Wire document overlays/tooltips/copy without replacing primary content.",
    ),
    (
        "Keep SVG labels at the publication support-text size",
        "non-layout",
        "Adjust labels inside fixed SVG geometry.",
    ),
)
HEAD_PROGRAMS = (
    (
        "Protocol-aware first-screen font preloads:",
        "pre-paint",
        "Activate owned font hints with protocol-correct credentials before stylesheets.",
    ),
    (
        "KPress pre-paint bootstrap",
        "pre-paint",
        "Set persisted reader attributes before body paint.",
    ),
    (
        "A site page shown inside another page",
        "pre-paint",
        "Set embed and allowlisted atlas attributes before body paint.",
    ),
    (
        "CoreText uses linear advances",
        "pre-paint",
        "Select the host font hinting attribute before body paint.",
    ),
)


@dataclass(frozen=True)
class Script:
    source: str
    category: str
    reason: str
    bytes: int


def classify(source: str, text: str, *, inline: bool = False) -> Script:
    """Classify a reviewed program; fail closed when a new family is shipped."""
    if inline:
        if text.lstrip().startswith("// Input response and registered forwarding:"):
            category, reason = FAMILIES["forward"]
            return Script(source, category, reason, len(text.encode()))
        if len(text.encode()) > 4096:
            raise ValueError(f"inline startup script exceeds 4096 bytes: {source}")
        for marker, category, reason in HEAD_PROGRAMS:
            if marker in text[:500]:
                return Script(source, category, reason, len(text.encode()))
    else:
        family = re.sub(r"\.[0-9a-f]{16}(?=\.js$)", "", Path(source).name).removesuffix(".js")
        if family in FAMILIES:
            category, reason = FAMILIES[family]
            return Script(source, category, reason, len(text.encode()))
        for marker, category, reason in PAPER_PROGRAMS:
            if marker in text[:500]:
                return Script(source, category, reason, len(text.encode()))
        # Linked paper helpers retain their names inside the tiny program; they
        # reserve/release a preparation promise and never typeset primary content.
        if len(text) < 100 and "finishMathBootstrap" in text:
            return Script(
                source,
                "non-layout",
                "Release the prepared-math readiness promise.",
                len(text.encode()),
            )
        if "squaresMath" in text and "katex" in text and len(text) > 100_000:
            return Script(
                source,
                "input-response",
                "Pinned KaTeX and kpress metrics for interactive paper controls.",
                len(text.encode()),
            )
    raise ValueError(f"unclassified executable script: {source}")


class _Scripts(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.items: list[tuple[dict[str, str | None], str]] = []
        self.attributes: dict[str, str | None] | None = None
        self.parts: list[str] = []
        self.application: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        application = values.get("data-application-src")
        if application:
            self.application.append(application)
        if tag == "script":
            self.attributes = values
            self.parts = []

    def handle_data(self, data: str) -> None:
        if self.attributes is not None:
            self.parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self.attributes is not None:
            self.items.append((self.attributes, "".join(self.parts)))
            self.attributes = None


def inventory(directory: Path) -> tuple[list[Script], list[str]]:
    """Inspect executable tags and linked application programs, including unused assets."""
    from devtools.render_overview import SITE_URL  # noqa: PLC0415

    root = directory.resolve()
    project_root = urlsplit(SITE_URL).path
    declarations: dict[str, Script] = {}
    failures: list[str] = []

    def linked(page: Path, src: str) -> None:
        address = urlsplit(src)
        if address.scheme or address.netloc:
            failures.append(
                f"script must be a relative first-party asset: {page.relative_to(root)}: {src}"
            )
            return
        asset_path = unquote(address.path)
        if asset_path.startswith("/"):
            if not asset_path.startswith(project_root):
                failures.append(f"root-absolute script is outside the project: {src}")
                return
            path = (root / asset_path.removeprefix(project_root)).resolve()
        else:
            path = (page.parent / asset_path).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            failures.append(f"script asset missing or outside publication: {src}")
            return
        name = path.relative_to(root).as_posix()
        if name not in declarations:
            try:
                declarations[name] = classify(name, path.read_text(encoding="utf-8"))
            except ValueError as error:
                failures.append(str(error))

    for page in sorted(root.rglob("*.html")):
        parsed = _Scripts()
        parsed.feed(page.read_text(encoding="utf-8"))
        for index, (attributes, text) in enumerate(parsed.items):
            if attributes.get("type") in {"application/json", "application/ld+json"}:
                continue
            if src := attributes.get("src"):
                linked(page, src)
            elif text.strip():
                name = f"{page.relative_to(root)}#script-{index + 1}"
                try:
                    declarations[name] = classify(name, text, inline=True)
                except ValueError as error:
                    failures.append(str(error))
        for src in parsed.application:
            linked(page, src)
    for path in sorted(root.rglob("*.js")):
        name = path.relative_to(root).as_posix()
        if name not in declarations:
            try:
                declarations[name] = classify(name, path.read_text(encoding="utf-8"))
            except ValueError as error:
                failures.append(str(error))
    return list(declarations.values()), sorted(set(failures))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument(
        "--json", action="store_true", help="Emit the complete shipped inventory"
    )
    args = parser.parse_args(argv)
    records, failures = inventory(args.directory)
    if args.json:
        print(
            json.dumps(
                {"scripts": [asdict(row) for row in records], "failures": failures}, indent=2
            )
        )
    else:
        print(f"script inventory: {len(records)} declarations, {len(failures)} failures")
        for failure in failures:
            print(failure)
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
