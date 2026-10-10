"""Complete pinned source custody and derived-only outside-horizon retention."""

from __future__ import annotations

import json
import lzma
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from types import MappingProxyType
from typing import Any

import pytest

from devtools import check_source_coverage
from devtools import couzo_extended_reports as reports
from sqpack.yamlio import load_yaml

#: The source's binary64 renderings: a side as `.15f`, a coordinate as `.17e`.
SIDE = f"{20.0:.15f}"
ZERO = format(0.0, ".17e")


def synthetic_source(
    side: str = SIDE, token: str = ZERO
) -> tuple[dict[str, Any], dict[str, tuple[str, str]]]:
    """All twenty counts, historical roles and nested tree structure, no geometry."""
    trees: dict[str, dict[str, Any]] = {sha: {} for sha in reports.COMMITS}
    blobs: dict[str, str] = {}
    inputs = []
    for commit, path, role in sorted(reports.input_roster()):
        if role == "current-outside-horizon" and path.endswith(".txt"):
            n = int(path.removeprefix("n").removesuffix(".txt"))
            text = reports.canonical_pose(n, side, [(token, token, token)] * n)
        else:
            text = f"ordinary fixture {commit} {path}\n"
        raw = text.encode()
        sha = reports.git_identity("blob", raw)
        leaf = {
            "path": path,
            "mode": "100644",
            "type": "blob",
            "sha": sha,
            "size": len(raw),
            "url": f"https://api.github.com/repos/{reports.REPOSITORY}/git/blobs/{sha}",
        }
        trees[commit][path] = leaf
        blobs[sha] = text
        inputs.append({**leaf, "commit": commit, "role": role})
    for commit in reports.COMMITS:
        sha = reports.git_identity("blob", b"unselected nested source")
        path = "certificates/context.txt"
        trees[commit][path] = {
            "path": path,
            "mode": "100644",
            "type": "blob",
            "sha": sha,
            "size": 24,
            "url": f"https://api.github.com/repos/{reports.REPOSITORY}/git/blobs/{sha}",
        }
    pins = {
        sha: (reports.tree_root(trees[sha]), reports.PINS[sha][1]) for sha in reports.COMMITS
    }
    return {
        "format": reports.FORMAT,
        "repository": reports.REPOSITORY,
        "standing_horizon": 324,
        "counts": list(reports.COUNTS),
        "commits": {
            sha: {"sha": sha, "tree": {"sha": root}, "parents": [{"sha": parent}]}
            for sha, (root, parent) in pins.items()
        },
        "trees": trees,
        "inputs": inputs,
        "blobs": blobs,
        "licensing": {"untrusted_source_metadata": True},
        "qualification": "synthetic custody fixture; overlapping poses are unverified",
    }, pins


@pytest.fixture
def ordinary_source(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    packet, pins = synthetic_source()
    monkeypatch.setattr(reports, "PINS", pins)
    return packet


@pytest.fixture(scope="module")
def derived_outputs() -> Mapping[str, bytes]:
    packet, pins = synthetic_source()
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(reports, "PINS", pins)
        return MappingProxyType(reports.export_contents(packet))


def test_git_tree_reconstruction_uses_directory_byte_order_and_executable_modes() -> None:
    blob = reports.git_identity("blob", b"one\n")

    def leaf(path: str, mode: str) -> dict[str, Any]:
        return {
            "path": path,
            "mode": mode,
            "type": "blob",
            "sha": blob,
            "size": 4,
            "url": f"https://api.github.com/repos/{reports.REPOSITORY}/git/blobs/{blob}",
        }

    nested = reports.git_identity("tree", b"100755 z\0" + bytes.fromhex(blob))
    body = b"100644 a.c\0" + bytes.fromhex(blob) + b"40000 a\0" + bytes.fromhex(nested)
    assert reports.tree_root({"a/z": leaf("a/z", "100755"), "a.c": leaf("a.c", "100644")}) == (
        reports.git_identity("tree", body)
    )


@pytest.mark.parametrize("path", ["", "/a", "a/", "a//b", "../a", "a/./b", "a\\b", "a\0b"])
def test_git_paths_refuse_noncanonical_names(path: str) -> None:
    with pytest.raises(ValueError, match=r"canonical Git path"):
        reports.path_parts(path)


def test_complete_source_fixture_retains_every_current_and_historical_role(
    ordinary_source: dict[str, Any],
) -> None:
    reports.check_ordinary(ordinary_source)
    assert len(ordinary_source["inputs"]) == 73
    assert {
        tuple(row[key] for key in ("commit", "path", "role"))
        for row in ordinary_source["inputs"]
    } == (reports.input_roster())


@pytest.mark.parametrize(
    "mutant",
    [
        "root",
        "parent",
        "nested-mode",
        "drop",
        "duplicate",
        "relabel",
        "orphan",
        "blob",
        "size",
        "extra-field",
        "counts",
        "horizon",
    ],
)
def test_source_custody_refuses_complete_input_and_lineage_mutants(
    ordinary_source: dict[str, Any],
    mutant: str,
) -> None:
    packet = deepcopy(ordinary_source)
    commit = reports.COMMITS[2]
    if mutant == "root":
        packet["commits"][commit]["tree"]["sha"] = "0" * 40
    elif mutant == "parent":
        packet["commits"][commit]["parents"][0]["sha"] = "0" * 40
    elif mutant == "nested-mode":
        packet["trees"][commit]["certificates/context.txt"]["mode"] = "100755"
    elif mutant == "drop":
        packet["inputs"].pop()
    elif mutant == "duplicate":
        packet["inputs"].append(deepcopy(packet["inputs"][-1]))
    elif mutant == "relabel":
        packet["inputs"][-1]["role"] = "source-context"
    elif mutant == "orphan":
        packet["blobs"]["0" * 40] = "unclaimed"
    elif mutant == "blob":
        packet["blobs"][packet["inputs"][-1]["sha"]] += "changed"
    elif mutant == "size":
        packet["inputs"][-1]["size"] += 1
    elif mutant == "extra-field":
        packet["unclaimed_raw_source"] = "new source"
    elif mutant == "counts":
        packet["counts"] = packet["counts"][:-1]
    else:
        packet["standing_horizon"] = True
    messages = {
        "root": "pinned Git root",
        "parent": "pinned Git root",
        "nested-mode": "pinned Git root",
        "drop": "role roster",
        "duplicate": "role roster",
        "relabel": "role roster",
        "orphan": "orphan source",
        "blob": "blob identity",
        "size": "pinned tree",
        "extra-field": "ordinary-source format",
        "counts": "scope or lineage",
        "horizon": "scope or lineage",
    }
    with pytest.raises(ValueError, match=messages[mutant]):
        reports.check_ordinary(packet)


def test_removed_source_absence_is_checked_even_with_self_consistent_tree(
    ordinary_source: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    packet = deepcopy(ordinary_source)
    old = reports.COMMITS[0]
    later = reports.COMMITS[1]
    path = f"n{reports.REMOVED[0]}.txt"
    packet["trees"][later][path] = deepcopy(packet["trees"][old][path])
    root = reports.tree_root(packet["trees"][later])
    pins = deepcopy(reports.PINS)
    pins[later] = (root, pins[later][1])
    monkeypatch.setattr(reports, "PINS", pins)
    packet["commits"][later]["tree"]["sha"] = root
    with pytest.raises(ValueError, match=r"removed input"):
        reports.check_ordinary(packet)


@pytest.mark.parametrize(
    "decoded",
    [
        b'{"a":1,"a":2}',
        b'{"a":NaN}',
        b'{"a":Infinity}',
        b'{"a":1e9999}',
        b"[]",
        b"\xff",
        b'{"a":',
    ],
)
def test_xz_json_refuses_duplicate_nonfinite_and_invalid_records(decoded: bytes) -> None:
    with pytest.raises(
        ValueError, match=r"duplicate JSON|nonfinite JSON|JSON object|UTF-8|utf-8|Expecting"
    ):
        reports.decode_xz(lzma.compress(decoded))


@pytest.mark.parametrize(
    "mutation", ["truncated", "concatenated", "trailing", "decoded", "compressed", "memory"]
)
def test_xz_stream_and_resource_boundaries(
    mutation: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    raw = lzma.compress(b'{"a":"value"}')
    if mutation == "truncated":
        raw = raw[:-1]
    elif mutation == "concatenated":
        raw += raw
    elif mutation == "trailing":
        raw += b"trailing"
    elif mutation == "decoded":
        monkeypatch.setattr(reports, "MAX_DECODED_BYTES", 5)
    elif mutation == "compressed":
        monkeypatch.setattr(reports, "MAX_COMPRESSED_BYTES", len(raw) - 1)
    else:
        monkeypatch.setattr(reports, "MAX_XZ_MEMORY", 1024)
    with pytest.raises(ValueError, match=r"XZ source|byte ceiling"):
        reports.decode_xz(raw)


@pytest.mark.parametrize(
    ("side", "row"),
    [
        ("0", ("0", "0", "0")),
        ("NaN", ("0", "0", "0")),
        ("20", ("Infinity", "0", "0")),
        ("20", ("1e1001", "0", "0")),
        ("20", ("1" * 129, "0", "0")),
    ],
)
def test_decimal_report_literals_are_finite_bounded_and_positive(
    side: str,
    row: tuple[str, str, str],
) -> None:
    with pytest.raises(ValueError, match=r"positive|decimal|literal|franciscouzo"):
        reports.parsed_pose(reports.canonical_pose(1, side, [row]), 1)


@pytest.mark.parametrize(
    ("side", "token"),
    [
        ("20.0", ZERO),
        ("20.00000000000000", ZERO),
        (SIDE, "0.0"),
        (SIDE, "0.0000000000000000e+00"),
        (SIDE, "0.00000000000000000E+00"),
        (SIDE, "1.00000000000000000e-01"),
        (SIDE, "1_0.00000000000000000e+00"),
    ],
)
def test_pose_tokens_must_be_the_binary64_renderings_the_claim_states(
    side: str,
    token: str,
) -> None:
    """`fact` writes a binary64-compatible encoding, so a token that is not one refuses."""
    with pytest.raises(ValueError, match=r"binary64"):
        reports.parsed_pose(reports.canonical_pose(1, side, [(token, ZERO, ZERO)]), 1)
    tenth = format(0.1, ".17e")
    assert reports.parsed_pose(reports.canonical_pose(1, SIDE, [(tenth, ZERO, ZERO)]), 1) == (
        SIDE,
        [(tenth, ZERO, ZERO)],
    )


def test_packet_check_refuses_a_self_consistent_packet_without_binary64_encoding(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Custody alone accepts these short tokens; only the encoding check refuses them."""
    packet, pins = synthetic_source(side="20.0", token="0.0")
    monkeypatch.setattr(reports, "PINS", pins)
    with pytest.raises(ValueError, match=r"binary64"):
        reports.export_contents(packet)
    with pytest.MonkeyPatch.context() as unchecked:
        unchecked.setattr(reports, "binary64_rendering", lambda _side, _rows: None)
        destination = write_derived(tmp_path, monkeypatch, reports.export_contents(packet))
        assert reports.check_packet(destination) == dict.fromkeys(reports.COUNTS, "20.0")
    with pytest.raises(ValueError, match=r"binary64"):
        reports.check_packet(destination)


def reordered(packet: Mapping[str, Any]) -> dict[str, Any]:
    """The same custody content, serialized in reversed key and list order."""
    shuffled = dict(reversed(list(deepcopy(packet).items())))
    shuffled["trees"] = {
        sha: {
            path: dict(reversed(list(leaf.items())))
            for path, leaf in reversed(list(leaves.items()))
        }
        for sha, leaves in reversed(list(packet["trees"].items()))
    }
    shuffled["inputs"] = [
        dict(reversed(list(row.items()))) for row in reversed(packet["inputs"])
    ]
    return shuffled


def test_export_bytes_depend_on_custody_content_not_preparation_order(
    ordinary_source: dict[str, Any],
    derived_outputs: Mapping[str, bytes],
) -> None:
    shuffled = reordered(ordinary_source)

    def identity(row: Mapping[str, Any]) -> tuple[str, str, str]:
        return row["commit"], row["path"], row["role"]

    assert {**shuffled, "inputs": []} == {**ordinary_source, "inputs": []}
    assert sorted(shuffled["inputs"], key=identity) == sorted(
        ordinary_source["inputs"], key=identity
    )
    assert list(shuffled["inputs"][0]) != list(ordinary_source["inputs"][0])
    assert reports.export_contents(shuffled) == dict(derived_outputs)
    custody = json.loads(derived_outputs["acquisition/sources.json"])["sources"][0]["custody"]
    assert [(row["commit"], row["path"], row["role"]) for row in custody["inputs"]] == (
        reports.input_order()
    )
    assert list(custody["trees"]) == sorted(reports.COMMITS)
    for leaves in custody["trees"].values():
        assert list(leaves) == sorted(leaves)
        assert all(list(leaf) == sorted(leaf) for leaf in leaves.values())


@pytest.mark.usefixtures("ordinary_source")
@pytest.mark.parametrize("mutation", ["input-order", "leaf-order", "key-order", "layout"])
def test_retained_metadata_must_be_the_canonical_export_bytes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    derived_outputs: Mapping[str, bytes],
    mutation: str,
) -> None:
    """Reordered or re-laid-out metadata with the same content refuses; the original passes."""
    destination = write_derived(tmp_path, monkeypatch, derived_outputs)
    path = destination / "acquisition/sources.json"
    original = path.read_bytes()
    value = reports.read_json(path)
    assert (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode() == original
    custody = value["sources"][0]["custody"]
    if mutation == "input-order":
        custody["inputs"].reverse()
    elif mutation == "leaf-order":
        leaves = custody["trees"][reports.COMMITS[2]]
        custody["trees"][reports.COMMITS[2]] = dict(reversed(list(leaves.items())))
    elif mutation == "key-order":
        custody["inputs"] = [dict(reversed(list(row.items()))) for row in custody["inputs"]]
    indent = 1 if mutation == "layout" else 2
    path.write_text(json.dumps(value, indent=indent, ensure_ascii=False) + "\n")
    with pytest.raises(ValueError, match=r"canonical export"):
        reports.check_packet(destination)
    path.write_bytes(original)
    assert len(reports.check_packet(destination)) == 20


def write_derived(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    outputs: Mapping[str, bytes],
) -> Path:
    destination = tmp_path / reports.PACKET.name
    monkeypatch.setattr(reports, "REPO", tmp_path)
    for name, raw in outputs.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    (destination / "README.md").write_text("Derived numerical facts only.\n")
    return destination


def test_derived_export_preserves_complete_pose_tokens_without_raw_assets(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    ordinary_source: dict[str, Any],
    derived_outputs: Mapping[str, bytes],
) -> None:
    destination = write_derived(tmp_path, monkeypatch, derived_outputs)
    claims = reports.check_packet(destination)
    assert claims == dict.fromkeys(reports.COUNTS, SIDE)
    record = reports.read_json(destination / "acquisition/sources.json")
    source = record["sources"][0]
    assert set(source) == reports.SOURCE_KEYS
    assert set(source["custody"]) == reports.CUSTODY_KEYS
    assert source["raw_asset_retained"] is False
    assert source["licence"] is None
    assert not list(destination.rglob("*.txt"))
    assert not list(destination.rglob("*.svg"))
    assert len(list((destination / "facts").glob("*.yaml"))) == 20
    assert (
        source["cases"][-1]["source_blob"]
        == ordinary_source["trees"][reports.COMMITS[2]]["n379.txt"]["sha"]
    )
    # The all-overlapping synthetic poses pass custody and representation, never geometry.


@pytest.mark.parametrize(
    "mutation", ["source-raw", "custody-raw", "commit-message", "licence", "assurance"]
)
def test_derived_metadata_cannot_add_raw_bytes_or_promote_source_claims(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    ordinary_source: dict[str, Any],
    mutation: str,
    derived_outputs: Mapping[str, bytes],
) -> None:
    destination = write_derived(tmp_path, monkeypatch, derived_outputs)
    path = destination / "acquisition/sources.json"
    value = reports.read_json(path)
    source = value["sources"][0]
    if mutation == "source-raw":
        source["raw_source"] = "upstream bytes"
    elif mutation == "custody-raw":
        source["custody"]["blobs"] = ordinary_source["blobs"]
    elif mutation == "commit-message":
        source["custody"]["commits"][reports.COMMITS[0]]["message"] = "unbound claim"
    elif mutation == "licence":
        source["licence"] = "permission not established"
    else:
        source["qualification"] = "verified geometry"
    path.write_text(json.dumps(value))
    with pytest.raises(
        ValueError, match=r"retention differs|raw source fields|commit metadata"
    ):
        reports.check_packet(destination)


@pytest.mark.usefixtures("ordinary_source")
@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ("commit-root", "commit metadata"),
        ("commit-parent", "commit metadata"),
        ("tree-mode", "pinned Git root"),
    ],
)
def test_retained_lineage_is_compared_whole_and_its_trees_rebuilt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    derived_outputs: Mapping[str, bytes],
    mutation: str,
    message: str,
) -> None:
    """The retained commit block is held whole against PINS, and every tree is rebuilt."""
    destination = write_derived(tmp_path, monkeypatch, derived_outputs)
    path = destination / "acquisition/sources.json"
    value = reports.read_json(path)
    custody = value["sources"][0]["custody"]
    commit = reports.COMMITS[2]
    if mutation == "commit-root":
        custody["commits"][commit]["tree"]["sha"] = "0" * 40
    elif mutation == "commit-parent":
        custody["commits"][commit]["parents"][0]["sha"] = "0" * 40
    else:
        custody["trees"][commit]["certificates/context.txt"]["mode"] = "100755"
    path.write_text(json.dumps(value))
    with pytest.raises(ValueError, match=message):
        reports.check_packet(destination)


@pytest.mark.usefixtures("ordinary_source")
def test_fixed_schema_envelope_refuses_before_selected_schema_io(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    derived_outputs: Mapping[str, bytes],
) -> None:
    destination = write_derived(tmp_path, monkeypatch, derived_outputs)
    path = destination / "facts/n-327.yaml"
    original = path.read_bytes()
    outside = tmp_path / "outside-schema.yaml"
    outside.write_text("{}\n")
    path.write_bytes(
        original.replace(b"../../../../witnesses/witness.schema.yaml", str(outside).encode(), 1)
    )
    reads: list[Path] = []
    original_read = Path.read_text

    def read_guard(path: Path, *args: Any, **kwargs: Any) -> str:
        if path.resolve() == outside.resolve():
            reads.append(path)
            raise AssertionError("fact-selected schema must never be read")
        return original_read(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", read_guard)
    with pytest.raises(ValueError, match=r"fixed schema envelope"):
        reports.check_packet(destination)
    assert reads == []
    path.write_bytes(original)
    assert len(reports.check_packet(destination)) == 20
    assert reads == []


@pytest.mark.usefixtures("ordinary_source")
def test_last_derived_pose_mutation_refuses_and_restoration_passes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    derived_outputs: Mapping[str, bytes],
) -> None:
    destination = write_derived(tmp_path, monkeypatch, derived_outputs)
    path = destination / "facts/n-379.yaml"
    original = path.read_bytes()
    edited = format(0.1, ".17e").encode()
    path.write_bytes(original.replace(b"angle: '" + ZERO.encode(), b"angle: '" + edited, 1))
    with pytest.raises(ValueError, match=r"complete pinned source"):
        reports.check_packet(destination)
    path.write_bytes(original.replace(reports.SOURCE_KEY.encode(), b"[unbound attribution]"))
    with pytest.raises(ValueError, match=r"derived witness metadata"):
        reports.check_packet(destination)
    path.write_bytes(original)
    assert len(reports.check_packet(destination)) == 20


@pytest.mark.usefixtures("ordinary_source")
def test_derived_metadata_symlink_and_orphan_asset_refuse(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    derived_outputs: Mapping[str, bytes],
) -> None:
    destination = write_derived(tmp_path, monkeypatch, derived_outputs)
    path = destination / "acquisition/sources.json"
    original = path.read_bytes()
    elsewhere = tmp_path / "outside.json"
    elsewhere.write_bytes(original)
    path.unlink()
    path.symlink_to(elsewhere)
    with pytest.raises(ValueError, match=r"private"):
        reports.check_packet(destination)
    path.unlink()
    path.write_bytes(original)
    (destination / "n327.svg").write_text("<svg/>")
    with pytest.raises(ValueError, match=r"unexpected"):
        reports.check_packet(destination)


def test_export_preflight_refuses_before_creating_any_packet_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    ordinary_source: dict[str, Any],
) -> None:
    monkeypatch.setattr(reports, "REPO", tmp_path)
    source = tmp_path / "ordinary.json.xz"
    ordinary_source["inputs"].pop()
    source.write_bytes(lzma.compress(json.dumps(ordinary_source).encode()))
    destination = tmp_path / "new-packet"
    with pytest.raises(ValueError, match=r"role roster"):
        reports.export(source, destination)
    assert not destination.exists()


def test_export_refuses_symlinked_destination_before_source_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(reports, "REPO", tmp_path)
    ordinary = tmp_path / "ordinary"
    ordinary.mkdir()
    alias = tmp_path / "alias"
    alias.symlink_to(ordinary, target_is_directory=True)
    with pytest.raises(ValueError, match=r"new private packet"):
        reports.export(tmp_path / "missing-source.xz", alias / "new-packet")
    assert not (ordinary / "new-packet").exists()


def test_retained_outside_horizon_packet_has_twenty_complete_source_reports(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tokens: list[str] = []
    parsed_counts: list[int] = []
    original = reports.parsed_pose

    def capture_pose(text: str, expected_n: int) -> tuple[str, list[tuple[str, str, str]]]:
        side, rows = original(text, expected_n)
        parsed_counts.append(expected_n)
        tokens.extend(token for row in rows for token in row)
        return side, rows

    monkeypatch.setattr(reports, "parsed_pose", capture_pose)
    claims = reports.check_packet()
    assert tuple(claims) == reports.COUNTS
    assert min(claims) > 324
    record = reports.read_json(reports.PACKET / "acquisition/sources.json")
    assert len(record["sources"][0]["custody"]["inputs"]) == 73
    assert sum(reports.COUNTS) == 7104
    assert tuple(parsed_counts) == reports.COUNTS
    assert len(tokens) == 21312
    assert all(format(float(token), ".17e") == token for token in tokens)
    claim = reports.fact(327, claims[327], [])["claim"]
    assert "observed binary64-compatible" in claim["precision"]["rounding"]
    assert "author computation precision unverified" in claim["precision"]["rounding"]
    coverage = load_yaml(check_source_coverage.COVERAGE.read_text())
    source = check_source_coverage.source_by_id(coverage, reports.SOURCE_ID)
    assert check_source_coverage.load_claims(reports.ROOT / source["claims_record"]) == claims
    own = [
        row
        for row in coverage["beyond_horizon_claims"]
        if row["source_id"] == reports.SOURCE_ID
    ]
    assert {row["n"]: row["value"] for row in own} == claims
    assert all(row["assurance"] == "reported" for row in own)
    # 2d32a6e's later reports at n = 375 and 378 supersede two of these dated rows,
    # which keep their ffd900d facts; the other eighteen are still current.
    superseded = {row["n"]: row["superseded_by"] for row in own if "superseded_by" in row}
    assert superseded == dict.fromkeys((375, 378), "couzo-extended-range-updates-2026-10-08")
    assert all(
        row["disposition"]
        == ("superseded" if row["n"] in superseded else "tracked-outside-case-corpus")
        for row in own
    )
    assert coverage["case_corpus"]["n_max"] == 324
