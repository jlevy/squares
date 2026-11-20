"""Lane r1012: rewrite a corners certificate with ids 1..n, values unchanged.

Usage: r1012_renumber.py CERTIFICATE OUT.yaml

Written after the findings' freeze. This repository's witness-corners adapter reads
squares numbered 1 to n in order, and the certificate numbers them square-0 to
square-108. This program reads the certificate through r1012_reader, writes the same
side and corners, in the same order, with ids 1 to n through r1012_writer, reads the
result back and checks that the side and every corner are unchanged. It decides
nothing.
"""

import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.set_int_max_str_digits(0)

import r1012_reader  # noqa: E402
import r1012_writer  # noqa: E402


def main(argv):
    src, out = argv[1], argv[2]
    p = r1012_reader.read_path(src)
    n = p["n"]
    text = r1012_writer.write(n, p["side"], list(range(1, n + 1)), p["corners"])
    back = r1012_reader.read_bytes(text)
    if back["side"] != p["side"] or back["corners"] != p["corners"]:
        print("values changed")
        return 2
    with open(out, "wb") as handle:
        handle.write(text)
    print(f"renumbered {n} squares 1..{n}; source sha256 {p['sha256']}; "
          f"written sha256 {hashlib.sha256(text).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
