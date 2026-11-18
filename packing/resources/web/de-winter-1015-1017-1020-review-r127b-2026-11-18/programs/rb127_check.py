"""Decide one certificate of s(127), every square, wall and pair (lane r127b-1118).

Usage, for a report's two files (form J, the centre file, and form C, its corner twin):

    python -I -B rb127_check.py pair LABEL PIN EXACT.json WITNESS.yaml ISSUE.json OUT.json

and for the house certificate, a single corner file, with the house witness on ``main``:

    python -I -B rb127_check.py house LABEL CANDIDATE.yaml HOUSE_WITNESS.yaml OUT.json

A pair is decided twice by the two methods, natively (method A on form J's rows,
method B on form C's corners) and crossed (A on the poses of form C's corners, B on the
corners of form J's rows), which also decides each file on its own by both methods.
The verdict is ``ACCEPT`` only when both files read strictly, they state the same count
and the same side, square ``k`` of form C is the square of row ``k`` of form J for every
``k``, both decisions accept, the two methods agree at every wall and pair in each file,
and the margins and clearances from the two files are identical exactly.

The receipt also records the facts the issue states, and the side against the packing's
extent and against the issue's prints. Nothing here uses floating point to decide; the
binary64 values printed beside exact fractions are descriptions.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rb127_axes as A  # noqa: E402
import rb127_decide as D  # noqa: E402
import rb127_fmt as F  # noqa: E402
import rb127_issue as I  # noqa: E402
import rb127_read as R  # noqa: E402
import rb127_twin as T  # noqa: E402

Q = tuple[int, int]


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fr(v: Q) -> Fraction:
    return Fraction(v[0], v[1])


def digest_list(values: list[Any]) -> str:
    return hashlib.sha256("\n".join(str(v) for v in values).encode()).hexdigest()


def tilts(rows: list[tuple[Q, Q, Q, Q]]) -> dict[str, Any]:
    upright = 0
    small = {"below 1e-9 degrees": 0, "1e-9 to 1e-3 degrees": 0, "1e-3 to 1 degrees": 0, "beyond 1 degree": 0}
    largest = 0.0
    dirs = set()
    for _, _, c, s in rows:
        cf, sf = fr(c), fr(s)
        if cf * sf == 0:
            upright += 1
            continue
        a, b = abs(cf), abs(sf)
        lo, hi = (a, b) if a < b else (b, a)
        deg = math.degrees(math.atan2(float(lo), float(hi)))
        largest = max(largest, deg)
        dirs.add((lo, hi))
        if deg < 1e-9:
            small["below 1e-9 degrees"] += 1
        elif deg < 1e-3:
            small["1e-9 to 1e-3 degrees"] += 1
        elif deg < 1:
            small["1e-3 to 1 degrees"] += 1
        else:
            small["beyond 1 degree"] += 1
    return {
        "exactly_upright": upright,
        "tilted": len(rows) - upright,
        "tilted_by_angle_description": small,
        "largest_turn_degrees_description": f"{largest:.6f}",
        "distinct_tilted_orientations": len(dirs),
    }


def close_pairs(rows: list[tuple[Q, Q, Q, Q]]) -> int:
    pts = [(fr(r[0]), fr(r[1])) for r in rows]
    n = len(pts)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            dx = pts[j][0] - pts[i][0]
            dy = pts[j][1] - pts[i][1]
            if dx * dx + dy * dy < 2:
                count += 1
    return count


def side_facts(rows: list[tuple[Q, Q, Q, Q]], side: Q) -> dict[str, Any]:
    ip = [A.to_ipose(*r) for r in rows]
    S = fr(side)
    xs_lo = min(A.centre(p)[0] - A.half_extent(p) for p in ip)
    xs_hi = max(A.centre(p)[0] + A.half_extent(p) for p in ip)
    ys_lo = min(A.centre(p)[1] - A.half_extent(p) for p in ip)
    ys_hi = max(A.centre(p)[1] + A.half_extent(p) for p in ip)
    width, height = xs_hi - xs_lo, ys_hi - ys_lo
    ext = max(width, height)
    places = F.terminating_places(S)
    return {
        "side_exact": F.exact(S),
        "side_as_written": f"{side[0]}/{side[1]}",
        "side_in_lowest_terms": math.gcd(side[0], side[1]) == 1,
        "side_terminates_at_places": places,
        "side_decimal_exact": F.floor_places(S, places) if places is not None else None,
        "side_floor_30": F.floor_places(S, 30),
        "side_ceil_12": F.ceil_places(S, 12),
        "side_ceil_16": F.ceil_places(S, 16),
        "side_nearest_16": F.nearest_places(S, 16),
        "extent_left_bottom": [F.exact(xs_lo), F.exact(ys_lo)],
        "extent_right_top": [F.exact(xs_hi), F.exact(ys_hi)],
        "width": F.exact(width),
        "height": F.exact(height),
        "side_less_width_sci": F.sci(S - width, 8),
        "side_less_height_sci": F.sci(S - height, 8),
        "side_less_extent": F.exact(S - ext),
        "side_less_extent_sci": F.sci(S - ext, 8),
        "side_equals_extent": S == ext,
        "side_at_least_extent": S >= ext,
    }


def _cmp_decisions(nat: dict[str, Any], cro: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    np_, cp = nat["pairs"], cro["pairs"]
    out["margins_identical_A_J_vs_A_C"] = all(
        a.get("margin_a") == b.get("margin_a") and "margin_a" in a for a, b in zip(np_, cp, strict=True)
    )
    out["B_identical_B_C_vs_B_J"] = all(
        a.get("class_b") == b.get("class_b") and a.get("area_b") == b.get("area_b") and "class_b" in a
        for a, b in zip(np_, cp, strict=True)
    )
    out["clearances_identical"] = all(
        a.get("clearances_a") == b.get("clearances_a") and "clearances_a" in a
        for a, b in zip(nat["walls"], cro["walls"], strict=True)
    )
    out["B_walls_identical"] = all(
        a.get("classes_b") == b.get("classes_b") and a.get("inside_b") == b.get("inside_b") and "classes_b" in a
        for a, b in zip(nat["walls"], cro["walls"], strict=True)
    )
    # Each file on its own: A on its poses against B on its corners.
    out["form_J_alone_pairs_agree"] = all(
        a.get("class_a") == b.get("class_b") and "class_a" in a for a, b in zip(np_, cp, strict=True)
    )
    out["form_C_alone_pairs_agree"] = all(
        b.get("class_a") == a.get("class_b") and "class_a" in b for a, b in zip(np_, cp, strict=True)
    )
    out["form_J_alone_walls_agree"] = all(
        a.get("classes_a") == b.get("classes_b") and "classes_a" in a
        for a, b in zip(nat["walls"], cro["walls"], strict=True)
    )
    out["form_C_alone_walls_agree"] = all(
        b.get("classes_a") == a.get("classes_b") and "classes_a" in b
        for a, b in zip(nat["walls"], cro["walls"], strict=True)
    )
    out["all"] = all(v for v in out.values())
    return out


def margins_digest(dec: dict[str, Any]) -> str:
    return digest_list([f"{r['pair'][0]},{r['pair'][1]}:{r.get('margin_a')}" for r in dec["pairs"]])


def clearances_digest(dec: dict[str, Any]) -> str:
    return digest_list([f"{r['square']}:{r.get('clearances_a')}" for r in dec["walls"]])


def counts(dec: dict[str, Any]) -> dict[str, Any]:
    touching = [list(r["pair"]) for r in dec["pairs"] if r.get("margin_a") == 0]
    wall_contacts = []
    for r in dec["walls"]:
        for w in range(4):
            if r["clearances_a"][w] == 0:
                wall_contacts.append([r["square"], ("left", "bottom", "right", "top")[w]])
    below = {}
    for t in (Fraction(1, 10**27), Fraction(1, 10**18), Fraction(1, 10**12), Fraction(1, 10**9), Fraction(1, 10**3)):
        below[F.sci(t, 1)] = sum(1 for r in dec["pairs"] if r.get("margin_a") is not None and r["margin_a"] < t)
    return {
        "touching_pairs": len(touching),
        "touching_pairs_list": touching,
        "wall_contacts": len(wall_contacts),
        "wall_contacts_list": wall_contacts,
        "pairs_with_margin_below": below,
    }


def claim_box(rows, corners, side: Q) -> dict[str, Any]:
    dec = D.decide(rows, corners, side, squares=list(range(len(rows))), pairs=[])
    return {"side": f"{side[0]}/{side[1]}", "verdict_walls_only": dec["verdict"], "problems": dec["problems"][:10]}


def dec_float(text: str) -> Fraction:
    whole, _, frac = text.partition(".")
    return Fraction(int(whole + frac), 10 ** len(frac))


def run_pair(label: str, pin: str, jpath: str, cpath: str, ipath: str) -> dict[str, Any]:
    t0 = time.process_time()
    jb, cb = Path(jpath).read_bytes(), Path(cpath).read_bytes()
    rec: dict[str, Any] = {
        "program": "rb127_check.py",
        "mode": "pair",
        "label": label,
        "pin": pin,
        "files": {"exact_json": {"path": jpath, "sha256": sha256(jb), "bytes": len(jb)},
                  "witness_yaml": {"path": cpath, "sha256": sha256(cb), "bytes": len(cb)}},
    }
    issue = I.read_issue(ipath)
    rec["issue"] = issue
    try:
        J = R.read_form_j(jb)
        C = R.read_form_c(cb)
    except R.ReadError as exc:
        rec["verdict"] = "REFUSE"
        rec["read_error"] = str(exc)
        return rec
    rec["reading"] = {
        "form_J": {"n": J["n"], "key_order": J["key_order"], "flags": J["flags"], "scalars": J["scalars"]},
        "form_C": {"n": C["n"], "id_style": C["id_style"], "witness_id": C["witness_id"], "schema": C["schema"],
                   "claim": C["claim"], "has_source": C["has_source"], "has_certificate": C["has_certificate"],
                   "flags": C["flags"], "scalars": C["scalars"]},
    }
    problems = []
    if not (J["n"] == C["n"] == len(J["rows"]) == len(C["corners"])):
        problems.append("counts differ")
    if fr(J["side"]) != fr(C["side"]):
        problems.append("the two files state different sides")
    rec["sides_equal_as_values"] = fr(J["side"]) == fr(C["side"])
    rec["sides_equal_as_written"] = J["side"] == C["side"]
    tw = T.twin(J["rows"], C["corners"])
    rec["twin"] = tw
    if not tw["holds"]:
        problems.append(f"twin fails at {len(tw['failures'])} squares")
    side = J["side"]
    nat = D.decide(J["rows"], C["corners"], side)
    cposes = [T.pose_of_corners(c) for c in C["corners"]]
    jcorners = [T.corners_pq(r) for r in J["rows"]]
    cro = D.decide(cposes, jcorners, side)
    rec["decision_native"] = D.summary(nat)
    rec["decision_crossed"] = D.summary(cro)
    agree = _cmp_decisions(nat, cro)
    rec["agreement"] = agree
    rec["margins_digest_native"] = margins_digest(nat)
    rec["margins_digest_crossed"] = margins_digest(cro)
    rec["clearances_digest_native"] = clearances_digest(nat)
    rec["clearances_digest_crossed"] = clearances_digest(cro)
    if nat["verdict"] != "ACCEPT":
        problems.append("native decision refuses")
    if cro["verdict"] != "ACCEPT":
        problems.append("crossed decision refuses")
    if not agree["all"]:
        problems.append("the decisions disagree somewhere")
    rec["counts"] = counts(nat)
    rec["side_facts"] = side_facts(J["rows"], side)
    rec["tilts"] = tilts(J["rows"])
    cp = close_pairs(J["rows"])
    S = fr(side)
    claims: dict[str, Any] = {"close_pairs_centres_below_sqrt2": cp,
                              "close_pairs_stated": issue["close_pairs"],
                              "close_pairs_as_stated": all(v == cp for v in issue["close_pairs"]) and bool(issue["close_pairs"]),
                              "commit_as_pinned": issue["commit"] == pin}
    ceil12 = F.ceil_places(S, 12)
    claims["side_ceil_12"] = ceil12
    if issue["title_side_print"] is not None:
        claims["title_print"] = issue["title_side_print"]
        claims["title_print_is_ceil_12"] = issue["title_side_print"] == ceil12
    if issue["claim_print_rounded_up"] is not None:
        claims["body_print"] = issue["claim_print_rounded_up"]
        claims["body_print_is_ceil_12"] = issue["claim_print_rounded_up"] == ceil12
        cbox = dec_float(issue["claim_print_rounded_up"])
        claims["body_print_at_least_side"] = cbox >= S
        claims["claim_box"] = claim_box(J["rows"], C["corners"], (cbox.numerator, cbox.denominator))
    if issue["claim_exact"] is not None:
        p, q = (int(v) for v in issue["claim_exact"].split("/"))
        claims["body_exact"] = issue["claim_exact"]
        claims["body_exact_equals_side"] = Fraction(p, q) == S
        claims["body_exact_as_written_in_files"] = (p, q) == side
        dec_print = rec["side_facts"]["side_decimal_exact"]
        claims["body_exact_decimal"] = issue["claim_exact_decimal"]
        claims["side_decimal_exact"] = dec_print
        claims["body_exact_decimal_is_exact"] = issue["claim_exact_decimal"] == dec_print
    if issue["title_side_print"] is not None and issue["claim_print_rounded_up"] is None:
        tbox = dec_float(issue["title_side_print"])
        claims["claim_box_title"] = claim_box(J["rows"], C["corners"], (tbox.numerator, tbox.denominator))
    if issue["band_squares"] is not None:
        claims["band_squares_stated"] = int(issue["band_squares"])
        claims["tilted_squares"] = rec["tilts"]["tilted"]
    if issue["kaggle_side"] is not None:
        kag = dec_float(issue["kaggle_side"])
        claims["kaggle_side"] = issue["kaggle_side"]
        claims["kaggle_less_side_sci"] = F.sci(kag - S, 6)
        claims["kaggle_difference_print"] = issue["kaggle_difference_print"]
        claims["kaggle_difference_sense"] = issue["kaggle_difference_sense"]
    rec["claims"] = claims
    rec["problems"] = problems
    rec["verdict"] = "ACCEPT" if not problems else "REFUSE"
    rec["cpu_seconds"] = round(time.process_time() - t0, 2)
    return rec


def run_house(label: str, cpath: str, hpath: str) -> dict[str, Any]:
    t0 = time.process_time()
    cb = Path(cpath).read_bytes()
    hb = Path(hpath).read_bytes()
    rec: dict[str, Any] = {
        "program": "rb127_check.py",
        "mode": "house",
        "label": label,
        "files": {"candidate_yaml": {"path": cpath, "sha256": sha256(cb), "bytes": len(cb)},
                  "house_witness_yaml": {"path": hpath, "sha256": sha256(hb), "bytes": len(hb)}},
    }
    try:
        C = R.read_form_c(cb)
    except R.ReadError as exc:
        rec["verdict"] = "REFUSE"
        rec["read_error"] = str(exc)
        return rec
    rec["reading"] = {"form_C": {"n": C["n"], "id_style": C["id_style"], "witness_id": C["witness_id"],
                                 "schema": C["schema"], "claim": C["claim"], "certificate": C["certificate_block"],
                                 "source": C["source_block"], "flags": C["flags"], "scalars": C["scalars"]}}
    side = C["side"]
    cposes = [T.pose_of_corners(c) for c in C["corners"]]
    dec = D.decide(cposes, C["corners"], side)
    rec["decision_form_C_alone"] = D.summary(dec)
    rec["margins_digest"] = margins_digest(dec)
    rec["counts"] = counts(dec)
    rec["side_facts"] = side_facts(cposes, side)
    rec["tilts"] = tilts(cposes)
    rec["close_pairs_centres_below_sqrt2"] = close_pairs(cposes)
    problems = [] if dec["verdict"] == "ACCEPT" else ["decision refuses"]
    # The house witness on main against this certificate.
    try:
        H = R.read_center_basis(hb)
        same_side = fr(H["side"]) == fr(side)
        same_centres = sum(
            1 for a, b in zip(H["rows"], cposes, strict=True) if fr(a[0]) == fr(b[0]) and fr(a[1]) == fr(b[1])
        )
        same_squares = 0
        for a, b in zip(H["rows"], cposes, strict=True):
            ca, sa, cb_, sb = fr(a[2]), fr(a[3]), fr(b[2]), fr(b[3])
            if fr(a[0]) == fr(b[0]) and fr(a[1]) == fr(b[1]) and (cb_, sb) in [(ca, sa), (-sa, ca), (-ca, -sa), (sa, -ca)]:
                same_squares += 1
        rec["house_witness"] = {"witness_id": H["witness_id"], "n": H["n"], "same_side_exactly": same_side,
                                "squares_with_same_centre": same_centres,
                                "squares_identical_in_order": same_squares}
    except R.ReadError as exc:
        rec["house_witness"] = {"read_error": str(exc)}
    rec["problems"] = problems
    rec["verdict"] = "ACCEPT" if not problems else "REFUSE"
    rec["cpu_seconds"] = round(time.process_time() - t0, 2)
    return rec


def _jsonable(x: Any) -> Any:
    if isinstance(x, Fraction):
        return F.exact(x)
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    return x


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[1] == "pair" and len(argv) == 8:
        rec = run_pair(argv[2], argv[3], argv[4], argv[5], argv[6])
        out = argv[7]
    elif len(argv) >= 2 and argv[1] == "house" and len(argv) == 6:
        rec = run_house(argv[2], argv[3], argv[4])
        out = argv[5]
    else:
        print(__doc__)
        return 2
    Path(out).write_text(json.dumps(_jsonable(rec), indent=1) + "\n", encoding="utf-8")
    print(f"{rec['label']}: {rec['verdict']}")
    return 0 if rec["verdict"] == "ACCEPT" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
