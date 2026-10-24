"""think-l49q: Couzo's 304 at fa6237e and Evan Daniel's exact descents at 8a8879a.

Two watched-repository publications that no issue reports. Couzo's
``certificates/best/n304.cert`` is retained by the issue-763 packet; the
``couzo-n304-2026-10-23`` packet pins it as ``identical_to`` that copy, and the importer
reads it from there (`upper_bound_reports._upstream`). Evan Daniel's
``evand-kaggle-descents-2026-10-24`` packet retains his certificates at 268, 303 and 304.
The general importer's checks run on both packets through ``test_upper_bound_reports``;
these hold what is particular to them: the copy read through the other packet and a twin
that differs refused, the exact sides and their margins in report order, the 303 that is
not recorded, the sharp controls that meet the certificates' margins, and the measured
identities the register states. Every test reads retained packets only; none needs the
network.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import shutil
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import acquire_source
from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports

COUZO = "couzo-n304-2026-10-23"
COUZO_763 = "couzo-issue763-2026-10-23"
DANIEL = "evand-kaggle-descents-2026-10-24"
CERT = "certificates/best/n304.cert"
#: The certificate's SHA-256, as Couzo's certified_bounds.json at fa6237e states it.
DIGEST = "c8433dd798aef6f190790c6c78c63b4ab5c26baabe372405f8ff9029d175231d"
COUZO_304 = Fraction(
    42654421699169959072564987841514227093543746926117736119087439,
    2379353056489745832681562849107891444171481219500000000000000,
)
DANIEL_268 = Fraction(8437180857934672912242411148233, 5 * 10**29)
DANIEL_303 = Fraction(17907238274538241192624181047171, 10**30)
DANIEL_304 = Fraction(1792689890035674158972360842897, 10**29)
#: T-240's sides at 268 and 303, issue 763's certificates at 964ee2b.
T240_268 = Fraction(78645658458105249171306580101, 4660659750118000000000000000)
T240_303 = Fraction(
    55035101387261868285958438488216555614454417144023299,
    3073388523105741896887024831655729584500000000000000,
)


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _rows(name: str) -> dict[int, dict[str, Any]]:
    return {row["n"]: row for row in reports.check_claims(reports.packet_path(name))["results"]}


def _pending(row: dict[str, Any], report: str) -> dict[str, Any]:
    (found,) = [other for other in row["pending"] if other["report"] == report]
    return found


def test_couzo_s_304_is_read_from_the_issue_763_packet_s_copy() -> None:
    packet = reports.packet_path(COUZO)
    record = reports.acquisition(packet)
    assert record["retained_file_count"] == 0
    (item,) = [item for item in record["pinned_only"] if item["path"] == CERT]
    twin = reports.REPO / item.get("identical_to", "")
    assert twin == reports.packet_path(COUZO_763) / "source" / CERT
    assert item["sha256"] == DIGEST == hashlib.sha256(twin.read_bytes()).hexdigest()
    (certificate,) = reports.read_facts(packet).values()
    assert (certificate.n, certificate.side, len(certificate.poses)) == (304, COUZO_304, 304)
    assert reports.house_side("[Couzo n304 2026-10-23]", 304) == COUZO_304


def test_a_twin_that_is_not_the_pinned_bytes_is_refused(tmp_path: Path) -> None:
    source = reports.REPO / reports.acquisition(reports.packet_path(COUZO))["archived_path"]
    item: acquire_source.PinnedOnly = {
        "path": CERT,
        "bytes": 1,
        "sha256": DIGEST,
        "reason": "a test",
        "identical_to": "packing/resources/web/couzo-issue763-2026-10-23/source/README.md",
    }
    with pytest.raises(reports.ReportError, match="not the bytes the packet pins"):
        reports._upstream(source, {CERT: item}, CERT)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    outside: acquire_source.PinnedOnly = {**item, "identical_to": str(tmp_path / "n304.cert")}
    with pytest.raises(reports.ReportError, match="private repository file"):
        reports._upstream(source, {CERT: outside}, CERT)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]


#: An original-gzip twin: the 20 October packet keeps n-204.cert.gz as the upstream bytes.
GZ_PATH = "search/regularize/lists/certs/n-204.cert.gz"
GZ_TWIN = f"packing/resources/web/evand-regularized-2026-10-20/source/{GZ_PATH}"


def test_an_original_gzip_twin_is_read_as_custody_reads_it() -> None:
    """A twin that is an original gzip is held to its digest as stored, the bytes the custody
    check compares, then decompressed as `_read` returns a retained ``.gz``; held to the
    digest of its decompressed bytes instead, it is refused (review A9 of #792)."""
    source = reports.REPO / reports.acquisition(reports.packet_path(COUZO))["archived_path"]
    stored = (reports.REPO / GZ_TWIN).read_bytes()
    item: acquire_source.PinnedOnly = {
        "path": GZ_PATH,
        "bytes": len(stored),
        "sha256": hashlib.sha256(stored).hexdigest(),
        "reason": "a test",
        "identical_to": GZ_TWIN,
    }
    assert acquire_source.twin_bytes(GZ_TWIN, reports.REPO) == stored
    read = reports._upstream(source, {GZ_PATH: item}, GZ_PATH)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    assert read == gzip.decompress(stored)
    assert read.startswith(b"# exact certificate")
    wrong: acquire_source.PinnedOnly = {**item, "sha256": hashlib.sha256(read).hexdigest()}
    with pytest.raises(reports.ReportError, match="not the bytes the packet pins"):
        reports._upstream(source, {GZ_PATH: wrong}, GZ_PATH)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]


def test_a_twin_past_the_source_bound_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    """A twin is read within the bound `_read` applies to a retained file,
    ``MAX_SOURCE_BYTES``, not the retained-data default (review B2 of #792)."""
    packet = reports.packet_path(COUZO)
    source = reports.REPO / reports.acquisition(packet)["archived_path"]
    twins = reports._twins(reports.acquisition(packet))  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    size = len((reports.packet_path(COUZO_763) / "source" / CERT).read_bytes())
    monkeypatch.setattr(reports, "MAX_SOURCE_BYTES", size - 1)
    with pytest.raises(reports.ReportError, match="exceeds"):
        reports._upstream(source, twins, CERT)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    monkeypatch.setattr(reports, "MAX_SOURCE_BYTES", size)
    assert hashlib.sha256(reports._upstream(source, twins, CERT)).hexdigest() == DIGEST  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]


def test_a_changed_copy_in_the_issue_763_packet_fails_custody(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path / "private"
    web = repo / reports.WEB.relative_to(reports.REPO)
    for name in (COUZO, COUZO_763, "couzo-issue678-2026-10-18"):
        shutil.copytree(reports.WEB / name, web / name)
    monkeypatch.setattr(reports, "REPO", repo)
    monkeypatch.setattr(reports, "WEB", web)
    monkeypatch.setattr(kernel, "REPO", repo)
    twin = web / COUZO_763 / "source" / CERT
    twin.write_bytes(twin.read_bytes() + b"\n")
    with pytest.raises(reports.ReportError, match="packet custody"):
        reports.read_facts(reports.packet_path(COUZO))


def test_couzo_s_304_is_the_smallest_report_and_below_t186() -> None:
    (row,) = _rows(COUZO).values()
    assert (row["n"], row["smallest"]) == (304, reports.THIS)
    assert (row["case"]["result"], row["case"]["relation"]) == ("T-186", "below")
    assert Fraction(2528, 10**6) < Fraction(row["case"]["difference"]) < Fraction(2529, 10**6)
    assert {other["relation"] for other in row["pending"]} == {"below"}


def test_daniel_s_sides_in_report_order() -> None:
    rows = _rows(DANIEL)
    assert {n: Fraction(row["exact_side"]) for n, row in rows.items()} == {
        268: DANIEL_268,
        303: DANIEL_303,
        304: DANIEL_304,
    }
    assert [n for n, row in rows.items() if row["requested"]] == [268, 304]
    # 268: below T-240 by its exact margin, 4.48e-12, and so the smallest report.
    t240 = _pending(rows[268], "T-240 (#763)")
    assert t240["relation"] == "below"
    assert Fraction(t240["difference"]) == T240_268 - DANIEL_268
    assert Fraction(447, 10**14) < T240_268 - DANIEL_268 < Fraction(449, 10**14)
    assert rows[268]["smallest"] == reports.THIS
    # 303: above T-240, which #763 reported first, so not recorded.
    assert _pending(rows[303], "T-240 (#763)")["relation"] == "above"
    assert rows[303]["smallest"] == "T-240 (#763)"
    assert Fraction(26, 10**5) < DANIEL_303 - T240_303
    # 304: below T-241, Couzo's certificate of the same packing, by 3.04e-9.
    t241 = _pending(rows[304], "T-241 (fa6237e)")
    assert (t241["result"], t241["relation"]) == ("T-241", "below")
    assert Fraction(t241["difference"]) == COUZO_304 - DANIEL_304
    assert Fraction(303, 10**11) < COUZO_304 - DANIEL_304 < Fraction(304, 10**11)
    assert rows[304]["smallest"] == reports.THIS


@pytest.mark.parametrize(
    ("packet", "receipt", "n", "wall"),
    [
        (DANIEL, "receipts/sharp-controls-n268.json", 268, Fraction(5, 10**21)),
        (DANIEL, "receipts/sharp-controls-n304.json", 304, Fraction(5, 10**21)),
        (COUZO, "receipts/sharp-controls.json", 304, Fraction(1, 10**15)),
    ],
)
def test_the_sharp_controls_meet_each_certificate_s_margins(
    packet: str, receipt: str, n: int, wall: Fraction
) -> None:
    path = reports.packet_path(packet)
    (margins,) = [
        m for k, m in reports.margins(reports.check_certification(path)).items() if k == n
    ]
    for route in kernel.ROUTES:
        assert Fraction(margins[f"{route}_containment_clearance"]) == wall
    found = _json(path / receipt)
    assert (found["n"], found["all_as_expected"]) == (n, True)
    assert Fraction(found["side"]) == reports.read_facts(path, {n})[n].side
    controls = (*kernel.SHARP_CONTROLS, "squares-moved-past-near-wall-contact")
    seen = {(row["control"], row["where"]) for row in found["controls"]}
    assert seen == {(c, w) for c in controls for w in ("at-contact", "past-contact")}
    for row in found["controls"]:
        past = row["where"] == "past-contact"
        assert set(row["routes"]) == set(kernel.ROUTES)
        for verdict in row["routes"].values():
            assert verdict["passed"] is not past
            assert Fraction(verdict[row["margin"]]) == (-kernel.SHARP_EPSILON if past else 0)


def _pair(first: str, second: str) -> dict[str, Any]:
    identity = _json(reports.packet_path(DANIEL) / "measure/identity.json")
    (found,) = [p for p in identity["pairs"] if p["first"] == first and p["second"] == second]
    return found


def test_the_measured_identities_the_register_states() -> None:
    # 268: another placement of T-240's arrangement, under the mirror; not a re-solve.
    t240 = _pair("Daniel 268 (s268_lightning.cert)", "T-240 268 (#763 n268.cert)")[
        "nearest_centre"
    ]
    assert (t240["one_to_one"], t240["symmetry"]) == (True, 4)
    assert (t240["moved_beyond"]["1e-1"], t240["moved_beyond"]["1e-3"]) == (0, 135)
    assert t240["moved_beyond"]["1e-9"] == 165
    own = _pair(
        "Daniel 268 (s268_lightning.cert)", "Daniel 268 input (s268_lightning.input.txt)"
    )
    assert own["nearest_centre"]["symmetry"] == 0
    assert own["nearest_centre"]["moved_beyond"]["1e-3"] == 0
    # 304: T-241's packing descended; the source's input is that packing to 2.05e-9.
    t241 = _pair(
        "Daniel 304 (s304_pub.cert)", "Couzo 304 (fa6237e certificates/best/n304.cert)"
    )["nearest_centre"]
    assert (t241["one_to_one"], t241["symmetry"], t241["moved_beyond"]["1e-3"]) == (True, 0, 0)
    assert float(t241["largest_displacement"]) < 5e-4
    given = _pair(
        "Daniel 304 input (s304_pub.input.txt)",
        "Couzo 304 (fa6237e certificates/best/n304.cert)",
    )["nearest_centre"]
    assert float(given["largest_displacement"]) < 3e-9
    # Couzo's 304 is another arrangement than the house's.
    house = _pair("Couzo 304 (fa6237e certificates/best/n304.cert)", "T-186 304 (house)")
    assert house["nearest_centre"]["one_to_one"] is False
    assert house["assignment"]["moved_beyond"]["1e-1"] == 54
