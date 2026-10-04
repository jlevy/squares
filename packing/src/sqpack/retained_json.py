"""Width-bounded JSON for the large results the repository retains.

**A retained result is written so that a line is a record, and every line can be read in
a review.** `json.dumps` with `indent=2` puts every scalar on its own line, which is right
for a small document a person reads top to bottom and wrong for a census of thousands of
rows: the file is mostly brackets and indentation, and one changed row is a dozen-line
hunk. Written compactly, a record is one line and a change to it is one changed line, so
a diff shows which records moved -- until a record is a whole case's per-square detail,
and its line is longer than any diff view will show.

So a value is written compactly, on one line, when that line fits in `WIDTH` characters,
and is otherwise opened, two spaces a level: an object one key per line and a list of
records one element per line, each child laid out by the same rule, and a list of scalars
filled, as many to a line as fit. A record that fits stays one line; one too large to
review as a line becomes lines that are; a long vector of numbers becomes a block of full
lines rather than a line per number. The width counts the whole line -- indentation, the
`"key": ` prefix and the trailing comma -- so a line is longer than `WIDTH` only when what
it holds cannot be split: a scalar or a key longer than that by itself, since a scalar is
never split, or an empty container or a bracket nested so deep that its indentation alone
fills the width. The document itself always opens, so each top-level key starts a line,
and an empty object or list is `{}` or `[]`.

On 2026-10-03 the five largest results of one branch were 201,257 lines of `indent=2`
text, 4.9 MB, and most of a 275,273-line pull request. Written a record per line by depth
alone they were 3,022 lines, but 802 of those lines were over 1,000 characters and one was
92,680. Written here they are 27,501 lines and 2.9 MB, the longest line 996 characters,
and they parse to the same documents.

`sort_keys`, `ensure_ascii`, `allow_nan` and `default` mean what they mean to `json.dumps`
and apply at every level, so a writer that switches here keeps its arguments. The text is
a function of the document, those arguments and the width alone, and it parses to what
`json.dumps` would have written, keys in the same order.

**The cost is linear in the document.** Deciding whether a value fits by encoding it, and
then encoding its children again when it does not, costs the document's size once for
every level opened. Instead each container is measured once, bottom up: a container of
scalars by the encoder in one call, any other from its children's lengths. A container no
wider than the width keeps its text, joined from its children's, so writing a line encodes
nothing again.
"""

from __future__ import annotations

import json
import math
from collections.abc import Callable
from dataclasses import dataclass, field
from json import encoder as json_encoder
from json.encoder import encode_basestring, encode_basestring_ascii
from typing import Any

__all__ = ["WIDTH", "dumps"]

#: The longest line written, counting its indentation, key prefix and trailing comma. Wide
#: enough that a typical record is one line; narrow enough that every line can be read in
#: a diff. Past it, a line holds only what cannot be split, in practice one long string.
WIDTH = 1000
INDENT = "  "

_NATIVE = (dict, list, tuple, str, int, float, bool, type(None))
_CONTAINERS = (dict, list, tuple)
#: The exact types whose text is the same wherever they stand. A subclass, or anything
#: `default` converts, is measured by the encoder itself instead.
_SCALAR_TYPES = frozenset({str, int, float, bool, type(None)})
_STRING_KEYS = frozenset({str})
_LITERALS = {None: "null", True: "true", False: "false"}
# What `JSONEncoder.encode({key: None})` puts after the key text.
_NULL_VALUE_SUFFIX = ":null}"
# The C encoder `JSONEncoder.iterencode` builds, absent where `_json` is not compiled in.
_C_MAKE_ENCODER: Callable[..., Callable[[Any, int], tuple[str, ...]]] | None = getattr(
    json_encoder, "c_make_encoder", None
)


def dumps(
    document: Any,
    *,
    sort_keys: bool = False,
    ensure_ascii: bool = True,
    allow_nan: bool = True,
    default: Callable[[Any], Any] | None = None,
    width: int = WIDTH,
) -> str:
    """`document` as width-bounded JSON text, ending in a newline."""
    encoder = json.JSONEncoder(
        sort_keys=sort_keys,
        ensure_ascii=ensure_ascii,
        allow_nan=allow_nan,
        default=default,
        separators=(",", ":"),
    )
    string = encode_basestring_ascii if ensure_ascii else encode_basestring
    writer = _Writer(encoder, _compact(encoder, string), default, width, string)
    writer.write(document, 0, "", "", opened=True)
    return "\n".join(writer.lines) + "\n"


def _compact(encoder: json.JSONEncoder, string: Callable[[str], str]) -> Callable[[Any], str]:
    """The encoder's compact text of a value, from a C encoder built once.

    `JSONEncoder.encode` builds a fresh C encoder on every call, which costs more than
    encoding a short record; a measure that encodes tens of thousands of them builds one
    here, with the arguments `JSONEncoder.iterencode` gives it. Where the C accelerator is
    absent, `JSONEncoder.encode` is the same text.
    """
    if _C_MAKE_ENCODER is None:
        return encoder.encode
    # The C encoder adds an object to `markers` while encoding it and removes it after, so
    # one dictionary serves every call; a call that raises ends the whole `dumps`.
    built = _C_MAKE_ENCODER(
        {},
        encoder.default,
        string,
        None,
        encoder.key_separator,
        encoder.item_separator,
        encoder.sort_keys,
        encoder.skipkeys,
        encoder.allow_nan,
    )

    def compact(value: Any) -> str:
        return "".join(built(value, 0))

    return compact


@dataclass(slots=True)
class _Writer:
    encoder: json.JSONEncoder
    compact: Callable[[Any], str]
    default: Callable[[Any], Any] | None
    width: int
    string: Callable[[str], str]
    lines: list[str] = field(default_factory=list[str])
    # Compact lengths of containers, the compact texts of those no wider than the width,
    # and what `default` made of foreign objects, by `id`. They hold for one call, while
    # the document and `converted` keep every keyed object alive.
    sizes: dict[int, int] = field(default_factory=dict[int, int])
    texts: dict[int, str] = field(default_factory=dict[int, str])
    converted: dict[int, Any] = field(default_factory=dict[int, Any])
    measuring: set[int] = field(default_factory=set[int])
    # Each string key's text with its colon, as a compact object writes it.
    keys: dict[str, str] = field(default_factory=dict[str, str])

    def write(
        self, value: Any, depth: int, prefix: str, suffix: str, *, opened: bool = False
    ) -> None:
        """Append the lines of `value`: the first indented `depth` levels and led by
        `prefix` (a key, or nothing), the last ended by `suffix` (a comma, or nothing).

        `opened` opens a non-empty container whether or not it would fit.
        """
        value = self.convert(value)
        indent = INDENT * depth
        if not isinstance(value, _CONTAINERS) or not value:
            self.lines.append(f"{indent}{prefix}{self.text(value)}{suffix}")
            return
        if (
            not opened
            and len(indent) + len(prefix) + self.size(value) + len(suffix) <= self.width
        ):
            self.lines.append(f"{indent}{prefix}{self.texts[id(value)]}{suffix}")
            return
        if isinstance(value, dict):
            items = sorted(value.items()) if self.encoder.sort_keys else list(value.items())
            self.lines.append(f"{indent}{prefix}{{")
            last = len(items) - 1
            for index, (name, item) in enumerate(items):
                comma = "," if index < last else ""
                self.write(item, depth + 1, f"{self.key(name)}: ", comma)
            self.lines.append(f"{indent}}}{suffix}")
            return
        elements = [self.convert(item) for item in value]
        self.lines.append(f"{indent}{prefix}[")
        if any(isinstance(item, _CONTAINERS) for item in elements):
            last = len(elements) - 1
            for index, item in enumerate(elements):
                self.write(item, depth + 1, "", "," if index < last else "")
        else:
            self.fill([self.text(item) for item in elements], INDENT * (depth + 1))
        self.lines.append(f"{indent}]{suffix}")

    def fill(self, texts: list[str], indent: str) -> None:
        """Scalars as many to a line as fit, every line but the last ending in a comma.

        A scalar wider than the line by itself still takes a line of its own.
        """
        row: list[str] = []
        length = 0  # of ",".join(row)
        last = len(texts) - 1
        for index, text in enumerate(texts):
            comma = 1 if index < last else 0
            if row and len(indent) + length + 1 + len(text) + comma > self.width:
                self.lines.append(f"{indent}{','.join(row)},")
                row, length = [], 0
            length += len(text) + (1 if row else 0)
            row.append(text)
        self.lines.append(f"{indent}{','.join(row)}")

    def size(self, value: Any) -> int:
        """The length of the compact text of `value`, a converted container, measured once.

        A container no wider than the width keeps its text too, joined from its children's,
        so the line that writes it encodes nothing again. The loop writes the common exact
        types itself, as `text` and `key` would, because it runs once per value.
        """
        identity = id(value)
        known = self.sizes.get(identity)
        if known is not None:
            return known
        if identity in self.measuring:
            message = "Circular reference detected"
            raise ValueError(message)
        is_dict = isinstance(value, dict)
        if _SCALAR_TYPES.issuperset(map(type, value.values() if is_dict else value)) and (
            not is_dict or _STRING_KEYS.issuperset(map(type, value))
        ):
            text = self.compact(value)
            total = len(text)
            if total <= self.width:
                self.texts[identity] = text
            self.sizes[identity] = total
            return total
        self.measuring.add(identity)
        width, texts, keys, string, compact = (
            self.width,
            self.texts,
            self.keys,
            self.string,
            self.compact,
        )
        foreign = self.default is not None
        # Two brackets and a comma between elements, and in an object a colon after each
        # key. A partial total is a lower bound, so the pieces stop once it passes the width.
        total = 1 + len(value)
        pieces: list[tuple[Any, str]] | None = []
        for name, child in value.items() if is_dict else enumerate(value):
            if is_dict:
                key = keys.get(name) if type(name) is str else None
                if key is None:
                    key = self.key(name) + ":"
            else:
                key = ""
            item = self.convert(child) if foreign else child
            kind = type(item)
            if kind is list and _SCALAR_TYPES.issuperset(map(type, item)):
                # A list of scalars, the commonest container, measured here rather than
                # through `size`; it is measured again only if this container opens.
                piece = key + compact(item)
                total += len(piece)
            elif kind is dict or kind is list or isinstance(item, _CONTAINERS):
                total += len(key) + self.size(item)
                if pieces is None:
                    continue
                piece = key + texts.get(id(item), "")
            else:
                if kind is str:
                    piece = key + string(item)
                elif kind is float and math.isfinite(item):
                    piece = key + float.__repr__(item)
                elif kind is int:
                    piece = key + int.__repr__(item)
                else:
                    piece = key + self.text(item)
                total += len(piece)
            if pieces is not None:
                if total > width:
                    pieces = None
                else:
                    pieces.append((name, piece))
        self.measuring.discard(identity)
        if pieces is not None:
            if is_dict and self.encoder.sort_keys:
                pieces.sort(key=_name)
            opening, closing = ("{", "}") if is_dict else ("[", "]")
            texts[identity] = opening + ",".join(piece for _, piece in pieces) + closing
        self.sizes[identity] = total
        return total

    def convert(self, value: Any) -> Any:
        """`value`, or what `default` makes of it if `json` cannot write it.

        Converted once and kept, so a converted object is measured and laid out as what it
        became; anything still foreign goes to the encoder, which applies `default` again
        under its own circular-reference check.
        """
        if self.default is None or isinstance(value, _NATIVE):
            return value
        identity = id(value)
        if identity not in self.converted:
            self.converted[identity] = self.default(value)
        return self.converted[identity]

    def text(self, value: Any) -> str:
        """A value the layout never opens -- a scalar, an empty container, anything still
        foreign -- as the encoder writes it. The common exact types are written here,
        each the way the encoder writes it; the rest are left to the encoder."""
        kind = type(value)
        if kind is str:
            return self.string(value)
        if kind is float and math.isfinite(value):
            return float.__repr__(value)
        if kind is int:
            return int.__repr__(value)
        if value is None or kind is bool:
            return _LITERALS[value]
        return self.compact(value)

    def key(self, name: Any) -> str:
        """An object key as the encoder writes it, a string key cached with its colon."""
        if type(name) is not str:
            return _key(name, self.encoder)
        text = self.keys.get(name)
        if text is None:
            text = self.keys[name] = self.string(name) + ":"
        return text[:-1]


def _name(piece: tuple[Any, str]) -> Any:
    return piece[0]


def _key(key: Any, encoder: json.JSONEncoder) -> str:
    """An object key as the encoder writes it.

    Encoding a one-entry object and cutting the key out of it keeps every rule `json` has for
    keys -- numbers and booleans turned to strings, other types refused, `ensure_ascii` --
    without restating any of them here.
    """
    text = encoder.encode({key: None})
    return text[1 : -len(_NULL_VALUE_SUFFIX)]
