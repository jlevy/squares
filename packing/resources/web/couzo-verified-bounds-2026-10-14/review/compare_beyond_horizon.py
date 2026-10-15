"""Compare franciscouzo/square-packing@487b058's beyond-horizon certificates with every report.

The packet pins the 296 certificates 487b058 adds or changes beyond n = 324 by digest only
(OR-18: 33 MB). This script reads each one's exact header side from a checkout at the pin,
holds the file to the digest the packet's manifest records, and compares the side, in
report order, with what stood at the count when 487b058 was committed
(2026-10-14T17:45:39Z), then with the two later reports from the same repository.

Earlier members at a count:

- every row of ``beyond_horizon_claims`` in ``packing/frontier/source-coverage.yaml``,
  current or superseded, at the exact side its packet's claim record states, else as its
  printed value within one unit of its last place;
- every exact side beyond 324 in a packet claim record under ``packing/resources/web/``;
- Kevin Fang's theorem inventory (exact header sides, ``inventory-headers.json``) and his
  composite table (``table.csv``, sides rounded up at 15 places), both retained in the
  fang-excess-theorem-2026-10-13 packet;
- the printed steps of the 14 October ledger beyond 324;
- Evan Daniel's tiling certificate at 964 (evand/square-packing@49907ec), given exactly on
  the command line;
- the grid side ceil(sqrt(n)).

A side is recorded when it is below every number every earlier member may be; equal to an
exact member is a tie the earlier holder keeps. Later members: issue #607's submissions
(43ac7d2) and the 4e4c8ce index, which supersede a recorded row where smaller.

Run from ``packing/`` with the project interpreter::

    python -I resources/web/couzo-verified-bounds-2026-10-14/review/compare_beyond_horizon.py \\
        --repo REPO --checkout CHECKOUT --sub-607 SUB.json --index-4e4c8ce MANIFEST.json \\
        --gobel GOBEL.json --out .../review/beyond-horizon-comparison.json \\
        --claims-out .../review/beyond-horizon-claims.json

SUB.json is ``submissions/2026-10-14/manifest.json`` at 43ac7d2, MANIFEST.json is
``certificates/best/manifest.json`` at 4e4c8ce and GOBEL.json is ``gobel_bounds.json`` at
58a7833, each read from the same repository.

No program of the source runs; the checkout is read as data.
"""

from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

import yaml

PIN = "487b05809099d8f7d006aaeb6bfc1ebe95cb8d0d"
FIRST = "2026-10-14T17:45:39Z"
PACKET = "packing/resources/web/couzo-verified-bounds-2026-10-14"
#: Evan Daniel's tiling certificate at 964, search/tilings/n964.cert at 49907ec (2026-10-08).
EVAND_964 = Fraction(13758246984533944841354281437, 431841354281437000000000000)


def header_side(path: Path) -> tuple[int, Fraction]:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or not line.strip():
            continue
        n, side = line.split()[:2]
        return int(n), Fraction(side)
    raise ValueError(f"{path}: no header")


def ceiling(side: Fraction, places: int = 12) -> str:
    """The side rounded up at ``places`` decimal places, exactly."""
    q = -((-side.numerator * 10**places) // side.denominator)
    whole, frac = divmod(q, 10**places)
    return f"{whole}.{frac:0{places}d}"


def record_text(value: dict, key: str) -> str:
    """A record with one row of ``key`` per line, as the packets' claim records are laid out."""
    head = [f"  {json.dumps(k)}: {json.dumps(v)}" for k, v in value.items() if k != key]
    body = ",\n".join("    " + json.dumps(row) for row in value[key])
    return "{\n" + ",\n".join([*head, f'  "{key}": [\n' + body + "\n  ]"]) + "\n}\n"


def printed(value: str) -> tuple[Fraction, Fraction]:
    unit = Fraction(1, 10 ** len(value.partition(".")[2]))
    p = Fraction(value)
    return p - unit, p + unit


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--checkout", required=True)
    ap.add_argument("--sub-607", required=True)
    ap.add_argument("--index-4e4c8ce", required=True)
    ap.add_argument("--gobel", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--claims-out", required=True)
    a = ap.parse_args()
    repo, checkout = Path(a.repo), Path(a.checkout)
    web = repo / "packing/resources/web"

    manifest = {}
    for line in (repo / PACKET / "acquisition/upstream-subtree.sha256").read_text().splitlines():
        digest, path = line.split("  ./", 1)
        manifest[path] = digest
    sides = {}
    for path, digest in manifest.items():
        if not (path.startswith("certificates/n") and path.endswith(".cert")):
            continue
        raw = (checkout / path).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == digest, path
        n, side = header_side(checkout / path)
        if n > 324:
            sides[n] = side

    exact_by_packet: dict[tuple[str, int], Fraction] = {}
    members: dict[int, list[dict]] = {n: [] for n in sides}

    def add(n, label, low, high, exact=None):
        if n in members:
            members[n].append({"label": label, "low": low, "high": high, "exact": exact})

    for path in glob.glob(str(web / "*/acquisition/*claims.json")):
        d = json.loads(Path(path).read_text())
        if not isinstance(d, dict) or "results" not in d:
            continue
        name = Path(path).parts[-3]
        for r in d["results"]:
            n = r.get("n")
            if isinstance(n, int) and n > 324 and r.get("exact_side"):
                try:
                    v = Fraction(r["exact_side"])
                except ValueError:
                    continue
                if (name, n) not in exact_by_packet:
                    exact_by_packet[(name, n)] = v
                    add(n, f"packet {name}", v, v, v)

    coverage = yaml.safe_load((repo / "packing/frontier/source-coverage.yaml").read_text())
    for row in coverage["beyond_horizon_claims"]:
        n, sid = row["n"], row["source_id"]
        if (sid, n) in exact_by_packet:
            continue  # the same report, already exact
        low, high = printed(str(row["value"]))
        add(n, f"beyond-horizon row {sid} ({row.get('disposition')})", low, high)

    fang = web / "fang-excess-theorem-2026-10-13"
    for row in json.loads((fang / "acquisition/inventory-headers.json").read_text())["rows"]:
        v = Fraction(row["side"])
        add(row["count"], f"Fang theorem {row['file']} (5f3bdbf)", v, v, v)
    with (fang / "source/composites/table.csv").open() as handle:
        for row in csv.DictReader(handle):
            p = Fraction(row["side_rounded_up_15"])
            add(int(row["count"]), f"Fang composite {row['id']} (bef5c42)",
                p - Fraction(1, 10**15), p)

    ledger = json.loads(
        (repo / "packing/campaign/issue-intake/upper-bounds-20261014/ledger.json").read_text()
    )
    for c in ledger["counts"]:
        for s in c["steps"]:
            side = s.get("side") or ""
            if c["n"] > 324 and "." in side:
                low, high = printed(side)
                add(c["n"], f"ledger step {s['report']} ({s.get('reported_at')})", low, high)

    add(964, "evand tilings n964 (49907ec)", EVAND_964, EVAND_964, EVAND_964)
    for n in members:
        g = Fraction(math.isqrt(n - 1) + 1)
        add(n, "grid", g, g, g)

    later = {}
    for c in json.loads(Path(a.sub_607).read_text())["certificates"]:
        later.setdefault(int(c["n"]), []).append(("#607 (43ac7d2)", Fraction(c["rational_side"])))
    for k, w in json.loads(Path(a.index_4e4c8ce).read_text())["witnesses"].items():
        if w.get("bound"):
            try:
                later.setdefault(int(k), []).append(("4e4c8ce index", Fraction(w["bound"])))
            except ValueError:
                pass

    # The side the source prints for each count: certificates/README.md, rounded up at 12.
    prints = {}
    for line in (checkout / "certificates/README.md").read_text(encoding="utf-8").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and cells[0].isdigit() and cells[1].startswith("`"):
            prints[int(cells[0])] = cells[2]
    for n, s in sides.items():
        assert prints[n] == ceiling(s) or (
            Fraction(prints[n]) - Fraction(1, 10**12) < s <= Fraction(prints[n])
        ), (n, prints[n])

    # Göbel's square and strip constructions, with deletion, as the source computed them
    # exactly over Q(sqrt 2) at 58a7833 (gobel_bounds.json): not a member, since the record
    # holds none beyond 324, but a closed form a row may only re-rationalize.
    gobel = [
        (w["n"], Fraction(w["enclosure_lower"]), Fraction(w["bound"]), w["exact_bound"]["expression"])
        for w in json.loads(Path(a.gobel).read_text())["witnesses"]
    ]

    rows, tally = [], {}
    for n in sorted(sides):
        s = sides[n]
        ms = members[n]
        best = min(ms, key=lambda m: m["high"])
        if all(s < m["low"] for m in ms):
            verdict = "recorded"
        elif any(m["exact"] is not None and m["exact"] == s for m in ms):
            verdict = "not recorded: equal"
        elif any(s >= m["high"] for m in ms):
            verdict = "not recorded: above"
        else:
            verdict = "undecided"
        tally[verdict] = tally.get(verdict, 0) + 1
        sup = [
            {"report": lab, "below_by": float(s - v)}
            for lab, v in later.get(n, [])
            if v < s
        ]
        reach = [w for w in gobel if w[0] >= n]
        goebel = None
        if reach:
            g = min(reach, key=lambda w: w[2])
            relation = "above" if s > g[2] else ("below" if s < g[1] else "undecided")
            goebel = {"from_count": g[0], "closed_form": g[3], "relation": relation}
        rows.append({
            "n": n,
            "side": f"{s.numerator}/{s.denominator}",
            "printed": prints[n],
            "ceiling_12": ceiling(s),
            "verdict": verdict,
            "best_earlier": best["label"],
            "best_earlier_high": f"{float(best['high']):.15f}",
            "margin_below_best": float(best["low"] - s),
            "superseded_by_later": sup,
            "goebel": goebel,
        })
    out = {
        "format": "couzo-487b058-beyond-horizon-comparison-v1",
        "revision": PIN,
        "first_committed": FIRST,
        "counts": len(rows),
        "tally": tally,
        "pair_decisions_for_replay": sum(3 * n * (n - 1) for n in sides),
        "rows": rows,
    }
    out["goebel_above"] = [r["n"] for r in rows if (r["goebel"] or {}).get("relation") == "above"]
    Path(a.out).write_text(record_text(out, "rows"))
    # The record a beyond-horizon row reads (check_source_coverage.load_claims): the
    # recorded counts, each at the side the source prints.
    head = {
        "format": "upper-bound-beyond-horizon-claims-v1",
        "issue": "(no issue)",
        "source": "https://github.com/franciscouzo/square-packing",
        "revision": PIN,
        "horizon": 324,
    }
    results = [
        {
            "n": r["n"],
            "offered_side": r["printed"],
            "exact_side": r["side"],
            "ceiling": ceiling(Fraction(r["side"]), 16),
            "first_committed": FIRST,
        }
        for r in rows
        if r["verdict"] == "recorded"
    ]
    Path(a.claims_out).write_text(record_text({**head, "results": results}, "results"))
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))


if __name__ == "__main__":
    main()
