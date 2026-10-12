"""Issues #503 and #504: PingYou Ltd's certificates at 207 and 153, imported by declaration.

Each release states its packing twice, as ``[x, y, t]`` JSON (`pingyou-json`) and as a
rational corners Witness/v2 (`witness-corners`); neither is retained, so ``derive`` holds
the second to the first from a checkout at the pin. The general importer's checks run on
both packets through ``test_upper_bound_reports``; these hold the two adapters, the
derive-time comparison and what is particular to the packets. Only the synthetic
upstream below needs Git; nothing needs the network.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from collections.abc import Mapping
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
from test_upper_bound_reports import CENTRED, DELEEUW

from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools import upper_bound_reports as reports

N207 = "pingyou-n207-certificate-2026-10-11"
N153 = "pingyou-n153-certificate-2026-10-11"
SIDES = {
    N207: (207, Fraction(148809603730436756319360591381170501178639, 10**40)),
    N153: (153, Fraction(6435006925203522001385040447, 5 * 10**26)),
}
#: The digests issues #503 and #504 state for each release's certificate and witness.
STATED = {
    N207: {
        "n207.cert.json": "1c334f3170ece68cf2c2f16341660f7a80ef44bf7a9cdb083940d1b99756c071",
        "pingyou-n207-rational.yaml": (
            "09e6d0dff17ae71ae84bde1466b805a67f3b1592496f9ca438b02bde603f6182"
        ),
        "01-squares-project.zip": (
            "d3b6505292ce647903708c7e5d6f8476a686d360ebcc22547dbd3c20ebe96ed6"
        ),
    },
    N153: {
        "n153.cert.json": "31b3fb3cba73528fab21d085a34f3209684a868e7116059ea5c21e664bca1ff2",
        "pingyou-n153-rational.yaml": (
            "963d6ca7cce053e7ff22baf6438bdf5776b7b06d01e1509e654c73966b9e4d41"
        ),
        "n153-squares-project.zip": (
            "dcc512828a8b6629d2d414f4ac20d417c2a4d5dc2968b9abe586676abe868d97"
        ),
    },
}


def _bytes(value: Any) -> bytes:
    return json.dumps(value).encode()


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


#: The synthetic upstream's commit time, which dates the synthetic packet.
DATE = "2026-10-10T00:00:00Z"


def _git(directory: Path, *arguments: str) -> str:
    environment = {**os.environ, "GIT_AUTHOR_DATE": DATE, "GIT_COMMITTER_DATE": DATE}
    identity = ["-c", "user.name=Test", "-c", "user.email=test@example.invalid"]
    completed = subprocess.run(
        ["git", *identity, "-C", str(directory), *arguments],
        capture_output=True,
        text=True,
        check=True,
        env=environment,
    )
    return completed.stdout.strip()


def _readme(packet: Path, rows: list[Any]) -> None:
    """The packet README's Compressed Files table, which custody holds to the facts."""
    table = "\n".join(row.markdown() for row in rows)
    (packet / "README.md").write_text(
        "# Synthetic\n\n## Compressed Files\n\n"
        "| Stored File | Origin | Git Blob of Original | SHA-256 of Original |\n"
        f"| --- | --- | --- | --- |\n{table}\n"
    )


# --------------------------------------------------------------------------- pingyou-json

#: The synthetic two-square packing of ``test_upper_bound_reports``, centres in [0, 3]^2.
ROWS = [["1", "1", "0"], ["2", "2", "1/3"]]
PINGYOU = {
    "n": 2,
    "s_exact": "3",
    "note": "rational centers and t=tan(theta/2)",
    "dilation_exact": "5000000000001/5000000000000",
    "raw_side": 2.9999999999994,
    "squares": ROWS,
    "provenance": {"construction": "synthetic", "angle": 39.09},
}


def _expected() -> legacy.Certificate:
    return reports.parse_certificate(_bytes(CENTRED), 2, "centred-json")


def test_the_pingyou_rows_read_as_the_centred_certificate_does() -> None:
    assert reports.parse_certificate(_bytes(PINGYOU), 2, "pingyou-json") == _expected()
    bare = {key: PINGYOU[key] for key in ("n", "s_exact", "squares")}
    assert reports.parse_certificate(_bytes(bare), 2, "pingyou-json") == _expected()


@pytest.mark.parametrize(
    "value",
    [
        {**PINGYOU, "s_decimal": "3.0"},
        {**PINGYOU, "raw_side": "3"},
        {**PINGYOU, "raw_side": True},
        {**PINGYOU, "provenance": ["synthetic"]},
        {**PINGYOU, "dilation_exact": 1},
        {key: item for key, item in PINGYOU.items() if key != "s_exact"},
    ],
)
def test_the_pingyou_adapter_refuses_fields_its_format_does_not_state(
    value: Mapping[str, Any],
) -> None:
    with pytest.raises(reports.ReportError, match="PingYou certificate"):
        reports.parse_certificate(_bytes(value), 2, "pingyou-json")


# --------------------------------------------------------------------------- witness-corners


def _corners(certificate: legacy.Certificate) -> dict[str, Any]:
    """The certificate as a rational corners Witness/v2, in the order sqpack writes."""
    return {
        "softschema": {
            "contract": "packing.squares:Witness/v2",
            "schema": "witness.schema.yaml",
            "envelope": "witness",
            "status": "enforced",
        },
        "witness": {
            "id": "W-synthetic-corners",
            "n": certificate.n,
            "side": legacy.literal(certificate.side),
            "square_size": "1",
            "representation": "corners",
            "scalar": {"kind": "rational"},
            "coordinates": dict(reports.CORNER_FRAME),
            "squares": [
                {
                    "id": index,
                    "corners": [
                        [legacy.literal(x), legacy.literal(y)]
                        for x, y in reports.pose_corners(pose)
                    ],
                }
                for index, pose in enumerate(certificate.poses, start=1)
            ],
            "claim": {
                "coordinate_provenance": "verified",
                "method": "exact-algebraic",
                "limitations": "Synthetic.",
            },
            "certificate": {"kind": "exact-rational-sat"},
        },
    }


def test_a_corner_witness_reads_back_to_the_poses_it_draws() -> None:
    document = _corners(_expected())
    assert reports.parse_certificate(_bytes(document), 2, "witness-corners") == _expected()


def test_corners_listed_from_another_vertex_read_as_another_packing() -> None:
    document = _corners(_expected())
    corners = document["witness"]["squares"][1]["corners"]
    corners.append(corners.pop(0))
    turned = reports.parse_certificate(_bytes(document), 2, "witness-corners")
    assert turned != _expected()
    assert turned.poses[1].x == _expected().poses[1].x
    assert turned.poses[1].t != _expected().poses[1].t


def _mutate(kind: str) -> dict[str, Any]:
    document = _corners(_expected())
    witness = document["witness"]
    if kind == "not-a-square":
        witness["squares"][1]["corners"][2][0] += "1"
    elif kind == "clockwise":
        witness["squares"][1]["corners"].reverse()
    elif kind == "frame":
        witness["coordinates"]["origin"] = "container-center"
    elif kind == "schema":
        document["softschema"]["schema"] = "../../witness.schema.yaml"
    elif kind == "order":
        witness["squares"].reverse()
    elif kind == "count":
        witness["n"] = 1
        witness["squares"].pop()
    elif kind == "algebraic":
        witness["squares"][0]["corners"][0][0] = ["1", "0"]
    return document


@pytest.mark.parametrize(
    ("kind", "message"),
    [
        ("not-a-square", "not a unit square's"),
        ("clockwise", "not a unit square's"),
        ("frame", "lower-left frame"),
        ("schema", "as its schema"),
        ("order", "numbered 1..n"),
        ("count", "lower-left frame"),
        ("algebraic", "rational string"),
    ],
)
def test_a_corner_witness_refuses_what_is_no_unit_square_in_order(
    kind: str, message: str
) -> None:
    with pytest.raises(reports.ReportError, match=message):
        reports.parse_certificate(_bytes(_mutate(kind)), 2, "witness-corners")


# --------------------------------------------------------------------------- derive


@pytest.fixture
def synthetic(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A private repository root the importer and its kernel write into."""
    repo = tmp_path / "private"
    web = repo / reports.WEB.relative_to(reports.REPO)
    monkeypatch.setattr(reports, "REPO", repo)
    monkeypatch.setattr(reports, "WEB", web)
    monkeypatch.setattr(kernel, "REPO", repo)
    return repo


def _derived_pair(tmp_path: Path, witness: Mapping[str, Any]) -> tuple[Path, Path]:
    """A derived-only packet whose certificate row names a corner witness of its packing."""
    upstream = tmp_path / "upstream"
    upstream.mkdir()
    _git(upstream, "init", "--quiet")
    (upstream / "certificate.json").write_text(json.dumps(CENTRED, indent=2) + "\n")
    (upstream / "witness.yaml").write_text(json.dumps(witness, indent=2) + "\n")
    _git(upstream, "add", "certificate.json", "witness.yaml")
    _git(upstream, "commit", "--quiet", "-m", "certificate and witness")
    packet = reports.WEB / "synthetic-pair-2026-10-10"
    (packet / "acquisition").mkdir(parents=True)
    _write_json(
        packet / "acquisition/declaration.json",
        {
            "format": "external-source-declaration-v1",
            "id": "synthetic-pair",
            "source_url": "https://example.invalid/synthetic-pair",
            "source_ref": "main",
            "source_commit": _git(upstream, "rev-parse", "HEAD"),
            "retrieved_at_utc": "2026-10-11T00:00Z",
            "git_scope": "Both files of a synthetic one-commit repository.",
            "archived_dir": "source",
            "license": "None stated: derived-only custody.",
            "claims": ["s(2) <= 3, a synthetic certificate and its corner witness."],
            "scope": ["certificate.json", "witness.yaml"],
            "pinned_only": [{"match": "*", "reason": "Derived-only custody."}],
        },
    )
    reports.acquire_source.acquire(packet, upstream, reports.REPO)
    deleeuw = reports.ROOT / "resources/web" / DELEEUW / reports.DECLARATION
    declaration = _json(deleeuw)
    declaration.update(
        {
            "issue": "https://example.invalid/issue",
            "certificates": [
                {
                    "n": 2,
                    "path": "certificate.json",
                    "format": "centred-json",
                    "offered": "3.0",
                    "first_committed": DATE,
                    "same_packing": [{"path": "witness.yaml", "format": "witness-corners"}],
                    "fact": "facts/n-002.yaml",
                }
            ],
            "requested": [2],
            "replayed": [2],
            "houses": [
                {
                    "n": 2,
                    "reader": "grid",
                    "source_key": "[Kingbird]",
                    "holders": "the grid",
                    "reported_value": "2",
                    "verified_value": "2",
                    "evidence": ["E-basic-grid-upper"],
                }
            ],
            "pending": [],
        }
    )
    _write_json(packet / reports.DECLARATION, declaration)
    _readme(packet, [])
    return packet, upstream


def test_derive_holds_a_pinned_corner_witness_to_the_certificate(
    synthetic: Path, tmp_path: Path
) -> None:
    assert synthetic == reports.REPO
    packet, upstream = _derived_pair(tmp_path, _corners(_expected()))
    _readme(packet, reports.derive(packet, upstream))
    assert reports.read_facts(packet) == {2: _expected()}
    assert [row.stored for row in reports.derive(packet, upstream, check=True)] == [
        "facts/n-002.yaml.gz"
    ]


def test_derive_refuses_a_pinned_witness_of_another_packing(
    synthetic: Path, tmp_path: Path
) -> None:
    assert synthetic == reports.REPO
    second = legacy.Pose(Fraction(2), Fraction(2), Fraction(0))
    other = legacy.Certificate(2, Fraction(3), (_expected().poses[0], second))
    packet, upstream = _derived_pair(tmp_path, _corners(other))
    with pytest.raises(reports.ReportError, match=r"witness\.yaml states another packing"):
        reports.derive(packet, upstream)
    assert not (packet / "facts").exists()


def test_derive_reads_only_files_the_packet_pins(synthetic: Path, tmp_path: Path) -> None:
    assert synthetic == reports.REPO
    packet, upstream = _derived_pair(tmp_path, _corners(_expected()))
    path = packet / reports.DECLARATION
    declaration = _json(path)
    declaration["certificates"][0]["same_packing"][0]["path"] = "README.md"
    _write_json(path, declaration)
    shutil.copyfile(upstream / "witness.yaml", upstream / "README.md")
    with pytest.raises(reports.ReportError, match="not a file this packet pins"):
        reports.derive(packet, upstream)


# --------------------------------------------------------------------------- the packets


@pytest.mark.parametrize("name", [N207, N153])
def test_each_packet_pins_the_release_and_retains_no_upstream_byte(name: str) -> None:
    packet = reports.packet_path(name)
    (source,) = _json(packet / "acquisition/sources.json")["sources"]
    assert (source["retained_file_count"], source["retained_total_bytes"]) == (0, 0)
    pinned = {item["path"]: item["sha256"] for item in source["pinned_only"]}
    assert {path: pinned[path] for path in STATED[name]} == STATED[name]
    declaration = reports.load_declaration(packet)
    (row,) = declaration["certificates"]
    assert [other["path"] for other in row.get("same_packing", [])] == [
        path for path in STATED[name] if path.endswith("rational.yaml")
    ]


@pytest.mark.parametrize("name", [N207, N153])
def test_each_fact_is_the_issue_side_and_the_smallest_report_at_its_count(name: str) -> None:
    n, side = SIDES[name]
    packet = reports.packet_path(name)
    assert reports.read_facts(packet)[n].side == side
    (row,) = reports.check_claims(packet)["results"]
    assert row["smallest"] == reports.THIS
    assert row["case"]["relation"] == "below"
    assert row["case"]["result"] == "T-127"
    for other in row["pending"]:
        assert other["relation"] == "below"
        assert "printed" not in other
        assert Fraction(other["exact_side"]) == reports.house_side(
            {
                "T-136": "[SQUISH third request 2026-10-09]",
                "T-146": "[Daniel regularized lists 2026-10-10]",
            }[other["result"]],
            n,
        )


def test_the_153_claims_read_the_regularized_side_the_issue_names() -> None:
    (row,) = reports.check_claims(reports.packet_path(N153))["results"]
    regularized = next(other for other in row["pending"] if other["result"] == "T-146")
    assert Fraction(regularized["exact_side"]) == Fraction(
        402250932783786874180075932249, 31250000000000000000000000000
    )
    # The side reduction issue #504 prints, exactly.
    assert Fraction(regularized["difference"]) == Fraction("0.002015998674135970992348937968")
