#!/usr/bin/env python3
"""Lean modules from the pickled certificates of run_v7.py: one module per root, the pair
certificates encoded (`LemmaEDec.decPC`, `enc_cert.py`).

    emit_v7.py --cert DIR --out DIR [--lo I --hi J] [--nproc N]
"""
import argparse, glob, os, pickle, sys
sys.set_int_max_str_digits(0)
from multiprocessing import Pool
from types import SimpleNamespace

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_exact as G  # noqa: E402
from gen_tree import Glue  # noqa: E402
from enc_cert import enc_pc, enc_sb  # noqa: E402
import capk  # noqa: E402
from run_v7 import SG, RG, MQ, sorted_cover  # noqa: E402


def lean_pc(c):
    """a pair certificate: one encoded number list, or (`XMODE`) one per sub-bin"""
    if not XMODE:
        return "decPC [" + ",".join(map(str, enc_pc(c))) + "]"
    if c == 'par':
        return "PairCert.par"
    return "PairCert.bins [" + ", ".join("decSB [" + ",".join(map(str, enc_sb(sb))) + "]" for sb in c) + "]"


def to_lean_enc(lf, name):
    rows = ",\n    ".join("[" + ", ".join(lean_pc(c) for c in row) + "]" for row in lf.certs)
    return (f"def {name} : ExLeaf where\n"
            f"  wx := {'true' if lf.wx else 'false'}\n  wy := {'true' if lf.wy else 'false'}\n"
            f"  chs := [{', '.join(G.ltup(e) for e in lf.chs)}]\n"
            f"  cvs := [{', '.join(G.ltup(e) for e in lf.cvs)}]\n"
            f"  crs := [{', '.join(G.lrm(r) for r in lf.crs)}]\n"
            f"  Ls := [{', '.join(G.lPL(P) for P in lf.Ls)}]\n"
            f"  hbx := [{', '.join(G.lbx(b) for b in lf.hbx)}]\n"
            f"  vbx := [{', '.join(G.lbx(b) for b in lf.vbx)}]\n"
            f"  certs := [\n    {rows}]\n"
            + ("  ex := true\n" if lf.ex else "") + ("  ey := true\n" if lf.ey else "")
            + G.lcred(getattr(lf, 'cred', None)))


G.to_lean = to_lean_enc
_rects = None


def emit(path, outdir):
    global _rects
    if _rects is None:
        _rects = sorted_cover()[5]
    d = pickle.load(open(path, 'rb'))
    idx, root, tree = d['idx'], d['root'], d['tree']
    g = Glue(5, SG, RG, 10 ** 12, MQ)
    body = []
    for b, c in d['leaves'].items():
        if 'capk' in c:
            body.append(capk.to_lean(c['capk'], c['name'], 5, c['S'], c['R'], 10 ** 12, c['box']))
            g.leaf_names[b] = (f"{c['name']}_ok", c['S'], c['R'], 'cap')
            continue
        lf = SimpleNamespace(**c)
        body.append(G.to_lean_split(lf, c['name']))
        g.leaf_names[b] = (f"{c['name']}_ok", c['S'], c['R'])
    hdr = ["import Sqpack.V7.Data", "import Sqpack.LemmaEDec", "import Sqpack.CapK", "namespace SquarePacking.LemmaELeaf",
           "open ZMTreeM LemmaEVert LemmaEPoly ZMTree LemmaE", "set_option maxRecDepth 100000",
           "set_option maxHeartbeats 0"]
    txt = "\n".join(hdr + body + [g.root_thm(f"root_{idx:05d}", root, tree, _rects),
                                  "end SquarePacking.LemmaELeaf"]) + "\n"
    out = os.path.join(outdir, f"R{idx:05d}.lean")
    with open(out + ".tmp", 'w') as f:
        f.write(txt)
    os.replace(out + ".tmp", out)
    return idx, len(txt)


XMODE = os.environ.get('V7_X', '0') == '1'   # EXACT leaves through `LemmaELeafX` (rows' minima)
HDR = ["import Sqpack.V7.Data", "import Sqpack.LemmaEDec", "import Sqpack.LemmaESplit", "import Sqpack.CapK"] + \
    (["import Sqpack.ExTreeX", "import Sqpack.LemmaESplitX"] if XMODE else [])
OPEN = ["noncomputable section  -- checked by the kernel only: no compiled code",
        "namespace SquarePacking.LemmaELeaf", "open ZMTreeM LemmaEVert LemmaEPoly ZMTree LemmaE",
        "set_option maxRecDepth 100000", "set_option maxHeartbeats 0"]


def _write(path, txt):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + ".tmp", 'w') as f:
        f.write(txt)
    os.replace(path + ".tmp", path)


def emit_split(path, outdir, chunk):
    """one module per leaf (definitions and head), one per group of rows (at most `chunk` pair
    theorems), and the root module (the leaves' `exOk` and the root theorem)"""
    global _rects
    if _rects is None:
        _rects = sorted_cover()[5]
    d = pickle.load(open(path, 'rb'))
    idx, root, tree = d['idx'], d['root'], d['tree']
    g = Glue(5, SG, RG, 10 ** 12, MQ)
    rdir = f"R{idx:05d}"
    imports, oks, total = [], [], 0
    for b, c in d['leaves'].items():
        name = c['name']
        if 'capk' in c:
            txt = "\n".join(HDR + OPEN + [capk.to_lean(c['capk'], name, 5, c['S'], c['R'], 10 ** 12, c['box']),
                                           "end SquarePacking.LemmaELeaf"]) + "\n"
            _write(os.path.join(outdir, rdir, f"{name}.lean"), txt); total += len(txt)
            imports.append(f"import Sqpack.V7.{rdir}.{name}")
            g.leaf_names[b] = (f"{name}_ok", c['S'], c['R'], 'cap')
            continue
        lf = SimpleNamespace(**c)
        defs, rows, ok = G.to_lean_parts(lf, name, X=XMODE)
        base = f"Sqpack.V7.{rdir}.{name}"
        txt = "\n".join(HDR + OPEN + [defs, "end SquarePacking.LemmaELeaf"]) + "\n"
        _write(os.path.join(outdir, rdir, f"{name}.lean"), txt); total += len(txt)
        groups, cur, size = [], [], 0
        for r in rows:
            k = r.count("theorem ")
            if cur and size + k > chunk:
                groups.append(cur); cur, size = [], 0
            cur.append(r); size += k
        if cur: groups.append(cur)
        for gi, grp in enumerate(groups):
            txt = "\n".join([f"import {base}"] + OPEN + grp + ["end SquarePacking.LemmaELeaf"]) + "\n"
            _write(os.path.join(outdir, rdir, f"{name}_g{gi}.lean"), txt); total += len(txt)
            imports.append(f"import {base}_g{gi}")
        oks.append(ok)
        g.leaf_names[b] = (f"{name}_ok", c['S'], c['R']) + (('x',) if XMODE else ())
    txt = "\n".join(HDR + imports + OPEN + oks + [g.root_thm(f"root_{idx:05d}", root, tree, _rects),
                                                    "end SquarePacking.LemmaELeaf"]) + "\n"
    _write(os.path.join(outdir, f"{rdir}.lean"), txt); total += len(txt)
    return idx, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cert', default=os.path.join(HERE, '..', 'v7cert'))
    ap.add_argument('--out', default=os.path.join(HERE, '..', 'Sqpack', 'V7'))
    ap.add_argument('--lo', type=int, default=0)
    ap.add_argument('--hi', type=int, default=10 ** 9)
    ap.add_argument('--mod', type=int, default=1, help='only the roots with index %% MOD == REM')
    ap.add_argument('--rem', type=int, default=0)
    ap.add_argument('--nproc', type=int, default=1)
    ap.add_argument('--chunk', type=int, default=0, help='split modules: pair theorems per row group (0: one module per root)')
    a = ap.parse_args()
    paths = sorted(p for p in glob.glob(os.path.join(a.cert, 'R*.pkl'))
                   if a.lo <= int(os.path.basename(p)[1:6]) < a.hi and int(os.path.basename(p)[1:6]) % a.mod == a.rem)
    with Pool(a.nproc) as pool:
        tot = 0
        jobs = [(p, a.out, a.chunk) for p in paths] if a.chunk else [(p, a.out) for p in paths]
        for idx, n in pool.starmap(emit_split if a.chunk else emit, jobs):
            tot += n
    print(len(paths), "modules", tot, "bytes")


if __name__ == '__main__':
    main()
