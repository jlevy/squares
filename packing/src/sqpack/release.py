"""The version this project's reader-facing artifacts carry, and the rule that keeps it true.

The explainer prints it in its credits and the atlas draws it in its footer, and the
workbench and the videos show it too, so a release is stamped in one place and all of
them follow. This is the publication's version, not the package's: `pyproject.toml`
versions the code, and the two move for different reasons.

It is written `v0.4.1-f5e113` (the owner, 2026-09-22): the edition's semver core, then
the first six characters of the last commit that changed the evidence and data. Two
artifacts drawn from the same data carry the same version, whatever code commit built
them. The rule that keeps that true without any artifact chasing its own hash:

1. **Every artifact prints `PUBLICATION_EDITION`, whose hash is the pinned
   `DATA_REVISION`.** Nothing reads git to stamp a version, so a render needs no history
   -- the deploy's shallow checkout and a source tarball stamp the same string as a full
   clone -- and the committed atlas, the page rendered beside it and a video built from
   the same tree cannot disagree.
2. **`DATA_REVISION` must be what git says** -- `data_revision`, the last commit that
   changed `DATA_PATHS`. `tests/test_release.py` fails when the two differ, wherever git
   can answer; both pull-request behavioral shards check out full history, so every pull
   request asks.
3. **A commit that changes the data is followed by one that re-pins**: `DATA_REVISION`
   set to the hash the failing test names, and the stamped artifacts rebuilt
   (`build_known_best_atlas --update`). No commit can contain its own hash, so the pin
   trails the data by one commit, as `PUBLICATION_REVISION` always trailed the content
   it named. Only a branch's head has to agree: merges here are merge commits, so the
   data commit a branch pinned is still the last one on `main` after it lands. If
   `main`'s data also moved meanwhile, the merge is itself the new data commit, so the
   pull request's merge ref fails the check until the branch merges `main` and re-pins.
4. **The re-pinning commit is not itself a data commit.** The artifacts that carry the
   stamp are excluded from the data (`DATA_EXCLUDED`); counting them would make each
   re-stamp a new data commit, and the pin would chase its own hash forever. A test fails
   when a text file inside the data paths carries the stamp without being excluded.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import NamedTuple


class PublicationHistoryEntry(NamedTuple):
    """One retained public edition and its headline result scope."""

    version: str
    first_labeled: str
    result_scope: str


#: The two editions retained in the explainer's short public history, newest first.
#: Dates say when each label first appeared in Git as an edition of this publication,
#: rather than when a theorem was proved or when the page was deployed.
PUBLICATION_HISTORY = (
    PublicationHistoryEntry(
        version="v0.4.1",
        first_labeled="September 22, 2026",
        result_scope=(
            "The shared-version edition: the page and the atlas carry one version, "
            "named for the last commit that changed the data, and the atlas adds "
            "T-030's $s(18) ≥ 4679/1000$."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.0",
        first_labeled="September 10, 2026",
        result_scope=(
            "The T-025/T-026 proof edition: T-025 proves "
            "$s(11) ≥ 191/50 = 3.82$, and T-026 proves "
            "$s(11) ≥ 3.8264474…$."
        ),
    ),
)

#: The edition the figures and the explainer state. Choose at most one version bump per
#: merge, and keep it fixed while revising that pull request.
PUBLICATION_VERSION = PUBLICATION_HISTORY[0].version

#: Where the edition stands, said ahead of the version. Empty once it is final; the
#: join below then drops it and the stray space with it, so going final is one edit.
PUBLICATION_STATUS = ""

#: What the shared version's hash names (the owner, 2026-09-22): the last commit that
#: changed the evidence and data every artifact is drawn from. Repository-relative, as
#: every declared path here is.
DATA_PATHS: tuple[str, ...] = ("packing/frontier", "packing/atlas/known-best")

#: What inside `DATA_PATHS` is not evidence and data, and so never moves the version, as
#: git pathspecs. The atlas composites and their raster and PDF exports carry the stamp
#: and are drawn from the data rather than being it; counting them would make the commit
#: that re-stamps them a data commit (rule 4 above). The video spikes are the players'
#: code, and the videos themselves are release assets, never committed.
#:
#: The registers' own READMEs join them on 2026-09-22, on the same grounds: they document
#: how a record is written, and nothing is drawn from them. `e560571f2` edited
#: `frontier/README.md` alone -- the prose on registration evidence, no packing record and
#: no bound -- and under the old list that moved the version every artifact prints, which
#: would have restamped the atlas and dated a cut whose every frame was identical. A
#: version that changes when the instructions change is not naming the evidence.
DATA_EXCLUDED: tuple[str, ...] = (
    "packing/atlas/known-best/known-best-1-*",
    "packing/atlas/known-best/video",
    "packing/frontier/README.md",
    "packing/atlas/known-best/README.md",
)

#: How many characters of that commit the version carries (the owner, 2026-09-22).
DATA_REVISION_LENGTH = 6

#: The last data commit, pinned in full: what `data_revision` returned when it was last
#: re-pinned. Full rather than six characters so the drift check compares a commit, not
#: a prefix.
DATA_REVISION = "e7c8cca1b7e588f53efc25ca8112a315326f7279"

#: The version, written the one way it is ever written: `v0.4.1-f5e113`. Semver core,
#: then the data revision, in the shape a build identifier takes everywhere else.
#:
#: This is the value to reach for. It exists because the artifacts that stamp an edition
#: used to compose their own strings from the parts, in two files and two languages, and
#: the page named a different commit from the atlas. Hand-assembled spellings of one fact
#: are how they come to disagree.
PUBLICATION_STAMP = f"{PUBLICATION_VERSION}-{DATA_REVISION[:DATA_REVISION_LENGTH]}"

#: How the version is written wherever it is stamped: the stamp, with the status ahead
#: of it while there is one. The atlas footer, the explainer's credits and every other
#: artifact take this string whole, so none can disagree about whether the reader is
#: holding a draft, nor about how the version is spelled.
PUBLICATION_EDITION = " ".join(part for part in (PUBLICATION_STATUS, PUBLICATION_STAMP) if part)

#: The date that edition carries, written the way a reader reads it.
PUBLICATION_DATE = PUBLICATION_HISTORY[0].first_labeled

#: The commit the committed claim documents link to (`render_explainer.edition_file`), at
#: this repository's short length. It is pinned for the reason `DATA_REVISION` is: those
#: documents are compared byte for byte with a fresh render, so a link naming the build
#: commit would fail their drift check forever. It is in no version string. It moves
#: when the claim documents are regenerated for an edition, while the page's own links
#: name the commit it is built from (`render_explainer.link_revision`).
PUBLICATION_REVISION = "277f8b1a"


def data_pathspec() -> tuple[str, ...]:
    """`DATA_PATHS` less `DATA_EXCLUDED`, as the arguments git takes after `--`."""
    return (*DATA_PATHS, *(f":(exclude){path}" for path in DATA_EXCLUDED))


def _shallow_boundary(repo: Path) -> frozenset[str]:
    """The commits a shallow clone's history is cut at; none in a complete clone."""
    found = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--git-path", "shallow"],
        capture_output=True,
        text=True,
        check=False,
    )
    if found.returncode != 0:
        return frozenset()
    shallow = Path(found.stdout.strip())
    shallow = shallow if shallow.is_absolute() else repo / shallow
    return frozenset(shallow.read_text().split()) if shallow.is_file() else frozenset()


def data_revision(repo: Path) -> str:
    """The full hash of the last commit in `repo` that changed the data, as git says.

    Raises where git cannot say: outside a repository, and in a shallow clone whose cut
    falls before the answer. git reports the commit a shallow history is cut at as
    changing every path, since it cannot see that commit's parent, so the boundary is
    refused rather than returned: a version stamped from it would name the wrong data.
    """
    found = subprocess.run(
        ["git", "-C", str(repo), "log", "-1", "--format=%H", "--", *data_pathspec()],
        capture_output=True,
        text=True,
        check=False,
    )
    revision = found.stdout.strip()
    if found.returncode != 0 or not revision:
        raise RuntimeError(
            f"git cannot name the last data commit in {repo}: "
            f"{found.stderr.strip() or 'no commit touches ' + ', '.join(DATA_PATHS)}"
        )
    if revision in _shallow_boundary(repo):
        raise RuntimeError(
            f"git cannot name the last data commit in {repo}: its shallow history is cut "
            f"at {revision[:12]}, so whether that commit changed the data cannot be seen"
        )
    return revision


def data_version(repo: Path) -> str:
    """The shared version as git says it is now, which the pinned one must equal.

    Artifacts print `PUBLICATION_EDITION` rather than this, so that a render needs no
    history; this is what the drift check holds that pin to.
    """
    return f"{PUBLICATION_VERSION}-{data_revision(repo)[:DATA_REVISION_LENGTH]}"
