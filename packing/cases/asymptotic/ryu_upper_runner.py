"""Run one retained program of Ryu's k2-minus-c-upper preprint as its author ran it.

The programs import their siblings (``run_z.py`` imports ``r38`` and ``chk``), which
plain ``python script.py`` allows because it puts the script's folder first on the import
path. A replay here runs under ``python -I``, which does not, so this runner puts that
folder *last* on the path and runs the script as ``__main__``: the standard library and
the installed packages are always found first, and a file in the retained folder can only
supply a name nothing else does. ``ryu_upper_replay`` calls it; every program it runs was
read before it was first replayed (the packet README lists them).

Usage::

    python -I cases/asymptotic/ryu_upper_runner.py /abs/path/to/program.py [ARGS...]
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


def main() -> None:
    script = Path(sys.argv[1]).resolve()
    sys.argv = [str(script), *sys.argv[2:]]
    sys.path.append(str(script.parent))
    runpy.run_path(str(script), run_name="__main__")


if __name__ == "__main__":
    main()
