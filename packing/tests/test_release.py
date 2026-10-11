"""One spelling of the version, in one place, and the pin that keeps it naming the data.

The atlas footer and the explainer's credits each used to compose the stamp from the
parts, in two files and two languages, and the page named its build commit where the
atlas named a pinned one. Hand-assembled spellings of one fact are how they come to
disagree. What is pinned here is the shape, the single source, and the drift check that
holds the pinned data revision to git. (The explainer's credits print the paper's own
version since 2026-10-02; the stamp is the site's and the posters'.)

The site's version history is held to two rules of its own: it only grows, back to the
first edition, and each edition is dated by when it was first published rather than when
its label was first written down. The papers' own versions are held beside it: a paper's
history lists the editions in which that paper changed, at the numbers and dates they
were published under, and no paper's version carries the site's edition or the data hash.

A re-pin is one line and rebuilds nothing (`devtools.release_pin`, with tests of its
own). The posters and the films are stamped when they are drawn, with `edition_at` their
own data revision, and `tests/test_known_best_composites.py` holds a poster to that.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

from sqpack.release import (
    COMPOSITES_MAY_TRAIL,
    DATA_REVISION,
    DATA_REVISION_LENGTH,
    EXPLAINER_FIRST_PUBLISHED,
    EXPLAINER_HISTORY,
    EXPLAINER_VERSION,
    FIRST_PUBLISHED,
    OPTIMALITY_REVIEW_EDITION,
    OPTIMALITY_REVIEW_VERSION,
    PUBLICATION_DATE,
    PUBLICATION_EDITION,
    PUBLICATION_HISTORY,
    PUBLICATION_REVISION,
    PUBLICATION_STAMP,
    PUBLICATION_STATUS,
    PUBLICATION_VERSION,
    PublicationHistoryEntry,
    commit_date,
    data_pathspec,
    data_revision,
    data_version,
    edition_at,
    last_change_date,
)

REPO = Path(__file__).resolve().parents[2]

#: `v0.4.1-f5e113`: a semver core, a hyphen, and six characters of the data commit.
STAMP = re.compile(rf"v\d+\.\d+\.\d+-[0-9a-f]{{{DATA_REVISION_LENGTH}}}")

#: The identity and settings a scratch repository commits under, so the user's global
#: signing and hooks cannot reach it.
SCRATCH_GIT = (
    "-c",
    "user.name=release test",
    "-c",
    "user.email=release-test@example.invalid",
    "-c",
    "commit.gpgsign=false",
    "-c",
    "core.hooksPath=/dev/null",
)


def _git(repo: Path, *arguments: str) -> str:
    done = subprocess.run(
        ("git", "-C", str(repo), *SCRATCH_GIT, *arguments),
        capture_output=True,
        text=True,
        check=True,
    )
    return done.stdout.strip()


def _commit(repo: Path, path: str, text: str, when: str | None = None) -> str:
    """Write `path` under `repo`, commit it alone, and return the commit's hash.

    `when` is the commit's author date, with its offset, as `--date` takes it.
    """
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)
    _git(repo, "add", path)
    dated = () if when is None else (f"--date={when}",)
    _git(repo, "commit", "--quiet", "-m", f"touch {path}", *dated)
    return _git(repo, "rev-parse", "HEAD")


@pytest.fixture
def history(tmp_path: Path) -> tuple[Path, str]:
    """A scratch repository whose last data commit is followed by three that are not.

    One commit redraws an atlas composite and one edits a video spike, which the data
    paths exclude; one changes a file outside them. Returns the repository and the hash
    of its last data commit.
    """
    repo = tmp_path / "origin"
    repo.mkdir()
    _git(repo, "init", "--quiet")
    _commit(repo, "packing/frontier/n-017.md", "first\n")
    data = _commit(repo, "packing/frontier/n-017.md", "second\n")
    _commit(repo, "packing/atlas/known-best/known-best-1-100.svg", "<svg/>\n")
    _commit(repo, "packing/atlas/known-best/video/spikes/player.js", "play();\n")
    _commit(repo, "README.md", "prose\n")
    return repo, data


def _version(entry: PublicationHistoryEntry) -> tuple[int, ...]:
    return tuple(int(part) for part in entry.version.removeprefix("v").split("."))


def test_the_history_keeps_every_edition_back_to_the_first() -> None:
    """An edition that was published stays in the history, and the first one most of all.

    This test used to say the history was "the two retained editions", which is the rule
    that let adding v0.4.1 drop v0.3.0 -- the proof of s(11) >= 381/100 the publication
    began with -- and pass. The history now only grows: every edition ever published is
    listed, newest first, and the oldest is the 381/100 edition. A new edition goes on the
    front; nothing comes off the back.
    """
    versions = [entry.version for entry in PUBLICATION_HISTORY]
    assert {"v0.4.2", "v0.4.1", "v0.4.0", "v0.3.0"} <= set(versions)
    assert len(set(versions)) == len(versions)
    assert [_version(e) for e in PUBLICATION_HISTORY] == sorted(
        (_version(e) for e in PUBLICATION_HISTORY), reverse=True
    )
    first = PUBLICATION_HISTORY[-1]
    assert first.version == "v0.3.0"
    assert "381/100" in first.result_scope
    assert all("weak" not in entry.result_scope.lower() for entry in PUBLICATION_HISTORY)
    assert PUBLICATION_HISTORY[0].version == PUBLICATION_VERSION


def test_each_edition_is_dated_by_when_it_was_first_published() -> None:
    """The dates are first publication, read from the Pages deployments, not labelling.

    Two of the three differ from the old label dates, in opposite directions: v0.3.0 went
    live on September 5 and was named on September 8; v0.4.0 was named on a branch on
    September 10 and went live on September 13. The deployments behind each are in the
    comment on `PUBLICATION_HISTORY`.
    """
    dated = {entry.version: entry.first_published for entry in PUBLICATION_HISTORY}
    assert dated["v0.3.0"] == "September 5, 2026"
    assert dated["v0.4.0"] == "September 13, 2026"
    assert dated["v0.4.1"] == "September 22, 2026"
    assert dated["v0.4.2"] == "September 28, 2026"
    assert PUBLICATION_HISTORY[0].first_published == PUBLICATION_DATE
    assert PUBLICATION_HISTORY[-1].first_published == FIRST_PUBLISHED


#: The explainer's editions that were published under the site's numbering, before the
#: papers were versioned on their own (the owner, 2026-10-01). Each keeps the number and
#: the day it was published under, exactly: "we don't want to retroactively change any
#: version number that we have published where there's a change of the paper".
SHARED_PAPER_EDITIONS = {"v0.3.0", "v0.4.0", "v0.4.2"}
#: The site's editions under which the paper did not change: a site and atlas edition
#: (the shared version stamp and T-030) and the website edition. Not versions of the
#: paper, so not in its history.
SITE_ONLY_EDITIONS = {"v0.4.1", "v0.5.0"}


def test_the_explainers_history_is_its_own_editions_at_their_published_numbers() -> None:
    """The paper's history lists the editions in which the paper changed, newest first,
    and nothing else: a published number under which the paper changed stays as
    published, number and date, and an edition under which it did not is not a version
    of the paper (the owner, 2026-10-01). The editions it shared with the site are held
    to the site's record for both; the ones it drops are held out.
    """
    versions = [entry.version for entry in EXPLAINER_HISTORY]
    assert len(set(versions)) == len(versions)
    assert [_version(e) for e in EXPLAINER_HISTORY] == sorted(
        (_version(e) for e in EXPLAINER_HISTORY), reverse=True
    )
    assert set(versions) >= SHARED_PAPER_EDITIONS
    assert not SITE_ONLY_EDITIONS & set(versions)
    site = {entry.version: entry for entry in PUBLICATION_HISTORY}
    for entry in EXPLAINER_HISTORY:
        assert re.fullmatch(r"v\d+\.\d+\.\d+", entry.version), entry.version
        assert entry.result_scope.endswith("."), entry.version
        assert "weak" not in entry.result_scope.lower()
        if entry.version in SHARED_PAPER_EDITIONS:
            assert entry.first_published == site[entry.version].first_published, entry.version
    first = EXPLAINER_HISTORY[-1]
    assert first.version == "v0.3.0"
    assert "381/100" in first.result_scope
    assert EXPLAINER_HISTORY[0].version == EXPLAINER_VERSION
    assert EXPLAINER_FIRST_PUBLISHED == first.first_published == FIRST_PUBLISHED
    # The paper's first number of its own (the owner, 2026-10-01: "a patch revision to
    # the paper itself"), dated by the deployment that first served the article in its
    # present substance, recorded in the comment on `EXPLAINER_HISTORY`.
    dated = {entry.version: entry.first_published for entry in EXPLAINER_HISTORY}
    scoped = {entry.version: entry.result_scope for entry in EXPLAINER_HISTORY}
    assert dated["v0.4.3"] == "October 1, 2026"
    assert "T-060" in scoped["v0.4.3"]
    assert "V3/C3" in scoped["v0.4.3"]


def test_a_papers_version_carries_no_data_hash_and_no_site_edition() -> None:
    """A paper's version is its own, plain: the site's stamp and the six characters of
    the data commit are the site's and the posters', and appear in no paper's version."""
    for version in (EXPLAINER_VERSION, OPTIMALITY_REVIEW_EDITION):
        assert STAMP.search(version) is None, version
        assert DATA_REVISION[:DATA_REVISION_LENGTH] not in version
        assert PUBLICATION_EDITION not in version
    assert re.fullmatch(r"v\d+\.\d+\.\d+", OPTIMALITY_REVIEW_VERSION)
    assert OPTIMALITY_REVIEW_EDITION.endswith(OPTIMALITY_REVIEW_VERSION)


def test_the_stamp_is_a_version_and_a_data_revision_and_nothing_else() -> None:
    assert STAMP.fullmatch(PUBLICATION_STAMP), PUBLICATION_STAMP
    assert re.fullmatch(r"[0-9a-f]{40}", DATA_REVISION), DATA_REVISION
    assert f"{PUBLICATION_VERSION}-{DATA_REVISION[:DATA_REVISION_LENGTH]}" == PUBLICATION_STAMP


def test_the_edition_is_the_stamp_with_the_status_ahead_of_it() -> None:
    """And drops the status cleanly when there is none, so going final is one edit."""
    assert PUBLICATION_EDITION.endswith(PUBLICATION_STAMP)
    expected = (
        f"{PUBLICATION_STATUS} {PUBLICATION_STAMP}" if PUBLICATION_STATUS else PUBLICATION_STAMP
    )
    assert expected == PUBLICATION_EDITION
    assert "  " not in PUBLICATION_EDITION
    assert PUBLICATION_EDITION.strip() == PUBLICATION_EDITION


def test_a_drawn_asset_is_stamped_with_the_edition_at_its_own_data_revision() -> None:
    """Rule 4: one spelling of the version, at whichever data commit an asset shows.

    A page prints the edition at the pin. A poster or a film keeps the edition at the
    commit it was drawn from, written by the same function, so the two differ in the
    six characters that say which data each shows and in nothing else.
    """
    assert edition_at(DATA_REVISION) == PUBLICATION_EDITION
    earlier = "0123456789abcdef0123456789abcdef01234567"
    assert edition_at(earlier).endswith(f"{PUBLICATION_VERSION}-012345")
    assert edition_at(earlier).removesuffix("012345") == (
        PUBLICATION_EDITION.removesuffix(DATA_REVISION[:DATA_REVISION_LENGTH])
    )
    # The owner's rule of 2026-10-01, on by default: a poster may trail the data until
    # the next version. `test_known_best_composites` exercises both positions.
    assert COMPOSITES_MAY_TRAIL is True


@pytest.mark.parametrize("revision", [DATA_REVISION, PUBLICATION_REVISION])
def test_each_pinned_revision_names_a_commit_this_repository_has(revision: str) -> None:
    """A hash a reader cannot resolve is worse than no hash.

    The version is printed in a footer precisely so someone can go and look, and the
    claim documents' links are followed, so each pin is held to being a real commit here
    rather than being any characters that happen to be hexadecimal. Skipped rather than
    failed where git cannot answer: a source tarball is a legitimate way to have this
    package, and a shallow clone's cut can fall above the commit.
    """
    found = subprocess.run(
        ("git", "-C", str(REPO), "cat-file", "-t", revision),
        capture_output=True,
        text=True,
        check=False,
    )
    if found.returncode != 0 and "not a git repository" in found.stderr.lower():
        pytest.skip("not a git checkout")
    if found.returncode != 0 and _git(REPO, "rev-parse", "--is-shallow-repository") == "true":
        pytest.skip(f"{revision} is below this shallow clone's cut")
    assert found.returncode == 0, f"{revision}: {found.stderr.strip()}"
    assert found.stdout.strip() == "commit", found.stdout.strip()


def test_the_pinned_revision_is_an_unambiguous_object_prefix() -> None:
    """Repository growth must not force a historical edition's stamp to change.

    Git's automatic abbreviation length grows with the object database and can differ
    between clones. The pinned prefix must still identify exactly one object, rather
    than have the same length as today's unrelated HEAD abbreviation.
    """
    found = subprocess.run(
        ("git", "rev-parse", f"--disambiguate={PUBLICATION_REVISION}"),
        capture_output=True,
        text=True,
        check=False,
    )
    if found.returncode != 0 and "not a git repository" in found.stderr.lower():
        return
    assert found.returncode == 0, found.stderr.strip()
    matches = found.stdout.splitlines()
    assert len(matches) == 1, matches
    assert matches[0].startswith(PUBLICATION_REVISION)


def test_the_pinned_data_revision_is_the_last_data_commit() -> None:
    """The drift check: every artifact prints the pin, so the pin must be what git says.

    It fails on the commit that changes the data, since no commit can carry its own
    hash, and passes again once a following commit re-pins; the message says how.
    """
    try:
        live = data_revision(REPO)
    except RuntimeError as error:
        pytest.skip(str(error))
    assert live == DATA_REVISION, (
        f"the data changed at {live[:12]}, but the version still names "
        f"{DATA_REVISION[:12]}: run `python -m devtools.release_pin --update` from "
        f"packing/, which sets DATA_REVISION = {live!r} in "
        "packing/src/sqpack/release.py, and commit that one line. Nothing is rebuilt: "
        "the atlas posters state the data they were drawn from and are not re-stamped"
    )
    assert data_version(REPO) == PUBLICATION_STAMP


def test_no_file_inside_the_data_carries_the_stamp_unless_it_is_excluded() -> None:
    """Rule 4: a stamped file counted as data would make every re-stamp a data commit.

    The pin would then chase its own hash: re-pinning rewrites the file, the rewrite is
    the new last data commit, and the pin is stale again. Only text files can be
    searched; the raster and PDF exports are excluded with the composite they are drawn
    from.
    """
    search = ("grep", "-lIF", "-e", PUBLICATION_STAMP, "--", *data_pathspec())
    found = subprocess.run(
        ("git", "-C", str(REPO), *search),
        capture_output=True,
        text=True,
        check=False,
    )
    if found.returncode > 1:
        pytest.skip(found.stderr.strip() or "git grep cannot search here")
    assert not found.stdout.strip(), (
        f"these carry {PUBLICATION_STAMP!r} inside the data paths; add them to "
        f"DATA_EXCLUDED or stop stamping them:\n{found.stdout}"
    )


def test_the_data_commit_is_the_last_one_that_changed_the_data(
    history: tuple[Path, str],
) -> None:
    """Redrawing a composite, editing a video spike and editing prose do not count."""
    repo, data = history
    assert data_revision(repo) == data
    assert data_version(repo) == f"{PUBLICATION_VERSION}-{data[:DATA_REVISION_LENGTH]}"


def test_dated_pdf_exports_do_not_move_the_data_revision(history: tuple[Path, str]) -> None:
    repo, data = history
    for name in (
        "known-best-1-100.pdf",
        "known-best-1-324.pdf",
        "square-packings-100-20261008.pdf",
        "square-packings-324-20261008.pdf",
        "square-packings-324-20261009.pdf",
    ):
        path = f"packing/atlas/known-best/{name}"
        _commit(repo, path, "generated PDF receipt\n")
        assert path not in _git(repo, "ls-files", "--", *data_pathspec()).splitlines()
        assert data_revision(repo) == data
    changed = _commit(repo, "packing/atlas/known-best/manifest.json", "new evidence\n")
    assert data_revision(repo) == changed


def test_a_merge_keeps_the_data_commit_its_branch_pinned(history: tuple[Path, str]) -> None:
    """Rule 3's claim about merge commits, held here rather than asserted in prose.

    A branch whose data is the only data that moved keeps its data commit through the
    merge, so the pin it carries is still right on `main`. When `main`'s data moved too,
    the merge itself is the new data commit, and the pin has to follow it.
    """
    repo, _ = history
    base = _git(repo, "rev-parse", "HEAD")
    _git(repo, "switch", "--quiet", "-c", "branch")
    branch_data = _commit(repo, "packing/frontier/n-018.md", "branch\n")
    _git(repo, "switch", "--quiet", "-")
    _commit(repo, "docs.md", "main moves, but not its data\n")
    _git(repo, "merge", "--quiet", "--no-ff", "--no-edit", "branch")
    assert data_revision(repo) == branch_data

    _git(repo, "switch", "--quiet", "-c", "second", base)
    _commit(repo, "packing/frontier/n-019.md", "second branch\n")
    _git(repo, "switch", "--quiet", "-")
    _git(repo, "merge", "--quiet", "--no-ff", "--no-edit", "second")
    assert data_revision(repo) == _git(repo, "rev-parse", "HEAD")


def test_a_shallow_clone_cut_above_the_data_commit_refuses_to_name_one(
    history: tuple[Path, str], tmp_path: Path
) -> None:
    """git reports a shallow clone's cut as changing every path, so the cut is refused.

    Before this was checked, a one-commit clone answered with its own `HEAD` -- a
    commit that touched no data -- and exited zero, which is how the deploy's shallow
    checkout would have stamped a version naming the wrong commit.
    """
    repo, data = history
    shallow = tmp_path / "shallow"
    _git(tmp_path, "clone", "--quiet", "--depth", "1", f"file://{repo}", str(shallow))
    with pytest.raises(RuntimeError, match="shallow history is cut"):
        data_revision(shallow)

    # Five commits reach the one below the data commit, so the data commit is not the cut.
    deep_enough = tmp_path / "deep-enough"
    _git(tmp_path, "clone", "--quiet", "--depth", "5", f"file://{repo}", str(deep_enough))
    assert data_revision(deep_enough) == data


def test_a_directory_that_is_not_a_repository_cannot_name_a_data_commit(
    tmp_path: Path,
) -> None:
    with pytest.raises(RuntimeError, match="cannot name the last data commit"):
        data_revision(tmp_path)


def test_a_commit_is_dated_on_its_authors_own_calendar(tmp_path: Path) -> None:
    """A date derived from a commit is the day its author would say it was made.

    The commit records its own offset from UTC, so the answer does not depend on the
    machine that asks: 23:30 at seven hours behind UTC is the 28th, though it is the
    29th in UTC, and 00:30 at nine hours ahead is the 30th, though it is the 29th there.
    """
    repo = tmp_path / "origin"
    repo.mkdir()
    _git(repo, "init", "--quiet")
    west = _commit(repo, "paper.md", "one\n", "2026-09-28T23:30:00-07:00")
    east = _commit(repo, "paper.md", "two\n", "2026-09-30T00:30:00+09:00")
    assert commit_date(repo, west) == "2026-09-28"
    assert commit_date(repo, east) == "2026-09-30"
    with pytest.raises(RuntimeError, match="git cannot date"):
        commit_date(repo, "0" * 40)
    with pytest.raises(RuntimeError, match="git cannot date"):
        commit_date(tmp_path, west)


def test_the_last_change_to_a_text_is_its_latest_commit_merges_excluded(
    tmp_path: Path,
) -> None:
    """What a paper's "revised" line is held to, and each way it could be wrong.

    The latest author date among the commits that changed the file. A commit to another
    file does not count; a merge is not when anyone wrote the text, so it does not
    either; and of two branches merged out of order the later change wins, though git
    lists the earlier one first.
    """
    repo = tmp_path / "origin"
    repo.mkdir()
    _git(repo, "init", "--quiet")
    _commit(repo, "paper.md", "one\n", "2026-09-28T12:00:00+00:00")
    base = _git(repo, "rev-parse", "HEAD")
    _commit(repo, "other.md", "prose\n", "2026-10-05T12:00:00+00:00")
    assert last_change_date(repo, "paper.md") == "2026-09-28"

    _git(repo, "switch", "--quiet", "-c", "branch", base)
    _commit(repo, "paper.md", "one\ntwo\n", "2026-10-01T12:00:00+00:00")
    _git(repo, "switch", "--quiet", "-")
    _commit(repo, "notes.md", "later, and not the paper\n", "2026-10-03T12:00:00+00:00")
    _git(
        repo,
        "-c",
        "user.name=release test",
        "merge",
        "--quiet",
        "--no-ff",
        "--no-edit",
        "branch",
    )
    assert last_change_date(repo, "paper.md") == "2026-10-01"
    assert last_change_date(repo, "paper.md", "other.md") == "2026-10-05"

    with pytest.raises(RuntimeError, match="no commit changes it"):
        last_change_date(repo, "absent.md")
    with pytest.raises(RuntimeError, match="cannot date the last change"):
        last_change_date(tmp_path, "paper.md")

    shallow = tmp_path / "shallow"
    _git(tmp_path, "clone", "--quiet", "--depth", "1", f"file://{repo}", str(shallow))
    with pytest.raises(RuntimeError, match="history is shallow"):
        last_change_date(shallow, "paper.md")
