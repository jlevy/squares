"""A203 -- the CSP panel and the page: A202's stage-0 panel (fig203.panel0 / side0) per pad, plus, per pad, the CSP
panel: H's box magnified with its UNITS (sub-rect x tilt bin at depth ud) -- grey = alive after the mutual clip,
red 'M' = dead by the mutual clip (no compatible option of a slot some free square must meet), white = never alive
(pins / walls / H's forced-slot clip); the dead options lettered by rule (H = H-consistency, F = after settle) with
their numbers; the milliseconds per rule.   python fig203b.py <nid>  ->  docs/residue_map/csp203_<nid>.svg"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fig203 as F                                             # noqa: E402

text, defs, S0, RULECOL = F.text, F.defs, F.S0, F.RULECOL


def csp_panel(cert, body, ox, oy, W=260):
    rounds = cert.get("csp") or []
    if not rounds:
        body.append(text(ox, oy + 12, "no CSP record", 8, "#900"))
        return oy + 20
    last = rounds[-1]
    ur = last.get("unit_rects") or {}
    alive = {tuple(u) for u in last.get("unit_alive") or []}
    dead_units = {tuple(d["unit"]): d["rule"] for r in rounds for d in (r.get("dead_units") or [])}
    keys = [tuple(int(v) for v in k.strip("[]").split(",")) for k in ur]
    if not keys:
        body.append(text(ox, oy + 12, "no H units", 8, "#900"))
        return oy + 20
    nx = max(k[0] for k in keys) + 1
    ny = max(k[1] for k in keys) + 1
    nb = max(k[2] for k in keys) + 1
    hb = cert.get("H_record") or [0, 1, 0, 1]
    cw, ch = W / nx, W / ny
    body.append(text(ox, oy - 4, "CSP: H's box %s x tilt %.1f-%.1f deg as %d x %d sub-rects x %d tilt bins (strips, left = low tilt); grey alive, red M = mutual clip, white = never alive" % (
        [round(v, 3) for v in hb[:4]], hb[4], hb[5], nx, ny, nb), 7, "#333"))
    body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#fff" stroke="#000" stroke-width="1"/>' % (ox, oy, W, W))
    all_units = set(keys) | set(dead_units)
    for (i, j, b) in sorted(all_units):
        x = ox + i * cw + b * (cw / nb)
        y = oy + (ny - 1 - j) * ch
        if (i, j, b) in alive:
            body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="url(#stipple)" stroke="#bbb" stroke-width="0.2"/>' % (x, y, cw / nb, ch))
        elif (i, j, b) in dead_units:
            body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#ffcdd2" stroke="#c62828" stroke-width="0.3"/>' % (x, y, cw / nb, ch))
            body.append(text(x + cw / nb / 2, y + ch / 2 + 2, "M", 5, "#c62828", True, "middle"))
    for i in range(nx + 1):
        body.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#888" stroke-width="0.5"/>' % (ox + i * cw, oy, ox + i * cw, oy + W))
    for j in range(ny + 1):
        body.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#888" stroke-width="0.5"/>' % (ox, oy + j * ch, ox + W, oy + j * ch))
    yy = oy + W + 14
    L = []
    for r in rounds:
        ms = r.get("ms") or {}
        st_ = r.get("settle") or {}
        L.append(("round %d: %d H units (%d pieces) -> %d alive; %d options (%d pieces); mutual clip %s in %d iteration(s); dead options %d" % (
            r.get("round", 0), r["n_units"], r.get("n_hpieces", 0), r["alive_units"], r["n_opts"], r["n_opt_pieces"], r.get("dead_unit_count"), r.get("iterations", 0), len(r.get("dead_opts") or [])), 7.5, "#000", True))
        L.append(("  ms: build %s | masks %s (rule S: %s node tests, %s leaf pairs in numpy blocks, %s block cache hits) | settle %s | clip %s" % (
            ms.get("build"), ms.get("masks"), r.get("sat_tests"), r.get("leaf_pairs"), r.get("block_hits"), ms.get("settle"), ms.get("clip_total")), 7, "#333", False))
        if st_:
            L.append(("  settle kills %s; rule ms %s; %d options refined, %d died" % (st_.get("kills"), st_.get("rule_ms"), len(st_.get("options") or []), st_.get("n_dead_options", 0)), 7, "#333", False))
        for d in r.get("dead_opts") or []:
            L.append(("  %s  cell %d %s: hull %s, %d pieces%s" % (d["rule"], d["cell"], "+".join(d["S"]), d.get("hull"), d.get("n_pieces", 0),
                                                            (", %d pairs refined -> %d dead in %s ms" % (d["pairs"], d["pairs_dead"], d["ms"])) if d["rule"] == "F" else
                                                            (", nearest unit at max distance %s" % d.get("nearest_maxdist"))), 7, RULECOL.get(d["rule"], "#c00"), False))
    L.append(("H = no piece of the row is rule-S compatible with any alive H piece; F = the same after the settle refinement; M = H unit with no compatible option of a slot a free square must meet", 6.5, "#555", False))
    for t, sz, c, b in L:
        t = str(t)
        while True:
            body.append(text(ox, yy, t[:150], sz, c, b)); yy += sz + 3; t = t[150:]
            if not t:
                break
    return yy


def page_svg(nid, certs):
    S = 118
    PW = int(S0 * S) + 20
    TW = 600
    CW = 700
    body = [text(20, 22, "%s -- A203 csp203: STAGE 0 (A202's closed-form layer) + the piece-level CSP (H-consistency, the mutual clip, the settle, the H-mask count), <= 30 s per pad, drawn first" % nid, 13, "#000", True),
            text(20, 38, "grey stipple = sub-rects where some forced slot's meeter may still sit; white + letter = dead (P pins, W walls, C CN vs H, M tilt-SAT vs H, L chord row, R reach / A161 miss, H / F = H-consistency); "
                 "red boxes + letter = dead option rows (H / F); dashed colour = slot unit + its alive-union box; blue = pins; black = H with a hypothesis square at an admissible pose; yellow = the count's witness.", 8, "#444"),
            text(20, 50, "read-only from certs/csp203_*.json; rendered %s" % time.strftime("%Y-%m-%d %H:%M:%S"), 8, "#444")]
    y0 = 70
    ybot = y0
    for k, c in enumerate(certs):
        ox = 20 + k * (PW + TW + CW)
        body.append(text(ox, y0 - 6, "PANEL stage 0 + CSP / pad %s: %s" % (c.get("pad"), c["_file"]), 9, "#000", True))
        yb = F.panel0(c, body, ox, y0, S)
        yt = F.side0(c, body, ox + PW + 10, y0 + 12)
        yc = csp_panel(c, body, ox + PW + TW + 20, y0 + 12)
        ybot = max(ybot, yb, yt, yc)
    W = len(certs) * (PW + TW + CW) + 40
    return "\n".join(['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" font-family="Segoe UI, sans-serif" style="background:#fff">' % (W, ybot + 20), defs()] + body + ["</svg>"])


def render(nid):
    certs = F.load(nid)
    if not certs:
        return None
    os.makedirs(F.OUTD, exist_ok=True)
    p = os.path.join(F.OUTD, "csp203_%s.svg" % nid)
    open(p, "w", encoding="utf-8").write(page_svg(nid, certs))
    return p


if __name__ == "__main__":
    print(render(sys.argv[1]))
