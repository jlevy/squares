"""OR-18's unit of repository size: a blob as Git stores it.

`OR-18` counts a file's size as its blob's, compressed as Git packs it, because that is what
a clone downloads for it and what history keeps. This module is that unit's one
definition. `devtools.upper_bound_houses sizes` measures a staged adoption's witnesses with
it, and `devtools.check_added_blobs` holds each of a branch's new blobs to the per-blob
ceiling in `devtools/added-blobs.yaml` with it. A set's size is not a sum of these: since
22 October 2026 it is the thin pack of the set's new objects, deltas included, which that
guard asks Git for.

The size is the blob object, the header ``blob <size>`` and a NUL then the content,
compressed by zlib at its default level, as Git compresses an object in a pack
(`core.compression`) before any delta. A loose object, as `git hash-object -w` first
writes it, is compressed at Git's default loose level and comes out a little larger. The
figure depends only on the content and the zlib build. The interpreter build fixes the zlib
build, since the pinned interpreter has zlib built in, and another build, such as zlib-ng,
can change the figure. A golden test in `test_added_blob_guard` pins both forms to recorded
figures, so it fails if the zlib build changes. Git's own `%(objectsize:disk)` does not
have that property, since it depends on how a clone happened to pack and delta its objects.
"""

from __future__ import annotations

import zlib


def stored_size(data: bytes) -> int:
    """The bytes Git keeps for a file: its blob object compressed at zlib's default level."""
    return len(zlib.compress(b"blob %d\x00" % len(data) + data, zlib.Z_DEFAULT_COMPRESSION))


class StoredSize:
    """`stored_size` of content fed in pieces, so that a large blob is never held whole.

    zlib decides what to emit only once it holds a full lookahead, so the compressed length
    does not depend on how the content is split; `test_added_blob_guard` checks that against
    `stored_size` for many ways of splitting it.
    """

    __slots__ = ("_compressor", "_total")

    def __init__(self, size: int) -> None:
        # zlib.compress takes no memory level and uses 8, so it is stated here, not defaulted.
        self._compressor = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, memLevel=8)
        self._total = len(self._compressor.compress(b"blob %d\x00" % size))

    def update(self, chunk: bytes | memoryview) -> None:
        self._total += len(self._compressor.compress(chunk))

    def result(self) -> int:
        return self._total + len(self._compressor.flush())


def stored_size_bound(size: int) -> int:
    """The most `stored_size` can be for any content of `size` bytes.

    It is zlib's `compressBound` over the object, so a blob whose bound is under a ceiling is
    under it whatever its content, and its content need not be read to decide that.
    """
    length = len(b"blob %d\x00" % size) + size
    return length + (length >> 12) + (length >> 14) + (length >> 25) + 13
