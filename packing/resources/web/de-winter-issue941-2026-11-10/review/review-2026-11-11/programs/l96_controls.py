"""Controls for the L96 review, stated in advance and then decided by both methods.

Usage:
  python -I -B l96_controls.py plan PLAN_JSON CERT...   # states every outcome; decides no modified file
  python -I -B l96_controls.py run PLAN_JSON OUT_DIR CERT...

Controls, per certificate (C1-C6 and C9 are whole-file, decided by both methods through
the driver; C7 is pair-level and C8 square-level, decided by both methods directly):
  C1 every t negated (the rotation read the other way)
  C2 the side lowered by 1/q, one unit of its own last place
  C3 the side set to its 10-place floor
  C4 the side set to its 10-place ceiling, the issue's claim
  C5 the last square given square 1's (x, y, t)
  C6 square 1 translated by (side, 0)
  C7 every pair with margin below 1e-9, or touching, closed along its centre line to exact
     contact, and 1e-30 past it
  C8 every square moved to its nearest wall by its clearance, and 1e-30 past it
  C9 every square transposed, (x, y, t) -> (y, x, -t)
"""

import hashlib
import json
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l96_check as C  # noqa: E402
import l96_clip as B  # noqa: E402
import l96_read as R  # noqa: E402
import l96_sat as A  # noqa: E402
from gmpy2 import mpq  # noqa: E402

E30 = F(1, 10**30)
E9 = F(1, 10**9)
WALLS = ("left", "bottom", "right", "top")
TRANSPOSE = {"left": "bottom", "bottom": "left", "right": "top", "top": "right"}


def fs(q):
    q = F(q)
    return f"{q.numerator}/{q.denominator}" if q.denominator != 1 else str(q.numerator)


def write_cert(side, triples):
    lines = [f"{len(triples)} {fs(side)}"] + [" ".join(fs(v) for v in t) for t in triples]
    return ("\n".join(lines) + "\n").encode()


def load(path):
    with open(path, "rb") as fh:
        data = fh.read()
    cert = R.read_cert(data)
    side = F(*cert["side"])
    trip = [tuple(F(*v) for v in t) for t in cert["squares"]]
    return data, side, trip


def lam_star(si, sj):
    """Least lambda at which moving j by -lambda*d (d = centre j - centre i) makes contact."""
    dx, dy = sj[0] - si[0], sj[1] - si[1]
    lam = None
    for ax, ay, own_i in ((si[2], si[3], True), (-si[3], si[2], True), (sj[2], sj[3], False), (-sj[3], sj[2], False)):
        proj = abs(ax * dx + ay * dy)
        if proj == 0:
            continue
        H = F(1, 2) + A.support(ax, ay, sj if own_i else si)
        cand = 1 - H / proj
        lam = cand if lam is None or cand > lam else lam
    return lam


def near_pairs(trip):
    """Every pair with centres at most 2 apart, with its exact margin (pairs farther apart
    have margin above 0.4 and cannot fall below 1e-9)."""
    sqs = [A.square(*t) for t in trip]
    cells = {}
    for k, t in enumerate(trip):
        cells.setdefault((t[0].__floor__(), t[1].__floor__()), []).append(k)
    out = []
    for i, t in enumerate(trip):
        cx, cy = t[0].__floor__(), t[1].__floor__()
        for ddx in range(-3, 4):
            for ddy in range(-3, 4):
                for j in cells.get((cx + ddx, cy + ddy), ()):
                    if j <= i:
                        continue
                    dx, dy = trip[j][0] - t[0], trip[j][1] - t[1]
                    if dx * dx + dy * dy <= 4:
                        m, _ = A.margin(sqs[i], sqs[j])
                        out.append((i + 1, j + 1, m))
    return sqs, out


def plan(plan_path, paths):
    out = {"programs": C.program_digests() | {"l96_controls.py": C.sha256(os.path.join(HERE, "l96_controls.py"))}, "files": {}}
    for path in paths:
        data, side, trip = load(path)
        n = len(trip)
        sqs = [A.square(*t) for t in trip]
        clear = {k + 1: A.walls(s, side) for k, s in enumerate(sqs)}
        contacts = sorted([k, w] for k in clear for w in WALLS if clear[k][w] == 0)
        q = side.denominator
        floor10 = F((side.numerator * 10**10) // side.denominator, 10**10)
        ceil10 = -F(((-side).numerator * 10**10) // (-side).denominator, 10**10)

        def lowered(delta):
            outside = sorted([k, w] for k in clear for w in ("right", "top") if clear[k][w] < delta)
            touch = sorted(
                [k, w] for k in clear for w in WALLS if (clear[k][w] - (delta if w in ("right", "top") else 0)) == 0
            )
            return {"verdict": "REFUSE" if outside else "ACCEPT", "outside": outside, "contacts": touch}

        _, pairs = near_pairs(trip)
        sel = sorted([i, j] for i, j, m in pairs if m < E9)
        nearest = []
        for k in range(1, n + 1):
            w = min(WALLS, key=lambda w: (clear[k][w], WALLS.index(w)))
            nearest.append([k, w, fs(clear[k][w])])
        out["files"][os.path.basename(path)] = {
            "sha256": hashlib.sha256(data).hexdigest(),
            "n": n,
            "C1": {"verdict": "REFUSE", "overlapping": "at least one, equal by both methods", "outside": [], "contacts": contacts},
            "C2": {"side": fs(side - F(1, q))} | lowered(F(1, q)),
            "C3": {"side": fs(floor10)} | lowered(side - floor10),
            "C4": {"side": fs(ceil10)} | lowered(side - ceil10),
            "C5": {"verdict": "REFUSE", "overlaps": [[1, n]], "margin": "-1", "area": "1"},
            "C6": {"verdict": "REFUSE", "outside": [[1, "right"]], "overlaps": []},
            "C7": {"pairs": sel, "at": "contact", "past": "overlap"},
            "C8": {"squares": nearest, "at": "contact", "past": "outside"},
            "C9": {"verdict": "ACCEPT", "contacts": sorted([k, TRANSPOSE[w]] for k, w in contacts), "margins": "equal where both decide"},
        }
        print(os.path.basename(path), "planned:", len(sel), "near pairs;", len(contacts), "wall contacts", flush=True)
    with open(plan_path, "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")


def outside_of(rec):
    probs = [p for p in rec["problems"] if p.startswith("outside")]
    return probs


def run(plan_path, out_dir, paths):
    with open(plan_path, "rb") as fh:
        plan_bytes = fh.read()
    pl = json.loads(plan_bytes)
    os.makedirs(out_dir, exist_ok=True)
    digests = C.program_digests() | {"l96_controls.py": C.sha256(os.path.join(HERE, "l96_controls.py"))}
    for path in paths:
        name = os.path.basename(path)
        st = pl["files"][name]
        data, side, trip = load(path)
        assert hashlib.sha256(data).hexdigest() == st["sha256"]
        n = len(trip)
        res = {}

        def whole(tag, side2, trip2):
            rec, ra, rb = C.check_bytes(write_cert(side2, trip2))
            outs_a = sorted([k, w] for k in ra["clearances"] for w in WALLS if ra["clearances"][k][w] < 0)
            outs_b = sorted([k, w] for k in rb["clearances"] for w in WALLS if rb["clearances"][k][w] < 0)
            return rec, ra, rb, outs_a, outs_b

        # C1
        rec, ra, rb, oa, ob = whole("C1", side, [(x, y, -t) for x, y, t in trip])
        ok = (
            rec["verdict"] == "REFUSE"
            and rec["pairs"]["overlaps_A"]
            and rec["pairs"]["overlaps_A"] == rec["pairs"]["overlaps_B"]
            and not oa
            and not ob
            and sorted(rec["walls"]["contacts"]) == st["C1"]["contacts"]
        )
        res["C1"] = {"as_stated": bool(ok), "overlapping_pairs": len(rec["pairs"]["overlaps_A"])}
        # C2-C4
        for tag in ("C2", "C3", "C4"):
            rec, ra, rb, oa, ob = whole(tag, F(st[tag]["side"]), trip)
            ok = (
                rec["verdict"] == st[tag]["verdict"]
                and oa == st[tag]["outside"]
                and ob == st[tag]["outside"]
                and sorted(rec["walls"]["contacts"]) == st[tag]["contacts"]
                and not rec["pairs"]["overlaps_A"]
                and not rec["pairs"]["overlaps_B"]
            )
            res[tag] = {"as_stated": bool(ok), "outside": len(oa), "verdict": rec["verdict"]}
        # C5
        rec, ra, rb, oa, ob = whole("C5", side, trip[:-1] + [trip[0]])
        key = (1, n)
        ok = (
            rec["verdict"] == "REFUSE"
            and rec["pairs"]["overlaps_A"] == [[1, n]]
            and rec["pairs"]["overlaps_B"] == [[1, n]]
            and ra["margins"][key][0] == -1
            and C.as_frac(rb["areas"][key]) == 1
            and not oa
        )
        res["C5"] = {"as_stated": bool(ok)}
        # C6
        x, y, t = trip[0]
        rec, ra, rb, oa, ob = whole("C6", side, [(x + side, y, t)] + trip[1:])
        ok = rec["verdict"] == "REFUSE" and oa == [[1, "right"]] and ob == [[1, "right"]] and not rec["pairs"]["overlaps_A"] and not rec["pairs"]["overlaps_B"]
        res["C6"] = {"as_stated": bool(ok)}
        # C7, pair-level
        sqs = [A.square(*tt) for tt in trip]
        bad7 = []
        for i, j in st["C7"]["pairs"]:
            si, sj = sqs[i - 1], sqs[j - 1]
            lam = lam_star(si, sj)
            dx, dy = trip[j - 1][0] - trip[i - 1][0], trip[j - 1][1] - trip[i - 1][1]
            for delta, want in ((0, "contact"), (E30, "overlap")):
                l2 = lam + delta
                tj = (trip[i - 1][0] + dx * (1 - l2), trip[i - 1][1] + dy * (1 - l2), trip[j - 1][2])
                m, _ = A.margin(si, A.square(*tj))
                pi = B.corners(*(mpq(v.numerator, v.denominator) for v in trip[i - 1]))
                pj = B.corners(*(mpq(v.numerator, v.denominator) for v in tj))
                cb, _ = B.pair_class(pi, pj)
                if A.classify(m) != want or cb != want:
                    bad7.append([i, j, str(delta), A.classify(m), cb])
        res["C7"] = {"as_stated": not bad7, "pairs": len(st["C7"]["pairs"]), "not_as_stated": bad7}
        # C8, square-level
        bad8 = []
        for k, w, c in st["C8"]["squares"]:
            c = F(c)
            x, y, t = trip[k - 1]
            for delta, want in ((0, "contact"), (E30, "outside")):
                mv = c + delta
                x2, y2 = {"left": (x - mv, y), "right": (x + mv, y), "bottom": (x, y - mv), "top": (x, y + mv)}[w]
                wa = A.walls(A.square(x2, y2, t), side)[w]
                wb = C.as_frac(B.walls(B.corners(*(mpq(v.numerator, v.denominator) for v in (x2, y2, t))), mpq(side.numerator, side.denominator))[w])
                got_a = "contact" if wa == 0 else ("outside" if wa < 0 else "inside")
                got_b = "contact" if wb == 0 else ("outside" if wb < 0 else "inside")
                if got_a != want or got_b != want:
                    bad8.append([k, w, str(delta), got_a, got_b])
        res["C8"] = {"as_stated": not bad8, "squares": len(st["C8"]["squares"]), "not_as_stated": bad8}
        # C9
        rec0, ra0, _ = C.check_bytes(data)
        rec, ra, rb, oa, ob = whole("C9", side, [(y, x, -t) for x, y, t in trip])
        common = set(ra0["margins"]) & set(ra["margins"])
        eq = all(ra0["margins"][k][0] == ra["margins"][k][0] for k in common)
        clear_eq = all(ra0["clearances"][k][w] == ra["clearances"][k][TRANSPOSE[w]] for k in ra0["clearances"] for w in WALLS)
        ok = rec["verdict"] == "ACCEPT" and sorted(rec["walls"]["contacts"]) == st["C9"]["contacts"] and rec["pairs"]["contacts"] == rec0["pairs"]["contacts"] and eq and clear_eq
        res["C9"] = {"as_stated": bool(ok), "margins_compared": len(common)}
        allok = all(v["as_stated"] for v in res.values())
        rec_out = {"file": name, "programs": digests, "plan_sha256": hashlib.sha256(plan_bytes).hexdigest(), "controls": res, "result": "EVERY_CONTROL_AS_STATED" if allok else "NOT_AS_STATED"}
        with open(os.path.join(out_dir, "controls-" + name.replace(".cert", ".json")), "w") as fh:
            json.dump(rec_out, fh, indent=1)
            fh.write("\n")
        print(name, rec_out["result"], {k: (v["as_stated"], v.get("overlapping_pairs", v.get("pairs", v.get("outside", "")))) for k, v in res.items()}, flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "plan":
        plan(sys.argv[2], sys.argv[3:])
    else:
        run(sys.argv[2], sys.argv[3], sys.argv[4:])
