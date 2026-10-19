"""Triage diagnostic for #594: write the drop-heaviest-point and drop-heaviest-segment mutants
of the s(76) cover with the repository's own devtools.replay_evand_zmx2.mutate, and print
where the dropped mass sits (the zmx2 root cells to run each control on).

usage: python -I make_mutants.py PACKING_DIR COVER OUT_DIR
"""

import hashlib
import sys
from pathlib import Path

packing, cover, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(packing))
from devtools.replay_evand_zmx2 import mutate  # noqa: E402

text = cover.read_text()
for kind in ("drop-heaviest-point", "drop-heaviest-segment"):
    m = mutate(text, kind)
    path = out / f"s76_{kind}.txt"
    path.write_text(m.text)
    print(kind, m.detail, "removed", m.removed, "rows", m.rows if hasattr(m, "rows") else "",
          "sha256", hashlib.sha256(m.text.encode()).hexdigest())
