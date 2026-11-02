"""A recorder for displayed constants and their rounding conventions.

Q's Section 12.1 fixes the conventions: `x = d...` is a truncation (d <= x < d + u);
`x <= v` is x rounded up at its last digit (v - u < x <= v); `x >= v` is x rounded
down (v <= x < v + u); `x < v` is a chosen bound. For an upper or lower bound the
proofs need only x <= v (x >= v); the other half is the display convention, recorded
separately as `display`.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from fractions import Fraction
from pathlib import Path

from iv import Iv


def unit_of(v: str) -> Fraction:
    s = v.strip().lower().replace(" ", "")
    if "e" in s:
        mant, ex = s.split("e")
        e = int(ex)
    else:
        mant, e = s, 0
    dec = len(mant.split(".")[1]) if "." in mant else 0
    return Fraction(1, 10**dec) * Fraction(10) ** e


def dec(x: Fraction, sig: int = 30) -> str:
    """A decimal string of x with about `sig` significant digits (for receipts)."""
    if x == 0:
        return "0"
    neg = x < 0
    x = abs(x)
    e = 0
    while x >= 10:
        x /= 10
        e += 1
    while x < 1:
        x *= 10
        e -= 1
    digits = int(x * 10 ** (sig - 1))
    s = str(digits)
    out = f"{s[0]}.{s[1:]}e{e:+d}"
    return ("-" if neg else "") + out


def _tri(lo_ok: bool, hi_ok: bool) -> bool | None:
    if lo_ok:
        return True
    if hi_ok:
        return False
    return None


class Recorder:
    def __init__(self, program: str) -> None:
        self.program = program
        self.rows: list[dict[str, object]] = []

    def _add(self, cid: str, where: str, what: str, rel: str, shown: str, x: Iv | None,
             needed: bool | None, display: bool | None = None, note: str = "") -> None:
        row: dict[str, object] = {"id": cid, "where": where, "what": what, "relation": rel, "shown": shown,
                                  "needed": needed}
        if display is not None:
            row["display"] = display
        if x is not None:
            row["enclosure"] = [dec(x.lo), dec(x.hi)]
        if note:
            row["note"] = note
        self.rows.append(row)

    def upper(self, cid: str, where: str, what: str, x: Iv, v: str, note: str = "") -> None:
        """Displayed `x <= v`, rounded up at the last digit."""
        vq, u = Fraction(v), unit_of(v)
        needed = _tri(x.hi <= vq, x.lo > vq)
        display = _tri(x.lo > vq - u, x.hi <= vq - u)
        self._add(cid, where, what, "<=", v, x, needed, display, note)

    def lower(self, cid: str, where: str, what: str, x: Iv, v: str, note: str = "") -> None:
        """Displayed `x >= v`, rounded down at the last digit."""
        vq, u = Fraction(v), unit_of(v)
        needed = _tri(x.lo >= vq, x.hi < vq)
        display = _tri(x.hi < vq + u, x.lo >= vq + u)
        self._add(cid, where, what, ">=", v, x, needed, display, note)

    def below(self, cid: str, where: str, what: str, x: Iv, v: str, note: str = "") -> None:
        """A chosen strict bound `x < v`."""
        vq = Fraction(v)
        self._add(cid, where, what, "<", v, x, _tri(x.hi < vq, x.lo >= vq), None, note)

    def above(self, cid: str, where: str, what: str, x: Iv, v: str, note: str = "") -> None:
        """A chosen strict bound `x > v`."""
        vq = Fraction(v)
        self._add(cid, where, what, ">", v, x, _tri(x.lo > vq, x.hi <= vq), None, note)

    def trunc(self, cid: str, where: str, what: str, x: Iv, d: str, note: str = "") -> None:
        """Displayed `x = d...`: d <= x < d + u."""
        dq, u = Fraction(d), unit_of(d)
        ok = _tri(x.lo >= dq and x.hi < dq + u, x.hi < dq or x.lo >= dq + u)
        self._add(cid, where, what, "trunc", d + "...", x, ok, None, note)

    def equal(self, cid: str, where: str, what: str, x: Fraction, v: str, note: str = "") -> None:
        self._add(cid, where, what, "==", v, Iv(x), x == Fraction(v), None, note)

    def fact(self, cid: str, where: str, what: str, verdict: bool | None, x: Iv | None = None,
             note: str = "") -> None:
        self._add(cid, where, what, "fact", "", x, verdict, None, note)

    def summary(self) -> dict[str, int]:
        n = len(self.rows)
        return {
            "checks": n,
            "needed_true": sum(1 for r in self.rows if r["needed"] is True),
            "needed_false": sum(1 for r in self.rows if r["needed"] is False),
            "needed_undecided": sum(1 for r in self.rows if r["needed"] is None),
            "display_checked": sum(1 for r in self.rows if "display" in r),
            "display_true": sum(1 for r in self.rows if r.get("display") is True),
            "display_false": sum(1 for r in self.rows if r.get("display") is False),
        }

    def write(self, out: Path, extra: dict[str, object] | None = None) -> dict[str, object]:
        here = Path(__file__).resolve().parent
        digests = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in sorted(here.glob("*.py"))}
        receipt: dict[str, object] = {
            "program": self.program,
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "program_sha256": digests,
            "summary": self.summary(),
            "checks": self.rows,
        }
        if extra:
            receipt.update(extra)
        out.write_text(json.dumps(receipt, indent=1) + "\n")
        return receipt
