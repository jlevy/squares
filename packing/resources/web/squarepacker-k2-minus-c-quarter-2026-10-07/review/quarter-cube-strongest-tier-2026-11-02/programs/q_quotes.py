"""Q's quotations of [R] against [R]'s own text.

Section 2 of the quarter-power preprint (Q) quotes the statements of [R] (Ryu,
k2-minus-c v1.2) "verbatim", adapting only cross-references, and Remarks 2.2 and 2.4
and Proposition 2.1 quote sentences from [R]'s proofs and remarks. This program
extracts every quoted statement and sentence from Q's TeX and finds it in [R]'s TeX,
after replacing every \\ref{...}, \\label{...} and \\cite{...} by a placeholder and
collapsing white space. It decides fidelity of quotation only, not the mathematics.

Usage: python -I q_quotes.py Q_TEX R_TEX OUT.json
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

# Q's quoted statement (ImpStatement number) -> [R]'s environment label.
LABELS = {
    "2.1": "lem:red", "3.1": "lem:geom", "3.2": "lem:G", "3.3": "cor:W1", "3.4": "lem:A", "3.5": "lem:E",
    "4.1": "lem:cg", "4.2": "lem:bd", "4.3": "prop:FL", "4.4": "lem:cone", "4.5": "prop:FLpar",
    "4.8": "lem:count", "4.9": "lem:Kw", "4.10": "lem:Kw9", "4.12": "lem:slit", "4.13": "lem:Bh",
    "4.14": "lem:Bv", "4.15": "lem:Eline",
}


def norm(s: str) -> str:
    s = re.sub(r"%[^\n]*", "", s)
    s = re.sub(r"\\(?:ref|eqref|label|cite)\{[^}]*\}", "@", s)
    s = re.sub(r"\\cite\[[^\]]*\]\{[^}]*\}", "@", s)
    s = s.replace("~", " ")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def r_env(rtex: str, label: str) -> str | None:
    m = re.search(r"\\begin\{(lemma|proposition|corollary|theorem)\}(\[[^\]]*\])?\\label\{" + re.escape(label) + r"\}(.*?)\\end\{\1\}",
                  rtex, re.S)
    return None if m is None else m.group(3)


def repo_path(p: Path) -> str:
    """The input's path from the repository root, or as given outside a checkout.

    Both inputs are named paper.tex, so a key by file name would keep one digest.
    """
    resolved = p.resolve()
    for parent in resolved.parents:
        if (parent / ".git").exists():
            return resolved.relative_to(parent).as_posix()
    return p.as_posix()


def main(qpath: Path, rpath: Path, out: Path) -> int:
    qtex, rtex = qpath.read_text(), rpath.read_text()
    rn = norm(rtex)
    rows: list[dict[str, object]] = []
    for m in re.finditer(r"\\begin\{ImpStatement\}\{(\w+)\}\{([\d.]+)\}\\label\{([^}]*)\}(.*?)\\end\{ImpStatement\}", qtex, re.S):
        kind, num, qlabel, body = m.group(1), m.group(2), m.group(3), m.group(4)
        qb = norm(body)
        row: dict[str, object] = {"quote": f"{kind} {num}", "q_label": qlabel}
        if num == "4.11":
            # Only the first sentence is quoted, ending in [\dots].
            first = qb.replace("[\\dots]", "").strip()
            row["r_source"] = "the remark after Lemma 4.10 (lem:Kw9)"
            row["match"] = first in rn
            row["kind"] = "prefix of the remark"
        else:
            rb = r_env(rtex, LABELS[num])
            row["r_source"] = LABELS[num]
            row["match"] = rb is not None and norm(rb) == qb
            row["kind"] = "whole statement"
            if not row["match"] and rb is not None:
                a, b = norm(rb), qb
                i = 0
                while i < min(len(a), len(b)) and a[i] == b[i]:
                    i += 1
                row["first_difference"] = {"r": a[max(0, i - 40): i + 60], "q": b[max(0, i - 40): i + 60]}
        rows.append(row)
    # Quoted sentences, as Q prints them inside ``...''.
    sentences = []
    rn_plain = re.sub(r"\\emph\{([^}]*)\}", r"\1", rn)
    for m in re.finditer(r"``(.*?)''", qtex, re.S):
        s = norm(m.group(1))
        if len(s) < 25:
            continue
        if "\\Fs" in s or "T_s" in s:
            # Q's own phrases about its scale flows, not quotations of [R].
            continue
        # Q prints [R]'s numbers (Lemma~4.10, Section~6) where [R] may have \ref; let each
        # numbered reference match either the placeholder or the literal number.
        pat = re.escape(s)
        pat = re.sub(r"(Lemma|Lemmas|Section|Proposition|Remark|Corollary)\\ (\d+(?:\\\.\d+)?)",
                     lambda mm: mm.group(1) + r"\ (?:@|" + mm.group(2) + ")", pat)
        found = re.search(pat, rn) is not None
        emph_only = False
        if not found and re.search(pat, rn_plain) is not None:
            found, emph_only = True, True
        row = {"quote": s[:160], "found_in_R": found}
        if emph_only:
            row["note"] = "found after removing \\emph from [R]'s text: Q drops one emphasis"
        sentences.append(row)
    digests = {repo_path(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in (qpath, rpath)}
    here = Path(__file__).resolve()
    receipt = {
        "program": "q_quotes.py",
        "program_sha256": hashlib.sha256(here.read_bytes()).hexdigest(),
        "inputs_sha256": digests,
        "statements": rows,
        "sentences": sentences,
        "summary": {
            "statements": len(rows),
            "statements_matching": sum(1 for r in rows if r["match"]),
            "sentences": len(sentences),
            "sentences_found": sum(1 for s in sentences if s["found_in_R"]),
        },
    }
    out.write_text(json.dumps(receipt, indent=1) + "\n")
    print(receipt["summary"])
    for r in rows:
        if not r["match"]:
            print("MISMATCH", r)
    for s in sentences:
        if not s["found_in_R"]:
            print("NOT FOUND:", s["quote"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])))
