"""Custody of the release asset of mixed_n29_L582 and the identity of the
source's verifier, read in memory (review think-1lri).  Nothing is extracted to
disk and nothing of the source is executed.  Adapted from the n = 28 and n = 30
review's program to this packet's single-asset manifest.

- the asset's size and SHA-256 against source-manifest.json;
- every member's size and SHA-256 against the manifest's asset_members, and the
  packet's retained copies (release/) against the members (candidate.json is
  retained as gzip, so its decompressed bytes are compared; the retained .gz must
  be one member);
- the sealed inner bundle: its members against the manifest and against its own
  files-sha256.json, which payloads repeat the outer asset's, and its README
  against the pinned one;
- the nested verifier archive: its digest against the one the 8 October packet
  pins, its build digest recomputed by the crate's build.rs rule (SHA-256 over
  Cargo.toml, Cargo.lock, build.rs and the sorted src/*.rs, each as name NUL bytes
  NUL), and a file-by-file comparison with packing/sqverify_fast at the given
  revisions (git show), with the facts of admission the review reads, recorded as
  booleans only.

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
import zlib
from pathlib import Path


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_blob(b: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def tar_members(data: bytes) -> dict:
    out = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
        for m in tf.getmembers():
            if m.isfile():
                out[m.name] = tf.extractfile(m).read()
    return out


def tar_kinds(data: bytes) -> dict:
    kinds: dict = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
        for m in tf.getmembers():
            k = "file" if m.isfile() else "dir" if m.isdir() else "link" if (m.issym() or m.islnk()) else "other"
            kinds[k] = kinds.get(k, 0) + 1
    return kinds


def build_digest(files: dict, root: str) -> str:
    names = ["Cargo.toml", "Cargo.lock", "build.rs"]
    names += sorted(k[len(root):] for k in files
                    if k.startswith(root + "src/") and k.endswith(".rs") and k.count("/") == root.count("/") + 1)
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
    r = subprocess.run(["git", "-C", str(repo), "ls-tree", "-r", "--name-only", "--full-tree", rev, path],
                       capture_output=True, text=True)
    return r.stdout.split()


def one_member(raw: bytes) -> bool:
    d = zlib.decompressobj(wbits=31)
    d.decompress(raw)
    d.flush()
    return d.eof and not d.unused_data


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
    problems = []
    rel = manifest["release"]
    data = (args.assets / rel["asset"]).read_bytes()
    cert = retention["assets"][0]["certificate"]
    rec = {
        "certificate": cert,
        "asset": rel["asset"],
        "bytes": len(data),
        "sha256": sha(data),
        "equal_to_pin": len(data) == rel["bytes"] and sha(data) == rel["sha256"] == rel["api_digest"].split(":")[1],
        "tar_entry_kinds": tar_kinds(data),
    }
    members = tar_members(data)
    prefix = f"certificates/{cert}/"
    listed = {m["path"]: m for m in manifest["asset_members"]}
    got = {k[len(prefix):]: v for k, v in members.items() if k.startswith(prefix)}
    rec["member_paths"] = sorted(members)
    rec["members_outside_prefix"] = sorted(k for k in members if not k.startswith(prefix))
    rec["members_equal_manifest"] = set(got) == set(listed) and all(
        len(got[p]) == listed[p]["bytes"] and sha(got[p]) == listed[p]["sha256"] and git_blob(got[p]) == listed[p]["git_blob"]
        for p in listed)
    checks = {}
    for m in retention["assets"][0]["members"]:
        if "stored" not in m:
            continue
        stored = (args.packet / m["stored"]).read_bytes()
        inner = got[m["path"][len(prefix):]]
        if m["form"] == "gzip":
            checks[m["stored"]] = one_member(stored) and gzip.decompress(stored) == inner
        else:
            checks[m["stored"]] = stored == inner
    rec["retained_copies_equal_members"] = checks
    retained_files = sorted(str(p.relative_to(args.packet)) for p in (args.packet / "release").rglob("*") if p.is_file())
    rec["retained_files"] = retained_files
    rec["retained_files_are_exactly_the_stored_members"] = retained_files == sorted(checks)
    sealed_name = manifest["sealed_inner_bundle"]["name"]
    sealed = tar_members(got[sealed_name])
    roots = {k.split("/")[0] for k in sealed}
    sroot = (next(iter(roots)) + "/") if len(roots) == 1 and all("/" in k for k in sealed) else ""
    sm = {k[len(sroot):]: v for k, v in sealed.items()}
    fsha = json.loads(sm["files-sha256.json"])
    smanifest = {m["path"]: m for m in manifest["sealed_inner_bundle"]["members"]}
    rec["sealed"] = {
        "root": sroot,
        "members": len(sm),
        "equal_manifest": set(sm) == set(smanifest) and all(sha(sm[p]) == smanifest[p]["sha256"] and len(sm[p]) == smanifest[p]["bytes"] for p in sm),
        "matches_its_files_sha256": all(p in sm and sha(sm[p]) == d for p, d in fsha.items()),
        "files_sha256_entries": len(fsha),
        "unlisted_in_its_files_sha256": sorted(set(sm) - set(fsha)),
        "payloads_repeating_outer": sorted(p for p in sm if p in got and sm[p] == got[p]),
        "readme_sha256": sha(sm["README.md"]),
    }
    pinned_readme = next(d for d in manifest["source_documents"] if d["path"].endswith("/README.md"))
    rec["sealed"]["readme_differs_from_pinned"] = rec["sealed"]["readme_sha256"] != pinned_readme["sha256"]
    rec["sealed"]["files_sha256_readme_entry_is_sealed_edition"] = fsha.get("README.md") == rec["sealed"]["readme_sha256"]
    docs_in_sealed = {}
    for d in manifest["source_documents"]:
        rel_path = d["path"].split(prefix, 1)[1]
        if rel_path in sm:
            docs_in_sealed[rel_path] = sha(sm[rel_path]) == d["sha256"]
    rec["sealed"]["pinned_documents_equal_sealed_copies"] = docs_in_sealed
    arch_name = "check2/src/sqverify-proof-net-fe12e036c.tar.gz"
    arch = got[arch_name]
    rec["archive_sha256"] = sha(arch)
    rec["archive_equals_common_verifier_source"] = sha(arch) == manifest["common_verifier_source"]["sha256"]
    rec["archive_in_sealed_bundle_identical"] = sm.get(arch_name) == arch
    for k in ("equal_to_pin", "members_equal_manifest", "archive_equals_common_verifier_source"):
        if not rec[k]:
            problems.append(k)
    if not all(checks.values()) or not rec["retained_files_are_exactly_the_stored_members"]:
        problems.append("retained copies")
    if not (rec["sealed"]["equal_manifest"] and rec["sealed"]["matches_its_files_sha256"]):
        problems.append("sealed bundle")

    files = tar_members(arch)
    root = "sqverify_fast/" if any(k.startswith("sqverify_fast/") for k in files) else ""
    digest = build_digest(files, root)
    nested = {
        "archive_sha256": sha(arch),
        "files": len(files),
        "tar_entry_kinds": tar_kinds(arch),
        "root": root,
        "build_digest_by_build_rs_rule": digest,
        "build_digest_equals_declared": digest == manifest["common_verifier_source"]["declared_build_digest"],
        "build_rs_sha256": sha(files[root + "build.rs"]),
    }
    if not nested["build_digest_equals_declared"]:
        problems.append("nested build digest")
    comps = {}
    amap = {k[len(root):]: v for k, v in files.items()}
    for rev in args.revs:
        repo_files = [p for p in git_ls(args.repo, rev, "packing/sqverify_fast") if not p.endswith("/")]
        rmap = {p[len("packing/sqverify_fast/"):]: git_show(args.repo, rev, p) for p in repo_files}
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

        def dup_reader(text: bytes) -> bytes:
            s = text.decode(errors="replace")
            i = s.find("struct DuplicateKeyCheck")
            j = s.find("fn read_json", i)
            return s[i:j].encode() if i >= 0 and j > i else b""

        comps[rev] = {
            "repo_build_digest": build_digest({"x/" + k: v for k, v in rmap.items()}, "x/"),
            "identical": same,
            "differ": differ,
            "only_in_archive": sorted(set(amap) - set(rmap)),
            "only_in_repo": sorted(set(rmap) - set(amap)),
            "duplicate_key_reader_found": bool(dup_reader(rmap["src/certificate.rs"])),
            "duplicate_key_reader_identical": bool(dup_reader(amap["src/certificate.rs"]))
            and dup_reader(amap["src/certificate.rs"]) == dup_reader(rmap["src/certificate.rs"]),
        }
    nested["comparisons"] = comps
    cert_rs = amap["src/certificate.rs"].decode(errors="replace")
    nested["certificate_rs_facts"] = {
        "reads_proof_net": 'object.get("proof_net")' in cert_rs,
        "requires_exactly_step_and_last": 'net.len() != 2 || !net.contains_key("step") || !net.contains_key("last")' in cert_rs,
        "refuses_proof_net_beside_certificate_metadata": "proof_net and certificate metadata may not both set the net" in cert_rs,
        "refuses_proof_net_outside_format_M": "proof_net is accepted only for format M" in cert_rs,
        "reads_a_count_field": '"count"' in cert_rs,
        "refuses_top_level_net_outside_format_L": 'contains_key("net")' in cert_rs,
        "checks_tangent_form_for_per_bin": "B (1 + D / (1 - D^2/4)) >= 1 for the per-bin domain" in cert_rs,
    }
    out = {"asset": rec, "nested": nested, "problems": problems,
           "status": "CUSTODY_HOLDS" if not problems else "CUSTODY_PROBLEM"}
    text = json.dumps(out, indent=1)
    if args.out:
        args.out.write_text(text + "\n")
    print(text)
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
