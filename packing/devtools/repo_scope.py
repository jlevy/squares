"""Which trees in the checkout are this repository's to be answerable for.

Two sweeps ask that question and used to answer it separately. `check_svg_rendering`
named `vendor` in a frozenset; `check_documentation` did not sweep vendored prose at
all, and instead carried a `vendor/**/*.md` exclusion in the document map. The map's
loader requires every exclusion to match at least one file, so on a plain `git clone`
-- `vendor/kpress` present as an empty directory, no submodule checked out -- the docs
check failed with `document exclusion is empty` (think-5e7k). Both workflows pass
`submodules: true`, which is the only reason CI never saw it.

Both are now the predicate below, and the vendored set is read from `.gitmodules`
rather than typed, so a second submodule is excluded by being declared (think-f4vl).
A directory that is not checked out is still vendored: the answer comes from the
declaration, not from what happens to be on disk.
"""

from __future__ import annotations

import re
from functools import cache
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

#: `path = <value>` inside a `[submodule "..."]` stanza. The file is INI-shaped but not
#: `configparser`-shaped: git allows tabs, repeated sections and comment forms that
#: module rejects, and only one key here is wanted.
_SUBMODULE_PATH = re.compile(r"^\s*path\s*=\s*(.+?)\s*$", re.MULTILINE)


@cache
def vendored_directories() -> frozenset[str]:
    """Every submodule path `.gitmodules` declares, repository-relative and POSIX.

    Read once and cached: both sweeps call it per candidate path, and the file does not
    change under a running check.
    """
    gitmodules = REPO / ".gitmodules"
    if not gitmodules.is_file():
        return frozenset()
    declared = _SUBMODULE_PATH.findall(gitmodules.read_text(encoding="utf-8"))
    return frozenset(Path(path).as_posix() for path in declared)


def is_vendored(path: Path) -> bool:
    """Whether `path` is inside a declared submodule.

    Compared on path parts rather than on the string, so `vendor/kpress-notes` is not
    matched by a declared `vendor/kpress`.
    """
    parts = path.resolve().relative_to(REPO).parts
    prefixes = {"/".join(parts[:length]) for length in range(1, len(parts) + 1)}
    return bool(prefixes & vendored_directories())
