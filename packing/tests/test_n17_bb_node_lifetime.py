"""The standing BB replay releases full records only after their last scheduled use."""

from __future__ import annotations

import copy
import time
import weakref
from pathlib import Path
from typing import Any, override

import pytest

from devtools import verify_n17_bb_certificate as bb


class FullRecord(dict[str, Any]):
    """Weak-referenceable decoded node, so tests observe retention rather than a cache."""


def record(ident: int, parent: int | None, *, closed: bool = False) -> dict[str, Any]:
    return {
        "id": ident,
        "parent": parent,
        "angles": [["0/1", "1/1"]],
        "windows": [],
        "closed": "cell" if closed else None,
        "split": None if closed else {"angle": [0, "1/2"]},
        "final": None if closed else [["0/1", "1/1", "0/1", "1/1"]],
        "rounds": [],
    }


class Replay(bb.Verifier):
    """Record parent data at the numerical-check boundary without producing a proof."""

    def __init__(self, chunks: list[list[dict[str, Any]]], bad: set[int]) -> None:
        self.directory = Path("unused")
        self.manifest = {"chunks": [str(i) for i in range(len(chunks))]}
        self.failures = []
        self.counts = {}
        self.calls: list[tuple[int, int | None]] = []
        self.bad = bad

    @override
    def check_node(self, node: bb.Node, parent: bb.Node | None) -> None:
        ident = node["id"]
        assert parent is None or parent["id"] == node["parent"]
        if parent is not None:
            assert parent["final_q"] == [(bb.Q(0), bb.Q(1), bb.Q(0), bb.Q(1))]
        self.calls.append((ident, None if parent is None else parent["id"]))
        self.tick("attempted")
        if ident in self.bad:
            raise bb.CertificateError(f"node {ident}: injected refusal")


def replay(
    monkeypatch: pytest.MonkeyPatch,
    chunks: list[list[dict[str, Any]]],
    *,
    chosen: set[int] | None = None,
    bad: set[int] | None = None,
    structure: bool = False,
) -> tuple[Replay, tuple[int, int], list[set[int]]]:
    verifier = Replay(chunks, bad or set())
    flat = [node for chunk in chunks for node in chunk]
    children: dict[int | None, list[int]] = {}
    for node in flat:
        children.setdefault(node["parent"], []).append(node["id"])
    tree = bb.Tree(
        {node["id"]: node for node in flat},
        {node["id"]: c for c, chunk in enumerate(chunks) for node in chunk},
        children,
        {},
        0,
        {},
    )
    if structure:
        bb.check_tree(verifier, tree)
    references: dict[int, weakref.ReferenceType[FullRecord]] = {}
    boundaries: list[set[int]] = []

    def read(_directory: Path, name: str) -> dict[str, Any]:
        boundaries.append({i for i, ref in references.items() if ref() is not None})
        decoded = [FullRecord(copy.deepcopy(node)) for node in chunks[int(name)]]
        for node in decoded:
            references[node["id"]] = weakref.ref(node)
        return {"nodes": decoded}

    monkeypatch.setattr(bb, "read_named", read)
    result = bb.check_nodes(
        verifier,
        tree,
        set(tree.index) if chosen is None else chosen,
        progress=False,
        clock=time.perf_counter(),
    )
    boundaries.append({i for i, ref in references.items() if ref() is not None})
    return verifier, result, boundaries


def test_reverse_ids_preserve_a_parents_pending_check(monkeypatch: pytest.MonkeyPatch) -> None:
    verifier, result, boundaries = replay(
        monkeypatch,
        [
            [record(9, None), record(1, 9, closed=True), record(2, 9, closed=True)],
            [record(10, None, closed=True)],
        ],
    )
    assert result == (4, 0)
    assert verifier.calls == [(1, 9), (2, 9), (9, None), (10, None)]
    assert verifier.failures == []
    assert 9 not in boundaries[1]
    assert boundaries[-1] == set()


def test_cross_chunk_children_keep_the_parent_until_both_attempts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    verifier, result, boundaries = replay(
        monkeypatch,
        [
            [record(0, None)],
            [record(1, 0, closed=True)],
            [record(2, 0, closed=True)],
            [record(3, None, closed=True)],
        ],
    )
    assert result == (4, 0)
    assert verifier.calls == [(0, None), (1, 0), (2, 0), (3, None)]
    assert 0 in boundaries[1]
    assert 0 in boundaries[2]
    assert 0 not in boundaries[3]


def test_sample_counts_only_selected_children(monkeypatch: pytest.MonkeyPatch) -> None:
    verifier, result, boundaries = replay(
        monkeypatch,
        [
            [record(0, None)],
            [record(1, 0, closed=True)],
            [record(2, 0, closed=True)],
            [record(3, None, closed=True)],
        ],
        chosen={0, 1, 3},
    )
    assert result == (3, 0)
    assert verifier.calls == [(0, None), (1, 0), (3, None)]
    assert 0 not in boundaries[2]


def test_failed_internal_node_still_supplies_its_descendants(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    verifier, result, boundaries = replay(
        monkeypatch,
        [
            [record(0, None)],
            [record(1, 0), record(2, 0, closed=True)],
            [record(3, 1, closed=True)],
            [record(4, 1, closed=True)],
            [record(5, None, closed=True)],
        ],
        bad={1, 4},
    )
    assert result == (6, 2)
    assert verifier.calls == [(0, None), (1, 0), (2, 0), (3, 1), (4, 1), (5, None)]
    assert verifier.failures == ["node 1: injected refusal", "node 4: injected refusal"]
    assert verifier.counts == {"attempted": 6}
    assert 0 not in boundaries[2]
    assert 1 in boundaries[2]
    assert 1 in boundaries[3]
    assert 1 not in boundaries[4]


def test_missing_parent_stays_a_refusal_and_releases_a_finished_child(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    verifier, result, boundaries = replay(
        monkeypatch,
        [[record(0, 8)], [record(1, 0, closed=True)], [record(2, None, closed=True)]],
    )
    assert result == (2, 0)
    assert verifier.calls == [(1, 0), (2, None)]
    assert verifier.failures == ["node 0: parent 8 not loaded"]
    assert 0 in boundaries[1]
    assert 0 not in boundaries[2]


def test_a_closed_parent_cannot_supply_malformed_children_in_later_chunks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    verifier, result, boundaries = replay(
        monkeypatch,
        [
            [record(0, None, closed=True)],
            [record(1, 0, closed=True)],
            [record(2, 0, closed=True)],
        ],
        structure=True,
    )
    assert result == (1, 0)
    assert verifier.calls == [(0, None)]
    assert verifier.failures == [
        "T3: closed node 0 has children",
        "T3: 2 nodes unreachable from the root",
        "node 1: parent 0 not loaded",
        "node 2: parent 0 not loaded",
    ]
    assert 0 not in boundaries[1]


def test_completed_internal_records_do_not_accumulate_on_a_long_branch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    chunks = [[record(0, None)]]
    for level in range(1, 33):
        parent = 2 * (level - 1)
        chunks.append(
            [
                record(2 * level - 1, parent, closed=True),
                record(2 * level, parent, closed=level == 32),
            ]
        )
    verifier, result, boundaries = replay(monkeypatch, chunks)
    assert result == (65, 0)
    assert verifier.counts == {"attempted": 65}
    # The prior loop retains all 32 open records. This observes actual decoded
    # records, including transient local references, rather than a cache-size counter.
    assert max(map(len, boundaries)) == 1
    assert boundaries[-1] == set()
