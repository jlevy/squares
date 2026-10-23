#!/usr/bin/env python3
"""Sharp controls of the T-229 review (lane c-review-t229-math): a premise check.

For each certificate it builds mutants at exact contact and 1e-30 past it, writes each
in the source's certificate format, and decides each with this review's checker
(review_t229_check.py, both routes) and with the two maintained exact routes, reached
through the packet's own evand-cert adapter (devtools.upper_bound_reports
.parse_certificate) and called exactly as devtools.evand_arrangement_reports.run_case
calls them:

    exact_verify  legacy.exact_verify(kernel.to_witness(certificate, **profile))
    independent   legacy.independent.check_squares(legacy.corner_squares(certificate), side)

with the profile (witness prefix and claim limitations) of the packet's declaration.
It also runs the kernel's own sharp controls (kernel.run_sharp), at contact and past it.

Mutants, each from the source certificate:
    F0  side lowered by the least top-or-right clearance: a corner on the far wall
    F1  and by 1e-30 more: refused on a wall
    N0  every square moved toward the near wall of least clearance by that clearance
    N1  by the clearance + 1e-30: refused on a wall
    P0  one square of the least-gap pair (this review's route Z, every pair) moved along
        the pair's best separating axis toward the other by exactly the gap: a contact
    P1  by the gap + 1e-30: refused on an overlap
    R1  the last row dropped: refused by every reader
    R2  the first coordinate that has a terminating decimal expansion written as that exact
        decimal: a reader difference, not a control (this review's reader refuses
        decimals; the maintained reader reads them exactly)

The maintained routes' verdicts are theirs; this program adds the mutants and the
expectations, and decides no certificate itself.

Run from packing/ with the project interpreter and the worktree on PYTHONPATH:
    sharp_controls_t229.py OUT_DIR PACKET_NAME LABEL=N=CERT_OR_FACT [...]
"""

import json
import os
import sys
import time
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import review_t229_check as rc  # noqa: E402
from devtools import evand_arrangement_reports as kernel  # noqa: E402
from devtools import evand_exact_certificates as legacy  # noqa: E402
from devtools import upper_bound_reports as ubr  # noqa: E402

EPS = Fraction(1, 10**30)


def lit(v):
    v = Fraction(v)
    return f"{v.numerator}" if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def text_of(n, side, rows, comment="# mutant of the T-229 review"):
    lines = [comment, f"{n} {lit(side)}"]
    lines += [f"{lit(x)} {lit(y)} {lit(t)}" for (x, y, t) in rows]
    return "\n".join(lines) + "\n"


def basis(t):
    d = 1 + t * t
    return (1 - t * t) / d, 2 * t / d


def certificate_bytes(path):
    """The certificate in the source's format: the file itself, or, for the packet's derived
    fact, its squares written back as x y t with t = s / (1 + c) exactly, which the
    half-angle map inverts, so the source's file need not be retained to run the controls."""
    pk = rc.load(path)
    if pk["format"] == "evand-cert":
        return open(path, "rb").read()
    rows = []
    for r in pk["squares"]:
        c, s = Fraction(*r["rot"][1]), Fraction(*r["rot"][2])
        if c == -1:
            raise ValueError("a basis with c = -1 has no finite half-angle tangent")
        rows.append((Fraction(*r["x"]), Fraction(*r["y"]), s / (1 + c)))
    text = text_of(pk["n"], Fraction(*pk["side"]), rows,
                   comment="# the packet's derived fact, written back in the certificate format")
    back = rc.read_cert_text(text)
    if rc.same(back, pk)["same_packing_exactly"] is not True:
        raise ValueError("the fact does not convert back to an equal certificate")
    return text.encode("ascii")


def maintained(raw, n, profile):
    try:
        cert = ubr.parse_certificate(raw, n, "evand-cert")
    except Exception as exc:  # the adapter's refusal is the reader's verdict
        return {"reader": f"refused: {exc}"}, None
    out = {}
    t0 = time.process_time()
    first, _report = legacy.exact_verify(kernel.to_witness(cert, **profile))
    t1 = time.process_time()
    second = legacy.independent.check_squares(legacy.corner_squares(cert), cert.side)
    t2 = time.process_time()
    for route, v, sec in (("exact_verify", first, t1 - t0), ("independent", second, t2 - t1)):
        out[route] = {"passed": bool(v["verification_passed"]),
                      "least_wall": v["minimum_containment_clearance"],
                      "least_gap": v["minimum_best_pair_gap"],
                      "pairs": v["pairs_tested"],
                      "failures": [str(f) for f in v["failures"][:3]],
                      "cpu_seconds": round(sec, 3)}
    return out, cert


def mine(text):
    try:
        pk = rc.read_cert_text(text)
    except rc.ReadError as exc:
        return {"reader": f"refused: {exc}"}
    res = rc.decide(pk)
    z, c = res["route_Z"], res["route_C"]
    return {"route_Z": {"passed": z["accepted"], "least_wall": z["least_wall_clearance"],
                        "least_gap": z.get("least_gap"), "touching": z["touching"][:5],
                        "overlaps": z["overlaps"][:5], "wall_failures": z["wall_failures"][:5],
                        "wall_contacts": len(z["wall_contacts"]), "cpu_seconds": z["cpu_seconds"]},
            "route_C": {"passed": c["accepted"], "least_wall": c["least_wall_clearance"],
                        "touching": c["touching"][:5], "overlaps": c["overlaps"][:5],
                        "corners_outside": c["corners_outside"][:5],
                        "wall_contacts": c["wall_contacts"], "cpu_seconds": c["cpu_seconds"]},
            "routes_agree": res["routes_agree"]}


def verdicts(entry):
    """Every decider's accept/refuse on one mutant, None where its reader refused."""
    out = {}
    m = entry["review"]
    out["review_Z"] = None if "reader" in m else m["route_Z"]["passed"]
    out["review_C"] = None if "reader" in m else m["route_C"]["passed"]
    k = entry["maintained"]
    out["exact_verify"] = None if "reader" in k else k["exact_verify"]["passed"]
    out["independent"] = None if "reader" in k else k["independent"]["passed"]
    return out


def mutants(label, n, raw, check_entry):
    pk = rc.read_cert_text(raw.decode("ascii"))
    S = Fraction(*pk["side"])
    rows = [(Fraction(*r["x"]), Fraction(*r["y"]), Fraction(*r["rot"][1])) for r in pk["squares"]]
    ext = []
    for x, y, t in rows:
        c, s = basis(t)
        h = (abs(c) + abs(s)) / 2
        ext.append((x - h, y - h, S - x - h, S - y - h))
    far = min(min(e[2], e[3]) for e in ext)
    left = min(e[0] for e in ext)
    bottom = min(e[1] for e in ext)
    near, axis = (left, "x") if left <= bottom else (bottom, "y")
    z = check_entry["route_Z"]
    i, j = z["least_gap_pair"]
    gap = Fraction(z["least_gap"])
    name = z["least_gap_axis"]
    xi, yi, ti = rows[i - 1]
    xj, yj, tj = rows[j - 1]
    ci, si = basis(ti)
    cj, sj = basis(tj)
    nvec = {"u_i": (ci, si), "v_i": (-si, ci), "u_j": (cj, sj), "v_j": (-sj, cj)}[name]
    proj = nvec[0] * (xj - xi) + nvec[1] * (yj - yi)
    sign = 1 if proj > 0 else -1

    def moved_pair(step):
        out = list(rows)
        out[j - 1] = (xj - sign * step * nvec[0], yj - sign * step * nvec[1], tj)
        return out

    def shifted(step):
        if axis == "x":
            return [(x - step, y, t) for (x, y, t) in rows]
        return [(x, y - step, t) for (x, y, t) in rows]

    first = None
    for idx, (x, y, t) in enumerate(rows):
        for k, v in enumerate((x, y)):
            d = v.denominator
            while d % 2 == 0:
                d //= 2
            while d % 5 == 0:
                d //= 5
            if d == 1 and v.denominator > 1:
                first = (idx, k, v)
                break
        if first:
            break
    out = [
        ("F0", "accept", f"side lowered by the least top-or-right clearance {float(far):.6e}",
         text_of(n, S - far, rows)),
        ("F1", "refuse", "side lowered by that clearance + 1e-30", text_of(n, S - far - EPS, rows)),
        ("N0", "accept", f"every square moved by -{axis} {float(near):.6e}, the least near-wall clearance",
         text_of(n, S, shifted(near))),
        ("N1", "refuse", "by that clearance + 1e-30", text_of(n, S, shifted(near + EPS))),
        ("P0", "accept", f"square {j} moved toward square {i} along {name} by the gap {float(gap):.10e}",
         text_of(n, S, moved_pair(gap))),
        ("P1", "refuse", "by the gap + 1e-30", text_of(n, S, moved_pair(gap + EPS))),
        ("R1", "refuse", "the last row dropped", text_of(n, S, rows[:-1])),
    ]
    if first is not None:
        idx, k, v = first
        lines = text_of(n, S, rows).split("\n")
        toks = lines[2 + idx].split()
        q = v.denominator
        places = 0
        while 10**places % q:
            places += 1
        digits = abs(v.numerator) * (10**places // q)
        s = str(digits).rjust(places + 1, "0")
        dec = ("-" if v < 0 else "") + s[:-places] + "." + s[-places:]
        assert Fraction(dec) == v
        toks[k] = dec
        lines[2 + idx] = " ".join(toks)
        out.append(("R2", "reader difference",
                    f"square {idx + 1}'s {'xy'[k]} written as the exact decimal {dec}",
                    "\n".join(lines)))
    facts = {"far_clearance": lit(far), "near_clearance": lit(near), "near_axis": axis,
             "pair": [i, j], "gap": lit(gap), "axis": name, "moved_square": j}
    return out, facts


def main(argv):
    out_dir, packet_name, specs = argv[0], argv[1], argv[2:]
    packet = ubr.packet_path(packet_name)
    declaration = ubr.load_declaration(packet)
    profile = {"witness_prefix": declaration["witness_prefix"],
               "claim_limitations": declaration["claim_limitations"]}
    ok_all = True
    for spec in specs:
        label, n, path = spec.split("=", 2)
        n = int(n)
        raw = certificate_bytes(path)
        check_entry = rc.decide(rc.read_cert_text(raw.decode("ascii")))
        # The adapter's certificate equals the packet's own fact, as read_facts admits it.
        adapter = ubr.parse_certificate(raw, n, "evand-cert")
        fact = ubr.read_facts(packet, {n})[n]
        report = {"label": label, "n": n, "certificate": path,
                  "adapter_equals_packet_fact": adapter == fact, "mutants": [], "run_sharp": []}
        built, facts = mutants(label, n, raw, check_entry)
        report["construction"] = facts
        for code, expect, what, text in built:
            entry = {"mutant": code, "expect": expect, "what": what}
            entry["review"] = mine(text)
            entry["maintained"], _cert = maintained(text.encode("ascii"), n, profile)
            v = verdicts(entry)
            entry["verdicts"] = v
            if expect == "accept":
                ok = all(x is True for x in v.values())
            elif expect == "refuse":
                ok = all(x is not True for x in v.values())
            else:
                ok = True
            entry["as_expected"] = ok
            ok_all = ok_all and ok
            report["mutants"].append(entry)
            k = entry["maintained"]
            m = entry["review"]
            print(f"{label} {code} expect={expect} verdicts={v} ok={ok}")
            if "reader" not in k:
                print(f"    maintained: exact_verify wall={k['exact_verify']['least_wall'][:40]} "
                      f"gap={k['exact_verify']['least_gap'][:40]} fail={k['exact_verify']['failures'][:1]}; "
                      f"independent wall={k['independent']['least_wall'][:40]} "
                      f"gap={k['independent']['least_gap'][:40]} fail={k['independent']['failures'][:1]}")
            else:
                print(f"    maintained reader: {k['reader'][:100]}")
            if "reader" not in m:
                print(f"    review: Z wall={m['route_Z']['least_wall'][:40]} gap={str(m['route_Z']['least_gap'])[:40]} "
                      f"touch={m['route_Z']['touching']} overlaps={m['route_Z']['overlaps']} "
                      f"wallfail={m['route_Z']['wall_failures']}; C touch={m['route_C']['touching']} "
                      f"overlaps={m['route_C']['overlaps']} agree={m['routes_agree']}")
            else:
                print(f"    review reader: {m['reader'][:100]}")
        for control in kernel.SHARP_CONTROLS:
            for past in (False, True):
                try:
                    res = kernel.run_sharp(fact, control, past=past, **profile)
                except Exception as exc:  # recorded, and counted as not as expected
                    report["run_sharp"].append({"control": control, "past": past,
                                                "error": str(exc), "as_expected": False})
                    ok_all = False
                    print(f"{label} run_sharp {control} past={past} ERROR {exc}")
                    continue
                row = {"control": control, "past": past,
                       "result": {r: {"passed": v["passed"], "wall": str(v["wall"]), "gap": str(v["gap"])}
                                  for r, v in res.items()}}
                ok = all(v["passed"] is (not past) for v in res.values())
                row["as_expected"] = ok
                ok_all = ok_all and ok
                report["run_sharp"].append(row)
                print(f"{label} run_sharp {control} past={past} " + "; ".join(
                    f"{r}: passed={v['passed']} wall={str(v['wall'])[:30]} gap={str(v['gap'])[:30]}"
                    for r, v in res.items()) + f" ok={ok}")
        tag = label.replace("@", "-n").replace(":", "-")
        with open(os.path.join(out_dir, f"out-controls-{tag}.json"), "w") as fh:
            json.dump(report, fh, indent=1)
    print("all as expected" if ok_all else "NOT ALL AS EXPECTED")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
