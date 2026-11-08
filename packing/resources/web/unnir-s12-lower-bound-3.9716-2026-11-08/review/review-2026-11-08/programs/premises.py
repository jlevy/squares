"""Independent premise check for a weighted-point s(n) lower-bound certificate.

Written for the L58 review of jlevy/squares issue #924 without reading either
producer checker (Daniel's Rust `verify`, Ryu's C++ `indep_scan`) or any tool of
the jlevy/squares repository.  It reads only the certificate text.

Format, as the producer's README and the file itself describe it:

    line 1   SIDE_NUM SIDE_DEN      container side = SIDE_NUM / SIDE_DEN
    line 2   D                      coordinate denominator
    line 3   W                      weight denominator
    line 4   M                      number of points
    M lines  X Y WT                 point (X/D, Y/D) with weight WT/W

Everything is exact integer / Fraction arithmetic.  Prints a JSON receipt.

Usage:  python -I premises.py CERT N_SQUARES [EXPECTED_SHA256]
"""

import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction


def die(msg):
    print(json.dumps({"ok": False, "error": msg}))
    sys.exit(2)


def parse_strict(raw: bytes):
    """Line-structured parse; refuses anything but the exact layout."""
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError:
        die("non-ASCII byte in certificate")
    if "\r" in text:
        die("carriage return in certificate")
    if not text.endswith("\n"):
        die("certificate does not end in a newline")
    lines = text[:-1].split("\n")

    def ints(line_no, expected):
        parts = lines[line_no].split(" ")
        if len(parts) != expected or any(
            not p or not (p.isdigit() or (p[0] == "-" and p[1:].isdigit()))
            for p in parts
        ):
            die(f"line {line_no + 1} is not {expected} space-separated integers: {lines[line_no]!r}")
        return [int(p) for p in parts]

    if len(lines) < 4:
        die("short header")
    side_num, side_den = ints(0, 2)
    (d,) = ints(1, 1)
    (w,) = ints(2, 1)
    (m,) = ints(3, 1)
    if len(lines) != 4 + m:
        die(f"declared {m} points but found {len(lines) - 4} point lines")
    pts = [tuple(ints(4 + i, 3)) for i in range(m)]
    return side_num, side_den, d, w, m, pts


def parse_tokens(raw: bytes):
    """Whitespace-token parse, the reading a lenient checker would make."""
    toks = [int(t) for t in raw.split()]
    side_num, side_den, d, w, m = toks[:5]
    body = toks[5:]
    return side_num, side_den, d, w, m, [tuple(body[3 * i : 3 * i + 3]) for i in range(len(body) // 3)], len(body)


def main():
    if len(sys.argv) not in (3, 4):
        print(__doc__)
        sys.exit(2)
    path, n = sys.argv[1], int(sys.argv[2])
    raw = open(path, "rb").read()
    digest = hashlib.sha256(raw).hexdigest()
    out = {"certificate": path, "sha256": digest, "bytes": len(raw)}
    if len(sys.argv) == 4:
        out["sha256_matches_expected"] = digest == sys.argv[3]

    side_num, side_den, d, w, m, pts = parse_strict(raw)
    t = parse_tokens(raw)
    out["token_parse_agrees"] = t[:5] == (side_num, side_den, d, w, m) and t[5] == pts and t[6] == 3 * m

    side = Fraction(side_num, side_den)
    out["side"] = f"{side.numerator}/{side.denominator}"
    out["side_decimal"] = f"{side_num / side_den:.10f}"
    out["side_header"] = [side_num, side_den]
    out["D"] = d
    out["W"] = w
    out["declared_points"] = m
    out["parsed_points"] = len(pts)

    checks = {}
    checks["D_positive"] = d > 0
    checks["W_positive"] = w > 0
    checks["side_den_positive"] = side_den > 0
    checks["side_equals_9929_over_2500"] = side == Fraction(9929, 2500)
    checks["side_header_denominator_equals_D"] = side_den == d
    # side in units of 1/D; integer exactly when side * D is an integer
    sd = side * d
    checks["side_times_D_integer"] = sd.denominator == 1
    S = int(sd) if sd.denominator == 1 else None
    out["side_in_D_units"] = str(sd)

    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ws = [p[2] for p in pts]
    checks["all_weights_positive"] = all(v > 0 for v in ws)
    checks["all_points_in_closed_container"] = all(
        0 <= Fraction(x, d) <= side and 0 <= Fraction(y, d) <= side for x, y, _ in pts
    )
    checks["no_point_on_container_boundary"] = all(
        0 < Fraction(x, d) < side and 0 < Fraction(y, d) < side for x, y, _ in pts
    )
    loc = Counter((x, y) for x, y, _ in pts)
    checks["points_distinct"] = len(loc) == len(pts)

    total = sum(ws)
    out["total_weight_numerator"] = total
    out["total_weight"] = f"{total}/{w}"
    out["total_weight_decimal"] = f"{total / w:.15f}"
    margin = n * w - total
    out["margin_below_n_numerator"] = margin
    out["margin_below_n"] = f"{margin}/{w}"
    checks["total_strictly_below_n"] = Fraction(total, w) < n

    # D4 symmetry of the weighted multiset about the container centre
    if S is not None:
        ms = Counter(pts)
        maps = {
            "id": lambda x, y: (x, y),
            "rot90": lambda x, y: (S - y, x),
            "rot180": lambda x, y: (S - x, S - y),
            "rot270": lambda x, y: (y, S - x),
            "mirror_x": lambda x, y: (S - x, y),
            "mirror_y": lambda x, y: (x, S - y),
            "diag": lambda x, y: (y, x),
            "antidiag": lambda x, y: (S - y, S - x),
        }
        sym = {}
        for name, f in maps.items():
            img = Counter()
            for (x, y, wt), c in ms.items():
                img[(*f(x, y), wt)] += c
            sym[name] = img == ms
        out["D4_maps_preserving"] = sym
        checks["D4_symmetric"] = all(sym.values())
        # orbit census
        seen = set()
        orbit_sizes = Counter()
        for x, y, wt in pts:
            if (x, y) in seen:
                continue
            orb = {f(x, y) for f in maps.values()}
            seen |= orb
            orbit_sizes[len(orb)] += 1
        out["orbit_size_census"] = dict(sorted(orbit_sizes.items()))
        out["centre_point_present"] = (2 * 0 + S) % 2 == 0 and (S // 2, S // 2) in loc

    out["weight_census"] = {
        "min": min(ws),
        "max": max(ws),
        "distinct": len(set(ws)),
        "points_with_weight_1": sum(1 for v in ws if v == 1),
        "weight_of_weight_le_10_points": sum(v for v in ws if v <= 10),
    }
    out["coordinate_range_D_units"] = [min(xs + ys), max(xs + ys)]
    out["checks"] = checks
    out["ok"] = all(checks[k] for k in (
        "D_positive", "W_positive", "side_den_positive", "all_weights_positive",
        "total_strictly_below_n", "D4_symmetric", "points_distinct",
        "all_points_in_closed_container", "side_equals_9929_over_2500",
    ) if k in checks) and out["token_parse_agrees"]
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
