"""Re-evaluation of the census-to-capture link facts of one sq19 capture state.

For state S (3435, 3438 or 3442) the retained modules assert by `native_decide`
  Sq19.Capture.S<k>.cells_ok      the state's cells are the census cells of its roster, shifted by -sigma;
  Sq19.Capture.S<k>.mask_ok       the x reflection maps the roster into census mask k;
  Sq19.Capture.S<k>.width_checked every base angle window is at least pi/2 wide;
  Sq19.Capture.S<k>.tile_checked  the pieces tile owner 12's window, in order.
Their data (`rosterNat`, `cells`, `sigma`, `baseList`, `pieceLo`, `pieceHi`) is in
the release archive `sq19-generated-S<k>.tar.xz`, not retained here. This program
reads the extracted Common.lean and each piece's P<i>Tab.lean (captured piece) or
P<i>Data.lean (excluded piece) of one state, and the retained
census cells, symmetry table and census masks, and decides the four facts in
exact rational arithmetic. It also checks the extracted files against
expected/generated-sources.sha256.

    python -I check_capture_link.py SQ19_DIR ARCHIVE_DIR STATE [--json OUT]

ARCHIVE_DIR holds `Sq19Lean/Capture/S<k>/...` as the archive extracts it.
Standard library only.
"""

import argparse
import hashlib
import json
import re
import sys
from fractions import Fraction as F

HALF_PI_UPPER = F(314159265358979323847, 200000000000000000000)
NUM = r"-?\d+(?:/\d+)?"


def cells_table(text):
    i = text.index("def vertices")
    j = text.index("![", i) + 2
    out, depth, k = [], 0, j
    buf = []
    while True:
        ch = text[k]
        if ch == "[":
            depth += 1
        elif ch == "]":
            if depth == 0:
                break
            depth -= 1
        buf.append(ch)
        k += 1
    for line in "".join(buf).splitlines():
        line = line.split("--")[0].strip()
        if line.startswith("["):
            out.append([(F(a.replace(" ", "")), F(b.replace(" ", ""))) for a, b in re.findall(r"\(([^,()]+),\s*([^()]+?)\)", line)])
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("sq19")
    ap.add_argument("archive")
    ap.add_argument("state", type=int, choices=(3435, 3438, 3442))
    ap.add_argument("--json")
    a = ap.parse_args()
    k = a.state
    S = a.sq19 + "/Sq19Lean/"
    D = f"{a.archive}/Sq19Lean/Capture/S{k}/"
    listed = dict(reversed(line.split("  ", 1)) for line in
                  open(a.sq19 + "/expected/generated-sources.sha256", encoding="utf-8").read().splitlines() if line)
    listed = {p.strip(): h for p, h in listed.items()}
    state_txt = open(S + f"Capture/S{k}/State.lean", encoding="utf-8").read()
    pieces = sorted(int(x) for x in re.findall(rf"import Sq19Lean\.Capture\.S{k}\.P(\d+)\n", state_txt))
    def piece_file(i):
        tab = f"P{i}Tab.lean"
        return tab if f"Sq19Lean/Capture/S{k}/{tab}" in listed else f"P{i}Data.lean"

    files = ["Common.lean"] + [piece_file(i) for i in pieces]
    digests_ok = True
    for f in files:
        h = hashlib.sha256(open(D + f, "rb").read()).hexdigest()
        digests_ok &= listed.get(f"Sq19Lean/Capture/S{k}/{f}") == h
    common = open(D + "Common.lean", encoding="utf-8").read()
    sigma = F(re.search(rf"def sigma : Rat := \(({NUM}) : Rat\)", common).group(1))
    roster = [int(x) for x in re.search(r"def rosterNat : List Nat := \[([0-9, ]+)\]", common).group(1).split(",")]
    cells_body = common.split("def cells : List (List (Rat × Rat)) := [", 1)[1].split("\n/--", 1)[0]
    cells = [[(F(x), F(y)) for x, y in re.findall(rf"\(\(({NUM}) : Rat\), \(({NUM}) : Rat\)\)", line)]
             for line in cells_body.splitlines() if line.strip().startswith("[")]
    base_body = common.split("def baseList : List (Rat × Rat) := [", 1)[1].split("]", 1)[0]
    base = [(F(x), F(y)) for x, y in re.findall(rf"\(\(({NUM}) : Rat\), \(({NUM}) : Rat\)\)", base_body)]
    split_owner = int(re.search(r"def splitOwner : Nat := (\d+)", common).group(1))
    windows = []
    for i in pieces:
        tab = open(D + piece_file(i), encoding="utf-8").read()
        lo = F(re.search(rf"def pieceLo : Rat := \(({NUM}) : Rat\)", tab).group(1))
        hi = F(re.search(rf"def pieceHi : Rat := \(({NUM}) : Rat\)", tab).group(1))
        windows.append((lo, hi))
    V = cells_table(open(S + "Census/Cells.lean", encoding="utf-8").read())
    orbit = open(S + "Cover/OrbitData.lean", encoding="utf-8").read()
    perm1 = [int(x) for x in re.findall(r"\[([0-9, ]+)\]", orbit[orbit.index("def permRows"):])[1].split(",")]
    census = [int(w, 16) for w in orbit.split('def censusHex : String := "', 1)[1].split('"', 1)[0].split()]
    r = [x % 25 for x in roster]
    res = {
        "digests_match_expected": digests_ok,
        "roster_injective": len(roster) == 19 and len(set(r)) == 19,
        "cells_ok": len(cells) == 19 and all(cells[j] == [(x - sigma, y - sigma) for x, y in V[r[j]]] for j in range(19)),
        "mask_ok": all(census[k] >> perm1[r[j]] & 1 for j in range(19)),
        "mask_is_exactly_the_reflected_roster": sum(1 << perm1[c] for c in r) == census[k],
        "width_checked": len(base) == 19 and all(HALF_PI_UPPER <= hi - lo for lo, hi in base),
        "tile_checked": split_owner == 12 and windows[0][0] == base[12][0] and windows[-1][1] == base[12][1]
        and all(windows[i][1] == windows[i + 1][0] for i in range(len(windows) - 1)),
    }
    res["pieces"] = [[str(lo), str(hi)] for lo, hi in windows]
    ok = all(v for key, v in res.items() if key != "pieces")
    for key, v in res.items():
        if key != "pieces":
            print(f"{'PASS' if v else 'FAIL'}  S{k} {key}")
    print(f"S{k}: {len(pieces)} piece(s) of owner 12's window, in degrees "
          f"{[(round(float(lo) * 180 / 3.141592653589793, 3), round(float(hi) * 180 / 3.141592653589793, 3)) for lo, hi in windows]}")
    print("PASS" if ok else "FAIL")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(res | {"all_checks_pass": ok}, f, indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
