"""Machine audit of Bentz 2010, Lemma 10: the printed point `(1, 1.74)` is transposed.

Lemma 10 as printed (transcription line 122, raw extraction line 290): a box covering
`A(1, 0.914)` and no other Figure 2 point contains `(1.12, 1)`, `(1, 1.74)`, and
`(1.87, 0.76)`; its one-line proof replaces `A` by each point and asserts the set
stays unavoidable. For `(1, 1.74)` that assertion is false, and this module carries
the exact refutation: the axis-aligned box of side `1001/1000` centred at
`(73/50, 7/10)` lies inside `[0, 4]^2` and strictly avoids every point of
`(Figure 2 minus A) union {(1, 1.74)}` -- certified by `sqpack.falsify` with every
decision an exact rational sign.

Three independent lines say the intended point is `(1.74, 1)`:

- the same escape box strictly contains `(1.74, 1)`, so the transposed replacement
  set has no such escape (checked exactly here);
- Section 3.2's `S_A = {A, (1.13, 1), (1.4, 1), (1.74, 1), (1.87, 0.76)}` is
  justified "by Lemmas 10 and 11", and `(1.4, 1)`, `(1.74, 1)` lie in the convex
  hull of `A`, `(1.12, 1)`, `(1.74, 1)`, `(1.87, 0.76)` but not in the hull the
  printed lemma gives;
- `(1, 1.74)` is exactly the `y = x` mirror of `(1.74, 1)` -- the point the
  symmetric (`B`-covering) version of the lemma delivers, which is how Section 3.1
  uses it ("each corner-restricted box will contain one of `(1, 1.74)`,
  `(1.6, 1)`, or their symmetric counterparts").

Whether the transposition is the paper's or the extraction pipeline's cannot be
decided from this repository (the raw text is column-interleaved pdftotext output
and carries the same reading), so the finding is held as a typed source delta in
the H-041 discipline: the encoding proceeds against the corrected point, the
printed reading is preserved beside it, and the verdict stays unresolved with
needs_review until the owner checks the published PDF.

Usage, from `packing/`:
    uv run --frozen python -m cases.bentz13.lemma10_audit
"""

from __future__ import annotations

import time
from fractions import Fraction

from cases.bentz13.packing import Rat, build
from sqpack.falsify import CertificationRefusedError, certify_escape

#: The escape box: axis-aligned, side 1001/1000, centre (73/50, 7/10).
CENTER = (Rat.of(Fraction(73, 50)), Rat.of(Fraction(7, 10)))
LENGTH = Rat.of(Fraction(1001, 1000))
#: Lemma 10's replacement point as printed, and the corrected reading.
PRINTED = (Rat.of(1), Rat.of(Fraction(174, 100)))
CORRECTED = (Rat.of(Fraction(174, 100)), Rat.of(1))


def replacement_points(
    replacement: tuple[Rat, Rat],
) -> list[tuple[str, tuple[Rat, Rat]]]:
    """(Figure 2 minus A) union {replacement}, as named exact points."""
    set_points, _vertices, _plan = build()
    points = [(name, point) for name, point in set_points.items() if name != "a1"]
    points.append(("replacement", replacement))
    return points


def audit() -> dict[str, object]:
    side = Rat.of(4)
    one = Rat.of(1)
    zero = Rat.of(0)
    escape = certify_escape(
        side=side,
        length=LENGTH,
        center=CENTER,
        cosine=one,
        sine=zero,
        points=replacement_points(PRINTED),
    )
    try:
        certify_escape(
            side=side,
            length=LENGTH,
            center=CENTER,
            cosine=one,
            sine=zero,
            points=replacement_points(CORRECTED),
        )
    except CertificationRefusedError as refusal:
        corrected_refusal = {
            "reason": str(refusal),
            "defeated_by": refusal.defeated_by,
        }
    else:
        raise AssertionError(
            "the escape box unexpectedly avoids the corrected replacement set too"
        )
    return {
        "claim_audited": (
            "Lemma 10 as printed: the Figure 2 set stays unavoidable when A is "
            "replaced by (1, 1.74)"
        ),
        "verdict": (
            "refuted as printed: the box below avoids every point of the printed "
            "replacement set; the corrected reading (1.74, 1) is contained by the "
            "same box, so this escape does not exist against it"
        ),
        "escape_certificate": escape,
        "corrected_point_refusal": corrected_refusal,
        "status": "unresolved; needs_review (source delta held in the H-041 discipline)",
    }


def main() -> int:
    started = time.monotonic()
    record = audit()
    elapsed = time.monotonic() - started
    print(record["claim_audited"])
    print(record["verdict"])
    refusal = record["corrected_point_refusal"]
    print(f"corrected-point check: {refusal['reason']} ({refusal['defeated_by']})")  # type: ignore[index]
    print(f"wall: {elapsed:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
