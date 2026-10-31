#!/usr/bin/env python3
"""Complete zm_mixed.py check of the s(44) = 7 certificate, in two stages, resumable.

Stage A: the whole D4 root grid (9,800 roots), split into 35 x-columns, at --depth 24.
Stage B: every root that stage A left with uncertified boxes, swept again in full at --depth 30.
The certificate is verified when every D4 root finished stage A, and every root with uncertified boxes in
stage A has a stage-B run with 0 uncertified boxes.  This is exactly the procedure behind the logs in
verification/logs/zm_mixed/ (there, 24 of the 27 stage-B roots ran on a Mac and 3 in the cloud).

Usage (from the repository root, after verify.sh has cloned the pinned checkers into build/square-packing):
  python3 verification/zm_mixed_check.py run   [--jobs N]     # run (or resume) both stages, then audit
  python3 verification/zm_mixed_check.py audit [DIR]          # audit finished runs; default build/zm,
                                                              # or verification/logs/zm_mixed for our logs
Cost: about 140 CPU-hours in total (stage A ~110, stage B ~30); wall time = that / number of cores.
Each job writes its own resume file, so the run can be stopped (Ctrl-C) and restarted at any time.
"""
import glob, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CERT = os.path.join(ROOT, 'certificate', 's44_cover_7.txt')
SHA = 'c9fde0f1e7013f3f61f4a8d673b6bcaf9c5e54c914b6462164d7326ba254cae0'
CHK = os.path.join(ROOT, 'build', 'square-packing', 'search')
OUT = os.path.join(ROOT, 'build', 'zm')
BASE = ['--d4', '--nproc', '1', '--disj', '--chain-from', '0']


def jsonl_records(path):
    for line in open(path):
        d = json.loads(line)
        if 'root' in d:
            yield tuple(d['root']), d.get('unc') or []


def run_one(tag, depth, region):
    if os.path.exists(os.path.join(OUT, tag + '.done')):
        return tag
    cmd = [sys.executable, 'zm_mixed.py', 'cert', CERT, *BASE, '--depth', str(depth), *region,
           '--resume', os.path.join(OUT, tag + '.jsonl'), '--manifest', os.path.join(OUT, tag + '_manifest.json')]
    with open(os.path.join(OUT, tag + '.out'), 'a') as log:
        subprocess.run(cmd, cwd=CHK, stdout=log, stderr=subprocess.STDOUT)
    if 'UNCERTIFIED' in open(os.path.join(OUT, tag + '.out')).read():   # the run reached its summary line
        open(os.path.join(OUT, tag + '.done'), 'w').close()
    print('finished', tag, flush=True)
    return tag


def stage_b_roots(d):
    bad = {}
    for f in sorted(glob.glob(os.path.join(d, 'col*.jsonl'))):
        for r, u in jsonl_records(f):
            if u: bad[r] = len(u)
    return bad


def region_of(r):
    cx0, cx1, cy0, cy1, u0, u1 = r
    reg = ['--cx-lo', cx0, '--cx-hi', cx1, '--cy-lo', cy0, '--cy-hi', cy1, '--u-hi', u1]
    if F(u0) > 0: reg += ['--u-lo', u0]
    return reg


def run(jobs):
    import hashlib
    assert hashlib.sha256(open(CERT, 'rb').read()).hexdigest() == SHA, 'certificate hash mismatch'
    assert os.path.exists(os.path.join(CHK, 'zm_mixed.py')), 'run verification/verify.sh --fast first (clones the checkers)'
    os.makedirs(OUT, exist_ok=True)
    cols = [12] + [j for j in range(35) if j != 12]           # column 12 is the slowest: start it first
    with ThreadPoolExecutor(jobs) as ex:
        list(ex.map(lambda j: run_one(f'col{j:02d}', 24, ['--cx-lo', f'{j}/10', '--cx-hi', f'{j + 1}/10']), cols))
    bad = stage_b_roots(OUT)
    print(f'stage A done; {len(bad)} roots go to stage B (depth 30)', flush=True)
    with ThreadPoolExecutor(jobs) as ex:
        list(ex.map(lambda ir: run_one(f'deep{ir[0]:02d}', 30, region_of(ir[1])), enumerate(sorted(bad))))
    return audit(OUT)


def audit(d):
    sys.path.insert(0, CHK if os.path.exists(CHK) else os.path.join(ROOT, 'build'))
    try:
        import zeromargin as zm
        want = {tuple(str(v) for v in r) for r in zm.d4_roots(F(7), F(1, 10), 8)}
    except ImportError:
        want = None
    A = {}
    for f in glob.glob(os.path.join(d, '**', 'col*.jsonl'), recursive=True):
        for r, u in jsonl_records(f): A[r] = u
    B = {}
    for f in glob.glob(os.path.join(d, '**', '*.jsonl'), recursive=True):
        if os.path.basename(f).startswith('col'): continue
        hdr = json.loads(open(f).readline())
        if hdr.get('settings', {}).get('depth') != 30 or hdr.get('sha256', {}).get('input') != SHA: continue
        for r, u in jsonl_records(f):
            if not u: B[r] = True
    bad = [r for r, u in A.items() if u]
    print(f'stage A: {len(A)} roots finished' + (f' of {len(want)} expected' if want else ''))
    missing = sorted(want - set(A)) if want else []
    if want is None: print('  (zeromargin.py not found: root-grid completeness not checked; clone the checkers first)')
    print(f'stage A: {len(bad)} roots with uncertified boxes ({sum(len(A[r]) for r in bad)} boxes)')
    open_ = [r for r in bad if r not in B]
    print(f'stage B: {len(bad) - len(open_)} of them re-swept at depth 30 with 0 uncertified')
    ok = not missing and not open_ and want is not None
    for r in missing[:5]: print('  missing root', r)
    for r in open_[:5]: print('  root still uncertified', r)
    print('RESULT:', 'VERIFIED-D4 (complete)' if ok else 'NOT VERIFIED / INCOMPLETE')
    return 0 if ok else 1


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] not in ('run', 'audit'):
        print(__doc__); sys.exit(2)
    if a[0] == 'run':
        n = int(a[a.index('--jobs') + 1]) if '--jobs' in a else os.cpu_count()
        sys.exit(run(n))
    sys.exit(audit(a[1] if len(a) > 1 else OUT))
