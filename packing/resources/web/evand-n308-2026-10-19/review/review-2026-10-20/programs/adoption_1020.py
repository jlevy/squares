"""Compare each certificate exactly with its case ceiling and every other report at its
count, each side re-read from retained bytes.

Written for the stage 4 review of 20 October 2026. It decides nothing. Every side is
read here with a reader of this program's own, from the bytes the repository keeps, not
from the packets' frozen claim records:

- the case's verified ceiling from ``packing/frontier/n-NNN.md``'s front matter
  (``verified_upper_bound.exact_form``) and from the house witness
  (``witnesses/known-best/n-NNN.yaml``, its ``side``), which must agree;
- T-141 from ``hunt3_n308.cert``, T-135 from Fang's ``n0308.cert``, T-182 and T-172
  from Couzo's two ``n154.cert``, T-160 from ``tt_n154.cert`` (each file's header);
- #593 from Mishapolk's ``facts/n-154.yaml.gz`` and ``facts/n-308.yaml.gz`` (``side``).

It then holds the packets' ``acquisition/claims.json`` to these sides and differences,
prints every side smallest first rounded up at sixteen places with its difference from
the smallest, and holds the issue's twelve-place print to the certificate's side rounded
up at twelve places.

Usage, from ``packing/``::

    python -I adoption_1020.py --json OUT.json
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

WEB = Path("resources/web")
FRONTIER = Path("frontier")
WITNESSES = Path("witnesses/known-best")

CERTS = {
    308: ("evand-n308-2026-10-19", "source/search/packer/candidates/s308_d308.cert", "17.997149121271"),
    154: ("evand-n154-sweep-2026-10-20", "source/search/packer/candidates/s154_sw.cert", "12.921100940762"),
}
#: Other reports at the count: label -> (packet, path, how to read).
OTHERS = {
    308: {
        "T-141 (#489)": ("evand-record-hunt3-2026-10-10", "source/search/packer/candidates/hunt3_n308.cert", "cert"),
        "T-135 (#484)": ("fang-two-wedge-certificates-2026-10-10", "source/n0308/n0308.cert", "cert"),
        "#593": ("mishapolk-records-2026-10-14", "facts/n-308.yaml.gz", "fact"),
    },
    154: {
        "T-182 (#586)": ("couzo-certificates-2026-10-13", "source/certificates/n154.cert", "cert"),
        "T-172 (#583)": ("couzo-issue583-2026-10-13", "source/certificates/n154.cert", "cert"),
        "T-160 (#552)": ("evand-n154-2026-10-12", "source/search/packer/candidates/tt_n154.cert", "cert"),
        "#593": ("mishapolk-records-2026-10-14", "facts/n-154.yaml.gz", "fact"),
    },
}
HOUSE = {308: "T-174", 154: "T-186"}


def exact(text: str) -> Fraction:
    return Fraction(text.strip())


def cert_header(path: Path) -> tuple[int, Fraction]:
    for line in path.read_text("utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            n, s = line.split()
            return int(n), exact(s)
    raise ValueError(path)


def fact_side(path: Path, n: int) -> Fraction:
    text = gzip.decompress(path.read_bytes()).decode("utf-8")
    assert re.search(rf"^  n: {n}$", text, re.M), path
    match = re.search(r"^  side: (\S+)$", text, re.M)
    assert match, path
    return exact(match.group(1))


def witness_side(n: int) -> Fraction:
    text = (WITNESSES / f"n-{n}.yaml").read_text("utf-8")
    assert re.search(rf"^  n: {n}$", text, re.M)
    match = re.search(r"^  side: (\S+)$", text, re.M)
    assert match
    return exact(match.group(1))


def case_ceiling(n: int) -> Fraction:
    text = (FRONTIER / f"n-{n}.md").read_text("utf-8")
    block = re.search(r"^  verified_upper_bound:\n((?:    .*\n)+)", text, re.M)
    assert block, n
    match = re.search(r"^    exact_form: (\S+)$", block.group(1), re.M)
    assert match, n
    return exact(match.group(1))


def up(value: Fraction, places: int) -> str:
    scaled = -((-value.numerator * 10**places) // value.denominator)
    whole, rest = divmod(scaled, 10**places)
    return f"{whole}.{rest:0{places}d}"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args(argv)
    report: dict[str, object] = {}
    problems: list[str] = []
    for n, (packet, path, printed) in CERTS.items():
        count, side = cert_header(WEB / packet / path)
        assert count == n
        ceiling = case_ceiling(n)
        house = witness_side(n)
        if ceiling != house:
            problems.append(f"n={n}: case exact_form != house witness side")
        rows = {HOUSE[n] + " (case ceiling, house)": ceiling}
        for label, (opacket, opath, kind) in OTHERS[n].items():
            if kind == "cert":
                c, s = cert_header(WEB / opacket / opath)
                assert c == n
                rows[label] = s
            else:
                rows[label] = fact_side(WEB / opacket / opath, n)
        claims = json.loads((WEB / packet / "acquisition/claims.json").read_text("utf-8"))["results"][0]
        if exact(claims["exact_side"]) != side:
            problems.append(f"n={n}: claims.json exact_side differs")
        if exact(claims["case"]["exact_side"]) != ceiling or exact(claims["case"]["difference"]) != ceiling - side:
            problems.append(f"n={n}: claims.json case side or difference differs")
        for pending in claims["pending"]:
            label = pending["report"]
            if label not in rows:
                problems.append(f"n={n}: claims.json pending {label} not re-read here")
                continue
            if exact(pending["exact_side"]) != rows[label] or exact(pending["difference"]) != rows[label] - side:
                problems.append(f"n={n}: claims.json {label} side or difference differs")
        if up(side, 12) != printed:
            problems.append(f"n={n}: issue print {printed} != side rounded up at 12 places {up(side, 12)}")
        if claims["ceiling"] != up(side, 16):
            problems.append(f"n={n}: claims.json ceiling != side rounded up at 16 places")
        ordered = sorted([("this certificate", side), *rows.items()], key=lambda item: item[1])
        smallest = ordered[0][1]
        table = [
            {
                "report": label,
                "side_up16": up(value, 16),
                "above_smallest": str(value - smallest),
                "above_smallest_float": f"{float(value - smallest):.4e}",
            }
            for label, value in ordered
        ]
        report[str(n)] = {
            "side": str(side),
            "side_up12": up(side, 12),
            "side_up16": up(side, 16),
            "issue_prints": printed,
            "case_ceiling": str(ceiling),
            "house_witness_side": str(house),
            "below_case_by": str(ceiling - side),
            "below_case_by_float": f"{float(ceiling - side):.6e}",
            "ordered": table,
            "smallest": ordered[0][0],
        }
        print(f"n={n}: side {up(side,16)} (prints {printed}); below the case by {float(ceiling-side):.4e}; smallest: {ordered[0][0]}")
        for row in table:
            print(f"   {row['report']:40s} {row['side_up16']}  +{row['above_smallest_float']}")
    report["problems"] = problems
    for problem in problems:
        print("PROBLEM", problem)
    args.json.write_text(json.dumps(report, indent=1) + "\n", "utf-8")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
