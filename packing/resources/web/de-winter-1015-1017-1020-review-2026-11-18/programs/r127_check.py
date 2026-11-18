"""Decide one certificate file and its claim.

Lane r127-1118.  Written for this review; imports only its own modules.

    python -I -B r127_check.py FILE --claim DECIMAL [--claim-exact P/Q]
        [--claim-decimal-exact DECIMAL] --out OUT.json

Reads FILE strictly (r127_read), decides it by both methods (r127_decide), and checks
the claim's arithmetic exactly: the claimed print C against the certificate's side S
(C >= S, and whether C is the 12-place ceiling of S), and where the issue states the
side exactly, as a fraction or as a terminating decimal, whether that equals S.  The
receipt carries the file's SHA-256.  Exit status 0 on ACCEPT, 1 on REFUSE, 2 when the
reader refuses the file.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I drops the script dir

import argparse
import hashlib
import json
import sys
import time
from fractions import Fraction

import r127_decide as D
import r127_read as R


def ceil_places(q: Fraction, places: int) -> Fraction:
    scale = 10**places
    num = q * scale
    c = -((-num.numerator) // num.denominator)
    return Fraction(c, scale)


def floor_places(q: Fraction, places: int) -> Fraction:
    scale = 10**places
    num = q * scale
    return Fraction(num.numerator // num.denominator, scale)


def decimal_fraction(text: str) -> Fraction:
    if not all(ch.isdigit() or ch == "." for ch in text) or text.count(".") != 1:
        raise ValueError(f"not a plain decimal: {text}")
    return Fraction(text)


def claim_facts(side: Fraction, claim: str, exact: str | None, dec_exact: str | None) -> dict:
    c = decimal_fraction(claim)
    places = len(claim.split(".")[1])
    out = {
        "claim": claim,
        "claim_places": places,
        "claim_at_least_side": c >= side,
        "claim_less_side": D.fs(c - side),
        "claim_less_side_decimal": D.sci(c - side),
        "ceiling_at_claim_places": D.dec(ceil_places(side, places), places),
        "claim_is_ceiling": c == ceil_places(side, places),
        "floor_at_claim_places": D.dec(floor_places(side, places), places),
    }
    if exact is not None:
        out["stated_exact"] = exact
        out["stated_exact_equals_side"] = Fraction(exact) == side
    if dec_exact is not None:
        out["stated_decimal"] = dec_exact
        out["stated_decimal_equals_side"] = decimal_fraction(dec_exact) == side
        out["side_less_stated_decimal"] = D.fs(side - decimal_fraction(dec_exact))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--claim", required=True)
    ap.add_argument("--claim-exact")
    ap.add_argument("--claim-decimal-exact")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    t0 = time.process_time()
    raw = open(a.file, "rb").read()
    receipt: dict = {"program": "r127_check.py", "file": a.file,
                     "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
    try:
        p = R.read_path(a.file)
    except R.ReadError as exc:
        receipt.update({"verdict": "READER_REFUSES", "reason": str(exc)})
        json.dump(receipt, open(a.out, "w"), indent=1)
        print(f"{a.file}: READER_REFUSES {exc}")
        return 2
    receipt["form"] = p.form
    receipt["scalars"] = p.scalars
    receipt["not_lowest_terms"] = p.not_lowest[:20]
    receipt["not_lowest_terms_count"] = len(p.not_lowest)
    receipt["ids_first_last"] = [str(p.ids[0]), str(p.ids[-1])]
    if p.meta:
        receipt["meta"] = {k: v for k, v in p.meta.items()}
    d = D.decide_full(p)
    s = D.summarize(d)
    receipt["decision"] = s
    receipt["claim"] = claim_facts(p.side, a.claim, a.claim_exact, a.claim_decimal_exact)
    receipt["verdict"] = s["verdict"]
    receipt["cpu_seconds"] = round(time.process_time() - t0, 2)
    json.dump(receipt, open(a.out, "w"), indent=1, default=str)
    lm = s["least_margin"]
    print(f"{a.file}: {s['verdict']} n={s['n']} pairs={s['pairs']} classes={s['pair_classes_A']}"
          f" least={lm['decimal'] if lm else None} {lm['pair'] if lm else ''}"
          f" contacts={ {k: len(v) for k, v in s['wall_contacts'].items()} }"
          f" claim_is_ceiling={receipt['claim']['claim_is_ceiling']}"
          f" cpu={receipt['cpu_seconds']}s")
    return 0 if s["verdict"] == "ACCEPT" else 1


if __name__ == "__main__":
    sys.exit(main())
