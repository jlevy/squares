"""How the site links this repository: every link names the default branch.

Every page the site serves links a repository file or directory at `main`, as
`blob/main/PATH` for a file, `tree/main/PATH` for a directory and
`raw.githubusercontent.com/jlevy/squares/main/PATH` for an image, with any `?plain=1`
or `#L…` anchor kept. A link that named the commit a page was built from was a
permalink to a commit that a squash merge leaves on no branch, and GitHub answers such
a link with a 404 once the branch that held it is deleted. `main` is where the site is
deployed from, so a link to it opens the file the page was built from until the next
deploy, and the file as it now is after that.

What keeps those links from breaking is that the paths they name are stable: the
reader documents the site links by name are defined once here, and each renderer links
them through these constants rather than by writing the path again. A path that is not
in the tree `main` will hold fails the render (`site_documents`) or the render-time test
(`tests/test_repo_links.py`), and the deployed-site check refuses any page that links a
commit by its hash, the two reviews aside.

Two things name a commit on purpose. The committed claim documents name their edition's
revision (`render_n11_lower_bounds_explainer.edition_file`); they are not site pages. The
reviews are site pages, Parts II and III of the n = 11 series, and each pins every citation
to the commit it was built from (`render_n11_optimality_review.link_revision`, and the
threshold-bound review's renderer, which is modelled on it, the same way): a paper cites the
evidence as it stood when it was typeset, with anchors into reviews and receipts that keep
changing on `main`. The hazard above does not reach a deployed review, since the deploy builds
it from the commit it deploys, which `main` keeps; the deployed-site check holds each of its
citations to that commit and to its tree (`check_published_site.paper_citations`).
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path
from typing import Literal
from urllib.parse import quote

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent

REPO_URL = "https://github.com/jlevy/squares"
RAW_URL = "https://raw.githubusercontent.com/jlevy/squares"
#: The branch every repository link on the site names, and the one the site deploys from.
DEFAULT_BRANCH = "main"

# The reader documents the site links by name, repository-relative. Each is also served
# as a page of its own (`site_documents.DOCUMENTS`); these are the paths its GitHub link
# and its page's source share.
README = "README.md"
TUTORIAL = "TUTORIAL.md"
SYNOPSIS = "SYNOPSIS.md"
CONVENTIONS = "conventions.md"
DEVELOPMENT = "development.md"
EPISTEMICS = "epistemics.md"
# Three generated views of the record that are not served as pages. The results register
# and the status table are each shown by a page built from the same record, the results
# table and the frontier atlas, which is where a link to either leads
# (`site_documents.RECORD_PAGES`). The defect log is a record of the toolchain, internal
# to the repository, and a link to it opens the file on `main`.
RESULTS = "packing/frontier/RESULTS.md"
STATUS = "packing/frontier/STATUS.md"
DEFECTS = "defects.md"

Kind = Literal["blob", "tree", "raw"]


def _inside(path: Path | str) -> str | None:
    """`path` as a repository-relative POSIX path, or `None` where it lies outside."""
    if isinstance(path, str):
        return path.strip("/")
    try:
        return path.resolve().relative_to(REPO).as_posix()
    except ValueError:
        return None


def relative(path: Path | str) -> str:
    """The repository-relative POSIX path of `path`, absolute or already relative."""
    inside = _inside(path)
    if inside is None:
        raise SystemExit(f"{path} is outside the repository and cannot be linked")
    return inside


def path_kind(path: Path | str) -> Literal["blob", "tree"] | None:
    """What `path` is in the repository: a file (`blob`), a directory (`tree`), or
    neither (`None`), as GitHub will serve it.

    The working tree answers where it has the path, and the commit being rendered
    (`repository_tree`) where it does not. The second half is what a partial checkout
    needs: the Pages jobs check the repository out without the directories under
    `packing/resources` and `packing/campaign`, 504 MB the render never opens, and a
    renderer that asked the disk alone whether a record's source, packet or certificate
    exists dropped every link into them from the deployed site while a full checkout
    kept them (found 2026-10-01 by comparing the two). A path on disk that no commit
    holds yet is still found, as it was.
    """
    inside = _inside(path)
    if inside is None:
        return None
    on_disk = REPO / inside
    if on_disk.is_dir():
        return "tree"
    if on_disk.is_file():
        return "blob"
    tree = repository_tree()
    if inside in tree.files:
        return "blob"
    return "tree" if inside in tree.directories else None


def repo_url(
    path: Path | str, fragment: str = "", *, kind: Kind | None = None, ref: str = DEFAULT_BRANCH
) -> str:
    """The GitHub URL of a repository file or directory on `main`.

    `kind` is read from the checkout when it is not given (`path_kind`, which asks the
    commit where a partial checkout lacks the path): GitHub serves a directory under
    `tree/` and a file under `blob/`, and redirects the other way round, so the
    canonical one is written and no link is a redirect. `fragment` is appended as given,
    `?plain=1#L12` or `#section`. `ref` exists for the committed claim documents alone,
    which name their edition's revision (`render_n11_lower_bounds_explainer.edition_file`).
    """
    rel = relative(path)
    if kind is None:
        kind = path_kind(rel) or "blob"
    quoted = quote(rel, safe="/")
    if kind == "raw":
        return f"{RAW_URL}/{ref}/{quoted}{fragment}"
    suffix = f"/{quoted}" if quoted else ""
    return f"{REPO_URL}/{kind}/{ref}{suffix}{fragment}"


def branch_file(path: Path | str, fragment: str = "") -> str:
    """A repository file's URL on `main`, as the "On GitHub" links and the rest name it."""
    return repo_url(path, fragment, kind="blob")


#: A link into this repository that names a commit by its hash, full or abbreviated,
#: rather than a branch. Release downloads (`/releases/…`) are not repository paths.
HASH_PINNED = re.compile(
    r"(?:"
    + re.escape(REPO_URL)
    + r"/(?:blob|tree|raw)|"
    + re.escape(RAW_URL)
    + r")/[0-9a-f]{7,40}/[^\s\"'<>)]*"
)

#: A link to a path on `main`: the kind, then the path with any query or anchor.
BRANCH_LINK = re.compile(
    r"(?:"
    + re.escape(REPO_URL)
    + r"/(blob|tree|raw)|"
    + re.escape(RAW_URL)
    + r")/"
    + re.escape(DEFAULT_BRANCH)
    + r"(?:/([^\s\"'<>)?#]*))?"
)

#: First-party result reports are citations, not files in the repository's tree.
REPORT_LINK = re.compile(
    re.escape(REPO_URL)
    + r"/(?:issues/[1-9][0-9]*(?:#issuecomment-[1-9][0-9]*)?"
    + r"|discussions/[1-9][0-9]*(?:#discussioncomment-[1-9][0-9]*)?)"
)


def is_report_link(url: str) -> bool:
    """Whether `url` cites a numbered issue/discussion or its numbered comment."""
    return REPORT_LINK.fullmatch(url) is not None


def hash_pinned_links(text: str) -> list[str]:
    """Every repository link in `text` that names a commit rather than `main`."""
    return sorted(set(HASH_PINNED.findall(text)))


def branch_paths(text: str) -> set[tuple[str, str]]:
    """Every (kind, path) `text` links on `main`, `raw` for a raw file; `""` is the root."""
    return {(kind or "raw", path.rstrip("/")) for kind, path in BRANCH_LINK.findall(text)}


@dataclass(frozen=True)
class RepositoryTree:
    """A commit's tracked files and directories, the root as `""`, and its submodules:
    each path with the repository and commit it pins."""

    files: frozenset[str]
    directories: frozenset[str]
    submodules: dict[str, tuple[str, str]] = field(default_factory=dict)

    def missing(self, links: set[tuple[str, str]]) -> list[str]:
        """Each (kind, path) of `links` that this tree does not have, as `kind/path`."""
        absent = []
        for kind, path in sorted(links):
            has = path in self.directories if kind == "tree" else path in self.files
            if not has:
                absent.append(f"{kind}/{path}")
        return absent


def _ls_tree(revision: str, *flags: str) -> frozenset[str]:
    found = subprocess.run(
        ("git", "ls-tree", "-r", *flags, "--name-only", "-z", revision),
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    if found.returncode != 0:
        raise SystemExit(f"git ls-tree {revision} failed: {found.stderr.strip()}")
    return frozenset(name for name in found.stdout.split("\0") if name)


def _submodules(revision: str) -> dict[str, tuple[str, str]]:
    """Each submodule at `revision`: its path, its repository's URL and pinned commit."""
    listed = subprocess.run(
        ("git", "config", "--blob", f"{revision}:.gitmodules", "--get-regexp", "url"),
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    found: dict[str, tuple[str, str]] = {}
    for line in listed.stdout.splitlines():
        key, _, url = line.partition(" ")
        path = key.removeprefix("submodule.").removesuffix(".url")
        entry = subprocess.run(
            ("git", "ls-tree", revision, path),
            cwd=REPO,
            capture_output=True,
            text=True,
            check=False,
        ).stdout.split()
        if len(entry) >= 3 and entry[1] == "commit":
            found[path] = (url.removesuffix(".git"), entry[2])
    return found


@cache
def repository_tree(revision: str = "HEAD") -> RepositoryTree:
    """Every file and directory at `revision`, and its submodules.

    The default is the checkout's `HEAD`: the site is rendered and deployed from `main`,
    so the tree being rendered is the tree its `blob/main/` links will open.
    """
    return RepositoryTree(
        _ls_tree(revision), _ls_tree(revision, "-d") | {""}, _submodules(revision)
    )
