#!/usr/bin/env python3
# ruff: noqa: E501, RUF001, TRY004, TRY300, TRY301
"""Classify the full side-2 configuration spaces for three and four unit squares.

The mathematical reduction is analytic: every unit square in a side-2 container
contains the container centre, and a genuinely rotated one contains it in its interior.
Thus a packing of at least two squares is axis-aligned.  What remains is a finite exact
disjunction over pairwise left/right/above/below relations in ``[0, 1]^2``.

For ``n = 3`` the checker retains the labelled cell complex, its ``S3`` quotient, the
``D4 x S3`` orbit interval, exact strata and representative packings.  For ``n = 4`` it
retains the exhaustive zero-dimensional grid classification.  Replay rebuilds every
record field and byte-compares the deterministic SVG rather than trusting a stored
summary.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
import time
from collections import Counter, deque
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import cast
from xml.etree import ElementTree as ET

from strif import atomic_output_file

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sqpack.canonical import canonical_key
from sqpack.render.numbers import format_svg_number
from sqpack.render.svg import append_metadata, serialize_svg, svg_tag
from sqpack.verify import verify_packing

SCHEMA_VERSION = 1
SIDE = Fraction(2)
COORDINATES_PER_SQUARE = 2
SEPARATION_RELATIONS_PER_PAIR = 4
N3_RAW_BRANCHES = 64
N3_CONSISTENT_BRANCHES = 24
N3_LABELLED_VERTICES = 24
N3_LABELLED_EDGES = 24
N3_LABELLED_COMPONENTS = 2
N3_COMPONENT_SIZE = 12
N3_UNLABELLED_VERTICES = 4
N3_UNLABELLED_EDGES = 4
N3_QUOTIENT_VERTICES = 2
N3_QUOTIENT_EDGES = 1
N4_RAW_BRANCHES = 4096
N4_CONSISTENT_BRANCHES = 96
N4_LABELLED_STATES = 24
N4_BRANCHES_PER_STATE = 4
ALPERT_PDF_SHA256 = "74bd2006610543d710f885908a69a65fa7e3c13657a3a22e1a63c9f202a3b6b6"
ALPERT_RAW_SHA256 = "9b2e4092c1ce74caf3fe89d798ec4c0c000d943d83fd087dfe9a3dd7b003be60"
ALVARADO_PDF_SHA256 = "f7f2845a2a7e579b65c56ac43b8e517a915f2fd89e6bcb3b0a7292e930d2f852"
ALVARADO_RAW_SHA256 = "df9a79b00137e0fe678351a0682a237022182ce78b9882c7fbdd0c55ccf39ddd"
ALPERT_PDF = ROOT / (
    "resources/papers/"
    "alpert-bauer-kahle-macpherson-spendlove-2023-hard-squares-configuration-spaces.pdf"
)
ALPERT_RAW = ROOT / (
    "resources/papers/"
    "alpert-bauer-kahle-macpherson-spendlove-2023-hard-squares-configuration-spaces.raw.md"
)
ALVARADO_PDF = ROOT / (
    "resources/papers/alvarado-garduno-gonzalez-2025-square-section-braid-groups.pdf"
)
ALVARADO_RAW = ROOT / (
    "resources/papers/alvarado-garduno-gonzalez-2025-square-section-braid-groups.raw.md"
)

GRID_CORNERS = (
    (Fraction(0), Fraction(0)),
    (Fraction(1), Fraction(0)),
    (Fraction(1), Fraction(1)),
    (Fraction(0), Fraction(1)),
)
CORNER_INDEX = {point: index for index, point in enumerate(GRID_CORNERS)}
RELATION_NAMES = ("left", "right", "below", "above")
N3_SAMPLE_PARAMETERS = (
    Fraction(0),
    Fraction(1, 8),
    Fraction(1, 4),
    Fraction(1, 2),
)

SVG_WIDTH = 1200
SVG_HEIGHT = 900
CYCLE_OFFSETS = (
    (0, -100),
    (50, -87),
    (87, -50),
    (100, 0),
    (87, 50),
    (50, 87),
    (0, 100),
    (-50, 87),
    (-87, 50),
    (-100, 0),
    (-87, -50),
    (-50, -87),
)
GLYPH_BOARD_SIZE = 120
GLYPH_SQUARE_SIZE = GLYPH_BOARD_SIZE // 2

Variable = tuple[int, int]
State = tuple[tuple[int, int], ...]
Edge = tuple[str, str]


@dataclass(frozen=True)
class SeparationCell:
    """One consistent choice of a separating direction for every labelled pair."""

    selection: tuple[int, ...]
    free_variables: tuple[Variable, ...]
    states: tuple[State, ...]


def fraction_sign(value: Fraction) -> int:
    """Exact sign for the independent validity oracle."""
    return (value > 0) - (value < 0)


def fraction_text(value: Fraction) -> str:
    """Canonical JSON spelling for an exact rational."""
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def sha256(path: Path) -> str:
    """Hash a persisted external source at the archive trust boundary."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def state_id(state: State) -> str:
    """Stable id for a labelled corner configuration."""
    return "|".join(f"{label}@{x}{y}" for label, (x, y) in enumerate(state))


def assignments_for_relation(
    first: int, second: int, relation: int
) -> tuple[tuple[Variable, int], tuple[Variable, int]]:
    """Endpoint assignments imposed by one exact non-overlap disjunct."""
    if relation == 0:
        return (((first, 0), 0), ((second, 0), 1))
    if relation == 1:
        return (((first, 0), 1), ((second, 0), 0))
    if relation == 2:
        return (((first, 1), 0), ((second, 1), 1))
    return (((first, 1), 1), ((second, 1), 0))


def enumerate_separation_cells(n: int) -> tuple[int, list[SeparationCell]]:
    """Enumerate all pairwise separation disjuncts exactly."""
    pairs = list(itertools.combinations(range(n), 2))
    raw_count = SEPARATION_RELATIONS_PER_PAIR ** len(pairs)
    all_variables = tuple(
        (square, coordinate)
        for square in range(n)
        for coordinate in range(COORDINATES_PER_SQUARE)
    )
    cells: list[SeparationCell] = []
    for selection in itertools.product(range(SEPARATION_RELATIONS_PER_PAIR), repeat=len(pairs)):
        assignments: dict[Variable, int] = {}
        consistent = True
        for (first, second), relation in zip(pairs, selection, strict=True):
            for variable, value in assignments_for_relation(first, second, relation):
                if variable in assignments and assignments[variable] != value:
                    consistent = False
                    break
                assignments[variable] = value
            if not consistent:
                break
        if not consistent:
            continue
        free = tuple(variable for variable in all_variables if variable not in assignments)
        states: list[State] = []
        if not free:
            states.append(
                tuple(
                    (assignments[(square, 0)], assignments[(square, 1)]) for square in range(n)
                )
            )
        elif len(free) == 1:
            for endpoint in (0, 1):
                complete = assignments | {free[0]: endpoint}
                states.append(
                    tuple((complete[(square, 0)], complete[(square, 1)]) for square in range(n))
                )
        cells.append(SeparationCell(selection, free, tuple(states)))
    return raw_count, cells


def exact_square(
    lower_left: tuple[Fraction, Fraction],
) -> tuple[tuple[Fraction, Fraction], ...]:
    """Corners of one axis-aligned unit square."""
    x, y = lower_left
    one = Fraction(1)
    return ((x, y), (x + one, y), (x + one, y + one), (x, y + one))


def verify_state(state: State) -> bool:
    """Run a labelled corner state through the independent exact geometry oracle."""
    squares = [exact_square((Fraction(x), Fraction(y))) for x, y in state]
    return verify_packing(squares, SIDE, sign=fraction_sign).valid


def graph_summary(vertices: set[str], edges: set[Edge]) -> dict[str, object]:
    """Exact component and Betti data for a finite graph."""
    adjacency = {vertex: set() for vertex in vertices}
    for first, second in edges:
        adjacency[first].add(second)
        adjacency[second].add(first)
    components: list[list[str]] = []
    unseen = set(vertices)
    while unseen:
        root = min(unseen)
        queue = deque([root])
        unseen.remove(root)
        component: list[str] = []
        while queue:
            vertex = queue.popleft()
            component.append(vertex)
            for neighbour in sorted(adjacency[vertex]):
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    queue.append(neighbour)
        components.append(sorted(component))
    components.sort(key=lambda component: component[0])
    degree_counts = Counter(len(adjacency[vertex]) for vertex in vertices)
    return {
        "vertices": sorted(vertices),
        "edges": [list(edge) for edge in sorted(edges)],
        "vertex_count": len(vertices),
        "edge_count": len(edges),
        "component_count": len(components),
        "component_sizes": [len(component) for component in components],
        "components": components,
        "degree_histogram": {
            str(degree): count for degree, count in sorted(degree_counts.items())
        },
        "betti": [len(components), len(edges) - len(vertices) + len(components)],
    }


def hole_index(state: State) -> int:
    """Missing grid corner of an n=3 endpoint state."""
    occupied = {(Fraction(x), Fraction(y)) for x, y in state}
    missing = set(GRID_CORNERS) - occupied
    if len(missing) != 1:
        raise ValueError(f"state is not a three-corner configuration: {state}")
    return CORNER_INDEX[missing.pop()]


def relation_records(n: int, cells: list[SeparationCell]) -> list[dict[str, object]]:
    """Deterministic retained map from raw relation selections to cells or states."""
    pairs = list(itertools.combinations(range(n), 2))
    records: list[dict[str, object]] = []
    for cell in cells:
        labels = [
            f"{first}-{second}:{RELATION_NAMES[relation]}"
            for (first, second), relation in zip(pairs, cell.selection, strict=True)
        ]
        record: dict[str, object] = {"selection": labels}
        if cell.free_variables:
            square, coordinate = cell.free_variables[0]
            record["free_variable"] = f"{'xy'[coordinate]}{square}"
            record["endpoints"] = sorted(state_id(state) for state in cell.states)
        else:
            record["state"] = state_id(cell.states[0])
        records.append(record)
    return records


def transform_point(
    point: tuple[Fraction, Fraction], *, turn: int, reflected: bool
) -> tuple[Fraction, Fraction]:
    """One D4 action on the lower-left parameter square."""
    x, y = point
    for _ in range(turn):
        x, y = y, Fraction(1) - x
    if reflected:
        x = Fraction(1) - x
    return x, y


def d4_actions() -> tuple[tuple[int, bool], ...]:
    """The eight distinct parameter-square symmetries."""
    actions = tuple((turn, reflected) for reflected in (False, True) for turn in range(4))
    images = {
        tuple(transform_point(point, turn=turn, reflected=reflected) for point in GRID_CORNERS)
        for turn, reflected in actions
    }
    if len(images) != len(actions):
        raise ValueError("D4 action enumeration is not faithful")
    return actions


def stabilizer_order(points: tuple[tuple[Fraction, Fraction], ...]) -> int:
    """D4 stabilizer of an unlabelled configuration in parameter space."""
    target = set(points)
    return sum(
        {transform_point(point, turn=turn, reflected=reflected) for point in points} == target
        for turn, reflected in d4_actions()
    )


def quotient_parameter(value: Fraction) -> Fraction:
    """Fundamental-domain coordinate for reflection along one unlabelled edge."""
    return min(value, Fraction(1) - value)


def n3_positions(parameter: Fraction) -> tuple[tuple[Fraction, Fraction], ...]:
    """Canonical representative in the D4 x S3 fundamental interval."""
    return (
        (Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(0)),
        (parameter, Fraction(1)),
    )


def wall_incidences(positions: tuple[tuple[Fraction, Fraction], ...]) -> list[list[str]]:
    """Container-wall incidences for lower-left unit-square coordinates."""
    records: list[list[str]] = []
    for square, (x, y) in enumerate(positions):
        walls = []
        if x == 0:
            walls.append("left")
        if x == 1:
            walls.append("right")
        if y == 0:
            walls.append("bottom")
        if y == 1:
            walls.append("top")
        records.append([str(square), *walls])
    return records


def contact_record(
    first: int,
    second: int,
    positions: tuple[tuple[Fraction, Fraction], ...],
) -> dict[str, object]:
    """Exact contact length and active-axis count for two axis-aligned squares."""
    first_x, first_y = positions[first]
    second_x, second_y = positions[second]
    dx = abs(first_x - second_x)
    dy = abs(first_y - second_y)
    active_axes = int(dx == 1 and dy <= 1) + int(dy == 1 and dx <= 1)
    if active_axes == 0:
        raise ValueError(f"pair {(first, second)} is not in contact")
    length = max(Fraction(0), Fraction(1) - (dy if dx == 1 else dx))
    return {
        "pair": [first, second],
        "contact_length": fraction_text(length),
        "active_sat_axes": active_axes,
    }


def sample_record(parameter: Fraction) -> dict[str, object]:
    """Exact n=3 representative plus the current two-key identity diagnostics."""
    positions = n3_positions(parameter)
    squares = [exact_square(point) for point in positions]
    verification = verify_packing(squares, SIDE, sign=fraction_sign)
    if not verification.valid or verification.touching_pairs != 3:
        raise ValueError(f"exact n=3 sample failed at {parameter}:\n{verification}")
    contacts = [
        contact_record(first, second, positions)
        for first, second in itertools.combinations(range(3), 2)
    ]
    centres_x = [float(x + Fraction(1, 2)) for x, _ in positions]
    centres_y = [float(y + Fraction(1, 2)) for _, y in positions]
    key = canonical_key(centres_x, centres_y, [0.0, 0.0, 0.0], float(SIDE))
    walls = wall_incidences(positions)
    return {
        "parameter": fraction_text(parameter),
        "lower_left_positions": [[fraction_text(x), fraction_text(y)] for x, y in positions],
        "wall_incidence_count": sum(len(record) - 1 for record in walls),
        "wall_incidences": walls,
        "pair_contact_count": 3,
        "active_sat_axis_count": sum(
            cast(int, contact["active_sat_axes"]) for contact in contacts
        ),
        "contacts": contacts,
        "exact_valid": True,
        "geometric_key": key.geometric,
        "contact_certificate": key.contact,
    }


def orientation_forcing_record() -> dict[str, object]:
    """The checked algebraic core of the arbitrary-rotation equality argument."""
    half = Fraction(1, 2)
    one_minus_half_w = (Fraction(1), -half)
    w_times_inner = (Fraction(0), *one_minus_half_w)
    left_coefficients = (
        half - w_times_inner[0],
        -w_times_inner[1],
        -w_times_inner[2],
    )
    w_minus_one = (Fraction(-1), Fraction(1))
    right_coefficients = (
        half * w_minus_one[0] * w_minus_one[0],
        half * 2 * w_minus_one[0] * w_minus_one[1],
        half * w_minus_one[1] * w_minus_one[1],
    )
    if left_coefficients != right_coefficients:
        raise ValueError("centre-projection polynomial identity failed")
    non_axis_test = Fraction(5, 4)
    projection_bound = non_axis_test * (Fraction(1) - non_axis_test / 2)
    if not projection_bound < Fraction(1, 2):
        raise ValueError("non-axis centre-projection strictness control failed")
    return {
        "container_chart": "[-1,1]^2",
        "orientation_chart": "physical theta modulo pi/2, represented by [0,pi/2) with endpoints identified",
        "support_width": "w=|cos(theta)|+|sin(theta)|",
        "containment": "|z_x|,|z_y| <= 1-w/2",
        "projection_bound": "|z.u|,|z.v| <= w(1-w/2)",
        "exact_identity": "1/2-w(1-w/2)=(w-1)^2/2",
        "equality_case": "w=1 iff the physical square is axis-aligned",
        "packing_consequence": (
            "a genuinely rotated square contains the container centre in its interior; "
            "every other contained unit square contains that point, so interiors overlap"
        ),
        "coefficient_identity_checked": True,
        "strict_non_axis_control": {
            "w": fraction_text(non_axis_test),
            "projection_bound": fraction_text(projection_bound),
            "below_half": True,
        },
    }


def literature_record(
    n: int,
    labelled_betti: list[int],
    labelled_f_vector: list[int],
    *,
    unlabelled_betti: list[int] | None = None,
) -> dict[str, object]:
    """Bind the result to the retrieved primary sources without extending their scope."""
    hashes = {
        "alpert_pdf": sha256(ALPERT_PDF),
        "alpert_raw": sha256(ALPERT_RAW),
        "alvarado_pdf": sha256(ALVARADO_PDF),
        "alvarado_raw": sha256(ALVARADO_RAW),
    }
    expected_hashes = {
        "alpert_pdf": ALPERT_PDF_SHA256,
        "alpert_raw": ALPERT_RAW_SHA256,
        "alvarado_pdf": ALVARADO_PDF_SHA256,
        "alvarado_raw": ALVARADO_RAW_SHA256,
    }
    if hashes != expected_hashes:
        raise ValueError(f"archived primary-source hash drift: {hashes}")
    if n == 3:
        alpert_betti = [2, 2]
        alpert_f_vector: list[int] | None = [24, 24]
        alvarado_match = unlabelled_betti == [1, 1]
        alpert_evidence = "Table 1 (page 2622) and Table 2 (page 2624)"
    else:
        alpert_betti = [24, 0]
        alpert_f_vector = None
        alvarado_match = None
        alpert_evidence = "Table 1 (page 2622); no n=4 f-vector is tabulated"
    return {
        "alpert_et_al_2023": {
            "scope": "ordered axis-parallel C(n;2,2), not arbitrary rotations or the D4 quotient",
            "pdf_sha256": hashes["alpert_pdf"],
            "raw_sha256": hashes["alpert_raw"],
            "reported_betti": alpert_betti,
            "reported_f_vector": alpert_f_vector,
            "derived_match": labelled_betti == alpert_betti
            and (alpert_f_vector is None or labelled_f_vector == alpert_f_vector),
            "evidence": alpert_evidence,
        },
        "alvarado_garduno_gonzalez_2025": {
            "scope": "unlabelled axis-parallel UC(pq-1,p x q) up to homotopy",
            "pdf_sha256": hashes["alvarado_pdf"],
            "raw_sha256": hashes["alvarado_raw"],
            "reported_n3_type": "wedge of one circle" if n == 3 else "not used for this cell",
            "derived_match": alvarado_match,
        },
        "plakhta_2021": {
            "status": "publisher_access_blocked",
            "scope": "affine-polytope and connectivity methods; no claim imported without primary text",
            "doi": "10.2140/agt.2021.21.1445",
        },
        "novelty_scope": "none; literature comparison is incomplete while Plakhta remains unretrieved",
    }


def require_literature_matches(
    literature: dict[str, object], *, require_unlabelled_n3: bool
) -> None:
    """Fail closed when a retained primary-source comparison does not match."""
    alpert = literature.get("alpert_et_al_2023")
    alvarado = literature.get("alvarado_garduno_gonzalez_2025")
    if not isinstance(alpert, dict) or alpert.get("derived_match") is not True:
        raise ValueError("labelled Alpert et al. invariant comparison failed")
    if require_unlabelled_n3 and (
        not isinstance(alvarado, dict) or alvarado.get("derived_match") is not True
    ):
        raise ValueError("unlabelled Alvarado-Garduno-Gonzalez comparison failed")


def build_n3_model() -> dict[str, object]:
    """Build the exhaustive n=3 cell complexes and quotient strata."""
    raw_count, cells = enumerate_separation_cells(3)
    if raw_count != N3_RAW_BRANCHES or len(cells) != N3_CONSISTENT_BRANCHES:
        raise ValueError(f"n=3 branch count drift: {raw_count} raw, {len(cells)} consistent")
    if {len(cell.free_variables) for cell in cells} != {1}:
        raise ValueError("every consistent n=3 separation branch must be one-dimensional")
    labelled_vertices = {state_id(state) for cell in cells for state in cell.states}
    labelled_edges: set[Edge] = {
        cast(Edge, tuple(sorted((state_id(cell.states[0]), state_id(cell.states[1])))))
        for cell in cells
    }
    labelled = graph_summary(labelled_vertices, labelled_edges)
    if (
        labelled["vertex_count"] != N3_LABELLED_VERTICES
        or labelled["edge_count"] != N3_LABELLED_EDGES
        or labelled["component_count"] != N3_LABELLED_COMPONENTS
        or labelled["component_sizes"] != [N3_COMPONENT_SIZE, N3_COMPONENT_SIZE]
        or labelled["degree_histogram"] != {"2": N3_LABELLED_VERTICES}
        or labelled["betti"] != [2, 2]
    ):
        raise ValueError("labelled n=3 graph is not two 12-cycles")
    state_lookup = {state_id(state): state for cell in cells for state in cell.states}
    unlabelled_vertices = {str(hole_index(state)) for state in state_lookup.values()}
    unlabelled_edges: set[Edge] = {
        cast(
            Edge,
            tuple(sorted((str(hole_index(cell.states[0])), str(hole_index(cell.states[1]))))),
        )
        for cell in cells
    }
    unlabelled = graph_summary(unlabelled_vertices, unlabelled_edges)
    if (
        unlabelled["vertex_count"] != N3_UNLABELLED_VERTICES
        or unlabelled["edge_count"] != N3_UNLABELLED_EDGES
        or unlabelled["component_count"] != 1
        or unlabelled["degree_histogram"] != {"2": N3_UNLABELLED_VERTICES}
        or unlabelled["betti"] != [1, 1]
    ):
        raise ValueError("S3 quotient is not the four-cycle")
    corner_permutations = {
        tuple(
            CORNER_INDEX[transform_point(point, turn=turn, reflected=reflected)]
            for point in GRID_CORNERS
        )
        for turn, reflected in d4_actions()
    }
    corner_orbit = {permutation[0] for permutation in corner_permutations}
    edge_orbit = {
        tuple(sorted((permutation[0], permutation[1]))) for permutation in corner_permutations
    }
    if len(corner_orbit) != 4 or len(edge_orbit) != 4:
        raise ValueError("D4 is not transitive on the four quotient vertices and edges")
    samples = [sample_record(parameter) for parameter in N3_SAMPLE_PARAMETERS]
    contact_certificates = [str(sample["contact_certificate"]) for sample in samples]
    geometric_keys = [str(sample["geometric_key"]) for sample in samples]
    if len(set(contact_certificates)) != 2 or len(set(contact_certificates[1:])) != 1:
        raise ValueError("n=3 contact certificates do not distinguish only the corner stratum")
    if len(set(geometric_keys)) != len(geometric_keys):
        raise ValueError(
            "n=3 geometric samples should remain distinct in the quotient interval"
        )
    strata = [
        {
            "id": "C",
            "name": "corner/L endpoint",
            "parameter": "0",
            "stratum_dimension": 0,
            "local_dimension": 1,
            "stabilizer_order": stabilizer_order(n3_positions(Fraction(0))),
            "wall_incidences": 6,
            "pair_contacts": 3,
            "active_sat_axes": 4,
        },
        {
            "id": "G",
            "name": "generic slider",
            "parameter": "0<lambda<1/2",
            "stratum_dimension": 1,
            "local_dimension": 1,
            "stabilizer_order": stabilizer_order(n3_positions(Fraction(1, 4))),
            "wall_incidences": 5,
            "pair_contacts": 3,
            "active_sat_axes": 3,
        },
        {
            "id": "M",
            "name": "centred slider endpoint",
            "parameter": "1/2",
            "stratum_dimension": 0,
            "local_dimension": 1,
            "stabilizer_order": stabilizer_order(n3_positions(Fraction(1, 2))),
            "wall_incidences": 5,
            "pair_contacts": 3,
            "active_sat_axes": 3,
        },
    ]
    if [stratum["stabilizer_order"] for stratum in strata] != [2, 1, 2]:
        raise ValueError("n=3 quotient stabilizers drifted")
    literature = literature_record(3, [2, 2], [24, 24], unlabelled_betti=[1, 1])
    require_literature_matches(literature, require_unlabelled_n3=True)
    return {
        "schema_version": SCHEMA_VERSION,
        "subject": {
            "n": 3,
            "square_side": "1",
            "container_side": "2",
            "scope": "all physical orientations, with each square angle modulo pi/2",
        },
        "orientation_forcing": orientation_forcing_record(),
        "separation_enumeration": {
            "raw_branch_count": raw_count,
            "consistent_branch_count": len(cells),
            "dimension_histogram": {"1": len(cells)},
            "records": relation_records(3, cells),
        },
        "spaces": {
            "labelled": labelled | {"homeomorphism_type": "two disjoint circles"},
            "s3_quotient": unlabelled | {"homeomorphism_type": "circle"},
            "d4_s3_quotient": {
                "vertex_count": N3_QUOTIENT_VERTICES,
                "edge_count": N3_QUOTIENT_EDGES,
                "component_count": 1,
                "betti": [1, 0],
                "homeomorphism_type": "closed interval [0,1/2]",
                "parameter": "lambda=min(x,1-x)",
                "display_parameter_identification": "t~2-t for t in [1/2,3/2]",
                "incidence": {"closure(G)": ["C", "G", "M"]},
                "strata": strata,
            },
        },
        "samples": samples,
        "literature": literature,
        "determination": {
            "outcome": "criterion_met",
            "claim": "F_3(2) is two labelled circles; its S3 quotient is a circle and its D4 x S3 quotient is a closed interval",
            "scope": "complete side-2 physical configuration space; no claim for larger side or n>=5",
        },
    }


def build_n4_model() -> dict[str, object]:
    """Build the exhaustive n=4 grid classification."""
    raw_count, cells = enumerate_separation_cells(4)
    if raw_count != N4_RAW_BRANCHES or len(cells) != N4_CONSISTENT_BRANCHES:
        raise ValueError(f"n=4 branch count drift: {raw_count} raw, {len(cells)} consistent")
    if {len(cell.free_variables) for cell in cells} != {0}:
        raise ValueError("every consistent n=4 branch must be zero-dimensional")
    states = {state_id(cell.states[0]): cell.states[0] for cell in cells}
    multiplicities = Counter(state_id(cell.states[0]) for cell in cells)
    if len(states) != N4_LABELLED_STATES or set(multiplicities.values()) != {
        N4_BRANCHES_PER_STATE
    }:
        raise ValueError("n=4 branches do not reduce four-to-one onto 24 labelled grids")
    if not all(verify_state(state) for state in states.values()):
        raise ValueError("an enumerated n=4 grid state failed exact verification")
    stabilizer = stabilizer_order(GRID_CORNERS)
    if stabilizer != len(d4_actions()):
        raise ValueError("the unlabelled 2 x 2 grid does not have full D4 stabilizer")
    literature = literature_record(4, [24, 0], [24])
    require_literature_matches(literature, require_unlabelled_n3=False)
    return {
        "schema_version": SCHEMA_VERSION,
        "subject": {
            "n": 4,
            "square_side": "1",
            "container_side": "2",
            "scope": "all physical orientations, with each square angle modulo pi/2",
        },
        "orientation_forcing": orientation_forcing_record(),
        "separation_enumeration": {
            "raw_branch_count": raw_count,
            "consistent_branch_count": len(cells),
            "dimension_histogram": {"0": len(cells)},
            "unique_state_count": len(states),
            "branch_multiplicity_per_state": N4_BRANCHES_PER_STATE,
            "records": relation_records(4, cells),
        },
        "spaces": {
            "labelled": {
                "vertex_count": len(states),
                "edge_count": 0,
                "component_count": len(states),
                "betti": [len(states), 0],
                "homeomorphism_type": "24 isolated labelled grids",
                "states": sorted(states),
            },
            "s4_quotient": {
                "vertex_count": 1,
                "edge_count": 0,
                "component_count": 1,
                "betti": [1, 0],
                "homeomorphism_type": "point",
            },
            "d4_s4_quotient": {
                "vertex_count": 1,
                "edge_count": 0,
                "component_count": 1,
                "betti": [1, 0],
                "homeomorphism_type": "point",
                "stabilizer_order": stabilizer,
                "stabilizer_structure": "D4 in the combined D4 x S4 action",
            },
        },
        "literature": literature,
        "determination": {
            "outcome": "criterion_met",
            "claim": "F_4(2) is 24 isolated labelled grids and both symmetry quotients are one point",
            "scope": "complete side-2 physical configuration space; no claim for n>=5",
        },
    }


def render_n3_moduli_svg(model: dict[str, object]) -> str:
    """Render the deterministic n=3 quotient and stratum map."""
    if model["subject"] != {
        "n": 3,
        "square_side": "1",
        "container_side": "2",
        "scope": "all physical orientations, with each square angle modulo pi/2",
    }:
        raise ValueError("the n=3 renderer received the wrong semantic model")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" role="img">',
        "<title>Exact optimal configuration spaces for three unit squares in side 2</title>",
        "<desc>Two labelled 12-cycles quotient to one unlabelled four-cycle and then to the C-G-M interval. Packing glyphs show the corner, generic, and centred strata.</desc>",
        "<style>",
        ":root{--bg:#fbfaf7;--ink:#17202a;--muted:#637083;--line:#8290a3;--panel:#ffffff;--c:#d97706;--g:#2563eb;--m:#7c3aed;--sq1:#0f766e;--sq2:#be123c;--sq3:#7c3aed}",
        "@media(prefers-color-scheme:dark){:root{--bg:#111827;--ink:#f3f4f6;--muted:#aab4c3;--line:#64748b;--panel:#1f2937;--c:#f59e0b;--g:#60a5fa;--m:#a78bfa;--sq1:#2dd4bf;--sq2:#fb7185;--sq3:#c4b5fd}}",
        "text{font-family:ui-sans-serif,system-ui,-apple-system,sans-serif;fill:var(--ink)} .muted{fill:var(--muted)} .edge{stroke:var(--line);stroke-width:2;fill:none} .panel{fill:var(--panel);stroke:var(--line);stroke-width:1.5} .node{stroke:var(--panel);stroke-width:2} .label{font-size:15px;font-weight:650} .small{font-size:12px}",
        "</style>",
        f'<rect width="{SVG_WIDTH}" height="{SVG_HEIGHT}" fill="var(--bg)"/>',
        '<text x="55" y="55" font-size="27" font-weight="750">F₃(2): exact quotient and stratum map</text>',
        '<text x="55" y="82" class="muted" font-size="14">Arbitrary rotations add no configurations; the full physical space is axis-aligned.</text>',
        '<rect class="panel" x="45" y="105" width="670" height="360" rx="14"/>',
        '<text x="70" y="140" class="label">Labelled space: two disjoint 12-cycles</text>',
    ]
    for component, (centre_x, centre_y, colour) in enumerate(
        ((230, 290, "var(--g)"), (520, 290, "var(--m)"))
    ):
        points = [(centre_x + dx, centre_y + dy) for dx, dy in CYCLE_OFFSETS]
        for index, (x, y) in enumerate(points):
            next_x, next_y = points[(index + 1) % len(points)]
            lines.append(
                f'<line id="labelled-{component}-edge-{index}" class="edge" x1="{x}" y1="{y}" x2="{next_x}" y2="{next_y}"/>'
            )
        for index, (x, y) in enumerate(points):
            lines.append(
                f'<circle id="labelled-{component}-vertex-{index}" class="node" cx="{x}" cy="{y}" r="7" fill="{colour}"/>'
            )
        lines.append(
            f'<text x="{centre_x}" y="{centre_y + 5}" text-anchor="middle" class="small">component {component + 1}</text>'
        )
    lines += [
        '<text x="690" y="280" text-anchor="middle" class="label">/ S₃</text>',
        '<path class="edge" d="M650 295 H735" marker-end="url(#arrow)"/>',
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="var(--line)"/></marker></defs>',
        '<rect class="panel" x="750" y="105" width="405" height="360" rx="14"/>',
        '<text x="775" y="140" class="label">Unlabelled quotient: one four-cycle</text>',
    ]
    four_cycle = ((860, 220), (1020, 220), (1020, 380), (860, 380))
    for index, (x, y) in enumerate(four_cycle):
        next_x, next_y = four_cycle[(index + 1) % len(four_cycle)]
        lines.append(
            f'<line id="s3-edge-{index}" class="edge" x1="{x}" y1="{y}" x2="{next_x}" y2="{next_y}"/>'
        )
        lines.append(
            f'<circle id="s3-vertex-{index}" class="node" cx="{x}" cy="{y}" r="9" fill="var(--c)"/>'
        )
    lines += [
        '<text x="940" y="305" text-anchor="middle" class="small">missing-corner cycle</text>',
        '<text x="940" y="430" text-anchor="middle" class="muted small">The D₄ reflection fixes each edge midpoint.</text>',
        '<rect class="panel" x="45" y="495" width="1110" height="360" rx="14"/>',
        '<text x="70" y="530" class="label">Full quotient by D₄ × S₃: interval λ ∈ [0, 1/2]</text>',
        '<line id="quotient-edge" x1="180" y1="600" x2="1020" y2="600" stroke="var(--g)" stroke-width="8" stroke-linecap="round"/>',
        '<circle id="stratum-C" cx="180" cy="600" r="15" fill="var(--c)" class="node"/>',
        '<circle id="stratum-M" cx="1020" cy="600" r="15" fill="var(--m)" class="node"/>',
        '<text x="180" y="575" text-anchor="middle" class="label">C</text>',
        '<text x="600" y="575" text-anchor="middle" class="label">G</text>',
        '<text x="1020" y="575" text-anchor="middle" class="label">M</text>',
        '<text x="180" y="630" text-anchor="middle" class="small">walls 6 · axes 4 · stab 2</text>',
        '<text x="600" y="630" text-anchor="middle" class="small">walls 5 · axes 3 · stab 1</text>',
        '<text x="1020" y="630" text-anchor="middle" class="small">walls 5 · axes 3 · stab 2</text>',
    ]
    glyphs = (
        (180, Fraction(0), "corner/L"),
        (600, Fraction(1, 4), "generic"),
        (1020, Fraction(1, 2), "centred"),
    )
    for centre_x, parameter, label in glyphs:
        board_x = centre_x - GLYPH_BOARD_SIZE // 2
        board_y = 675
        lines.append(
            f'<g id="packing-{fraction_text(parameter).replace("/", "-")}" transform="translate({board_x},{board_y})">'
        )
        lines.append(
            f'<rect x="0" y="0" width="{GLYPH_BOARD_SIZE}" height="{GLYPH_BOARD_SIZE}" fill="none" stroke="var(--ink)" stroke-width="3"/>'
        )
        for square, (x, y) in enumerate(n3_positions(parameter)):
            svg_x = format_svg_number(x.numerator * GLYPH_SQUARE_SIZE / x.denominator)
            flipped = Fraction(1) - y
            svg_y = format_svg_number(
                flipped.numerator * GLYPH_SQUARE_SIZE / flipped.denominator
            )
            lines.append(
                f'<rect x="{svg_x}" y="{svg_y}" width="{GLYPH_SQUARE_SIZE}" height="{GLYPH_SQUARE_SIZE}" fill="var(--sq{square + 1})" fill-opacity="0.78" stroke="var(--panel)" stroke-width="1.5"/>'
            )
        lines.append("</g>")
        lines.append(
            f'<text x="{centre_x}" y="820" text-anchor="middle" class="small">λ={fraction_text(parameter)} · {label}</text>'
        )
    lines += [
        '<text x="70" y="842" class="muted small">C and M are zero-dimensional orbit strata. Only C changes the active signature; M is singular because its stabilizer jumps.</text>',
        "</svg>",
        "",
    ]
    root = ET.fromstring("\n".join(lines))
    style = root.find(svg_tag("style"))
    if style is None:
        raise ValueError("the n=3 figure lost its renderer-owned style")
    root.remove(style)
    colours = {
        "--bg": "#fbfaf7",
        "--ink": "#17202a",
        "--muted": "#637083",
        "--line": "#8290a3",
        "--panel": "#ffffff",
        "--c": "#d97706",
        "--g": "#2563eb",
        "--m": "#7c3aed",
        "--sq1": "#0f766e",
        "--sq2": "#be123c",
        "--sq3": "#7c3aed",
    }
    class_attributes = {
        "muted": {"fill": colours["--muted"]},
        "edge": {"stroke": colours["--line"], "stroke-width": "2", "fill": "none"},
        "panel": {
            "fill": colours["--panel"],
            "stroke": colours["--line"],
            "stroke-width": "1.5",
        },
        "node": {"stroke": colours["--panel"], "stroke-width": "2"},
        "label": {"font-size": "15", "font-weight": "650"},
        "small": {"font-size": "12"},
    }
    for node in root.iter():
        if node.tag == svg_tag("text"):
            node.attrib.setdefault("font-family", "ui-sans-serif, system-ui, sans-serif")
            node.attrib.setdefault("fill", colours["--ink"])
        for class_name in node.attrib.get("class", "").split():
            for attribute, value in class_attributes.get(class_name, {}).items():
                node.attrib.setdefault(attribute, value)
        for attribute, attribute_value in tuple(node.attrib.items()):
            resolved_value = attribute_value
            for variable, colour in colours.items():
                resolved_value = resolved_value.replace(f"var({variable})", colour)
            node.set(attribute, resolved_value)
    title = root.find(svg_tag("title"))
    description = root.find(svg_tag("desc"))
    if title is None or description is None:
        raise ValueError("the n=3 figure requires an accessible name")
    title.set("id", "figure-title")
    description.set("id", "figure-description")
    root.set("aria-labelledby", "figure-title figure-description")
    metadata = append_metadata(
        root,
        {
            "evidence": "proved-optimum",
            "source-id": "exp-014-h-032-n3-optimal-moduli",
            "view": "exact-quotient-map",
        },
    )
    root.remove(metadata)
    root.insert(2, metadata)
    return serialize_svg(root)


def invalid_lowered_slider_rejected() -> bool:
    """Known-overlap control through the independent exact verifier."""
    positions = (
        (Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(0)),
        (Fraction(1, 4), Fraction(7, 8)),
    )
    squares = [exact_square(point) for point in positions]
    return not verify_packing(squares, SIDE, sign=fraction_sign).valid


def run_n3_selftests(model: dict[str, object], svg: str) -> dict[str, bool]:
    """Known-answer mutations for topology, identity, quotient and render drift."""
    spaces = model["spaces"]
    if not isinstance(spaces, dict):
        raise ValueError("n=3 spaces record is malformed")
    labelled = spaces["labelled"]
    if not isinstance(labelled, dict):
        raise ValueError("n=3 labelled record is malformed")
    vertices = {str(vertex) for vertex in labelled["vertices"]}
    edges: set[Edge] = {
        cast(Edge, tuple(str(value) for value in edge)) for edge in labelled["edges"]
    }
    components = labelled["components"]
    if not isinstance(components, list) or len(components) != 2:
        raise ValueError("n=3 component record is malformed")
    removed = graph_summary(vertices, set(sorted(edges)[1:]))
    first_component = components[0]
    second_component = components[1]
    if not isinstance(first_component, list) or not isinstance(second_component, list):
        raise ValueError("n=3 component members are malformed")
    bridged_edges = set(edges)
    bridged_edges.add(
        cast(Edge, tuple(sorted((str(first_component[0]), str(second_component[0])))))
    )
    bridged = graph_summary(vertices, bridged_edges)
    samples = model["samples"]
    if not isinstance(samples, list):
        raise ValueError("n=3 samples record is malformed")
    certificates = [
        str(sample["contact_certificate"]) for sample in samples if isinstance(sample, dict)
    ]
    literature = model["literature"]
    if not isinstance(literature, dict):
        raise ValueError("n=3 literature record is malformed")
    alpert = literature.get("alpert_et_al_2023")
    alvarado = literature.get("alvarado_garduno_gonzalez_2025")
    original_svg_hash = hashlib.sha256(svg.encode()).hexdigest()
    return {
        "deleted_family_edge_is_rejected": removed["betti"] != [2, 2],
        "collapsed_label_components_are_rejected": bridged["component_count"] != 2,
        "constant_closed_family_certificate_is_rejected": len(set(certificates)) == 2,
        "unreduced_display_parameter_is_rejected": quotient_parameter(Fraction(1, 4))
        == quotient_parameter(Fraction(3, 4)),
        "nonaxis_center_boundary_equality_is_rejected": Fraction(5, 4)
        * (Fraction(1) - Fraction(5, 8))
        < Fraction(1, 2),
        "lowered_slider_overlap_is_rejected": invalid_lowered_slider_rejected(),
        "duplicate_or_missing_cells_are_rejected": len(edges)
        == len(set(edges))
        == N3_LABELLED_EDGES,
        "labelled_and_unlabelled_source_scopes_are_separate": isinstance(alpert, dict)
        and alpert.get("reported_betti") == [2, 2]
        and alpert.get("derived_match") is True
        and isinstance(alvarado, dict)
        and alvarado.get("derived_match") is True,
        "stale_svg_is_rejected": original_svg_hash
        != hashlib.sha256((svg + " ").encode()).hexdigest(),
    }


def run_n4_selftests(model: dict[str, object]) -> dict[str, bool]:
    """Known-answer mutations for the rigid n=4 cell."""
    enumeration = model["separation_enumeration"]
    spaces = model["spaces"]
    if not isinstance(enumeration, dict) or not isinstance(spaces, dict):
        raise ValueError("n=4 record is malformed")
    labelled = spaces["labelled"]
    quotient = spaces["d4_s4_quotient"]
    if not isinstance(labelled, dict) or not isinstance(quotient, dict):
        raise ValueError("n=4 spaces record is malformed")
    literature = model["literature"]
    if not isinstance(literature, dict):
        raise ValueError("n=4 literature record is malformed")
    alpert = literature.get("alpert_et_al_2023")
    invalid_grid = (
        exact_square((Fraction(0), Fraction(0))),
        exact_square((Fraction(1), Fraction(0))),
        exact_square((Fraction(0), Fraction(1))),
        exact_square((Fraction(1, 2), Fraction(1))),
    )
    return {
        "missing_grid_state_is_rejected": int(labelled["vertex_count"]) - 1
        != N4_LABELLED_STATES,
        "positive_dimensional_branch_is_rejected": enumeration["dimension_histogram"]
        == {"0": N4_CONSISTENT_BRANCHES},
        "branch_alias_multiplicity_is_checked": enumeration["branch_multiplicity_per_state"]
        == N4_BRANCHES_PER_STATE,
        "shifted_grid_overlap_is_rejected": not verify_packing(
            invalid_grid, SIDE, sign=fraction_sign
        ).valid,
        "combined_stabilizer_is_full_D4": quotient["stabilizer_order"] == 8,
        "unreported_source_f_vector_remains_null": isinstance(alpert, dict)
        and alpert.get("reported_betti") == [24, 0]
        and alpert.get("reported_f_vector") is None
        and alpert.get("derived_match") is True,
    }


def build_result(n: int) -> tuple[dict[str, object], str | None]:
    """Build one deterministic terminal result and optional n=3 SVG."""
    model = build_n3_model() if n == 3 else build_n4_model()
    svg = render_n3_moduli_svg(model) if n == 3 else None
    selftests = run_n3_selftests(model, svg) if svg is not None else run_n4_selftests(model)
    if not all(selftests.values()):
        failed = [name for name, passed in selftests.items() if not passed]
        raise ValueError(f"small-n selftests failed: {failed}")
    model["selftests"] = selftests
    if svg is not None:
        model["artifacts"] = {
            "svg": "atlas/n-003-optimal-moduli.svg",
            "svg_sha256": hashlib.sha256(svg.encode()).hexdigest(),
        }
    return model, svg


def write_text_atomic(path: Path, text: str) -> None:
    """Write a retained artifact atomically."""
    with atomic_output_file(path, make_parents=True) as temporary:
        temporary.write_text(text, encoding="utf-8")


def replay_record(record_path: Path, svg_path: Path | None, n: int) -> dict[str, object]:
    """Rebuild and compare every semantic and rendered field."""
    loaded = json.loads(record_path.read_text(encoding="utf-8"))
    expected, expected_svg = build_result(n)
    if loaded != expected:
        raise ValueError("retained JSON record differs from the exact regenerated model")
    if n == 3:
        if svg_path is None:
            raise ValueError("n=3 replay requires --check-svg")
        if expected_svg is None or svg_path.read_text(encoding="utf-8") != expected_svg:
            raise ValueError("retained n=3 SVG differs from the deterministic render")
    elif svg_path is not None:
        raise ValueError("n=4 has no SVG; omit --check-svg")
    determination = expected["determination"]
    if not isinstance(determination, dict):
        raise ValueError("determination record is malformed")
    return {
        "schema_version": SCHEMA_VERSION,
        "n": n,
        "record_replayed": True,
        "svg_replayed": n == 3,
        "determination_outcome": determination["outcome"],
        "selftests": expected["selftests"],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, choices=(3, 4), required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--record", type=Path, help="write the exact JSON record atomically")
    mode.add_argument("--replay", type=Path, help="rebuild and compare a retained JSON record")
    parser.add_argument("--svg", type=Path, help="write the deterministic n=3 SVG")
    parser.add_argument("--check-svg", type=Path, help="byte-compare the retained n=3 SVG")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.monotonic()
    try:
        if args.replay is not None:
            if args.svg is not None:
                raise ValueError("--svg is generation-only; use --check-svg with --replay")
            summary = replay_record(args.replay, args.check_svg, args.n)
        else:
            if args.check_svg is not None:
                raise ValueError("--check-svg requires --replay")
            result, svg = build_result(args.n)
            if args.n == 3 and args.record is not None and args.svg is None:
                raise ValueError("n=3 retained generation requires --svg")
            if args.n == 4 and args.svg is not None:
                raise ValueError("n=4 has no SVG output")
            if args.record is not None:
                write_text_atomic(
                    args.record, json.dumps(result, indent=2, sort_keys=True) + "\n"
                )
            if args.svg is not None:
                if svg is None:
                    raise ValueError("renderer produced no n=3 SVG")
                write_text_atomic(args.svg, svg)
            determination = result["determination"]
            if not isinstance(determination, dict):
                raise ValueError("determination record is malformed")
            summary = {
                "schema_version": SCHEMA_VERSION,
                "n": args.n,
                "record_written": args.record is not None,
                "svg_written": args.svg is not None,
                "determination_outcome": determination["outcome"],
                "selftests": result["selftests"],
            }
        summary["elapsed_seconds"] = round(time.monotonic() - started, 6)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
