"""Which source's packing a case's house drawing pictures.

A case record's `reported_upper_bound.source_key` names where its side comes from, and
nearly always that is also where the drawn packing comes from. The exception is the
report that solved known-best packings to their exact optima: it moves a case's side by
at most 5e-11 and keeps the packing, so the atlas pictures the packing from the source
that held the count before, which the report's comparison receipt names
(`devtools.evand_exact_certificates compare`).

One rule for every reader: the atlas builder reads the house witness from the pictured
source, and a case page credits its house drawing, "as published", to the same source
(regularization policy, section 12).
"""

from __future__ import annotations

import json
from functools import cache

#: The exact-optima report's source key, which reports a side but pictures no packing.
EXACT_OPTIMA_SOURCE_KEY = "[evand exact optima 2026-10-05]"


@cache
def exact_optima_pictured() -> dict[int, str]:
    """The source key each exact optimum's packing is pictured from, by count."""
    from devtools.evand_exact_certificates import COMPARISON_RECEIPT  # noqa: PLC0415

    receipt = json.loads(COMPARISON_RECEIPT.read_text(encoding="utf-8"))
    return {int(row["n"]): str(row["earlier_source_key"]) for row in receipt["rows"]}


def pictured_source_key(n: int, reported_source_key: str) -> str:
    """The source whose geometry the atlas reads for case `n`: the record's own, except
    where an exact optimum of a packing reports the side and its finder's source holds
    the pose."""
    if reported_source_key != EXACT_OPTIMA_SOURCE_KEY:
        return reported_source_key
    pictured = exact_optima_pictured().get(n)
    if pictured is None:
        raise ValueError(f"n={n}: no source holds the packing of its exact optimum")
    return pictured
