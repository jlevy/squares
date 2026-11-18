"""Whole-packing decisions for the review of jlevy/squares#1031, by both methods.

Written for this review; imports nothing from this repository or the source.

``decide_a`` runs method A (``rv1031_axes``) on poses; ``decide_b`` runs method B
(``rv1031_clip``) on corners.  ``compare`` holds the two to equal classes at every pair
and every wall.  No distance filter and no tolerance is applied: every pair is decided.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction

from gmpy2 import mpq

import rv1031_axes as A
import rv1031_clip as B

WALLS = ("left", "bottom", "right", "top")


def fstr(v: Fraction) -> str:
    return f"{v.numerator}/{v.denominator}" if v.denominator != 1 else str(v.numerator)


def short(v: Fraction | int | float, digits: int = 12) -> str:
    """A short decimal print of an exact value (for reading, never for deciding)."""
    v = Fraction(v)
    if v == 0:
        return "0"
    neg = v < 0
    v = abs(v)
    e = 0
    while v >= 10:
        v /= 10
        e += 1
    while v < 1:
        v *= 10
        e -= 1
    scaled = round(v * 10 ** (digits - 1))
    if scaled >= 10**digits:
        scaled //= 10
        e += 1
    s = str(scaled)
    mant = s[0] + "." + s[1:]
    return f"{'-' if neg else ''}{mant}e{e:+d}"


def decide_a(poses: list[A.Pose], side: Fraction, pairs: list[tuple[int, int]] | None = None) -> dict:
    margins = A.all_margins(poses, pairs)
    clear = A.all_clearances(poses, side)
    return {"margins": margins, "clearances": clear}


def decide_b(corners: list[list[tuple[Fraction, Fraction]]], side: Fraction, pairs: list[tuple[int, int]] | None = None) -> dict:
    """Method B: unit tests, senses, pair classes and areas, wall terms, areas inside."""
    sq = [B.to_mpq(c) for c in corners]
    senses = [B.unit_square_sense(c) for c in sq]
    bad = [k for k, s in enumerate(senses) if s is None]
    side_q = mpq(side.numerator, side.denominator)
    if bad:
        return {"unit_failures": bad, "senses": senses}
    cc = [B.ccw(c) for c in sq]
    n = len(cc)
    classes: dict[tuple[int, int], tuple[str, object]] = {}
    todo = pairs if pairs is not None else [(i, j) for i in range(n) for j in range(i + 1, n)]
    for i, j in todo:
        classes[(i, j)] = B.pair_class(cc[i], cc[j])
    walls = [B.wall_terms(c, side_q) for c in cc]
    inside = [B.area_inside(c, side_q) for c in cc]
    return {"unit_failures": [], "senses": senses, "classes": classes, "walls": walls, "inside": inside}


def margins_digest(margins: dict[tuple[int, int], Fraction]) -> str:
    h = hashlib.sha256()
    for (i, j) in sorted(margins):
        h.update(f"{i + 1} {j + 1} {fstr(margins[(i, j)])}\n".encode())
    return h.hexdigest()


def clearances_digest(clear: list[tuple[Fraction, ...]]) -> str:
    h = hashlib.sha256()
    for k, c in enumerate(clear, start=1):
        h.update((f"{k} " + " ".join(fstr(x) for x in c) + "\n").encode())
    return h.hexdigest()


def compare(da: dict, db: dict) -> dict:
    """Classes of A and B at every pair and wall, and the summary of both."""
    out: dict = {"pair_mismatches": [], "wall_mismatches": [], "inside_not_one": []}
    if db.get("unit_failures"):
        out["unit_failures"] = [k + 1 for k in db["unit_failures"]]
        return out
    for key, m in da["margins"].items():
        ka = A.klass(m)
        kb, area = db["classes"][key]
        if ka != kb:
            out["pair_mismatches"].append([key[0] + 1, key[1] + 1, ka, kb])
        if kb != "overlap" and area != 0:
            out["pair_mismatches"].append([key[0] + 1, key[1] + 1, "area", str(area)])
    for k, (ca, cb) in enumerate(zip(da["clearances"], db["walls"], strict=True)):
        for w in range(4):
            fa = A.wall_class(ca[w])
            fb = A.wall_class(B.mpq_to_fraction(cb[w]))
            if fa != fb:
                out["wall_mismatches"].append([k + 1, WALLS[w], fa, fb])
            if ca[w] != B.mpq_to_fraction(cb[w]):
                out["wall_mismatches"].append([k + 1, WALLS[w], "value", fstr(ca[w])])
        contained_a = min(ca) >= 0
        if (db["inside"][k] == 1) != contained_a:
            out["inside_not_one"].append([k + 1, str(db["inside"][k])])
    return out


def summarize_a(da: dict, side: Fraction, list_limit: int = 2000) -> dict:
    margins = da["margins"]
    counts = {"apart": 0, "contact": 0, "overlap": 0}
    for m in margins.values():
        counts[A.klass(m)] += 1
    contacts = sorted(k for k, m in margins.items() if m == 0)
    overlaps = sorted(k for k, m in margins.items() if m < 0)
    pos = [(m, k) for k, m in margins.items() if m > 0]
    least = min(((m, k) for k, m in margins.items()), default=None)
    least_pos = min(pos, default=None)
    thresholds = [Fraction(1, 10**e) for e in (30, 20, 15, 12, 9, 6, 3, 2, 1)]
    below = {f"1e-{e}": sum(1 for m, _ in pos if m < t) for e, t in zip((30, 20, 15, 12, 9, 6, 3, 2, 1), thresholds, strict=True)}
    wall_counts = {w: {"clear": 0, "contact": 0, "cross": 0} for w in WALLS}
    wall_contacts = []
    least_wall = None
    for k, c in enumerate(da["clearances"], start=1):
        for w in range(4):
            wall_counts[WALLS[w]][A.wall_class(c[w])] += 1
            if c[w] == 0:
                wall_contacts.append([k, WALLS[w]])
            if least_wall is None or c[w] < least_wall[0]:
                least_wall = (c[w], k, WALLS[w])
    pos_walls = [(c[w], k, WALLS[w]) for k, c in enumerate(da["clearances"], start=1) for w in range(4) if c[w] > 0]
    least_pos_wall = min(pos_walls, default=None)
    out = {
        "pairs": len(margins),
        "classes": counts,
        "least_margin": None if least is None else {"pair": [least[1][0] + 1, least[1][1] + 1], "exact": fstr(least[0]), "short": short(least[0])},
        "least_positive_margin": None if least_pos is None else {"pair": [least_pos[1][0] + 1, least_pos[1][1] + 1], "exact": fstr(least_pos[0]), "short": short(least_pos[0])},
        "positive_margins_below": below,
        "contact_pairs": [[i + 1, j + 1] for i, j in contacts[:list_limit]],
        "contact_pairs_listed_all": len(contacts) <= list_limit,
        "overlap_pairs": [[i + 1, j + 1, short(margins[(i, j)])] for i, j in overlaps[:list_limit]],
        "margins_sha256": margins_digest(margins),
        "walls": wall_counts,
        "wall_contacts": wall_contacts,
        "least_clearance": None if least_wall is None else {"square": least_wall[1], "wall": least_wall[2], "exact": fstr(least_wall[0]), "short": short(least_wall[0])},
        "least_positive_clearance": None if least_pos_wall is None else {"square": least_pos_wall[1], "wall": least_pos_wall[2], "exact": fstr(least_pos_wall[0]), "short": short(least_pos_wall[0])},
        "clearances_sha256": clearances_digest(da["clearances"]),
    }
    return out


def summarize_b(db: dict) -> dict:
    if db.get("unit_failures"):
        return {"unit_failures": [k + 1 for k in db["unit_failures"]]}
    counts = {"apart": 0, "contact": 0, "overlap": 0}
    for kb, _ in db["classes"].values():
        counts[kb] += 1
    senses = {"ccw": 0, "cw": 0}
    for s in db["senses"]:
        senses[s] += 1
    return {
        "pairs": len(db["classes"]),
        "classes": counts,
        "senses": senses,
        "overlap_area_total": str(sum((a for k, a in db["classes"].values() if k == "overlap"), mpq(0))),
        "squares_with_area_inside_one": sum(1 for a in db["inside"] if a == 1),
    }


def extent(poses: list[A.Pose]) -> dict:
    """The packing's exact extent: least x and y reached, width and height."""
    hs = [A.half_extent(p) for p in poses]
    xmin = min(p[0] - h for p, h in zip(poses, hs, strict=True))
    xmax = max(p[0] + h for p, h in zip(poses, hs, strict=True))
    ymin = min(p[1] - h for p, h in zip(poses, hs, strict=True))
    ymax = max(p[1] + h for p, h in zip(poses, hs, strict=True))
    return {"xmin": xmin, "xmax": xmax, "ymin": ymin, "ymax": ymax, "width": xmax - xmin, "height": ymax - ymin}


def verdict_ok(sa: dict, cmp_: dict) -> bool:
    if cmp_.get("unit_failures") or cmp_["pair_mismatches"] or cmp_["wall_mismatches"] or cmp_["inside_not_one"]:
        return False
    if sa["classes"]["overlap"]:
        return False
    return all(sa["walls"][w]["cross"] == 0 for w in WALLS)
