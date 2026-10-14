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
import re
import struct
import subprocess
from collections.abc import Iterator
from datetime import date
from functools import cache
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
        printed_date: str | None = None,
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
                + (
                    '      <sqpack:value name="infographic-version">'
                    f"{identity.version}</sqpack:value>\n"
                    if identity.version != atlas.LEGACY_INFOGRAPHIC_VERSION
                    else ""
                )
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
            '  <text data-feature="release-stamp">'
            f"{stamp or f'{printed_date or shown.formatted_date} · {shown.stamp}'}</text>\n"
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
        render_composite_pdf.composite_pdf(self.canvas.spec.stem).write_bytes(
            b"%PDF-1.5\n%%EOF\n"
            + (
                b"%"
                + render_composite_pdf.PDF_VERSION_KEY
                + b": "
                + shown.version.encode("ascii")
                + b"\n"
                if shown.version != atlas.LEGACY_INFOGRAPHIC_VERSION
                else b""
            )
            + b"%"
            + render_composite_pdf.PDF_SOURCE_KEY
            + b": "
            + digest.encode("ascii")
            + b"\n"
        )
        return svg_text


@pytest.fixture
def family(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Family]:
    """A synthetic composite family the builder reads in place of the retained two.

    The figure record states one case, and git is not asked about the synthetic data
    revisions, which are no commits; `_identity_git_problems` has tests of its own.
    """
    packing = tmp_path / "packing"
    atlas_root = packing / "atlas/known-best"
    atlas_root.mkdir(parents=True)
    credit_name = "credit-attributions.json"
    (atlas_root / credit_name).write_bytes((atlas.ATLAS_ROOT / credit_name).read_bytes())
    attributions = atlas._print_attributions  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    attributions.cache_clear()
    monkeypatch.setattr(atlas, "ROOT", packing)
    monkeypatch.setattr(atlas, "ATLAS_ROOT", atlas_root)
    monkeypatch.setattr(render_composite_pdf, "ATLAS_ROOT", atlas_root)
    published = release.component_version("infographics")
    monkeypatch.setattr(release, "published_infographic_version", lambda _repo: published)
    monkeypatch.setattr(atlas, "_published_composite_text", lambda path: path.read_text())
    monkeypatch.setattr(
        atlas,
        "_figure_entries",
        lambda: {18: {"side": {"display": SIDE}, "lower": {"display": LOWER, "shown": True}}},
    )
    monkeypatch.setattr(atlas, "_identity_git_problems", lambda _path, _identity: [])
    made = Family(tmp_path)
    monkeypatch.setattr(atlas, "COMPOSITES", (made.canvas,))
    try:
        yield made
    finally:
        attributions.cache_clear()


def current() -> atlas.CompositeIdentity:
    return atlas.CompositeIdentity(
        release.DATA_REVISION, "2026-10-01", release.component_version("infographics")
    )


def trailing() -> atlas.CompositeIdentity:
    return atlas.CompositeIdentity(
        EARLIER, "2026-09-28", release.component_version("infographics")
    )


def test_a_composite_that_shows_the_pinned_data_and_agrees_with_it_passes(
    family: Family,
) -> None:
    family.write(current())
    findings = atlas.composite_findings()
    assert findings.problems == ()
    assert findings.notes == (
        (
            f"atlas/known-best/synthetic.svg shows {release.INFOGRAPHIC_EDITION}, data of "
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
    stamp = release.infographic_edition_at(EARLIER)
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
            f"expected ({identity.poster_stamp!r},)"
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
    monkeypatch.setattr(release, "INFOGRAPHIC_VERSION", "v9.9.9")
    monkeypatch.setattr(atlas, "INFOGRAPHIC_VERSION", "v9.9.9")
    problems = atlas.composite_findings().problems
    assert len(problems) == 1
    assert problems[0] == (
        "atlas/known-best/synthetic.svg was drawn for another version than v9.9.9; "
        "redraw it with --update-composites after cutting the infographic edition"
    )


def test_a_dateline_that_is_not_the_date_of_the_composites_data_fails(family: Family) -> None:
    """The dateline is the day of the data the cards show, not of a release.

    It used to be the release's first-published date, and stood at September 28 while
    the posters were redrawn with the results of the 29th and 30th.
    """
    identity = current()
    family.write(identity, printed_date="September 28, 2026")
    assert identity.dateline == "Including new results (October 1, 2026)"
    assert atlas.composite_findings().problems == (
        (
            "atlas/known-best/synthetic.svg release-stamp is "
            f"('September 28, 2026 · {identity.stamp}',); "
            f"expected ({identity.poster_stamp!r},)"
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
    family.write(identity, stamp="v0.4.2-afd831")
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
    assert atlas.drawable_identity() == atlas.CompositeIdentity(
        last, "2026-10-01", atlas.INFOGRAPHIC_VERSION
    )

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
    assert atlas.drawable_identity() == atlas.CompositeIdentity(
        last, "2026-10-01", atlas.INFOGRAPHIC_VERSION
    )

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
        assert texts == expected
        assert identity.stamp.startswith(release.INFOGRAPHIC_VERSION + "-")


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


def test_a_site_cut_leaves_the_retained_infographic_edition_valid(
    family: Family,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    family.write(current())
    monkeypatch.setattr(release, "PUBLICATION_VERSION", "v0.6.0")
    assert atlas.composite_findings().problems == ()


def test_the_complete_pair_refuses_mixed_versions(
    family: Family,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    second = Family(family.root)
    second.canvas = atlas.CompositeCanvas(
        CompositeSpec(first_n=18, last_n=18, columns=1, stem="synthetic-second")
    )
    family.write(current())
    version = release.successor_version(current().version, "patch")
    second.write(atlas.CompositeIdentity(release.DATA_REVISION, "2026-10-01", version))
    monkeypatch.setattr(atlas, "COMPOSITES", (family.canvas, second.canvas))
    assert (
        f"infographic family has mixed versions: {current().version}, {version}"
        in atlas.composite_findings().problems
    )


@pytest.mark.parametrize("missing", ["svg", "png", "pdf"])
def test_each_advertised_family_output_is_required(family: Family, missing: str) -> None:
    family.write(current())
    path = {
        "svg": family.canvas.svg_path,
        "png": family.canvas.rasters[0].path,
        "pdf": render_composite_pdf.composite_pdf("synthetic"),
    }[missing]
    path.unlink()
    assert any(
        path.name in problem and "missing" in problem
        for problem in atlas.composite_findings().problems
    )


def test_a_changed_redraw_is_refused_before_any_existing_edition_is_overwritten(
    family: Family,
) -> None:
    svg = family.write(current())
    paths = [
        family.canvas.svg_path,
        *(export.path for export in family.canvas.rasters),
        render_composite_pdf.composite_pdf("synthetic"),
    ]
    retained = {path: path.read_bytes() for path in paths}
    atlas.validate_composite_redraws([(family.canvas, svg)], current())
    with pytest.raises(ValueError, match="requires the complete pair"):
        atlas.validate_composite_redraws([], current())
    with pytest.raises(ValueError, match="would change under existing infographic version"):
        atlas.validate_composite_redraws(
            [(family.canvas, svg.replace(LOWER, "3.826"))], current()
        )
    assert {path: path.read_bytes() for path in paths} == retained


def test_a_new_family_revision_uses_a_recorded_successor_on_both_graphics(
    family: Family,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    previous = release.component_version("infographics")
    before = family.write(current())
    version = release.successor_version(previous, "patch")
    revised = atlas.CompositeIdentity(release.DATA_REVISION, "2026-10-01", version)
    after = family.write(revised)
    family.write(current())
    entry = release.PublicationHistoryEntry(version, "October 13, 2026", "Refresh the pair.")
    monkeypatch.setattr(release, "INFOGRAPHIC_HISTORY", (entry, *release.INFOGRAPHIC_HISTORY))
    with pytest.raises(ValueError, match="needs a release-impact decision"):
        atlas.validate_composite_redraws([(family.canvas, after)], revised)
    decision = release.ReleaseImpactDecision(
        "infographics", previous, version, "patch", "Refresh the pair."
    )
    monkeypatch.setattr(release, "RELEASE_IMPACTS", (decision, *release.RELEASE_IMPACTS))
    atlas.validate_composite_redraws([(family.canvas, after)], revised)
    assert family.canvas.svg_path.read_text() == before
    assert atlas.retained_identity(after).version == version
    with pytest.raises(ValueError, match="mixed infographic redraw identity"):
        atlas.validate_composite_redraws([(family.canvas, before)], revised)


def test_a_successor_without_version_metadata_is_refused(family: Family) -> None:
    identity = atlas.CompositeIdentity(release.DATA_REVISION, "2026-10-01", "v0.5.1")
    svg = family.write(identity)
    svg = re.sub(
        r'      <sqpack:value name="infographic-version">[^<]+</sqpack:value>\n', "", svg
    )
    family.canvas.svg_path.write_text(svg)
    assert any(
        "release-stamp" in problem and "expected" in problem
        for problem in atlas.composite_findings().problems
    )


def test_an_export_correction_requires_a_successor_even_when_the_svg_is_identical(
    family: Family,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    svg = family.write(current())
    export = family.canvas.rasters[0]
    retained = export.path.read_bytes()
    export.path.write_bytes(b"previously published incorrect raster")
    monkeypatch.setattr(atlas, "png_export_bytes", lambda *_args, **_kwargs: retained)
    update = atlas._update_png_export  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    with pytest.raises(ValueError, match="before correcting the export"):
        update(export, svg, preserve_edition=True)
    assert export.path.read_bytes() == b"previously published incorrect raster"
    update(export, svg, preserve_edition=False)
    assert export.path.read_bytes() == retained


def test_standalone_pdf_correction_cannot_replace_an_existing_edition(
    family: Family,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    family.write(current())
    pdf = render_composite_pdf.composite_pdf("synthetic")
    original = (
        b"%PDF-1.5\npreviously published without a receipt\n%%EOF\n%"
        + render_composite_pdf.PDF_VERSION_KEY
        + b": "
        + current().version.encode("ascii")
        + b"\n"
    )
    pdf.write_bytes(original)
    monkeypatch.setattr(
        render_composite_pdf, "render_pdf_bytes", lambda _stem: b"%PDF-1.5\ncorrected\n%%EOF\n"
    )
    with pytest.raises(ValueError, match="existing infographic version"):
        render_composite_pdf.update("synthetic")
    assert pdf.read_bytes() == original
    assert render_composite_pdf.main(["--update", "--stem", "synthetic"]) == 1
    assert "existing infographic version" in capsys.readouterr().err
    assert pdf.read_bytes() == original


@pytest.fixture
def cut_pair(
    family: Family,
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[atlas.CompositeIdentity, list[tuple[atlas.CompositeCanvas, str]], dict[Path, bytes]]:
    second = Family(family.root)
    second.canvas = atlas.CompositeCanvas(
        CompositeSpec(first_n=18, last_n=18, columns=1, stem="synthetic-second")
    )
    previous = release.component_version("infographics")
    version = release.successor_version(previous, "patch")
    identity = atlas.CompositeIdentity(release.DATA_REVISION, "2026-10-01", version)
    drawings = []
    for graphic in (family, second):
        drawings.append((graphic.canvas, graphic.write(identity)))
        graphic.write(current())
    monkeypatch.setattr(atlas, "COMPOSITES", (family.canvas, second.canvas))
    monkeypatch.setattr(atlas, "INFOGRAPHIC_VERSION", version)
    entry = release.PublicationHistoryEntry(
        version, "October 13, 2026", "Refresh both graphics."
    )
    decision = release.ReleaseImpactDecision(
        "infographics", previous, version, "patch", "Refresh both graphics."
    )
    monkeypatch.setattr(release, "INFOGRAPHIC_HISTORY", (entry, *release.INFOGRAPHIC_HISTORY))
    monkeypatch.setattr(release, "RELEASE_IMPACTS", (decision, *release.RELEASE_IMPACTS))
    monkeypatch.setattr(atlas, "png_export_bytes", _synthetic_png)
    monkeypatch.setattr(
        render_composite_pdf,
        "render_svg_pdf_bytes",
        _synthetic_pdf,
    )
    paths = [
        path
        for canvas, _svg in drawings
        for path in (
            canvas.svg_path,
            *(export.path for export in canvas.rasters),
            render_composite_pdf.composite_pdf(canvas.spec.stem),
        )
    ]
    return identity, drawings, {path: path.read_bytes() for path in paths}


def _synthetic_pdf(svg_text: str) -> bytes:
    stated = render_composite_pdf.pdf_date_text(render_composite_pdf.svg_data_date(svg_text))
    return (
        f"%PDF-1.5\n/CreationDate ({stated})\n/ModDate ({stated})\nprepared artwork\n%%EOF\n"
    ).encode("ascii")


def _synthetic_png(
    export: atlas.RasterExport, svg_text: str, *, full_png: bytes | None = None
) -> bytes:
    del full_png
    header = struct.pack(">IIBBBBB", export.width, export.height, 8, 2, 0, 0, 0)
    blank = (
        atlas.PNG_SIGNATURE
        + atlas._png_chunk(b"IHDR", header)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
        + atlas._png_chunk(b"IEND", b"")  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    )
    digest = hashlib.sha256(svg_text.encode("utf-8")).hexdigest()
    return atlas._png_with_summary_source(blank, digest)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001


@pytest.mark.parametrize(
    ("producer", "failure_index"), [("png", 1), ("png", 3), ("pdf", 1), ("pdf", 2)]
)
def test_producer_failure_leaves_the_complete_old_family_and_retry_keeps_the_cut_version(
    cut_pair: tuple[
        atlas.CompositeIdentity, list[tuple[atlas.CompositeCanvas, str]], dict[Path, bytes]
    ],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    producer: str,
    failure_index: int,
) -> None:
    identity, drawings, old = cut_pair
    stage = tmp_path / "staged-family"
    calls = 0
    armed = True

    def failure() -> None:
        nonlocal calls
        calls += 1
        # Every vector is staged already, but neither live SVG has moved.
        assert all((stage / canvas.svg_path.name).is_file() for canvas, _svg in drawings)
        assert {path: path.read_bytes() for path in old} == old
        if armed and calls == failure_index:
            raise OSError("injected producer failure")

    if producer == "png":

        def png(
            export: atlas.RasterExport, svg: str, *, full_png: bytes | None = None
        ) -> bytes:
            failure()
            return _synthetic_png(export, svg, full_png=full_png)

        monkeypatch.setattr(atlas, "png_export_bytes", png)
    else:

        def pdf(_svg: str) -> bytes:
            failure()
            return _synthetic_pdf(_svg)

        monkeypatch.setattr(render_composite_pdf, "render_svg_pdf_bytes", pdf)
    with pytest.raises(OSError, match="injected producer failure"):
        atlas.staged_composite_family(drawings, identity, stage)
    assert {path: path.read_bytes() for path in old} == old
    armed = False
    staged = atlas.staged_composite_family(drawings, identity, stage)
    assert set(staged) == set(old)
    assert {path: path.read_bytes() for path in old} == old
    atlas.promote_composite_family(staged, stage)
    assert atlas.composite_findings().problems == ()
    assert all(
        atlas.retained_identity(canvas.svg_path.read_text()).version == identity.version
        for canvas, _svg in drawings
    )
    assert all(
        render_composite_pdf.pdf_version(
            render_composite_pdf.composite_pdf(canvas.spec.stem).read_bytes()
        )
        == identity.version
        for canvas, _svg in drawings
    )


@pytest.mark.parametrize("failure_index", [1, 3, 8])
def test_promotion_failure_restores_every_old_final_and_allows_retry(
    cut_pair: tuple[
        atlas.CompositeIdentity, list[tuple[atlas.CompositeCanvas, str]], dict[Path, bytes]
    ],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure_index: int,
) -> None:
    identity, drawings, old = cut_pair
    stage = tmp_path / "staged-family"
    staged = atlas.staged_composite_family(drawings, identity, stage)
    promote = atlas._promote_composite_file  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    calls = 0

    def fail_after_commit(destination: Path, source: Path) -> None:
        nonlocal calls
        promote(destination, source)
        if source.parent.name != "backups":
            calls += 1
            if calls == failure_index:
                raise OSError("injected promotion failure after commit")

    monkeypatch.setattr(atlas, "_promote_composite_file", fail_after_commit)
    with pytest.raises(OSError, match="injected promotion failure"):
        atlas.promote_composite_family(staged, stage)
    assert {path: path.read_bytes() for path in old} == old
    monkeypatch.setattr(atlas, "_promote_composite_file", promote)
    # Retry staging from the same held edition must see the old family, not new SVGs.
    staged = atlas.staged_composite_family(drawings, identity, stage)
    atlas.promote_composite_family(staged, stage)
    assert atlas.composite_findings().problems == ()


def test_invalid_staged_export_receipt_blocks_all_promotion(
    cut_pair: tuple[
        atlas.CompositeIdentity, list[tuple[atlas.CompositeCanvas, str]], dict[Path, bytes]
    ],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    identity, drawings, old = cut_pair
    monkeypatch.setattr(
        atlas,
        "png_export_bytes",
        lambda export, _svg, **_kwargs: _synthetic_png(export, "wrong source"),
    )
    with pytest.raises(ValueError, match="receipt"):
        atlas.staged_composite_family(drawings, identity, tmp_path / "stage")
    assert {path: path.read_bytes() for path in old} == old


def test_same_edition_pdf_with_valid_receipt_is_reused_without_redrawing(
    family: Family,
) -> None:
    svg = family.write(current())
    pdf = render_composite_pdf.composite_pdf("synthetic")
    before = pdf.read_bytes()

    def fail_if_redrawn() -> bytes:
        pytest.fail("a valid same-edition PDF must be retained byte-for-byte")

    assert render_composite_pdf.prepared_pdf(svg, before, render=fail_if_redrawn) == before
    assert pdf.read_bytes() == before


@pytest.mark.parametrize("arguments", [["--update"], ["--update", "--stem", "synthetic"]])
def test_standalone_published_pdf_update_uses_the_complete_staged_family(
    monkeypatch: pytest.MonkeyPatch,
    arguments: list[str],
) -> None:
    calls = []
    monkeypatch.setattr(
        render_composite_pdf, "published_stems", lambda: ("synthetic", "second")
    )
    monkeypatch.setattr(atlas, "update_composites", lambda: calls.append("complete family"))
    assert render_composite_pdf.main(arguments) == 0
    assert calls == ["complete family"]


def test_the_update_entrypoint_recovers_from_producer_failure_without_rebumping(
    cut_pair: tuple[
        atlas.CompositeIdentity, list[tuple[atlas.CompositeCanvas, str]], dict[Path, bytes]
    ],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    identity, drawings, old = cut_pair
    svg_by_path = {canvas.svg_path: svg for canvas, svg in drawings}
    monkeypatch.setattr(atlas, "drawable_identity", lambda: identity)
    monkeypatch.setattr(atlas.build_composite_figure_data, "check", lambda: None)
    entries = cache(atlas._figure_entries)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    monkeypatch.setattr(atlas, "_figure_entries", entries)
    monkeypatch.setattr(atlas, "_retained_problems", lambda: ([], None))
    monkeypatch.setattr(atlas, "retained_cases", lambda _numbers: [])
    monkeypatch.setattr(atlas, "_cards", lambda _cases, _canvas: [])
    monkeypatch.setattr(
        atlas,
        "render_known_best_summary_svg",
        lambda _cards, canvas, _identity: svg_by_path[canvas.svg_path],
    )
    stages: list[Path] = []

    def staging_directory(**_kwargs: str) -> str:
        path = tmp_path / f"publication-stage-{len(stages)}"
        path.mkdir()
        stages.append(path)
        return str(path)

    monkeypatch.setattr(atlas, "mkdtemp", staging_directory)

    def failing_pdf(_svg: str) -> bytes:
        assert {path: path.read_bytes() for path in old} == old
        raise OSError("injected PDF production failure")

    monkeypatch.setattr(render_composite_pdf, "render_svg_pdf_bytes", failing_pdf)
    with pytest.raises(OSError, match="injected PDF production failure"):
        atlas.update_composites()
    assert {path: path.read_bytes() for path in old} == old
    assert not stages[0].exists()
    monkeypatch.setattr(
        render_composite_pdf,
        "render_svg_pdf_bytes",
        _synthetic_pdf,
    )
    atlas.update_composites()
    assert atlas.composite_findings().problems == ()
    assert not stages[1].exists()
    completed = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in old}
    atlas.update_composites()
    assert {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in old} == completed
    assert not stages[2].exists()
    assert release.component_version("infographics") == identity.version


def test_a_successor_pdf_cannot_be_corrected_again_under_the_same_version(
    cut_pair: tuple[
        atlas.CompositeIdentity, list[tuple[atlas.CompositeCanvas, str]], dict[Path, bytes]
    ],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    identity, drawings, _old = cut_pair
    stage = tmp_path / "stage"
    atlas.promote_composite_family(
        atlas.staged_composite_family(drawings, identity, stage), stage
    )
    monkeypatch.setattr(
        release, "published_infographic_version", lambda _repo: identity.version
    )
    pdf = render_composite_pdf.composite_pdf("synthetic")
    # Once main publishes the successor, losing a receipt does not reopen its edition.
    original = pdf.read_bytes().split(b"\n%" + render_composite_pdf.PDF_SOURCE_KEY, 1)[0]
    pdf.write_bytes(original)
    assert render_composite_pdf.pdf_version(original) == identity.version
    with pytest.raises(ValueError, match="existing infographic version"):
        render_composite_pdf.update("synthetic")
    assert pdf.read_bytes() == original


def test_an_incomplete_staging_map_cannot_be_promoted(
    cut_pair: tuple[
        atlas.CompositeIdentity, list[tuple[atlas.CompositeCanvas, str]], dict[Path, bytes]
    ],
    tmp_path: Path,
) -> None:
    identity, drawings, old = cut_pair
    stage = tmp_path / "stage"
    staged = atlas.staged_composite_family(drawings, identity, stage)
    staged.pop(render_composite_pdf.composite_pdf("synthetic"))
    with pytest.raises(ValueError, match="every configured SVG, PNG and PDF"):
        atlas.promote_composite_family(staged, stage)
    assert {path: path.read_bytes() for path in old} == old


def test_wrong_staged_pdf_dates_leave_every_final_untouched(
    cut_pair: tuple[
        atlas.CompositeIdentity, list[tuple[atlas.CompositeCanvas, str]], dict[Path, bytes]
    ],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    identity, drawings, old = cut_pair
    monkeypatch.setattr(
        render_composite_pdf,
        "render_svg_pdf_bytes",
        lambda svg: _synthetic_pdf(svg).replace(b"20261001", b"20261002"),
    )
    with pytest.raises(ValueError, match="PDF dates other than its SVG"):
        atlas.staged_composite_family(drawings, identity, tmp_path / "stage")
    assert {path: path.read_bytes() for path in old} == old


def test_pdf_producer_renders_prepared_svg_without_reading_retained_artwork(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    svg = (
        f'<svg {SVG_NAMESPACES} width="10" height="10">'
        '<metadata><sqpack:profile version="8">'
        '<sqpack:value name="data-date">2026-10-01</sqpack:value>'
        '</sqpack:profile></metadata><rect width="10" height="10" fill="red"/></svg>'
    )

    def forbid_retained_read(_stem: str) -> Path:
        pytest.fail("the prepared SVG producer cannot read retained artwork")

    monkeypatch.setattr(render_composite_pdf, "composite_svg", forbid_retained_read)
    pdf = render_composite_pdf.render_svg_pdf_bytes(svg)
    assert pdf.startswith(render_composite_pdf.PDF_SIGNATURE)
    assert render_composite_pdf.pdf_dates(pdf) == {
        "CreationDate": "20261001120000Z",
        "ModDate": "20261001120000Z",
    }


def test_rollback_failure_retains_old_bytes_at_the_reported_backup_path(
    cut_pair: tuple[
        atlas.CompositeIdentity, list[tuple[atlas.CompositeCanvas, str]], dict[Path, bytes]
    ],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    identity, drawings, old = cut_pair
    stage = tmp_path / "stage"
    staged = atlas.staged_composite_family(drawings, identity, stage)
    promote = atlas._promote_composite_file  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001

    def fail_promotion_and_rollback(destination: Path, source: Path) -> None:
        if source.parent.name == "backups":
            raise OSError("rollback denied")
        promote(destination, source)
        raise OSError("promotion failed after commit")

    monkeypatch.setattr(atlas, "_promote_composite_file", fail_promotion_and_rollback)
    with pytest.raises(atlas.CompositePromotionError, match=str(stage / "backups")):
        atlas.promote_composite_family(staged, stage)
    assert (stage / "backups/0").read_bytes() == old[drawings[0][0].svg_path]
    assert all(
        (stage / f"backups/{index}").read_bytes() == old[path]
        for index, path in enumerate(staged)
    )


@pytest.mark.parametrize(
    "marker",
    [
        b"v0.5.1-invalid",
        b"Draft v0.5.1",
        b"v01.5.1",
        b"v0.5.1\n%sqpack-infographic-version: v0.5.1",
    ],
)
def test_malformed_or_ambiguous_pdf_editions_do_not_fall_back_to_the_legacy_baseline(
    marker: bytes,
) -> None:
    pdf = b"%PDF-1.5\n%sqpack-infographic-version: " + marker + b"\n%%EOF\n"
    with pytest.raises(ValueError, match=r"is not a version|unambiguous infographic edition"):
        render_composite_pdf.pdf_version(pdf)


def _candidate_guard_cut(monkeypatch: pytest.MonkeyPatch) -> tuple[str, str]:
    published = release.RELEASE_POLICY_BASELINES["infographics"]
    candidate = release.successor_version(published, "minor")
    history = (
        release.PublicationHistoryEntry(candidate, "October 14, 2026", "A candidate redesign."),
        release.PublicationHistoryEntry(published, "October 2, 2026", "Published baseline."),
    )
    decision = release.ReleaseImpactDecision(
        "infographics", published, candidate, "minor", "A candidate redesign."
    )
    monkeypatch.setattr(release, "INFOGRAPHIC_HISTORY", history)
    monkeypatch.setattr(
        release,
        "RELEASE_IMPACTS",
        (
            decision,
            *(item for item in release.RELEASE_IMPACTS if item.component != "infographics"),
        ),
    )
    monkeypatch.setattr(release, "published_infographic_version", lambda _repo: published)
    return published, candidate


def _guard_svg(version: str, body: str) -> str:
    return (
        f"<svg {SVG_NAMESPACES}><metadata>"
        '<sqpack:profile version="8">'
        '<sqpack:value name="data-date">2026-10-01</sqpack:value>'
        f'<sqpack:value name="data-revision">{release.DATA_REVISION}</sqpack:value>'
        f'<sqpack:value name="infographic-version">{version}</sqpack:value>'
        f"</sqpack:profile></metadata><text>{body}</text></svg>"
    )


def test_unpublished_pair_can_be_corrected_at_its_selected_edition_but_main_cannot(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    published, candidate = _candidate_guard_cut(monkeypatch)
    canvases = [
        atlas.CompositeCanvas(CompositeSpec(first_n=18, last_n=18, columns=1, stem=stem))
        for stem in ("guard-one", "guard-two")
    ]
    files = {canvas.svg_path: _guard_svg(published, "Published") for canvas in canvases}
    main = dict(files)
    monkeypatch.setattr(atlas, "resolved_composites", lambda: tuple(canvases))
    monkeypatch.setattr(Path, "is_file", lambda path: path in files)
    monkeypatch.setattr(Path, "read_text", lambda path, **_kwargs: files[path])
    monkeypatch.setattr(atlas, "_published_composite_text", lambda path: main[path])
    identity = atlas.CompositeIdentity(release.DATA_REVISION, "2026-10-01", candidate)
    first = [(canvas, _guard_svg(candidate, "First candidate")) for canvas in canvases]
    atlas.validate_composite_redraws(first, identity)
    files.update((canvas.svg_path, svg) for canvas, svg in first)
    atlas.validate_composite_redraws(first, identity)
    corrected = [(canvas, _guard_svg(candidate, "Review correction")) for canvas in canvases]
    atlas.validate_composite_redraws(corrected, identity)
    assert all(atlas.retained_identity(svg).version == candidate for _canvas, svg in corrected)
    with pytest.raises(ValueError, match="complete pair"):
        atlas.validate_composite_redraws(corrected[:1], identity)
    files[canvases[0].svg_path] = _guard_svg("v0.4.2", "Unrelated retained edition")
    with pytest.raises(ValueError, match="neither main nor its selected successor"):
        atlas.validate_composite_redraws(corrected, identity)
    files.update((canvas.svg_path, svg) for canvas, svg in first)
    main.update(files)
    monkeypatch.setattr(release, "published_infographic_version", lambda _repo: candidate)
    atlas.validate_composite_redraws(first, identity)
    with pytest.raises(ValueError, match="existing infographic version"):
        atlas.validate_composite_redraws(corrected, identity)
    # Local edits cannot redefine what main already published.
    files.update((canvas.svg_path, svg) for canvas, svg in corrected)
    with pytest.raises(ValueError, match="existing infographic version"):
        atlas.validate_composite_redraws(corrected, identity)


def test_unpublished_pdf_corrections_keep_one_cut_and_published_corrections_refuse(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    published, candidate = _candidate_guard_cut(monkeypatch)
    old = (
        b"%PDF-1.5\npublished\n%%EOF\n%"
        + render_composite_pdf.PDF_VERSION_KEY
        + b": "
        + published.encode()
        + b"\n"
    )
    first_svg = _guard_svg(candidate, "First candidate")
    first = render_composite_pdf.prepared_pdf(
        first_svg, old, render=lambda: b"%PDF-1.5\nfirst candidate\n%%EOF\n"
    )
    assert render_composite_pdf.pdf_version(first) == candidate

    def must_not_render() -> bytes:
        raise AssertionError("an identical retry must retain its PDF")

    assert render_composite_pdf.prepared_pdf(first_svg, first, render=must_not_render) == first
    corrected_svg = _guard_svg(candidate, "Review correction")
    corrected = render_composite_pdf.prepared_pdf(
        corrected_svg, first, render=lambda: b"%PDF-1.5\nreview correction\n%%EOF\n"
    )
    assert corrected != first
    assert render_composite_pdf.pdf_version(corrected) == candidate
    assert (
        render_composite_pdf.pdf_receipt(corrected)
        == hashlib.sha256(corrected_svg.encode()).hexdigest()
    )
    unrelated = old.replace(published.encode(), b"v0.4.2")
    with pytest.raises(ValueError, match="neither main nor its selected successor"):
        render_composite_pdf.prepared_pdf(corrected_svg, unrelated, render=must_not_render)
    monkeypatch.setattr(release, "published_infographic_version", lambda _repo: candidate)
    with pytest.raises(ValueError, match="existing infographic version"):
        render_composite_pdf.prepared_pdf(
            corrected_svg, first, render=lambda: b"%PDF-1.5\nreview correction\n%%EOF\n"
        )
