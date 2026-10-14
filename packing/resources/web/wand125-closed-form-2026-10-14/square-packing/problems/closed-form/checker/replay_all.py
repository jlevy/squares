#!/usr/bin/env python3
"""Replay every record of the closed-form certificate with replay4d.

Usage (from problems/closed-form):

    python3 checker/replay_all.py --assets DIR [--threads T] [--jobs J] [--only 1,2,34] [--work DIR]

DIR holds the release assets interval_<d0>_<d1>.tar.gz. For each interval listed in intervals.json the script
checks the tarball's SHA-256, unpacks it, checks the SHA-256 of every member, runs

    checker/target/release/replay4d <family> <region>.rec --region x0 x1 y0 y1 --threads T --out <result>.json

for the four regions, and checks that replay4d prints REPLAY OK and that its root and leaf counts match
intervals.json. Results are written to <work>/results/. A region that already has an OK result is skipped, so the
script can be stopped and restarted. Python 3 standard library only.
"""
import argparse, concurrent.futures as cf, hashlib, json, os, subprocess, sys, tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REGIONS = ('straddle', 'left', 'top', 'right')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
    return h.hexdigest()


def unpack(iv, assets, work):
    tag = iv['asset'][:-len('.tar.gz')]; d = os.path.join(work, tag)
    if not os.path.isdir(d):
        tp = os.path.join(assets, iv['asset'])
        if sha(tp) != iv['asset_sha256']: sys.exit(f'{iv["asset"]}: SHA-256 mismatch')
        with tarfile.open(tp) as t:
            for m in t.getmembers():
                if not (m.isfile() and m.name.startswith(tag + '/') and '..' not in m.name): sys.exit(f'{iv["asset"]}: unexpected member {m.name}')
            t.extractall(work, filter='data') if sys.version_info >= (3, 12) else t.extractall(work)
    want = {'family.json': iv['family_sha256'], 'family_right.json': iv['family_right_sha256']}
    want.update({g['file']: g['sha256'] for g in iv['regions'].values()})
    for f, h in want.items():
        if sha(os.path.join(d, f)) != h: sys.exit(f'{tag}/{f}: SHA-256 mismatch')
    return tag, d


def run(binary, tag, d, reg, g, threads, res):
    out = os.path.join(res, f'{tag}.{reg}.json')
    if os.path.exists(out) and json.load(open(out)).get('ok') is True: return tag, reg, 'skipped (already OK)'
    cmd = [binary, os.path.join(d, g['family']), os.path.join(d, g['file']), '--region', *g['bounds'],
           '--threads', str(threads), '--out', out + '.tmp']
    p = subprocess.run(cmd, capture_output=True, text=True)
    last = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ''
    if last != 'REPLAY OK': return tag, reg, f'FAILED: {last or p.stderr.strip()[-200:]}'
    o = json.load(open(out + '.tmp'))
    if o['roots'] != g['roots'] or sum(o['kinds'].values()) != g['leaves']:
        return tag, reg, f'FAILED: counts differ from intervals.json ({o["roots"]} roots, {sum(o["kinds"].values())} leaves)'
    os.replace(out + '.tmp', out)
    return tag, reg, f'REPLAY OK ({o["roots"]} roots, {sum(o["kinds"].values())} leaves)'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--assets', required=True); ap.add_argument('--threads', type=int, default=os.cpu_count() or 1)
    ap.add_argument('--jobs', type=int, default=1, help='regions replayed at the same time')
    ap.add_argument('--only', default='', help='comma-separated interval numbers (1-34)'); ap.add_argument('--work', default='replay-work')
    a = ap.parse_args()
    binary = os.path.join(HERE, 'target', 'release', 'replay4d')
    if not os.path.exists(binary): sys.exit('build the checker first: (cd checker && cargo build --locked --release -p replay4d)')
    ivs = json.load(open(os.path.join(ROOT, 'intervals.json')))['intervals']
    if a.only: ivs = [iv for iv in ivs if str(iv['index']) in a.only.split(',')]
    res = os.path.join(a.work, 'results'); os.makedirs(res, exist_ok=True)
    tasks = []
    for iv in ivs:
        tag, d = unpack(iv, a.assets, a.work)
        tasks += [(tag, d, reg, iv['regions'][reg]) for reg in REGIONS]
    bad = 0
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for tag, reg, msg in ex.map(lambda t: run(binary, t[0], t[1], t[2], t[3], a.threads, res), tasks):
            print(f'{tag} {reg}: {msg}', flush=True); bad += msg.startswith('FAILED')
    print('ALL REPLAY OK' if not bad else f'{bad} region(s) FAILED')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
