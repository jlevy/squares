"""#847's filled-end sample: the author's builder writes out, our routes decide.

`devtools.filled_end_sample` writes out five of V2.0's rows with the author's own
``build`` and decides each certificate on both maintained exact routes. The refusals
come first: a malformed table, a malformed sampled row, and a builder whose packing is
not the row's. Then the agreements: 1182 built again to the receipt's digest and
accepted by both routes, and the receipt read back.
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


def test_a_malformed_table_is_refused(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The table's bytes are the packet's custody (`acquire_source --check`), so no
    digest is compared here; the table is still read as untrusted data, and a header
    other than `COLUMNS`, a short row or a count given twice is refused."""
    copied = _moved(tmp_path, monkeypatch)
    table = copied / sample.TABLE
    original = table.read_bytes()
    first, _, rest = original.partition(b"\n")
    second = rest.split(b"\n", 1)[0]
    cases = {
        "the header is not": first.replace(b"side_exact", b"side_exactly") + b"\n" + rest,
        "row 1: 11 fields": first + b"\n" + second.rsplit(b",", 1)[0] + b"\n",
        "n = 1182 appears twice": first + b"\n" + second + b"\n" + second + b"\n",
    }
    for reason, data in cases.items():
        table.write_bytes(data)
        with pytest.raises(sample.SampleError, match=re.escape(reason)):
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
    """The receipt reads back: its header, five counts of 5,134 rows, each certificate
    written out again to the size, side and SHA-256 the receipt names, verified on both
    routes, and every control refused by both."""
    assert sample.check() == []
    receipt = json.loads((sample.PACKET / sample.RECEIPT).read_text(encoding="utf-8"))
    assert receipt["coverage"] == {"checked": 5, "of": 5134, "unit": "rows"}
    assert [row["n"] for row in receipt["rows"]] == list(sample.SAMPLE)


def test_an_altered_receipt_is_refused(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """In a copy of the packet, a receipt naming another record, another certificate at
    2505, or a route that accepted a control at 7500 is named for each."""
    copied = _moved(tmp_path, monkeypatch)
    path = copied / sample.RECEIPT
    receipt = json.loads(path.read_text(encoding="utf-8"))
    receipt["doi"] = "10.5281/zenodo.23681705"
    receipt["rows"][1]["certificate_sha256"] = "0" * 64
    receipt["rows"][3]["controls"][0]["refused_by_independent"] = False
    path.write_text(json.dumps(receipt), encoding="utf-8")
    assert sample.check() == [
        "the receipt's header is not this module's",
        "n=2505: the builder writes another certificate than the receipt's",
        "n=7500: a route accepted a control",
    ]
