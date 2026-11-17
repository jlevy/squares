"""Decide de Winter's `.cert` certificates by two exact methods that share only the reader.

L96 review program. Usage:
  python -I -B l96_check.py OUT_DIR CERT...
For each certificate it writes OUT_DIR/check-nNNNN.json and prints one line. The verdict
is ACCEPT only when the reader accepts the file, both methods find every square a unit
square inside [0, side]^2 and no pair overlapping, their four clearances per square are
equal exactly, and their contact and overlap sets are equal.
"""

import hashlib
import json
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l96_clip as B  # noqa: E402
import l96_read as R  # noqa: E402
import l96_sat as A  # noqa: E402

PROGRAMS = ("l96_read.py", "l96_sat.py", "l96_clip.py", "l96_check.py")
WALLS = ("left", "bottom", "right", "top")


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def program_digests():
    return {p: sha256(os.path.join(HERE, p)) for p in PROGRAMS}


def frac_str(q):
    return f"{q.numerator}/{q.denominator}" if q.denominator != 1 else str(q.numerator)


def floor_dec(q, k):
    v = (q.numerator * 10**k) // q.denominator
    sign = "-" if v < 0 else ""
    v = abs(v)
    return f"{sign}{v // 10**k}.{v % 10**k:0{k}d}"


def ceil_dec(q, k):
    v = -((-q.numerator * 10**k) // q.denominator)
    sign = "-" if v < 0 else ""
    v = abs(v)
    return f"{sign}{v // 10**k}.{v % 10**k:0{k}d}"


def sci(q):
    return f"{float(q):.6e}"


def as_frac(x):
    return F(int(x.numerator), int(x.denominator))


def check_bytes(data):
    """Decide one certificate given as bytes. Returns (receipt dict, A result, B result)."""
    rec = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    try:
        cert = R.read_cert(data)
    except R.ReadError as exc:
        rec["reader"] = f"REFUSED: {exc}"
        rec["verdict"] = "REFUSE"
        return rec, None, None
    rec["reader"] = "accepted"
    rec["comments"] = cert["comments"]
    rec["n"] = cert["n"]
    rec["scalars"] = cert["scalars"]
    rec["noncanonical_scalars"] = cert["noncanonical_scalars"]
    side = F(*cert["side"])
    rec["side"] = {
        "exact": frac_str(side),
        "floor_20": floor_dec(side, 20),
        "ceil_10": ceil_dec(side, 10),
        "ceil_12": ceil_dec(side, 12),
    }
    tilted = sum(1 for _, _, t in cert["squares"] if t[0] != 0)
    rec["squares_tilted"] = tilted
    rec["squares_axis_aligned"] = cert["n"] - tilted
    ra = A.decide(cert["side"], cert["squares"])
    rb = B.decide(cert["side"], cert["squares"])
    problems = []
    if ra["bad_unit"] or rb["bad_unit"]:
        problems.append(f"not unit squares: A {ra['bad_unit'][:5]} B {rb['bad_unit'][:5]}")
    # Containment, both methods, and their exact agreement.
    outside_a, outside_b, contacts, mismatch = [], [], [], 0
    least_pos = None
    for k in range(1, cert["n"] + 1):
        ca, cb = ra["clearances"][k], rb["clearances"][k]
        for w in WALLS:
            va, vb = ca[w], as_frac(cb[w])
            if va != vb:
                mismatch += 1
            if va < 0:
                outside_a.append([k, w])
            if vb < 0:
                outside_b.append([k, w])
            if va == 0:
                contacts.append([k, w])
            elif va > 0 and (least_pos is None or va < least_pos[0]):
                least_pos = (va, k, w)
    if outside_a or outside_b:
        problems.append(f"outside: A {outside_a[:5]} B {outside_b[:5]}")
    if mismatch:
        problems.append(f"{mismatch} clearances differ between methods")
    # Pairs.
    con_a = sorted(k for k, (m, _) in ra["margins"].items() if m == 0)
    ovl_a = sorted(k for k, (m, _) in ra["margins"].items() if m < 0)
    con_b = sorted(k for k, c in rb["classes"].items() if c == "contact")
    ovl_b = sorted(k for k, c in rb["classes"].items() if c == "overlap")
    if ovl_a or ovl_b:
        problems.append(f"overlapping pairs: A {ovl_a[:5]} B {ovl_b[:5]}")
    if con_a != con_b or ovl_a != ovl_b:
        problems.append("methods disagree on contact or overlap sets")
    pos = sorted((m, k) for k, (m, _) in ra["margins"].items() if m > 0)
    rec["walls"] = {
        "contacts": contacts,
        "least_positive_clearance": None
        if least_pos is None
        else {"exact": frac_str(least_pos[0]), "approx": sci(least_pos[0]), "square": least_pos[1], "wall": least_pos[2]},
        "clearances_equal_between_methods": mismatch == 0,
    }
    far = []
    for k in range(1, cert["n"] + 1):
        for w in ("right", "top"):
            far.append(ra["clearances"][k][w])
    rec["least_far_wall_clearance"] = sci(min(far))
    rec["pairs"] = {
        "total": ra["pairs_total"],
        "A_decided_by_x_line": ra["pairs_decided_by_x_line"],
        "A_decided_by_y_line": ra["pairs_decided_by_y_line"],
        "A_decided_by_margin": ra["pairs_decided_by_margin"],
        "A_least_x_line_gap": None if ra["least_x_line_gap"] is None else sci(ra["least_x_line_gap"]),
        "A_least_y_line_gap": None if ra["least_y_line_gap"] is None else sci(ra["least_y_line_gap"]),
        "B_not_enumerated": rb["pairs_not_enumerated"],
        "B_decided_by_disc": rb["pairs_decided_by_disc"],
        "B_clipped": rb["pairs_clipped"],
        "contacts": [list(k) for k in con_a],
        "overlaps_A": [list(k) for k in ovl_a],
        "overlaps_B": [list(k) for k in ovl_b],
        "classes_equal": con_a == con_b and ovl_a == ovl_b,
        "least_positive_margin": None
        if not pos
        else {"exact": frac_str(pos[0][0]), "approx": sci(pos[0][0]), "pair": list(pos[0][1])},
        "smallest_ten_positive_margins": [[sci(m), list(k)] for m, k in pos[:10]],
        "positive_margins_below": {
            e: sum(1 for m, _ in pos if m < F(1, 10**int(e[3:]))) for e in ("1e-12", "1e-10", "1e-9", "1e-8", "1e-6")
        },
    }
    rec["problems"] = problems
    rec["verdict"] = "ACCEPT" if not problems else "REFUSE"
    return rec, ra, rb


def main():
    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    digests = program_digests()
    for path in sys.argv[2:]:
        with open(path, "rb") as fh:
            data = fh.read()
        rec, _, _ = check_bytes(data)
        rec = {"file": os.path.basename(path), "programs": digests, **rec}
        name = os.path.basename(path).replace(".cert", "")
        with open(os.path.join(out_dir, f"check-{name}.json"), "w") as fh:
            json.dump(rec, fh, indent=1)
            fh.write("\n")
        lp = rec.get("pairs", {}).get("least_positive_margin") or {}
        print(
            rec["file"],
            rec["verdict"],
            rec.get("n"),
            rec.get("side", {}).get("ceil_10"),
            "contacts(wall)=%d" % len(rec.get("walls", {}).get("contacts", [])),
            "contacts(pair)=%d" % len(rec.get("pairs", {}).get("contacts", [])),
            "least=%s %s" % (lp.get("approx"), lp.get("pair")),
            rec.get("problems"),
            flush=True,
        )


if __name__ == "__main__":
    main()
