"""Decide a house witness at 179 and #954's certificate with the frozen checker.

Run twice: for T-174's witness on main at c8448724e, and for T-291's (#954's packing,
re-expressed center-basis) on main at b5b12c206, after PR #956 merged.

Lane L108, blind stage 4 review of jlevy/squares#959. Written after the findings were
frozen. The house witness is center-basis rational; its corners are written exactly as
c - u/2 - w/2, c + u/2 - w/2, c + u/2 + w/2, c - u/2 + w/2 with u the basis and w = u
turned a quarter counterclockwise, and decided by the frozen l108_check.decide. #954's
certificate is read by the frozen reader with its twin.

Usage: python -I -B l108_house.py LABEL HOUSE.yaml CERT954.yaml CERT954.json OUT.json
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import l108_check as check  # noqa: E402
import l108_reader as reader  # noqa: E402

KEEP = ("verdict", "not_unit_a", "not_unit_b", "counterclockwise", "clockwise", "walls_decided", "wall_disagreements", "walls_outside", "wall_contacts", "least_positive_wall_clearance", "positive_wall_clearances_below", "pairs_decided", "pair_disagreements", "overlapping_pair_count", "touching_pairs", "clipped_area_sum", "least_margin", "pairs_below")


def house_certificate(path: Path) -> reader.Certificate:
    w = yaml.safe_load(path.read_text(encoding="utf-8"))["witness"]
    assert w["representation"] == "center-basis" and w["scalar"]["kind"] == "rational"
    half = Fraction(1, 2)
    squares = []
    for k, sq in enumerate(w["squares"], start=1):
        assert sq["id"] == k
        cx, cy = (Fraction(str(v)) for v in sq["center"])
        c, s = (Fraction(str(v)) for v in sq["basis"])
        ux, uy, wx, wy = c * half, s * half, -s * half, c * half
        pts = [(cx - ux - wx, cy - uy - wy), (cx + ux - wx, cy + uy - wy), (cx + ux + wx, cy + uy + wy), (cx - ux + wx, cy - uy + wy)]
        squares.append(tuple(((x.numerator, x.denominator), (y.numerator, y.denominator)) for x, y in pts))
    side = Fraction(str(w["side"]))
    return reader.Certificate(n=int(w["n"]), side=(side.numerator, side.denominator), squares=tuple(squares), tree={})


def summary(res: dict[str, Any]) -> dict[str, Any]:
    out = {k: res.get(k) for k in KEEP}
    if isinstance(out.get("least_margin"), dict):
        out["least_margin"] = {k: v for k, v in out["least_margin"].items() if k != "exact"}
    if isinstance(out.get("least_positive_wall_clearance"), dict):
        out["least_positive_wall_clearance"] = {k: v for k, v in out["least_positive_wall_clearance"].items() if k != "exact"}
    out["wall_contact_count"] = len(res.get("wall_contacts", []))
    return out


def main(argv: list[str]) -> int:
    label = argv[1]
    house = house_certificate(Path(argv[2]))
    res_house = check.decide(house)
    c954 = reader.read_paths(Path(argv[3]), Path(argv[4]))
    res_954 = check.decide(c954)
    receipt = {
        "program": "l108_house.py",
        "decider_sha256": check.program_digests(),
        label: {"file_sha256": check.sha256_file(Path(argv[2])), **summary(res_house)},
        "n954": {"file_sha256": check.sha256_file(Path(argv[3])), **summary(res_954)},
    }
    Path(argv[5]).write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    for name in (label, "n954"):
        r = receipt[name]
        print(name, r["verdict"], "touching", r["touching_pairs"], "contacts", r["wall_contact_count"], "least", r["least_margin"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
