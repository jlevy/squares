"""Lane r1052's check of a two-form certificate: form J (poses) and form C (corners).

Usage: r1052_check.py J_FILE C_FILE J_BLOB C_BLOB N CLAIM OUT_JSON

J_BLOB and C_BLOB are the git blob ids the source tree lists (``-`` to skip that test);
N the count the claim is about; CLAIM the claimed side as printed. The verdict is ACCEPT
only when: each file is the blob the tree lists; both files are read; each holds N
squares and the same side; square k of form C is square k of form J (its four corners
are c +- u/2 +- v/2, listed as a cyclic rotation of them in either sense); each file is
decided ACCEPT by both methods, every square, wall and pair, with the two methods in
agreement everywhere; the two files' decisions are equal, margin for margin and clearance
for clearance; and the claimed side is at least the file's side, with both methods
accepting the same squares in the box of the claimed side. No distance filter and no
tolerance is applied anywhere.
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import r1052_decide as decide_mod  # noqa: E402
import r1052_geom as geom  # noqa: E402
import r1052_reader as reader  # noqa: E402

THRESHOLDS = (60, 50, 40, 30, 20, 15, 12, 9, 6, 3, 2, 1)


def sci(value: Fraction, digits: int = 6) -> str:
    """A decimal print of an exact value for reading; decides nothing."""
    if value == 0:
        return "0"
    sign = "-" if value < 0 else ""
    v = abs(value)
    e = len(str(v.numerator)) - len(str(v.denominator))
    while Fraction(10) ** e > v:
        e -= 1
    while Fraction(10) ** (e + 1) <= v:
        e += 1
    mant = v / Fraction(10) ** e
    scaled = (mant * 10**digits).__floor__()
    s = str(scaled)
    return f"{sign}{s[0]}.{s[1:]}e{e:+d}"


def decimal(value: Fraction, places: int) -> str:
    """The first ``places`` decimals of a value, truncated toward zero; decides nothing."""
    sign = "-" if value < 0 else ""
    v = abs(value)
    whole = v.numerator // v.denominator
    frac = (v - whole) * 10**places
    return f"{sign}{whole}.{str(frac.__floor__()).zfill(places)}"


def sqrt_print(value: Fraction, digits: int = 6) -> str:
    """sqrt of a non-negative exact value, printed to ``digits`` figures (rounded down)."""
    if value == 0:
        return "0"
    scale = 10 ** (2 * 80)
    root = isqrt((value * scale).__floor__())
    return sci(Fraction(root, 10**80), digits)


def ratstr(value: Fraction) -> str:
    return str(value)


def ceiling_at(value: Fraction, places: int) -> Fraction:
    return Fraction(-((-value * 10**places).__floor__()), 10**places)


def floor_at(value: Fraction, places: int) -> Fraction:
    return Fraction((value * 10**places).__floor__(), 10**places)


def twin(
    poses: list[tuple[Fraction, Fraction, Fraction, Fraction]], corners: list[list[tuple[Fraction, Fraction]]]
) -> list[int]:
    """The squares (1-based) whose form C corners are not form J's, cyclically either way."""
    bad = []
    for k, (pose, listed) in enumerate(zip(poses, corners, strict=True)):
        mine = geom.corners(pose)
        options = []
        for seq in (mine, mine[::-1]):
            for r in range(4):
                options.append(seq[r:] + seq[:r])
        if listed not in options:
            bad.append(k + 1)
    return bad


def summarize(result: dict[str, Any], side: Fraction) -> dict[str, Any]:
    pairs = result["pairs"]
    out: dict[str, Any] = {"verdict": result["verdict"], "problems": result["problems"][:50]}
    out["problem_count"] = len(result["problems"])
    out["disagreements"] = result["disagreements"][:50]
    out["disagreement_count"] = len(result["disagreements"])
    classes: dict[str, int] = {}
    for _, cls, _, _ in pairs.values():
        classes[cls] = classes.get(cls, 0) + 1
    out["pairs"] = len(pairs)
    out["pair_classes"] = classes
    ordered = sorted(pairs.items(), key=lambda kv: kv[1][0])
    out["least_margins"] = [
        {"pair": [i + 1, j + 1], "margin": ratstr(m), "margin_sci": sci(m), "class": cls}
        for (i, j), (m, cls, _, _) in ordered[:25]
    ]
    out["margins_below"] = {
        f"1e-{t}": sum(1 for (m, _, _, _) in pairs.values() if m < Fraction(1, 10**t)) for t in THRESHOLDS
    }
    out["contacts"] = [[i + 1, j + 1] for (i, j), (_, cls, _, _) in ordered if cls == "contact"]
    gaps = [(g, key) for key, (_, cls, g, _) in pairs.items() if cls == "apart" and g is not None]
    if gaps:
        g2, key = min(gaps)
        out["least_euclidean_gap"] = {
            "pair": [key[0] + 1, key[1] + 1],
            "gap_squared": ratstr(g2),
            "gap_sci": sqrt_print(g2),
            "margin_of_that_pair": sci(pairs[key][0]),
        }
        out["least_euclidean_gaps"] = [
            {"pair": [k[0] + 1, k[1] + 1], "gap_sci": sqrt_print(g), "margin_sci": sci(pairs[k][0])}
            for g, k in sorted(gaps)[:12]
        ]
    walls = result["walls"]
    names = decide_mod.WALLS
    contacts: dict[str, list[int]] = {w: [] for w in names}
    least: dict[str, Any] = {}
    crossing: dict[str, list[int]] = {w: [] for w in names}
    for k, row in enumerate(walls):
        if row is None:
            continue
        for w, name in enumerate(names):
            c = row["clearances"][w]
            if c == 0:
                contacts[name].append(k + 1)
            elif c < 0:
                crossing[name].append(k + 1)
            elif name not in least or c < least[name][0]:
                least[name] = (c, k + 1)
    out["wall_contacts"] = contacts
    out["wall_crossings"] = crossing
    out["least_positive_clearance"] = {
        name: {"square": sq, "clearance": ratstr(c), "clearance_sci": sci(c)} for name, (c, sq) in least.items()
    }
    rows = [row for row in walls if row is not None]
    if rows:
        lo = [min(row["clearances"][w] for row in rows) for w in range(4)]
        out["extent"] = {
            "min_left": ratstr(lo[0]),
            "min_bottom": ratstr(lo[1]),
            "min_right": ratstr(lo[2]),
            "min_top": ratstr(lo[3]),
            "width": decimal(side - lo[0] - lo[2], 40),
            "height": decimal(side - lo[1] - lo[3], 40),
            "least_right_or_top": ratstr(min(lo[2], lo[3])),
            "least_right_or_top_sci": sci(min(lo[2], lo[3])),
        }
        out["inside_area_all_one"] = all(row["inside_area"] == 1 for row in rows)
    out["counterclockwise"] = sum(1 for s in result["sense"] if s == 1)
    out["clockwise"] = sum(1 for s in result["sense"] if s == -1)
    return out


def cross_equal(one: dict[str, Any], two: dict[str, Any]) -> list[str]:
    diffs = []
    if set(one["pairs"]) != set(two["pairs"]):
        return ["different pair sets"]
    for key, row in one["pairs"].items():
        other = two["pairs"][key]
        if row[0] != other[0] or row[1] != other[1]:
            diffs.append(f"pair {key[0] + 1},{key[1] + 1}: margins differ")
    for k, (a, b) in enumerate(zip(one["walls"], two["walls"], strict=True)):
        if (a is None) != (b is None) or (a is not None and b is not None and a["clearances"] != b["clearances"]):
            diffs.append(f"square {k + 1}: clearances differ")
    return diffs


def main(argv: list[str]) -> int:
    j_path, c_path, j_blob, c_blob, n_text, claim_text, out_path = argv[1:8]
    t0 = time.process_time()
    n = int(n_text)
    claim = Fraction(claim_text)
    receipt: dict[str, Any] = {"program": "r1052_check.py", "claim": claim_text, "n": n}
    problems: list[str] = []
    files: dict[str, Any] = {}
    read: dict[str, Any] = {}
    for label, path, blob, fn in (
        ("J", j_path, j_blob, reader.read_form_j),
        ("C", c_path, c_blob, reader.read_form_c),
    ):
        data = Path(path).read_bytes()
        info = {
            "path_name": Path(path).name,
            "bytes": len(data),
            "sha256": reader.sha256(data),
            "git_blob": reader.git_blob_id(data),
            "expected_blob": blob,
        }
        if blob != "-" and info["git_blob"] != blob:
            problems.append(f"form {label}: git blob {info['git_blob']} is not {blob}")
        try:
            got = fn(data)
            read[label] = got
            info["read"] = "read"
            for key in ("n", "format", "witness_id", "origin", "angle_unit", "envelope_keys", "witness_keys",
                        "claim_keys", "scalar_forms", "ascii", "final_newline", "yaml_loader"):
                if key in got:
                    info[key] = got[key]
            info["side"] = ratstr(got["side"])
            info["noncanonical_count"] = len(got["noncanonical"])
            info["noncanonical_first"] = got["noncanonical"][:10]
            if "ids" in got:
                info["ids_first_last"] = [got["ids"][0], got["ids"][-1]] if got["ids"] else []
                info["ids_in_order"] = got["ids"] == [f"square-{k + 1}" for k in range(len(got["ids"]))]
            if got["n"] != n:
                problems.append(f"form {label}: {got['n']} squares, the claim is about {n}")
        except reader.Refused as exc:
            info["read"] = f"refused: {exc}"
            problems.append(f"form {label}: refused by the reader: {exc}")
        files[label] = info
    receipt["files"] = files
    decisions: dict[str, Any] = {}
    if "J" in read and "C" in read:
        jj, cc = read["J"], read["C"]
        if jj["side"] != cc["side"]:
            problems.append("the two files state different sides")
        if jj["n"] == cc["n"]:
            bad = twin(jj["poses"], cc["corners"])
            receipt["twin"] = {"squares_differing": bad, "holds": not bad}
            if bad:
                problems.append(f"twin: {len(bad)} squares of form C are not form J's")
        else:
            problems.append("the two files hold different counts")
    side = read["J"]["side"] if "J" in read else (read["C"]["side"] if "C" in read else None)
    for label in ("J", "C"):
        if label not in read:
            continue
        got = read[label]
        if label == "J":
            res = decide_mod.decide(got["side"], poses=got["poses"])
        else:
            res = decide_mod.decide(got["side"], corners=got["corners"])
        decisions[label] = res
        receipt[f"decision_{label}"] = summarize(res, got["side"])
        if res["verdict"] != "ACCEPT":
            problems.append(f"form {label}: refused by the decision ({len(res['problems'])} problems, "
                            f"{len(res['disagreements'])} disagreements)")
        if label == "J":
            axis = sum(1 for (_, _, a, b) in got["poses"] if a == 0 or b == 0)
            receipt["axis_aligned_J"] = axis
            receipt["turned_J"] = len(got["poses"]) - axis
    if "J" in decisions and "C" in decisions:
        diffs = cross_equal(decisions["J"], decisions["C"])
        receipt["files_decide_alike"] = {"holds": not diffs, "differences": diffs[:20], "count": len(diffs)}
        if diffs:
            problems.append(f"the two files' decisions differ in {len(diffs)} places")
    if side is not None:
        cl: dict[str, Any] = {
            "side": ratstr(side),
            "side_decimal_70": decimal(side, 70),
            "side_numerator_digits": len(str(side.numerator)),
            "side_denominator_digits": len(str(side.denominator)),
            "claim": claim_text,
            "claim_minus_side": ratstr(claim - side),
            "claim_minus_side_sci": sci(claim - side),
            "ceiling_12": decimal(ceiling_at(side, 12), 12),
            "floor_12": decimal(floor_at(side, 12), 12),
            "claim_is_ceiling_12": claim == ceiling_at(side, 12),
            "side_minus_floor_12_sci": sci(side - floor_at(side, 12)),
        }
        if claim < side:
            problems.append("the claimed side is below the certificate's side")
        boxes = {}
        for label in ("J", "C"):
            if label not in read:
                continue
            got = read[label]
            if label == "J":
                res = decide_mod.decide(claim, poses=got["poses"], distance=False)
            else:
                res = decide_mod.decide(claim, corners=got["corners"], distance=False)
            boxes[label] = {"verdict": res["verdict"], "problems": res["problems"][:10],
                            "disagreements": res["disagreements"][:10]}
            if res["verdict"] != "ACCEPT":
                problems.append(f"form {label}: refused in the box of the claimed side")
        cl["claim_box"] = boxes
        receipt["claim_arithmetic"] = cl
    receipt["problems"] = problems
    receipt["verdict"] = "ACCEPT" if not problems else "REFUSE"
    receipt["cpu_seconds"] = round(time.process_time() - t0, 1)
    receipt["python"] = sys.version.split()[0]
    Path(out_path).write_text(json.dumps(receipt, indent=1) + "\n")
    print(f"{receipt['verdict']} {n} squares, side {decimal(side, 30) if side is not None else '?'}, "
          f"{len(problems)} problems, {receipt['cpu_seconds']} CPU s")
    return 0 if receipt["verdict"] == "ACCEPT" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
