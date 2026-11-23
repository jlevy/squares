#!/usr/bin/env python3
"""Verify and admit Evan Daniel's original same-side regularized view of n = 304.

Run `python -m devtools.regularize_author_view` from packing to measure the retained
certificate against the current atlas. Add `--update` to write its drawing and the
admission receipt. The original certificate and review stay in the source archive.
"""

from __future__ import annotations

import argparse
import gzip
import json
import math
import time
from collections.abc import Mapping, Sequence
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import census_drawing_regularity as census
from devtools import check_half_angle_area as area
from devtools import check_rational_witness_independent as independent
from devtools import evand_exact_certificates as evand
from devtools import regularize_axis_components as axis
from devtools import regularize_evand as driver
from devtools import regularize_select as select
from devtools import render_regularized_atlas as atlas_views
from sqpack.witness import exact_verify
from sqpack.yamlio import load_yaml

REPO = Path(__file__).resolve().parents[2]
N = 304
PACKET = Path("packing/resources/web/evand-issue914-2026-11-05")
CERTIFICATE = PACKET / "source/search/packer/candidates/s304_1105_regularized.cert"
AUTHOR_REPORT = CERTIFICATE.with_suffix(".json")
REVIEW = PACKET / "review/review-2026-11-05/out/feasibility/s304_1105_regularized.json"
SOURCE_COMMIT = "bb4cc78e5b35103c1f177db55e9cf08974e66563"
OUTPUT = "author-certificate"
RUN = "evand-author-regularize-n304-2026-11-23"
DATE = "2026-11-23"
RECEIPT = Path(f"packing/cases/regularized_drawings/think-dc96-{DATE}/admission.json")
METHOD = (
    f"Evan Daniel's original regularization, evand/square-packing@{SOURCE_COMMIT}, "
    "imported and verified by devtools.regularize_author_view"
)


def retained_source(
    root: Path,
) -> tuple[evand.Certificate, dict[str, Any], dict[str, str], str]:
    """Read the retained certificate, its author settings and its archived review."""
    text = (root / CERTIFICATE).read_bytes().decode("utf-8")
    review = driver.read_json(root / REVIEW)
    certificate = evand.parse(text, expected_n=N)
    if (
        review["label"] != CERTIFICATE.stem
        or not Path(review["path"]).as_posix().endswith(f"/{CERTIFICATE.as_posix()}")
        or review["n"] != N
        or review["side"] != evand.literal(certificate.side)
        or review["pairs_expected"] != math.comb(N, 2)
        or not review["methods_agree_pair_by_pair"]
        or any(
            record["verdict"] != "accept"
            for record in (review, review["method_a"], review["method_b"])
        )
    ):
        raise ValueError("the author certificate does not match the archived acceptance")
    report = driver.read_json(root / AUTHOR_REPORT)
    if (
        report["n"] != N
        or report["S_cert"] != evand.literal(certificate.side)
        or report["by"] != ["Evan Daniel"]
        or report["cert_valid"] is not True
    ):
        raise ValueError("the author report does not describe the retained certificate")
    provenance = {
        "author": "Evan Daniel",
        "source_commit": SOURCE_COMMIT,
        "certificate": CERTIFICATE.as_posix(),
        # The acquisition packet holds custody. This is the archived review's provenance.
        "sha256": review["sha256"],
        "author_report": AUTHOR_REPORT.as_posix(),
        "archived_review": REVIEW.as_posix(),
    }
    return certificate, report, provenance, text


def source_problems(root: Path, view: Mapping[str, Any]) -> list[str]:
    """Hold a published author view to the original certificate's exact coordinates."""
    try:
        certificate, report, provenance, _text = retained_source(root)
    except (KeyError, OSError, ValueError) as error:
        return [f"n={N}: original regularization cannot be read: {error}"]
    if report["policy"] != "conservative" or report["level"] not in (0, 1, 2):
        return [f"n={N}: original regularization is outside the conservative levels"]
    source = evand.basis_witness(certificate)
    geometry = (
        "n",
        "side",
        "square_size",
        "representation",
        "scalar",
        "coordinates",
        "squares",
    )
    problems = [
        f"n={N}: author view changes the certificate's {key}"
        for key in geometry
        if view.get(key) != source[key]
    ]
    if (view.get("certificate") or {}).get("generated") != provenance:
        problems.append(f"n={N}: author view does not name the retained certificate and review")
    return problems


def current_entry() -> dict[str, Any]:
    index = driver.read_json(REPO / driver.LAYER_INDEX_PATH)
    return next(row for row in index["entries"] if row["n"] == N)


def atlas_view(entry: dict[str, Any], *, at: Path | None = None) -> dict[str, Any]:
    """Read an indexed view using the renderer's existing artifact contract."""
    layout = replace(atlas_views.LAYOUT, repo=REPO)
    if at is not None:
        entry = {**entry, "view": {**entry["view"], "path": layout.relative(at)}}
    return atlas_views.view_witness(entry, layout)


def restore_previous(view: Path, backup: Path, entry: dict[str, Any]) -> None:
    """Recover the view named by the old index after an interrupted author install."""
    atlas_view(entry, at=backup)
    original = backup.read_bytes()
    installed = view.read_bytes()
    if installed == original:
        return
    interrupted = load_yaml(gzip.decompress(installed).decode("utf-8"))["witness"]
    certificate = interrupted.get("certificate") or {}
    if (
        certificate.get("generator") != axis.EVAND_AUTHOR_GENERATOR
        or certificate.get("run") != RUN
        or source_problems(REPO, interrupted)
    ):
        raise ValueError("the n304 recovery copy would replace an unrelated drawing")
    with atomic_output_file(view) as temporary:
        temporary.write_bytes(original)


def original_receipt(measured: Mapping[str, Any], *, recovering: bool) -> dict[str, Any]:
    """Hold the saved receipt to the author, house and fresh admission measurements."""
    original = driver.read_json(REPO / RECEIPT)
    keys = ("source", "house", "side", "identity")
    if recovering:
        keys = (*keys, "prior_view", "comparison", "contacts", "decision")
    if (
        any(original.get(key) != measured[key] for key in keys)
        or (original.get("run") or {}).get("id") != RUN
        or not (original.get("half_angle_check") or {}).get("passed")
        or not (original.get("comparison") or {}).get("gains")
        or original["comparison"]["after"] != measured["comparison"]["after"]
    ):
        raise ValueError("the author view needs its original admission receipt")
    return original


def candidate(entry: Mapping[str, Any]) -> tuple[driver.Admitted, dict[str, Any]]:
    """Check the exact side and all three required routes, then apply selection."""
    certificate, report, provenance, raw = retained_source(REPO)
    reference = entry.get("reference") or entry
    source = reference["source"]
    house = load_yaml((REPO / source["witness"]).read_text(encoding="utf-8"))["witness"]
    frame = driver.source_frame(house)
    facts = driver.case_facts(N)
    bound = driver.verified_bound(facts)
    if frame.side != certificate.side or bound is None or bound.compare(certificate.side) != 0:
        raise ValueError("the author certificate must match the exact house and verified sides")

    view = evand.basis_witness(certificate)
    view["id"] = f"{source['id']}-regularized"
    first, _report = exact_verify(view, rational_backend="gmp")
    side, corners = axis.view_corners(view)
    second = independent.check_squares(corners, side, rational_backend="gmp")
    raw_side, raw_poses = area.parse_certificate(raw, N)
    half_angle = area.decide(raw_side, raw_poses)
    routes = {
        "repository_verifier": first["verification_passed"],
        "independent_checker": second["verification_passed"],
        "half_angle": half_angle.passed,
    }
    pairs = math.comb(N, 2)
    if (
        not all(routes.values())
        or first["pairs_tested"] != pairs
        or second["pairs_tested"] != pairs
        or raw_side != side
        or half_angle.pairs != pairs
    ):
        raise ValueError(
            "all three exact checkers must agree on the side and accept every pair"
        )
    view["claim"]["coordinate_provenance"] = "verified"
    view["claim"]["limitations"] = (
        "Evan Daniel's exact regularized certificate, independently verified at the "
        "record's exact side. This certificate establishes feasibility."
    )

    # Row 10 reads the author settings along with the measured identity and contacts.
    # Here `same` labels the exact side for the table. It does not claim a re-solve.
    ident, contacts, move, equal = driver._measure_view(  # noqa: SLF001 -- same admission measurements
        n=N, witness=house, frame=frame, document=view, named=(), of=OUTPUT
    )
    regressions = driver._regression_count(contacts)  # noqa: SLF001 -- shared row 7 input
    decision = driver.classify(
        driver.Measured(
            "same",
            produced=True,
            routes=routes,
            relation="same",
            side=side,
            bound=bound,
            pose_equals_witness=equal,
            one_to_one=ident["one_to_one"],
            unnamed_turns=tuple(ident.get("unnamed_turns") or ()),
            regressions=regressions,
            variant=report["policy"],
            level=report["level"],
            max_move=move,
            visible_change=driver.visible_change(ident, contacts),
            totals_fall=driver.totals_fall(contacts),
            determined_merge=any(
                change[0] == "determined-merge" for change in report["angle_changes"]
            ),
        )
    )
    if decision.row != axis.ADMITTING_ROW or decision.decision != "admit":
        raise ValueError(f"the author view did not pass row 10: {decision.reason}")

    regularization = {
        "n": N,
        "of_witness": source["id"],
        "provenance": driver.packing_credit(
            facts, (house.get("source") or {}).get("key"), "same"
        ),
        "by": axis.EVAND_AUTHOR_SOURCE_KEY,
        "method": METHOD,
        "side": "same",
        "identity": {
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
        },
    }
    admitted = driver.Admitted(
        n=N,
        generator=axis.EVAND_AUTHOR_GENERATOR,
        run={"id": RUN, "output": OUTPUT},
        source=source,
        side={
            "reported": frame.side_text,
            "view": evand.literal(side),
            "relation": "same",
            "view_minus_reported": "0.000e+00",
            "view_minus_verified_upper_bound": "0.000e+00",
        },
        view=view,
        provenance=provenance,
        routes=routes,
        decision={
            "row": decision.row,
            "decision": decision.decision,
            "reason": decision.reason,
        },
        measured={
            "identity_by": f"{driver.IDENTITY_BY}, in devtools.regularize_evand",
            "shades_by": f"{driver.SHADES_BY}, in devtools.regularize_evand",
            "contacts": {rule: contacts[rule] for rule in driver.RULE_NAMES},
            "symmetry": ident["symmetry"],
            "regressions": regressions,
            "level": report["level"],
            "groups": [report["groups_before"], report["groups_after"]],
        },
        regularization=regularization,
        house_after=contacts["house"]["after"],
    )
    current = driver.current_view(N)
    if current is None:
        raise ValueError("the atlas has no retained n304 drawing to compare")
    current_path, current_view = current
    before = select.measured(
        N, census.Drawing(N, "regularized-view", current_path, entry["generator"]), current_view
    )
    after = select.measured(
        N,
        census.Drawing(
            N, "regularized-view", CERTIFICATE.as_posix(), axis.EVAND_AUTHOR_GENERATOR
        ),
        view,
    )
    gains, losses = select.compare(after, before)
    if losses or (not gains and entry["generator"] != axis.EVAND_AUTHOR_GENERATOR):
        raise ValueError(f"the author view does not improve today's drawing: {losses}")
    receipt = {
        "n": N,
        "source": provenance,
        "house": source,
        "prior_view": entry["view"],
        "side": admitted.side,
        "author_settings": {
            key: report[key]
            for key in ("policy", "level", "orientation_g", "shape", "angle_changes")
        },
        "fresh_gmp_checks": {"repository_verifier": first, "independent_checker": second},
        "half_angle_check": {
            "method": "devtools.check_half_angle_area.decide",
            "source": CERTIFICATE.as_posix(),
            "side": evand.literal(raw_side),
            **asdict(half_angle),
        },
        "identity": regularization["identity"],
        "contacts": contacts,
        "decision": asdict(decision),
        "comparison": {"before": before, "after": after, "gains": gains, "losses": losses},
    }
    return admitted, receipt


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--update", action="store_true", help="publish the verified drawing and receipt"
    )
    args = parser.parse_args(argv)
    started, cpu = time.perf_counter(), time.process_time()
    entry = current_entry()
    view = REPO / entry["view"]["path"]
    backup = view.with_name(f".{view.name}.before-author-install")
    recovering = (
        args.update and backup.is_file() and entry["generator"] != axis.EVAND_AUTHOR_GENERATOR
    )
    if recovering:
        restore_previous(view, backup, entry)
    installed = atlas_view(entry) if args.update else None
    admitted, receipt = candidate(entry)
    if not args.update:
        print(json.dumps(receipt, indent=2, default=str))
        return 0
    if not receipt["comparison"]["gains"]:
        if installed is None or source_problems(REPO, installed):
            raise ValueError("the installed author drawing does not match its source")
        retained = original_receipt(receipt, recovering=False)
        if backup.is_file():
            atlas_view({**entry, "view": retained["prior_view"]}, at=backup)
            backup.unlink()
        print(f"n={N}: the original author drawing and admission receipt are already published")
        return 0
    generators = {
        axis.EVAND_AUTHOR_GENERATOR: {
            "tool": "packing/devtools/regularize_author_view.py",
            "generated_by": "python -m devtools.regularize_author_view --update",
            "method": METHOD,
            "credit": axis.EVAND_AUTHOR_CREDIT,
            "source_url": "https://github.com/evand/square-packing",
            "source_commit": SOURCE_COMMIT,
        }
    }
    run = {
        "id": RUN,
        "generator": axis.EVAND_AUTHOR_GENERATOR,
        "finished": DATE,
        "parameters": {
            "certificate": CERTIFICATE.as_posix(),
            "admission_receipt": RECEIPT.as_posix(),
            "verification_backends": ["gmp", "half-angle area"],
        },
        "counts": 1,
        "decisions": {"admit": 1},
        "cost": {
            "cpu_seconds": round(time.process_time() - cpu, 3),
            "wall_seconds": round(time.perf_counter() - started, 3),
            "workers": 1,
            "note": (
                "Measured import verification and admission checks. "
                "Author run cost was unreported."
            ),
        },
    }
    # The shared installer writes the view before the index. Keep the incumbent for
    # recovery until both writes succeed, and retain its measured comparison first.
    if not recovering:
        with atomic_output_file(backup) as temporary:
            temporary.write_bytes(view.read_bytes())
    if recovering and (REPO / RECEIPT).is_file():
        run = original_receipt(receipt, recovering=True)["run"]
    else:
        receipt["run"] = run
        driver.write_json(REPO / RECEIPT, receipt)
    published = driver.admit_views([admitted], REPO, generators=generators, runs=[run])
    if published["written"] != [N]:
        raise ValueError(f"the layer refused the author view: {published}")
    backup.unlink()
    print(f"n={N}: published the author certificate and admission receipt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
