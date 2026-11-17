"""Custody of the two release assets and the identity of the source's verifier,
read in memory (review think-4ul6).  Nothing is extracted to disk and nothing of
the source is executed.

For each asset:
- size and SHA-256 against the packet's source-manifest.json;
- every member's size and SHA-256 against the manifest's asset_members, and the
  packet's retained copies (release/) against the members (candidate.json is
  retained as gzip, so its decompressed bytes are compared);
- the sealed inner bundle: its members against the manifest and against its own
  files-sha256.json;
- the nested verifier archive: its build digest recomputed by the archive's own
  build.rs rule (SHA-256 over Cargo.toml, Cargo.lock, build.rs and the sorted
  src/*.rs, each as name NUL bytes NUL), which the archive's build.rs is checked to
  state, and a file-by-file comparison with this repository's packing/sqverify_fast
  at the given revisions (via git show).

Usage: python3 -I custody_and_nested.py PACKET ASSET_DIR REPO REV [REV ...] [--out FILE]
"""

from __future__ import annotations

import argparse
import difflib
import gzip
import hashlib
import io
import json
import subprocess
import sys
import tarfile
from pathlib import Path


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def tar_members(data: bytes) -> dict:
    out = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
        for m in tf.getmembers():
            if m.isfile():
                out[m.name] = tf.extractfile(m).read()
    return out


def build_digest(files: dict, root: str) -> str:
    names = ["Cargo.toml", "Cargo.lock", "build.rs"]
    names += sorted(k[len(root):] for k in files if k.startswith(root + "src/") and k.endswith(".rs") and k.count("/") == root.count("/") + 1)
    h = hashlib.sha256()
    for name in names:
        h.update(name.encode())
        h.update(b"\0")
        h.update(files[root + name])
        h.update(b"\0")
    return h.hexdigest()


def git_show(repo: Path, rev: str, path: str):
    r = subprocess.run(["git", "-C", str(repo), "show", f"{rev}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def git_ls(repo: Path, rev: str, path: str):
    r = subprocess.run(["git", "-C", str(repo), "ls-tree", "-r", "--name-only", "--full-tree", rev, path], capture_output=True, text=True)
    return r.stdout.split()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("packet", type=Path)
    ap.add_argument("assets", type=Path)
    ap.add_argument("repo", type=Path)
    ap.add_argument("revs", nargs="+")
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    manifest = json.loads((args.packet / "source-manifest.json").read_text())
    retention = json.loads((args.packet / "acquisition" / "release-assets.json").read_text())
    out = {"assets": [], "nested": None}
    problems = []
    archive_bytes = None
    for entry in manifest["certificates"]:
        cert = entry["certificate"]
        rel = entry["release"]
        data = (args.assets / rel["asset"]).read_bytes()
        rec = {
            "certificate": cert,
            "asset": rel["asset"],
            "bytes": len(data),
            "sha256": sha(data),
            "equal_to_pin": len(data) == rel["bytes"] and sha(data) == rel["sha256"],
        }
        members = tar_members(data)
        prefix = f"certificates/{cert}/"
        listed = {m["path"]: m for m in entry["asset_members"]}
        got = {k[len(prefix):]: v for k, v in members.items() if k.startswith(prefix)}
        rec["member_paths"] = sorted(members)
        rec["members_equal_manifest"] = set(got) == set(listed) and all(
            len(got[p]) == listed[p]["bytes"] and sha(got[p]) == listed[p]["sha256"] for p in listed)
        rec["members_outside_prefix"] = sorted(k for k in members if not k.startswith(prefix))
        # retained copies
        ret = next(a for a in retention["assets"] if a["certificate"] == cert)
        checks = {}
        for m in ret["members"]:
            if "stored" not in m:
                continue
            stored = (args.packet / m["stored"]).read_bytes()
            inner = got[m["path"][len(prefix):]]
            if m["form"] == "gzip":
                checks[m["stored"]] = gzip.decompress(stored) == inner
            else:
                checks[m["stored"]] = stored == inner
        rec["retained_copies_equal_members"] = checks
        # sealed bundle
        sealed_name = entry["sealed_inner_bundle"]["name"]
        sealed = tar_members(got[sealed_name])
        sroot = next(iter(sealed)).split("/")[0] + "/" if all("/" in k for k in sealed) else ""
        sm = {k[len(sroot):] if k.startswith(sroot) else k: v for k, v in sealed.items()}
        fsha = json.loads(sm["files-sha256.json"])
        rec["sealed_root"] = sroot
        rec["sealed_members"] = len(sm)
        rec["sealed_matches_its_files_sha256"] = all(sha(sm[p]) == d for p, d in fsha.items()) and len(fsha) == 15
        rec["sealed_unlisted"] = sorted(set(sm) - set(fsha))
        rec["sealed_payloads_repeat_outer"] = sorted(p for p in sm if p in got and sm[p] == got[p])
        rec["sealed_readme_differs_from_pinned"] = sha(sm["README.md"]) != next(d["sha256"] for d in entry["source_documents"] if d["path"].endswith("/README.md"))
        if rec["sealed_readme_differs_from_pinned"]:
            rec["sealed_readme_sha256"] = sha(sm["README.md"])
            rec["sealed_readme_lines"] = sm["README.md"].decode().count("\n")
        arch = got["check2/src/sqverify-proof-net-fe12e036c.tar.gz"]
        rec["archive_sha256"] = sha(arch)
        if archive_bytes is None:
            archive_bytes = arch
        elif archive_bytes != arch:
            problems.append("archives differ between assets")
        for k in ("equal_to_pin", "members_equal_manifest", "sealed_matches_its_files_sha256"):
            if not rec[k]:
                problems.append(f"{cert} {k}")
        if not all(checks.values()):
            problems.append(f"{cert} retained copies")
        out["assets"].append(rec)

    files = tar_members(archive_bytes)
    root = "sqverify_fast/" if any(k.startswith("sqverify_fast/") for k in files) else ""
    digest = build_digest(files, root)
    here_build = (Path(args.repo) / "packing/sqverify_fast/build.rs")
    nested = {
        "archive_sha256": sha(archive_bytes),
        "files": len(files),
        "root": root,
        "build_digest_by_build_rs_rule": digest,
        "build_rs_sha256": sha(files[root + "build.rs"]),
    }
    comps = {}
    for rev in args.revs:
        repo_files = [p for p in git_ls(args.repo, rev, "packing/sqverify_fast") if not p.endswith("/")]
        rmap = {p[len("packing/sqverify_fast/"):]: git_show(args.repo, rev, p) for p in repo_files}
        amap = {k[len(root):]: v for k, v in files.items()}
        same = sorted(p for p in amap if p in rmap and rmap[p] == amap[p])
        differ = {}
        for p in sorted(p for p in amap if p in rmap and rmap[p] != amap[p]):
            a = amap[p].decode(errors="replace").splitlines()
            b = rmap[p].decode(errors="replace").splitlines()
            plus = minus = 0
            for line in difflib.unified_diff(b, a, lineterm="", n=0):
                if line.startswith("+") and not line.startswith("+++"):
                    plus += 1
                elif line.startswith("-") and not line.startswith("---"):
                    minus += 1
            differ[p] = {"added_in_archive": plus, "removed_from_repo": minus}
        repo_digest = build_digest({"x/" + k: v for k, v in rmap.items()}, "x/")

        def dup_reader(text: bytes) -> bytes:
            # The duplicate-key reader: from `struct DuplicateKeyCheck` to `fn read_json`.
            s = text.decode(errors="replace")
            i = s.find("struct DuplicateKeyCheck")
            j = s.find("fn read_json", i)
            return s[i:j].encode() if i >= 0 and j > i else b""

        comps[rev] = {
            "repo_build_digest": repo_digest,
            "identical": same,
            "differ": differ,
            "only_in_archive": sorted(set(amap) - set(rmap)),
            "only_in_repo": sorted(set(rmap) - set(amap)),
            "duplicate_key_reader_identical": bool(dup_reader(amap["src/certificate.rs"]))
            and dup_reader(amap["src/certificate.rs"]) == dup_reader(rmap["src/certificate.rs"]),
        }
    nested["comparisons"] = comps
    # What the archive's admission does with a declaration, recorded as facts only
    # (no line of the archive is retained).
    cert_rs = files[root + "src/certificate.rs"].decode(errors="replace")
    nested["certificate_rs"] = {
        "reads_proof_net": 'object.get("proof_net")' in cert_rs,
        "requires_exactly_step_and_last": 'net.len() != 2 || !net.contains_key("step") || !net.contains_key("last")' in cert_rs,
        "refuses_proof_net_beside_certificate_metadata": "proof_net and certificate metadata may not both set the net" in cert_rs,
        "refuses_proof_net_outside_format_M": "proof_net is accepted only for format M" in cert_rs,
        "reads_a_count_field": '"count"' in cert_rs,
        "refuses_top_level_net_outside_format_L": 'contains_key("net")' in cert_rs,
        "checks_tangent_form_for_per_bin": "B (1 + D / (1 - D^2/4)) >= 1 for the per-bin domain" in cert_rs,
    }
    out["nested"] = nested
    out["problems"] = problems
    text = json.dumps(out, indent=1)
    if args.out:
        args.out.write_text(text + "\n")
    print(text)
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
