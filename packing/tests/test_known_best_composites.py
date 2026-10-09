"""A poster states the data it was drawn from, and is held to that statement.

Until 2026-10-01 the atlas posters printed the pinned data revision, so every data commit
rewrote eight binaries to change six characters. Now each records the data commit and
date it was drawn from, its footer and dateline are held to that record, and it may
trail the pin until the next version (`sqpack.release`, rules 4 and 5). What is pinned
here is each half of that rule and its refusal: a poster that claims the current data
and does not show it fails, one that trails is listed, one drawn for another version
fails, and one whose record names no data commit fails.

Every composite here but the last tests' is synthetic and lives in a scratch directory,
so no test draws a poster or reads the 324-case corpus.
"""

from __future__ import annotations

import hashlib
import struct
import subprocess
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from devtools import build_known_best_atlas as atlas
from devtools import render_composite_pdf
from sqpack import release
from sqpack.known_best import CompositeSpec

REPO = Path(__file__).resolve().parents[2]

#: A data commit that is not the pin, and one that is, for the synthetic family.
EARLIER = "1" * 40
SVG_NAMESPACES = (
    'xmlns="http://www.w3.org/2000/svg" '
    'xmlns:sqpack="https://github.com/jlevy/thinking-scratchpad/ns/sqpack/v1"'
)
SIDE = "s(18) ≤ 4.822876"
LOWER = "s(18) ≥ 4.679"

#: The identity and settings a scratch repository commits under, so the user's global
#: signing and hooks cannot reach it.
SCRATCH_GIT = (
    "-c",
    "user.name=composite test",
    "-c",
    "user.email=composite-test@example.invalid",
    "-c",
    "commit.gpgsign=false",
    "-c",
    "core.hooksPath=/dev/null",
)


def _git(repo: Path, *arguments: str, when: str | None = None) -> str:
    environment = None
    if when is not None:
        environment = {
            "GIT_AUTHOR_DATE": when,
            "GIT_COMMITTER_DATE": when,
            "PATH": "/usr/bin:/bin",
        }
    done = subprocess.run(
        ("git", "-C", str(repo), *SCRATCH_GIT, *arguments),
        capture_output=True,
        text=True,
        check=True,
        env=environment,
    )
    return done.stdout.strip()


def _commit(repo: Path, path: str, text: str, when: str) -> str:
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)
    _git(repo, "add", path)
    _git(repo, "commit", "--quiet", "-m", f"touch {path}", when=when)
    return _git(repo, "rev-parse", "HEAD")


class Family:
    """One synthetic composite and its exports in a scratch atlas directory."""

    def __init__(self, root: Path) -> None:
        self.canvas = atlas.CompositeCanvas(
            CompositeSpec(first_n=18, last_n=18, columns=1, stem="synthetic")
        )
        self.root = root

    def write(
        self,
        identity: atlas.CompositeIdentity | None,
        *,
        lower: str = LOWER,
        stamp: str | None = None,
        dateline: str | None = None,
        exports_of: str | None = None,
    ) -> str:
        """Write the SVG and exports that carry its receipt; returns the SVG text.

        `exports_of` draws the exports from another SVG's text, which is a family whose
        vector changed after its rasters were drawn.
        """
        record = (
            ""
            if identity is None
            else (
                f'      <sqpack:value name="data-date">{identity.data_date}</sqpack:value>\n'
                '      <sqpack:value name="data-revision">'
                f"{identity.data_revision}</sqpack:value>\n"
            )
        )
        shown = identity or atlas.CompositeIdentity(EARLIER, "2026-09-28")
        svg_text = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg {SVG_NAMESPACES} width="{self.canvas.width}" '
            f'height="{self.canvas.height}">\n'
            '  <metadata>\n    <sqpack:profile version="8">\n'
            f"{record}"
            "    </sqpack:profile>\n  </metadata>\n"
            f'  <text data-feature="release">{dateline or shown.dateline}</text>\n'
            f'  <text data-feature="release-stamp">{stamp or shown.stamp}</text>\n'
            '  <g data-feature="packing-card" data-n="18">\n'
            '    <text data-feature="packing-label">18</text>\n'
            f'    <text data-feature="side-bound">{SIDE}</text>\n'
            f'    <text data-feature="lower-bound">{lower}</text>\n'
            "  </g>\n</svg>\n"
        )
        self.canvas.svg_path.parent.mkdir(parents=True, exist_ok=True)
        self.canvas.svg_path.write_text(svg_text, encoding="utf-8")
        digest = hashlib.sha256((exports_of or svg_text).encode("utf-8")).hexdigest()
        for export in self.canvas.rasters:
            header = struct.pack(">IIBBBBB", export.width, export.height, 8, 2, 0, 0, 0)
            blank = (
                atlas.PNG_SIGNATURE
                + atlas._png_chunk(b"IHDR", header)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
                + atlas._png_chunk(b"IEND", b"")  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
            )
            export.path.write_bytes(
                atlas._png_with_summary_source(blank, digest)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
            )
        render_composite_pdf.composite_pdf("synthetic").write_bytes(
            b"%PDF-1.5\n%%EOF\n%"
            + render_composite_pdf.PDF_SOURCE_KEY
            + b": "
            + digest.encode("ascii")
            + b"\n"
        )
        return svg_text


@pytest.fixture
def family(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Family:
    """A synthetic composite family the builder reads in place of the retained two.

    The figure record states one case, and git is not asked about the synthetic data
    revisions, which are no commits; `_identity_git_problems` has tests of its own.
    """
    packing = tmp_path / "packing"
    atlas_root = packing / "atlas/known-best"
    monkeypatch.setattr(atlas, "ROOT", packing)
    monkeypatch.setattr(atlas, "ATLAS_ROOT", atlas_root)
    monkeypatch.setattr(render_composite_pdf, "ATLAS_ROOT", atlas_root)
    monkeypatch.setattr(
        atlas,
        "_figure_entries",
        lambda: {18: {"side": {"display": SIDE}, "lower": {"display": LOWER, "shown": True}}},
    )
    monkeypatch.setattr(atlas, "_identity_git_problems", lambda _path, _identity: [])
    made = Family(tmp_path)
    monkeypatch.setattr(atlas, "COMPOSITES", (made.canvas,))
    return made


def current() -> atlas.CompositeIdentity:
    return atlas.CompositeIdentity(release.DATA_REVISION, "2026-10-01")


def trailing() -> atlas.CompositeIdentity:
    return atlas.CompositeIdentity(EARLIER, "2026-09-28")


def test_a_composite_that_shows_the_pinned_data_and_agrees_with_it_passes(
    family: Family,
) -> None:
    family.write(current())
    findings = atlas.composite_findings()
    assert findings.problems == ()
    assert findings.notes == (
        (
            f"atlas/known-best/synthetic.svg shows {release.PUBLICATION_EDITION}, data of "
            "2026-10-01: the data every page prints"
        ),
    )


def test_a_composite_that_claims_the_pinned_data_and_does_not_show_it_fails(
    family: Family,
) -> None:
    """The strictness the atlas check always had, kept where the claim is made.

    A poster whose data revision is the pin says it shows what every page prints, so a
    card that disagrees with the current figure record is drift, as it was when the
    poster printed the pin itself.
    """
    family.write(current(), lower="s(18) ≥ 4.67")
    assert atlas.composite_findings().problems == (
        (
            "atlas/known-best/synthetic.svg n=18 lower-bound is "
            "('s(18) ≥ 4.67',); expected ('s(18) ≥ 4.679',)"
        ),
    )


def test_a_composite_that_trails_the_pin_is_listed_and_fails_nothing(family: Family) -> None:
    """Rule 5: between version bumps a poster may show older data, and says which.

    The same stale card as the test above. Once the pin has moved past the poster's own
    data revision the card is a note naming the case, which every check prints, and no
    data commit has to redraw eight binaries to clear it.
    """
    family.write(trailing(), lower="s(18) ≥ 4.67")
    findings = atlas.composite_findings()
    assert findings.problems == ()
    stamp = release.edition_at(EARLIER)
    assert findings.notes == (
        (
            f"atlas/known-best/synthetic.svg shows {stamp}, data of 2026-09-28; the pin has "
            f"moved to {release.DATA_REVISION[:12]}, and the composite is redrawn at the next "
            "version or by --update-composites"
        ),
        (
            "atlas/known-best/synthetic.svg trails the data in 1 place, which fails nothing "
            "until the next version:"
        ),
        (
            "  atlas/known-best/synthetic.svg n=18 lower-bound is "
            "('s(18) ≥ 4.67',); expected ('s(18) ≥ 4.679',)"
        ),
    )


def test_with_trailing_switched_off_a_trailing_card_fails(
    family: Family, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The owner's switch, exercised in the position it is not in.

    `COMPOSITES_MAY_TRAIL = False` is the other contract: a poster is redrawn whenever a
    card changes. The trailing poster of the test above then fails on the same card.
    """
    monkeypatch.setattr(atlas, "COMPOSITES_MAY_TRAIL", False)
    family.write(trailing(), lower="s(18) ≥ 4.67")
    assert atlas.composite_findings().problems == (
        (
            "atlas/known-best/synthetic.svg n=18 lower-bound is "
            "('s(18) ≥ 4.67',); expected ('s(18) ≥ 4.679',)"
        ),
    )


def test_a_trailing_composite_that_still_agrees_with_the_data_has_nothing_to_list(
    family: Family,
) -> None:
    """Most data commits change no card: thirty re-pins in a row changed none."""
    family.write(trailing())
    findings = atlas.composite_findings()
    assert findings.problems == ()
    assert len(findings.notes) == 1
    assert "trails" not in findings.notes[0]


@pytest.mark.parametrize("identity", [current(), trailing()])
def test_a_stamp_that_is_not_the_composites_own_record_fails(
    family: Family, identity: atlas.CompositeIdentity
) -> None:
    """The footer is held to the record the drawing carries, trailing or not.

    Trailing excuses a card that the data has since moved past. It never excuses a
    footer that names data other than the drawing's own, which is the one statement a
    poster makes about itself.
    """
    family.write(identity, stamp="v0.0.0-000000")
    assert atlas.composite_findings().problems == (
        (
            "atlas/known-best/synthetic.svg release-stamp is ('v0.0.0-000000',); "
            f"expected ({identity.stamp!r},)"
        ),
        (
            "atlas/known-best/synthetic.svg was drawn for another version than "
            f"{release.PUBLICATION_VERSION}; redraw it with --update-composites"
        ),
    )


def test_a_version_bump_fails_every_composite_until_it_is_redrawn(
    family: Family, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Rule 5's other half: a poster may trail the data, never the version.

    The retained poster is right under the version it was drawn for. Bump the version
    and its stamp is no longer what its record gives, so the check fails and names the
    command, which is what makes a version bump the moment the large assets are rebuilt.
    """
    family.write(trailing())
    assert atlas.composite_findings().problems == ()
    monkeypatch.setattr(release, "PUBLICATION_VERSION", "v9.9.9")
    monkeypatch.setattr(atlas, "PUBLICATION_VERSION", "v9.9.9")
    problems = atlas.composite_findings().problems
    assert len(problems) == 2
    assert "expected ('v9.9.9-111111',)" in problems[0]
    assert problems[1] == (
        "atlas/known-best/synthetic.svg was drawn for another version than v9.9.9; "
        "redraw it with --update-composites"
    )


def test_a_dateline_that_is_not_the_date_of_the_composites_data_fails(family: Family) -> None:
    """The dateline is the day of the data the cards show, not of a release.

    It used to be the release's first-published date, and stood at September 28 while
    the posters were redrawn with the results of the 29th and 30th.
    """
    identity = current()
    family.write(identity, dateline="Including new results (September 28, 2026)")
    assert identity.dateline == "Including new results (October 1, 2026)"
    assert atlas.composite_findings().problems == (
        (
            "atlas/known-best/synthetic.svg release is "
            "('Including new results (September 28, 2026)',); "
            "expected ('Including new results (October 1, 2026)',)"
        ),
    )


def test_a_composite_with_no_record_of_its_data_fails(family: Family) -> None:
    family.write(None)
    assert atlas.composite_findings().problems == (
        (
            "atlas/known-best/synthetic.svg records no data-revision or data-date: it does "
            "not say what data it was drawn from; redraw it with --update-composites"
        ),
    )


@pytest.mark.parametrize(
    ("identity", "problem"),
    [
        (
            atlas.CompositeIdentity("afd831", "2026-10-01"),
            "data-revision 'afd831' is not a full commit",
        ),
        (
            atlas.CompositeIdentity(EARLIER, "October 1, 2026"),
            "data-date 'October 1, 2026' is not an ISO date",
        ),
    ],
)
def test_a_malformed_record_fails(
    family: Family, identity: atlas.CompositeIdentity, problem: str
) -> None:
    family.write(identity, stamp="v0.4.2-afd831", dateline="Including new results")
    assert atlas.composite_findings().problems == (f"atlas/known-best/synthetic.svg {problem}",)


def test_exports_drawn_from_another_svg_fail_whether_or_not_it_trails(family: Family) -> None:
    """Trailing is about the data. Within a family every export is of this SVG."""
    family.write(trailing(), exports_of="<svg/>\n")
    assert atlas.composite_findings().problems == (
        "missing or stale atlas/known-best/synthetic.png preview receipt",
        "missing or stale atlas/known-best/synthetic@2x.png high-resolution export receipt",
        "missing or stale atlas/known-best/synthetic.pdf export receipt",
    )


def test_a_redraw_that_differs_fails_a_current_composite_and_lists_a_trailing_one(
    family: Family,
) -> None:
    """The whole `--check`'s half: the bytes a rebuild draws under the composite's record.

    The redraw is handed in, as the whole check hands in the rebuilt corpus. A current
    composite that is not what the rebuild draws fails, naming the card; a trailing one
    is listed the same way.
    """
    retained = family.write(current())
    redrawn = retained.replace(LOWER, "s(18) ≥ 4.68")
    assert atlas.composite_findings(lambda _canvas, _identity: retained).problems == ()
    assert atlas.composite_findings(lambda _canvas, _identity: redrawn).problems == (
        (
            "atlas/known-best/synthetic.svg is not what a rebuild draws under its own record, "
            "in 1 part: n=18"
        ),
    )

    retained = family.write(trailing())
    findings = atlas.composite_findings(
        lambda _canvas, _identity: retained.replace(LOWER, "s(18) ≥ 4.68")
    )
    assert findings.problems == ()
    assert findings.notes[-1].endswith("in 1 part: n=18")


def test_a_redraw_is_compared_part_by_part() -> None:
    """A difference names the frame or the cases it is in, not merely that there is one."""
    differences = atlas._redraw_differences  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    card = '  <g data-feature="packing-card" data-n="{n}">\n    <text>{text}</text>\n  </g>\n'
    drawing = "<svg>\n  <text>frame</text>\n" + "".join(
        card.format(n=n, text=f"s({n})") for n in (1, 2, 3)
    )
    assert differences(drawing, drawing) == []
    assert differences(drawing, drawing.replace("s(2)", "t(2)")) == ["n=2"]
    assert differences(drawing, drawing.replace("frame", "title")) == ["the frame"]
    assert differences(drawing, drawing.replace("s(1)", "t(1)").replace("s(3)", "t(3)")) == [
        "n=1",
        "n=3",
    ]
    shorter = "<svg>\n  <text>frame</text>\n" + card.format(n=1, text="s(1)")
    assert differences(drawing, shorter) == ["n=2", "n=3"]
    assert differences("<svg/>", "<svg />") == ["the frame"]


@pytest.fixture
def history(tmp_path: Path) -> tuple[Path, str, str, str]:
    """A scratch repository: a data commit, a later one, and a commit that is neither.

    Returns the repository, the first data commit, the last data commit and a commit
    that changed no data. The dates are fixed, each with its own offset from UTC.
    """
    repo = tmp_path / "origin"
    repo.mkdir()
    _git(repo, "init", "--quiet")
    first = _commit(repo, "packing/frontier/n-017.md", "first\n", "2026-09-28T23:30:00-07:00")
    last = _commit(repo, "packing/frontier/n-017.md", "second\n", "2026-10-01T09:00:00-07:00")
    prose = _commit(repo, "README.md", "prose\n", "2026-10-02T09:00:00-07:00")
    return repo, first, last, prose


def test_a_record_is_held_to_the_repository_where_git_can_answer(
    history: tuple[Path, str, str, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """The revision is a data commit in this history, and the date is that commit's.

    The date is the author's, on the author's calendar: 23:30 at seven hours behind UTC
    is the 28th, though it is already the 29th in UTC.
    """
    repo, first, last, prose = history
    monkeypatch.setattr(atlas, "REPOSITORY_ROOT", repo)
    check = atlas._identity_git_problems  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    name = "atlas/known-best/synthetic.svg"

    assert check(name, atlas.CompositeIdentity(first, "2026-09-28")) == []
    assert check(name, atlas.CompositeIdentity(last, "2026-10-01")) == []
    assert check(name, atlas.CompositeIdentity(first, "2026-09-29")) == [
        f"{name} dates its data 2026-09-29; {first[:12]} is dated 2026-09-28"
    ]
    assert check(name, atlas.CompositeIdentity(prose, "2026-10-02")) == [
        f"{name} names {prose[:12]} as its data, which did not change the data"
    ]
    assert check(name, atlas.CompositeIdentity("2" * 40, "2026-10-01")) == [
        f"{name} names {'2' * 12} as its data, which is not a commit here"
    ]

    _git(repo, "switch", "--quiet", "-c", "elsewhere", first)
    aside = _commit(repo, "packing/frontier/n-018.md", "aside\n", "2026-10-03T09:00:00+00:00")
    _git(repo, "switch", "--quiet", "-")
    assert check(name, atlas.CompositeIdentity(aside, "2026-10-03")) == [
        f"{name} names {aside[:12]} as its data, which is not in this history"
    ]


def test_a_shallow_clone_that_holds_the_commit_is_not_asked_for_its_history(
    history: tuple[Path, str, str, str], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The pull request's record sweeps run in a one-commit partial clone, which fetches
    the commit a composite names and has no ancestry to place it in (jlevy/squares#285,
    2026-10-01: both posters were reported as naming a commit not in this history). The
    date is still held; whether the commit is an ancestor, and whether it changed the
    data, are left to a clone with history."""
    repo, first, _, _ = history
    _git(repo, "config", "uploadpack.allowAnySHA1InWant", "true")
    clone = tmp_path / "clone"
    _git(tmp_path, "clone", "--quiet", "--depth", "1", repo.as_uri(), str(clone))
    _git(clone, "fetch", "--quiet", "--depth", "1", "origin", first)
    assert _git(clone, "rev-parse", "--is-shallow-repository") == "true"
    monkeypatch.setattr(atlas, "REPOSITORY_ROOT", clone)
    check = atlas._identity_git_problems  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    name = "atlas/known-best/synthetic.svg"
    assert check(name, atlas.CompositeIdentity(first, "2026-09-28")) == []
    assert check(name, atlas.CompositeIdentity(first, "2026-09-29")) == [
        f"{name} dates its data 2026-09-29; {first[:12]} is dated 2026-09-28"
    ]


def test_a_record_is_not_judged_where_git_cannot_answer(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A source tarball is a legitimate way to hold these files; nothing is reported."""
    monkeypatch.setattr(atlas, "REPOSITORY_ROOT", tmp_path)
    check = atlas._identity_git_problems  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    assert check("synthetic.svg", atlas.CompositeIdentity(EARLIER, "2026-10-01")) == []


def test_a_composite_is_drawn_only_from_data_the_pin_names(
    history: tuple[Path, str, str, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """A drawing is stamped with the pin, so the pin has to be the data in the tree.

    Three refusals, each a way the stamp would name data the cards do not show: the pin
    is behind git, the data has uncommitted changes, or there is no repository to ask.
    """
    repo, first, last, _prose = history
    monkeypatch.setattr(atlas, "REPOSITORY_ROOT", repo)

    monkeypatch.setattr(atlas, "DATA_REVISION", last)
    assert atlas.drawable_identity() == atlas.CompositeIdentity(last, "2026-10-01")

    monkeypatch.setattr(atlas, "DATA_REVISION", first)
    with pytest.raises(ValueError, match="release_pin --update"):
        atlas.drawable_identity()

    monkeypatch.setattr(atlas, "DATA_REVISION", last)
    (repo / "packing/frontier/n-017.md").write_text("uncommitted\n")
    with pytest.raises(ValueError, match="uncommitted changes"):
        atlas.drawable_identity()
    _git(repo, "checkout", "--quiet", "--", "packing/frontier/n-017.md")

    # A redrawn composite is not data, so drawing one does not block drawing the next.
    composite = repo / "packing/atlas/known-best/known-best-1-100.svg"
    composite.parent.mkdir(parents=True)
    composite.write_text("<svg/>\n")
    assert atlas.drawable_identity() == atlas.CompositeIdentity(last, "2026-10-01")

    monkeypatch.setattr(atlas, "REPOSITORY_ROOT", repo.parent)
    with pytest.raises(ValueError, match="stamped with the data commit it shows"):
        atlas.drawable_identity()


def test_the_metadata_a_composite_writes_is_the_metadata_the_pdf_reads() -> None:
    """One name for the data's date, in the module that writes it and the one that reads."""
    assert atlas.IDENTITY_DATE_KEY == render_composite_pdf.DATA_DATE_KEY
    text = (
        "<svg>\n  <metadata>\n"
        '    <sqpack:value name="data-date">2026-10-01</sqpack:value>\n'
        f'    <sqpack:value name="data-revision">{EARLIER}</sqpack:value>\n'
        '    <sqpack:value name="generated-by">a &amp; b</sqpack:value>\n'
        "  </metadata>\n"
        '  <sqpack:value name="data-date">outside the block</sqpack:value>\n</svg>\n'
    )
    assert render_composite_pdf.svg_metadata(text) == {
        "data-date": "2026-10-01",
        "data-revision": EARLIER,
        "generated-by": "a & b",
    }
    assert atlas.retained_identity(text) == atlas.CompositeIdentity(EARLIER, "2026-10-01")
    assert render_composite_pdf.svg_metadata("<svg/>") == {}


def test_the_builder_redraws_composites_only_when_asked() -> None:
    """`--update` is the data layer; the posters have a command of their own.

    `--restamp-only` is gone with the thing it did: nothing re-stamps a poster.
    """
    parser = atlas.parser()
    assert parser.parse_args(["--update-composites"]).update_composites
    assert parser.parse_args(["--check-composites"]).check_composites
    assert not parser.parse_args(["--update"]).update_composites
    with pytest.raises(SystemExit):
        parser.parse_args(["--restamp-only"])
    with pytest.raises(SystemExit):
        parser.parse_args(["--update", "--update-composites"])


def test_the_retained_composites_agree_with_their_own_records() -> None:
    """The two posters in the tree: each says what it was drawn from, and is held to it.

    This is `build_known_best_atlas --check-composites`, which the pull-request surface
    also runs inside the atlas step. It rebuilds nothing.
    """
    findings = atlas.composite_findings()
    assert findings.problems == ()
    for canvas in atlas.COMPOSITES:
        svg_text = canvas.svg_path.read_text(encoding="utf-8")
        identity = atlas.retained_identity(svg_text)
        root = ET.fromstring(svg_text)
        texts = {
            node.attrib.get("data-feature"): "".join(node.itertext())
            for node in root.iter("{http://www.w3.org/2000/svg}text")
            if node.attrib.get("data-feature") in {"release", "release-stamp"}
        }
        expected = {"release-stamp": identity.poster_stamp}
        if not canvas.information_in_corner:
            expected = {"release": identity.dateline, "release-stamp": identity.stamp}
        assert texts == expected
        assert identity.stamp.startswith(release.PUBLICATION_VERSION + "-")


def test_a_composite_pdf_is_dated_by_its_data_and_not_by_the_clock() -> None:
    """The PDF's properties give the day of the data, at noon UTC.

    cairo stamped the second the builder ran, to the local offset, so the properties of
    a poster said when someone last re-stamped it. Noon rather than midnight because a
    reader shows the instant in its own timezone, and midnight UTC is the evening before
    in California.
    """
    for canvas in atlas.COMPOSITES:
        stem = canvas.spec.stem
        day = render_composite_pdf.data_date(stem)
        stated = render_composite_pdf.pdf_date_text(day)
        pdf = render_composite_pdf.composite_pdf(stem).read_bytes()
        assert render_composite_pdf.pdf_dates(pdf) == {
            "CreationDate": stated,
            "ModDate": stated,
        }, stem
    assert render_composite_pdf.pdf_date_text(date(2026, 10, 1)) == "20261001120000Z"
    assert render_composite_pdf.pdf_dates(
        b"<< /CreationDate (D:20261001195544+00'00') /ModDate (20261001120000Z) >>"
    ) == {"CreationDate": "20261001195544+00'00'", "ModDate": "20261001120000Z"}
