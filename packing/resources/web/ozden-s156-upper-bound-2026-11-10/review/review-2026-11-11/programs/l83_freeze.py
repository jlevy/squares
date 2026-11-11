"""Write the SHA-256 of named files with a UTC time (review L83).

Usage: python -I -B l83_freeze.py OUT.txt LABEL FILE...
"""

import hashlib
import sys
from datetime import UTC, datetime
from pathlib import Path


def main(argv: list[str]) -> int:
    out, label, files = Path(argv[1]), argv[2], [Path(p) for p in argv[3:]]
    lines = [f"# {label}", f"# frozen {datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')}"]
    for p in files:
        lines.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}")
    out.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print("digest of this list:", hashlib.sha256(out.read_bytes()).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
