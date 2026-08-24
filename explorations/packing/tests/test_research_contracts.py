"""Fast contracts for reusable numerical research helpers."""

from __future__ import annotations

import math

from sqpack.closed_form import recognise


def test_closed_form_recognises_simple_surd_without_overclaiming() -> None:
    form = recognise(2 + math.sqrt(2) / 2)

    assert form is not None
    assert (form.p, form.q, form.d, form.r) == (4, 1, 2, 2)
    assert recognise(math.pi, tol=1e-14) is None
