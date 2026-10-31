"""#847's filled-end sample: the author's builder, held to a digest, decided by our routes.

`devtools.filled_end_sample` writes out five of V2.0's rows with the author's own
``build`` and decides each certificate on both maintained exact routes. The refusals
come first: a builder or a table whose bytes are not the ones the author's digests bind,
a malformed sampled row, and a builder whose packing is not the row's. Then the
agreements: 1182 built again to the receipt's digest and accepted by both routes, and
the receipt read back.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import couzo_678_replay as base
from devtools import evand_exact_certificates as legacy
from devtools import filled_end_sample as sample


def _moved(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A copy of the packet that the module reads instead of the retained one."""
    copied = tmp_path / "packet"
    shutil.copytree(sample.PACKET, copied)
    monkeypatch.setattr(sample, "PACKET", copied)
    return copied


def test_a_builder_or_table_other_than_the_bound_one_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The builder runs only with the SHA-256 of the V1.0 archive's member, and the table
    is read only with the SHA-256 #847 states; one byte changed in either is refused
    before anything runs or is read."""
    copied = _moved(tmp_path, monkeypatch)
    builder = copied / sample.BUILDER
    builder.write_bytes(builder.read_bytes() + b"\n")
    with pytest.raises(
        sample.SampleError, match=re.escape("is not the V1.0 archive's filled_ends.py")
    ):
        sample.builder()
    table = copied / sample.TABLE
    table.write_bytes(table.read_bytes().replace(b"1182,35,", b"1182,36,", 1))
    with pytest.raises(sample.SampleError, match="is not the table #847 states"):
        sample.rows()


def test_a_row_the_builder_does_not_reproduce_is_refused() -> None:
    """A builder whose side is not the row's exact side, or that makes another number of
    squares, is refused; so is a row whose K is not ceil(sqrt(n)) or whose literal is
    not matched whole."""
    row = sample.rows()[1182]
    side = Fraction(row["side_exact"])
    square = (Fraction(1, 2), Fraction(1, 2), Fraction(0))

    def wider(*_: object) -> tuple[Fraction, list[tuple[Fraction, ...]]]:
        return side + Fraction(1, 10**30), [square] * 1182

    def fewer(*_: object) -> tuple[Fraction, list[tuple[Fraction, ...]]]:
        return side, [square] * 1181

    with pytest.raises(sample.SampleError, match="the builder's side is not the row's"):
        sample.certificate(1182, wider)
    with pytest.raises(sample.SampleError, match="the builder made 1181 squares"):
        sample.certificate(1182, fewer)
    with pytest.raises(sample.SampleError, match=r"K = 36 is not ceil\(sqrt\(n\)\)"):
        sample.parameters({**row, "K": "36"})
    with pytest.raises(sample.SampleError, match="tV is '1/0x'"):
        sample.parameters({**row, "tV": "1/0x"})


def test_the_first_count_builds_to_the_receipt_s_digest_and_passes_both_routes() -> None:
    """1182, written out again by the author's builder, has the receipt's SHA-256 and side,
    and both exact routes accept it."""
    stored = json.loads((sample.PACKET / sample.RECEIPT).read_text(encoding="utf-8"))["rows"][0]
    cert = sample.certificate(1182)
    text = legacy.serialize(cert).encode("utf-8")
    assert (stored["n"], stored["exact_side"]) == (1182, legacy.literal(cert.side))
    assert hashlib.sha256(text).hexdigest() == stored["certificate_sha256"]
    result = base.decide(base.geometry(cert))
    assert (result["sqpack"]["passed"], result["independent"]["passed"]) == (True, True)


def test_the_receipt_holds() -> None:
    """The receipt reads back: the digests the custody binds, five counts of 5,134 rows,
    each certificate verified on both routes and every control refused by both."""
    assert sample.check() == []
    receipt = json.loads((sample.PACKET / sample.RECEIPT).read_text(encoding="utf-8"))
    assert receipt["coverage"] == {"checked": 5, "of": 5134, "unit": "rows"}
    assert [row["n"] for row in receipt["rows"]] == list(sample.SAMPLE)
