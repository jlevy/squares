"""Current transition relations preserve archival picture scope after source replacement."""

from __future__ import annotations

import ast
import copy
import inspect
import json
import math
from fractions import Fraction

import pytest

from sqpack import witness as witness_module
from sqpack.yamlio import safe_load
from workbench_tools import build_candidate as build
from workbench_tools import check_candidate as check


def shared_sources() -> tuple[dict, dict]:
    source = {
        "kind": "kingbird-derived-facts",
        "source_n": 296,
        "listed_n": [295, 296],
        "url": "https://kingbird.myphotos.cc/packing/square-296.svg",
    }
    return {"n": 295, "source": copy.deepcopy(source)}, {"n": 296, "source": source}


def test_archival_catalogue_relation_requires_both_current_sources() -> None:
    previous, following = shared_sources()
    assert build.recorded_shared_picture(previous, following)
    original = copy.deepcopy(following)
    previous["source"] = {
        "kind": "packet-derived-facts",
        "source_n": 295,
        "listed_n": [295],
        "url": "https://github.com/ry-xu/square_packing",
    }
    assert not build.recorded_shared_picture(previous, following)
    assert following == original


def test_current_shared_picture_still_refuses_changed_complete_poses() -> None:
    previous, following = shared_sources()
    with pytest.raises(ValueError, match="poses differ"):
        build.match_pair(
            {"n": 295, "keys": ["old"]},
            {"keys": ["changed", "new"]},
            [],
            [],
            following,
            manifest_entry_previous=previous,
        )


def test_actual_replaced_295_uses_general_complete_pose_matching() -> None:
    manifest = json.loads(build.MANIFEST.read_text())["atlas"]["entries"]
    entries = {row["n"]: row for row in manifest}
    following = copy.deepcopy(entries[296])
    assert 295 in following["source"]["listed_n"]
    assert not build.recorded_shared_picture(entries[295], entries[296])
    result = build.match_pair(
        build.load_witness(295),
        build.load_witness(296),
        build.load_rendering(295),
        build.load_rendering(296),
        entries[296],
        manifest_entry_previous=entries[295],
    )
    assert result["kind"] == "matched"
    assert len(result["map"]) == len(set(result["map"])) == 295
    assert entries[296] == following


def test_all_retained_experiment_callers_bind_the_current_matcher_signature() -> None:
    directory = build.REPO / "packing/atlas/known-best/video/spikes/v2-transitions"
    signature = inspect.signature(build.match_pair)
    calls = 0
    for name in ("experiment_angle_weight.py", "experiment_block_matching.py"):
        for node in ast.walk(ast.parse((directory / name).read_text())):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            if node.func.attr != "match_pair":
                continue
            arguments = [object()] * len(node.args)
            keywords = {item.arg: object() for item in node.keywords if item.arg is not None}
            assert len(keywords) == len(node.keywords)
            signature.bind(*arguments, **keywords)
            previous = next(
                item.value for item in node.keywords if item.arg == "manifest_entry_previous"
            )
            assert isinstance(previous, ast.Subscript)
            assert isinstance(previous.value, ast.Name)
            assert previous.value.id == "manifest"
            assert isinstance(previous.slice, ast.Name)
            assert previous.slice.id == "n"
            calls += 1
    assert calls == 5


@pytest.mark.parametrize("n", [51, 105, 52])
def test_independent_center_reader_preserves_every_exact_or_numerical_center(
    n: int,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = build.WITNESSES / f"n-{n:03d}.yaml"
    original = path.read_bytes()
    data = safe_load(original.decode())["witness"]

    def forbidden(*_args: object, **_kwargs: object) -> None:
        pytest.fail("presentation reader called a geometric predicate")

    for name in ("verify_packing", "exact_verify", "numerical_check"):
        monkeypatch.setattr(witness_module, name, forbidden)

    def scalar(value: str | list[str]) -> float:
        if isinstance(value, list):
            a, b = value
            return float(Fraction(a)) + float(Fraction(b)) * math.sqrt(2)
        return float(Fraction(value))

    expected = [tuple(scalar(value) for value in row["center"]) for row in data["squares"]]
    actual = check.witness_centres(n)
    assert len(actual) == len(expected) == n
    for result, source in zip(actual, expected, strict=True):
        assert result == pytest.approx(source, rel=0, abs=1e-14)
    assert path.read_bytes() == original
