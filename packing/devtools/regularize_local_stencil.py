#!/usr/bin/env python3
"""Test an exact local placement at the house side and admit it if it improves the drawing.

From packing, preview with
`python -m devtools.regularize_local_stencil --n 127 --stack 108 110 116`.
The three square IDs name the fixed anchor, its right neighbor, and the square
immediately above that neighbor in the witness's native frame. The upper square
is straightened. The other 125 placements in this example stay fixed.

To align faces on a selected first-party axis view, use `--n 259 --face 118 114`.
Each `--face MOVED ANCHOR` places MOVED against ANCHOR along the dominant native
coordinate. Multiple pairs are applied in order and checked together.

Use `--install --receipt packing/cases/regularized_drawings/RUN/receipt.json`
to write the verified view and its admission receipt. Regenerate the atlas and
case records through the normal regularization process.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import time
from collections.abc import Sequence
from dataclasses import asdict
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import census_drawing_regularity as census
from devtools import default_drawings, regularize_select
from devtools import regularize_axis_components as axis
from devtools import regularize_evand as driver
from devtools import regularize_grid_slack as grid
from devtools import regularize_same_side as same
from sqpack.witness import validate_witness_document, witness_document
from sqpack.yamlio import load_yaml

REPO = Path(__file__).resolve().parents[2]
TOOL = "packing/devtools/regularize_local_stencil.py"
METHOD = (
    "regularize_local_stencil/1: exact axis-aligned stack from a fixed source square, "
    "with all other placements held and both exact verification routes applied"
)
FACE_METHOD = (
    "regularize_local_stencil/2: aligned faces on the selected regularize_axis_components/2 "
    "drawing, with its other squares and all its rotations held at the registered side"
)
AXIS_ORIENTATIONS = {(1, 0), (-1, 0), (0, 1), (0, -1)}
RECEIPTS = Path("packing/cases/regularized_drawings")


def view_path(n: int) -> str:
    return f"{driver.LAYER_DIR}/n-{n:03d}-regularized.yaml.gz"


def receipt_path(path: Path) -> Path:
    resolved = (REPO / path).resolve()
    if resolved.parent.parent != REPO / RECEIPTS or resolved.name != "receipt.json":
        raise ValueError(
            "the receipt must be receipt.json in a regularized drawings run directory"
        )
    return resolved


def stack(
    frame: same.Frame, labels: Sequence[str]
) -> tuple[list[same.Point], list[same.Matched], list[int]]:
    """Close the two full sides of a stack in a rational witness's native frame."""
    by_id = {str(label): index for index, label in enumerate(frame.ids)}
    if len(labels) != 3 or len(set(labels)) != 3 or not set(labels) <= by_id.keys():
        raise ValueError("the stack needs three distinct IDs from the witness")
    if frame.kind != "rational":
        raise ValueError("the local stack requires a rational source")
    left, right, upper = [by_id[label] for label in labels]
    if any(frame.rotations[index] not in AXIS_ORIENTATIONS for index in (left, right)):
        raise ValueError("the stack's anchor and right neighbor must already be axis aligned")
    x, y = frame.centers[left]
    centers = list(frame.centers)
    centers[right] = (x + 1, y)
    centers[upper] = (x + 1, y + 1)
    matched = [
        same.Matched(rotation, index, 0) for index, rotation in enumerate(frame.rotations)
    ]
    matched[upper] = same.Matched((Fraction(1), Fraction(0)), None, 0)
    return centers, matched, [upper + 1]


def aligned_faces(
    frame: same.Frame, faces: Sequence[Sequence[str]]
) -> tuple[list[same.Point], list[dict[str, Any]]]:
    """Translate each moved square against the named anchor and keep every requested side."""
    if frame.kind != "rational" or not faces:
        raise ValueError("face alignment requires a rational frame and at least one pair")
    indices = {str(label): i for i, label in enumerate(frame.ids)}
    centers = frame.centers.copy()
    steps: list[dict[str, Any]] = []
    for pair in faces:
        if len(pair) != 2 or pair[0] == pair[1] or not set(pair) <= indices.keys():
            raise ValueError("each face needs two distinct square IDs from the base drawing")
        moved, anchor = [indices[label] for label in pair]
        if any(frame.rotations[i] not in AXIS_ORIENTATIONS for i in (moved, anchor)):
            raise ValueError("both squares of each face must be exactly axis aligned")
        x, y = centers[moved]
        ax, ay = centers[anchor]
        dx, dy = x - ax, y - ay
        if abs(dx) == abs(dy):
            raise ValueError("the two centers have no unique dominant axis")
        offset = (1 if dx > 0 else -1, 0) if abs(dx) > abs(dy) else (0, 1 if dy > 0 else -1)
        target = ax + offset[0], ay + offset[1]
        centers[moved] = target
        steps.append(
            {
                "moved": pair[0],
                "anchor": pair[1],
                "offset": list(offset),
                "translation": [same.literal(target[0] - x), same.literal(target[1] - y)],
            }
        )
    for step in steps:
        x, y = centers[indices[step["moved"]]]
        ax, ay = centers[indices[step["anchor"]]]
        if [x - ax, y - ay] != step["offset"]:
            raise ValueError("a later move reopened an earlier requested face")
    if centers == frame.centers:
        raise ValueError("the requested faces already coincide on the base drawing")
    return centers, steps


def certified_view(
    witness: dict[str, Any],
    frame: same.Frame,
    labels: Sequence[str],
    *,
    face_centers: list[same.Point] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], list[int]]:
    """Check the candidate read back from its witness representation, on both routes."""
    if face_centers is None:
        centers, matched, straightened = stack(frame, labels)
        method = "local stack"
    else:
        centers = face_centers
        matched = [same.Matched(rotation, i, 0) for i, rotation in enumerate(frame.rotations)]
        straightened = []
        method = "local face alignment"
    view = same.same_side_witness(
        witness, frame, centers, matched, view_id=grid.regularized_id(witness)
    )
    view["claim"]["limitations"] = (
        f"An exact same-side placement made by the {method} generator. "
        "This certificate establishes feasibility."
    )
    document = load_yaml(witness_document(view))
    validate_witness_document(
        document,
        path=grid.WITNESS_SCHEMA.parent / "local-stencil.yaml",
        fallback_schema=grid.WITNESS_SCHEMA,
    )
    decoded = document["witness"]
    replay = same.exact_frame(decoded)
    if (
        replay.side != frame.side
        or replay.ids != frame.ids
        or replay.centers != centers
        or replay.rotations != [item.rotation for item in matched]
    ):
        raise ValueError("the serialized placement does not reproduce the proposed geometry")
    verdicts = same.verify_both(decoded, replay.centers, matched, replay.side)
    pairs = math.comb(len(centers), 2)
    if not all(
        route["passed"] and route["pairs_tested"] == pairs for route in verdicts.values()
    ):
        raise ValueError(f"the proposed placement failed exact verification: {verdicts}")
    decoded["claim"]["coordinate_provenance"] = "verified"
    return decoded, verdicts, straightened


def drawing_before(n: int) -> tuple[census.Drawing, dict[str, Any]]:
    """Read the same selected witness or view as the site's default renderer."""
    entries = census.read_index(REPO)
    selected = default_drawings.regularized_defaults(
        REPO / default_drawings.RECORD_PATH, REPO / census.INDEX
    )
    return census.drawing_for(REPO, n, {key: entries[key] for key in selected})


def face_base(
    n: int,
    reference: dict[str, Any],
    source: dict[str, Any],
    drawing: dict[str, Any],
    *,
    selected: bool,
    selection_digest: str,
) -> tuple[same.Frame, dict[str, Any]]:
    """Replay the axis recipe from the house. The digest records the input as published."""
    layout = driver.layer_layout(REPO)
    manifest = next(row for row in axis.manifest_entries(layout) if row["n"] == n)
    original, text, _seconds = axis.atlas_record(manifest, layout, smallest_dilation=False)
    for entry in (reference, original):
        if (
            entry.get("n") != n
            or entry.get("generator") != axis.ALGORITHM
            or entry.get("status") != "regularized"
            or (entry.get("view") or {}).get("path") != view_path(n)
            or not (entry.get("exact_verification") or {}).get("passed")
            or any(
                entry["source"].get(k) != source[k] for k in ("witness", "id", "scalar_kind")
            )
        ):
            raise ValueError(
                "the base must match the verified axis drawing of the official house"
            )
    if text is None:
        raise ValueError("the original axis drawing could not be regenerated from the house")
    rebuilt = load_yaml(text)["witness"]
    if (
        rebuilt["n"] != n
        or rebuilt["id"] != f"{source['id']}-regularized"
        or any(drawing[k] != rebuilt[k] for k in ("id", "n", "source"))
    ):
        raise ValueError("the drawing and regenerated axis base name different sources")
    frame = same.exact_frame(rebuilt)
    if selected:
        incumbent = same.exact_frame(drawing)
        if (
            incumbent.kind != "rational"
            or incumbent.ids != frame.ids
            or incumbent.side != frame.side
            or incumbent.centers != frame.centers
            or incumbent.rotations != frame.rotations
        ):
            raise ValueError("the selected geometry differs from the regenerated axis base")
    provenance = {
        "generator": axis.ALGORITHM,
        "recipe": "devtools.regularize_axis_components.atlas_record",
        "smallest_dilation": False,
        "source": source,
        "id": rebuilt["id"],
        "path_at_selection": view_path(n),
        "sha256": selection_digest,
    }
    return frame, provenance


def prepare(
    n: int, labels: Sequence[str], run: str, *, faces: Sequence[Sequence[str]] = ()
) -> tuple[driver.Admitted, dict[str, Any]]:
    source_path = Path(f"packing/witnesses/known-best/n-{n:03d}.yaml")
    source_bytes = (REPO / source_path).read_bytes()
    house = load_yaml(source_bytes.decode("utf-8"))["witness"]
    frame = same.exact_frame(house)
    facts = driver.case_facts(n)
    bound = driver.verified_bound(facts)
    if bound is None or bound.compare(frame.side) != 0:
        raise ValueError("the exact house side must equal the registered bound")

    origin = {
        "witness": source_path.as_posix(),
        "id": str(house["id"]),
        "scalar_kind": str(house["scalar"]["kind"]),
        "sha256": hashlib.sha256(source_bytes).hexdigest(),
    }
    drawing, current = drawing_before(n)
    generator = axis.LOCAL_STENCIL_GENERATOR
    face_centers = None
    if faces:
        if labels or drawing.generator != axis.ALGORITHM or drawing.path != view_path(n):
            raise ValueError("face alignment requires the selected first-party axis drawing")
        entry = census.read_index(REPO)[n]
        text = gzip.decompress((REPO / drawing.path).read_bytes())
        base, base_record = face_base(
            n,
            entry,
            origin,
            current,
            selected=True,
            selection_digest=hashlib.sha256(text).hexdigest(),
        )
        if base.side != frame.side or base.ids != frame.ids:
            raise ValueError("the axis base differs from the house side or square IDs")
        frame = base
        face_centers, steps = aligned_faces(base, faces)
        generator = axis.LOCAL_FACE_GENERATOR
        provenance = {"native_frame": True, "base": base_record, "faces": steps}
    else:
        if len(labels) != 3:
            raise ValueError("the stack needs three distinct IDs from the witness")
        provenance = {
            "native_frame": True,
            "anchor": labels[0],
            "right": labels[1],
            "upper": labels[2],
        }
    view, verdicts, straightened = certified_view(
        house, frame, labels, face_centers=face_centers
    )
    measured = grid.measure(n, house, view, straightened)
    report = {
        "n": n,
        "measured": measured,
        "attempts": [{"exact": {"side": same.literal(frame.side), "verdicts": verdicts}}],
    }
    decision = grid.decided(report, house)
    if decision.row != axis.ADMITTING_ROW or decision.decision != "admit":
        raise ValueError(f"the placement did not pass row 10: {decision.reason}")
    if measured["drawing"]["replica_disagrees"]:
        raise ValueError("the contact census disagrees with the renderer")

    before = regularize_select.measured(n, drawing, current)
    after = regularize_select.measured(
        n,
        census.Drawing(n, "regularized-view", view_path(n), generator),
        view,
    )
    gains, losses = regularize_select.compare(after, before)
    if losses or not gains:
        raise ValueError(
            f"the placement must improve the displayed drawing without losses: {losses}"
        )

    ident = measured["identity"]
    contacts = measured["shades"]
    identity = {
        "basis": "measured",
        "measured_in": driver.LAYER_INDEX_PATH,
        "one_to_one": ident["one_to_one"],
        **(
            {
                "moved": int(ident["moved"]),
                "max_move": float(ident["max_move"]),
                "max_turn_deg": float(ident["max_turn_deg"]),
            }
            if ident["one_to_one"]
            else {}
        ),
    }
    regularization = {
        "n": n,
        "of_witness": house["id"],
        "provenance": driver.packing_credit(
            facts, (house.get("source") or {}).get("key"), "same"
        ),
        "by": "project",
        "method": FACE_METHOD if faces else METHOD,
        "side": "same",
        "identity": identity,
    }
    admitted = driver.Admitted(
        n=n,
        generator=generator,
        run={"id": run, "output": "same"},
        source=origin,
        side={
            "reported": str(house["side"]),
            "view": same.literal(frame.side),
            "relation": "same",
            "view_minus_reported": "0.000e+00",
            "view_minus_verified_upper_bound": "0.000e+00",
        },
        view=view,
        provenance=provenance,
        routes={"repository_verifier": True, "independent_checker": True},
        decision={
            "row": decision.row,
            "decision": decision.decision,
            "reason": decision.reason,
        },
        measured={
            "identity_by": driver.IDENTITY_BY,
            "shades_by": driver.SHADES_BY,
            "contacts": {name: contacts[name] for name in driver.RULE_NAMES},
            "symmetry": int(ident.get("symmetry") or 0),
            "regressions": driver.regression_count(contacts),
            "level": None,
            "groups": [],
        },
        regularization=regularization,
        house_after=contacts["house"]["after"],
    )
    receipt = {
        "n": n,
        "source": origin,
        "construction": provenance,
        "side": admitted.side,
        "verdicts": verdicts,
        "identity": ident,
        "contacts": contacts,
        "decision": asdict(decision),
        "comparison": {"before": before, "after": after, "gains": gains, "losses": losses},
    }
    return admitted, receipt


def run_id(receipt: Path) -> str:
    return f"local-stencil-{receipt.parent.name}"


def already_installed(
    n: int, labels: Sequence[str], receipt: Path, *, faces: Sequence[Sequence[str]] = ()
) -> bool:
    """Recognize a completed install only after matching both the recipe and view."""
    entry = census.read_index(REPO).get(n) or {}
    generator = axis.LOCAL_FACE_GENERATOR if faces else axis.LOCAL_STENCIL_GENERATOR
    if entry.get("generator") != generator or entry["run"]["id"] != run_id(receipt):
        return False
    if not receipt.is_file():
        raise ValueError("the installed stencil needs its original admission receipt")
    admitted = json.loads(receipt.read_text(encoding="utf-8"))
    index_runs = driver.read_json(REPO / driver.LAYER_INDEX_PATH)["runs"]
    published = next((run for run in index_runs if run["id"] == entry["run"]["id"]), None)
    if (
        published is None
        or published != admitted.get("run")
        or published["parameters"]["admission_receipt"] != receipt.relative_to(REPO).as_posix()
        or admitted["comparison"]["after"]["drawing"]["path"] != view_path(n)
        or not all(
            admitted["verdicts"][route]["passed"]
            and admitted["verdicts"][route]["pairs_tested"] == math.comb(n, 2)
            for route in ("exact_verify", "independent")
        )
    ):
        raise ValueError("the retained receipt does not establish this installed run")
    construction = admitted["construction"]
    if admitted["n"] != n:
        raise ValueError("the retained receipt names a different count")
    _, installed = census.drawing_for(REPO, n, {n: entry})
    if faces:
        if labels or [(s["moved"], s["anchor"]) for s in construction["faces"]] != [
            tuple(pair) for pair in faces
        ]:
            raise ValueError("the retained receipt names different face pairs")
        frame, base = face_base(
            n,
            entry["reference"],
            admitted["source"],
            installed,
            selected=False,
            selection_digest=construction["base"]["sha256"],
        )
        centers, steps = aligned_faces(frame, faces)
        expected = {"native_frame": True, "base": base, "faces": steps}
        if (
            construction != expected
            or installed["certificate"]["generated"] != expected
            or {k: published["parameters"].get(k) for k in expected} != expected
        ):
            raise ValueError("the installed face recipe disagrees with the regenerated base")
        rotations = frame.rotations
    else:
        if [construction[key] for key in ("anchor", "right", "upper")] != list(labels):
            raise ValueError("the retained receipt names a different stack")
        _, house = census.drawing_for(REPO, n, {})
        frame = same.exact_frame(house)
        centers, matched, _ = stack(frame, labels)
        rotations = [item.rotation for item in matched]
    replay = same.exact_frame(installed)
    if (
        replay.side != frame.side
        or replay.ids != frame.ids
        or replay.centers != centers
        or replay.rotations != rotations
    ):
        raise ValueError("the installed drawing does not match its stencil")
    return True


def pending_paths(receipt: Path) -> tuple[Path, Path]:
    return receipt.with_name(".install-state.json"), receipt.with_name(".previous-view.yaml.gz")


def restore_interrupted(n: int, receipt: Path) -> None:
    """Restore only this count's old view while the atlas still names it."""
    state, backup = pending_paths(receipt)
    if not state.is_file():
        return
    prior = driver.read_json(state)
    if prior["n"] != n or prior["entry"] != census.read_index(REPO).get(n):
        raise ValueError("the atlas entry changed during the unfinished install")
    target = REPO / view_path(n)
    if prior["had_view"]:
        with atomic_output_file(target) as temporary:
            temporary.write_bytes(backup.read_bytes())
    else:
        target.unlink(missing_ok=True)
    receipt.unlink(missing_ok=True)
    state.unlink()
    backup.unlink(missing_ok=True)


def install(
    admitted: driver.Admitted, receipt: dict[str, Any], path: Path, elapsed: float, cpu: float
) -> None:
    """Install a decided view through the common atlas writer."""
    path = receipt_path(path)
    if path.exists():
        raise ValueError(f"receipt already exists: {path.relative_to(REPO)}")
    run = {
        "id": admitted.run["id"],
        "generator": admitted.generator,
        "finished": datetime.now(UTC).date().isoformat(),
        "parameters": {
            **admitted.provenance,
            "admission_receipt": path.relative_to(REPO).as_posix(),
        },
        "counts": 1,
        "decisions": {"admit": 1},
        "cost": {"wall_seconds": round(elapsed, 3), "cpu_seconds": round(cpu, 3), "workers": 1},
    }
    face = admitted.generator == axis.LOCAL_FACE_GENERATOR
    arguments = "--face MOVED ANCHOR" if face else "--stack A B C"
    generator = {
        "tool": TOOL,
        "generated_by": f"python -m devtools.regularize_local_stencil --n N {arguments}",
        "method": FACE_METHOD if face else METHOD,
        "credit": axis.ADMITTED_CREDITS[admitted.generator],
    }
    # Stage the receipt first. If the writer stops between the view and the
    # index, a retry can restore just that count's view before measuring again.
    target = REPO / view_path(admitted.n)
    state, backup = pending_paths(path)
    prior = {
        "n": admitted.n,
        "entry": census.read_index(REPO).get(admitted.n),
        "had_view": target.is_file(),
    }
    if prior["had_view"]:
        with atomic_output_file(backup, make_parents=True) as temporary:
            temporary.write_bytes(target.read_bytes())
    driver.write_json(state, prior)
    try:
        driver.write_json(path, {**receipt, "run": run})
        result = driver.admit_views(
            [admitted], REPO, generators={admitted.generator: generator}, runs=[run]
        )
    except Exception:
        if census.read_index(REPO).get(admitted.n) == prior["entry"]:
            restore_interrupted(admitted.n, path)
        raise
    if result["written"] != [admitted.n]:
        restore_interrupted(admitted.n, path)
        raise ValueError(f"the atlas did not accept the placement: {result}")
    state.unlink()
    backup.unlink(missing_ok=True)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", required=True, type=int)
    recipe = parser.add_mutually_exclusive_group(required=True)
    recipe.add_argument("--stack", nargs=3, metavar=("ANCHOR", "RIGHT", "UPPER"), default=())
    recipe.add_argument("--face", nargs=2, action="append", metavar=("MOVED", "ANCHOR"))
    parser.add_argument("--install", action="store_true")
    parser.add_argument(
        "--receipt", type=Path, help="repository-relative receipt.json for --install"
    )
    args = parser.parse_args(argv)
    if args.install != (args.receipt is not None):
        parser.error("--install and --receipt are used together")
    start, cpu = time.perf_counter(), time.process_time()
    path = receipt_path(args.receipt) if args.receipt is not None else None
    if path is not None and already_installed(args.n, args.stack, path, faces=args.face or ()):
        for staged in pending_paths(path):
            staged.unlink(missing_ok=True)
        print(f"n={args.n}: the verified placement is already in the layer")
        return 0
    if path is not None:
        restore_interrupted(args.n, path)
    run = run_id(path) if path is not None else "local-stencil-preview"
    admitted, receipt = prepare(args.n, args.stack, run, faces=args.face or ())
    if path is not None:
        install(admitted, receipt, path, time.perf_counter() - start, time.process_time() - cpu)
        print(f"n={args.n}: installed the verified local placement")
    else:
        print(json.dumps(receipt, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
