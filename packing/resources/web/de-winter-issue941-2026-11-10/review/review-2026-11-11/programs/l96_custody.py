"""Custody of the retained source files, read as data.

L96 review program. Usage:
  python -I -B l96_custody.py OUT_JSON ISSUES_JSON P941 P942 PA0C
where each P is a packet's `source/` directory. For each packet it digests every retained
file (SHA-256 and git blob id), holds the files to the SHA256SUMS retained beside them,
compares the three pins' SHA256SUMS with each other, and compares each README table with
the issue or comment that reports it. The upstream repository was not reachable from
this session (the GitHub API refused it), so nothing here is held to upstream blobs.
"""

import hashlib
import json
import os
import re
import sys

ROW = re.compile(r"^\|\s*(\d+)\s*\|(.*)\|\s*$")


def digests(path):
    with open(path, "rb") as fh:
        b = fh.read()
    return hashlib.sha256(b).hexdigest(), hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest(), len(b)


def sums(path):
    out = {}
    with open(path) as fh:
        for line in fh:
            h, name = line.rstrip("\n").split("  ", 1)
            out[name] = h
    return out


def rows(text, cols):
    out = {}
    for line in text.splitlines():
        m = ROW.match(line.strip())
        if m:
            cells = [c.strip() for c in m.group(2).split("|")]
            out[int(m.group(1))] = cells[:cols]
    return out


def main():
    out_path, issues_path = sys.argv[1:3]
    packets = {"941@71da0d5": sys.argv[3], "942@a9486ed": sys.argv[4], "addendum@a0c4fc8": sys.argv[5]}
    sub = {"941@71da0d5": "above324", "942@a9486ed": "above324_refined", "addendum@a0c4fc8": "above324_refined"}
    report = {"upstream": "not reached: the GitHub API refused JoostdeWinter/square-packing in this session", "packets": {}}
    all_sums = {}
    for key, src in packets.items():
        d = os.path.join(src, sub[key])
        files = {}
        for root, _, names in os.walk(src):
            for nm in sorted(names):
                p = os.path.join(root, nm)
                sha, blob, size = digests(p)
                files[os.path.relpath(p, src)] = {"sha256": sha, "git_blob": blob, "bytes": size}
        s = sums(os.path.join(d, "SHA256SUMS"))
        all_sums[key] = s
        held = {}
        for name, h in s.items():
            rel = os.path.join(sub[key], name)
            if rel in files:
                held[name] = "equal" if files[rel]["sha256"] == h else "DIFFERENT"
            else:
                held[name] = "not retained here"
        unlisted = [f for f in files if f.startswith(sub[key] + "/") and os.path.basename(f) not in s and not f.endswith("SHA256SUMS")]
        report["packets"][key] = {"files": files, "sha256sums": held, "retained_but_unlisted": unlisted}
    # Across pins.
    a, b = all_sums["942@a9486ed"], all_sums["addendum@a0c4fc8"]
    report["a9486ed_vs_a0c4fc8"] = {
        "names_only_at_a0c4fc8": sorted(set(b) - set(a)),
        "names_only_at_a9486ed": sorted(set(a) - set(b)),
        "shared_names_with_different_digest": sorted(k for k in set(a) & set(b) if a[k] != b[k]),
    }
    report["verify_cert_py_digest_at_each_pin"] = {k: v.get("verify_cert.py") for k, v in all_sums.items()}
    # README tables against the reports.
    with open(issues_path) as fh:
        iss = json.load(fh)
    body = {f"#{i['number']}": i["body"] for i in iss["issues"]}
    body["comment"] = iss["comments"][0]["body"]

    def readme(key):
        with open(os.path.join(packets[key], sub[key], "README.md")) as fh:
            return fh.read()

    cmp = {}
    r941, t941 = rows(readme("941@71da0d5"), 3), rows(body["#941"], 3)
    cmp["#941 vs above324/README.md"] = {"rows": len(t941), "equal": r941 == t941}
    r942, t942 = rows(readme("942@a9486ed"), 4), rows(body["#942"], 4)
    cmp["#942 vs above324_refined/README.md at a9486ed"] = {"rows": len(t942), "equal": r942 == t942}
    ra, tc = rows(readme("addendum@a0c4fc8"), 4), rows(body["comment"], 4)
    cmp["comment vs above324_refined/README.md at a0c4fc8, its six rows"] = {
        "rows": len(tc),
        "equal": {n: ra.get(n) for n in tc} == tc,
    }
    cmp["a0c4fc8 README's other sixteen rows vs #942"] = {"equal": {n: ra.get(n) for n in t942} == t942}
    cmp["a0c4fc8 README rows"] = len(ra)
    report["readme_tables"] = cmp
    with open(out_path, "w") as fh:
        json.dump(report, fh, indent=1)
        fh.write("\n")
    for k, v in report["packets"].items():
        print(k, {n: s for n, s in v["sha256sums"].items() if s != "equal"}, "unlisted:", v["retained_but_unlisted"])
    print("pins:", report["a9486ed_vs_a0c4fc8"])
    print("verify_cert.py:", report["verify_cert_py_digest_at_each_pin"])
    print("tables:", cmp)


if __name__ == "__main__":
    main()
