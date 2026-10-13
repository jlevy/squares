"""Paper II's figures stay bound to Overbeck's certificate and the retained replays.

Each figure is checked three ways: it is a self-contained static SVG that fits a phone's
column in glyphs the shipped face carries; what it labels is what the pinned data says,
read here independently of the module; and a changed input is refused before anything is
drawn. The figures are rendered once, in a module fixture, so no test pays for the
render in its own call time.
"""

from __future__ import annotations

import gzip
import json
import re
from collections import Counter
from fractions import Fraction
from math import comb
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

import kpress
import pytest

from devtools import check_general_pose_tree_census as census
from devtools import n11_threshold_figures as figures
from devtools import paper_figures as pf
from sqpack.fractional.certificate import d4_images

SVG = f"{{{pf.SVG_NS}}}"
ANY_CASE = re.IGNORECASE
FACE = (
    Path(kpress.__file__).parent / "format/static/fonts/source-sans-3-latin-wght-normal.woff2"
)
#: A phone's column, and the screen size the label script holds a diagram's labels at
#: (`diagram-labels.js`): the page's support text, about 17 px; notes a little smaller.
COLUMN, LABEL_PX, NOTE_PX = 358.0, 17.0, 15.6
#: An average advance of the sans face, in ems, a little above what it measures.
ADVANCE = 0.5
CONTRACT_CERT_FACTS = {
    "CERT_GAMMA",
    "CERT_M",
    "CERT_ELEVEN_GAMMA",
    "CERT_SURPLUS_UNITS",
    "CERT_ROWS",
    "CERT_SITES",
    "CERT_POINT_SITES",
    "CERT_ORBITS",
    "CERT_CHARGE_ORBITS",
    "CERT_FEATURES",
    "CERT_A",
    "CERT_L0",
    "CERT_BOUND",
}


@pytest.fixture(scope="module")
def rendered() -> dict[str, str]:
    return figures.render_figures()


@pytest.fixture(scope="module")
def roots(rendered: dict[str, str]) -> dict[str, ET.Element]:
    return {key: ET.fromstring(svg) for key, svg in rendered.items()}


@pytest.fixture(scope="module")
def facts() -> dict[str, str]:
    return figures.caption_facts()


@pytest.fixture(scope="module")
def raw() -> dict[str, Any]:
    value: dict[str, Any] = json.loads(figures.CERTIFICATE.read_bytes())
    return value


@pytest.fixture(scope="module")
def python() -> dict[str, Any]:
    value: dict[str, Any] = json.loads(figures.PYTHON_EVIDENCE.read_bytes())
    return value


@pytest.fixture(scope="module")
def evaluator(raw: dict[str, Any]) -> census.WitnessEvaluator:
    """T-059's own independent exact evaluator, which imports no producer code."""
    return census.witness_evaluator(raw, len(raw["entries"]))


def _sites(raw: dict[str, Any]) -> list[tuple[Fraction, Fraction]]:
    scale = raw["coordinate_denominator"]
    side = Fraction(raw["L"])
    sites: list[tuple[Fraction, Fraction]] = []
    for x, y, _ in raw["point_orbits"]:
        sites.extend(sorted(set(d4_images(Fraction(x, scale), Fraction(y, scale), side))))
    return sites


def _data(root: ET.Element, name: str) -> list[ET.Element]:
    return [node for node in root.iter() if name in node.attrib]


# Contract ------------------------------------------------------------------------------


def test_the_figure_contract(rendered: dict[str, str], facts: dict[str, str]) -> None:
    assert figures.FIGURE_KEYS == (
        "CHANGES_SVG",
        "LADDER_SVG",
        "ROADMAP_SVG",
        "CHARGE_SVG",
        "BUDGET_SVG",
        "FAMILIES_SVG",
        "CORE_SVG",
        "CATALOGUE_SVG",
        "ENVELOPE_SVG",
        "SIGNED_SVG",
        "FIELD_SVG",
        "MINIMA_SVG",
    )
    assert tuple(rendered) == figures.FIGURE_KEYS
    assert set(facts) >= CONTRACT_CERT_FACTS
    prefixes = {key.removesuffix("_SVG") for key in figures.FIGURE_KEYS} | {"CERT"}
    for key, value in facts.items():
        assert re.fullmatch(r"[A-Z0-9]+(?:_[A-Z0-9]+)+", key), key
        assert key.split("_", 1)[0] in prefixes, key
        assert value.strip(), key


def test_every_input_is_declared_and_repository_relative() -> None:
    repository = figures.REPOSITORY
    declared = set(figures.FIGURE_INPUTS)
    read = {
        figures.CERTIFICATE,
        figures.PYTHON_EVIDENCE,
        figures.T026_CERTIFICATE,
        figures.T059_JOURNAL,
        figures.NATIVE_ROWS,
        figures.RESULTS,
    }
    assert declared == {path.relative_to(repository).as_posix() for path in read}
    for relative in declared:
        assert not relative.startswith("/")
        assert (repository / relative).is_file()


def test_the_archived_checker_is_never_imported() -> None:
    """`exact_mixed.py` imports numba; the certificate goes through the native loader."""
    source = Path(figures.__file__).read_text(encoding="utf-8")
    assert "exact_mixed" not in source.replace("archived `exact_mixed.py`", "")
    assert "load_kleddamag_parent_core" in source


# Self-containment, width and glyphs ----------------------------------------------------


@pytest.mark.parametrize("key", figures.FIGURE_KEYS)
def test_each_figure_is_a_self_contained_accessible_svg(
    key: str, rendered: dict[str, str]
) -> None:
    content = rendered[key]
    root = ET.fromstring(content)
    assert root.tag == f"{SVG}svg"
    assert root.attrib["role"] == "img"
    assert root.attrib["class"].startswith("n11-diagram n11-")
    labelled = root.attrib["aria-labelledby"].split()
    ids = {node.attrib["id"] for node in root.iter() if "id" in node.attrib}
    assert len(labelled) == 2
    assert set(labelled) <= ids
    assert root.find(f"{SVG}title") is not None
    assert root.find(f"{SVG}desc") is not None
    assert not re.search(r"<\s*(script|image|foreignObject|iframe|use)\b", content, ANY_CASE)
    assert not re.search(
        r"\b(?:href|xlink:href|src|onload|onclick|style)\s*=", content, ANY_CASE
    )
    # The only address is the namespace, and the only reference a local pattern.
    assert re.findall(r"https?://[^\"' ]+", content) == [pf.SVG_NS]
    for reference in re.findall(r"url\(#([^)]+)\)", content):
        assert reference in ids
    # Fixed ink on a light ground: the paper's stylesheet must list this class.
    assert re.search(r'\b(?:fill|stroke)="#[0-9a-f]{6}"', content)


def test_identifiers_are_unique_across_the_paper(roots: dict[str, ET.Element]) -> None:
    ids = [
        node.attrib["id"]
        for root in roots.values()
        for node in root.iter()
        if "id" in node.attrib
    ]
    assert len(ids) == len(set(ids))
    classes = [root.attrib["class"].split()[1] for root in roots.values()]
    assert len(classes) == len(set(classes))


def _viewbox(root: ET.Element) -> tuple[float, float, float, float]:
    left, top, width, height = (float(v) for v in root.attrib["viewBox"].split())
    return left, top, width, height


@pytest.mark.parametrize("key", figures.FIGURE_KEYS)
def test_each_figure_fits_a_phone_column(key: str, roots: dict[str, ET.Element]) -> None:
    """No figure is wider than 390 px, and at a phone's column every label, held at the
    support size by the label script, stays inside the drawing: none needs a sideways
    scroll."""
    root = roots[key]
    left, top, width, height = _viewbox(root)
    assert width <= pf.PHONE_WIDTH
    assert float(root.attrib["width"]) == width
    units_per_px = width / COLUMN
    for node in root.iter(f"{SVG}text"):
        value = "".join(node.itertext())
        size = (NOTE_PX if "note" in node.attrib["class"] else LABEL_PX) * units_per_px
        extent = len(value) * ADVANCE * size
        x = float(node.attrib["x"])
        start = {"start": x, "middle": x - extent / 2, "end": x - extent}[
            node.attrib.get("text-anchor", "start")
        ]
        assert left - 1 <= start, (key, value)
        assert start + extent <= left + width + 1, (key, value)
        y = float(node.attrib["y"])
        assert top <= y - 0.7 * size, (key, value)
        assert y <= top + height, (key, value)


def test_labels_use_only_glyphs_the_shipped_face_carries(roots: dict[str, ET.Element]) -> None:
    """Γ, L₀, ≤, ≥ and subscripts are a caption's, not a label's (adversarial review
    of Paper III, §3.4: fourteen of its 21 labels were drawn from a fallback face)."""
    ttlib = pytest.importorskip("fontTools.ttLib")
    cmap = ttlib.TTFont(FACE).getBestCmap()
    for key, root in roots.items():
        for node in root.iter(f"{SVG}text"):
            value = "".join(node.itertext())
            missing = {character for character in value if ord(character) not in cmap}
            assert not missing, (key, value, missing)


def test_no_figure_letters_a_sentence(roots: dict[str, ET.Element]) -> None:
    for key, root in roots.items():
        for node in root.iter(f"{SVG}text"):
            assert not "".join(node.itertext()).rstrip().endswith("."), key


# Refusals ------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "pin",
    ["CERTIFICATE_SHA", "PYTHON_EVIDENCE_SHA", "T026_SHA", "T059_SHA", "NATIVE_ROWS_SHA"],
)
def test_a_changed_input_pin_refuses_every_figure_and_fact(
    pin: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(figures, pin, "0" * 64)
    with pytest.raises(ValueError, match="changed figure input"):
        figures.render_figures()
    with pytest.raises(ValueError, match="changed figure input"):
        figures.caption_facts()


def test_a_changed_ladder_pin_refuses_the_figures(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(pf, "LADDER_DIGEST", "0" * 64)
    with pytest.raises(ValueError, match="changed figure input"):
        figures.render_figures()


def test_a_changed_evidence_file_is_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    altered = json.loads(figures.PYTHON_EVIDENCE.read_text(encoding="utf-8"))
    altered["rows"][figures.TIGHT_ROW]["minimum_units"] += 1
    path = tmp_path / "python.json"
    path.write_text(json.dumps(altered), encoding="utf-8")
    monkeypatch.setattr(figures, "PYTHON_EVIDENCE", path)
    with pytest.raises(ValueError, match="changed figure input"):
        figures.caption_facts()


# Labels bound to data, figure by figure ------------------------------------------------


def test_certificate_facts_are_the_certificates(
    facts: dict[str, str], raw: dict[str, Any], python: dict[str, Any]
) -> None:
    gamma = Fraction(raw["minimum_units"], raw["weight_denominator"])
    budget = Fraction(raw["budget_units"], raw["weight_denominator"])
    assert facts["CERT_GAMMA"] == str(float(gamma))
    assert facts["CERT_M"] == str(float(budget))
    assert Fraction(facts["CERT_ELEVEN_GAMMA"]) == 11 * gamma
    surplus = 11 * raw["minimum_units"] - raw["budget_units"]
    assert (
        facts["CERT_SURPLUS_UNITS"] == f"{surplus:,}" == f"{python['counting_surplus_units']:,}"
    )
    assert facts["CERT_ROWS"] == f"{len(raw['entries']):,}" == f"{python['intervals']:,}"
    sites = _sites(raw)
    assert facts["CERT_SITES"] == f"{len(sites):,}"
    weighted = sum(
        len(
            set(
                d4_images(
                    Fraction(x), Fraction(y), Fraction(raw["L"]) * raw["coordinate_denominator"]
                )
            )
        )
        for x, y, w in raw["point_orbits"]
        if w
    )
    assert facts["CERT_POINT_SITES"] == f"{weighted:,}"
    assert facts["CERT_ORBITS"] == f"{len(raw['point_orbits']):,}"
    assert facts["CERT_CHARGE_ORBITS"] == f"{len(raw['charge_orbits']):,}"
    features = sum(len(row["sets"]) for row in raw["charge_orbits"] if row["weight"])
    assert facts["CERT_FEATURES"] == f"{features:,}"
    assert (facts["CERT_A"], facts["CERT_L0"]) == (raw["A"], raw["L"])
    assert facts["CERT_BOUND"] == raw["bound"] == str(Fraction(raw["L"]) / Fraction(raw["A"]))


def test_changes_counts_come_from_both_certificates(
    roots: dict[str, ET.Element], facts: dict[str, str]
) -> None:
    t026 = json.loads(figures.T026_CERTIFICATE.read_bytes())
    assert facts["CHANGES_T026_POINTS"] == f"{len(t026['atoms']):,}" == "584"
    assert facts["CHANGES_T026_TRIPLES"] == f"{len(t026['threshold_atoms']):,}" == "320"
    assert facts["CHANGES_T026_NET"] == f"{t026['direction_steps']:,}"
    assert facts["CHANGES_T026_B"] == t026["square_side"]
    share = Fraction(t026["point_mass"]) / Fraction(t026["total_budget"])
    assert facts["CHANGES_T026_POINT_SHARE"] == f"{round(100 * share)}%"
    root = roots["CHANGES_SVG"]
    bars = _data(root, "data-share")
    # Two bars, each of shares summing to one: T-026's two families, T-037's four.
    assert [node.attrib["data-family"] for node in bars] == [
        "point",
        "2-of-3",
        "point",
        "2-of-3",
        "2-of-5",
        "3-of-5",
    ]
    assert sum(Fraction(node.attrib["data-share"]) for node in bars[:2]) == 1
    assert sum(Fraction(node.attrib["data-share"]) for node in bars[2:]) == 1
    assert Fraction(bars[0].attrib["data-share"]) == share
    sides = {node.attrib["data-side"] for node in _data(root, "data-side")}
    assert sides == {"1", facts["CERT_A"]}
    degrees = _data(root, "data-degree")
    assert (
        sum(int(node.attrib["data-count"]) for node in degrees[:45])
        == t026["direction_steps"] + 1
    )
    assert sum(int(node.attrib["data-count"]) for node in degrees[45:]) == int(
        facts["CERT_ROWS"].replace(",", "")
    )


def test_ladder_labels_are_the_registers(
    roots: dict[str, ET.Element], facts: dict[str, str]
) -> None:
    root = roots["LADDER_SVG"]
    records = pf.ladder_records()
    for node in _data(root, "data-value"):
        assert node.text == pf.ladder_value(records[node.attrib["data-value"]])
    assert facts["LADDER_GAP"] == "0.0020836"


def test_roadmap_numbers_are_facts(roots: dict[str, ET.Element], facts: dict[str, str]) -> None:
    labels = " ".join(
        "".join(node.itertext()) for node in roots["ROADMAP_SVG"].iter(f"{SVG}text")
    )
    for key in ("CERT_ELEVEN_GAMMA", "CERT_M", "CERT_SITES", "CERT_ROWS"):
        assert facts[key] in labels


def test_one_k_of_m_charge_is_paid_exactly_where_it_holds_three(
    roots: dict[str, ET.Element], facts: dict[str, str], raw: dict[str, Any]
) -> None:
    orbit = raw["charge_orbits"][figures.CHARGE_ORBIT]
    assert orbit["weight"] == max(row["weight"] for row in raw["charge_orbits"])
    assert (orbit["threshold"], len(orbit["sets"][0])) == (3, 5)
    assert Fraction(facts["CHARGE_WEIGHT"]) == Fraction(
        orbit["weight"], raw["weight_denominator"]
    )
    assert facts["CHARGE_WEIGHT"] == "0.067038144"
    sites = _sites(raw)
    members = [sites[i] for i in orbit["sets"][0]]
    # Capture decided here, exactly, from the row's own rationals.
    _, _, tangent, side = (Fraction(value) for value in raw["entries"][figures.CHARGE_ROW])
    cosine, sine = (1 - tangent**2) / (1 + tangent**2), 2 * tangent / (1 + tangent**2)
    held = []
    for cx, cy in figures.CHARGE_CORES:
        held.append(
            sum(
                abs(cosine * (x - cx) + sine * (y - cy)) <= side / 2
                and abs(-sine * (x - cx) + cosine * (y - cy)) <= side / 2
                for x, y in members
            )
        )
    assert held == [3, 2]
    cores = _data(roots["CHARGE_SVG"], "data-core")
    assert [(n.attrib["data-holds"], n.attrib["data-paid"]) for n in cores] == [
        ("3", "true"),
        ("2", "false"),
    ]
    hull = _data(roots["CHARGE_SVG"], "data-orbit")[0]
    assert hull.attrib["data-weight"] == str(
        Fraction(orbit["weight"], raw["weight_denominator"])
    )
    assert facts["CHARGE_SITES"].count("(") == 5
    assert "(1.1938, 1.7190)" in facts["CHARGE_SITES"]


def test_the_budget_bars_sum_to_m_and_miss_eleven_cores_by_the_surplus(
    roots: dict[str, ET.Element], facts: dict[str, str], raw: dict[str, Any]
) -> None:
    root = roots["BUDGET_SVG"]
    budgets = [Fraction(node.attrib["data-budget"]) for node in _data(root, "data-budget")]
    assert len(budgets) == 4
    assert sum(budgets) == Fraction(raw["budget_units"], raw["weight_denominator"])
    surplus = _data(root, "data-surplus")[0].attrib["data-surplus"]
    assert int(surplus) == 11 * raw["minimum_units"] - raw["budget_units"] == 107864
    assert facts["BUDGET_SURPLUS"] == "107,864"
    assert sum(
        Fraction(facts[k])
        for k in (
            "BUDGET_POINTS",
            "BUDGET_TWO_OF_THREE",
            "BUDGET_TWO_OF_FIVE",
            "BUDGET_THREE_OF_FIVE",
        )
    ) == Fraction(facts["BUDGET_M"])


def test_the_site_map_counts_every_site_by_role(
    roots: dict[str, ET.Element], facts: dict[str, str], raw: dict[str, Any]
) -> None:
    sites = _sites(raw)
    weighted: set[int] = set()
    index = 0
    scale = raw["coordinate_denominator"]
    side = Fraction(raw["L"])
    for x, y, w in raw["point_orbits"]:
        size = len(set(d4_images(Fraction(x, scale), Fraction(y, scale), side)))
        if w:
            weighted.update(range(index, index + size))
        index += size
    in_charge = {
        member
        for row in raw["charge_orbits"]
        if row["weight"]
        for members in row["sets"]
        for member in members
    }
    assert in_charge | weighted == set(range(len(sites)))
    counts = {
        node.attrib["data-role"]: int(node.attrib["data-count"])
        for node in _data(roots["FAMILIES_SVG"], "data-role")
    }
    assert counts == {
        "point-only": len(weighted - in_charge),
        "shared": len(weighted & in_charge),
        "charge-only": len(in_charge - weighted),
    }
    assert (facts["FAMILIES_POINT_ONLY"], facts["FAMILIES_SHARED"]) == ("352", "144")
    assert facts["FAMILIES_CHARGE_ONLY"] == "4,788"
    assert facts["FAMILIES_IN_CHARGE"] == f"{len(in_charge):,}"
    paid = _data(roots["FAMILIES_SVG"], "data-holds")
    assert [node.attrib["data-holds"] for node in paid] == ["2", "2"]
    largest = {
        family: max(
            (row["weight"], i)
            for i, row in enumerate(raw["charge_orbits"])
            if f"{row['threshold']}-of-{len(row['sets'][0])}" == family
        )[1]
        for family in ("2-of-3", "2-of-5")
    }
    assert largest == {"2-of-3": figures.TRIPLE_ORBIT, "2-of-5": figures.PAIR_ORBIT}


def test_each_core_is_strictly_inside_its_parent(
    roots: dict[str, ET.Element], python: dict[str, Any]
) -> None:
    cores = _data(roots["CORE_SVG"], "data-margin")
    assert [node.attrib["data-row"] for node in cores] == ["0", str(figures.TIGHT_ROW)]
    for node in cores:
        assert Fraction(node.attrib["data-margin"]) > 0
    assert Fraction(python["strict_core_margin"]) == Fraction(1, 10**12)


def test_the_catalogue_marks_exactly_the_rows_below_one(
    roots: dict[str, ET.Element], facts: dict[str, str], python: dict[str, Any]
) -> None:
    below = {
        row["row"]: row["minimum_units"]
        for row in python["rows"]
        if row["minimum_units"] < 10**9
    }
    assert set(below) == {*figures.TIGHT_PAIR, figures.TIGHT_ROW}
    marks = {
        node.attrib["data-tight"]: int(node.attrib["data-minimum"])
        for node in _data(roots["CATALOGUE_SVG"], "data-minimum")
    }
    assert marks == {
        str(figures.TIGHT_ROW): below[figures.TIGHT_ROW],
        " ".join(map(str, figures.TIGHT_PAIR)): below[figures.TIGHT_PAIR[0]],
    }
    bins = _data(roots["CATALOGUE_SVG"], "data-bin")
    assert sum(int(node.attrib["data-count"]) for node in bins) == len(python["rows"])
    assert facts["CATALOGUE_TIGHT_ANGLES"] == "44.58°\N{EN DASH}44.59°"
    assert facts["CATALOGUE_PAIR_ANGLES"] == "30.63°\N{EN DASH}30.65°"


def test_the_envelope_inset_is_the_rows_margin(
    roots: dict[str, ET.Element], facts: dict[str, str], raw: dict[str, Any]
) -> None:
    left, right, _, _ = (Fraction(value) for value in raw["entries"][figures.TIGHT_ROW])
    parent = Fraction(raw["A"])
    widths = [(1 - u * u) / (1 + u * u) + 2 * u / (1 + u * u) for u in (left, right)]
    radius = parent * min(widths) / 2
    root = roots["ENVELOPE_SVG"]
    assert Fraction(_data(root, "data-rho")[0].attrib["data-rho"]) == radius
    assert (
        Fraction(_data(root, "data-half")[0].attrib["data-half"])
        == Fraction(raw["L"]) / 2 - radius
    )
    assert facts["ENVELOPE_RHO"] == f"{float(radius):.6f}"
    # Upper semicontinuity on the drawn slice: every event's closed value is a charge
    # the certificate takes, and none is below the row's minimum.
    events = [Fraction(node.attrib["data-charge"]) for node in _data(root, "data-event")]
    assert events
    assert min(events) >= Fraction(raw["minimum_units"], raw["weight_denominator"])


def test_the_signed_rectangles_carry_the_binomial_coefficients(
    roots: dict[str, ET.Element], facts: dict[str, str]
) -> None:
    terms = {
        node.attrib["data-subset"]: int(node.attrib["data-coefficient"])
        for node in _data(roots["SIGNED_SVG"], "data-coefficient")
    }
    assert terms == {"12": 1, "13": 1, "23": 1, "123": -2}
    for subset, coefficient in terms.items():
        assert coefficient == (-1) ** (len(subset) - 2) * comb(len(subset) - 1, 1)
    # On a cell whose core holds the first `held` sites, the terms present are the
    # subsets of those sites, and their coefficients sum to [held ≥ 2].
    for held in range(4):
        present = [c for s, c in terms.items() if set(s) <= set("123"[:held])]
        assert sum(present) == int(held >= 2)
    assert facts["SIGNED_ABS_SUMS"] == "5, 49, 31"
    assert facts["SIGNED_EXPANSION_WEIGHT"] == "184,231,386,320"


def test_the_field_minimiser_is_t059s_exact_witness(
    roots: dict[str, ET.Element],
    facts: dict[str, str],
    python: dict[str, Any],
    evaluator: census.WitnessEvaluator,
) -> None:
    lines = gzip.decompress(figures.T059_JOURNAL.read_bytes()).decode().splitlines()
    record = next(
        json.loads(line) for line in lines[1:] if json.loads(line)["row"] == figures.TIGHT_ROW
    )
    assert record["witness_replayed"] is True
    witness = tuple(Fraction(value) for value in record["witness"])
    node = _data(roots["FIELD_SVG"], "data-witness")[0]
    assert tuple(Fraction(v) for v in node.attrib["data-witness"].split()) == witness
    exact = evaluator.charge(figures.TIGHT_ROW, *witness)
    assert int(node.attrib["data-charge"]) == exact == record["minimum"]
    assert exact == python["rows"][figures.TIGHT_ROW]["minimum_units"] == 999962528
    assert facts["FIELD_MIN"] == "0.999962528"
    levels = [
        Fraction(n.attrib["data-level-bound"])
        for n in _data(roots["FIELD_SVG"], "data-level-bound")
    ]
    assert levels == list(figures.FIELD_LEVELS)
    assert levels == sorted(levels)


def test_the_minima_figure_matches_the_source_histogram_and_the_native_bounds(
    roots: dict[str, ET.Element], facts: dict[str, str], python: dict[str, Any]
) -> None:
    minima = [row["minimum_units"] for row in python["rows"]]
    histogram = {int(k): v for k, v in python["histogram"].items()}
    assert Counter(minima) == histogram
    assert facts["MINIMA_VALUES"] == str(len(histogram)) == "11"
    assert facts["MINIMA_TOP_ROWS"] == f"{histogram[max(histogram)]:,}" == "11,981"
    native = [json.loads(line) for line in figures.NATIVE_ROWS.read_text().splitlines()[1:]]
    lower = {row["index"]: row["lower"] for row in native}
    assert sorted(lower) == list(range(len(minima)))
    assert min(lower.values()) >= python["minimum_units"]
    assert all(lower[i] <= minima[i] for i in lower)
    assert facts["MINIMA_NATIVE_BELOW_ONE"] == f"{sum(v < 10**9 for v in lower.values()):,}"
    assert facts["MINIMA_NATIVE_EQUAL"] == f"{sum(lower[i] == minima[i] for i in lower):,}"
    assert (facts["MINIMA_NATIVE_BELOW_ONE"], facts["MINIMA_NATIVE_EQUAL"]) == ("10,541", "384")
    tight = {node.attrib["data-tight"] for node in _data(roots["MINIMA_SVG"], "data-tight")}
    assert tight == {str(figures.TIGHT_ROW), " ".join(map(str, figures.TIGHT_PAIR))}
    top = _data(roots["MINIMA_SVG"], "data-top")[0]
    assert int(top.attrib["data-top"]) == max(histogram)
