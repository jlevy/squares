"""Which trees the checkout is answerable for, answered once from `.gitmodules`.

Two sweeps asked that question separately and disagreed about the vendored tree in
opposite directions. `check_svg_rendering` swept it, which is D-455.
`check_documentation` did not sweep it, and excluded its prose through a document-map
pattern instead -- which fails on a plain `git clone`, because the map's loader requires
every exclusion to match a file and an unchecked-out submodule matches none (think-5e7k).

`devtools.repo_scope` is the one answer, and it comes from the declaration rather than
from the working tree, so it is the same on a clone with submodules and one without.
"""

from __future__ import annotations

from devtools.repo_scope import REPO, is_vendored, vendored_directories
from sqpack.yamlio import safe_load


def test_the_vendored_set_is_what_gitmodules_declares() -> None:
    """Read, not typed. A second submodule is excluded by being declared."""
    declared = vendored_directories()
    assert declared == {"vendor/kpress"}, sorted(declared)
    for path in declared:
        assert (REPO / path).is_dir(), f"{path} is declared but not a directory"


def test_a_path_inside_a_declared_submodule_is_vendored() -> None:
    assert is_vendored(REPO / "vendor" / "kpress" / "README.md")
    assert is_vendored(REPO / "vendor" / "kpress")


def test_a_sibling_sharing_a_prefix_is_not_vendored() -> None:
    """Compared on path parts, so `vendor/kpress-notes` is not `vendor/kpress`.

    A string prefix test would call it vendored and stop policing our own prose in it.
    """
    assert not is_vendored(REPO / "vendor" / "kpress-notes" / "README.md")
    assert not is_vendored(REPO / "README.md")
    assert not is_vendored(REPO / "packing" / "devtools" / "repo_scope.py")


def test_every_map_pattern_matches_a_file_no_submodule_supplies() -> None:
    """The regression: a map pattern satisfied only by vendored files fails a plain clone.

    The loader requires every collection and every exclusion to match at least one file,
    and reports `document exclusion is empty` when one does not. A pattern whose only
    matches live inside a submodule therefore passes with `submodules: true` -- which is
    what both workflows pass -- and fails a plain `git clone`. That is precisely what
    `vendor/**/*.md` did (think-5e7k).

    Checked by matching each pattern the way the loader does and then discarding the
    vendored files, rather than by reasoning about the pattern's prefix: `vendor/**/*.md`
    has the prefix `vendor`, which is not itself a declared submodule path, so prefix
    arithmetic reports it clean.
    """
    map_path = REPO / "docs" / "project" / "document-map.yaml"
    document_map = safe_load(map_path.read_text("utf-8"))
    patterns = [
        entry["pattern"] for key in ("collections", "exclusions") for entry in document_map[key]
    ]
    assert patterns, "the map declares no patterns; this check would pass vacuously"
    for pattern in patterns:
        without_submodules = [
            path for path in REPO.glob(pattern) if path.is_file() and not is_vendored(path)
        ]
        assert without_submodules, f"{pattern} matches only files a submodule supplies"
