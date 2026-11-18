"""Written after the checker freeze (lane r1021-1118): adapters for the predecessors' layouts.

Why it exists.  #1023 merged at 05:46:46Z on 18 November, before this lane's checker
freeze (pushed 06:08:53Z), but the lane learned it only after the freeze; T-320 and
T-321 then became the houses at 268 and 270, and the brief asks for them as well as
T-289 and T-283.  The frozen reader refuses two layouts these predecessors use:

- single-quoted corner scalars: '0' where a corner lies on a wall, in T-289's and
  T-283's files (3 and 2 lines), and every scalar of Polkovskyi's Witness/v2 files;
  the frozen rule demanding plain scalars was too strict, since '0' and 0 are the same
  scalar text (finding F3);
- Polkovskyi's evand-cert text files: a comment line, "n side", then one line
  "x y r" per square, r a rational whose meaning this program does not assume.

This program removes the quotes from side and corner lines only, checks with
PyYAML's loader that every value is unchanged, and reads each .cert line by the
frozen scalar grammar.  It tries four readings of r (r = tan(t/2), r = cot(t/2),
and each mirrored) and keeps the one under which the frozen twin test pairs every
square exactly with the Witness/v2 file's corners.  Every decision and measurement
is then made by the frozen modules unchanged (r1021_check, r1021_contract,
r1021_identity, r1021_measure's functions, r1021_controls' writer).

Usage: python -I -B r1021_post.py SRC_DIR T289 T283 POLK_DIR WIT0_DIR WIT1_DIR OUT_DIR
       python -I -B r1021_post.py unquote IN OUT
       python -I -B r1021_post.py cert CERT UNQUOTED_WITNESS OUT_FORM_J

SRC_DIR holds de Winter's four files; T289 and T283 the houses' certificates;
POLK_DIR n268.cert, n270.cert, polk-n-268.yaml and polk-n-270.yaml (#1009's files as
main retains them); WIT0_DIR and WIT1_DIR the house witnesses n-268.yaml and
n-270.yaml on main at 0f191a2d23 and at 86284ec203.  It writes the converted files and
post-*.json receipts to OUT_DIR.
"""

from __future__ import annotations

import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # this packet's programs/, run with -I

import hashlib
import json
import re
import time
from fractions import Fraction

import yaml

import r1021_check as chk
import r1021_contract as con
import r1021_controls as ctl
import r1021_geom as geom
import r1021_identity as ident
import r1021_measure as msr
import r1021_read as rd
from r1021_fmt import ceil_places, floor_places, sci

QUOTED = re.compile(r"^(?P<pre>  side: |    - - |      - )'(?P<v>-?[0-9]+(?:/[0-9]+)?)'$")


def unquote(raw: bytes) -> tuple[bytes, int, bool]:
    """Unquote side and corner scalars; return the bytes, the lines changed, and whether
    PyYAML reads every side and corner value of the two files as the same text."""
    lines = raw.decode("ascii").split("\n")
    changed = 0
    out = []
    for ln in lines:
        m = QUOTED.match(ln)
        if m:
            out.append(m.group("pre") + m.group("v"))
            changed += 1
        else:
            out.append(ln)
    new = "\n".join(out).encode("ascii")
    a = yaml.load(raw, Loader=yaml.CSafeLoader)["witness"]
    b = yaml.load(new, Loader=yaml.CSafeLoader)["witness"]
    same = str(a["side"]) == str(b["side"]) and a["n"] == b["n"] and len(a["squares"]) == len(b["squares"]) and all(
        [[str(v) for v in pt] for pt in sa["corners"]] == [[str(v) for v in pt] for pt in sb["corners"]]
        and str(sa["id"]) == str(sb["id"])
        for sa, sb in zip(a["squares"], b["squares"], strict=True))
    return new, changed, same


def read_cert(raw: bytes):
    lines = raw.decode("ascii").rstrip("\n").split("\n")
    if not lines[0].startswith("#"):
        msg = "cert: no comment line"
        raise rd.ReadError(msg)
    n_text, side_text = lines[1].split(" ")
    n = int(n_text)
    flags: list = []
    side = rd.scalar(side_text, "cert side", flags)
    rows = []
    for k, ln in enumerate(lines[2:], start=1):
        toks = ln.split(" ")
        if len(toks) != 3:
            msg = f"cert: line of square {k} has {len(toks)} tokens"
            raise rd.ReadError(msg)
        rows.append(tuple(rd.scalar(t, f"cert square {k}[{m}]", flags) for m, t in enumerate(toks)))
    if len(rows) != n:
        msg = f"cert: {len(rows)} squares for n = {n}"
        raise rd.ReadError(msg)
    return n, side, side_text, rows, flags


def readings(r: Fraction):
    out = {}
    out["tan-half"] = ((1 - r * r) / (1 + r * r), 2 * r / (1 + r * r))
    out["cot-half"] = ((r * r - 1) / (r * r + 1), 2 * r / (r * r + 1))
    out["tan-half mirrored"] = (out["tan-half"][0], -out["tan-half"][1])
    out["cot-half mirrored"] = (out["cot-half"][0], -out["cot-half"][1])
    return out


def cert_to_form_j(raw_cert: bytes, witness_squares):
    n, side, side_text, rows, flags = read_cert(raw_cert)
    tally = {}
    poses_by = {}
    for name in ("tan-half", "cot-half", "tan-half mirrored", "cot-half mirrored"):
        poses = []
        for x, y, r in rows:
            c, s = readings(r)[name]
            poses.append((x, y, c, s))
        fails = sum(1 for q, p in zip(witness_squares, poses, strict=True) if geom.twin_match(q, p) is None)
        tally[name] = fails
        poses_by[name] = poses
    good = [name for name, f in tally.items() if f == 0]
    if not good:
        return None, {"readings_twin_failures": tally, "flags": len(flags)}
    poses = poses_by[good[0]]
    raw_j = ctl.write_form_j(n, side_text, ctl.rows_text(poses))
    return raw_j, {"reading": good[0], "readings_twin_failures": tally, "flags": len(flags), "n": n,
                   "side_text": side_text}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write(path: str, raw: bytes) -> None:
    with open(path, "wb") as f:
        f.write(raw)


def step(pred_label, pred_poses, pred_side, pred_c, succ_label, succ_poses, succ_side) -> dict:
    od = con.option_d(pred_side, pred_c, succ_side)
    t0 = time.process_time()
    idm = ident.measure(pred_poses, pred_side, succ_poses, succ_side)
    return {
        "step": f"{pred_label} -> {succ_label}",
        "gain": sci(od["gain"], 10),
        "predecessor_margin": sci(od["predecessor_margin"], 10),
        "gain_over_margin": sci(od["gain_over_margin"], 8) if od["gain_over_margin"] is not None else None,
        "successor_below_shrunk_predecessor_by": sci(od["successor_below_shrunk_predecessor_by"], 10),
        "new_under_option_d": od["new_under_option_d"],
        "prints_12": [ceil_places(pred_side, 12), ceil_places(pred_c["shrunk_side"], 12), ceil_places(succ_side, 12)],
        "floors_16": [floor_places(pred_side, 16), floor_places(pred_c["shrunk_side"], 16), floor_places(succ_side, 16)],
        "identity": {**idm, "cpu": round(time.process_time() - t0, 2)},
    }


def main(argv: list[str]) -> int:
    if len(argv) == 3 and argv[0] == "unquote":  # r1021_post.py unquote IN OUT
        raw = open(argv[1], "rb").read()
        new, changed, same = unquote(raw)
        write(argv[2], new)
        print(argv[1], "lines unquoted", changed, "values unchanged", same, "sha256", sha(new))
        return 0 if same else 1
    if len(argv) == 4 and argv[0] == "cert":  # r1021_post.py cert CERT UNQUOTED_WITNESS OUT_FORM_J
        fw = rd.read_corners(open(argv[2], "rb").read(), "square-k", "form C")
        raw_j, info = cert_to_form_j(open(argv[1], "rb").read(), fw["squares"])
        print(argv[1], info)
        if raw_j is None:
            return 1
        write(argv[3], raw_j)
        return 0
    if len(argv) != 7:
        print(__doc__)
        return 2
    src, t289, t283, polk, wit0, wit1, out = argv
    t_all = time.process_time()
    rec: dict = {"written": "after the checker freeze", "conversions": {}, "checks": {}, "counts": {}}
    for n, house_path, house_id, polk_id in ((268, t289, "T-289", "T-320"), (270, t283, "T-283", "T-321")):
        # de Winter's report, read by the frozen readers as published
        raw_j = open(_os.path.join(src, f"n{n}_exact.json"), "rb").read()
        raw_c = open(_os.path.join(src, f"n{n}_witness.yaml"), "rb").read()
        fj = rd.read_form_j(raw_j)
        succ, s_succ = fj["rows"], fj["side"]
        # the Ozden house: its quoted '0' scalars unquoted, then the frozen check
        raw_h = open(house_path, "rb").read()
        raw_hu, changed, same = unquote(raw_h)
        write(_os.path.join(out, f"unquoted-{house_id}.yaml"), raw_hu)
        rec["conversions"][house_id] = {"source_sha256": sha(raw_h), "unquoted_sha256": sha(raw_hu),
                                        "lines_unquoted": changed, "values_unchanged": same}
        res_h = chk.check_house(raw_hu)
        rec["checks"][house_id] = {k: v for k, v in res_h.items() if not k.startswith("_")}
        house = res_h["_poses"]
        s_house = rd.read_corners(raw_hu, "int", "house file")["side"]
        # the Polkovskyi house: the witness unquoted, the .cert read as form J by the reading that pairs every square
        raw_pw = open(_os.path.join(polk, f"polk-n-{n}.yaml"), "rb").read()
        raw_pwu, changed_p, same_p = unquote(raw_pw)
        fpw = rd.read_corners(raw_pwu, "square-k", "form C")
        raw_cert = open(_os.path.join(polk, f"n{n}.cert"), "rb").read()
        raw_pj, info = cert_to_form_j(raw_cert, fpw["squares"])
        rec["conversions"][polk_id] = {"witness_sha256": sha(raw_pw), "witness_unquoted_sha256": sha(raw_pwu),
                                       "lines_unquoted": changed_p, "values_unchanged": same_p,
                                       "cert_sha256": sha(raw_cert), **info,
                                       "form_j_sha256": sha(raw_pj) if raw_pj else None}
        write(_os.path.join(out, f"unquoted-{polk_id}.yaml"), raw_pwu)
        if raw_pj is None:
            rec["checks"][polk_id] = {"verdict": "NOT CONVERTED"}
            continue
        write(_os.path.join(out, f"form-j-{polk_id}.json"), raw_pj)
        res_p = chk.check_report(raw_pj, raw_pwu)
        rec["checks"][polk_id] = {k: v for k, v in res_p.items() if not k.startswith("_")}
        polk_poses = rd.read_form_j(raw_pj)["rows"]
        s_polk = rd.read_form_j(raw_pj)["side"]
        # contraction margins, each shrunk packing decided by both methods (frozen)
        entry: dict = {"sides": {"#10%d" % (21 if n == 268 else 22): msr.print_facts(s_succ), house_id: msr.print_facts(s_house),
                                 polk_id: msr.print_facts(s_polk)}}
        f_s, c_s = msr.contraction_facts(succ, s_succ, "successor")
        f_h, c_h = msr.contraction_facts(house, s_house, house_id)
        f_p, c_p = msr.contraction_facts(polk_poses, s_polk, polk_id)
        entry["contraction"] = {"successor": f_s, house_id: f_h, polk_id: f_p}
        succ_label = "#1021" if n == 268 else "#1022"
        entry["steps"] = [
            step(polk_id, polk_poses, s_polk, c_p, succ_label, succ, s_succ),
            step(house_id, house, s_house, c_h, succ_label, succ, s_succ),
            step(house_id, house, s_house, c_h, polk_id, polk_poses, s_polk),
        ]
        entry["house_witness_on_main_before_1023"] = msr.house_witness_compare(house, s_house,
                                                                                open(_os.path.join(wit0, f"n-{n}.yaml"), "rb").read())
        entry["house_witness_on_main_after_1023"] = msr.house_witness_compare(polk_poses, s_polk,
                                                                               open(_os.path.join(wit1, f"n-{n}.yaml"), "rb").read())
        rec["counts"][str(n)] = entry
        for s_ in entry["steps"]:
            print(n, s_["step"], "gain", s_["gain"], "margin", s_["predecessor_margin"], "ratio", s_["gain_over_margin"],
                  "new", s_["new_under_option_d"], "one-to-one", s_["identity"]["one_to_one_under"][:3])
    rec["cpu_total"] = round(time.process_time() - t_all, 1)
    with open(_os.path.join(out, "post-measure.json"), "w") as f:
        json.dump(rec, f, indent=1)
        f.write("\n")
    for k, v in rec["checks"].items():
        print(k, v.get("verdict"), v.get("reason", ""))
    return 0


if __name__ == "__main__":
    _sys.exit(main(_sys.argv[1:]))
