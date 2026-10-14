"""A211 (A209 copy) -- the queue files: code/queue_gallery.txt (the 22 alive k5 gallery pages of docs/shadows/STATUS.md, k5_11 first)
and code/queue_frontier.txt (the alive k5 frontier of A57's census, deepest-first within a tree, the gallery pages and
every node a ledger closes excluded).  Re-run to regenerate the frontier queue after kills land (the worker also
re-checks closure per node)."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
import load211 as L                                            # noqa: E402


def alive_gallery():
    txt = open(os.path.join(ROOT, "docs", "shadows", "STATUS.md"), encoding="utf-8").read()
    out = []
    for m in re.finditer(r"\| \[ \] \[`(k5_1[16]_interior_Y\d+)\.svg`\]", txt):
        if m.group(1) not in out:
            out.append(m.group(1))
    return out


if __name__ == "__main__":
    g = alive_gallery()
    open(os.path.join(HERE, "queue_gallery.txt"), "w", newline="\n").write("\n".join(g) + "\n")      # LF only: a CRLF line would leak a CR into the nid
    c = [d["nid"] for d in L.census() if d["nid"] not in set(g)]
    open(os.path.join(HERE, "queue_frontier.txt"), "w", newline="\n").write("\n".join(c) + "\n")
    print("gallery %d: %s" % (len(g), g))
    print("frontier %d (first 10: %s)" % (len(c), c[:10]))
