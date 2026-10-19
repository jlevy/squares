"""A214 -- A213's stage table plus the C-kernel rows:  python code/stages214.py off.prof on.prof
(stages213.py is used read-only; its ROWS list is extended, not edited.)"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "A213-int-polycore", "code")))
import stages213 as S                                          # noqa: E402  READ-ONLY (A213)

S.ROWS = S.ROWS[:-1] + [
    ("    ckernel214.vertex_ok_h (C, scalar)", [("ckernel214.py", "vertex_ok_h")]),
    ("    ckernel214.certify_h (C, batch)", [("ckernel214.py", "certify_h")]),
    ("    ckernel214.cbox_of (the per-box compile)", [("ckernel214.py", "cbox_of")]),
] + S.ROWS[-1:]

if __name__ == "__main__":
    S.main()
