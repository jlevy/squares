"""Lane L159's controls: decide the 20 stated controls and compare each with the plan.

Clean-room code written for the stage 4 review of issue #983, after the plan was stated
and hashed. Every whole-file control is decided by both methods over every square, wall
and pair (l159_check.decide); the reader controls change the YAML and the twin alike,
except G7, which changes the twin only; S5 is decided pair by pair and S6 square by
square, by both methods.

Usage: l159_controls.py CERT.yaml TWIN.json PLAN.json PLAN_FACTS.json CHECK.json OUT.json
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l159_clip as clip  # noqa: E402
import l159_geom as geom  # noqa: E402
import l159_sat as sat  # noqa: E402
from l159_check import Decision, decide, margin_digest  # noqa: E402
from l159_reader import Refused, read_texts  # noqa: E402

EPS = Fraction(1, 10**30)
WALLS = ("left", "bottom", "right", "top")


def frac_text(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def observe(d: Decision) -> dict[str, object]:
    """What a whole-file decision shows, in the plan's terms."""
    obs: dict[str, object] = {"verdict": d.verdict, "not_unit_a": d.not_unit_a, "not_unit_b": d.not_unit_b}
    if d.stopped:
        obs["stopped"] = d.stopped
        return obs
    obs["overlapping"] = sorted([list(k) for k, v in d.class_a.items() if v == "overlap"])
    obs["touching"] = sorted([list(k) for k, v in d.class_a.items() if v == "contact"])
    obs["wall_contacts"] = sorted([[i + 1, WALLS[k]] for i, row in enumerate(d.clearance) for k in range(4) if row[k] == 0])
    obs["wall_crossings"] = sorted([[i + 1, WALLS[k]] for i, row in enumerate(d.clearance) for k in range(4) if row[k] < 0])
    obs["not_contained"] = [i + 1 for i, ok in enumerate(d.contained_b) if not ok]
    obs["senses"] = "ccw" if all(s == 1 for s in d.sense_a) else "cw" if all(s == -1 for s in d.sense_a) else "mixed"
    obs["senses_agree"] = d.sense_a == d.sense_b
    obs["disagreements"] = len(d.disagreements)
    obs["margin_digest"] = margin_digest(d)
    if d.margins:
        k = min(d.margins, key=lambda x: (d.margins[x], x))
        obs["least_margin"] = [list(k), geom.sci(d.margins[k], 6)]
    return obs


def compare(d: Decision, expect: dict[str, object]) -> tuple[bool, list[str], dict[str, object]]:
    obs = observe(d)
    problems: list[str] = []
    for key, want in expect.items():
        if key == "overlapping" and want == "at_least_one":
            if not obs.get("overlapping"):
                problems.append("no overlapping pair")
        elif key == "overlap_exact":
            for i, j, m, a in want:  # type: ignore[union-attr]
                if d.margins.get((i, j)) != Fraction(m):
                    problems.append(f"margin of {(i, j)}")
                area = d.area_b.get((i, j), Fraction(0))
                if (a == "positive" and not area > 0) or (a != "positive" and area != Fraction(a)):
                    problems.append(f"area of {(i, j)}")
        elif key == "touching_margin_zero":
            if any(d.margins[tuple(k)] != 0 for k in obs["touching"]):  # type: ignore[union-attr]
                problems.append("touching margin not zero")
        elif key == "senses":
            if obs.get("senses") != want or not obs.get("senses_agree"):
                problems.append(f"senses {obs.get('senses')}")
        elif key == "margin_digest":
            if obs.get("margin_digest") != want:
                problems.append("margin digest differs")
        elif key in ("wall_contacts", "wall_crossings"):
            if obs.get(key) != sorted(want):  # type: ignore[arg-type]
                problems.append(f"{key} {obs.get(key)}")
        elif obs.get(key) != want:
            problems.append(f"{key} {obs.get(key)}")
    if "overlapping" in obs:
        obs["overlapping_count"] = len(obs["overlapping"])  # type: ignore[arg-type]
        if len(obs["overlapping"]) > 20:  # type: ignore[arg-type]
            obs["overlapping"] = obs["overlapping"][:20]  # type: ignore[index]
    obs.pop("margin_digest", None)
    return not problems, problems, obs


def reader_control(yaml_text: str, json_text: str, reason: str) -> tuple[bool, list[str], dict[str, object]]:
    try:
        read_texts(yaml_text, json_text)
    except Refused as exc:
        message = str(exc)
        ok = reason in message
        return ok, [] if ok else [f"refused for {message!r}"], {"refused": message}
    return False, ["accepted"], {"refused": None}


def main(argv: list[str]) -> int:
    cert, twin, plan_path, facts_path, check_path, out_path = (Path(a) for a in argv[1:7])
    yaml_text = cert.read_text(encoding="utf-8")
    json_text = twin.read_text(encoding="utf-8")
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    facts = json.loads(facts_path.read_text(encoding="utf-8"))
    check = json.loads(check_path.read_text(encoding="utf-8"))
    w = read_texts(yaml_text, json_text)
    side = Fraction(*w.side)
    squares = list(w.squares)
    n = w.n
    frames = [geom.centre_frame(c) for c in squares]
    side_text = f"{w.side[0]}/{w.side[1]}"
    results = []

    def as_side(x: Fraction) -> tuple[int, int]:
        return (x.numerator, x.denominator)

    for control in plan["controls"]:
        started = time.process_time()
        cid = control["id"]
        expect = control["expect"]
        if control["kind"] == "reader":
            twin_tree = json.loads(json_text)
            if cid == "G3":
                start = yaml_text.index(f"  - id: {n}\n")
                end = yaml_text.index("  claim:\n", start)
                y2 = yaml_text[:start] + yaml_text[end:]
                twin_tree["witness"]["squares"].pop()
                j2 = json.dumps(twin_tree, indent=2)
            elif cid == "G4":
                assert yaml_text.count(f"  - id: {n}\n") == 1
                y2 = yaml_text.replace(f"  - id: {n}\n", "  - id: 1\n")
                twin_tree["witness"]["squares"][n - 1]["id"] = 1
                j2 = json.dumps(twin_tree, indent=2)
            elif cid == "G7":
                y2 = yaml_text
                last = side_text[-1]
                altered = side_text[:-1] + ("1" if last != "1" else "2")
                assert json_text.count(f'"side": "{side_text}"') == 1
                j2 = json_text.replace(f'"side": "{side_text}"', f'"side": "{altered}"')
            elif cid == "G9":
                p, q = w.side
                doubled = f"{2 * p}/{2 * q}"
                assert yaml_text.count(f"  side: {side_text}\n") == 1
                y2 = yaml_text.replace(f"  side: {side_text}\n", f"  side: {doubled}\n")
                twin_tree["witness"]["side"] = doubled
                j2 = json.dumps(twin_tree, indent=2)
            else:
                raise ValueError(cid)
            ok, problems, obs = reader_control(y2, j2, expect["reason"])
        elif control["kind"] == "file":
            sq = list(squares)
            s = side
            if cid == "G1":
                sq[n - 1] = sq[0]
            elif cid == "G2":
                sq[0] = geom.translate(sq[0], (side, Fraction(0)))
            elif cid == "G5":
                c = list(sq[0])
                (xp, xq), y = c[2]
                x = Fraction(xp, xq) + EPS
                c[2] = ((x.numerator, x.denominator), y)
                sq[0] = tuple(c)
            elif cid == "G6":
                new = []
                for corners in sq:
                    pts = geom.as_fraction_points(corners)
                    total = pts[0][1] + pts[2][1]
                    new.append(tuple(geom.as_int_point((x, total - y)) for x, y in pts))
                sq = new
            elif cid == "G8":
                sq = [tuple(geom.as_int_point((y, x)) for x, y in geom.as_fraction_points(c)) for c in sq]
            elif cid == "G10":
                sq = [c[1:] + c[:1] for c in sq]
            elif cid == "G11":
                sq = [(c[0], c[3], c[2], c[1]) for c in sq]
            elif cid == "G12":
                sq = [tuple(geom.as_int_point((side - y, x)) for x, y in geom.as_fraction_points(c)) for c in sq]
            elif cid == "S1a":
                s = Fraction(w.side[0] - 1, w.side[1])
            elif cid == "S1b":
                s = side - EPS
            elif cid == "S1c":
                s = Fraction(facts["floor12"])
            elif cid == "S1d":
                s = Fraction(facts["ceil12"])
            elif cid in ("S4c", "S4p"):
                mv = control["move"]
                i, j = mv["pair"]
                mover = mv["mover"]
                other = i if mover == j else j
                co, uo, wo = frames[other - 1]
                cm, um, wm = frames[mover - 1]
                t0, t1, _ = geom.closing(co, uo, wo, cm, um, wm, EPS)
                t = t0 if mv["to"] == "contact" else t1
                sq[mover - 1] = geom.translate(sq[mover - 1], (t * (co[0] - cm[0]), t * (co[1] - cm[1])))
            else:
                raise ValueError(cid)
            d = decide(as_side(s), sq)
            ok, problems, obs = compare(d, expect)
        elif control["kind"] == "pairs":
            lines = []
            problems = []
            done = 0
            for i, j in expect["pairs"]:
                ci, ui, wi = frames[i - 1]
                cj, uj, wj = frames[j - 1]
                t0, t1, _ = geom.closing(ci, ui, wi, cj, uj, wj, EPS)
                lines.append(f"{i} {j} {frac_text(t0)} {frac_text(t1)}\n")
                a = sat.prepare(squares[i - 1])
                pa = clip.to_points(squares[i - 1])
                planes = clip.edge_half_planes(pa)
                for t, want_m, want_c in ((t0, Fraction(0), "contact"), (t1, -EPS, "overlap")):
                    moved = geom.translate(squares[j - 1], (t * (ci[0] - cj[0]), t * (ci[1] - cj[1])))
                    b = sat.prepare(moved)
                    m = sat.margin(a, b)  # type: ignore[arg-type]
                    cls_b, _ = clip.pair(clip.to_points(moved), planes)
                    if sat.margin_fraction(m) != want_m or sat.margin_class(m[0]) != want_c or cls_b != want_c:
                        problems.append(f"pair {(i, j)} at {want_c}")
                done += 1
            digest = hashlib.sha256("".join(lines).encode()).hexdigest()
            if digest != expect["closing_times_sha256"]:
                problems.append("closing times differ from the plan")
            ok = not problems
            obs = {"pairs_decided": done, "closing_times_sha256": digest}
        elif control["kind"] == "squares":
            lines = []
            problems = []
            counts = {wall: 0 for wall in WALLS}
            for (i, wall) in expect["nearest_walls"]:
                k = WALLS.index(wall)
                a0 = sat.prepare(squares[i - 1])
                c = sat.clearances(a0, w.side)[k]  # type: ignore[arg-type]
                if min(sat.clearances(a0, w.side)) != c:  # type: ignore[arg-type]
                    problems.append(f"square {i}: {wall} is not its nearest wall")
                lines.append(f"{i} {wall} {frac_text(c)}\n")
                counts[wall] += 1
                for extra, want_c, want_cls in ((Fraction(0), Fraction(0), "contact"), (EPS, -EPS, "cross")):
                    step = c + extra
                    v = {"left": (-step, Fraction(0)), "bottom": (Fraction(0), -step), "right": (step, Fraction(0)), "top": (Fraction(0), step)}[wall]
                    moved = geom.translate(squares[i - 1], v)
                    a = sat.prepare(moved)
                    got = sat.clearances(a, w.side)[k]  # type: ignore[arg-type]
                    pts = clip.to_points(moved)
                    cls_b = clip.walls(pts, w.side)[k]
                    inside = clip.contained(pts, w.side)
                    if got != want_c or sat.clearance_class(got) != want_cls or cls_b != want_cls or inside != (want_cls == "contact"):
                        problems.append(f"square {i} at {want_cls}")
            digest = hashlib.sha256("".join(lines).encode()).hexdigest()
            if digest != expect["nearest_walls_sha256"]:
                problems.append("nearest walls differ from the plan")
            ok = not problems
            obs = {"squares_decided": len(expect["nearest_walls"]), "nearest_wall_counts": counts, "nearest_walls_sha256": digest}
        else:
            raise ValueError(control["kind"])
        results.append(
            {
                "id": cid,
                "change": control["change"],
                "stated": control["stated"],
                "as_stated": ok,
                "problems": problems[:20],
                "observed": obs,
                "cpu_seconds": round(time.process_time() - started, 1),
            }
        )
        print(cid, "as stated" if ok else f"NOT AS STATED {problems[:3]}", flush=True)
    every = all(r["as_stated"] for r in results)
    receipt = {
        "program": "l159_controls.py",
        "certificate_sha256": hashlib.sha256(cert.read_bytes()).hexdigest(),
        "plan_sha256": hashlib.sha256(plan_path.read_bytes()).hexdigest(),
        "check_margin_list_sha256": check["margin_list_sha256"],
        "verdict": "EVERY_CONTROL_AS_STATED" if every else "SOME_CONTROL_NOT_AS_STATED",
        "as_stated": sum(1 for r in results if r["as_stated"]),
        "controls": results,
    }
    out_path.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    print(receipt["verdict"], receipt["as_stated"], "of", len(results))
    return 0 if every else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
