"""Stream-scan sq19's release archives: digests, forbidden constructs, native facts.

Reads one `sq19-generated-*.tar.xz` from a path or from standard input (so it can be
piped from curl without storing the archive), and for that archive
  * computes its SHA-256 and compares it with the retained SHA256SUMS digest;
  * checks every member against expected/generated-sources.sha256 (path and SHA-256);
  * counts, per member, declarations or commands that would widen the trust
    boundary beyond the `native_decide` facts: `axiom`, `sorry`, `admit`,
    `implemented_by`, `extern`, `unsafe`, `opaque`, `skipKernelTC`, `debug.`,
    `elab`, `macro`, `syntax`, `run_cmd`, `#eval`, `initialize`, `@[csimp]`;
  * counts the theorems proved `by native_decide` and lists their full names, so
    the union over the five archives can be compared with expected/axioms.txt.
It never extracts to disk and runs nothing it reads.

    curl -sSfL URL | python -I scan_archives.py SQ19_DIR NAME - --json OUT
    python -I scan_archives.py SQ19_DIR NAME ARCHIVE --json OUT

Standard library only.
"""

import argparse
import hashlib
import json
import re
import sys
import tarfile

FORBIDDEN = re.compile(
    rb"(?m)^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*"
    rb"(axiom|opaque|unsafe|elab|macro|syntax|run_cmd|#eval|initialize|builtin_initialize)\b"
    rb"|\bsorry\b|\badmit\b|implemented_by|@\[extern|skipKernelTC|\bdebug\.|@\[csimp")
THEOREM = re.compile(rb"(?m)^(?:private\s+)?theorem\s+(\S+)")
NAMESPACE = re.compile(rb"(?m)^(namespace|end)[ \t]+(\S+)")


class Hashing:
    def __init__(self, f):
        self.f, self.h, self.n = f, hashlib.sha256(), 0

    def read(self, k=-1):
        b = self.f.read(k)
        self.h.update(b)
        self.n += len(b)
        return b


def strip_comments(text):
    text = re.sub(rb"/-.*?-/", b"", text, flags=re.S)
    return re.sub(rb"--[^\n]*", b"", text)


def native_theorems(text):
    """Full names of theorems whose proof (up to the next declaration) uses native_decide."""
    out, ns = [], []
    events = sorted([(m.start(), "ns", m) for m in NAMESPACE.finditer(text)]
                    + [(m.start(), "thm", m) for m in THEOREM.finditer(text)], key=lambda e: e[0])
    starts = [e[0] for e in events] + [len(text)]
    for k, (pos, kind, m) in enumerate(events):
        if kind == "ns":
            if m.group(1) == b"namespace":
                ns.append(m.group(2).decode())
            elif ns:
                ns.pop()
            continue
        body = text[pos:starts[k + 1]]
        if b"native_decide" in body:
            out.append(".".join(ns + [m.group(1).decode()]))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("sq19")
    ap.add_argument("name", help="archive file name, e.g. sq19-generated-S3438.tar.xz")
    ap.add_argument("archive", help="path, or - for standard input")
    ap.add_argument("--sums", help="SHA256SUMS of the release (default: compare nothing)")
    ap.add_argument("--json")
    a = ap.parse_args()
    expected = {}
    for line in open(a.sq19 + "/expected/generated-sources.sha256", encoding="utf-8"):
        if line.strip():
            h, p = line.split("  ", 1)
            expected[p.strip()] = h
    raw = sys.stdin.buffer if a.archive == "-" else open(a.archive, "rb")
    src = Hashing(raw)
    members, mismatched, unexpected, hits, natives, nbytes = 0, [], [], [], [], 0
    with tarfile.open(fileobj=src, mode="r|xz") as tf:
        for ti in tf:
            if not ti.isfile():
                continue
            data = tf.extractfile(ti).read()
            members += 1
            nbytes += len(data)
            path = ti.name.removeprefix("./")
            h = hashlib.sha256(data).hexdigest()
            if path not in expected:
                unexpected.append(path)
            elif expected[path] != h:
                mismatched.append(path)
            if path.endswith(".lean"):
                code = strip_comments(data)
                for m in FORBIDDEN.finditer(code):
                    hits.append({"file": path, "match": m.group(0).decode(errors="replace").strip()[:80]})
                natives.extend(native_theorems(code))
    while src.read(1 << 20):
        pass
    digest = src.h.hexdigest()
    want = None
    if a.sums:
        for line in open(a.sums, encoding="utf-8"):
            h, n = line.split()
            if n == a.name:
                want = h
    res = {"archive": a.name, "sha256": digest, "sha256_matches_sums": want == digest if want else None,
           "compressed_bytes": src.n, "members": members, "uncompressed_bytes": nbytes,
           "digest_mismatches": mismatched, "unlisted_members": unexpected,
           "forbidden_hits": hits, "native_theorems": len(natives), "native_names": sorted(natives)}
    print(f"{a.name}: sha256 {digest[:16]}... match {res['sha256_matches_sums']}, {members} members, "
          f"{nbytes:,} bytes, {len(mismatched)} digest mismatches, {len(unexpected)} unlisted, "
          f"{len(hits)} forbidden hits, {len(natives)} native theorems")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(res, f, indent=1)
    ok = not mismatched and not unexpected and not hits and res["sha256_matches_sums"] is not False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
