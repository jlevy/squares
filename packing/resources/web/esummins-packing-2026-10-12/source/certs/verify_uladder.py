#!/usr/bin/env python3
"""verify_uladder.py -- exact-rational checker for `u-ladder-manifest-v1` files (A80).

Stdlib only (fractions, json, os, sys).  A manifest packages one rung of the U ladder
(docs/proofs/u_ladder.md): the U_1 re-insertion certificates at core slack delta (one per removed
square i: case-lp-certificate-v1 files, verified by the frozen verify_case.py -- their PASS
reports are part of the package) together with the pocket zones, and this checker re-derives
EVERYTHING the composition consumes from those files:

  (1) structure: each certificate is the tight Trump certificate's poses minus square i, cores
      at half-side a = 1/2 - delta and the tight tilt, budget 1, NO atoms (total 0), exactly one
      NO-family = the (hw_c, hw_t)-box around the tight pose of square i (upright squares carry
      the t~1 branch [1 - 2hw_t/(1+hw_t), 1], theorem_u.md sect. 3);
  (2) the frozen verifier's report for that file says PASS at depth >= 60, strict margin 0,
      unscaled weights, zero witnesses, same side, same file name;
  (3) Lemma B / Lemma U-C side conditions, exact: lambda = s''/s-hat from the A22 enclosure
      (z0, r_0), core containment margin 1/2 - a(1 + dtheta) - offset > 0 for every core;
  (4) the pocket zone pulled back through lambda lands in the basin box: dev_c = hw_c + drift +
      sqrt2*rho_B < r_c^B and dev_t = hw_t (+ hw_t^3 on the t~1 branch) + tilt slop < r_t^B for
      each basin the manifest names (Lean/A36 uniform 3/2000; A36 per coordinate; A40 per
      coordinate -- the checker knows these three by name);
  (5) the counting-row radius: the largest r with (U-C) r + sqrt2*lambda*(r + rho_B) + slop <= delta
      (docs/proofs/u_ladder.md Lemma U-C), reported per manifest.

Imported trust (stated, not re-derived): the A22 enclosure (z0, r_0 = 1e-50) and A65's two
80-digit tilt evaluations |2 atan(t_r) - theta_0| <= 1e-13, |tan(theta_0/2) - t_r| <= 1e-13
(theorem_u.md sect. 2; same tier as A22's own interval arithmetic) -- carried as manifest
fields dtheta_tilt_bound / dt_tilt_bound.  sqrt2 is bounded above by 14143/10000 (exact:
14143^2 = 200024449 > 2e8).

Corruption gates (each MUST make the checker fail):
    core     shift one core centre by 1e-6
    slack    replace one core's half-side by 1/2 - delta/2 (wrong slack)
    zone     widen one pocket zone 10x (must leave the Lean basin)
    report   flip one report's result to FAIL
    side     change one certificate's side by 1e-9

Usage:  python verify_uladder.py manifest.json [--corrupt {core,slack,zone,report,side}] [--quiet]
Exit 0 = PASS, 1 = FAIL, 2 = malformed.
"""
import json, os, sys
from fractions import Fraction as F

SQRT2_UB = F(14143, 10000)
BASINS = {"lean_A36_uniform": (F(3, 2000), F(3, 2000)),
          "A36_percoord": (F(37, 10000), F(37, 20000)),
          "A40_percoord": (F(5794, 884563), F(5794, 2 * 884563))}


class Fail(Exception):
    pass


def chk(cond, msg):
    if not cond:
        raise Fail(msg)


def load(path, base):
    return json.load(open(path if os.path.isabs(path) else os.path.join(base, path)))


def verify(mpath, corrupt=None, quiet=False):
    base = os.path.dirname(os.path.abspath(mpath))
    m = json.load(open(mpath))
    chk(m.get("format") == "u-ladder-manifest-v1", "bad manifest format")
    delta = F(m["delta"])
    rho_b = F(m.get("rho_B", "0"))
    chk(0 < delta < F(1, 2), "delta out of range")
    tight = load(m["tight_certificate"], base)
    kraw = load(m["krawczyk"], base)
    s2 = F(tight["side"])
    chk(F(m["s2"]) == s2, "manifest s2 != tight certificate side")
    sq = [{k: F(q[k]) for k in ("cx", "cy", "t")} for q in tight["squares"]]
    chk(len(sq) == 11, "tight certificate must have 11 squares")
    z0 = [F(x) for x in kraw["z0"]]
    r0 = F(kraw["r_0"])
    chk(r0 <= F(1, 10**50), "A22 enclosure radius unexpected")
    s_lo, s_hi = z0[33] - r0, z0[33] + r0
    chk(s_hi < s2, "s'' must lie strictly above the s-hat enclosure")
    lam_lo, lam_hi = s2 / s_hi, s2 / s_lo
    dth_tilt = F(m["dtheta_tilt_bound"]) + 2 * r0       # imported trust items (A65 ledger)
    dt_tilt = F(m["dt_tilt_bound"])
    dth_up = max(abs(z0[3 * j + 2]) for j in range(6)) + r0
    a_core = F(1, 2) - delta
    zones = {int(i): (F(v["hw_c"]), F(v["hw_t"])) for i, v in m["zones"].items()}
    chk(sorted(zones) == list(range(11)), "zones must cover squares 0..10")
    certs = m["certs"]
    chk(sorted(c["i"] for c in certs) == list(range(11)), "need exactly the 11 certificates")

    # (3) core containment margins (per square, independent of i)
    margins = []
    for j in range(11):
        cx, cy = sq[j]["cx"], sq[j]["cy"]
        lx_lo, lx_hi = lam_lo * (z0[3 * j] - r0), lam_hi * (z0[3 * j] + r0)
        ly_lo, ly_hi = lam_lo * (z0[3 * j + 1] - r0), lam_hi * (z0[3 * j + 1] + r0)
        off = max(abs(cx - lx_lo), abs(cx - lx_hi)) + max(abs(cy - ly_lo), abs(cy - ly_hi))
        dth = dth_tilt if j >= 6 else dth_up
        margins.append(F(1, 2) - a_core * (1 + dth) - off)

    worst_c = worst_t = F(0)
    for c in certs:
        i = c["i"]
        cert = load(c["file"], base)
        rep = load(c["report"], base)
        if corrupt == "side" and i == 0:
            cert["s"] = str(F(cert["s"]) + F(1, 10**9))
        if corrupt == "report" and i == 0:
            rep["result"] = "FAIL"
        if corrupt == "core" and i == 0:
            cert["hypotheses"]["cores"][0]["kx"] = str(F(cert["hypotheses"]["cores"][0]["kx"]) + F(1, 10**6))
        if corrupt == "slack" and i == 0:
            cert["hypotheses"]["cores"][0]["a"] = str(F(1, 2) - delta / 2)
        # (1) structure
        chk(cert.get("format") == "case-lp-certificate-v1", "cert %d: bad format" % i)
        chk(F(cert["s"]) == s2, "cert %d: side != s''" % i)
        chk(int(cert["n"]) == 11 and int(cert["budget"]) == 1, "cert %d: n/budget" % i)
        chk(cert["atoms"] == [] and cert["weights"] == [] and F(cert["total"]) == 0,
            "cert %d: must carry no atoms" % i)
        cores = cert["hypotheses"]["cores"]
        chk(len(cores) == 10, "cert %d: need 10 cores" % i)
        expect = [j for j in range(11) if j != i]
        for co, j in zip(cores, expect):
            chk(F(co["kx"]) == sq[j]["cx"] and F(co["ky"]) == sq[j]["cy"]
                and F(co["tm"]) == sq[j]["t"], "cert %d: core %d is not the tight pose" % (i, j))
            chk(F(co["a"]) == a_core, "cert %d: core %d half-side != 1/2 - delta" % (i, j))
        nfs = cert["hypotheses"]["nofams"]
        chk(len(nfs) == 1, "cert %d: exactly one NO-family" % i)
        nf = nfs[0]
        hwc, hwt = zones[i]
        if corrupt == "zone" and i == 6:
            hwc, hwt = 10 * hwc, 10 * hwt
            nf = {"x0": str(sq[i]["cx"] - hwc), "x1": str(sq[i]["cx"] + hwc),
                  "y0": str(sq[i]["cy"] - hwc), "y1": str(sq[i]["cy"] + hwc),
                  "t_intervals": [[str(sq[i]["t"] - hwt), str(sq[i]["t"] + hwt)]]}
        chk(F(nf["x0"]) == sq[i]["cx"] - hwc and F(nf["x1"]) == sq[i]["cx"] + hwc
            and F(nf["y0"]) == sq[i]["cy"] - hwc and F(nf["y1"]) == sq[i]["cy"] + hwc,
            "cert %d: zone box != declared (hw_c) box around the tight pose" % i)
        ti = [[F(a), F(b)] for a, b in nf["t_intervals"]]
        if i >= 6:
            chk(ti == [[sq[i]["t"] - hwt, sq[i]["t"] + hwt]], "cert %d: tilt zone" % i)
            dev_t = hwt + dt_tilt + r0
        else:
            h1 = 2 * hwt / (1 + hwt)
            chk(ti == [[F(0), hwt], [1 - h1, F(1)]], "cert %d: upright tilt zone (two branches)" % i)
            x = h1 / (2 - h1)                      # = hwt exactly
            dev_t = max(hwt + dth_up, x + x ** 3 + dth_up)
        # (2) report
        chk(rep.get("result") == "PASS", "cert %d: report is not PASS" % i)
        chk(os.path.basename(rep["cert"]) == os.path.basename(c["file"]), "cert %d: report names another file" % i)
        chk(F(rep["s"]) == s2 and int(rep["depth"]) >= 60 and F(rep["margin"]) == 0
            and F(rep["scale_weights"]) == 1 and F(rep["total"]) == 0 and int(rep["n"]) == 11
            and int(rep["stats"]["witnesses"]) == 0, "cert %d: report parameters" % i)
        # (4) zone -> basin deviation (pull-back through lambda, plus the shell drift)
        cx, cy = sq[i]["cx"], sq[i]["cy"]
        zx_lo, zx_hi = z0[3 * i] - r0, z0[3 * i] + r0
        zy_lo, zy_hi = z0[3 * i + 1] - r0, z0[3 * i + 1] + r0
        dev_x = max(abs((cx - hwc) / lam_hi - zx_hi), abs((cx + hwc) / lam_lo - zx_lo))
        dev_y = max(abs((cy - hwc) / lam_hi - zy_hi), abs((cy + hwc) / lam_lo - zy_lo))
        dev_c = max(dev_x, dev_y) + SQRT2_UB * rho_b
        worst_c, worst_t = max(worst_c, dev_c), max(worst_t, dev_t)

    chk(min(margins) > 0, "core containment margin <= 0")
    fits = {}
    for name in m["basins"]:
        chk(name in BASINS, "unknown basin %s" % name)
        rc, rt = BASINS[name]
        fits[name] = bool(worst_c < rc and worst_t < rt)
    chk(all(fits.values()), "pocket zone does not land in basin(s) %s" % [n for n, v in fits.items() if not v])
    # (5) counting-row radius from (U-C): r + sqrt2*lam*(r + rho_B) + slop <= delta
    slop = dt_tilt + SQRT2_UB * lam_hi * F(2, 10**14) + 4 * r0
    r_row = (delta - slop - SQRT2_UB * lam_hi * rho_b) / (1 + SQRT2_UB * lam_hi)
    chk(r_row > 0, "no positive counting-row radius")
    if not quiet:
        print("PASS u-ladder manifest %s: delta = %s (%.3e), 11 U_1 certificates structurally exact, "
              "reports PASS (depth >= 60), min core margin %.3e, pocket dev (c, t) = (%.4e, %.4e), "
              "basins %s, counting-row radius r <= %.4e (rho_B = %s), lambda - 1 in [%.2e, %.2e]"
              % (os.path.basename(mpath), delta, float(delta), float(min(margins)), float(worst_c),
                 float(worst_t), fits, float(r_row), rho_b, float(lam_lo - 1), float(lam_hi - 1)))
    return dict(delta=str(delta), min_core_margin=str(min(margins)), dev_c=str(worst_c),
                dev_t=str(worst_t), basins=fits, r_row=str(r_row))


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    corrupt = None
    for k, a in enumerate(argv):
        if a == "--corrupt":
            corrupt = argv[k + 1]
    quiet = "--quiet" in argv
    if not args:
        print(__doc__)
        return 2
    try:
        verify(args[0], corrupt=corrupt, quiet=quiet)
        return 0
    except Fail as e:
        print("FAIL: %s%s" % (e, " (corruption %s)" % corrupt if corrupt else ""))
        return 1
    except (KeyError, ValueError, TypeError, OSError) as e:
        print("MALFORMED: %r" % (e,))
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
