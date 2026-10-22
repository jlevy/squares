"""Measure Francisco Couzo's in-corpus certificates of issues 670, 672 and 675 pose by pose.

Written for the registration of those rows (think-2vjc, think-f28n, think-pvav, 22
October 2026), from the stage 1 triage's measurement program (c-triage-backlog-1022),
with its inputs read from the retained packets instead of fetched copies. A measurement
for credit; it decides nothing. It loads the measurement functions of the
evand-regularized-2026-10-20 packet's measure/identity.py from that file
(`certificate`, `centre_basis`, `measure`: the nearest centre under each of the box's
eight symmetries, kept only where one to one, and an optimal assignment of least total
squared centre displacement, scipy in binary64; exact sides and differences exact), and
measures:

- #672 at 229 against de Winter's #668 witness (T-196), the packing the author's comment
  names as its start;
- T-198 and T-199 (Evan Daniel's #674 opening and update) against #672 at 229, which
  #674 names as its start;
- #675 against #670 at 204, and T-223 (#678) against each, Couzo's own sequence.

#672 at 227 against T-196 and against T-225's view is in the evand-regularized packet's
measure/identity.json, which read #672's certificate from a fetched copy with the same
SHA-256 as the one retained here.

Usage, from packing/ with the project interpreter:
    python resources/web/couzo-issue672-2026-10-17/measure/identity.py \
        --out resources/web/couzo-issue672-2026-10-17/measure/identity.json
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

WEB = Path("resources/web")


def _functions():  # noqa: ANN202 -- a module loaded from a retained file
    sys.path[:0] = [str(Path.cwd()), str(Path.cwd() / "src")]
    path = WEB / "evand-regularized-2026-10-20/measure/identity.py"
    spec = importlib.util.spec_from_file_location("evand_regularized_identity", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", 1)[0])
    parser.add_argument("--out", type=Path, required=True)
    arguments = parser.parse_args(argv)
    m = _functions()
    p672_229 = m.certificate(WEB / "couzo-issue672-2026-10-17/source/certificates/n229.cert")
    p670_204 = m.certificate(WEB / "couzo-issue670-2026-10-17/source/certificates/n204.cert")
    p675_204 = m.certificate(WEB / "couzo-issue675-2026-10-18/source/certificates/best/n204.cert")
    t196_229 = m.centre_basis(
        WEB / "de-winter-upper-bounds-227-229-260-2026-10-17/source/n229/n229_exact.json.gz"
    )
    t198 = m.certificate(
        WEB / "evand-n229-dilation-2026-10-17/source/search/packer/candidates/s229.cert"
    )
    t199 = m.certificate(
        WEB / "evand-n229-dilation-update-2026-10-18/source/search/packer/candidates/s229_v2.cert"
    )
    t223_204 = m.certificate(WEB / "couzo-issue678-2026-10-18/source/certificates/best/n204.cert")
    pairs = [
        (229, "#672", "T-196 (#668)", p672_229, t196_229),
        (229, "T-198 (#674 opening)", "#672", t198, p672_229),
        (229, "T-199 (#674 update)", "#672", t199, p672_229),
        (204, "#675", "#670", p675_204, p670_204),
        (204, "T-223 (#678)", "#675", t223_204, p675_204),
        (204, "T-223 (#678)", "#670", t223_204, p670_204),
    ]
    out = []
    for n, view, against, first, second in pairs:
        row = {"n": n, "view": view, "against": against, **m.measure(first, second)}
        out.append(row)
        found = row["assignment"]
        print(
            n, view, "vs", against, "one to one", row["nearest_centre"].get("one_to_one"),
            "moved", found["moved_beyond"], "largest", found["largest_move"],
            "turn", found["largest_turn_degrees"], flush=True,
        )  # fmt: skip
    arguments.out.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
