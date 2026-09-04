#!/usr/bin/env python3
"""Render the standalone explainer page for a retained fractional certificate.

Every quantity the page states is read or derived from the certificate file, so
the page cannot drift from the bound it explains. When a rung moves, rerunning
this is the whole update: no number is typed twice.

The page is one self-contained file. Typography follows the kpress design
system, and the kpress distribution also supplies the reading faces and KaTeX,
which are inlined as data URIs. Nothing is fetched at view time, which is what
lets the same artifact serve from GitHub Pages, from a file:// URL, and from an
artifact host with a strict content-security policy.

Usage, from `packing/`:

    uv run --frozen --group site python -m devtools.render_certificate_page
    uv run --frozen --group site python -m devtools.render_certificate_page --check
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import TypedDict

from sqpack.fractional.certificate import (
    Certificate,
    conditions_without_sweep,
    d4_images,
    verify,
)
from sqpack.fractional.model import Atom
from sqpack.fractional.sweep import minimum_covered_mass

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
CASE = PACKING / "cases" / "n11_fractional_certificate"
TEMPLATE = Path(__file__).with_name("templates") / "certificate_page.html"
COARSENING = CASE / "net-coarsening.json"
OUTPUT = PACKING / "site" / "index.html"

# The prior state of the case, which the page reports next to the new bound.
PRIOR_LOWER = "3.788854"
PRIOR_SOURCE = "Stromquist 2003"
BEST_PACKING = "3.877084"
BEST_SOURCE = "Trump 1979 packing"

# Only the KaTeX faces this page can reach. The rest of the distribution's
# @font-face blocks are dropped rather than inlined; every one costs 30-40 KB.
KATEX_FACES = frozenset(
    {
        "KaTeX_AMS-Regular",
        "KaTeX_Caligraphic-Regular",
        "KaTeX_Main-Bold",
        "KaTeX_Main-Italic",
        "KaTeX_Main-Regular",
        "KaTeX_Math-Italic",
        "KaTeX_Size1-Regular",
        "KaTeX_Size2-Regular",
        "KaTeX_Size3-Regular",
        "KaTeX_Size4-Regular",
    }
)

# Latin subset, as kpress declares it for its own faces.
LATIN_RANGE = (
    "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,"
    "U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
)

# The kpress stylesheet chain, in the order `kpress.format.assets` loads it.
# page-reset first (it owns html/body for the standalone shell), print last.
KPRESS_STYLESHEETS = (
    "page-reset.css",
    "style-tokens.css",
    "syntax.css",
    "document.css",
    "components.css",
    "print.css",
)


def kpress_static() -> Path:
    """The kpress distribution's static asset root.

    Imported here rather than at module scope: kpress lives in the optional
    `site` dependency group, so importing it eagerly would make every other
    entry point in this package fail without it.
    """
    try:
        import kpress.format as kpress_format  # noqa: PLC0415
    except ModuleNotFoundError:  # pragma: no cover - a dependency-group failure
        raise SystemExit(
            "kpress is not installed. Run with `--group site`, which pins it."
        ) from None
    static = Path(kpress_format.__file__).parent / "static"
    if not (static / "katex" / "katex.min.js").is_file():
        raise SystemExit(f"kpress static assets are missing under {static}")
    return static


def data_uri(path: Path) -> str:
    return f"data:font/woff2;base64,{base64.b64encode(path.read_bytes()).decode()}"


def inline_font_urls(css: str, fonts: Path) -> str:
    """Rewrite `url("../fonts/x.woff2")` to a data URI, so the page fetches nothing."""

    def rewrite(match: re.Match[str]) -> str:
        name = match.group(1)
        return f'url("{data_uri(fonts / name)}")'

    return re.sub(r'url\("\.\./fonts/([A-Za-z0-9_.-]+)"\)', rewrite, css)


def kpress_css(static: Path) -> str:
    """The kpress design system as one stylesheet, its webfonts inlined.

    Taken whole rather than reimplemented: the reading measure, the type ramp,
    the heading and list treatments, the colour roles and both themes are the
    system's to define, and a page that re-declared a subset of them would drift
    from it silently. This page adds only what kpress has no component for.
    """
    parts = []
    for name in KPRESS_STYLESHEETS:
        parts.append(f"/* kpress: {name} */")
        parts.append((static / "css" / name).read_text(encoding="utf-8"))
    return inline_font_urls("\n".join(parts), static / "fonts")


def theme_bootstrap(static: Path) -> str:
    """kpress's pre-paint theme resolution, so light and dark match the system."""
    return (static / "js" / "theme-bootstrap.js").read_text(encoding="utf-8")


def katex_css(static: Path) -> str:
    """KaTeX's stylesheet with the reachable faces inlined and the rest dropped."""
    css = (static / "katex" / "katex.min.css").read_text(encoding="utf-8")

    def rewrite(match: re.Match[str]) -> str:
        block = match.group(0)
        ref = re.search(r"fonts/([A-Za-z0-9_-]+)\.woff2", block)
        if ref is None:
            return block
        if ref.group(1) not in KATEX_FACES:
            return ""
        uri = data_uri(static / "katex" / "fonts" / f"{ref.group(1)}.woff2")
        return block.replace(f"url(fonts/{ref.group(1)}.woff2)", f'url("{uri}")')

    return re.sub(r"@font-face\{[^}]*\}", rewrite, css)


class CoarseningRow(TypedDict):
    """One row of the retained net-coarsening measurement."""

    K: int
    D: str
    B: str
    least_mass: str
    least_mass_exact: str
    passes: bool
    seconds: float


@dataclass(frozen=True, slots=True)
class Facts:
    """Everything the page states about one certificate, derived from its file."""

    identifier: str
    n: int
    outer_side: Fraction
    square_side: Fraction
    steps: int
    atoms: tuple[Atom, ...]
    total_mass: Fraction
    least_mass: Fraction
    witness: tuple[Fraction, Fraction]
    orbits: int
    distinct_weights: int
    weight_scale: int
    largest_half_gap: Fraction


def load_certificate(path: Path) -> tuple[Certificate, dict[str, str]]:
    record = json.loads(path.read_text(encoding="utf-8"))
    limit = Fraction(record["angle_limit"])
    steps = int(record["direction_steps"])
    certificate = Certificate(
        n=int(record["n"]),
        outer_side=Fraction(record["outer_side"]),
        square_side=Fraction(record["square_side"]),
        atoms=tuple(
            Atom(f"{index:04d}", Fraction(x), Fraction(y), Fraction(weight))
            for index, (x, y, weight) in enumerate(record["atoms"])
        ),
        half_tangents=tuple(limit * k / steps for k in range(steps + 1)),
        symmetry=record["symmetry"],
    )
    return certificate, record


def derive(path: Path, *, full_sweep: bool = False) -> Facts:
    """Read a certificate and compute what the page reports, deciding it first.

    `C0` through `C3` are re-decided on every render: they are exact rational
    comparisons costing microseconds, and a page explaining a proof should not be
    renderable from a file those conditions refuse. `C4` is the expensive one, a
    sweep over every direction and minutes at this atom count, and the case
    already owns a replay gate that decides it, so re-deciding it here would buy
    a second copy of one verdict at the price of the build. The upright direction
    is swept regardless: the page marks its witness, and it bounds the record's
    declared least covered mass from below. `--verify-c4` runs the whole sweep.
    """
    certificate, record = load_certificate(path)
    refused = [report for report in conditions_without_sweep(certificate) if not report.holds]
    if refused:
        raise SystemExit(
            f"{path.name} fails {', '.join(r.name for r in refused)}; refusing to render"
        )
    if full_sweep:
        verdict = verify(certificate)
        if not verdict.accepted:
            raise SystemExit(
                f"{path.name} fails {', '.join(verdict.failures)}; refusing to render"
            )

    upright = certificate.directions[0]
    least, witness = minimum_covered_mass(
        certificate.atoms, upright, certificate.outer_side, certificate.square_side
    )

    seen: set[frozenset[tuple[Fraction, Fraction]]] = set()
    for atom in certificate.atoms:
        seen.add(frozenset(d4_images(atom.x, atom.y, certificate.outer_side)))

    scale = 1
    for atom in certificate.atoms:
        denominator = atom.weight.denominator
        scale = scale * denominator // _gcd(scale, denominator)

    declared_total = Fraction(record["total_mass"])
    if declared_total != certificate.total_mass:
        raise SystemExit(
            f"{path.name} declares total mass {declared_total}, "
            f"carries {certificate.total_mass}"
        )
    declared_least = Fraction(record["least_cell_mass"])
    if least < declared_least:
        raise SystemExit(
            f"{path.name} declares least cell mass {declared_least}, but the upright "
            f"direction alone reaches {least}"
        )

    return Facts(
        identifier=record["id"],
        n=certificate.n,
        outer_side=certificate.outer_side,
        square_side=certificate.square_side,
        steps=int(record["direction_steps"]),
        atoms=certificate.atoms,
        total_mass=certificate.total_mass,
        least_mass=least,
        witness=witness,
        orbits=len(seen),
        distinct_weights=len({atom.weight for atom in certificate.atoms}),
        weight_scale=scale,
        largest_half_gap=certificate.largest_half_gap_tangent,
    )


def _gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def frac_tex(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"\\frac{{{value.numerator}}}{{{value.denominator}}}"


def decimal(value: Fraction, places: int = 6) -> str:
    """An exact decimal where one exists, else a rounded one. No trailing zeros."""
    text = f"{float(value):.{places}f}".rstrip("0").rstrip(".")
    return text or "0"


def atom_array(facts: Facts) -> str:
    """`[x, y, weight x scale]` per atom: the page sums integers, not floats."""
    rows = []
    for atom in facts.atoms:
        weight = atom.weight * facts.weight_scale
        assert weight.denominator == 1
        rows.append(f"[{float(atom.x):.9g},{float(atom.y):.9g},{weight.numerator}]")
    return "const ATOMS=[" + ",".join(rows) + "];"


def coarsening_rows() -> list[CoarseningRow] | None:
    """The retained net-coarsening measurement, or None when it has not been run.

    The measurement costs minutes per net and belongs to one certificate, so a
    certificate that has not been measured yet renders without that figure
    rather than blocking on it or, worse, reusing another certificate's numbers.
    """
    if not COARSENING.is_file():
        return None
    payload = json.loads(COARSENING.read_text(encoding="utf-8"))
    return payload["rows"]


def coarsening_svg(rows: list[CoarseningRow]) -> tuple[str, str, str]:
    """Bars, value labels and axis labels for the net-coarsening figure."""
    left, width, gap = 100.0, 66.0, 50.0
    top, base = 30.0, 190.0
    bars, values, labels = [], [], []
    for index, row in enumerate(rows):
        x = left + index * (width + gap)
        mass = float(row["least_mass"])
        height = min(mass, 1.0) * (base - top)
        passes = bool(row["passes"])
        fill = 'fill="var(--doc-accent)"' if passes else 'fill="var(--doc-accent)" opacity=".3"'
        bars.append(
            f'<rect x="{x:.0f}" y="{base - height:.0f}" width="{width:.0f}" '
            f'height="{height:.0f}" {fill}/>'
        )
        emphasis = ' fill="var(--doc-accent)" font-weight="650"' if passes else ""
        values.append(
            f'<text x="{x + width / 2:.0f}" y="{base - height - 6:.0f}"{emphasis}>'
            f"{mass:.4f}</text>".replace(">0.0000<", ">0<")
        )
        tone = ' fill="var(--doc-text)"' if passes else ""
        labels.append(
            f'<text x="{x + width / 2:.0f}" y="210"{tone}>K = {row["K"]}</text>'
            f'<text x="{x + width / 2:.0f}" y="226" font-size="9.5">B {row["B"]}</text>'
        )
    return "\n        ".join(bars), "\n        ".join(values), "\n        ".join(labels)


def number_line(facts: Facts) -> dict[str, str]:
    """Positions on the 3.75-3.90 axis the header draws."""
    low, high, x0, x1 = 3.75, 3.90, 20.0, 680.0
    place = lambda v: x0 + (v - low) / (high - low) * (x1 - x0)  # noqa: E731
    bound = float(facts.outer_side)
    return {
        "PRIOR_X": f"{place(float(PRIOR_LOWER)):.0f}",
        "BOUND_X": f"{place(bound):.0f}",
        "BEST_X": f"{place(float(BEST_PACKING)):.0f}",
        "BAND_W": f"{place(float(BEST_PACKING)) - place(bound):.0f}",
    }


def substitutions(facts: Facts, static: Path) -> dict[str, str]:
    n = facts.n
    total = facts.total_mass
    shortfall = n - total
    gap_now = Fraction(BEST_PACKING) - facts.outer_side
    gap_before = Fraction(BEST_PACKING) - Fraction(PRIOR_LOWER)
    movement = facts.outer_side - Fraction(PRIOR_LOWER)
    margin = facts.least_mass - 1
    rows = coarsening_rows()
    if rows:
        bars, values, labels = coarsening_svg(rows)
        alt = "Least covered mass against net size: " + ", ".join(
            f"K={row['K']} gives {row['least_mass']}" for row in rows
        )
    else:
        bars = values = labels = alt = ""
    values_map = {
        "KPRESS_CSS": kpress_css(static) + katex_css(static),
        "THEME_BOOTSTRAP": theme_bootstrap(static),
        "KATEX_JS": (static / "katex" / "katex.min.js").read_text(encoding="utf-8"),
        "ATOMS": atom_array(facts),
        "ID": facts.identifier,
        "N": str(n),
        "N_ATOMS": f"{len(facts.atoms):,}",
        "N_ORBITS": str(facts.orbits),
        "N_DIRECTIONS": str(facts.steps + 1),
        "N_DIRECTIONS_MAX": str(facts.steps),
        "N_WEIGHTS": str(facts.distinct_weights),
        "L_TEX": frac_tex(facts.outer_side),
        "L_FRAC": f"{facts.outer_side.numerator}/{facts.outer_side.denominator}",
        "L_DEC": decimal(facts.outer_side),
        "L_JS": repr(float(facts.outer_side)),
        "B_FRAC": f"{facts.square_side.numerator}/{facts.square_side.denominator}",
        "B_JS": repr(float(facts.square_side)),
        "TOTAL_TEX": frac_tex(total),
        "TOTAL_DEC": decimal(total),
        "SHORTFALL": decimal(shortfall),
        "FILL_PCT": f"{float(total / n) * 100:.4f}",
        "LEAST_TEX": frac_tex(facts.least_mass),
        "LEAST_TEX_PLAIN": f"{facts.least_mass.numerator}/{facts.least_mass.denominator}",
        "LEAST_DEC": decimal(facts.least_mass),
        "LEAST_MARGIN": f"{(margin * facts.weight_scale).numerator:,}",
        "SCALE": f"1/{facts.weight_scale}",
        "SCALE_JS": str(facts.weight_scale),
        "WEIGHT_MIN": decimal(min(a.weight for a in facts.atoms), 5),
        "WEIGHT_MAX": decimal(max(a.weight for a in facts.atoms), 5),
        "WITNESS_TEX": (
            f"({facts.witness[0].numerator}/{facts.witness[0].denominator},\\; "
            f"{facts.witness[1].numerator}/{facts.witness[1].denominator})"
        ),
        "WITNESS_X_JS": f"{facts.witness[0].numerator}/{facts.witness[0].denominator}",
        "WITNESS_Y_JS": f"{facts.witness[1].numerator}/{facts.witness[1].denominator}",
        "PRIOR_LOWER": PRIOR_LOWER,
        "PRIOR_SOURCE": PRIOR_SOURCE,
        "BEST_PACKING": BEST_PACKING,
        "BEST_SOURCE": BEST_SOURCE,
        "MOVEMENT": decimal(movement),
        "GAP_NOW": decimal(gap_now),
        "GAP_BEFORE": decimal(gap_before),
        "COARSEN_ALT": alt,
        "COARSEN_BARS": bars,
        "COARSEN_VALUES": values,
        "COARSEN_LABELS": labels,
    }
    values_map.update(number_line(facts))
    return values_map


def render(certificate_path: Path, *, full_sweep: bool = False) -> str:
    facts = derive(certificate_path, full_sweep=full_sweep)
    template = TEMPLATE.read_text(encoding="utf-8")
    if coarsening_rows() is None:
        template = re.sub(
            r"<!--BEGIN:COARSENING-->.*?<!--END:COARSENING-->", "", template, flags=re.DOTALL
        )
    values = substitutions(facts, kpress_static())
    missing = {m.group(1) for m in re.finditer(r"\{\{([A-Z_]+)\}\}", template)} - values.keys()
    if missing:
        raise SystemExit(f"template placeholders with no value: {sorted(missing)}")
    for key, value in values.items():
        template = template.replace(f"{{{{{key}}}}}", value)
    return template


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--certificate",
        type=Path,
        default=CASE / "certificate.json",
        help="the certificate to explain (default: the retained n = 11 bound)",
    )
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero if the committed page differs from a fresh render",
    )
    parser.add_argument(
        "--verify-c4",
        action="store_true",
        help="sweep every direction before rendering; the case replay gate decides the same "
        "condition, so this is for a release build rather than an edit loop",
    )
    args = parser.parse_args(argv)

    page = render(args.certificate, full_sweep=args.verify_c4)
    if args.check:
        if not args.output.is_file():
            print(f"{args.output.relative_to(REPO)} has not been rendered", file=sys.stderr)
            return 1
        if args.output.read_text(encoding="utf-8") != page:
            print(f"{args.output.relative_to(REPO)} is stale; rerender it", file=sys.stderr)
            return 1
        print(f"{args.output.relative_to(REPO)} is current")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(page, encoding="utf-8")
    print(f"wrote {args.output.relative_to(REPO)} ({len(page) / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
