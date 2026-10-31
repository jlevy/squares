"""Stage 4's negative controls for the ``zmx2`` replays: mutated covers it refuses.

``campaign/result-import.md`` asks that two mutated certificates be refused by every
checker that accepted the original, with a test holding them. For each cover that
``devtools.replay_evand_zmx2`` replays, ``CONTROLS`` names two mutations and the root
region where ``zmx2`` refuses each, and the receipts are retained in
``receipts/controls/`` of the packet holding that case's replay. These tests read the
retained receipts and the retained covers only; nothing here runs ``cargo`` or ``zmx2``.

The s(76) and s(95) controls were run at intake by their packets' own scripts
(``receipts/programs/run_control.sh``), with ``mutate`` and the binary the driver built,
so their receipts name the scratch paths they ran in; the mutated cover's digest binds
each to ``mutate``. Those covers are also decided in part by ``zm_mixed.py``, so their
packets keep, beside the ``zmx2`` controls, ``zm_mixed.py pose``'s exact evaluation of
each mutated cover at a pose where it captures less than one, and of the published
cover at the same pose, where it captures more.
"""

from __future__ import annotations

import gzip
import hashlib
import re
import shlex
from collections import Counter
from fractions import Fraction
from functools import cache
from pathlib import Path

import pytest

from devtools import replay_evand_zmx2 as driver
from devtools.audit_evand_mixed_covers import MixedCover, parse_cover

WEB = driver.WEB

#: Where each case's controls are retained: the packet that holds its replay.
PACKETS = {
    32: WEB / "evand-zmx2-sym-atoms-2026-09-30",
    59: WEB / "wand125-point-and-mixed-2026-10-01",
    60: WEB / "evand-square-packing-2026-10-01",
    61: WEB / "wand125-point-n61-2026-09-30",
    76: WEB / "bengreff-s76-certificate-2026-10-14",
    77: WEB / "wand125-point-and-mixed-2026-10-01",
    95: WEB / "bengreff-s95-certificate-2026-10-15",
    44: WEB / "moh63-dev-s44-equals-7-2026-10-29",
}

#: The checker build receipt each packet's controls ran with, and where the packet keeps it.
BUILDS = {
    WEB / "evand-zmx2-sym-atoms-2026-09-30": ("92a4cfe8", "controls/zmx2_92a4cfe8_build.log"),
    WEB / "wand125-point-and-mixed-2026-10-01": (
        "6b7f0f79",
        "controls/zmx2_6b7f0f79_build.log",
    ),
    WEB / "evand-square-packing-2026-10-01": ("6b7f0f79", "controls/zmx2_6b7f0f79_build.log"),
    WEB / "wand125-point-n61-2026-09-30": ("6b7f0f79", "controls/zmx2_6b7f0f79_build.log"),
    WEB / "bengreff-s76-certificate-2026-10-14": ("6b7f0f79", "n76_zmx2_build.log"),
    WEB / "bengreff-s95-certificate-2026-10-15": ("6b7f0f79", "n95_zmx2_build.log"),
    WEB / "moh63-dev-s44-equals-7-2026-10-29": ("e2bb84e9", "n44_zmx2_build.log"),
}

#: The s(76) and s(95) packets' other controls: zmx2 on the cover without its wall
#: segments, which ``devtools.audit_evand_mixed_covers check`` compares with the replay,
#: and the ``zm_mixed.py pose`` receipts that `test_zm_mixed_pose_refuses_each_mutation`
#: holds, by the name each packet gave the original's.
POSES = {
    76: ("n76_pose_{kind}_violation.log", "n76_pose_original_at_{at}_control_violation.log"),
    95: ("n95_pose_{kind}_violation.log", "n95_pose_original_at_{at}_control.log"),
}
POSE_AT = {"drop-heaviest-point": "point", "drop-heaviest-segment": "segment"}


def other_controls(n: int) -> set[str]:
    kept = {f"n{n}_control_nowall_zmx2_d4.log", f"n{n}_control_nowall_zmx2_d4_roots.log.gz"}
    mutated, original = POSES[n]
    for kind, at in POSE_AT.items():
        kept |= {mutated.format(kind=kind), original.format(at=at)}
    return kept


#: A control receipt as this module's driver writes it.
CWD = re.compile(
    r"^# cwd: .* zmx2\.rs (?P<checker>[0-9a-f]{64}) built from retained bytes; "
    r"cover (?P<mutated>[0-9a-f]{64}), the (?P<kind>\S+) mutation of "
    r"(?P<original>[0-9a-f]{64}) decompressed from (?P<path>\S+): .*, removing mass "
    r"(?P<removed>\S+)$",
    re.MULTILINE,
)
#: As the s(76) and s(95) packets' run_control.sh wrote it, naming the binary it ran.
CWD_PACKET_SCRIPT = re.compile(
    r"^# cwd: scratch: zmx2\.rs (?P<checker>[0-9a-f]{64}) built from retained bytes "
    r"\(binary sha256 (?P<binary>[0-9a-f]{64})\); cover (?P<mutated>[0-9a-f]{64}), the "
    r"(?P<kind>\S+) mutation \(devtools\.replay_evand_zmx2\.mutate\) of "
    r"(?P<original>[0-9a-f]{64})$",
    re.MULTILINE,
)
HEADER = re.compile(
    r"^# zmx2 cert hash=\S+ mode=(?P<mode>\S+) .* "
    r"region=x(?P<x>\d+-\d+),y(?P<y>\d+-\d+),bins0-3$",
    re.MULTILINE,
)
DONE = re.compile(
    r"^done in \S+ wall: roots (?P<roots>\d+) \(missing 0\), .* uncertified (?P<unc>\d+),",
    re.MULTILINE,
)
VERDICT = re.compile(r"^NOT VERIFIED: (?P<unc>\d+) uncertified boxes$", re.MULTILINE)
FOOTER = re.compile(r"^# finished \S+; exit (?P<exit>\d+); ", re.MULTILINE)


@cache
def cover_text(n: int) -> str:
    return gzip.decompress(driver.CASES[n].cover.read_bytes()).decode("ascii")


def as_mixed(text: str) -> MixedCover:
    """Parse with the audit's own reader; a plain point cover is mixed with no segments."""
    if text.split("#", 1)[0].split()[:2] == ["mixed", "1"]:
        return parse_cover(text)
    return parse_cover("mixed 1\n" + text + "0\n0\n")


def total(cover: MixedCover) -> Fraction:
    mass = sum(w for *_, w in cover.points) + sum(s[4] for s in cover.segments)
    return Fraction(mass, cover.mass_denominator)


def edge(cover: MixedCover) -> int:
    scaled = cover.side * cover.denominator
    assert scaled.denominator == 1
    return scaled.numerator


def images(point: tuple[int, int], side: int) -> set[tuple[int, int]]:
    x, y = point
    out: set[tuple[int, int]] = set()
    for a, b in ((x, y), (y, x)):
        out |= {(a, b), (side - a, b), (a, side - b), (side - a, side - b)}
    return out


def point_weights(cover: MixedCover) -> Counter[tuple[int, int]]:
    weights: Counter[tuple[int, int]] = Counter()
    for x, y, w in cover.points:
        weights[(x, y)] += w
    return weights


Entry = tuple[tuple[int, int], tuple[int, int], int]


def segment_entries(cover: MixedCover) -> Counter[Entry]:
    entries: Counter[Entry] = Counter()
    for x0, y0, x1, y1, w in cover.segments:
        a, b = sorted(((x0, y0), (x1, y1)))
        entries[(a, b, w)] += 1
    return entries


def entry_images(entry: Entry, side: int) -> set[Entry]:
    """The images of a segment under the symmetries, by mapping both endpoints alike."""
    (ax, ay), (bx, by), w = entry
    maps = [
        lambda x, y: (x, y),
        lambda x, y: (side - x, y),
        lambda x, y: (x, side - y),
        lambda x, y: (side - x, side - y),
        lambda x, y: (y, x),
        lambda x, y: (side - y, x),
        lambda x, y: (y, side - x),
        lambda x, y: (side - y, side - x),
    ]
    out: set[Entry] = set()
    for g in maps:
        a, b = sorted((g(ax, ay), g(bx, by)))
        out.add((a, b, w))
    return out


def d4_invariant(cover: MixedCover) -> bool:
    """Points and segment entries are each mapped onto themselves by the symmetries."""
    side = edge(cover)
    weights = point_weights(cover)
    entries = segment_entries(cover)
    for g in (lambda x, y: (side - x, y), lambda x, y: (y, x)):
        if Counter({g(*p): w for p, w in weights.items()}) != weights:
            return False
        image: Counter[Entry] = Counter()
        for (a, b, w), count in entries.items():
            ga, gb = sorted((g(*a), g(*b)))
            image[(ga, gb, w)] += count
        if image != entries:
            return False
    return True


def expected_orbit_mass(cover: MixedCover, kind: str) -> Fraction:
    """The mass of the orbit ``kind`` names, found from the original cover alone."""
    side = edge(cover)
    if kind == "drop-heaviest-segment":
        entries = segment_entries(cover)
        heaviest = min(entries, key=lambda e: (-e[2], e[0], e[1]))
        orbit = entry_images(heaviest, side)
        mass = sum(e[2] * count for e, count in entries.items() if e in orbit)
        return Fraction(mass, cover.mass_denominator)
    weights = point_weights(cover)
    ranked = sorted(weights, key=lambda p: (-weights[p], p))
    orbit = images(ranked[0], side)
    if kind == "drop-second-heaviest-point":
        orbit = images(next(p for p in ranked if p not in orbit), side)
    return Fraction(sum(weights[p] for p in orbit), cover.mass_denominator)


def applicable(n: int) -> list[str]:
    has_segments = bool(as_mixed(cover_text(n)).segments)
    return [k for k in driver.MUTATIONS if has_segments or k != "drop-heaviest-segment"]


@pytest.mark.parametrize("n", sorted(driver.CASES))
def test_every_mutation_keeps_d4_and_removes_exactly_its_orbit(n: int) -> None:
    text = cover_text(n)
    original = as_mixed(text)
    assert d4_invariant(original)
    for kind in applicable(n):
        mutation = driver.mutate(text, kind)
        mutated = as_mixed(mutation.text)
        assert d4_invariant(mutated), kind
        removed = expected_orbit_mass(original, kind)
        assert removed > 0
        assert mutation.removed == removed == total(original) - total(mutated), kind
        assert mutated.mass_denominator == original.mass_denominator
        dropped = len(original.points) + len(original.segments)
        dropped -= len(mutated.points) + len(mutated.segments)
        assert dropped == mutation.rows > 0
        assert len(text.splitlines()) - len(mutation.text.splitlines()) == mutation.rows
        assert hashlib.sha256(mutation.text.encode()).hexdigest() != driver.CASES[n].sha256


def test_a_point_cover_has_no_segment_mutation() -> None:
    with pytest.raises(ValueError, match="no segments"):
        driver.mutate(cover_text(32), "drop-heaviest-segment")


def test_every_case_has_two_retained_controls() -> None:
    by_case = Counter(n for n, _ in driver.CONTROLS)
    assert by_case == dict.fromkeys(driver.CASES, 2)
    for (n, kind), control in driver.CONTROLS.items():
        assert kind in applicable(n)
        assert control.mode in {"d4", "full"}


def test_the_controls_directories_hold_only_the_controls() -> None:
    expected: dict[Path, set[str]] = {}
    for packet, (_, build) in BUILDS.items():
        expected[packet] = {Path(build).name} if build.startswith("controls/") else set()
    for n in POSES:
        expected[PACKETS[n]] |= other_controls(n)
    for n, kind in driver.CONTROLS:
        receipt = control_receipt(n, kind)
        expected[PACKETS[n]] |= {receipt.name, receipt.name.removesuffix(".log") + "_roots.log"}
    for packet, names in expected.items():
        assert {p.name for p in (packet / "receipts/controls").iterdir()} == names


def control_receipt(n: int, kind: str) -> Path:
    name = driver.CASES[n].name
    found = [
        p
        for p in (PACKETS[n] / "receipts/controls").glob(f"{name}_control_{kind}_zmx2_*.log")
        if not p.name.endswith("_roots.log")
    ]
    assert len(found) == 1, found
    return found[0]


@pytest.mark.parametrize("key", sorted(driver.CONTROLS), ids=lambda k: f"{k[0]}-{k[1]}")
def test_the_retained_control_is_refused_where_recorded(key: tuple[int, str]) -> None:
    n, kind = key
    case, control = driver.CASES[n], driver.CONTROLS[key]
    receipt = control_receipt(n, kind)
    text = receipt.read_text(encoding="utf-8")

    cwd = CWD.search(text)
    by_script = CWD_PACKET_SCRIPT.search(text) if cwd is None else None
    assert cwd is not None or by_script is not None
    mutation = driver.mutate(cover_text(n), kind)
    if cwd is not None:
        assert cwd["path"] == str(case.cover.relative_to(driver.REPO))
        assert Fraction(cwd["removed"]) == mutation.removed
    else:
        assert by_script is not None
        cwd = by_script
        assert cwd["binary"] == build_binary(PACKETS[n])
    assert cwd["kind"] == kind
    assert cwd["checker"] == driver.CHECKERS[case.checker][1]
    assert cwd["original"] == case.sha256
    assert cwd["mutated"] == hashlib.sha256(mutation.text.encode()).hexdigest()
    assert cwd["mutated"] != cwd["original"]

    command = shlex.split(text.splitlines()[0].removeprefix("# command: "))
    assert command[0].endswith("verify2/target/release/zmx2")
    assert command[1] == "cert"
    if by_script is None:
        assert command[0] == "verify2/target/release/zmx2"
    else:
        assert Path(command[2]).name == f"s{n}_{kind}.txt"
    assert f"--{control.mode}" in command
    assert all(flag in command for flag in case.flags)
    region = {
        flag: command[command.index(flag) + 1] for flag in ("--xlo", "--xhi", "--ylo", "--yhi")
    }
    assert f"{region['--xlo']}-{region['--xhi']}" == control.x
    assert f"{region['--ylo']}-{region['--yhi']}" == control.y

    header = HEADER.search(text)
    assert header is not None
    assert (header["mode"], header["x"], header["y"]) == (control.mode, control.x, control.y)
    verdict, done, footer = VERDICT.search(text), DONE.search(text), FOOTER.search(text)
    assert verdict is not None
    assert done is not None
    assert footer is not None
    assert int(verdict["unc"]) == int(done["unc"]) > 0
    assert int(footer["exit"]) == 0

    (x0, x1), (y0, y1) = (tuple(map(int, v.split("-"))) for v in (control.x, control.y))
    roots = (x1 - x0 + 1) * (y1 - y0 + 1) * 4 * (2 if control.mode == "full" else 1)
    assert int(done["roots"]) == roots
    log = receipt.with_name(receipt.name.removesuffix(".log") + "_roots.log")
    lines = log.read_text(encoding="utf-8").splitlines()
    assert lines[0] == header[0]
    root_lines = [line.split() for line in lines if line.startswith("ROOT ")]
    assert len(root_lines) == roots
    assert sum(int(f[f.index("uncert") + 1]) for f in root_lines) == int(verdict["unc"])


def build_binary(packet: Path) -> str:
    """The binary digest the packet's build receipt names."""
    text = (packet / "receipts" / BUILDS[packet][1]).read_text(encoding="utf-8")
    found = re.search(r"^# binary sha256: ([0-9a-f]{64})$", text, re.MULTILINE)
    assert found is not None
    return found[1]


@pytest.mark.parametrize("packet", sorted(BUILDS))
def test_the_build_receipt_names_the_checker_it_built(packet: Path) -> None:
    checker, build = BUILDS[packet]
    text = (packet / "receipts" / build).read_text(encoding="utf-8")
    assert f"zmx2.rs {driver.CHECKERS[checker][1]} " in text
    assert re.search(r"^# finished \S+; exit 0; ", text, re.MULTILINE)
    assert re.search(r"^# binary sha256: [0-9a-f]{64}$", text, re.MULTILINE)


#: ``zm_mixed.py pose``'s verdict: the exact capture of the closed unit square at a pose.
POSE = re.compile(
    r"^pose cx=(?P<cx>\S+) cy=(?P<cy>\S+) u=(?P<u>\S+) \(theta \S+ deg\), admissible True: "
    r"EXACT mu\(Q\) = (?P<mu>\d+/\d+) = \S+ \((?P<verdict>\*\*\* < 1 \*\*\*|OK)\)$",
    re.MULTILINE,
)
POSE_CWD = re.compile(
    r"^# cwd: scratch checker dir: zm_mixed\.py ee3e2915, mixed_cover\.py bb89de15, "
    r"zeromargin\.py 640fe453 \(retained evand packets\); cover (?P<cover>[0-9a-f]{64}), ",
    re.MULTILINE,
)


def pose_receipt(path: Path) -> tuple[str, tuple[Fraction, ...], Fraction]:
    """The cover digest, the pose and the exact capture a pose receipt records."""
    text = path.read_text(encoding="utf-8")
    cwd, pose = POSE_CWD.search(text), POSE.search(text)
    assert cwd is not None
    assert pose is not None, path
    assert re.search(r"^# finished \S+; exit 0; ", text, re.MULTILINE)
    mu = Fraction(pose["mu"])
    assert (mu < 1) == (pose["verdict"] != "OK")
    return cwd["cover"], tuple(Fraction(pose[k]) for k in ("cx", "cy", "u")), mu


@pytest.mark.parametrize("kind", sorted(POSE_AT))
@pytest.mark.parametrize("n", sorted(POSES))
def test_zm_mixed_pose_refuses_each_mutation(n: int, kind: str) -> None:
    """zm_mixed.py, in exact rationals, finds each mutated cover short of one at a pose
    in the D4 region where the published cover captures at least one."""
    controls = PACKETS[n] / "receipts/controls"
    mutated, original = POSES[n]
    digest, pose, mu = pose_receipt(controls / mutated.format(kind=kind))
    mutation = driver.mutate(cover_text(n), kind)
    assert digest == hashlib.sha256(mutation.text.encode()).hexdigest()
    assert mu < 1
    published, same_pose, before = pose_receipt(controls / original.format(at=POSE_AT[kind]))
    assert published == driver.CASES[n].sha256
    assert same_pose == pose
    assert before >= 1
    cx, cy, u = pose
    side = as_mixed(cover_text(n)).side
    assert 0 <= cx <= side / 2
    assert 0 <= cy <= side / 2
    assert 0 <= u <= Fraction(1, 2)


#: The 16 October review's zm_mixed.py control for s(76): job 054's cell, at a depth limit
#: of 12, run on the published cover and on the cover with every mass scaled by 199/200.
REVIEW_ZM_CONTROL = PACKETS[76] / "review/outputs/zm_control"


def test_zm_mixed_refuses_the_reviews_scaled_cover_where_it_certifies_the_published_one() -> (
    None
):
    """At equal settings on one cell, zm_mixed.py certifies the published s(76) cover and
    leaves the 199/200 mutant uncertified: the depth-12 pair of the review's section 7.4.
    Whether a refusal at that depth limit meets stage 4's control rule is the owner's
    question (the review's finding F8)."""
    from devtools.audit_evand_mixed_covers import (  # noqa: PLC0415
        CHECKER_B91D70B6,
        ZM_MIXED_SETTINGS,
        read_zm_mixed,
    )

    pinned = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in CHECKER_B91D70B6
    }
    cell = {
        "cx_lo": "22/5",
        "cx_hi": "89/20",
        "cy_lo": "9/4",
        "cy_hi": "23/10",
        "u_lo": "5/16",
        "u_hi": "11/32",
    }
    runs = {}
    for name in ("s76_cover_v5_j054_depth12", "n76_scaled-199-200_j054_depth12"):
        header, records = read_zm_mixed(REVIEW_ZM_CONTROL / f"{name}.jsonl")
        assert {k: v for k, v in header["sha256"].items() if k != "input"} == pinned
        settings = header["settings"]
        assert settings["region"] == cell
        assert settings["depth"] == 12
        assert all(settings[k] == v for k, v in ZM_MIXED_SETTINGS.items() if k != "depth")
        assert list(records) == [tuple(cell[k] for k in cell)]
        runs[name] = (header, next(iter(records.values())))
    (published, certified), (mutant, refused) = runs.values()
    assert published["sha256"]["input"] == driver.CASES[76].sha256
    assert certified["st"]["UNCERT"] == 0
    assert not certified["unc"]
    assert mutant["sha256"]["input"] != driver.CASES[76].sha256
    assert Fraction(mutant["total"]) == Fraction(published["total"]) * Fraction(199, 200)
    assert refused["st"]["UNCERT"] > 0
    log = (REVIEW_ZM_CONTROL / "n76_scaled-199-200_j054_depth12.log").read_text(
        encoding="utf-8"
    )
    assert "\nNOT VERIFIED (PARTIAL)\n" in log
    assert f"{mutant['sha256']['input']}  input " in log
