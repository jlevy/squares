"""Controls for the 1 October and the split imports in `devtools.audit_evand_mixed_covers`.

Three covers joined the two of the September 28 packet: Daniel's ``s(60) = 8`` from the
October 1 evand packet, and Hosono's ``s(59) = 8`` and ``s(77) = 9`` from Hosono's
October 1 packet. Daniel's ``s(32)`` sweep without the D4 fold came with the first. These
tests hold the fast part. Each new cover is well formed, weighs exactly what its source
states and less than the count it excludes, and is invariant under the square's
symmetries; a cover changed in one mass orbit or one position is refused. A ``zmx2`` log
must cover the region its side and mode derive, under either header version, and every
way of falling short is refused, on toy logs and on the source's own; region runs made
apart are one record only when their union is the region, each root once, under the same
header apart from ``region``. The source's logs compare root for root, joined replays
and ``.xz`` included, and its run manifests state the logs it ships. ``s(59)``'s two
``zm_mixed.py`` runs are undecided from their manifests, and per-root records decide
them only when a deeper run certifies every uncertified root.

Benjamin Greff's ``s(76)`` and ``s(95)`` covers are split: ``zmx2`` leaves a few D4 roots
and ``zm_mixed.py`` certifies their sub-roots. Both covers audit clean, the source's
records and this repository's replay are each one clean decision over the D4 region and
equal root for root, and a composite is refused when a sub-root is missing, uncertified,
run on another cover, at other settings or outside its region, or when the ``zmx2`` log
falls short of its region or leaves a root no sub-root covers.

`tests/test_evand_mixed_covers.py` holds the controls for ``s(21)`` and ``s(45)``.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from collections import Counter
from collections.abc import Callable, Mapping
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools.audit_evand_mixed_covers import (
    IMPORTED_CASES,
    POINT_COVERS,
    POINT_ONLY_CASES,
    REPO,
    SPLIT_CASES,
    ZM_MIXED_SETTINGS,
    Case,
    MixedCover,
    audit_cover,
    audit_split_composite,
    audit_zm_mixed,
    audit_zm_mixed_composite,
    audit_zm_mixed_manifests,
    audit_zmx2,
    audit_zmx2_manifest,
    check_imported_case,
    check_split_case,
    compare_sub_roots,
    cover_clean,
    main,
    parse_cover,
    read_record_bytes,
    sub_root_comparison_clean,
    zm_mixed_clean,
    zmx2_clean,
    zmx2_roots,
)

#: Total, points, segments, loaded lines 1..k and segment lengths. s(77)'s lengths are
#: s(60)'s 1/50, the band's 1/8, and the 2/1000 that replaced 84 points on loaded lines.
STATED = {
    59: ("1474762899/25000000", 26308, 5240, 7, {"1/50": 5240}),
    60: ("748233441/12500000", 23744, 5216, 7, {"1/50": 5216}),
    77: (
        "43347137744028965/562949953421312",
        28273,
        6420,
        8,
        {"1/500": 100, "1/50": 5952, "1/8": 368},
    ),
}
S32_SYM = POINT_COVERS[32].full_log


def _run(capsys: pytest.CaptureFixture[str], *argv: str) -> tuple[int, dict[str, Any]]:
    code = main(list(argv))
    return code, json.loads(capsys.readouterr().out)


# --- the covers --------------------------------------------------------------------------


@pytest.mark.parametrize("n", sorted(STATED))
def test_imported_cover_is_well_formed_light_and_symmetric(n: int) -> None:
    total, points, segments, lines, lengths = STATED[n]
    result = audit_cover(IMPORTED_CASES[n])
    assert cover_clean(result), result
    assert (result["total"], result["points"], result["segments"]) == (total, points, segments)
    assert Fraction(total) < n
    assert result["d4_invariant_entry_by_entry"]
    assert result["d4_invariant_as_measure"]
    assert result["points_on_segment_lines"] == 0
    interior = [str(c) for c in range(1, lines + 1)]
    assert result["lines_carrying_segments"] == {"x": interior, "y": interior}
    assert result["segment_lengths"] == lengths


def test_s77s_short_segments_are_its_84_replaced_points() -> None:
    # 68 points on one loaded line became one segment each, and 16 at a crossing of two
    # became two of half the mass: 84 points, 100 segments, centred where they were.
    cover = _cover(77)
    short = [s for s in cover.segments if abs(s[2] - s[0]) + abs(s[3] - s[1]) == 2]
    masses: dict[tuple[int, int], list[int]] = {}
    for a, b, c, d, w in short:
        masses.setdefault(((a + c) // 2, (b + d) // 2), []).append(w)
    assert len(short) == 100
    assert Counter(len(m) for m in masses.values()) == Counter({1: 68, 2: 16})
    on_lines = [(x, y) for x, y in masses if x % 1000 == 0 or y % 1000 == 0]
    assert len(on_lines) == 84
    assert all(m[0] == m[1] for m in masses.values() if len(m) == 2)


def test_the_cover_command_takes_the_new_cases(capsys: pytest.CaptureFixture[str]) -> None:
    code, result = _run(capsys, "cover", "--case", "77")
    assert code == 0, result
    assert result["mass_denominator"] == 2**49


def _write_cover(path: Path, cover: MixedCover) -> Path:
    rows = [
        "mixed 1",
        f"{cover.side.numerator} {cover.side.denominator}",
        str(cover.denominator),
        str(cover.mass_denominator),
        str(len(cover.points)),
        *(f"{x} {y} {w}" for x, y, w in cover.points),
        str(len(cover.segments)),
        *(" ".join(map(str, segment)) for segment in cover.segments),
        str(cover.polygons),
    ]
    path.write_text("\n".join(rows) + "\n", encoding="ascii")
    return path


def test_the_plain_point_cover_of_s61_audits_clean() -> None:
    result = audit_cover(POINT_ONLY_CASES[61])
    assert cover_clean(result), result
    assert result["segments"] == 0
    assert result["total"] == "8584985072679551/140737488355328"


def test_a_plain_cover_that_is_not_d4_invariant_is_refused(tmp_path: Path) -> None:
    plain = "8 1\n2000\n562949953421312\n2\n1000 2000 5\n3000 2000 5\n"
    path = tmp_path / "cover.txt"
    path.write_text(plain, encoding="ascii")
    result = audit_cover(POINT_ONLY_CASES[61], path)
    assert not cover_clean(result)
    assert not result["d4_invariant_entry_by_entry"]
    assert not result["counts_as_stated"]


def _cover(n: int) -> MixedCover:
    return parse_cover(read_record_bytes(IMPORTED_CASES[n].cover_path).decode("ascii"))


def _heavier_orbit(cover: MixedCover) -> MixedCover:
    """One unit more on every point of the first point's D4 orbit: still symmetric."""
    edge = int(cover.side * cover.denominator)
    x, y, _ = cover.points[0]
    orbit = {(a, b) for p, q in ((x, y), (y, x)) for a in (p, edge - p) for b in (q, edge - q)}
    points = tuple((x, y, w + 1 if (x, y) in orbit else w) for x, y, w in cover.points)
    return replace(cover, points=points)


def _moved_point(cover: MixedCover) -> MixedCover:
    """A point of positive mass moved 1/D along x: the same mass, the symmetry gone."""
    index = next(i for i, (_, _, w) in enumerate(cover.points) if w > 0)
    x, y, w = cover.points[index]
    points = (*cover.points[:index], (x + 1, y, w), *cover.points[index + 1 :])
    return replace(cover, points=points)


def _moved_short_segment(cover: MixedCover) -> MixedCover:
    """One of the 2/1000 segments that replaced line points slid 1/D along its line."""
    index = next(
        i for i, (a, b, c, d, _) in enumerate(cover.segments) if abs(c - a) + abs(d - b) == 2
    )
    a, b, c, d, w = cover.segments[index]
    shift = (0, 1) if a == c else (1, 0)
    moved = (a + shift[0], b + shift[1], c + shift[0], d + shift[1], w)
    segments = (*cover.segments[:index], moved, *cover.segments[index + 1 :])
    return replace(cover, segments=segments)


CONTROLS: list[tuple[int, Callable[[MixedCover], MixedCover], str]] = [
    *((n, _heavier_orbit, "total") for n in sorted(STATED)),
    *((n, _moved_point, "d4") for n in sorted(STATED)),
    (77, _moved_short_segment, "d4"),
]


@pytest.mark.parametrize(
    ("n", "mutate", "broken"), CONTROLS, ids=lambda v: getattr(v, "__name__", str(v))
)
def test_a_mutated_cover_is_refused(
    tmp_path: Path, n: int, mutate: Callable[[MixedCover], MixedCover], broken: str
) -> None:
    case = IMPORTED_CASES[n]
    result = audit_cover(case, _write_cover(tmp_path / "cover.txt", mutate(_cover(n))))
    assert not cover_clean(result)
    if broken == "total":
        assert not result["total_equals_stated"]
        assert Fraction(result["total"]) > case.total
        assert result["d4_invariant_entry_by_entry"]
        assert result["d4_invariant_as_measure"]
    else:
        assert result["total_equals_stated"]
        assert not result["d4_invariant_entry_by_entry"]
        assert not result["d4_invariant_as_measure"]


# --- zmx2 logs ---------------------------------------------------------------------------

#: A toy cover of side 2: 400 roots under d4, 3,200 under full.
TOY = Case(3, 2, "toy", "toy.txt", Fraction(5, 2), 0, 0)
V6B7F = "hash=0123456789abcdef mode={mode} atoms={atoms} depth=40 node_cap=20000000 kappa=1.5"


def _zmx2_lines(side: int, mode: str, atoms: str = "grid") -> list[str]:
    """A clean log as ``zmx2 cert`` writes it, numbered as ``zmx2.rs`` numbers roots."""
    cells = 10 * side if mode == "full" else 5 * side
    header = (
        f"# zmx2 cert {V6B7F.format(mode=mode, atoms=atoms)} K=30 "
        f"region=x0-{cells - 1},y0-{cells - 1},bins0-3"
    )
    lines = [header]
    for p in (0, 1) if mode == "full" else (0,):
        for i in range(cells):
            for j in range(cells):
                for k in range(4):
                    root_id = ((p * cells + i) * cells + j) * 4 + k
                    lines.append(
                        f"ROOT {root_id} pass {p} root {i}/10,{i + 1}/10,{j}/10,{j + 1}/10,"
                        f"{k}/8,{k + 1}/8 boxes 3 cert 2 empty 0 uncert 0 maxdepth 1 "
                        f"capped 0 ms 4"
                    )
    return lines


def _write(path: Path, lines: list[str]) -> Path:
    path.write_text("\n".join(lines) + "\n", encoding="ascii")
    return path


@pytest.mark.parametrize(
    ("side", "mode", "roots"),
    [
        (8, "d4", 6400),
        (8, "full", 51200),
        (9, "d4", 8100),
        (9, "full", 64800),
        (6, "full", 28800),
    ],
)
def test_the_region_follows_from_side_and_mode(side: int, mode: str, roots: int) -> None:
    assert len(zmx2_roots(side, mode)) == roots


def test_root_ids_are_the_ones_zmx2_writes() -> None:
    # A line of the source's s(32) --full --sym-atoms log.
    assert zmx2_roots(6, "full")[(1, "54/10,55/10,44/10,45/10,0/8,1/8")] == 27536


@pytest.mark.parametrize("mode", ["d4", "full"])
@pytest.mark.parametrize("atoms", ["grid", "pairpts", "pairpts+sym"])
def test_either_header_version_audits_clean(tmp_path: Path, mode: str, atoms: str) -> None:
    lines = _zmx2_lines(2, mode, atoms)
    result = audit_zmx2(TOY, _write(tmp_path / "roots.log", lines), mode)
    assert zmx2_clean(result), result
    assert result["roots_present"] == (400 if mode == "d4" else 3200)
    assert result["flags"]["pair_points"] == atoms.startswith("pairpts")
    assert result["flags"]["sym_atoms"] == atoms.endswith("+sym")


def _replace_in_root(old: str, new: str) -> Callable[[list[str]], list[str]]:
    def edit(lines: list[str]) -> list[str]:
        assert old in lines[5]
        return [*lines[:5], lines[5].replace(old, new), *lines[6:]]

    return edit


def _header(old: str, new: str) -> Callable[[list[str]], list[str]]:
    def edit(lines: list[str]) -> list[str]:
        assert old in lines[0]
        return [lines[0].replace(old, new), *lines[1:]]

    return edit


REFUSALS: dict[str, Callable[[list[str]], list[str]]] = {
    "missing root": lambda lines: lines[:-1],
    "uncertified": _replace_in_root(" uncert 0 ", " uncert 1 "),
    "capped": _replace_in_root(" capped 0 ", " capped 1 "),
    "uncert line": lambda lines: [*lines, "UNCERT 4 pass 0 box 0/10,1/10,0/10,1/10,0/8,1/8 |"],
    "wrong id": _replace_in_root("ROOT 4 ", "ROOT 40 "),
    "outside region": lambda lines: [*lines, lines[1].replace("pass 0", "pass 1")],
    "unparsed line": lambda lines: [*lines, "progress 25/400 roots"],
    "no header": lambda lines: lines[1:],
    "other mode": _header("mode=d4", "mode=full"),
    "partial region": _header("x0-9", "x0-8"),
    "umin": lambda lines: [lines[0] + " umin=2^-4/8", *lines[1:]],
    "unknown atoms": _header("atoms=grid", "atoms=grid+lucky"),
    "two headers": lambda lines: [*lines, lines[0].replace("depth=40", "depth=30")],
    "duplicated root": lambda lines: [*lines, lines[1]],
    "torn line": lambda lines: [*lines[:5], lines[5][:40] + lines[6], *lines[7:]],
    "region beyond the side": _header("x0-9", "x0-10"),
    "malformed region": _header("bins0-3", "bins0-3+"),
}


@pytest.mark.parametrize("name", sorted(REFUSALS))
def test_a_log_short_of_its_region_or_settings_is_refused(tmp_path: Path, name: str) -> None:
    lines = REFUSALS[name](_zmx2_lines(2, "d4"))
    assert not zmx2_clean(audit_zmx2(TOY, _write(tmp_path / "roots.log", lines), "d4"))


def test_a_root_recorded_twice_is_counted(tmp_path: Path) -> None:
    lines = _zmx2_lines(2, "d4")
    result = audit_zmx2(TOY, _write(tmp_path / "roots.log", [*lines, lines[1]]), "d4")
    assert result["roots_recorded_more_than_once"] == 1
    assert result["repeated_roots"] == ["pass 0 root 0/10,1/10,0/10,1/10,0/8,1/8"]


def _as_region_runs(lines: list[str], cut: int) -> tuple[list[str], list[str]]:
    """A whole-region log as the two runs ``--xhi cut-1`` and ``--xlo cut`` would write."""
    header, roots = lines[0], [line for line in lines[1:] if line.startswith("ROOT ")]
    last = int(re.findall(r"region=x0-(\d+),", header)[0])

    def run(lo: int, hi: int) -> list[str]:
        column = [r for r in roots if lo <= int(r.split()[5].split("/")[0]) <= hi]
        return [header.replace(f"region=x0-{last},", f"region=x{lo}-{hi},"), *column]

    return run(0, cut - 1), run(cut, last)


@pytest.mark.parametrize("mode", ["d4", "full"])
def test_region_runs_audit_as_one_whether_joined_or_apart(tmp_path: Path, mode: str) -> None:
    last = 9 if mode == "d4" else 19
    west, east = _as_region_runs(_zmx2_lines(2, mode), 3)
    apart = [_write(tmp_path / "west.log", west), _write(tmp_path / "east.log", east)]
    joined = _write(tmp_path / "joined.log", [*east, *west])
    regions = [f"x0-2,y0-{last},bins0-3", f"x3-{last},y0-{last},bins0-3"]
    for logs, order in ((apart, regions), ([joined], regions[::-1])):
        result = audit_zmx2(TOY, logs, mode)
        assert zmx2_clean(result), result
        assert result["joined"]
        assert [run["region"] for run in result["runs"]] == order
        assert result["roots_present"] == result["roots_in_region"]
    paths = [log["path"] for log in audit_zmx2(TOY, apart, mode)["logs"]]
    assert paths == [str(path) for path in apart]


#: Ways a joined record falls short, each applied to the (west, east) region runs.
JOIN_REFUSALS: dict[str, Callable[[list[str], list[str]], list[list[str]]]] = {
    "a run missing": lambda west, _east: [west],
    "other settings": lambda west, east: [
        west,
        [east[0].replace("depth=40", "depth=30"), *east[1:]],
    ],
    "a root beyond its run's limits": lambda west, east: [west[:-1], [*east, west[-1]]],
    "overlapping runs": lambda west, east: [west, [*east, west[1]]],
    "a header dropped": lambda west, east: [[*west, *east[1:]]],
    "the same run twice": lambda west, east: [west, east, east],
}


@pytest.mark.parametrize("name", sorted(JOIN_REFUSALS))
def test_a_joined_record_short_of_the_union_is_refused(tmp_path: Path, name: str) -> None:
    runs = JOIN_REFUSALS[name](*_as_region_runs(_zmx2_lines(2, "d4"), 3))
    paths = [_write(tmp_path / f"run{i}.log", run) for i, run in enumerate(runs)]
    assert not zmx2_clean(audit_zmx2(TOY, paths, "d4"))


def test_the_zmx2_command_derives_the_new_regions_and_requires_atoms(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    log = str(_write(tmp_path / "roots.log", _zmx2_lines(9, "d4", "pairpts")))
    code, result = _run(
        capsys, "zmx2", "--case", "77", "--mode", "d4", "--atoms", "pairpts", log
    )
    assert code == 0, result
    assert result["roots_present"] == 8100
    # What Hosono's README states of its unpublished run, reported beside the audit.
    assert (result["atoms_source_ran"], result["atoms_as_source_ran"]) == ("pairpts", True)
    assert result["boxes_stated_by_source"] == 5810824
    assert not result["boxes_equal_source_statement"]
    code, result = _run(capsys, "zmx2", "--case", "77", "--mode", "d4", "--atoms", "grid", log)
    assert code == 1
    assert not result["atoms_as_required"]
    # A side-9 log is not a side-8 one.
    code, result = _run(capsys, "zmx2", "--case", "59", "--mode", "d4", log)
    assert code == 1
    assert result["roots_outside_region"] == 8100 - 6400


# --- the source's logs, root for root ----------------------------------------------------


def _two_more_boxes(text: str) -> str:
    """The first root's census changed: one leaf split once more."""
    return re.sub(r" boxes (\d+) ", lambda m: f" boxes {int(m[1]) + 2} ", text, count=1)


def _replay(source: Path, path: Path, edit: Callable[[str], str] | None = None) -> Path:
    """The source's log as a replay might write it: other timings, roots reversed."""
    lines = read_record_bytes(source).decode("ascii").splitlines()
    header = [line for line in lines if line.startswith("# zmx2 cert ")][:1]
    roots = [re.sub(r" ms \d+$", " ms 7", line) for line in lines if line.startswith("ROOT ")]
    text = "\n".join([*header, *reversed(roots)]) + "\n"
    path.write_text(edit(text) if edit else text, encoding="ascii")
    return path


@pytest.mark.parametrize("mode", ["d4", "full"])
def test_a_replay_of_s60_compares_root_for_root(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], mode: str
) -> None:
    shipped = IMPORTED_CASES[60].bundle_dir / f"zmx2_{mode}" / "roots.log"
    replay = str(_replay(shipped, tmp_path / "roots.log"))
    code, audited = _run(
        capsys, "zmx2", "--case", "60", "--mode", mode, "--atoms", "grid", replay
    )
    assert code == 0, audited
    code, compared = _run(
        capsys, "compare-zmx2", "--case", "60", "--mode", mode, "--records", replay
    )
    assert code == 0, compared
    assert compared["roots_identical"] == audited["roots_in_region"]
    assert compared["shipped_roots_not_replayed"] == 0
    deeper = str(_replay(shipped, tmp_path / "deeper.log", _two_more_boxes))
    code, compared = _run(
        capsys, "compare-zmx2", "--case", "60", "--mode", mode, "--records", deeper
    )
    assert code == 1
    assert len(compared["roots_whose_census_differs"]) == 1


@pytest.mark.parametrize("mode", ["d4", "full"])
def test_a_replay_joined_from_region_runs_compares_root_for_root(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], mode: str
) -> None:
    shipped = IMPORTED_CASES[60].bundle_dir / f"zmx2_{mode}" / "roots.log"
    lines = _replay(shipped, tmp_path / "roots.log").read_text(encoding="ascii").splitlines()
    west, east = _as_region_runs(lines, 17)
    parts = [str(_write(tmp_path / "west.log", west)), str(_write(tmp_path / "east.log", east))]
    code, audited = _run(capsys, "zmx2", "--case", "60", "--mode", mode, *parts)
    assert code == 0, audited
    assert audited["joined"]
    assert [run["roots"] for run in audited["runs"]] == [len(west) - 1, len(east) - 1]
    code, compared = _run(
        capsys, "compare-zmx2", "--case", "60", "--mode", mode, "--records", *parts
    )
    assert code == 0, compared
    assert compared["headers_equal"]
    assert not compared["headers_identical"]
    assert set(compared["not_compared"]) == {"region", "ms"}
    assert compared["roots_identical"] == audited["roots_in_region"]
    # Each root once: the whole replay beside its parts repeats every root.
    whole = str(tmp_path / "roots.log")
    code, compared = _run(
        capsys, "compare-zmx2", "--case", "60", "--mode", mode, "--records", whole, *parts
    )
    assert code == 1
    assert compared["replay_roots_recorded_more_than_once"] == audited["roots_in_region"]


#: Each control on the source's own s(60) d4 log: the edit, and the field of the audit
#: and of the comparison that refuses it. A comparison counts a dropped root, not fails it.
S60_REFUSALS: dict[str, tuple[Callable[[list[str]], list[str]], str, str | None]] = {
    "dropped root": (lambda lines: lines[:-1], "roots_missing", None),
    "duplicated root": (
        lambda lines: [*lines, lines[-1]],
        "roots_recorded_more_than_once",
        "replay_roots_recorded_more_than_once",
    ),
    "uncert line": (
        lambda lines: [*lines, "UNCERT 7 pass 0 box 0/10,1/10,0/10,1/10,3/8,4/8 | x"],
        "uncert_lines",
        "replay_uncert_lines",
    ),
}


@pytest.mark.parametrize("name", sorted(S60_REFUSALS))
def test_a_mutated_s60_log_is_refused(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], name: str
) -> None:
    edit, audit_field, compare_field = S60_REFUSALS[name]
    shipped = IMPORTED_CASES[60].bundle_dir / "zmx2_d4" / "roots.log"
    lines = edit(read_record_bytes(shipped).decode("ascii").splitlines())
    log = str(_write(tmp_path / "roots.log", lines))
    code, audited = _run(capsys, "zmx2", "--case", "60", "--mode", "d4", log)
    assert code == 1
    assert audited[audit_field] == 1
    code, compared = _run(
        capsys, "compare-zmx2", "--case", "60", "--mode", "d4", "--records", log
    )
    if compare_field is None:
        assert code == 0, compared
        assert compared["shipped_roots_not_replayed"] == 1
    else:
        assert code == 1
        assert compared[compare_field] == 1


def test_the_source_zmx2_manifests_state_their_logs(tmp_path: Path) -> None:
    case = IMPORTED_CASES[60]
    shipped = case.bundle_dir / "zmx2_d4" / "roots.log"
    manifest = shipped.parent / "manifest.txt"
    stated = audit_zmx2_manifest(manifest, shipped, audit_zmx2(case, shipped, "d4"))
    assert stated["consistent"], stated
    assert stated["verdict_stated"] == "VERIFIED-D4"
    deeper = _replay(shipped, tmp_path / "deeper.log", _two_more_boxes)
    stated = audit_zmx2_manifest(manifest, deeper, audit_zmx2(case, deeper, "d4"))
    assert stated["header_as_stated"]
    assert stated["lines_as_stated"]
    assert not stated["log_sha256_as_stated"]
    assert not stated["totals_as_stated"]
    assert not stated["consistent"]


def test_the_s32_sym_atoms_log_is_read_from_xz_and_compared(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert S32_SYM is not None
    data = read_record_bytes(S32_SYM)
    # The digest the source's manifest gives for the log, decompressed.
    assert hashlib.sha256(data).hexdigest().startswith("3b867c398c121401")
    assert read_record_bytes(S32_SYM.with_suffix("")) == data
    replay = str(_replay(S32_SYM, tmp_path / "roots.log"))
    code, audited = _run(
        capsys, "zmx2", "--case", "32", "--mode", "full", "--atoms", "pairpts+sym", replay
    )
    assert code == 0, audited
    assert audited["roots_present"] == 28800
    assert audited["flags"]["pair_points"]
    assert audited["flags"]["sym_atoms"]
    code, compared = _run(
        capsys, "compare-zmx2", "--case", "32", "--mode", "full", "--records", replay
    )
    assert code == 0, compared
    assert compared["headers_equal"]
    assert compared["roots_identical"] == 28800
    plain = _replay(S32_SYM, tmp_path / "plain.log", lambda t: t.replace("+sym", "", 1))
    code, compared = _run(
        capsys, "compare-zmx2", "--case", "32", "--mode", "full", "--records", str(plain)
    )
    assert code == 1
    assert not compared["headers_equal"]


@pytest.mark.parametrize("n", [59, 77])
def test_no_reference_log_is_invented_for_wand125(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], n: int
) -> None:
    log = str(_write(tmp_path / "roots.log", _zmx2_lines(2, "d4")))
    with pytest.raises(SystemExit) as refused:
        main(["compare-zmx2", "--case", str(n), "--mode", "d4", "--records", log])
    assert refused.value.code == 2
    capsys.readouterr()


# --- zm_mixed.py -------------------------------------------------------------------------


def test_the_s60_records_cover_the_d4_region(capsys: pytest.CaptureFixture[str]) -> None:
    case = IMPORTED_CASES[60]
    records = case.bundle_dir / "zm_mixed_d4" / "roots.jsonl"
    code, result = _run(capsys, "zm-mixed", "--case", "60")  # the source's complete run
    assert code == 0, result
    assert result["records"] == str(records.relative_to(REPO))
    assert result["roots_present"] == 102400
    manifest = json.loads((records.parent / "manifest.json").read_text(encoding="utf-8"))
    shipped = {k: v for k, v in manifest["result"]["census"].items() if k != "cpu"}
    assert result["census"] == shipped
    code, stated = _run(capsys, "zm-mixed-manifest", "--case", "60")
    assert code == 0, stated
    assert stated["complete_run"]["records_match_manifest"]


def test_s77s_manifest_states_a_verification_it_cannot_show(
    capsys: pytest.CaptureFixture[str],
) -> None:
    code, stated = _run(capsys, "zm-mixed-manifest", "--case", "77")
    assert code == 0, stated
    assert not stated["records_audited"]
    assert not stated["complete_run"]["records_retained"]
    assert stated["complete_run"]["roots_stated"] == 129600
    assert stated["verdict"] == "stated verified"
    with pytest.raises(SystemExit) as refused:
        main(["zm-mixed", "--case", "77"])  # no record to default to
    assert refused.value.code == 2
    capsys.readouterr()


def test_s59s_two_runs_are_undecided_from_their_manifests(
    capsys: pytest.CaptureFixture[str],
) -> None:
    code, stated = _run(capsys, "zm-mixed-manifest", "--case", "59")
    assert code == 1
    assert stated["consistent"]
    assert not stated["states_complete_verification"]
    assert stated["complete_run"]["uncertified_boxes_stated"] == 6
    deep = stated["deep_run"]
    assert deep["roots_of_declared_region"] == ["27/20,7/5,13/10,27/20,1/4,9/32"]
    assert deep["depth"] == 34
    assert deep["uncertified_boxes_stated"] == 0
    assert stated["verdict"] == "undecided"
    assert len(stated["decided_from_manifests"]) == 3
    assert "neither published" in stated["undecided"]
    report, clean, undecided = check_imported_case(IMPORTED_CASES[59])
    assert clean
    assert undecided == stated["undecided"]
    assert report["zm_mixed_verdict"] == "undecided"
    assert cover_clean(report["cover"])
    # Without the deeper run nothing claims to close the 6 boxes: decided, not clean.
    alone = audit_zm_mixed_manifests(replace(IMPORTED_CASES[59], deep_manifest=None))
    assert alone["verdict"] == "not clean"
    assert "undecided" not in alone


#: A toy zm_mixed case of side 1 (1,600 roots) and the root R its deep run re-checks.
ROOT_R = ("1/4", "3/10", "1/5", "1/4", "1/4", "9/32")
BOX_IN_R = ["13/50", "27/100", "21/100", "11/50", "33/128", "17/64"]
REGION_R: dict[str, str | None] = dict(
    zip(("cx_lo", "cx_hi", "cy_lo", "cy_hi", "u_lo", "u_hi"), ROOT_R, strict=True)
)
NO_REGION: dict[str, str | None] = dict.fromkeys(REGION_R)


def _toy_zm_case(tmp_path: Path) -> Case:
    checker = tmp_path / "checker"
    checker.mkdir()
    for name in ("zm_mixed.py", "mixed_cover.py", "zeromargin.py"):
        (checker / name).write_text(f"# {name}\n", encoding="ascii")
    bundle = tmp_path / "certificates" / "toy"
    bundle.mkdir(parents=True)
    (bundle / "toy.txt").write_text("a toy cover\n", encoding="ascii")
    paths = tuple(checker / name for name in ("zm_mixed.py", "mixed_cover.py", "zeromargin.py"))
    return Case(3, 1, "toy", "toy.txt", Fraction(5, 2), 0, 0, source=tmp_path, checker=paths)


def _zm_header(
    case: Case, depth: int = 24, region: Mapping[str, str | None] = NO_REGION
) -> dict[str, Any]:
    assert case.checker is not None
    digests = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in case.checker
    }
    digests["input"] = hashlib.sha256(case.cover_path.read_bytes()).hexdigest()
    settings = {**ZM_MIXED_SETTINGS, "theta_bias": 4, "clip": True, "tprime": False}
    return {
        "kind": "zm_mixed cert header",
        "version": 2,
        "sha256": digests,
        "input": "toy.txt",
        "total": "5/2",
        "settings": {**settings, "depth": depth, "region": dict(region)},
    }


def _zm_record(root: tuple[str, ...], unc: list[list[str]] | None = None) -> dict[str, Any]:
    unc = unc or []
    st = {"ADM": 1, "EMPTY": 0, "UNCERT": len(unc), "boxes": 1 + 2 * len(unc), "maxdepth": 1}
    return {"label": "", "root": list(root), "st": {**st, "cpu": 0.01}, "unc": unc, "cpu": None}


def _zm_file(path: Path, header: dict[str, Any], records: list[dict[str, Any]]) -> Path:
    path.write_text(
        "\n".join(json.dumps(r) for r in [header, *records]) + "\n", encoding="utf-8"
    )
    return path


def _toy_roots() -> list[tuple[str, ...]]:
    xs = [str(Fraction(i, 20)) for i in range(11)]
    us = [str(Fraction(k, 32)) for k in range(17)]
    return [
        (xs[i], xs[i + 1], xs[j], xs[j + 1], us[k], us[k + 1])
        for i in range(10)
        for j in range(10)
        for k in range(16)
    ]


def _complete_run(tmp_path: Path, case: Case, unc: list[list[str]]) -> Path:
    records = [_zm_record(root, unc if root == ROOT_R else None) for root in _toy_roots()]
    return _zm_file(tmp_path / "complete.jsonl", _zm_header(case), records)


def _other_root(header: dict[str, Any], records: list[dict[str, Any]]) -> None:
    """The deep run certifies the next root up in ``u``, not ``R``."""
    header["settings"]["region"] = {**REGION_R, "u_lo": "9/32", "u_hi": "5/16"}
    records[0]["root"] = [*ROOT_R[:4], "9/32", "5/16"]


DEEP_FAULTS: dict[str, Callable[[dict[str, Any], list[dict[str, Any]]], None]] = {
    "none": lambda _header, _records: None,
    "uncertified": lambda _header, records: records[0].update(unc=[BOX_IN_R]),
    "other checker": lambda header, _records: header["sha256"].update(input="0" * 64),
    "other settings": lambda header, _records: header["settings"].update(cert_mode=False),
    "other root": _other_root,
    "root missing": lambda header, _records: header["settings"].update(
        region={**REGION_R, "u_hi": "5/16"}
    ),
}


@pytest.mark.parametrize("fault", sorted(DEEP_FAULTS))
def test_the_composite_is_clean_only_when_a_deep_run_certifies_every_open_root(
    tmp_path: Path, fault: str
) -> None:
    case = _toy_zm_case(tmp_path)
    complete = _complete_run(tmp_path, case, [BOX_IN_R, [*BOX_IN_R[:4], "1/4", "33/128"]])
    alone = audit_zm_mixed(case, complete)
    assert not zm_mixed_clean(alone)
    assert alone["uncertified_roots"] == [",".join(ROOT_R)]
    header, records = _zm_header(case, 34, REGION_R), [_zm_record(ROOT_R)]
    DEEP_FAULTS[fault](header, records)
    deep = _zm_file(tmp_path / "deep.jsonl", header, records)
    result = audit_zm_mixed_composite(case, complete, [deep])
    assert result["uncertified_boxes_listed"] == 2
    assert result["composite_clean"] == (fault == "none"), result
    assert [r["sha256_as_named"] for r in result["records_named_by_source_manifests"]] == [None]


def test_an_uncertified_box_outside_its_root_is_refused(tmp_path: Path) -> None:
    case = _toy_zm_case(tmp_path)
    complete = _complete_run(tmp_path, case, [[*BOX_IN_R[:5], "5/16"]])
    deep = _zm_file(
        tmp_path / "deep.jsonl", _zm_header(case, 34, REGION_R), [_zm_record(ROOT_R)]
    )
    result = audit_zm_mixed_composite(case, complete, [deep])
    assert not result["uncertified_boxes_inside_their_roots"]
    assert not result["composite_clean"]


# --- the split covers: s(76) and s(95) ---------------------------------------------------

#: Total, points, segments, the side, segment lengths, and what the source's two checkers
#: split: the zmx2 roots it leaves, the zm_mixed.py sub-roots, their boxes and depth.
SPLIT_STATED = {
    76: (
        "3788361049/50000000",
        41633,
        9744,
        9,
        {"1/500": 2104, "1/50": 5976, "1/16": 1664},
        (4, 64, 4950, 15),
    ),
    95: (
        "3791753447/40000000",
        48352,
        11438,
        10,
        {"1/500": 3222, "1/50": 5976, "1/16": 2240},
        (19, 304, 9614, 13),
    ),
}


@pytest.mark.parametrize("n", sorted(SPLIT_STATED))
def test_a_split_cover_is_well_formed_light_and_symmetric(n: int) -> None:
    total, points, segments, side, lengths, _ = SPLIT_STATED[n]
    result = audit_cover(SPLIT_CASES[n])
    assert cover_clean(result), result
    assert (result["total"], result["points"], result["segments"]) == (total, points, segments)
    assert Fraction(total) < n
    # Segment mass on every grid line, the container's four walls included.
    lines = sorted(str(c) for c in range(side + 1))
    assert result["lines_carrying_segments"] == {"x": lines, "y": lines}
    assert result["segment_lengths"] == lengths


@pytest.mark.parametrize("n", sorted(SPLIT_STATED))
def test_the_source_and_the_replay_are_each_one_decision_and_agree(n: int) -> None:
    *_, side, _, (open_roots, sub, boxes, depth) = SPLIT_STATED[n]
    region = len(zmx2_roots(side, "d4"))
    report, clean = check_split_case(SPLIT_CASES[n])
    assert clean, report
    for name in ("source_composite", "replay_composite"):
        composite = report[name]
        assert composite["composite_clean"]
        assert composite["open_root_count"] == open_roots
        assert composite["roots_certified_by_zmx2"] == region - open_roots
        assert composite["zm_mixed_roots_certified"] == sub == 16 * open_roots
        assert composite["sub_roots_tile_open_roots_exactly"]
        assert composite["open_roots_equal_source_list"]
        assert composite["zm_mixed_roots_equal_source_jobs"]
        assert composite["zm_mixed_census"]["boxes"] == boxes
        assert composite["zm_mixed_census"]["maxdepth"] == depth
        assert composite["zm_mixed_census"]["UNCERT"] == 0
    assert report["replay_zmx2_vs_source"]["roots_identical"] == region
    assert report["replay_zm_mixed_vs_source"]["roots_identical"] == sub
    assert report["wall_control_vs_replay"]["roots_identical"] == region


@pytest.mark.parametrize("n", sorted(SPLIT_STATED))
def test_the_composite_command_reads_the_replay_or_the_source(
    capsys: pytest.CaptureFixture[str], n: int
) -> None:
    case = SPLIT_CASES[n]
    assert case.split is not None
    for extra in ([], ["--source"]):
        code, result = _run(capsys, "composite", "--case", str(n), *extra)
        assert code == 0, result
        assert result["composite_clean"]
    code, result = _run(capsys, "compare-sub-roots", "--case", str(n))
    assert code == 0, result
    code, result = _run(
        capsys, "compare-zmx2", "--case", str(n), "--records", str(case.split.replay_zmx2)
    )
    assert code == 0, result
    # zmx2 alone does not decide a split cover: its open roots are uncertified.
    code, result = _run(capsys, "zmx2", "--case", str(n), "--mode", "d4", str(case.split.zmx2))
    assert code == 1
    assert result["uncertified_boxes"] > 0


def _split_copy(tmp_path: Path) -> tuple[Path, Path]:
    """The s(76) replay's zmx2 root log and sub-root records, copied for a fault."""
    split = SPLIT_CASES[76].split
    assert split is not None
    log = tmp_path / "roots.log"
    log.write_bytes(read_record_bytes(split.replay_zmx2))
    records = tmp_path / "zm_mixed"
    records.mkdir()
    for path in sorted(split.replay_zm_mixed.glob("j*.jsonl")):
        shutil.copyfile(path, records / path.name)
    return log, records


def _edit_record(
    records: Path, name: str, edit: Callable[[list[dict[str, Any]]], None]
) -> None:
    path = records / name
    lines = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    edit(lines)
    path.write_text("\n".join(json.dumps(line) for line in lines) + "\n", encoding="utf-8")


def _uncertify(lines: list[dict[str, Any]]) -> None:
    lines[1]["st"]["UNCERT"] = 1
    lines[1]["unc"] = [lines[1]["root"]]


def _move_root(lines: list[dict[str, Any]]) -> None:
    lines[1]["root"] = [*lines[1]["root"][:4], "0", "1/32"]


def _edit_log(log: Path, edit: Callable[[list[str]], list[str]]) -> None:
    log.write_text("\n".join(edit(log.read_text(encoding="ascii").splitlines())) + "\n")


def _drop_root(lines: list[str]) -> list[str]:
    first = next(i for i, line in enumerate(lines) if line.startswith("ROOT 0 "))
    return lines[:first] + lines[first + 1 :]


def _open_root(lines: list[str]) -> list[str]:
    return [
        re.sub(r" uncert 0 ", " uncert 1 ", line) if line.startswith("ROOT 0 ") else line
        for line in lines
    ]


def _cap_root(lines: list[str]) -> list[str]:
    """Root 0, with no uncertified box, marked capped: open, and tiled by no sub-root."""
    return [
        line.replace(" capped 0 ", " capped 1 ") if line.startswith("ROOT 0 ") else line
        for line in lines
    ]


def _with_header(lines: list[str], old: str, new: str) -> list[str]:
    return [
        line.replace(old, new) if line.startswith("# zmx2 cert ") else line for line in lines
    ]


def _every_record(records: Path, edit: Callable[[list[dict[str, Any]]], None]) -> None:
    """The same edit on every record file, so only the required settings can refuse it."""
    for path in sorted(records.glob("j*.jsonl")):
        _edit_record(records, path.name, edit)


SPLIT_FAULTS: dict[str, Callable[[Path, Path], object]] = {
    "none": lambda _log, _records: None,
    "sub-root missing": lambda _log, records: (records / "j000.jsonl").unlink(),
    "sub-root twice": lambda _log, records: shutil.copyfile(
        records / "j000.jsonl", records / "j999.jsonl"
    ),
    "uncertified": lambda _log, records: _edit_record(records, "j000.jsonl", _uncertify),
    "other cover": lambda _log, records: _edit_record(
        records, "j000.jsonl", lambda lines: lines[0]["sha256"].update(input="0" * 64)
    ),
    "other depth": lambda _log, records: _every_record(
        records, lambda lines: lines[0]["settings"].update(depth=23)
    ),
    "not certificate mode": lambda _log, records: _every_record(
        records, lambda lines: lines[0]["settings"].update(cert_mode=False)
    ),
    "other settings": lambda _log, records: _edit_record(
        records, "j001.jsonl", lambda lines: lines[0]["settings"].update(theta_bias=3)
    ),
    "root outside its region": lambda _log, records: _edit_record(
        records, "j000.jsonl", _move_root
    ),
    "zmx2 root missing": lambda log, _records: _edit_log(log, _drop_root),
    "zmx2 root left open": lambda log, _records: _edit_log(log, _open_root),
    "zmx2 root capped": lambda log, _records: _edit_log(log, _cap_root),
    "zmx2 log of another cover": lambda log, _records: _edit_log(
        log, lambda lines: _with_header(lines, "hash=96e61ce6a0aa2545", "hash=0000000000000000")
    ),
    "zmx2 at another depth": lambda log, _records: _edit_log(
        log, lambda lines: _with_header(lines, " depth=40 ", " depth=7 ")
    ),
    "zmx2 at another kappa": lambda log, _records: _edit_log(
        log, lambda lines: _with_header(lines, " kappa=1.5 ", " kappa=0.5 ")
    ),
    "zmx2 at another node cap": lambda log, _records: _edit_log(
        log, lambda lines: _with_header(lines, " node_cap=20000000 ", " node_cap=1000 ")
    ),
    "zmx2 at another K": lambda log, _records: _edit_log(
        log, lambda lines: _with_header(lines, " K=30 ", " K=7 ")
    ),
}


@pytest.mark.parametrize("fault", sorted(SPLIT_FAULTS))
def test_a_split_composite_is_clean_only_when_every_open_root_is_tiled(
    tmp_path: Path, fault: str
) -> None:
    log, records = _split_copy(tmp_path)
    SPLIT_FAULTS[fault](log, records)
    result = audit_split_composite(SPLIT_CASES[76], log, records)
    assert result["composite_clean"] == (fault == "none"), result


def test_a_replayed_sub_root_whose_census_differs_is_refused(tmp_path: Path) -> None:
    _, records = _split_copy(tmp_path)
    split = SPLIT_CASES[76].split
    assert split is not None
    assert sub_root_comparison_clean(compare_sub_roots(split.zm_mixed, records))
    _edit_record(records, "j005.jsonl", lambda lines: lines[1]["st"].update(boxes=1))
    result = compare_sub_roots(split.zm_mixed, records)
    assert result["files_that_differ"] == ["j005.jsonl"]
    assert not sub_root_comparison_clean(result)
