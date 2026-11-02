"""The cube-root preprint's citations of the quarter-power preprint, resolved.

The cube-root preprint (C) cites results of the quarter-power preprint (Q) by number
("[Q, Theorem 8.3(a)]", "Proposition 5.10", "(6.1)"). This program numbers Q's
theorem-like environments, subsections and equations as amsart does for Q's preamble
(one counter per section, shared by theorem, proposition, lemma, corollary, claim,
definition, example, notation and remark; equations numbered within sections), and
resolves every number C cites to Q's environment, its label and its title, so that a
reader can check each citation against the statement it names. It decides only the
resolution, and that the cited kind (Theorem, Lemma, ...) is the kind at that number.

Usage: python -I c_citations.py Q_TEX C_TEX OUT.json
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ENVS = ("theorem", "proposition", "lemma", "corollary", "claim", "definition", "example", "notation", "remark")
EQ_ENVS = ("equation", "align", "gather", "multline")


def number_q(qtex: str) -> dict[str, dict[str, str]]:
    body = qtex[qtex.index("\\begin{document}"):]
    sec, thm, sub, eq = 0, 0, 0, 0
    out: dict[str, dict[str, str]] = {}
    token = re.compile(
        r"\\section\*?\{|\\subsection\*?\{|\\begin\{(" + "|".join(ENVS + EQ_ENVS) + r")(\*?)\}(\[[^\]]*\])?|\\tag\{|\\nonumber|\\notag|\\\\"
    )
    pos = 0
    open_eq: str | None = None
    for m in token.finditer(body):
        t = m.group(0)
        if t.startswith("\\section"):
            if t.startswith("\\section*"):
                continue
            sec += 1
            thm = sub = eq = 0
            continue
        if t.startswith("\\subsection"):
            if t.startswith("\\subsection*"):
                continue
            sub += 1
            title = body[m.end(): body.index("}", m.end())]
            lab = re.search(r"\\label\{([^}]*)\}", body[m.end(): m.end() + 300])
            out[f"Section {sec}.{sub}"] = {"kind": "Section", "title": title, "label": lab.group(1) if lab else ""}
            continue
        env = m.group(1)
        if env in ENVS:
            if m.group(2) == "*":
                continue
            thm += 1
            num = f"{sec}.{thm}"
            lab = re.search(r"\\label\{([^}]*)\}", body[m.end(): m.end() + 400])
            title = (m.group(3) or "").strip("[]")
            out[f"{env.capitalize()} {num}"] = {"kind": env.capitalize(), "title": title,
                                               "label": lab.group(1) if lab else ""}
            out[num] = out[f"{env.capitalize()} {num}"]
        elif env in EQ_ENVS and m.group(2) != "*":
            # Number each line of the display that is not \nonumber'd: count the lines.
            end = body.index("\\end{" + env + "}", m.end())
            block = body[m.end(): end]
            if env == "equation":
                lines = [block]
            else:
                lines = re.split(r"\\\\", block)
            for line in lines:
                if "\\nonumber" in line or "\\notag" in line or "\\tag" in line:
                    continue
                eq += 1
                lab = re.search(r"\\label\{([^}]*)\}", line)
                out[f"({sec}.{eq})"] = {"kind": "Equation", "title": "", "label": lab.group(1) if lab else ""}
    return out


def main(qpath: Path, cpath: Path, out: Path) -> int:
    qtex, ctex = qpath.read_text(), cpath.read_text()
    qnum = number_q(qtex)
    cbody = ctex[ctex.index("\\begin{document}"):]
    # Every [Q, ...] bracket, and the list items of C's "Results used" subsection.
    cites: list[tuple[str, str]] = []
    for m in re.finditer(r"\[Q,\s*([^\]]*)\]", cbody):
        cites.append((m.group(1), cbody[max(0, m.start() - 80): m.end() + 20]))
    ru = cbody[cbody.index("\\subsection{Results used}"): cbody.index("\\section{The tilt budget}")]
    for line in ru.split("\\item")[1:]:
        if "From [R]" in line:
            line = line.split("From [R]")[0]
        line = re.sub(r"\[R,[^\]]*\]", "", line)  # citations of [R] inside an item about [Q]
        cites.append((line.strip(), "Results used"))
    pat = re.compile(r"(Theorems?|Lemmas?|Propositions?|Corollar(?:y|ies)|Definitions?|Remarks?|Sections?)~?(\d+\.\d+)((?:\([a-z]\)(?:--\([a-z]\))?(?:,\([a-z]\))*)?)"
                     r"((?:(?:,\s*|\s+and~?|~and~)\d+\.\d+(?:\([a-z]\)(?:--\([a-z]\))?(?:,\([a-z]\))*)?)*)|\((\d+\.\d+)\)")
    resolved: list[dict[str, object]] = []
    for text, ctx in cites:
        for m in pat.finditer(text):
            if m.group(5):
                key = f"({m.group(5)})"
                hit = qnum.get(key)
                resolved.append({"cited": key, "context": ctx[:120], "resolves_to": hit, "kind_ok": hit is not None})
                continue
            kind = m.group(1)
            base = kind.rstrip("s")
            base = {"Corollarie": "Corollary", "Corollar": "Corollary"}.get(base, base)
            if base.startswith("Corollar"):
                base = "Corollary"
            nums = [m.group(2)] + re.findall(r"\d+\.\d+", m.group(4) or "")
            for n in nums:
                if base == "Section":
                    hit = qnum.get(f"Section {n}")
                    ok = hit is not None
                else:
                    hit = qnum.get(n)
                    ok = hit is not None and hit["kind"] == base
                resolved.append({"cited": f"{base} {n}{m.group(3) if n == m.group(2) else ''}", "context": ctx[:120],
                                 "resolves_to": hit, "kind_ok": ok})
    uniq: dict[str, dict[str, object]] = {}
    for row in resolved:
        uniq.setdefault(str(row["cited"]), row)
    receipt = {
        "program": "c_citations.py",
        "program_sha256": hashlib.sha256(Path(__file__).resolve().read_bytes()).hexdigest(),
        "inputs_sha256": {p.name + ("" if p is qpath else "(C)"): hashlib.sha256(p.read_bytes()).hexdigest() for p in (qpath, cpath)},
        "q_numbering_size": len(qnum),
        "citations": sorted(uniq.values(), key=lambda r: str(r["cited"])),
        "summary": {"distinct_citations": len(uniq), "kind_ok": sum(1 for r in uniq.values() if r["kind_ok"])},
    }
    out.write_text(json.dumps(receipt, indent=1) + "\n")
    print(receipt["summary"])
    for row in receipt["citations"]:
        hit = row["resolves_to"] or {}
        print(f"{row['cited']:<28} -> {hit.get('kind','?'):<12} {hit.get('label',''):<26} {hit.get('title','')[:50]}  {'ok' if row['kind_ok'] else 'MISMATCH'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])))
