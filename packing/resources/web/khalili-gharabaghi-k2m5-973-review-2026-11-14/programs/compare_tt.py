"""Compare a run_tt.py output made here with the source's, chart by chart (review of #973, L144).

usage: python -I compare_tt.py MINE THEIRS
Per chart: ok, cells, fails, worst and the tile string must be equal (secs ignored); the corner-zone lines
("C_u corners", "... corners" and the CORNER / WCORNER detail lines) must be equal; the last line must be equal.
"""
import json
import sys


def read(path):
    charts, corners, last = {}, [], ""
    for ln in open(path):
        s = ln.strip()
        if not s:
            continue
        last = s
        if s.startswith("{"):
            d = json.loads(s)
            if "fails" in d:
                charts[d["chart"]] = {k: d.get(k) for k in ("tile", "h0", "ok", "cells", "fails", "worst")}
            else:
                corners.append({k: v for k, v in d.items() if k != "secs"})
        elif s.startswith(("CORNER", "WCORNER")) or s.startswith(".. {"):
            corners.append(s)
    return charts, corners, last


a, b = read(sys.argv[1]), read(sys.argv[2])
diff = {c: [a[0].get(c), b[0].get(c)] for c in set(a[0]) | set(b[0]) if a[0].get(c) != b[0].get(c)}
res = dict(mine=sys.argv[1].split("/")[-1], charts=len(a[0]), charts_theirs=len(b[0]), chart_diffs=diff,
           corner_lines_equal=a[1] == b[1], corner_lines=[len(a[1]), len(b[1])], last=[a[2], b[2]],
           identical=not diff and a[1] == b[1] and a[2] == b[2])
print(json.dumps(res))
