"""One spelling of the edition, in one place, in the shape a build identifier takes.

The atlas footer and the explainer's credits each used to compose the stamp from the
parts, in two files and two languages, joined by a literal ", revision ". Two
hand-assembled spellings of one fact is how they come to disagree, and neither could be
changed without remembering the other. What is pinned here is the shape and the single
source, not the values: bumping a version or cutting a new revision is an ordinary edit
to `sqpack.release` and should not need a test changed with it.
"""

from __future__ import annotations

import re
import subprocess

from sqpack.release import (
    PUBLICATION_EDITION,
    PUBLICATION_REVISION,
    PUBLICATION_STAMP,
    PUBLICATION_STATUS,
    PUBLICATION_VERSION,
)

#: `v0.1.0-3bd273e6`: a semver core, a hyphen, and this repository's short hash.
STAMP = re.compile(r"v\d+\.\d+\.\d+-[0-9a-f]{7,40}")


def test_the_stamp_is_a_version_and_a_revision_and_nothing_else() -> None:
    assert STAMP.fullmatch(PUBLICATION_STAMP), PUBLICATION_STAMP
    assert f"{PUBLICATION_VERSION}-{PUBLICATION_REVISION}" == PUBLICATION_STAMP


def test_the_edition_is_the_stamp_with_the_status_ahead_of_it() -> None:
    """And drops the status cleanly when there is none, so going final is one edit."""
    assert PUBLICATION_EDITION.endswith(PUBLICATION_STAMP)
    expected = (
        f"{PUBLICATION_STATUS} {PUBLICATION_STAMP}" if PUBLICATION_STATUS else PUBLICATION_STAMP
    )
    assert expected == PUBLICATION_EDITION
    assert "  " not in PUBLICATION_EDITION
    assert PUBLICATION_EDITION.strip() == PUBLICATION_EDITION


def test_the_revision_names_a_commit_this_repository_has() -> None:
    """A hash a reader cannot resolve is worse than no hash.

    The stamp is printed in a footer precisely so someone can go and look, so the
    revision is held to being a real object here rather than being any eight characters
    that happen to be hexadecimal. Skipped rather than failed where git cannot answer,
    since a source tarball is a legitimate way to have this package.
    """
    found = subprocess.run(
        ("git", "cat-file", "-t", PUBLICATION_REVISION),
        capture_output=True,
        text=True,
        check=False,
    )
    if found.returncode != 0 and "not a git repository" in found.stderr.lower():
        return
    assert found.returncode == 0, f"{PUBLICATION_REVISION}: {found.stderr.strip()}"
    assert found.stdout.strip() == "commit", found.stdout.strip()


def test_the_revision_is_the_length_this_repository_abbreviates_to() -> None:
    """So the footer's hash and `git rev-parse --short` agree, character for character.

    A shorter hash still resolves, which is why this is its own check rather than a
    clause of the shape above: what would go unnoticed is the stamp drifting to a
    different abbreviation than the one every other tool here prints.
    """
    short = subprocess.run(
        ("git", "rev-parse", "--short", "HEAD"),
        capture_output=True,
        text=True,
        check=False,
    )
    if short.returncode != 0:
        return
    assert len(PUBLICATION_REVISION) == len(short.stdout.strip())
