"""A203 (copy of A202's fig202 at d13f7420: panel0 / side0 / load; the CSP panel and the page are in fig203b) -- the page drawn
from the csp203 certificates (certs/csp203_<nid>_<pad>_s0.json) IMMEDIATELY after stage 0 + the CSP.
Drawing rules (the PI's): pins as pins (blue stock squares); H's record box dashed, its clipped box solid, with a
hypothesis square ONLY at an admissible pose (live200.admissible: container + pins; dashed schematic otherwise);
alive sub-rects grey stipple; dead sub-rects white with the killing rule's letter; slot boxes dashed in colour;
the count's witness cells yellow; every rule's kill count and milliseconds printed; a note saying what the panel IS.
    python fig203b.py <nid>           docs/residue_map/csp203_<nid>.svg
"""
import glob
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CERTS = os.path.join(HERE, "..", "certs")
OUTD = os.path.join(ROOT, "docs", "residue_map")
sys.path.insert(0, os.path.join(ROOT, "attempts", "A200-k516-quick", "code"))
import live200 as LV                                           # noqa: E402  READ-ONLY (A200): text / sq / poly / admissible / panel

S0 = LV.S0
SLOTCOL = LV.SLOTCOL
RULECOL = {"P": "#1565c0", "W": "#455a64", "C": "#c62828", "M": "#ad1457", "L": "#6a1b9a", "R": "#9e9e9e", "X": "#9e9e9e", "H": "#d84315", "F": "#bf360c", "": "#000"}
RULETXT = {"P": "pins (inscribed disc of radius 1/2 meets a pin core)", "W": "walls (w_min/2)", "C": "Lemma CN against every alive piece of H",
           "M": "relative-tilt separating-axis bound against H", "L": "open-chord row (pins + H + piece > s)",
           "R": "reach: no slot's widened box within reach (disc 1/sqrt2 / half-extent, then A161's exact miss X)",
           "H": "H-CONSISTENCY: no piece of the cell meeting the slot is compatible (rule S) with any alive H piece",
           "F": "H-CONSISTENCY after SETTLE (the pairs refined 2x2x2 x 3 levels with P/W/C/M/L/R/X and rule S)"}
text, sq, defs = LV.text, LV.sq, LV.defs


def panel0(cert, body, ox, oy, S, small=False):
    X = lambda x: ox + x * S
    Y = lambda y: oy + (S0 - y) * S

    def rect(r, fill, op, stroke, w=1.0, dash=""):
        return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="%.2f" stroke="%s" stroke-width="%.1f"%s/>' % (
            X(r[0]), Y(r[3]), max(0.6, (r[1] - r[0]) * S), max(0.6, (r[3] - r[2]) * S), fill, op, stroke, w, (' stroke-dasharray="%s"' % dash) if dash else "")

    def poly(P, fill, op, stroke, w=1.0, dash=""):
        pts = " ".join("%.1f,%.1f" % (X(x), Y(y)) for x, y in P)
        return '<polygon points="%s" fill="%s" fill-opacity="%.2f" stroke="%s" stroke-width="%.1f"%s/>' % (pts, fill, op, stroke, w, (' stroke-dasharray="%s"' % dash) if dash else "")

    body.append(rect((0, S0, 0, S0), "#fff", 1.0, "#000", 1.6))
    for ci, si, r, status, alive_slots in cert.get("subrects") or []:
        body.append(rect(r, "#fff", 1.0, "#e6e6e6", 0.3))
        if status != "" and not small:
            body.append(text(X(0.5 * (r[0] + r[1])), Y(0.5 * (r[2] + r[3])) + 2, status, 5.5, RULECOL.get(status, "#888"), False, "middle"))
    for r, ks in cert.get("alive_rects") or []:
        body.append(rect(r, "url(#stipple)", 1.0, "#bbb", 0.2))
    cells = {int(t["cell"]): t["rect"] for t in cert.get("tests") or [] if t.get("test") == "CELL"}
    for ci, r in sorted(cells.items()):
        body.append(rect(r, "none", 0, "#999", 0.6))
        if not small:
            body.append(text(X(r[0]) + 2, Y(r[3]) + 7, "%d" % ci, 6, "#777"))
    rounds = cert.get("rounds") or []
    rd = rounds[-1] if rounds else {}
    urec = rd.get("union") or {}
    for k, p in enumerate(cert.get("slots") or []):
        col = SLOTCOL[k % len(SLOTCOL)]
        wb = (cert.get("wbox") or {}).get(p)
        if wb:
            body.append(rect(wb, col, 0.06, col, 1.3, "6,3"))
            if not small:
                body.append(text(X(0.5 * (wb[0] + wb[1])), Y(wb[3]) + 9, p, 7.5, col, True, "middle"))
        bb = (urec.get(p) or {}).get("bbox")
        if bb:
            body.append(rect(bb, "none", 0, col, 0.9, "2,2"))
    roles = cert.get("roles") or {}
    pins = [(0.5 * (b[0] + b[1]), 0.5 * (b[2] + b[3])) for n_, b in roles.items() if n_.startswith("P")]
    for cx, cy in pins:
        body.append(poly(sq(cx, cy, 0.0), "#90caf9", 0.6, "#1565c0", 1.2))
    for name, b in roles.items():
        if name.startswith("P"):
            continue
        if name == "H" and cert.get("H_record"):
            body.append(rect(cert["H_record"], "none", 0, "#000", 0.8, "4,3"))
        body.append(rect(b, "none", 0, "#000", 1.8 if not small else 1.0))
        z, how = LV.admissible(b, pins)
        if z is None:
            cx, cy, th = 0.5 * (b[0] + b[1]), 0.5 * (b[2] + b[3]), math.radians(0.5 * (b[4] + b[5]))
            body.append(poly(sq(cx, cy, th), "none", 0, "#000", 0.8, "5,4"))
            how = "NO admissible pose found (dashed: schematic)"
        else:
            cx, cy, th = z
            body.append(poly(sq(cx, cy, th), "#00e5ff", 0.18, "#000", 1.0 if not small else 0.6))
        if not small:
            body.append(text(X(cx), Y(cy) + 4, name, 10, "#000", True, "middle"))
            body.append(text(X(cx), Y(cy) + 14, "%.1f deg of %.1f-%.1f; %s" % (math.degrees(th), b[4], b[5], how), 6.5, "#000", False, "middle"))
    for rd_ in cert.get("csp") or []:
        for d in rd_.get("dead_opts") or []:
            h = d.get("hull")
            if not h:
                continue
            body.append(rect(h, RULECOL.get(d["rule"], "#c00"), 0.25, RULECOL.get(d["rule"], "#c00"), 0.8))
            if not small:
                body.append(text(X(h[1]) + 1, Y(h[2]), "%s%d" % (d["rule"], d["cell"]), 5, RULECOL.get(d["rule"], "#c00"), True))
    for w in cert.get("witness") or []:
        try:
            name, ci, served, r = w[0], w[1], w[2], [float(v) for v in w[3]]
        except Exception:
            continue
        body.append(rect(r, "#ffe082", 0.35, "#8d6e00", 0.7, "3,2"))
        if not small:
            body.append(text(X(0.5 * (r[0] + r[1])), Y(0.5 * (r[2] + r[3])) + 3, "%s:%s" % (name, ",".join(served)) if served else name, 5.5, "#6d4c00", False, "middle"))
    return oy + S0 * S


def side0(cert, body, x, y):
    rounds = cert.get("rounds") or []
    rd = rounds[-1] if rounds else {}
    v = cert.get("verdict")
    col = "#c62828" if v == "DEAD" else "#2e7d32"
    L = [("%s  pad %s  STAGE 0 + CSP: %s  (%.0f ms)" % (cert["nid"], cert.get("pad"), v, 1000 * float(cert.get("seconds") or 0)), 11, col, True)]
    if cert.get("leaf"):
        s = str(cert["leaf"])
        while s:
            L.append((s[:100], 8, col, False)); s = s[100:]
    L.append(("STAGE 0 + CSP = closed-form tests only (A202's piece rules + A203's piece-pair CSP: no exact option table, no branching, no LP); verdict %s" % (cert.get("verifier") or "[C: closed-form trace]"), 7.5, "#333", False))
    L.append(("pieces: %d = 25 cells x %d sub-rects x %d tilt bins; dead by the slot-independent rules: %d; rounds %d" % (
        cert.get("n_pieces", 0), (cert.get("n_pieces", 0) // max(1, 25 * cert.get("n_bins", 1))), cert.get("n_bins", 0), cert.get("n_dead", 0), len(rounds)), 7.5, "#333", False))
    L.append(("rule   kills   ms     meaning", 8, "#000", True))
    for k, d in (cert.get("kills") or {}).items():
        L.append(("%-6s %6d %7.1f   %s" % (k, d["kills"], d["ms"], RULETXT.get(k, {"H-clip": "H's own pieces off the pins / walls / not meeting its forced slots"}.get(k, ""))), 7.5, RULECOL.get(k, "#333"), False))
    L.append(("slot      alive cells  cap   union diam / l-inf / chord row   why", 8, "#000", True))
    single = rd.get("single") or {}
    urec = rd.get("union") or {}
    caps = cert.get("caps") or {}
    for k, p in enumerate(cert.get("slots") or []):
        u = urec.get(p) or {}
        L.append(("%-9s %3d          %-4s  %s / %s / %s   %s" % (p, len(single.get(p) or {}), "-" if caps.get(p) is None else caps.get(p),
                                                          u.get("diam", "-"), u.get("linf", "-"), u.get("chord_row", "-"), str(u.get("why", ""))[:44]), 7.5, SLOTCOL[k % len(SLOTCOL)], False))
    cn, cc = rd.get("count_nochord") or {}, rd.get("count_chord") or {}
    L.append(("H reaches %s; forced H at %s; H box %s" % (rd.get("H_reach"), cert.get("forced_H") or "-", cert.get("roles", {}).get("H")), 7.5, "#333", False))
    L.append(("assignment count (Theorem COUNT + H-mask + piece pairs A1/S): no chords %s (%s nodes, prunes %s); with chords %s (%s nodes); free options %s; pairs %s" % (
        cn.get("feasible"), cn.get("nodes"), cn.get("prunes"), cc.get("feasible"), cc.get("nodes"), rd.get("n_free_opts"), rd.get("pair_stats")), 7.5, "#333", False))
    if cert.get("witness"):
        L.append(("witness of the count (yellow): a cell per square with the slots it would serve -- a counting witness, not a packing", 7.5, "#6d4c00", False))
    st = [s for s in cert.get("steps") or []]
    L.append(("steps: " + " > ".join("%s %.0fms" % (s["step"], 1000 * float(s.get("seconds", 0))) for s in st[:10]), 7, "#555", False))
    L.append(("window pending: %s;  lam %s;  rendered %s" % (cert.get("window_pending"), cert.get("lam"), time.strftime("%Y-%m-%d %H:%M:%S")), 7, "#555", False))
    yy = y
    for t, sz, c, b in L:
        t = str(t)
        while True:
            body.append(text(x, yy, t[:120], sz, c, b)); yy += sz + 4; t = t[120:]
            if not t:
                break
    return yy


def load(nid):
    out = []
    for f in sorted(glob.glob(os.path.join(CERTS, "csp203_%s_*_s*.json" % nid))):
        try:
            c = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        c["_file"] = os.path.basename(f)
        out.append(c)
    out.sort(key=lambda c: (int(c.get("stage", 0)), {"g1": 0, "window": 0, "zero": 1}.get(c.get("pad"), 2)))
    return out


