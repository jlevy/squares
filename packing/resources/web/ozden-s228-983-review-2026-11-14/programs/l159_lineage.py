"""Lane L159's lineage measure: the issue's counts against the record; decides nothing.

Written after the findings were frozen, for the stage 4 review of issue #983. The issue
says that, matched up to the square's eight symmetries, all 228 centres move by more
than 0.001 against the registry packing, 93 by more than 0.05 (largest 0.940), and 59
squares retilt by more than 1 degree, and that the record has 51 squares tilted beyond
0.5 degrees. This program places each registered packing at 228 in the new box under
the eight symmetries of its own box and five anchorings (the four corners and the
centre), assigns squares by least total squared move and by least summed move (the
Hungarian method in binary64), and reports the counts for each placement; it also asks
whether nearest centres pair the squares one to one.

Usage: l159_lineage.py CERT.yaml TWIN.json OUT.json LABEL=KIND:PATH ...
  KIND is witness-center-basis (rational centre and basis), evand-cert (rational centre
  and half-angle tangent, gzip or plain), or witness-center-angle (decimal centre and
  angle in radians).
"""

from __future__ import annotations

import gzip
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import yaml  # noqa: E402
from scipy.optimize import linear_sum_assignment  # noqa: E402

import l159_geom as geom  # noqa: E402
from l159_reader import read_paths  # noqa: E402

Loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
ANCHORS = ("lower-left", "lower-right", "upper-left", "upper-right", "centre")
SYMMETRIES = ("identity", "turn 90", "turn 180", "turn 270", "reflect x", "reflect y", "transpose", "anti-transpose")


def fold(deg: float) -> float:
    while deg > 45:
        deg -= 90
    while deg <= -45:
        deg += 90
    return deg


def read_reference(kind: str, path: Path) -> tuple[float, np.ndarray, np.ndarray]:
    """Side, centres (n x 2) and folded angles in degrees, in binary64."""
    if kind == "witness-center-basis":
        w = yaml.load(path.read_text(encoding="utf-8"), Loader=Loader)["witness"]
        side = float(Fraction(str(w["side"])))
        cs, angs = [], []
        for sq in w["squares"]:
            cs.append([float(Fraction(str(v))) for v in sq["center"]])
            c, s = (Fraction(str(v)) for v in sq["basis"])
            angs.append(fold(math.degrees(math.atan2(float(s), float(c)))))
        return side, np.array(cs), np.array(angs)
    if kind == "evand-cert":
        raw = path.read_bytes()
        text = gzip.decompress(raw).decode() if path.suffix == ".gz" else raw.decode()
        lines = [ln for ln in text.splitlines() if ln.strip() and not ln.startswith("#")]
        side = float(Fraction(lines[0].split()[1]))
        cs, angs = [], []
        for ln in lines[1:]:
            x, y, t = (Fraction(v) for v in ln.split()[:3])
            cs.append([float(x), float(y)])
            angs.append(fold(math.degrees(2 * math.atan(float(t)))))
        return side, np.array(cs), np.array(angs)
    if kind == "witness-center-angle":
        w = yaml.load(path.read_text(encoding="utf-8"), Loader=Loader)["witness"]
        assert w["coordinates"]["angle_unit"] == "radians"
        side = float(w["side"])
        cs = np.array([[float(v) for v in sq["center"]] for sq in w["squares"]])
        angs = np.array([fold(math.degrees(float(sq["angle"]))) for sq in w["squares"]])
        return side, cs, angs
    raise ValueError(kind)


def place(cs: np.ndarray, angs: np.ndarray, side: float, sym: int, shift: tuple[float, float]) -> tuple[np.ndarray, np.ndarray]:
    x, y = cs[:, 0], cs[:, 1]
    L = side
    maps = [
        (x, y), (L - y, x), (L - x, L - y), (y, L - x),
        (L - x, y), (x, L - y), (y, x), (L - y, L - x),
    ]
    px, py = maps[sym]
    a = angs if sym < 4 else -angs
    return np.stack([px + shift[0], py + shift[1]], axis=1), np.array([fold(v) for v in a])


def counts(moves: np.ndarray, turns: np.ndarray) -> dict[str, object]:
    return {
        "beyond_1e-3": int((moves > 1e-3).sum()),
        "beyond_5e-2": int((moves > 5e-2).sum()),
        "beyond_1e-1": int((moves > 1e-1).sum()),
        "largest_move": round(float(moves.max()), 6),
        "retilt_beyond_1_degree": int((np.abs(turns) > 1).sum()),
        "summed_move": round(float(moves.sum()), 6),
        "total_squared": round(float((moves**2).sum()), 6),
    }


def main(argv: list[str]) -> int:
    cert, twin, out_path = (Path(a) for a in argv[1:4])
    specs = argv[4:]
    w = read_paths(cert, twin)
    s = float(Fraction(*w.side))
    frames = [geom.centre_frame(c) for c in w.squares]
    new_c = np.array([[float(c[0]), float(c[1])] for c, _, _ in frames])
    new_a = np.array([fold(math.degrees(math.atan2(float(u[1]), float(u[0])))) for _, u, _ in frames])
    out: dict[str, object] = {
        "program": "l159_lineage.py",
        "new_tilted_beyond_half_degree": int((np.abs(new_a) > 0.5).sum()),
        "issue_claims": {"beyond_1e-3": 228, "beyond_5e-2": 93, "largest_move": 0.940, "retilt_beyond_1_degree": 59, "record_tilted_beyond_half_degree": 51},
        "references": {},
    }
    for spec in specs:
        label, rest = spec.split("=", 1)
        kind, path = rest.split(":", 1)
        side, cs, angs = read_reference(kind, Path(path))
        ref: dict[str, object] = {
            "kind": kind,
            "path": path,
            "tilted_beyond_half_degree": int((np.abs(angs) > 0.5).sum()),
            "tilted_beyond_one_degree": int((np.abs(angs) > 1).sum()),
            "placements": [],
        }
        d = s - side
        shifts = {"lower-left": (0.0, 0.0), "lower-right": (d, 0.0), "upper-left": (0.0, d), "upper-right": (d, d), "centre": (d / 2, d / 2)}
        matches = []
        best = {}
        one_to_one = []
        for sym in range(8):
            for anchor in ANCHORS:
                pc, pa = place(cs, angs, side, sym, shifts[anchor])
                dist = np.sqrt(((new_c[:, None, :] - pc[None, :, :]) ** 2).sum(axis=2))
                nearest = dist.argmin(axis=1)
                if len(set(nearest.tolist())) == len(nearest):
                    one_to_one.append([SYMMETRIES[sym], anchor])
                for rule, cost in (("least total squared move", dist**2), ("least summed move", dist)):
                    rows, cols = linear_sum_assignment(cost)
                    moves = dist[rows, cols]
                    turns = np.array([fold(new_a[i] - pa[j]) for i, j in zip(rows, cols, strict=True)])
                    c = counts(moves, turns)
                    entry = {"symmetry": SYMMETRIES[sym], "anchor": anchor, "assignment": rule, **c}
                    ref["placements"].append(entry)  # type: ignore[union-attr]
                    key = "total_squared" if rule.startswith("least total") else "summed_move"
                    if rule not in best or c[key] < best[rule][key]:  # type: ignore[operator]
                        best[rule] = entry
                    if (c["beyond_1e-3"], c["beyond_5e-2"], round(c["largest_move"], 3), c["retilt_beyond_1_degree"]) == (228, 93, 0.940, 59):  # type: ignore[arg-type]
                        matches.append(entry)
        ref["best"] = best
        # Which squares stay within 1e-3 under the placement of least total squared move.
        b = best["least total squared move"]
        pc, pa = place(cs, angs, side, SYMMETRIES.index(b["symmetry"]), shifts[b["anchor"]])  # type: ignore[arg-type]
        dist = np.sqrt(((new_c[:, None, :] - pc[None, :, :]) ** 2).sum(axis=2))
        rows, cols = linear_sum_assignment(dist**2)
        still = [int(i) + 1 for i, j in zip(rows, cols, strict=True) if dist[i, j] <= 1e-3]
        upright_both = [i for i in still if abs(new_a[i - 1]) < 1e-6 and abs(pa[cols[list(rows).index(i - 1)]]) < 1e-6]
        ref["best_within_1e-3"] = {"count": len(still), "upright_in_both": len(upright_both), "squares": still}
        ref["placements_matching_issue_counts"] = matches
        ref["nearest_centres_one_to_one"] = one_to_one
        ref["placements_with_beyond_1e-1_at_most"] = min(p["beyond_1e-1"] for p in ref["placements"])  # type: ignore[union-attr, index]
        ref.pop("placements")
        out["references"][label] = ref  # type: ignore[index]
        print(label, "tilted>0.5:", ref["tilted_beyond_half_degree"], "| best:", {k: (v["symmetry"], v["anchor"], v["beyond_5e-2"], v["beyond_1e-1"], v["largest_move"], v["retilt_beyond_1_degree"]) for k, v in best.items()}, "| issue matches:", [(m["symmetry"], m["anchor"], m["assignment"]) for m in matches], "| one-to-one:", one_to_one)
    out_path.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
