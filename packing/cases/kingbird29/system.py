"""The closed `n = 29` contact system, as a function of its six unknowns.

:mod:`cases.kingbird29.verify_svg` already transcribes everything here.  What it does
with the transcription is *evaluate* it: it recomputes each derived offset and each
defining equation from the serialized entity values and checks that the residuals sit
below the serialization tolerance.  It never solves.

The difference matters, and it is the whole reason this module exists.  Evaluating the
system tells you the published digits are consistent; it cannot give you more of them.
Solving the same transcription manufactures precision on demand, because the source
publishes a **complete closed system** — nine slide scalars in closed form and six
equations `f1 … f6` in `{s, a, b, c, d, i}` — rather than a bare numerical answer.

So this module substitutes each slide scalar by its closed form and exposes what is
left: six equations in six unknowns, square and ready for Newton.  It is deliberately a
transcription and not a derivation.  Nothing here infers a contact structure; the
contacts are the source's, and an independent extraction of them is separate work.
"""

from __future__ import annotations

import re
from pathlib import Path

import mpmath as mp

from cases.kingbird29.verify_svg import rotate_vector, vector_difference, vector_sum
from sqpack.promote.interval import cos_degrees, sin_degrees

ENTITY_RE = re.compile(r'<!ENTITY\s+([A-Za-z][A-Za-z0-9]*)\s+"([^"]+)">')

#: The unknowns, in the order the solver receives them.
UNKNOWNS = ("s", "a", "b", "c", "d", "i")

#: The nine slide scalars the source gives in closed form.  `r2` is derived and checked
#: by the reconstruction but does not appear in `f1 … f6`; it is kept because dropping a
#: published relation because this particular use has no need of it would quietly narrow
#: what the transcription claims to cover.
SLIDE_SCALARS = ("r1", "r2", "r3", "r4", "r5", "r8", "rB", "rC", "rD")

#: The defining equations, which vanish at the packing's pose.
EQUATIONS = ("f1", "f2", "f3", "f4", "f5", "f6")


class SystemTranscriptionError(ValueError):
    """The retained source did not supply what the transcription needs."""


#: Trig that dispatches on the scalar it is handed, so this transcription evaluates
#: over floats and over interval duals without being written twice.  See
#: :func:`sqpack.promote.interval.sin_degrees`.
_sin = sin_degrees
_cos = cos_degrees


def read_entities(source: Path) -> dict[str, str]:
    """Return the SVG's internal entity table as undecoded decimal strings."""
    text = source.read_text(encoding="utf-8")
    entities = dict(ENTITY_RE.findall(text))
    missing = [name for name in (*UNKNOWNS, *SLIDE_SCALARS) if name not in entities]
    if missing:
        raise SystemTranscriptionError(f"retained source declares no entity for {missing}")
    return entities


def seed(source: Path) -> tuple[str, ...]:
    """The serialized pose, as the six unknowns in :data:`UNKNOWNS` order."""
    entities = read_entities(source)
    return tuple(entities[name] for name in UNKNOWNS)


def slide_scalars(s, a, b, c, d, i) -> dict:  # noqa: PLR0917  (the system's six unknowns)
    """The nine slide scalars, each in closed form in the six unknowns."""
    scalars: dict = {}
    scalars["r1"] = (s - 5) * _sin(a)
    scalars["r2"] = 1 - (s - 5) * _cos(b)
    scalars["r3"] = (
        vector_sum((s - 1, mp.mpf(3)), rotate_vector(-c, (-1, 1)))[1] - (s - 2)
    ) / _cos(c)
    scalars["r4"] = (
        vector_sum((s - 3, mp.mpf(1)), rotate_vector(a, (1 - (s - 5) * _cos(a), 0)))[1] - 1
    ) / _cos(d)
    scalars["r5"] = (
        (s - 1)
        - vector_sum(
            (mp.mpf(2), mp.mpf(1)),
            rotate_vector(a, (1, -scalars["r1"])),
            rotate_vector(d, (1, -scalars["r4"])),
            rotate_vector(d, (1, 0)),
        )[0]
    ) / _sin(d)
    scalars["r8"] = 2 - rotate_vector(-b, (4 - s, 1))[1]
    scalars["rB"] = -vector_sum((s - 2, s - 2), rotate_vector(b, (-4, 1 - scalars["r8"])))[
        0
    ] / _sin(b)
    scalars["rC"] = (
        1
        - rotate_vector(
            -i,
            vector_difference(
                vector_sum(
                    (s - 2, s - 2),
                    rotate_vector(b, (-3, -scalars["r8"] - scalars["rB"])),
                ),
                (mp.mpf(1), mp.mpf(2)),
            ),
        )[1]
    )
    scalars["rD"] = rotate_vector(
        -b,
        vector_difference(
            vector_sum((mp.mpf(2), mp.mpf(1)), rotate_vector(a, (1, 1 - scalars["r1"]))),
            vector_sum((mp.mpf(1), mp.mpf(2)), rotate_vector(i, (1, -scalars["rC"]))),
        ),
    )[1] / _cos(i - b)
    return scalars


def equations(s, a, b, c, d, i) -> list:  # noqa: PLR0917  (the system's six unknowns)
    """`f1 … f6`, with every slide scalar replaced by its closed form.

    `verify_svg` evaluates these same six expressions against the *serialized* slide
    scalars, which makes them a consistency check on the publication.  Substituting the
    closed forms instead makes them a system in the six unknowns alone, which is what
    lets a solver produce digits the source never printed.
    """
    scalars = slide_scalars(s, a, b, c, d, i)
    r1, r3, r4, r5 = (scalars[name] for name in ("r1", "r3", "r4", "r5"))
    r8, r_c, r_d = (scalars[name] for name in ("r8", "rC", "rD"))
    upper_middle = vector_sum(
        (mp.mpf(1), mp.mpf(2)),
        rotate_vector(i, (1, -r_c + r_d)),
        rotate_vector(b, (2, 0)),
    )
    f1 = rotate_vector(
        -a,
        vector_difference(
            vector_sum((mp.mpf(1), mp.mpf(2)), rotate_vector(i, (1, -r_c))),
            vector_sum((mp.mpf(2), mp.mpf(1)), rotate_vector(a, (0, 1 - r1))),
        ),
    )[1]
    f2 = rotate_vector(
        -d,
        vector_difference(
            upper_middle,
            vector_sum(
                (mp.mpf(2), mp.mpf(1)),
                rotate_vector(a, (1, -r1)),
                rotate_vector(d, (1, -r4)),
                rotate_vector(d, (0, 1 - r5)),
            ),
        ),
    )[1]
    f3 = rotate_vector(
        -b,
        vector_difference(
            upper_middle,
            vector_sum(
                (mp.mpf(2), mp.mpf(1)),
                rotate_vector(a, (1, -r1)),
                rotate_vector(d, (1, 1 - r4)),
            ),
        ),
    )[1]
    f4 = rotate_vector(
        -b,
        vector_difference(
            vector_sum((s - 1, mp.mpf(3)), rotate_vector(-c, (-1, -r3))),
            upper_middle,
        ),
    )[0]
    f5 = rotate_vector(
        -b,
        vector_difference(
            vector_sum((s - 2, s - 2), rotate_vector(b, (-1, -r8))),
            vector_sum(
                (mp.mpf(1), mp.mpf(2)),
                rotate_vector(i, (1, -r_c + r_d)),
                rotate_vector(b, (0, 1)),
            ),
        ),
    )[1]
    f6 = (
        rotate_vector(
            c,
            vector_difference(
                (s - 1, mp.mpf(3)),
                vector_sum((s - 2, s - 2), rotate_vector(b, (0, -r8))),
            ),
        )[0]
        - 1
    )
    return [f1, f2, f3, f4, f5, f6]
