"""Write every frontier record's derivable algebraic facts, and say where each came from.

For each `frontier/n-NNN.md`, `sqpack.exact_values.algebraic_fields` decides the
`reported_upper_bound`'s `algebraic_degree`, `minimal_polynomial` and
`algebraic_source` from what the record already holds:

- a degree the catalogue prints is kept, with its polynomial, as `catalogue`;
- a closed form fixes both, which are derived from it as `derived-from-exact-form`;
- otherwise all three stay null.

Only those three lines of the front matter change, written as
`devtools.generate_frontier_case` writes them, so a regenerated draft and a backfilled
record agree. A record whose source is `contact-system` is left as it is: that fact was
computed from evidence this tool does not read. Closes think-kj6n.

Usage, from `packing/`:

    uv run --frozen --all-extras --group dev python -m devtools.backfill_algebraic_facts
    uv run --frozen --all-extras --group dev python -m devtools.backfill_algebraic_facts --check
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Sequence
from pathlib import Path

import yaml
from strif import atomic_output_file

from sqpack.exact_values import CATALOGUE, CONTACT_SYSTEM, algebraic_fields
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
CASES = range(1, 325)

FIELDS = ("algebraic_degree", "minimal_polynomial", "algebraic_source")
#: The reported upper bound's own keys sit at four spaces under `packing:`.
_KEY = re.compile(r"^    (?P<key>[a-z_]+):")
_BLOCK = "  reported_upper_bound:"


class BackfillError(RuntimeError):
    """A record whose front matter this tool cannot edit in place."""


def _fields_text(fields: dict[str, object]) -> list[str]:
    dumped = yaml.safe_dump(fields, allow_unicode=True, sort_keys=False, width=96)
    return ["    " + line if line else line for line in dumped.splitlines()]


def backfilled(text: str, n: int) -> str:
    """The record's text with its three algebraic lines rewritten."""
    _, front, body = text.split("---", 2)
    reported = safe_load(front)["packing"]["reported_upper_bound"]
    if reported.get("algebraic_source") == CONTACT_SYSTEM:
        return text
    # A degree is the catalogue's to keep only where the record says the catalogue printed
    # it, or where no source is recorded yet (a record from before the field existed). A
    # derived pair is recomputed from the closed form, so a second run changes nothing.
    printed = reported.get("algebraic_source") in {CATALOGUE, None}
    # These owner writers derive identities from complete finite source certificates.
    # Their legacy n51 polynomial omitted provenance; it was never a Kingbird claim.
    if reported.get("source_key") in {
        "[ry-xu square packing 2026]",
        "[Gupta rational refinements 2026-10-08]",
    }:
        printed = False
    fields = algebraic_fields(
        reported.get("exact_form"),
        reported.get("algebraic_degree") if printed else None,
        reported.get("minimal_polynomial") if printed else None,
    )
    lines = front.split("\n")
    try:
        start = lines.index(_BLOCK)
    except ValueError as error:
        raise BackfillError(f"n={n}: no {_BLOCK.strip()} block") from error
    kept: list[str] = []
    insert_at: int | None = None
    index = start + 1
    end = len(lines)
    while index < end:
        line = lines[index]
        if line and not line.startswith("   "):
            end = index
            break
        match = _KEY.match(line)
        if match and match["key"] in FIELDS:
            if insert_at is None:
                insert_at = len(kept)
            index += 1
            # Skip the value's continuation lines, which sit deeper than the key.
            while index < len(lines) and lines[index].startswith("     "):
                index += 1
            continue
        kept.append(line)
        index += 1
    if insert_at is None:
        raise BackfillError(f"n={n}: reported_upper_bound has no algebraic_degree line")
    block = kept[:insert_at] + _fields_text(fields) + kept[insert_at:]
    new_front = "\n".join([*lines[: start + 1], *block, *lines[end:]])
    return f"---{new_front}---{body}"


def run(*, check: bool) -> int:
    changed: list[int] = []
    for n in CASES:
        path = FRONTIER / f"n-{n:03d}.md"
        text = path.read_text(encoding="utf-8")
        new = backfilled(text, n)
        if new == text:
            continue
        changed.append(n)
        if not check:
            with atomic_output_file(path) as temporary:
                Path(temporary).write_text(new, encoding="utf-8")
    verb = "would change" if check else "changed"
    print(f"{verb} {len(changed)} record(s)" + (f": n = {changed}" if changed else ""))
    return 1 if check and changed else 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument(
        "--check", action="store_true", help="report records that would change; write none"
    )
    args = parser.parse_args(argv)
    return run(check=args.check)


if __name__ == "__main__":
    sys.exit(main())
