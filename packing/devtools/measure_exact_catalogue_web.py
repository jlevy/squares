"""Measure initial catalogue bytes and independently check the lazy data projection.

The metric is uncompressed file bytes for the default, unselected browser route.
It does not measure transfer compression, browser memory, rendering time or latency.
"""

from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import sys
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

from devtools.retained_data import read_retained_text

_CSS_URL = re.compile(r"url\(\s*['\"]?([^)'\"]+)")


class InitialAssets(HTMLParser):
    """Find automatic HTML resources and the explicitly declared lazy index."""

    def __init__(self) -> None:
        super().__init__()
        self.urls: list[str] = []
        self.styles: list[str] = []
        self.in_style = False
        self.index_url: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        source = values.get("src")
        if source and tag in {"script", "img", "iframe", "audio", "video", "source"}:
            self.urls.append(source)
        if tag == "link" and set((values.get("rel") or "").split()) & {
            "stylesheet",
            "icon",
            "preload",
            "modulepreload",
        }:
            target = values.get("href")
            if target:
                self.urls.append(target)
        if tag == "style":
            self.in_style = True
        index = values.get("data-index-url")
        if index:
            if self.index_url is not None:
                raise ValueError("multiple catalogue indexes")
            self.index_url = index
            self.urls.append(index)

    def handle_endtag(self, tag: str) -> None:
        if tag == "style":
            self.in_style = False

    def handle_data(self, data: str) -> None:
        if self.in_style:
            self.styles.append(data)


def local_path(url: str, *, base: Path, site: Path) -> Path | None:
    """Refuse uncountable remote assets and paths escaping the served site."""
    parsed = urlsplit(url.strip())
    if parsed.scheme == "data" or (not parsed.path and parsed.fragment):
        return None
    if parsed.scheme or parsed.netloc:
        raise ValueError(f"remote asset cannot be counted as local bytes: {url}")
    path = unquote(parsed.path)
    candidate = (site / path.lstrip("/") if path.startswith("/") else base / path).resolve()
    if not candidate.is_relative_to(site.resolve()):
        raise ValueError(f"asset escapes site: {url}")
    if not candidate.is_file():
        raise ValueError(f"missing asset: {url}")
    return candidate


def initial_assets(page: Path, site: Path) -> tuple[dict[str, int], Path]:
    """Count each local automatic resource once, including CSS resource references."""
    parser = InitialAssets()
    parser.feed(page.read_text(encoding="utf-8"))
    if parser.index_url is None:
        raise ValueError("browser has no data-index-url")
    index = local_path(parser.index_url, base=page.parent, site=site)
    if index is None:
        raise ValueError("index must be a local JSON file")
    pending = [(page, False)]
    for url in [*parser.urls, *_CSS_URL.findall("\n".join(parser.styles))]:
        path = local_path(url, base=page.parent, site=site)
        if path is not None:
            pending.append((path, path.suffix == ".css"))
    assets: dict[str, int] = {}
    while pending:
        path, is_css = pending.pop()
        name = path.relative_to(site.resolve()).as_posix()
        if name in assets:
            continue
        assets[name] = path.stat().st_size
        if is_css:
            for url in _CSS_URL.findall(path.read_text(encoding="utf-8")):
                referenced = local_path(url, base=path.parent, site=site)
                if referenced is not None:
                    pending.append((referenced, referenced.suffix == ".css"))
    return dict(sorted(assets.items())), index


def check_projection(register: dict[str, Any], index_path: Path, site: Path) -> dict[str, int]:
    """Compare records recursively against the register without using exporter code.

    Independently derive the intended subset: exclude superseded historical rows and
    superseded-catalogue-polynomial current notes. Every retained metadata field and
    integer coefficient must compare exactly; redundant polynomial text/LaTeX remain
    in the canonical archive.
    """
    index = json.loads(index_path.read_text(encoding="utf-8"))
    entries = index["entries"]
    if len({entry["id"] for entry in entries}) != len(entries):
        raise ValueError("duplicate browser record identity")
    base = index_path.parent.parent
    vectors = 0
    coefficients = 0

    def compare(original: Any, exported: Any) -> None:
        nonlocal vectors, coefficients
        if isinstance(original, list):
            if not isinstance(exported, list) or len(original) != len(exported):
                raise ValueError("record array differs from register")
            for left, right in zip(original, exported, strict=True):
                compare(left, right)
        elif isinstance(original, dict):
            if not isinstance(exported, dict):
                raise TypeError("record object differs from register")
            omitted = {"coefficients", "text", "latex"} if "coefficients" in original else set()
            added = {"coefficients_url", "order"} if omitted else set()
            if set(exported) != (set(original) - omitted) | added:
                raise ValueError("record metadata keys differ from register")
            for key in set(original) - omitted:
                compare(original[key], exported[key])
            if omitted:
                path = local_path(exported["coefficients_url"], base=base, site=site)
                if path is None:
                    raise ValueError("coefficient payload must be local")
                payload = json.loads(path.read_text(encoding="utf-8"))
                values = payload["coefficients"]
                if exported["order"] != "descending" or payload["order"] != "descending":
                    raise ValueError("coefficient order differs from register")
                if values != original["coefficients"] or not all(
                    isinstance(value, str) and re.fullmatch(r"[+-]?\d+", value)
                    for value in values
                ):
                    raise ValueError("coefficient strings differ from register")
                vectors += 1
                coefficients += len(values)
        elif type(original) is not type(exported) or original != exported:
            raise ValueError("record value differs from register")

    counts: dict[str, int] = {
        "omitted_superseded_historical": 0,
        "omitted_superseded_notes": 0,
    }
    for section, key in (("current", "entries"), ("historical", "historical_entries")):
        projected = [entry for entry in entries if entry["section"] == section]
        originals = register.get(key, [])
        if section == "historical":
            counts["omitted_superseded_historical"] = sum(
                original.get("kind") == "superseded" for original in originals
            )
            originals = [
                original for original in originals if original.get("kind") != "superseded"
            ]
        else:
            retained = []
            for original in originals:
                publication_record = original
                if isinstance(original.get("notes"), list):
                    notes = [
                        note
                        for note in original["notes"]
                        if not isinstance(note, dict)
                        or note.get("kind") != "superseded-catalogue-polynomial"
                    ]
                    counts["omitted_superseded_notes"] += len(original["notes"]) - len(notes)
                    publication_record = {**original, "notes": notes}
                retained.append(publication_record)
            originals = retained
        if len(projected) != len(originals):
            raise ValueError(f"{section} record count differs from register")
        counts[section] = len(originals)
        for original, entry in zip(originals, projected, strict=True):
            path = local_path(entry["metadata_url"], base=base, site=site)
            if path is None:
                raise ValueError("metadata payload must be local")
            payload = json.loads(path.read_text(encoding="utf-8"))
            if payload["id"] != entry["id"] or payload["section"] != section:
                raise ValueError("metadata belongs to another record")
            compare(original, payload["record"])
    if len(entries) != counts["current"] + counts["historical"]:
        raise ValueError("unclassified browser entries")
    for key in set(register) - {"entries", "historical_entries"}:
        compare(register[key], index[key])
    return {**counts, "coefficient_vectors": vectors, "integer_coefficients": coefficients}


def _maximum_fraction(value: str | float) -> float:
    """Accept only a finite, positive share of the complete archive."""
    fraction = float(value)
    if not 0 < fraction <= 1:
        raise ValueError("maximum fraction must be finite and greater than zero through one")
    return fraction


def measure(
    baseline: Path,
    site: Path,
    page: Path,
    register: Path,
    *,
    maximum_fraction: float = 0.25,
) -> dict[str, Any]:
    """Refuse invalid projections before judging the predeclared byte threshold."""
    threshold = _maximum_fraction(maximum_fraction)
    assets, index = initial_assets(page.resolve(), site.resolve())
    document = json.loads(read_retained_text(register))
    envelope = document.get("softschema", {}).get("envelope")
    original = document[envelope] if envelope else document
    coverage = check_projection(original, index, site)
    control = baseline.stat().st_size
    if control <= 0:
        raise ValueError("empty complete-HTML control")
    candidate = sum(assets.values())
    return {
        "metric": "initial_raw_bytes",
        "regime": "default unselected route; local uncompressed automatic assets and index",
        "control_bytes": control,
        "candidate_bytes": candidate,
        "maximum_fraction": threshold,
        "candidate_fraction": candidate / control,
        "passes_acceptance": candidate <= control * threshold,
        "assets": assets,
        "coverage": coverage,
        "validity": (
            "all retained publication metadata and coefficient strings compare exactly; "
            "superseded historical rows and current notes intentionally omitted"
        ),
        "exclusions": "clicked metadata/coefficient files and archives; no latency claim",
    }


def working_tree_dirty(repo: Path) -> bool:
    """Include staged and untracked inputs when recording working-tree provenance."""
    status = subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=normal"], cwd=repo, text=True
    )
    return bool(status.strip())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--site", type=Path, required=True)
    parser.add_argument("--page", default="papers/exact-side-values.html")
    parser.add_argument("--register", type=Path, default=Path("frontier/exact-values.json"))
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--maximum-fraction",
        type=_maximum_fraction,
        default=0.25,
        help="predeclared maximum initial-byte share of the complete archive (default: 0.25)",
    )
    args = parser.parse_args()
    result = measure(
        args.baseline,
        args.site,
        args.site / args.page,
        args.register,
        maximum_fraction=args.maximum_fraction,
    )
    repo = Path(__file__).resolve().parents[2]
    revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=repo, text=True
    ).strip()
    dirty = working_tree_dirty(repo)
    result["provenance"] = {
        "recorded": datetime.now(UTC).isoformat(),
        "revision": revision,
        "dirty": dirty,
        "platform": platform.platform(),
        "python": platform.python_version(),
        "command": sys.argv,
        "control": str(args.baseline.resolve()),
        "candidate": str((args.site / args.page).resolve()),
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    if not result["passes_acceptance"]:
        raise SystemExit("initial raw bytes exceed the predeclared maximum fraction")


if __name__ == "__main__":
    main()
