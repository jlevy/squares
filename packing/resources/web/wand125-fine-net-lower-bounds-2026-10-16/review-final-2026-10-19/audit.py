import gzip
import hashlib
import json
import subprocess
from fractions import Fraction as F

import yaml

REPO = "/Users/levy/wrk/github/squares/.worktrees/review-668-math-20261018"
HEAD = "3d34e828fddbe3b3a91172cc48b1ff07ba8d3b07"
BASE = "e22a9f9f46b44bac145f5a7da8ca00c42e13ecde"
PACKET = "wand125-fine-net-lower-bounds-2026-10-16"
ROOT = "packing/resources/web/" + PACKET
EXPECTED = [38, 40, 41, 43, 51, 68, 84, 85, 86, 88, 89, 91, 90, 92, 106, 107, 108, 110]


def git(*args):
    return subprocess.check_output(["git", "-C", REPO, *args])


def blob(path, ref=HEAD):
    return git("show", ref + ":" + path)


def read_json(raw, *, literal=False):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            assert key not in out, key
            out[key] = value
        return out
    return json.loads(raw, parse_float=str if literal else float, object_pairs_hook=unique)


def rho(t):
    return (1 + 2*t - t*t) / (2*(1 + t*t))


files = git("ls-tree", "-r", "--name-only", HEAD, ROOT).decode().splitlines()
paths = [p for p in files if "/release/certificates/" in p and p.endswith("/candidate.json.gz")]
assert len(paths) == 18
rows, candidates = [], {}
for path in paths:
    packed = blob(path)
    raw = gzip.decompress(packed)
    data = read_json(raw, literal=True)
    assert set(data) == {"n", "L", "B", "proof_net", "total_mass", "points", "rectangles"}
    assert set(data["proof_net"]) == {"step", "last"}
    n, L, B = data["n"], F(data["L"]), F(data["B"])
    D, m = F(data["proof_net"]["step"]), data["proof_net"]["last"]
    assert data["points"] == [] and 0 < B < 1 and D > 0 and 1 <= m < 2**16
    t, a = m*D, m*D - D/2
    assert t <= F(1, 2) and t*t + 2*t - 1 > 0 and a*a + 2*a - 1 < 0
    assert B*(1+D) < 1 and B*(1+D/(1-D*D/4)) < 1
    assert L*L >= 2*B*B and L >= 2*rho(a)
    M = F(0)
    expanded = {}
    for row in data["rectangles"]:
        assert set(row) == {"rectangle", "mass"}
        x0, y0, x1, y1 = map(F, row["rectangle"])
        weight = F(row["mass"])
        assert weight >= 0
        M += weight
        if not weight:
            continue
        assert 0 <= x0 < x1 <= L and 0 <= y0 < y1 <= L
        density = weight/(8*(x1-x0)*(y1-y0))
        assert 64*density <= 2**32
        if n == 108:
            for l, r, b, u in ((x0, x1, y0, y1), (y0, y1, x0, x1)):
                for left, right in ((l, r), (L-r, L-l)):
                    for bottom, top in ((b, u), (L-u, L-b)):
                        key = (left, right, bottom, top)
                        expanded[key] = expanded.get(key, F(0)) + density
    assert M == F(data["total_mass"]) and 0 < M < n
    premise = read_json(blob(ROOT + f"/receipts/premises-n{n}.json"))
    assert hashlib.sha256(raw).hexdigest() == premise["candidate_sha256"]
    if n == 108:
        assert len(expanded) == 6524
        assert sum(((r-l)*(u-b)*d for (l,r,b,u),d in expanded.items()), F(0)) == M
        assert max(expanded.values()) <= 2**96
    rows.append([n, str(L), len(data["rectangles"]), m+1, str(n-M), str(1-B*(1+D))])
    candidates[n] = (path, packed, data)
assert sorted(candidates) == sorted(EXPECTED)

retention = read_json(blob(ROOT + "/acquisition/release-assets.json"))
stored_count = pinned_count = 0
for asset in retention["assets"]:
    for member in asset["members"]:
        if "pinned_only" in member:
            assert ROOT + "/release/" + member["path"] not in files
            pinned_count += 1
            continue
        held = blob(ROOT + "/" + member["stored"])
        decoded = gzip.decompress(held) if member["form"] == "gzip" else held
        assert len(decoded) == member["bytes"]
        assert hashlib.sha256(decoded).hexdigest() == member["sha256"]
        stored_count += 1
assert len(retention["assets"]) == 18

old = yaml.safe_load(blob("packing/frontier/results.yaml", BASE))["results"]
new = yaml.safe_load(blob("packing/frontier/results.yaml"))["results"]
oldmap, newmap = ({r["id"]:r for r in seq} for seq in (old, new))
assert len(oldmap) == len(old) == 199 and len(newmap) == len(new) == 217
assert all(newmap[key] == value for key, value in oldmap.items())
added = [r for r in new if r["id"] not in oldmap]
assert [r["scope"]["n_values"][0] for r in added] == EXPECTED
for row in added:
    n = row["scope"]["n_values"][0]
    assert row["kind"] == "lower-bound"
    assert (row["verification"], row["confirmation"]) == (("V3", "C3") if n == 108 else ("V0", "C0"))
changed = git("diff", "--name-only", BASE, HEAD, "--", "packing/frontier/n-*.md").decode().splitlines()
assert changed == ["packing/frontier/n-108.md"]
fronts = [yaml.safe_load(blob("packing/frontier/n-108.md", ref).decode().split("---", 2)[1])["packing"] for ref in (BASE, HEAD)]
for field in ("verified_upper_bound", "reported_upper_bound"):
    assert fronts[0][field] == fronts[1][field]

census_root = "packing/benchmarks/measure-verifier/census-mixed"
cases = read_json(blob(census_root + "/census.json"))["cases"]
entries = [x for x in cases.values() if x["packet"] == PACKET]
assert len(entries) == 1
entry = entries[0]
cert = entry["certificate"]
log = [read_json(line) for line in gzip.decompress(blob(census_root + "/" + PACKET + "/" + cert + ".jsonl.gz")).splitlines()]
control = read_json(blob(census_root + "/" + PACKET + "/" + cert + ".control.json"))
summary = log[-1]
assert [r["r"] for r in log[:-1]] == list(range(201))
assert all(r["verdict"] == "verified" and F(r["threshold"]) == 1 and F(r["min_certified_lower_bound"]) >= 1 for r in log[:-1])
assert entry["n"] == 108 and entry["status"] == summary["status"] == "VERIFIED"
assert entry["returncode"] == 0 and entry["directions_verified"] == summary["directions"] == 201
assert entry["refused_directions"] == summary["refused_directions"] == []
assert summary["fault_injected_at_box"] is None
assert entry["build"] == summary["build"] == control["build"]
assert entry["binary_sha256"] == control["binary_sha256"]
assert entry["premises"] == summary["premises"]
sha = hashlib.sha256(candidates[108][1]).hexdigest()
assert sha == entry["candidate_sha256"] == control["candidate_sha256"] == summary["premises"]["input_sha256"]
assert control["kind"] == "sqverify-fast-control/v2" and control["status"] == "CONTROLS_REFUSED"
positive, scaled, near = control["runs"]
assert positive["name"] == "original" and positive["returncode"] == 0 and positive["verdict"] == "verified"
assert scaled["name"] == "scaled-99-100" and F(scaled["mutation"]["factor"]) == F(99,100)
sweep = scaled["sweep"]
assert sweep["directions"] == sweep["net_directions"] == 201
assert sweep["indices_complete"] and sweep["premises_agree"] and sweep["fault_injected_at_box"] is None
assert sweep["returncode"] == 1 and sweep["summary_status"] == "REFUSED" and sweep["verified_directions"] == []
assert sweep["summary_refused_directions"] == list(range(201))
assert [r["r"] for r in sweep["refused"]] == list(range(201))
for r in sweep["refused"]:
    assert all(r[k] is True for k in ("coverage_refusal", "in_domain", "capture_below_1", "captures_agree", "original_at_least_1"))
    high = F(531,50) - rho(max(F(0), r["r"]*F(83,40000)-F(83,80000)))
    assert all(F(531,100) <= F(x) <= high for x in r["pose"])
    assert F(r["capture"]) < 1
assert near["name"] == "near-threshold" and near["returncode"] == 1
assert near["verdict"] == "counterexample-candidate" and near["exact_below_threshold"] is True
assert F(near["witness"]["exact_coverage"]) < 1
claims = git("diff", "--name-only", "a450742e379ffbc2d4ef63885c67dda63bb7fe36", HEAD).decode().splitlines()
assert len(claims) == 6 and claims[-1] == "packing/src/sqpack/release.py"
for path in claims[:-1]:
    assert blob(path) == blob(path, "a450742e379ffbc2d4ef63885c67dda63bb7fe36").replace(b"/blob/c36eb7d6/", b"/blob/a450742e/")
assert blob(claims[-1]) == blob(claims[-1], "a450742e379ffbc2d4ef63885c67dda63bb7fe36").replace(b'PUBLICATION_REVISION = "c36eb7d6"', b'PUBLICATION_REVISION = "a450742e"')
assert git("rev-parse", "e952755bcad005738785ab8bab0d0b7176f34fed^{tree}") == git("rev-parse", BASE + "^{tree}")
print(json.dumps({"status":"PASS", "premises":[r for n in EXPECTED for r in rows if r[0] == n], "columns":["n","L","representatives","directions","mass_gap","shrink_gap"], "retained_members":stored_count, "digest_only_members":pinned_count, "inherited_results_unchanged":len(old), "prospective_results":len(new), "new_rungs":"one V3/C3; seventeen V0/C0", "significance":[[r["scope"]["n_values"][0],r["significance"]["score"]] for r in added], "verified_directions":201, "control_refusal_records":201, "claim_docs_only_link_replacements":5, "actual_main_tree_matches_base":True, "coverage_replayed":False}, indent=2))
