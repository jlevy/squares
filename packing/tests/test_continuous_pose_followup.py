"""The continuous-pose follow-up tool's exact parts, on small synthetic inputs."""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import continuous_pose_followup as followup
from devtools.audit_continuous_pose import ENDPOINTS, Claim, pose_input
from devtools.audit_wand125_declared_net import AuditError

#: The n = 28 certificate's stated parameters, which the tool must reproduce exactly.
B28 = Fraction(499, 500)
L28 = Fraction(573351, 100000)


def candidate(
    rows: list[tuple[list[str], str]], *, side: str = "3", total: str | None = None, n: int = 2
) -> bytes:
    masses = sum((Fraction(m) for _, m in rows), Fraction(0))
    value = {
        "n": n,
        "L": side,
        "B": "0.99",
        "proof_net": {"step": "1/100", "last": 10},
        "total_mass": total if total is not None else str(masses),
        "points": [],
        "rectangles": [{"rectangle": r, "mass": m} for r, m in rows],
    }
    return json.dumps(value).encode()


TWO = candidate([(["0", "0", "1", "1"], "1/2"), (["1/2", "1", "3/2", "2"], "3/4")])


def stated(n: int = 28) -> followup.Stated:
    return followup.Stated("continuous_n28_L5745", n, B28, Fraction(1), L28 / B28)


# --------------------------------------------------------------------------- premises


def test_crate_near_axis_side_and_margin_are_the_sources() -> None:
    """``sqverify_continuous``'s default ``A`` and its margin, as its summary prints them."""
    side = followup.crate_axis_side(B28, followup.CRATE_EPS)
    assert side == Fraction(4989999, 5000000)
    margin = B28 - side * followup.extent(followup.CRATE_EPS)
    assert margin == Fraction(200029979999, 500000000000005000000)


def test_check2_near_axis_side_and_margin_are_the_sources() -> None:
    """check2's ``A`` (the largest even grid side below ``B / W(eps)``) and its margin."""
    eps = Fraction(1, 10**6)
    side = followup.check2_axis_side(B28, eps)
    assert side == Fraction(249499501, 250000000)
    assert int(side * followup.GRID) % 2 == 0
    assert B28 - side * followup.extent(eps) == Fraction(1496999501, 250000000000250000000)


def test_crate_cuts_give_86_roots_ending_at_t() -> None:
    cuts = followup.crate_cuts(followup.CRATE_EPS, followup.CRATE_LAST_T)
    assert len(cuts) + 1 == 86
    assert cuts[0] == Fraction(1, 10**5)
    assert cuts[-1] == Fraction(41, 100)
    assert all(a < b for a, b in itertools.pairwise(cuts))


def test_scalar_chain_of_the_claim() -> None:
    density = followup.read_candidate(
        candidate([(["0", "0", "1", "1"], "2799999/100000")], side="5.73351", n=28), 28
    )
    chain = followup.scalar_chain(density, stated())
    assert chain["X"] == Fraction(1149, 200)
    assert chain["counting_margin"] == Fraction(1, 100000)
    assert chain["geometry_margin"] == Fraction(308811289201, 10000000000)
    assert chain["angle_coverage_polynomial"] == Fraction(89, 40000)


# --------------------------------------------------------------------------- the candidate


def test_read_candidate_expands_through_d4() -> None:
    density = followup.read_candidate(TWO, 2)
    assert density.side == 3
    assert len(density.rows) == 2
    assert density.terms == 16
    assert followup.mass(density) == Fraction(5, 4)
    assert density.sha256 == hashlib.sha256(TWO).hexdigest()
    # Each row has four distinct images: the corner square lies on the diagonal, and the
    # other is symmetric about y = 3/2.
    assert len(density.merged) == 8


def test_read_candidate_skips_zero_rows() -> None:
    raw = candidate([(["0", "0", "1", "1"], "1"), (["5", "5", "9", "9"], "0")])
    density = followup.read_candidate(raw, 2)
    assert density.listed == 2
    assert len(density.rows) == 1


@pytest.mark.parametrize(
    ("raw", "message"),
    [
        (candidate([(["0", "0", "1", "1"], "1")], total="2"), "total_mass"),
        (candidate([(["0", "0", "1", "1"], "-1")]), "negative"),
        (candidate([(["0", "0", "4", "1"], "1")]), "outside"),
        (candidate([(["1", "0", "1", "1"], "1")]), "degenerate"),
        (candidate([(["0", "0", "1", "1"], "1")], n=3), "n = 3"),
    ],
)
def test_read_candidate_refuses(raw: bytes, message: str) -> None:
    with pytest.raises(AuditError, match=message):
        followup.read_candidate(raw, 2)


def test_read_candidate_refuses_points() -> None:
    value = json.loads(TWO)
    value["points"] = [{"point": ["1", "1"], "mass": "1"}]
    with pytest.raises(AuditError, match="point masses"):
        followup.read_candidate(json.dumps(value).encode(), 2)


def test_mutant_is_exactly_scaled_and_recognized() -> None:
    factor = Fraction(985, 1000)
    original = followup.read_candidate(TWO, 2)
    scaled = followup.read_candidate(followup.mutant_bytes(TWO, factor), 2)
    assert followup.scaled_rows(original, scaled, factor)
    assert followup.mass(scaled) == followup.mass(original) * factor
    assert not followup.scaled_rows(original, scaled, Fraction(99, 100))
    value = json.loads(followup.mutant_bytes(TWO, factor))
    value["rectangles"][0]["mass"] = "1/2"
    value["total_mass"] = str(sum(Fraction(r["mass"]) for r in value["rectangles"]))
    uneven = followup.read_candidate(json.dumps(value).encode(), 2)
    assert not followup.scaled_rows(original, uneven, factor)


# --------------------------------------------------------------------------- kernel inputs


def test_pose_bytes_are_the_release_builder_with_b_in_decimal() -> None:
    density = followup.read_candidate(TWO, 2)
    data = followup.pose_bytes(density, Fraction(1, 2))
    expected = pose_input(density, Claim(n=2, L=Fraction(3), B=Fraction(1, 2)))
    assert data == expected
    lines = data.decode().splitlines()
    assert lines[1] == "0.5 0.5"
    assert int(lines[2]) == density.terms == len(lines) - 3


def test_axis_rows_round_inward_and_down() -> None:
    raw = candidate([(["1/3", "0", "1", "1"], "1")])
    density = followup.read_candidate(raw, 2)
    rows = followup.axis_rows_at(density, 1000)
    assert len(rows) == 8
    first = rows[0]
    assert first[0] == 333333334  # ceil(10^9 / 3): the support is rounded inward
    assert first[2] == 10**9
    # density 1 / (8 * 2/3) = 3/16, rounded down at scale 1000
    assert first[4] == 187


def test_axis_scale_drops_until_the_guards_hold() -> None:
    heavy = candidate([(["0", "0", "1/1000000", "1/1000000"], "100")])
    density = followup.read_candidate(heavy, 2)
    side = Fraction(1, 2)
    scale = followup.axis_scale(density, side)
    assert scale < followup.GRID
    length = int(density.side * followup.GRID)
    held = followup.axis_guards(
        followup.axis_rows_at(density, scale), length, int(side * followup.GRID)
    )
    assert held[2]
    over = followup.axis_guards(
        followup.axis_rows_at(density, scale * 10), length, int(side * followup.GRID)
    )
    assert not over[2]


def test_axis_bytes_header() -> None:
    density = followup.read_candidate(TWO, 2)
    data = followup.axis_bytes(density, Fraction(1, 2), Fraction(1), 10**8)
    head = data.decode().splitlines()[0].split()
    assert head == ["3000000000", "500000000", "1000000000", "100000000", "1", "1", "16"]


# --------------------------------------------------------------------------- source digests


def test_crate_source_digest_follows_build_rs() -> None:
    files = {
        "Cargo.toml": b"a",
        "Cargo.lock": b"b",
        "build.rs": b"c",
        "src/z.rs": b"z",
        "src/a.rs": b"y",
        "src/notes.md": b"ignored",
        "src/deep/x.rs": b"ignored",
        "README.md": b"ignored",
    }
    digest = hashlib.sha256()
    for name in ("Cargo.toml", "Cargo.lock", "build.rs", "src/a.rs", "src/z.rs"):
        digest.update(name.encode() + b"\0" + files[name] + b"\0")
    assert followup.crate_source_digest(files) == digest.hexdigest()


def test_check2_source_digest_follows_version_rule(tmp_path: Path) -> None:
    (tmp_path / "kernel").mkdir()
    (tmp_path / "b.py").write_bytes(b"b")
    (tmp_path / "kernel/a.cpp").write_bytes(b"a")
    listed = {
        "kernel/a.cpp": hashlib.sha256(b"a").hexdigest(),
        "b.py": hashlib.sha256(b"b").hexdigest(),
    }
    digest, held = followup.check2_source_digest(tmp_path, listed)
    lines = f"{listed['b.py']}  b.py\n{listed['kernel/a.cpp']}  kernel/a.cpp\n"
    assert digest == hashlib.sha256(lines.encode()).hexdigest()
    assert held
    (tmp_path / "b.py").write_bytes(b"changed")
    assert not followup.check2_source_digest(tmp_path, listed)[1]


# --------------------------------------------------------------------------- the logs


def crate_log(density: followup.Density, *, verdict: str = "verified") -> list[dict[str, Any]]:
    """A ``sqverify_continuous`` log consistent with ``density`` at the n = 28 parameters."""
    s = stated()
    side = followup.crate_axis_side(s.core, followup.CRATE_EPS)
    ends = [
        followup.CRATE_EPS,
        *followup.crate_cuts(followup.CRATE_EPS, followup.CRATE_LAST_T),
        followup.CRATE_LAST_T,
    ]
    premises = {
        "A": followup.text(side),
        "B": followup.text(s.core),
        "L": followup.text(density.side),
        "T": followup.text(followup.CRATE_LAST_T),
        "X": followup.text(density.side / s.core),
        "axis_containment_margin": followup.text(
            s.core - side * followup.extent(followup.CRATE_EPS)
        ),
        "counting_margin": followup.text(s.n * s.tau - followup.mass(density)),
        "eps": followup.text(followup.CRATE_EPS),
        "input_sha256": density.sha256,
        "mass": followup.text(followup.mass(density)),
        "n": s.n,
        "threshold": "1",
    }
    roots = [
        {
            "kind": "root",
            "index": k,
            "t": [followup.text(a), followup.text(b)],
            "verdict": verdict,
            "nodes": 3,
            "leaves": 2,
            "min_certified_lower_bound": "1.0000001",
            "seconds": "1.5",
        }
        for k, (a, b) in enumerate(itertools.pairwise(ends))
    ]
    summary = {
        "kind": "sqverify-fast-continuous-summary/v1",
        "status": "VERIFIED" if verdict == "verified" else "REFUSED",
        "claim": f"s(28) > {followup.text(s.claim)}" if verdict == "verified" else "",
        "roots": len(roots),
        "refused_roots": [] if verdict == "verified" else list(range(len(roots))),
        "nodes": 3 * len(roots),
        "leaves": 2 * len(roots),
    }
    axis = {
        "kind": "axis-patch",
        "verified": verdict == "verified",
        "min_certified_lower_bound": "1.001",
    }
    return [{"kind": "premises", "premises": premises}, axis, *roots, summary]


N28 = candidate([(["0", "0", "1", "1"], "2799999/100000")], side="5.73351", n=28)


def held(checks: list[followup.Check]) -> dict[str, bool]:
    return {c.name: c.held for c in checks}


def test_crate_log_checks_hold_on_a_consistent_log() -> None:
    density = followup.read_candidate(N28, 28)
    assert all(
        held(
            followup.crate_log_checks(crate_log(density), density, stated(), control=False)
        ).values()
    )
    control = followup.crate_log_checks(
        crate_log(density, verdict="refused"), density, stated(), control=True
    )
    assert all(held(control).values())


def test_crate_log_checks_catch_a_missing_root_and_a_low_bound() -> None:
    density = followup.read_candidate(N28, 28)
    log = crate_log(density)
    del log[5]
    assert not held(followup.crate_log_checks(log, density, stated(), control=False))[
        "roots are the default cuts of [eps, T]"
    ]
    log = crate_log(density)
    log[4]["min_certified_lower_bound"] = "0.9999999999"
    assert not held(followup.crate_log_checks(log, density, stated(), control=False))[
        "every root's least bound at least tau"
    ]
    log = crate_log(density)
    log[0]["premises"]["A"] = "1/2"
    assert not held(followup.crate_log_checks(log, density, stated(), control=False))[
        "premises as recomputed here"
    ]


def check2_receipt(*, budget: str = "4000000000") -> tuple[dict[str, Any], dict[str, Any]]:
    files = {"certificate_input.txt": "p" * 64, "axis_input.txt": "a" * 64}
    manifest = {"files": files, "axis_scale": "100"}
    slabs = [
        {
            "index": i,
            "arguments": [str(lo), str(hi), "1000000", "1", "1", budget],
            "accepted": True,
            "input_sha256": files["certificate_input.txt"],
            "seconds": 2.0,
            "kernel": {
                "status": "verified",
                "input_sha256": files["certificate_input.txt"],
                "nodes": 5,
                "leaves": 3,
                "lower_bound": 1.0000001,
            },
        }
        for i, (lo, hi) in enumerate(itertools.pairwise(ENDPOINTS))
    ]
    receipt = {
        "status": "VERIFIED",
        "claim": f"s(28) > {followup.text(L28 / B28)}",
        "manifest": manifest,
        "endpoints": list(ENDPOINTS),
        "slabs": slabs,
        "summary": {"nodes": 5 * len(slabs)},
        "build": {"configuration": {"sources": {"k.cpp": "k"}}},
        "axis": {
            "input_sha256": files["axis_input.txt"],
            "kernel": {
                "status": "AXIS_COVERAGE_PROVED",
                "input_sha256": files["axis_input.txt"],
                "minimum_numerator": "101",
                "scale": "100",
                "direct_sum_matches": True,
            },
        },
    }
    return receipt, manifest


def test_check2_receipt_checks_hold_and_catch_defects() -> None:
    receipt, manifest = check2_receipt()
    kernels = {"k.cpp": "k"}
    assert all(
        held(
            followup.check2_receipt_checks(receipt, manifest, stated(), kernels, control=False)
        ).values()
    )
    receipt["slabs"][3]["kernel"]["nodes"] = 6
    result = held(
        followup.check2_receipt_checks(receipt, manifest, stated(), kernels, control=False)
    )
    assert not result["every slab a full binary cover (nodes = 2 leaves - 1)"]
    receipt, manifest = check2_receipt()
    receipt["slabs"][7]["arguments"][1] = "1"
    result = held(
        followup.check2_receipt_checks(receipt, manifest, stated(), kernels, control=False)
    )
    assert not result["every slab run with its arguments"]
    receipt, manifest = check2_receipt()
    receipt["axis"]["kernel"]["minimum_numerator"] = "99"
    result = held(
        followup.check2_receipt_checks(receipt, manifest, stated(), kernels, control=False)
    )
    assert not result["axis proved at least tau"]
    receipt, manifest = check2_receipt()
    result = held(
        followup.check2_receipt_checks(
            receipt, manifest, stated(), {"k.cpp": "x"}, control=False
        )
    )
    assert not result["build sources are the pinned kernels"]


def test_restore_pinned_lays_identical_copies(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(followup, "REPO", tmp_path)
    (tmp_path / "copy").mkdir()
    (tmp_path / "copy/LICENSE").write_bytes(b"MIT")
    prefix = "problems/square-lower-bounds/certificates/c/"
    record = tmp_path / "sources.json"
    pins = [
        {
            "path": prefix + "kernel/LICENSE",
            "sha256": hashlib.sha256(b"MIT").hexdigest(),
            "identical_to": "copy/LICENSE",
        },
        {
            "path": "problems/square-lower-bounds/LICENSE",
            "sha256": "0" * 64,
            "identical_to": "copy/LICENSE",
        },
    ]
    record.write_text(json.dumps({"sources": [{"pinned_only": pins}]}))
    directory = tmp_path / "dir"
    directory.mkdir()
    restored = followup.restore_pinned(record, directory, "c")
    assert restored == [{"path": prefix + "kernel/LICENSE", "from": "copy/LICENSE"}]
    assert (directory / "kernel/LICENSE").read_bytes() == b"MIT"
    pins[0]["sha256"] = "1" * 64
    record.write_text(json.dumps({"sources": [{"pinned_only": pins}]}))
    (directory / "kernel/LICENSE").unlink()
    with pytest.raises(AuditError, match="differs"):
        followup.restore_pinned(record, directory, "c")


def test_price_takes_the_larger_ratio() -> None:
    runs = {
        "check1_roots": [
            {"thread_seconds": "2", "process_cpu_seconds": 3.0, "source_seconds": "1"}
        ],
        "pose_slabs": [
            {"kernel_seconds": "4", "process_cpu_seconds": 4.0, "source_seconds": "2"}
        ],
    }
    log = [{"kind": "root", "seconds": "3600"}, {"kind": "root", "seconds": "3600"}]
    receipt = {"slabs": [{"seconds": "1800"}, {"seconds": "1800"}]}
    out = followup.price(runs, log, receipt)
    assert out["check1_ratio_by_own_timing"] == 2
    assert out["check1_ratio_by_process_cpu"] == 3
    assert out["check1_replay_cpu_hours"] == 6
    assert out["check2_replay_cpu_hours"] == 2


def test_same_reads_two_decimal_texts_of_one_double() -> None:
    assert followup.same("1.0000000000972009", "1.000000000097201")
    assert not followup.same("1.0000000000972009", "1.0000000000972011")
    assert followup.same(3, 3)
    assert not followup.same("verified", "unresolved")


@pytest.mark.parametrize(
    ("row", "patch", "outcome"),
    [
        ({"verdict": "verified"}, {"verified": False}, "REFUSED_AT_AXIS"),
        ({"verdict": "refused"}, {"verified": True}, "REFUSED_AT_ROOT"),
        ({"verdict": "verified"}, {"verified": True}, "VERIFIED_AT_ROOT"),
    ],
)
def test_mutant_outcome(row: dict[str, Any], patch: dict[str, Any], outcome: str) -> None:
    assert followup.mutant_outcome(row, patch) == outcome
