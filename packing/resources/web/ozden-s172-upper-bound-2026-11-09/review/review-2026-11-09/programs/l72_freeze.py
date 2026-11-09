"""Write a frozen-digest file for a list of program files (lane L72, bead think-qqyg).

Usage: python -I -B l72_freeze.py OUT.txt HEADER.txt FILE...

The header's lines are written as comments, then one 'sha256  basename' line per file,
with the UTC time of writing in the first line. Decides nothing.
"""

import hashlib
import os
import sys
import time


def main(argv):
    out, header, files = argv[1], argv[2], argv[3:]
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(header, encoding="utf-8") as fh:
        lines = fh.read().rstrip("\n").split("\n")
    body = [f"# {lines[0].replace('{STAMP}', stamp)}"] + [f"# {x}".rstrip() for x in lines[1:]]
    body.append("#")
    body.append("# sha256  file")
    for f in files:
        with open(f, "rb") as fh:
            body.append(f"{hashlib.sha256(fh.read()).hexdigest()}  {os.path.basename(f)}")
    text = "\n".join(body) + "\n"
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(text)
    sys.stdout.write(text)
    sys.stdout.write(f"digest of {os.path.basename(out)}: {hashlib.sha256(text.encode()).hexdigest()}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
