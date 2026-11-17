"""Describe one count's certificate: tilts, near pairs, walls, digits. Decides nothing.

Lane c-review-1009-1117, stage 4 blind review of issue #1009. Written after the checker
and the controls plan were frozen and before the findings were; it is not in the frozen
checker list.

    python -I -B rv1009_describe.py CERT YAML ISSUE.json N OUT.json

It reads the two files through the frozen readers and measures, with the frozen method A
and closed forms: how the squares are tilted; which pairs are near and how their margins
are distributed; whether the near pairs share one contact factor (as a uniformly dilated
contact packing would); how many pairs lie within several centre distances, beside the
issue's "close pairs"; which squares are near each wall; and how long the scalars are.
"""

from __future__ import annotations

import json
import math
import sys
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rv1009_axes as axes  # noqa: E402
import rv1009_geom as geom  # noqa: E402
import rv1009_issue as issue  # noqa: E402
import rv1009_reader as reader  # noqa: E402

F = Fraction
NEAR = F(1, 10**9)
WALLS = ("left", "bottom", "right", "top")


def sci(value: Fraction, digits: int = 9) -> str:
    return f"{float(value):.{digits - 1}e}"


def exact(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)


def angle_degrees(t: Fraction) -> float:
    """The square's tilt in (-45, 45] degrees: its edge angle 2*atan(t) modulo 90."""
    angle = math.degrees(2.0 * math.atan(float(t)))
    angle = (angle + 45.0) % 90.0 - 45.0
    return angle


def spread(values: list[Fraction]) -> dict:
    if not values:
        return {"count": 0}
    ordered = sorted(values)
    return {
        "count": len(ordered),
        "distinct": len(set(ordered)),
        "least": sci(ordered[0]),
        "median": sci(ordered[len(ordered) // 2]),
        "greatest": sci(ordered[-1]),
    }


def main(argv: list[str]) -> int:
    cert_path, yaml_path, issue_path, n_text, out_path = argv[1:6]
    n = int(n_text)
    started = time.process_time()
    cert = reader.read_cert(Path(cert_path).read_bytes())
    wit = reader.read_witness(Path(yaml_path).read_bytes())
    stated = issue.read_issue(issue_path)
    if cert["n"] != n:
        msg = "the certificate is not of the count named"
        raise SystemExit(msg)
    side = F(*cert["side"])
    rows = [tuple(F(*v) for v in row) for row in cert["poses"]]
    poses = [axes.pose_from_xyt(*row) for row in cert["poses"]]

    # tilts
    tangents = Counter(t for _x, _y, t in rows)
    angles = [angle_degrees(t) for _x, _y, t in rows]
    upright = sum(1 for _x, _y, t in rows if t in (0, 1, -1))
    tiny = sum(1 for (_x, _y, t), a in zip(rows, angles, strict=True) if t not in (0, 1, -1) and abs(a) < 1e-9)
    small = sum(1 for a in angles if 1e-9 <= abs(a) < 1.0)
    large = sum(1 for a in angles if abs(a) >= 1.0)
    tilts = {
        "exactly_upright": upright,
        "tangent_zero": sum(1 for _x, _y, t in rows if t == 0),
        "turned_less_than_1e-9_degrees": tiny,
        "turned_1e-9_to_1_degree": small,
        "turned_beyond_1_degree": large,
        "largest_turn_degrees": round(max(abs(a) for a in angles), 4),
        "distinct_tangents": len(tangents),
        "negative_tangents": sum(1 for _x, _y, t in rows if t < 0),
        "commonest_tangents": [
            {
                "degrees": round(angle_degrees(t), 6),
                "count": count,
                "digits": [len(str(abs(t.numerator))), len(str(t.denominator))],
            }
            for t, count in tangents.most_common(8)
        ],
        "longest_tangent_digits": max(
            max(len(str(abs(t.numerator))), len(str(t.denominator))) for _x, _y, t in rows
        ),
    }

    # pairs
    near = []
    by_kind = Counter()
    factors = []
    dist_counts = Counter()
    bounds = {
        "centre_distance_below_sqrt2": F(2),
        "centre_distance_below_1.5": F(9, 4),
        "centre_distance_below_2": F(4),
    }
    margin_counts = Counter()
    for i in range(n):
        xi, yi, ti = rows[i]
        for j in range(i + 1, n):
            xj, yj, tj = rows[j]
            d2 = (xj - xi) ** 2 + (yj - yi) ** 2
            for name, bound in bounds.items():
                if d2 < bound:
                    dist_counts[name] += 1
            if d2 <= 2:
                dist_counts["centre_distance_at_most_sqrt2"] += 1
            m = axes.pair_margin(poses[i], poses[j])
            for name, bound in (("margin_below_1e-6", F(1, 10**6)), ("margin_below_1e-3", F(1, 10**3)), ("margin_below_1e-2", F(1, 100)), ("margin_below_1e-1", F(1, 10))):
                if m < bound:
                    margin_counts[name] += 1
            if m < NEAR:
                near.append((m, i + 1, j + 1))
                if ti in (0, 1, -1) and tj in (0, 1, -1):
                    by_kind["both upright"] += 1
                elif ti == tj:
                    by_kind["equal tangents"] += 1
                elif ti in (0, 1, -1) or tj in (0, 1, -1):
                    by_kind["one upright"] += 1
                else:
                    by_kind["two tilts"] += 1
                factors.append(geom.contact_scale_pair(rows[i], rows[j]))
    near.sort()
    values = Counter(m for m, _i, _j in near)
    one_less = [1 - g for g in factors]
    pairs = {
        "near_pairs_below_1e-9": len(near),
        "near_pairs_by_kind": dict(by_kind),
        "near_margins": spread([m for m, _i, _j in near]),
        "commonest_near_margins": [
            {"value": exact(v), "sci": sci(v, 12), "count": c} for v, c in values.most_common(6)
        ],
        "near_pairs_one_less_contact_factor": spread(one_less),
        "commonest_one_less_contact_factor": [
            {"sci": sci(v, 12), "count": c} for v, c in Counter(one_less).most_common(6)
        ],
        "least_five": [{"pair": [i, j], "margin": sci(m, 12)} for m, i, j in near[:5]],
        "greatest_five_near": [{"pair": [i, j], "margin": sci(m, 12)} for m, i, j in near[-5:]],
        "pairs_within": dict(dist_counts),
        "pairs_by_margin": dict(margin_counts),
        "issue_close_pairs": stated["files"][n]["close_pairs"],
    }

    # walls
    clear = [axes.wall_clearances(p, cert["side"]) for p in poses]
    walls = {}
    for w in range(4):
        close = [(clear[k][w], k + 1) for k in range(n) if clear[k][w] < NEAR]
        close.sort()
        vals = Counter(c for c, _k in close)
        walls[WALLS[w]] = {
            "squares_within_1e-9": len(close),
            "of_them_upright": sum(1 for _c, k in close if rows[k - 1][2] in (0, 1, -1)),
            "clearances": [{"value": exact(v), "sci": sci(v, 12), "count": c} for v, c in sorted(vals.items())[:6]],
            "greatest_within": sci(close[-1][0], 12) if close else None,
        }
    least = [min(clear[k][w] for k in range(n)) for w in range(4)]
    width = side - least[0] - least[2]
    height = side - least[1] - least[3]
    extent = {
        "width": exact(width),
        "height": exact(height),
        "side_less_width": exact(side - width),
        "side_less_width_sci": sci(side - width, 12),
        "side_less_height": exact(side - height),
        "side_less_height_sci": sci(side - height, 12),
        "width_less_height_sci": sci(width - height, 12),
    }

    # digits
    def digits(pairs_: list[tuple[int, int]]) -> dict:
        return {
            "longest_numerator": max(len(str(abs(p))) for p, _q in pairs_),
            "longest_denominator": max(len(str(q)) for _p, q in pairs_),
            "distinct_denominators": len({q for _p, q in pairs_}),
        }

    xs = [row[0] for row in cert["poses"]] + [row[1] for row in cert["poses"]]
    ts = [row[2] for row in cert["poses"]]
    cs = [v for quad in wit["squares"] for point in quad for v in point]
    lcm_xy = 1
    for _p, q in xs:
        lcm_xy = lcm_xy * q // math.gcd(lcm_xy, q)
    scalars = {
        "form_p_centres": digits(xs),
        "form_p_centres_common_denominator_digits": len(str(lcm_xy)),
        "form_p_tangents": digits(ts),
        "form_c_corners": digits(cs),
        "side_denominator": str(cert["side"][1]),
    }

    receipt = {
        "program": "rv1009_describe.py",
        "lane": "c-review-1009-1117",
        "n": n,
        "decides": "nothing",
        "tilts": tilts,
        "pairs": pairs,
        "walls": walls,
        "extent": extent,
        "scalars": scalars,
        "cpu_seconds": round(time.process_time() - started, 1),
    }
    Path(out_path).write_text(json.dumps(receipt, indent=1) + "\n", encoding="ascii")
    sys.stdout.write(
        f"n={n} upright={upright} near={len(near)} within_sqrt2={dist_counts['centre_distance_below_sqrt2']} "
        f"issue_close={stated['files'][n]['close_pairs']} cpu={receipt['cpu_seconds']}s\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
