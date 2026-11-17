"""L72 review utilities: digests, exact decimal prints and receipts. No geometry.

Lane L72 (bead think-qqyg), stage 4 review of issues 935 and 936. Written from the
mathematics alone; imports nothing from the squares repository or the source repositories.
"""

import hashlib
import json
import os
import platform
import sys
import time
from fractions import Fraction


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def frac_str(x):
    """Exact text of a rational: 'p/q' in lowest terms, or 'p' when q == 1."""
    x = Fraction(x)
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def floor_decimal(x, places):
    """The exact floor of x at `places` decimal places, as a decimal string."""
    x = Fraction(x)
    scale = 10**places
    k = (x.numerator * scale) // x.denominator  # floor division on integers
    return _fixed(k, places)


def ceil_decimal(x, places):
    """The exact ceiling of x at `places` decimal places, as a decimal string."""
    x = Fraction(x)
    scale = 10**places
    k = -((-x.numerator * scale) // x.denominator)
    return _fixed(k, places)


def _fixed(k, places):
    sign = "-" if k < 0 else ""
    k = abs(k)
    s = str(k).rjust(places + 1, "0")
    if places == 0:
        return sign + s
    return f"{sign}{s[:-places]}.{s[-places:]}"


def sci(x, digits=6):
    """A short scientific print of a rational (for prose only; exact values travel as text)."""
    x = Fraction(x)
    if x == 0:
        return "0"
    sign = "-" if x < 0 else ""
    x = abs(x)
    # exponent e with 10^e <= x < 10^(e+1), found exactly
    e = len(str(x.numerator)) - len(str(x.denominator))
    while Fraction(10) ** e > x:
        e -= 1
    while Fraction(10) ** (e + 1) <= x:
        e += 1
    m = x / Fraction(10) ** e
    mant = floor_decimal(m, digits - 1)
    return f"{sign}{mant}e{e:+03d}"


def is_lowest(num, den):
    from math import gcd

    return gcd(num, den) == 1


def environment():
    return {
        "python": sys.version.split()[0],
        "implementation": platform.python_implementation(),
        "isolated_flag": bool(sys.flags.isolated),
        "executable": sys.executable,
    }


def program_digests(paths):
    return {os.path.basename(p): sha256_file(p) for p in paths}


def write_receipt(path, payload):
    payload = dict(payload)
    payload.setdefault("written_utc", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    text = json.dumps(payload, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return sha256_bytes(text.encode("utf-8"))


def cpu_seconds():
    t = os.times()
    return t.user + t.system
