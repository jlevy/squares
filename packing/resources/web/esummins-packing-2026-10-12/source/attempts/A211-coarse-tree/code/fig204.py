"""A204 -- the page: one panel per ROUND and pad, drawn from the certificate (certs/polyclip204_<nid>.json) after every
round.  Drawing rules (memory: present-problems-spatially; A183.2): pins as pins; a role's PIECES as thin rects and its
certified K' filled; the hypothesis square ONLY at an admissible pose (the centre of the largest piece at its mid-tilt,
container + pins checked) with the dashed extremal outlines at that piece's own tilt ends -- never an excluded pose;
alive cells grey stipple (never green); slot boxes dashed in colour; the count's witness yellow; a note under every
panel saying what it IS and the seconds.      python fig204.py <nid> | gallery"""
import glob
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CERTS = os.path.join(HERE, "..", "certs")
OUTD = os.path.join(ROOT, "docs", "residue_map", "campaigns", "A204-polyclip")
sys.path.insert(0, os.path.join(ROOT, "attempts", "A200-k516-quick", "code"))
import live200 as LV                                           # noqa: E402  READ-ONLY (A200): text / sq / admissible / defs

S0, SLOTCOL, text, sq, defs = LV.S0, LV.SLOTCOL, LV.text, LV.sq, LV.defs
ROLECOL = ["#000000", "#6a1b9a", "#00695c", "#ef6c00", "#c62828", "#283593", "#4e342e", "#37474f"]


def panel(doc, snap, body, ox, oy, S, small=False):
    X = lambda x: ox + x * S
    Y = lambda y: oy + (S0 - y) * S

    def rect(r, fill, op, stroke, w=1.0, dash=""):
        return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="%.2f" stroke="%s" stroke-width="%.2f"%s/>' % (
            X(r[0]), Y(r[3]), max(0.5, (r[1] - r[0]) * S), max(0.5, (r[3] - r[2]) * S), fill, op, stroke, w, (' stroke-dasharray="%s"' % dash) if dash else "")

    def poly(P, fill, op, stroke, w=1.0, dash=""):
        return '<polygon points="%s" fill="%s" fill-opacity="%.2f" stroke="%s" stroke-width="%.2f"%s/>' % (
            " ".join("%.1f,%.1f" % (X(x), Y(y)) for x, y in P), fill, op, stroke, w, (' stroke-dasharray="%s"' % dash) if dash else "")

    body.append(rect((0, S0, 0, S0), "#fff", 1.0, "#000", 1.6))
    fz = snap.get("forcing") or {}
    cells = doc.get("cells") or []
    alive = set()
    for p, cs in (fz.get("single") or {}).items():
        alive |= set(int(c) for c in cs)
    for ci, r in enumerate(cells):
        body.append(rect(r, "url(#stipple)" if ci in alive else "#fff", 1.0, "#ddd", 0.3))
        if not small and ci in alive:
            body.append(text(X(r[0]) + 2, Y(r[3]) + 7, "%d" % ci, 5.5, "#888"))
    for k, p in enumerate(doc.get("slots") or []):
        col = SLOTCOL[k % len(SLOTCOL)]
        wb = ((doc.get("wbox_pad") or {}).get(snap.get("pad")) or doc.get("wbox") or {}).get(p)
        if wb:
            body.append(rect(wb, col, 0.05, col, 1.2, "6,3"))
            if not small:
                body.append(text(X(0.5 * (wb[0] + wb[1])), Y(wb[3]) + 9, p, 7, col, True, "middle"))
        bb = ((fz.get("union") or {}).get(p) or {}).get("bbox")
        if bb:
            body.append(rect(bb, "none", 0, col, 0.8, "2,2"))
    for w in fz.get("witness") or []:
        try:
            r = cells[int(w[1])]
        except Exception:
            continue
        body.append(rect(r, "#ffe082", 0.35, "#8d6e00", 0.7, "3,2"))
        if not small:
            body.append(text(X(0.5 * (r[0] + r[1])), Y(0.5 * (r[2] + r[3])) + 3, "%s:%s" % (w[0], ",".join(w[2])), 5, "#6d4c00", False, "middle"))
    roles = snap.get("roles") or {}
    pins = [(0.5 * (v["box"][0] + v["box"][1]), 0.5 * (v["box"][2] + v["box"][3])) for k, v in roles.items() if k.startswith("P")]
    for cx, cy in pins:
        body.append(poly(sq(cx, cy, 0.0), "#90caf9", 0.6, "#1565c0", 1.2))
    if doc.get("H_record"):
        body.append(rect(doc["H_record"], "none", 0, "#000", 0.7, "4,3"))
    ci_ = 0
    for name, v in roles.items():
        if name.startswith("P"):
            continue
        col = ROLECOL[ci_ % len(ROLECOL)]
        ci_ += 1
        for pc in v.get("pieces") or []:
            body.append(rect(pc, "none", 0, col, 0.25))
        body.append(rect(v["box"], "none", 0, col, 1.4 if not small else 0.8))
        if v.get("kprime"):
            body.append(poly(v["kprime"], col, 0.45, col, 0.8))
        pcs = v.get("pieces") or []
        big = max(pcs, key=lambda b: (b[1] - b[0]) * (b[3] - b[2]) * (b[5] - b[4] + 1e-9)) if pcs else v["box"]
        z, how = LV.admissible(big, pins)
        if z is None:
            cx, cy, th = 0.5 * (big[0] + big[1]), 0.5 * (big[2] + big[3]), math.radians(0.5 * (big[4] + big[5]))
            body.append(poly(sq(cx, cy, th), "none", 0, col, 0.8, "5,4"))
            how = "NO admissible pose found in the largest piece (dashed: schematic)"
        else:
            cx, cy, th = z
            body.append(poly(sq(cx, cy, th), "#00e5ff", 0.15, col, 1.0 if not small else 0.6))
            for tt in (big[4], big[5]):
                body.append(poly(sq(cx, cy, math.radians(tt)), "none", 0, col, 0.5, "3,2"))
        if not small:
            body.append(text(X(cx), Y(cy) + 4, name, 10, col, True, "middle"))
            body.append(text(X(cx), Y(cy) + 13, "%.1f deg in [%.1f, %.1f] of the largest piece; kept %s; %d pieces; %s" % (
                math.degrees(th), big[4], big[5], v.get("kept"), v.get("n_pieces", 0), how), 5.5, col, False, "middle"))
    return oy + S0 * S


def note_lines(doc, pad, snap):
    fz = snap.get("forcing") or {}
    fx = snap.get("fix") or {}
    L = [("PANEL = the node at the top of %s (pad %s): pins + H (seeded from A203's alive units) + %s after the seeded polygon + lonely clip FIXED POINT (nsub 4 / refine 2, %s passes, %s s)%s" % (
        snap.get("label"), pad, ", ".join(k for k in snap.get("roles", {}) if not k.startswith("P") and k != "H") or "no F role",
        fx.get("passes"), fx.get("seconds"), ("; lonely clip on %s" % fx.get("corners")) if fx.get("corners") else ""), 7, "#000", True)]
    L.append(("kept (of the record box; an F role of its seed) %s; K' areas %s; grey stipple = cells where a FREE meeter of some slot may still sit (this round's exact reach); yellow = the count's witness cells" % (
        {k: v for k, v in (fx.get("kept") or {}).items() if not k.startswith("P")}, {k: round(v, 3) for k, v in (fx.get("k_area") or {}).items() if not k.startswith("P")}), 6.5, "#333", False))
    if fz:
        L.append(("round %d: caps %s; forced H %s (all forced so far %s); forced roles %s; instantiated %s; changed %s" % (
            snap.get("round", 0), fz.get("caps"), fz.get("forced_H"), snap.get("forced_H"), fz.get("forced_role"), fz.get("instantiated"), fz.get("changed")), 6.5, "#333", False))
        for r, c in (fz.get("clips") or {}).items():
            L.append(("  reach clip on %s at %s: %d pieces, vol %.4g -> %.4g, box %s" % (r, c.get("slots"), c.get("n_pieces", 0), c.get("vol_before", 0), c.get("vol", 0), c.get("box_after")), 6.5, "#333", False))
    if snap.get("dead"):
        L.append(("DEAD: " + str(snap["dead"]), 7, "#c62828", True))
    L.append(("t = %s s into the pad's wall" % snap.get("t"), 6.5, "#555", False))
    return L


def side(doc, pad, body, x, y):
    d = doc["pads"].get(pad) or {}
    col = "#c62828" if d.get("verdict") == "DEAD" else "#2e7d32"
    L = [("%s  pad %s  A204 polygon-clip cascade: %s  (%s s, %d rounds)" % (doc["nid"], pad, d.get("verdict"), d.get("seconds"), len(d.get("round_times") or [])), 11, col, True)]
    if d.get("leaf"):
        s = str(d["leaf"])
        while s:
            L.append((s[:110], 8, col, False)); s = s[110:]
    st = d.get("start") or {}
    L.append(("start = %s (%s): H box %s, forced H %s, H units %s alive of %s; verdict %s" % (
        st.get("source"), st.get("file"), st.get("H_box"), st.get("forced_H"), st.get("n_units_alive"), st.get("n_units"), d.get("verifier")), 7, "#333", False))
    L.append(("round  fix s  passes  changed  kill   total s   kept", 8, "#000", True))
    for r in d.get("round_times") or []:
        L.append(("%-5s  %-5s  %-6s  %-7s  %-6s %-8s  %s" % (r.get("round"), r.get("fix"), (r.get("passes") or "-"), r.get("changed"), r.get("dead") or "-", r.get("seconds"),
                                                            {k: v for k, v in (r.get("kept") or {}).items() if not k.startswith("P")}), 7, "#333", False))
    if d.get("noroom"):
        L.append(("no-room leaf (A189): %s" % str(d["noroom"])[:200], 7, "#333", False))
    L.append(("window pending: %s; lam %s; rendered %s" % (d.get("window_pending"), d.get("lam"), time.strftime("%Y-%m-%d %H:%M:%S")), 7, "#555", False))
    yy = y
    for t, sz, c, b in L:
        t = str(t)
        while True:
            body.append(text(x, yy, t[:140], sz, c, b)); yy += sz + 4; t = t[140:]
            if not t:
                break
    return yy


def page_svg(doc):
    S = 96
    PW = int(S0 * S) + 24
    NH = 78
    body = [text(20, 22, "%s -- A204 polyclip204: the POLYGON-CLIP CASCADE to a fixed point on A203's survivor (pins + H seeded from A203's alive units + forced meeters as roles; polygon + lonely clip fixed point, exact reach clips ON THE PIECES, caps / Theorem FC / count; NO LP, NO tree)" % doc["nid"], 12, "#000", True),
            text(20, 36, "one panel per ROUND and pad (g1 = the page's window, then pad 0 = s0-only, WINDOW-PENDING); blue = pins; black = H (thin rects = its pieces, filled = certified K'); coloured = instantiated forced meeters; grey stipple = alive cells (never green); dashed colour = slot boxes + alive-union boxes; yellow = the count's witness", 8, "#444"),
            text(20, 48, "read-only from certs/polyclip204_%s.json; rendered %s" % (doc["nid"], time.strftime("%Y-%m-%d %H:%M:%S")), 8, "#444")]
    y = 64
    for pad in ("g1", "zero"):
        d = doc["pads"].get(pad)
        if not d:
            continue
        snaps = d.get("snapshots") or []
        ncol = 3
        nrow = max(1, (len(snaps) + ncol - 1) // ncol)
        side(doc, pad, body, 20 + ncol * PW + 10, y + 12)
        for k, snap in enumerate(snaps):
            ox, oy = 20 + (k % ncol) * PW, y + (k // ncol) * (S0 * S + NH + 12)
            panel(doc, snap, body, ox, oy, S)
            yy = oy + S0 * S + 10
            for t, sz, c, b in note_lines(doc, pad, snap):
                t = str(t)
                while True:
                    body.append(text(ox, yy, t[:95], sz, c, b)); yy += sz + 2; t = t[95:]
                    if not t:
                        break
        y += nrow * (S0 * S + NH + 12) + 30
    W = 20 + 3 * PW + 10 + 900
    return "\n".join(['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" font-family="Segoe UI, sans-serif" style="background:#fff">' % (W, y + 20), defs()] + body + ["</svg>"])


def render(doc):
    os.makedirs(OUTD, exist_ok=True)
    p = os.path.join(OUTD, "polyclip204_%s.svg" % doc["nid"])
    open(p, "w", encoding="utf-8").write(page_svg(doc))
    return p


def gallery():
    S = 52
    PW = int(S0 * S) + 16
    PH = PW + 34
    ncol = 6
    docs = []
    for f in sorted(glob.glob(os.path.join(CERTS, "polyclip204_*.json"))):
        try:
            docs.append(json.load(open(f, encoding="utf-8")))
        except Exception:
            continue
    body = [text(16, 20, "A204 polyclip204 -- the polygon-clip cascade to a fixed point over A203's survivors, one thumbnail per page (the last round at the g1 pad; red = DEAD at some pad); rendered %s" % time.strftime("%Y-%m-%d %H:%M:%S"), 12, "#000", True)]
    for k, doc in enumerate(docs):
        d = doc["pads"].get("g1") or {}
        snaps = d.get("snapshots") or []
        ox, oy = 16 + (k % ncol) * PW, 40 + (k // ncol) * PH
        if snaps:
            panel(doc, snaps[-1], body, ox, oy, S, small=True)
        dead = [(p, v) for p, v in doc["pads"].items() if v.get("verdict") == "DEAD"]
        body.append(text(ox, oy + S0 * S + 11, doc["nid"].replace("_interior", ""), 8, "#000", True))
        body.append(text(ox, oy + S0 * S + 21, ("DEAD pad %s: %s" % (dead[0][0], str(dead[0][1].get("clip") or "")[:22])) if dead else "ALIVE (%s)" % ", ".join("%s %dr" % (p, len(v.get("round_times") or [])) for p, v in doc["pads"].items()),
                         7, "#c62828" if dead else "#2e7d32"))
    nrow = max(1, (len(docs) + ncol - 1) // ncol)
    os.makedirs(OUTD, exist_ok=True)
    p = os.path.join(OUTD, "polyclip204_gallery.svg")
    open(p, "w", encoding="utf-8").write("\n".join(['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" font-family="Segoe UI, sans-serif" style="background:#fff">' % (ncol * PW + 32, 40 + nrow * PH), defs()] + body + ["</svg>"]))
    return p


if __name__ == "__main__":
    if sys.argv[1] == "gallery":
        print(gallery())
    else:
        print(render(json.load(open(os.path.join(CERTS, "polyclip204_%s.json" % sys.argv[1]), encoding="utf-8"))))
