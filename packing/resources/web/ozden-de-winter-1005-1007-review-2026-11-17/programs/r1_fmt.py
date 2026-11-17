"""How this review's receipts print exact rationals.  It decides nothing.

Lane R1, stage 4 review of #1005, #1006 and #1007.  Clean-room.

Every print is exact or truncated toward zero from the exact value by integer
arithmetic; nothing passes through a float.
"""

from __future__ import annotations

import json
from fractions import Fraction


def frac(value):
    """``p`` or ``p/q`` in lowest terms."""
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def dec(value, places):
    """The decimal expansion truncated toward zero at `places` places."""
    value = Fraction(value)
    sign = "-" if value < 0 else ""
    scaled = abs(value.numerator) * 10**places // value.denominator
    whole, part = divmod(scaled, 10**places)
    return f"{sign}{whole}.{part:0{places}d}" if places else f"{sign}{whole}"


def sci(value, digits=12):
    """Scientific notation with `digits` significant digits, truncated toward zero."""
    value = Fraction(value)
    if value == 0:
        return "0"
    sign = "-" if value < 0 else ""
    num, den = abs(value.numerator), value.denominator
    exponent = len(str(num)) - len(str(den))

    def at_least(power):
        """Whether num/den >= 10**power, in integers."""
        if power >= 0:
            return num >= den * 10**power
        return num * 10 ** (-power) >= den

    # bring the mantissa into [1, 10)
    while at_least(exponent + 1):
        exponent += 1
    while not at_least(exponent):
        exponent -= 1
    shift = digits - 1 - exponent
    if shift >= 0:
        mantissa = num * 10**shift // den
    else:
        mantissa = num // (den * 10 ** (-shift))
    text = str(mantissa)
    body = text[0] + ("." + text[1:] if len(text) > 1 else "")
    return f"{sign}{body}e{exponent}"


def exact_and_sci(value, digits=12):
    return {"exact": frac(value), "about": sci(value, digits)}


def ceil_places(value, places):
    """The least multiple of 10^-places that is at least `value`."""
    value = Fraction(value)
    scaled = value * 10**places
    up = -((-scaled.numerator) // scaled.denominator)
    return Fraction(up, 10**places)


def is_exact_decimal(value):
    """Whether the fraction is a terminating decimal."""
    den = Fraction(value).denominator
    for prime in (2, 5):
        while den % prime == 0:
            den //= prime
    return den == 1


def _flat(value):
    """A scalar, or a short list of scalars: printed on one line."""
    if isinstance(value, (list, tuple)):
        return len(value) <= 4 and all(not isinstance(v, (list, tuple, dict)) for v in value)
    return not isinstance(value, dict)


def to_json(value, indent=0):
    """JSON text with one key per line and lists of scalars or of short lists inline."""
    pad = " " * indent
    if isinstance(value, dict):
        if not value:
            return "{}"
        rows = [f"{pad} {json.dumps(str(k))}: {to_json(v, indent + 1)}" for k, v in value.items()]
        return "{\n" + ",\n".join(rows) + "\n" + pad + "}"
    if isinstance(value, (list, tuple)):
        if all(_flat(v) for v in value):
            return json.dumps(value)
        rows = [f"{pad} {to_json(v, indent + 1)}" for v in value]
        return "[\n" + ",\n".join(rows) + "\n" + pad + "]"
    return json.dumps(value)


def write_json(path, value):
    text = to_json(value) + "\n"
    json.loads(text)  # the receipt must be valid JSON
    with open(path, "w") as handle:
        handle.write(text)
