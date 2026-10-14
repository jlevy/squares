"""A202 -- the page drawn from the fast30 certificates (certs/f30_<nid>_<pad>_s<stage>.json), stage 0 IMMEDIATELY
after the closed-form layer and stage 1 (A200's exact option table on the surviving cells) when it has run.
Drawing rules (the PI's): pins as pins (blue stock squares); H's record box dashed, its clipped box solid, with a
hypothesis square ONLY at an admissible pose (live200.admissible: container + pins; dashed schematic otherwise);
alive sub-rects grey stipple; dead sub-rects white with the killing rule's letter; slot boxes dashed in colour;
the count's witness cells yellow; every rule's kill count and milliseconds printed; a note saying what the panel IS.
    python fig202.py <nid>            docs/residue_map/fast30_<nid>.svg
    python fig202.py gallery          docs/residue_map/fast30_gallery.svg
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
RULECOL = {"P": "#1565c0", "W": "#455a64", "C": "#c62828", "M": "#ad1457", "L": "#6a1b9a", "R": "#9e9e9e", "X": "#9e9e9e", "": "#000"}
RULETXT = {"P": "pins (inscribed disc of radius 1/2 meets a pin core)", "W": "walls (w_min/2)", "C": "Lemma CN against every alive piece of H",
           "M": "relative-tilt separating-axis bound against H", "L": "open-chord row (pins + H + piece > s)",
           "R": "reach: no slot's widened box within reach (disc 1/sqrt2 / half-extent, then A161's exact miss X)"}
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
    L = [("%s  pad %s  STAGE 0: %s  (%.0f ms)" % (cert["nid"], cert.get("pad"), v, 1000 * float(cert.get("seconds") or 0)), 11, col, True)]
    if cert.get("leaf"):
        s = str(cert["leaf"])
        while s:
            L.append((s[:100], 8, col, False)); s = s[100:]
    L.append(("STAGE 0 = closed-form tests only (no exact option table, no branching, no LP); verdict %s" % (cert.get("verifier") or "[C: closed-form trace]"), 7.5, "#333", False))
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
    L.append(("assignment count (Theorem COUNT, pair table A1/CN/MK): no chords %s (%s nodes); with chords %s (%s nodes); free options %s; pairs %s" % (
        cn.get("feasible"), cn.get("nodes"), cc.get("feasible"), cc.get("nodes"), rd.get("n_free_opts"), rd.get("pair_stats")), 7.5, "#333", False))
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
    for f in sorted(glob.glob(os.path.join(CERTS, "f30_%s_*_s*.json" % nid))):
        try:
            c = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        c["_file"] = os.path.basename(f)
        out.append(c)
    out.sort(key=lambda c: (int(c.get("stage", 0)), {"g1": 0, "window": 0, "zero": 1}.get(c.get("pad"), 2)))
    return out


def page_svg(nid, certs):
    S = 118
    PW = int(S0 * S) + 20
    TW = 600
    body = [text(20, 22, "%s -- A202 fast30: STAGE 0 (closed-form geometric kill layer, <= 30 s) drawn first; STAGE 1 (A200's exact option table on the surviving cells) below it when run" % nid, 13, "#000", True),
            text(20, 38, "grey stipple = sub-rects (centre cells x any tilt) where some forced slot's meeter may still sit; white + letter = dead, the letter is the rule (P pins, W walls, C CN vs H, M tilt-SAT vs H, L chord row, R reach / A161 miss); "
                 "dashed colour = slot unit + its alive-union box; blue = pins; black = H (record dashed, clipped solid) with a hypothesis square at an admissible pose; yellow = the count's witness.", 8, "#444"),
            text(20, 50, "read-only from certs/f30_*.json; rendered %s" % time.strftime("%Y-%m-%d %H:%M:%S"), 8, "#444")]
    y0 = 70
    ybot = y0
    rows = {0: [c for c in certs if int(c.get("stage", 0)) == 0], 1: [c for c in certs if int(c.get("stage", 0)) == 1]}
    for stage in (0, 1):
        for k, c in enumerate(rows[stage]):
            ox = 20 + k * (PW + TW)
            body.append(text(ox, y0 - 6, "PANEL stage %d / pad %s: %s" % (stage, c.get("pad"), c["_file"]), 9, "#000", True))
            if stage == 0:
                yb = panel0(c, body, ox, y0, S)
                yt = side0(c, body, ox + PW + 10, y0 + 12)
            else:
                yb = LV.panel(c, body, ox, y0, S)
                yt = LV.side_text(c, body, ox + PW + 10, y0 + 12, TW)
                body.append(text(ox + PW + 10, yt + 4, "STAGE 1 = A200's exact option table (A171 dead test / A161 miss, depth 5) on the cells stage 0 left alive, with stage 0's clipped H; verdict [C: exact-test trace]", 7.5, "#333"))
                yt += 14
            ybot = max(ybot, yb, yt)
        if rows[stage]:
            y0 = ybot + 40
    W = 2 * (PW + TW) + 40
    return "\n".join(['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" font-family="Segoe UI, sans-serif" style="background:#fff">' % (W, ybot + 20), defs()] + body + ["</svg>"])


def render(nid):
    certs = load(nid)
    if not certs:
        return None
    os.makedirs(OUTD, exist_ok=True)
    p = os.path.join(OUTD, "fast30_%s.svg" % nid)
    open(p, "w", encoding="utf-8").write(page_svg(nid, certs))
    return p


def gallery():
    S = 52
    PW = int(S0 * S) + 16
    PH = PW + 34
    ncol = 6
    files = sorted(glob.glob(os.path.join(CERTS, "f30_*_s0.json")))
    nids = sorted({os.path.basename(f)[4:].rsplit("_", 2)[0] for f in files})
    body = [text(16, 20, "A202 fast30 -- stage 0 (closed-form layer) over the k5_16 / k5_11 pages, one thumbnail per page (g1 pad; red = DEAD at some pad/stage); rendered %s" % time.strftime("%Y-%m-%d %H:%M:%S"), 12, "#000", True)]
    for k, nid in enumerate(nids):
        certs = load(nid)
        c = [x for x in certs if x.get("stage", 0) == 0 and x.get("pad") == "g1"] or certs
        c = c[0]
        dead = [x for x in certs if x.get("verdict") == "DEAD"]
        ox, oy = 16 + (k % ncol) * PW, 40 + (k // ncol) * PH
        panel0(c, body, ox, oy, S, small=True)
        col = "#c62828" if dead else "#2e7d32"
        body.append(text(ox, oy + S0 * S + 11, nid.replace("_interior", ""), 8, "#000", True))
        body.append(text(ox, oy + S0 * S + 21, ("DEAD s%s pad %s" % (dead[0].get("stage"), dead[0].get("pad"))) if dead else "ALIVE (%d certs)" % len(certs), 7, col))
    nrow = max(1, (len(nids) + ncol - 1) // ncol)
    doc = "\n".join(['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" font-family="Segoe UI, sans-serif" style="background:#fff">' % (ncol * PW + 32, 40 + nrow * PH), defs()] + body + ["</svg>"])
    p = os.path.join(OUTD, "fast30_gallery.svg")
    open(p, "w", encoding="utf-8").write(doc)
    return p


if __name__ == "__main__":
    if sys.argv[1] == "gallery":
        print(gallery())
    else:
        print(render(sys.argv[1]))
