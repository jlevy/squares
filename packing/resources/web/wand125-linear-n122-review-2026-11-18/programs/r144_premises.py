"""Every exact premise of mixed_n122_L1126, and the custody of its files.

Usage (python -I, from any directory outside the data):
  r144_premises.py --pin PIN --manifest SOURCE_MANIFEST --asset ASSET.tar.gz
                   --outer OUTER --bundle-tar BUNDLE.tar.gz --bundle BUNDLE_DIR
                   --repo REPO_ROOT --out OUT.json

PIN is a directory holding the pinned documents at their repository paths
(problems/square-lower-bounds/...), SOURCE_MANIFEST the packet's source-manifest.json on
main, ASSET the downloaded release asset, OUTER its extraction, BUNDLE.tar.gz the inner
proof bundle and BUNDLE_DIR its extraction (n122-L11.26-proof-bundle/).

Verdict PREMISES_HOLD when every check passes; otherwise PREMISES_FAIL with the list.
Written for this review; imports nothing from jlevy/squares or the source.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import tarfile
import time
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from r144_common import (  # noqa: E402
    angle_data,
    expand_images,
    frac_str,
    git_blob_id,
    image_of,
    load_candidate,
    rat,
    read_json_strict,
    sha256_bytes,
    sha256_file,
)

CERT_DIR = "problems/square-lower-bounds/certificates/mixed_n122_L1126"
CHECKER_SHA = "0249726ab1e67dc481e0c53f43b524902a48f95d051b1b08865a3cf3ef89a06d"
CAND_DIGEST = "c91a750977764335d3668599bf7e599539b30f7c81969372fc27ad90561e9ed4"


class Report:
    def __init__(self):
        self.checks = []

    def check(self, name, ok, **detail):
        self.checks.append({"check": name, "ok": bool(ok), **detail})
        return ok

    @property
    def failed(self):
        return [c["check"] for c in self.checks if not c["ok"]]


def read_json_loose(data: bytes):
    """JSON with float tokens kept as their exact decimal Fraction (for result records)."""
    return json.loads(data.decode("utf-8"), parse_float=lambda s: F(s))


def isqrt_bounds(n: F, scale: int):
    """Rational lo <= sqrt(n) <= hi with denominators 10^scale."""
    N = n.numerator * 10 ** (2 * scale)
    D = n.denominator
    # sqrt(N/D) = sqrt(N*D)/D
    r = math.isqrt(N * D)
    lo = F(r, D * 10**scale)
    hi = F(r + 1, D * 10**scale)
    assert lo * lo <= n <= hi * hi
    return lo, hi


def custody(rep: Report, a) -> dict:
    man = json.load(open(a.manifest))
    out = {}
    # 1. pinned documents
    docs = man["source_documents"]
    nd = 0
    for d in docs:
        p = os.path.join(a.pin, d["path"])
        data = open(p, "rb").read()
        ok = len(data) == d["bytes"] and sha256_bytes(data) == d["sha256"] and git_blob_id(data) == d["git_blob"]
        rep.check(f"document {d['path'].split('/')[-1]} size, sha256 and git blob", ok)
        nd += ok
        if "byte_identical_to_retained" in d:
            rp = os.path.join(a.repo, d["byte_identical_to_retained"])
            ok2 = os.path.exists(rp) and sha256_file(rp) == d["sha256"]
            rep.check(f"document {d['path'].split('/')[-1]} equals the retained copy on main", ok2, retained=d["byte_identical_to_retained"])
    out["documents"] = nd
    chk = open(os.path.join(a.pin, CERT_DIR, "code/unified_linear_verify.cpp"), "rb").read()
    rep.check("pinned checker sha256", sha256_bytes(chk) == CHECKER_SHA)
    # 2. asset
    asset_rec = read_json_strict(open(os.path.join(a.pin, CERT_DIR, "ASSET.json"), "rb").read())
    st = os.stat(a.asset)
    asha = sha256_file(a.asset)
    arec = asset_rec["assets"][0]
    rep.check("asset size and sha256 equal ASSET.json", st.st_size == arec["size"] and asha == arec["sha256"], size=st.st_size, sha256=asha)
    rep.check("asset size and sha256 equal the packet manifest", st.st_size == man["release"]["bytes"] and asha == man["release"]["sha256"])
    with tarfile.open(a.asset, "r:gz") as tf:
        mem = [(m.name, m.size, m.isreg()) for m in tf.getmembers()]
    names = sorted(m[0] for m in mem)
    rep.check(
        "asset holds exactly candidate.json, certificate.json and the proof bundle, all regular",
        names
        == sorted(
            [
                "certificates/mixed_n122_L1126/candidate.json",
                "certificates/mixed_n122_L1126/certificate.json",
                "certificates/mixed_n122_L1126/n122-L11.26-proof-bundle.tar.gz",
            ]
        )
        and all(m[2] for m in mem),
        members=mem,
    )
    audit = read_json_strict(open(os.path.join(a.pin, CERT_DIR, "completion-audit.json"), "rb").read())
    od = os.path.join(a.outer, "certificates/mixed_n122_L1126")
    bsha = sha256_file(a.bundle_tar)
    rep.check("bundle file is the one extracted from the asset", bsha == sha256_file(os.path.join(od, "n122-L11.26-proof-bundle.tar.gz")))
    rep.check("bundle sha256 equals completion-audit archive_sha256", bsha == audit["archive_sha256"], sha256=bsha, bytes=os.stat(a.bundle_tar).st_size)
    csha = sha256_file(os.path.join(od, "certificate.json"))
    rep.check("certificate.json sha256 equals completion-audit certificate_sha256", csha == audit["certificate_sha256"], sha256=csha)
    out["candidate_file_sha256"] = sha256_file(os.path.join(od, "candidate.json"))
    # 3. bundle members, streamed from the tarball and compared with the extraction
    import hashlib

    tar_digests = {}
    kinds = set()
    with tarfile.open(a.bundle_tar, "r:gz") as tf:
        for m in tf:
            kinds.add("reg" if m.isreg() else "other")
            if m.isreg():
                h = hashlib.sha256()
                f = tf.extractfile(m)
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
                tar_digests[m.name] = h.hexdigest()
    rep.check("bundle has 810 members, all regular files", len(tar_digests) == 810 and kinds == {"reg"}, members=len(tar_digests))
    top = "n122-L11.26-proof-bundle/"
    expect = {top + n for n in ("candidate.json", "certificate.json", "manifest.json", "replay-progress.json", "summary.json", "verify.cpp")}
    for j in range(201):
        for n in ("candidate.json", "input.txt", "result.json", "verify.cpp"):
            expect.add(f"{top}net{j:03d}/{n}")
    rep.check("bundle member names are the 6 top-level files and 4 per angle", set(tar_digests) == expect)
    mism = [n for n in tar_digests if sha256_file(os.path.join(os.path.dirname(a.bundle.rstrip("/")), n)) != tar_digests[n]]
    rep.check("extracted bundle equals the tarball byte for byte", not mism, mismatched=mism[:5])
    vc = [n for n in tar_digests if n.endswith("verify.cpp")]
    rep.check("all 202 checker copies equal the pinned checker", len(vc) == 202 and all(tar_digests[n] == CHECKER_SHA for n in vc))
    cand_sha = tar_digests[top + "candidate.json"]
    cc = [n for n in tar_digests if n.endswith("candidate.json")]
    rep.check("all 202 candidate copies equal the top-level candidate", len(cc) == 202 and all(tar_digests[n] == cand_sha for n in cc))
    rep.check("top-level candidate and certificate equal the asset's", cand_sha == out["candidate_file_sha256"] and tar_digests[top + "certificate.json"] == csha)
    pin_man = sha256_file(os.path.join(a.pin, CERT_DIR, "manifest.json"))
    rep.check("bundle manifest.json equals the pinned manifest.json", tar_digests[top + "manifest.json"] == pin_man)
    out["input_sha256"] = {int(n.split("/")[1][3:]): tar_digests[n] for n in tar_digests if n.endswith("input.txt")}
    return out


def candidate_checks(rep: Report, cand: dict, raw: bytes) -> dict:
    L, B = cand["L"], cand["B"]
    prims = cand["primitives"]
    out = {}
    rep.check("n = 122", cand["n"] == 122)
    rep.check("L = 563/50", L == F(563, 50), L=frac_str(L))
    rep.check("B = 9977/10000", B == F(9977, 10000), B=frac_str(B))
    rep.check("net step 83/40000, last index 200", cand["step"] == F(83, 40000) and cand["last"] == 200)
    kinds = {k: sum(1 for p in prims if p[0] == k) for k in ("point", "segment", "rectangle")}
    rep.check("502 point, 1268 segment and 3 rectangle primitives", kinds == {"point": 502, "segment": 1268, "rectangle": 3}, counts=kinds)
    bad_in, bad_deg, bad_mass = [], [], []
    for i, (k, g, m) in enumerate(prims):
        if not all(F(0) <= v <= L for v in g):
            bad_in.append(i)
        if k == "segment" and (g[0], g[1]) == (g[2], g[3]):
            bad_deg.append(i)
        if k == "rectangle" and not (g[0] < g[2] and g[1] < g[3]):
            bad_deg.append(i)
        if m <= 0:
            bad_mass.append(i)
    rep.check("every primitive lies in K = [0, L]^2", not bad_in, bad=bad_in[:5])
    rep.check("no degenerate segment or rectangle", not bad_deg, bad=bad_deg[:5])
    rep.check("every mass is positive", not bad_mass, bad=bad_mass[:5])
    total = sum((p[2] for p in prims), F(0))
    rep.check("masses sum to the stated total", total == cand["total_mass"], total=frac_str(total))
    rep.check("total mass below n (the budget)", total < cand["n"], gap=frac_str(cand["n"] - total))
    rep.check("total = 12199999/100000 = n - 1/100000", total == F(12199999, 100000))
    by_kind = {k: frac_str(sum((p[2] for p in prims if p[0] == k), F(0))) for k in kinds}
    out["mass_by_kind"] = by_kind
    out["mass_by_kind_float"] = {k: float(F(v)) for k, v in by_kind.items()}
    # segment orientation
    hor = sum(1 for p in prims if p[0] == "segment" and p[1][1] == p[1][3])
    ver = sum(1 for p in prims if p[0] == "segment" and p[1][0] == p[1][2])
    out["segments_horizontal"] = hor
    out["segments_vertical"] = ver
    out["segments_oblique"] = kinds["segment"] - hor - ver
    lens = [max(abs(p[1][2] - p[1][0]), abs(p[1][3] - p[1][1])) for p in prims if p[0] == "segment" and (p[1][1] == p[1][3] or p[1][0] == p[1][2])]
    if lens:
        out["axis_segment_length_range"] = [float(min(lens)), float(max(lens))]
    out["rectangles"] = [
        {"geometry": [frac_str(v) for v in p[1]], "mass": frac_str(p[2]), "width": float(p[1][2] - p[1][0]), "height": float(p[1][3] - p[1][1])}
        for p in prims
        if p[0] == "rectangle"
    ]
    # candidate digest by canonical forms
    obj = cand.get("raw", {})
    forms = {
        "sorted_compact": json.dumps(obj, sort_keys=True, separators=(",", ":")),
        "sorted_default": json.dumps(obj, sort_keys=True),
        "compact": json.dumps(obj, separators=(",", ":")),
        "file_bytes": None,
    }
    found = []
    for name, s in forms.items():
        d = sha256_bytes(raw) if s is None else sha256_bytes(s.encode())
        if d == CAND_DIGEST:
            found.append(name)
    rep.check("candidate_digest c91a7509... reproduced by a canonical form", bool(found), forms=found)
    # images, merging, invariance, orbits
    imgs = expand_images(prims, L)
    rep.check("8 images per primitive: 14184", len(imgs) == 14184, images=len(imgs))
    merged = {}
    for kind, g, m, _i, _g in imgs:
        merged[(kind, g)] = merged.get((kind, g), F(0)) + m
    out["distinct_images"] = len(merged)
    out["distinct_images_by_kind"] = {k: sum(1 for key in merged if key[0] == k) for k in kinds}
    inv_ok = True
    for gi in range(8):
        for (kind, g), m in merged.items():
            if kind == "point":
                h = image_of(kind, g, gi, L)
            else:
                h = image_of(kind, g, gi, L)
            if merged.get((kind, h)) != m:
                inv_ok = False
                break
        if not inv_ok:
            break
    rep.check("merged measure invariant under all eight symmetries of K", inv_ok)
    orbits = {}
    for i, (k, g, m) in enumerate(prims):
        key = (k, frozenset(image_of(k, g, gi, L) for gi in range(8)))
        orbits.setdefault(key, []).append(i)
    shared = [v for v in orbits.values() if len(v) > 1]
    out["distinct_orbits_by_kind"] = {k: sum(1 for key in orbits if key[0] == k) for k in kinds}
    out["primitives_sharing_an_orbit"] = len(shared)
    rep.check("the 1773 primitives are 1773 distinct D4 orbits", not shared and len(orbits) == 1773)
    sizes = {}
    for key in orbits:
        sizes[len(key[1])] = sizes.get(len(key[1]), 0) + 1
    out["orbit_sizes"] = {str(k): v for k, v in sorted(sizes.items())}
    # denominators
    den = 1
    for _k, g, _m in prims:
        for v in g:
            den = math.lcm(den, v.denominator)
    den = math.lcm(den, L.denominator, (B / 2).denominator, (L / 2).denominator)
    out["geometry_lcm_denominator"] = den
    out["geometry_lcm_times_L"] = float(den * L)
    return out


def net_checks(rep: Report, cand: dict, pin_manifest: dict) -> dict:
    L, B, D = cand["L"], cand["B"], cand["step"]
    out = {}
    t200 = D * 200
    rep.check("t_200 = 83/200", t200 == F(83, 200))
    q = t200 * t200 + 2 * t200 - 1
    rep.check("t_200^2 + 2 t_200 - 1 = 89/40000 > 0, so t_200 > tan(pi/8)", q == F(89, 40000) and q > 0)
    t = D * 199 + D / 2
    q2 = t * t + 2 * t - 1
    out["t199_plus_half_step_below_tan_pi_8"] = bool(q2 < 0)
    out["t199_plus_half_step_value"] = frac_str(q2)
    t = D * 200 - D / 2
    out["t200_minus_half_step_below_tan_pi_8"] = bool(t * t + 2 * t - 1 < 0)
    shrink = B * (1 + D)
    rep.check("B(1 + D) = 399908091/400000000 < 1", shrink == F(399908091, 400000000) and shrink < 1, value=frac_str(shrink))
    z = D / 2
    sharp = B * (1 + 2 * z - z * z) / (1 + z * z)
    out["sharp_core_extent_at_half_step"] = frac_str(sharp)
    out["sharp_clearance"] = frac_str(1 - sharp)
    # the bound used: (1 + 2z - z^2)/(1 + z^2) <= 1 + 2z for z >= 0
    rep.check("(1 + 2z - z^2)/(1 + z^2) <= 1 + 2z at z = D/2", (1 + 2 * z - z * z) / (1 + z * z) <= 1 + 2 * z)
    netm = pin_manifest["net"]
    rep.check(
        "manifest.json net facts equal the recomputed values",
        rat(netm["step"]) == D
        and netm["count"] == 201
        and rat(netm["endpoint"]) == t200
        and rat(netm["endpoint_check"]) == q
        and rat(netm["rotated_side_upper"]) == shrink
        and rat(netm["side_margin"]) == 1 - shrink
        and rat(netm["per_edge_margin"]) == (1 - shrink) / 2,
    )
    rep.check(
        "manifest.json n, L, B, mass and checker digest",
        pin_manifest["n"] == 122
        and rat(pin_manifest["L"]) == L
        and rat(pin_manifest["B"]) == B
        and rat(pin_manifest["mass"]) == cand["total_mass"]
        and pin_manifest["source_sha256"] == CHECKER_SHA
        and pin_manifest["candidate_digest"] == CAND_DIGEST
        and pin_manifest["angle_count"] == 201,
    )
    Es = [angle_data(j, D, L, B)["E"] for j in range(201)]
    rep.check("every centre domain is nonempty (E_j > 0)", all(e > 0 for e in Es), least=float(min(Es)), at=Es.index(min(Es)))
    out["E_range"] = [float(min(Es)), float(max(Es))]
    return out


def record_checks(rep: Report, cand: dict, a, inputs_sha: dict) -> dict:
    L, B, D = cand["L"], cand["B"], cand["step"]
    out = {}
    rows = []
    bad = []
    for j in range(201):
        d = os.path.join(a.bundle, f"net{j:03d}")
        r = read_json_loose(open(os.path.join(d, "result.json"), "rb").read())
        man = r["manifest"]
        ang = angle_data(j, D, L, B)
        ok = (
            r["status"] == "ANGLE_VERIFIED"
            and r["frontier"] == []
            and r["exact_witnesses"] == []
            and r["globally_verified"] is False
            and r["scope"] == "ONE_NET_ANGLE_ONLY"
            and man["index"] == j
            and rat(man["t"]) == ang["t"]
            and rat(man["L"]) == L
            and rat(man["B"]) == B
            and rat(man["E"]) == ang["E"]
            and rat(man["gamma"]) == 1
            and rat(man["mass"]) == cand["total_mass"]
            and man["source_sha256"] == CHECKER_SHA
            and man["candidate_digest"] == CAND_DIGEST
            and man["input_sha256"] == inputs_sha[j]
            and r["nodes"] == 2 * r["leaves"] - 1
            and r["lower"] >= 1
        )
        if not ok:
            bad.append(j)
        rows.append({"j": j, "nodes": r["nodes"], "leaves": r["leaves"], "lower": r["lower"], "seconds": r["seconds"]})
    rep.check("201 records: verified, empty frontier, manifest fields equal the recomputed t, E, L, B, gamma = 1, mass, digests; nodes = 2 leaves - 1; lower >= 1", not bad, bad=bad)
    cert = read_json_loose(open(os.path.join(a.bundle, "certificate.json"), "rb").read())
    cres = cert["results"]
    ok = (
        cert["status"] == "ALL_LINEAR_ANGLES_VERIFIED_AND_REPLAYED"
        and set(cres) == {str(j) for j in range(201)}
        and all(cres[str(j)]["status"] == "LINEAR_ANGLE_REPLAYED" and cres[str(j)]["input_sha256"] == inputs_sha[j] and cres[str(j)]["nodes"] == rows[j]["nodes"] and cres[str(j)]["index"] == j for j in range(201))
        and rat(cert["total_mass"]) == cand["total_mass"]
        and rat(cert["budget_gap"]) == cand["n"] - cand["total_mass"]
        and cert["source_sha256"] == CHECKER_SHA
        and cert["candidate_digest"] == CAND_DIGEST
    )
    rep.check("certificate.json lists the 201 records' digests and node counts", ok)
    summ = read_json_loose(open(os.path.join(a.bundle, "summary.json"), "rb").read())
    sres = summ["records"]
    ok = (
        summ["status"] == "ALL_LINEAR_ANGLES_VERIFIED_AND_REPLAYED"
        and summ["complete_angles"] == 201
        and summ["verified_angles"] == 201
        and set(sres) == {str(j) for j in range(201)}
        and all(sres[str(j)]["nodes"] == rows[j]["nodes"] and sres[str(j)]["seconds"] == rows[j]["seconds"] and sres[str(j)]["status"] == "ANGLE_VERIFIED" for j in range(201))
    )
    rep.check("summary.json agrees with the 201 records", ok)
    prog = json.load(open(os.path.join(a.bundle, "replay-progress.json")))
    rep.check("replay-progress.json: 201 of 201", prog == {"done": 201, "total": 201})
    out["nodes_total"] = sum(r["nodes"] for r in rows)
    out["nodes_max"] = max(r["nodes"] for r in rows)
    out["nodes_max_at"] = max(rows, key=lambda r: r["nodes"])["j"]
    out["nodes_min"] = min(r["nodes"] for r in rows)
    out["nodes_min_at"] = min(rows, key=lambda r: r["nodes"])["j"]
    out["seconds_total"] = float(sum(r["seconds"] for r in rows))
    low = sorted(rows, key=lambda r: r["lower"])
    out["least_lower"] = [{"j": r["j"], "lower_minus_one": float(r["lower"] - 1)} for r in low[:10]]
    out["records"] = [{"j": r["j"], "nodes": r["nodes"], "lower_minus_one": float(r["lower"] - 1), "seconds": float(r["seconds"])} for r in rows]
    return out


def comparisons(rep: Report, cand: dict, audit: dict) -> dict:
    L = cand["L"]
    out = {}
    lo2, hi2 = isqrt_bounds(F(2), 60)
    lo22, hi22 = isqrt_bounds(F(22), 60)
    G_lo = 2 * lo2 - 1 + (1100 + 10 * lo22) / 122
    G_hi = 2 * hi2 - 1 + (1100 + 10 * hi22) / 122
    out["green_G11_interval"] = [f"{float(G_lo):.15f}", f"{float(G_hi):.15f}"]
    # the record's exact form
    R_lo = F(489, 61) + 2 * lo2 + F(5, 61) * lo22
    R_hi = F(489, 61) + 2 * hi2 + F(5, 61) * hi22
    rep.check("the record's form 489/61 + 2 sqrt2 + (5/61) sqrt22 is Green's G_11", R_lo == G_lo and R_hi == G_hi)
    cw = rat(audit["compared_with"])
    rep.check("completion-audit compared_with is an upper bound on G_11", cw >= G_hi, excess_over_upper=float(cw - G_hi), excess_over_lower=float(cw - G_lo))
    imp = rat(audit["improvement_lower"])
    rep.check("improvement_lower = L - compared_with", imp == L - cw, value=float(imp))
    rep.check("L - G_11 > 0.0307191 (the README's claim)", L - G_hi > F(307191, 10**7), lower=f"{float(L - G_hi):.12f}")
    # Nagamochi at 126 and 127 (the record's forms 1 + sqrt(105), 1 + sqrt(106))
    rep.check("L > 1 + sqrt(105): (L - 1)^2 > 105", (L - 1) ** 2 > 105, square=frac_str((L - 1) ** 2))
    lo105, hi105 = isqrt_bounds(F(105), 40)
    out["gain_over_nagamochi_126"] = [float(L - 1 - hi105), float(L - 1 - lo105)]
    rep.check("L < 1 + sqrt(106), so n = 127 gains nothing", (L - 1) ** 2 < 106)
    out["sqrt_N"] = {N: bool(L * L > N) for N in range(121, 129)}
    rep.check("L^2 > N for N = 122..126 and L^2 < 127", all(L * L > N for N in range(122, 127)) and L * L < 127, L_squared=frac_str(L * L))
    out["gain_over_green_122_125"] = [float(L - G_hi), float(L - G_lo)]
    return out


def main():
    ap = argparse.ArgumentParser()
    for k in ("--pin", "--manifest", "--asset", "--outer", "--bundle-tar", "--bundle", "--repo", "--out"):
        ap.add_argument(k, required=True)
    a = ap.parse_args()
    t0 = time.process_time()
    rep = Report()
    res = {"program": "r144_premises.py"}
    res["custody"] = custody(rep, a)
    raw = open(os.path.join(a.bundle, "candidate.json"), "rb").read()
    cand = load_candidate(raw)
    res["candidate"] = candidate_checks(rep, cand, raw)
    pin_manifest = read_json_strict(open(os.path.join(a.pin, CERT_DIR, "manifest.json"), "rb").read())
    res["net"] = net_checks(rep, cand, pin_manifest)
    res["records"] = record_checks(rep, cand, a, res["custody"].pop("input_sha256"))
    audit = read_json_strict(open(os.path.join(a.pin, CERT_DIR, "completion-audit.json"), "rb").read())
    res["comparisons"] = comparisons(rep, cand, audit)
    res["checks"] = rep.checks
    res["failed"] = rep.failed
    res["verdict"] = "PREMISES_HOLD" if not rep.failed else "PREMISES_FAIL"
    res["cpu_seconds"] = round(time.process_time() - t0, 2)
    with open(a.out, "w") as f:
        json.dump(res, f, indent=1)
        f.write("\n")
    print(res["verdict"], f"{len(rep.checks)} checks, {len(rep.failed)} failed", res["failed"], f"cpu {res['cpu_seconds']} s")
    return 0 if not rep.failed else 1


if __name__ == "__main__":
    sys.exit(main())
