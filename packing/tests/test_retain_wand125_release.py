"""What a stage 4 replay reads, retained from a wand125 release asset by its pins.

`devtools.retain_wand125_release` writes chosen members of a pinned release asset and
chosen documents of the pinned commit into a packet written as authored facts, refusing
any byte whose digest is not the packet's source manifest's, and for a linear
certificate the acquisition pins `devtools.audit_wand125_linear` reads. The synthetic
packet here holds it to that contract and to its refusals; the retained packets of 11
October are held to their manifests.
"""

from __future__ import annotations

import dataclasses
import hashlib
import io
import json
import tarfile
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_wand125_point_and_mixed as mixed
from devtools import retain_wand125_release as retain
from devtools.retained_data import git_blob, read_retained_bytes

NAME = "mixed_n3_L4"
BUNDLE = "n3-L4-proof-bundle.tar.gz"
#: A retained code file whose bytes a document of the synthetic commit repeats.
CODE = (
    "packing/resources/web/wand125-point-and-mixed-2026-09-28/square-packing-bounds/"
    "certificates/mixed_n50_L740/code/score.py"
)
WEB = retain.PROJECT / "resources/web"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tarball(files: dict[str, bytes]) -> bytes:
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w:gz") as archive:
        for name, data in files.items():
            info = tarfile.TarInfo(name)
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))
    return stream.getvalue()


@dataclasses.dataclass
class Synthetic:
    packet: Path
    asset: Path
    members: dict[str, bytes]
    documents: dict[str, bytes]

    def fetch(self, url: str) -> bytes:
        prefix = f"/problems/square-lower-bounds/certificates/{NAME}/"
        return self.documents[url.split(prefix, 1)[1]]


def synthetic(tmp_path: Path, *, outside: bool = False) -> Synthetic:
    """A packet of one linear certificate, its asset and its commit's documents."""
    members = {
        "candidate.json": b"".join(b'{"row": %d}\n' % k for k in range(1200)),
        "certificate.json": b'{"results": {}}\n',
        BUNDLE: b"a proof bundle",
    }
    documents = {
        "README.md": b"# certificate\n",
        "manifest.json": b'{"n": 3}\n',
        "completion-audit.json": b'{"status": "AUDITED_AND_PACKAGED"}\n',
        "code/score.py": (retain.REPO / CODE).read_bytes(),
        "ASSET.json": b"{}\n",
    }
    files = {f"certificates/{NAME}/{name}": data for name, data in members.items()}
    if outside:
        files["elsewhere/extra.txt"] = b"x"
    data = tarball(files)
    tmp_path.mkdir(parents=True, exist_ok=True)
    asset = tmp_path / f"certificates__{NAME}.tar.gz"
    asset.write_bytes(data)
    notice = retain.NOTICE_COPY.read_bytes()
    manifest: dict[str, Any] = {
        "source_repository": "wand125/square-packing",
        "source_revision": "f" * 40,
        "source_revision_date": "2026-10-10T00:00:00Z",
        "release": {
            "repository": "wand125/square-packing",
            "tag": "square-lower-bounds-v1",
            "asset": asset.name,
            "url": f"https://example.invalid/{asset.name}",
            "bytes": len(data),
            "sha256": sha256(data),
        },
        "asset_members": [
            {"path": name, "bytes": len(value), "sha256": sha256(value)}
            for name, value in members.items()
        ],
        "source_documents": [
            {
                "path": f"problems/square-lower-bounds/certificates/{NAME}/{name}",
                "bytes": len(value),
                "sha256": sha256(value),
                **({"byte_identical_to_retained": CODE} if name.startswith("code/") else {}),
            }
            for name, value in documents.items()
        ],
        "license": {
            "project_notice": {
                "path": "problems/square-lower-bounds/LICENSE",
                "bytes": len(notice),
                "git_blob": git_blob(notice),
            }
        },
    }
    packet = tmp_path / "packet"
    packet.mkdir()
    (packet / "source-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return Synthetic(packet, asset, members, documents)


def retained(case: Synthetic, **changes: Any) -> dict[str, Any]:
    options: dict[str, Any] = {
        "members": ["candidate.json", "certificate.json"],
        "documents": ["README.md", "manifest.json", "completion-audit.json"],
        "write_acquisition": True,
        "fetch": case.fetch,
    } | changes
    return retain.retain(case.packet, NAME, case.asset, **options)


def test_members_and_documents_are_retained_by_the_archives_rule(tmp_path: Path) -> None:
    case = synthetic(tmp_path)
    result = retained(case)
    directory = case.packet / retain.ARCHIVED / "certificates" / NAME
    # The candidate has more than 1,000 lines, so it is stored as deterministic gzip.
    assert result["retained"]["candidate.json"].endswith("candidate.json.gz")
    assert (directory / "candidate.json.gz").is_file()
    assert not (directory / "candidate.json").exists()
    assert (directory / "certificate.json").is_file()
    assert len(result["compressed_rows"]) == 1
    expected = case.members | case.documents
    for name in ("candidate.json", "certificate.json", "README.md", "manifest.json"):
        assert read_retained_bytes(directory / name) == expected[name]
    # Nothing else of the asset or the commit is written.
    written = {path.name for path in directory.rglob("*") if path.is_file()}
    assert written == {
        "candidate.json.gz",
        "certificate.json",
        "README.md",
        "manifest.json",
        "completion-audit.json",
    }


def test_the_acquisition_pins_are_the_ones_the_linear_tools_read(tmp_path: Path) -> None:
    case = synthetic(tmp_path)
    retained(case)
    certificate = dataclasses.replace(
        mixed.MIXED["n84"],
        packet=case.packet,
        directory=Path("certificates", NAME),
        tarball=BUNDLE,
    )
    tree = mixed.read_subtree_manifest(certificate.subtree)
    files = case.members | case.documents
    assert tree == {Path("certificates", NAME, k): sha256(v) for k, v in files.items()} | {
        Path("LICENSE"): sha256(retain.NOTICE_COPY.read_bytes())
    }
    bundle = case.members[BUNDLE]
    assert mixed.tarball_pin(certificate) == (sha256(bundle), len(bundle))
    pin = mixed.release_pin(certificate)
    assert pin is not None
    assert pin["url"] == f"https://example.invalid/{case.asset.name}"
    assert pin["sha256"] == sha256(case.asset.read_bytes())
    assert pin["member"]["member"] == f"certificates/{NAME}/{BUNDLE}"
    record = json.loads(certificate.record.read_text(encoding="utf-8"))
    assert record["format"] == retain.FORMAT
    pinned = {row["path"]: row for row in record["sources"][0]["pinned_only"]}
    assert "release asset" in pinned[f"certificates/{NAME}/{BUNDLE}"]["reason"]
    assert pinned[f"certificates/{NAME}/code/score.py"]["identical_to"] == CODE
    assert pinned["LICENSE"]["identical_to"].endswith("wand125-rectangles/LICENSE")
    kept = {row["path"] for row in record["sources"][0]["retained"]}
    assert kept.isdisjoint(pinned)
    assert kept | set(pinned) == {path.as_posix() for path in tree}


def test_an_asset_that_is_not_the_pinned_one_is_refused(tmp_path: Path) -> None:
    case = synthetic(tmp_path)
    case.asset.write_bytes(case.asset.read_bytes() + b"\0")
    with pytest.raises(ValueError, match="is not"):
        retained(case)


def test_a_member_off_the_manifest_or_outside_the_directory_is_refused(
    tmp_path: Path,
) -> None:
    case = synthetic(tmp_path / "outside", outside=True)
    with pytest.raises(ValueError, match="unexpected archive member"):
        retained(case)
    case = synthetic(tmp_path / "changed")
    manifest = json.loads((case.packet / "source-manifest.json").read_text())
    manifest["asset_members"][0]["sha256"] = "0" * 64
    (case.packet / "source-manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="not the listed member"):
        retained(case)


def test_a_document_that_is_not_the_pinned_one_is_refused(tmp_path: Path) -> None:
    case = synthetic(tmp_path)
    case.documents["manifest.json"] = b'{"n": 4}\n'
    with pytest.raises(ValueError, match=r"manifest\.json is not the pinned one"):
        retained(case)


def test_only_members_and_documents_the_manifest_pins_are_taken(tmp_path: Path) -> None:
    case = synthetic(tmp_path)
    with pytest.raises(ValueError, match="not members of the asset"):
        retained(case, members=["run.jsonl.gz"])
    with pytest.raises(ValueError, match="not pinned documents"):
        retained(case, documents=["LICENSE"])


# --------------------------------------------------------------------------- the packets

#: Each packet retained on 11 October, with the certificates it retains.
RETAINED = {
    "wand125-fine-net-n29-2026-10-10": ("mixed_n29_L582",),
    "wand125-fine-net-n28-n30-2026-10-10": ("mixed_n28_L57425", "mixed_n30_L58925"),
    "wand125-linear-n122-2026-10-10": ("mixed_n122_L1126",),
}


@pytest.mark.parametrize("packet", sorted(RETAINED))
def test_each_retained_file_is_the_bytes_its_manifest_pins(packet: str) -> None:
    root = WEB / packet
    manifest = json.loads((root / "source-manifest.json").read_text(encoding="utf-8"))
    stored = manifest["raw_bytes_retained"]["files"]
    assert manifest["raw_bytes_in_git"] is True
    on_disk = sorted(
        path.relative_to(root).as_posix()
        for path in (root / retain.ARCHIVED).rglob("*")
        if path.is_file()
    )
    assert on_disk == sorted(stored)
    for name in RETAINED[packet]:
        entry = retain.certificate_entry(manifest, name)
        pins = {row["path"]: row["sha256"] for row in entry["asset_members"]}
        pins |= {
            relative: row["sha256"]
            for relative, row in retain.documents_of(entry, name).items()
        }
        directory = root / retain.ARCHIVED / "certificates" / name
        for path in sorted(directory.iterdir()):
            upstream = path.name.removesuffix(".gz")
            assert sha256(read_retained_bytes(directory / upstream)) == pins[upstream], path


def test_the_n122_subtree_pins_are_its_manifests_digests() -> None:
    root = WEB / "wand125-linear-n122-2026-10-10"
    manifest = json.loads((root / "source-manifest.json").read_text(encoding="utf-8"))
    entry = retain.certificate_entry(manifest, "mixed_n122_L1126")
    tree = mixed.read_subtree_manifest(root / "acquisition/upstream-subtree.sha256")
    directory = Path("certificates/mixed_n122_L1126")
    expected = {directory / row["path"]: row["sha256"] for row in entry["asset_members"]}
    expected |= {
        directory / relative: row["sha256"]
        for relative, row in retain.documents_of(entry, "mixed_n122_L1126").items()
    }
    expected[Path("LICENSE")] = sha256(retain.NOTICE_COPY.read_bytes())
    assert tree == expected
