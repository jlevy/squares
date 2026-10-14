"""A242 -- what the external bound s(11) > 31/8 (T-037) does to the lab's window artefacts.  DRY RUN ONLY.

    python attempts/A242-replay-31-8/code/adopt242.py --dry-run

Reads (never writes) campaign files; writes only results/adopt242_dryrun.{json,txt} in this attempt.  It never
touches CURRENT.json, a running campaign, a certificate or a verifier: adopting W' = [31/8, s0] is the
coordinator's call, and this prints the list it would act on.

Rule.  A kill record at pad lambda certifies the slab [s0/lambda, s0] (Lemma B.0 + the pads
pi_i = (lambda - 1)(i + 1 + 1/sqrt2)).  On W = [191/50, s0] a node needs a kill with s0/lambda <= 191/50; on
W' = [31/8, s0] one with s0/lambda <= 31/8, i.e. lambda >= lambda' = s0/(31/8) = 1.000538.  DEAD AT ONCE = a node
that is NOT dead on W but already dead on W' (some g1 / g2 / g3 / tube kill).  ALIVE ON W' = no kill at any
lambda >= lambda' (zero-pad kills certify s0 only).
"""
import glob, json, math, os, re, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
ATT = os.path.abspath(os.path.join(HERE, '..'))
REPO = os.path.abspath(os.path.join(ATT, '..', '..'))
RES = os.path.join(ATT, 'results')
S0, SHAT = F(969271, 250000), 3.877083590022814
W_LO, WP_LO = F(191, 50), F(31, 8)
LAM_W, LAM_WP = S0 / W_LO, S0 / WP_LO
TOL = 1e-9
RECORDS = [('A211', 'attempts/A211-coarse-tree/results/coarsetree211.jsonl'),
           ('A270', 'attempts/A270-k5-lower-slabs/results/terminal270.jsonl'),
           ('A269', 'attempts/A269-trump5-reemit/results/terminal269.jsonl')]
PAD_LAM = {'zero': 1.0, 'g1': float(F(3877084, 3861637))}          # A200 quick200.PADS (A211's two pads)
BELOW = [('A57 grid side 2 slab', 3.847016, 3.862404), ('A57 grid side 3 slab', 3.832450, 3.847780),
         ('A57 grid side 4 slab', 3.817940, 3.833212), ('A269 trump5 sub-slab', 3.82, 3.832084)]
SUPERSEDED = ['certs/measure_certificate_3.80.json', 'certs/measure_certificate_3.81.json',
              'certs/measure_certificate_3.82.json (Theorem 1 stays a Lean theorem; T-037 is an axiom)']


def pad(lam, i):
    return (lam - 1) * (i + 1 + 1 / math.sqrt(2))


def jl(path):
    p = os.path.join(REPO, path)
    if not os.path.exists(p):
        return None
    out = []
    for line in open(p, encoding='utf-8'):
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except ValueError:
                pass
    return out


def lam_of(rec, pads):
    for key in ('lam', 'lam_f'):
        if isinstance(rec.get(key), (int, float)):
            return float(rec[key])
        if isinstance(rec.get(key), str):
            return float(F(rec[key]))
    return pads.get(rec.get('pad'))


def pad_tables():
    pads = dict(PAD_LAM)
    for path in ('attempts/A270-k5-lower-slabs/results/pads270.json', 'attempts/A269-trump5-reemit/results/pads269.json'):
        try:
            d = json.load(open(os.path.join(REPO, path), encoding='utf-8'))
            for name, v in d['pads'].items():
                pads.setdefault(name, float(F(v['lam'])))
        except Exception as e:                                       # noqa: BLE001 -- report, never crash
            pads['_error_' + path] = repr(e)
    return pads


def ledger(pads):
    last, src, missing = {}, {}, []
    for tag, path in RECORDS:
        rows = jl(path)
        if rows is None:
            missing.append(path)
            continue
        for r in rows:
            nid, v = r.get('nid'), r.get('verdict')
            if not nid or v is None:
                continue
            base = re.sub(r'_r2(69|70)[a-z0-9]*$', '', nid)
            lam = lam_of(r, pads)
            key = (base, r.get('pad'))
            last[key] = (v, lam)                                     # the last pass of a (node, pad) is its state
            src[base] = tag
    nodes = {}
    for (base, p), (v, lam) in last.items():
        n = nodes.setdefault(base, {'src': src[base], 'pads': {}, 'W': False, 'Wp': False, 's0': False})
        n['pads'][p] = v
        if v == 'DEAD' and lam is not None:
            n['W'] |= lam >= float(LAM_W) - TOL
            n['Wp'] |= lam >= float(LAM_WP) - TOL
            n['s0'] = True
    once = sorted(b for b, n in nodes.items() if n['Wp'] and not n['W'])
    alive = sorted(b for b, n in nodes.items() if not n['Wp'])
    def by(L):
        d = {c: sum(1 for b in L if b.startswith(c)) for c in ('k5_11', 'k5_16', 'c0_')}
        d['other'] = len(L) - sum(d.values())
        return d
    return {'records_missing': missing, 'nodes': len(nodes), 'dead_on_W': sum(n['W'] for n in nodes.values()),
            'dead_on_Wprime': sum(n['Wp'] for n in nodes.values()), 'dead_at_once': len(once),
            'dead_at_once_by_class': by(once), 'alive_on_Wprime': len(alive), 'alive_on_Wprime_by_class': by(alive),
            'alive_on_Wprime_but_s0_dead': sum(1 for b in alive if nodes[b]['s0']),
            'dead_at_once_nodes': once, 'alive_on_Wprime_nodes': alive}


def tubes():
    out = {'certs': 0, 'reach_W': 0, 'reach_Wprime': 0, 'need_T_W': SHAT - 3.82, 'need_T_Wprime': SHAT - 3.875}
    for p in glob.glob(os.path.join(REPO, 'certs', 'tube_*.json')):
        try:
            T = float(F(json.load(open(p, encoding='utf-8'))['T']))
        except Exception:                                            # noqa: BLE001
            continue
        out['certs'] += 1
        out['reach_W'] += T >= out['need_T_W'] - TOL
        out['reach_Wprime'] += T >= out['need_T_Wprime'] - TOL
    return out


def tally(path, field='verdict'):
    rows = jl(path)
    if rows is None:
        return None
    c = {}
    for r in rows:
        k = str(r.get(field)).split(' ')[0]
        c[k] = c.get(k, 0) + 1
    return {'rows': len(rows), field: c}


def gate():
    g = {}
    for name in ('replay242.json', 'spot242.json'):
        try:
            g[name] = json.load(open(os.path.join(RES, name)))
        except Exception:                                            # noqa: BLE001
            g[name] = None
    rp, sp = g['replay242.json'], g['spot242.json']
    return {'replay': rp and rp.get('status'), 'spot': sp and sp.get('all_pass'),
            'adoptable': bool(rp and rp.get('status') == 'PASS_REPLAY_PYTHON_ALL_ROWS' and sp and sp.get('all_pass'))}


def main():
    if '--dry-run' not in sys.argv:
        raise SystemExit('adopt242: dry run only (pass --dry-run); adoption edits are the coordinator\'s call')
    pads = pad_tables()
    out = {'gate': gate(), 'window': {'W': [str(W_LO), str(S0)], 'Wprime': [str(WP_LO), str(S0)],
                                      'lambda_W': float(LAM_W), 'lambda_Wprime': float(LAM_WP),
                                      'pads_W': [pad(float(LAM_W), i) for i in range(5)],
                                      'pads_Wprime': [pad(float(LAM_WP), i) for i in range(5)],
                                      'pad_shrink_factor': (float(LAM_W) - 1) / (float(LAM_WP) - 1)},
           'pad_tables': {k: {'lam': v, 's_bot': (float(S0) / v if isinstance(v, float) else None),
                              'covers_W': isinstance(v, float) and v >= float(LAM_W) - TOL,
                              'covers_Wprime': isinstance(v, float) and v >= float(LAM_WP) - TOL}
                          for k, v in pads.items()},
           'ledger': ledger(pads), 'tube': tubes(),
           'slabs_wholly_below_31_8': [{'what': w, 'lo': lo, 'hi': hi} for w, lo, hi in BELOW],
           'superseded': SUPERSEDED,
           'basins_A207': {p: tally('attempts/A207-basin-clip/results/' + p) for p in
                           ('basin207.jsonl', 'basinclip207.jsonl', 's0basin207.jsonl')},
           'k0_cells_A185': tally('attempts/A185-boxed-windows-clause/results/win185.jsonl'),
           'notes': ['A270 g2/g3/g4 and A269 window/tube pad campaigns: needed only for (3.82, 3.861637]; void on W\'',
                     'A185 k0 cells: no side field; implied [3.82, s0] by K0-WIDEN (pad 0.025509) -> 0.000918 on W\'',
                     'A207 basins: drift over [1, lambda_1] shrinks by the pad factor; LP-ONLY rows are re-run candidates',
                     'CURRENT.json carries no window content; unchanged']}
    try:
        out['a270_frontier'] = json.load(open(os.path.join(REPO, 'attempts/A270-k5-lower-slabs/results/slabs270.json'),
                                              encoding='utf-8')).get('frontier')
    except Exception as e:                                           # noqa: BLE001
        out['a270_frontier'] = repr(e)
    json.dump(out, open(os.path.join(RES, 'adopt242_dryrun.json'), 'w'), indent=1)
    L = out['ledger']
    lines = ['A242 adopt242 --dry-run  (W = [191/50, s0] -> W\' = [31/8, s0]; NOTHING EDITED)',
             'gate: replay=%s spot=%s adoptable=%s' % (out['gate']['replay'], out['gate']['spot'], out['gate']['adoptable']),
             'pads pi_0..2: W %s -> W\' %s (x1/%.1f)' % (['%.6f' % x for x in out['window']['pads_W'][:3]],
                                                       ['%.6f' % x for x in out['window']['pads_Wprime'][:3]],
                                                       out['window']['pad_shrink_factor']),
             'pad tables covering W\': %s' % sorted(k for k, v in out['pad_tables'].items() if v['covers_Wprime']),
             'node ledger (A211 + A270 + A269 last pass per node and pad): %d nodes, dead on W %d, dead on W\' %d'
             % (L['nodes'], L['dead_on_W'], L['dead_on_Wprime']),
             'DEAD AT ONCE: %d %s' % (L['dead_at_once'], L['dead_at_once_by_class']),
             'alive on W\': %d %s (s0-dead among them %d)' % (L['alive_on_Wprime'], L['alive_on_Wprime_by_class'],
                                                            L['alive_on_Wprime_but_s0_dead']),
             'A270 frontier (g1-dead = dead on W\'): %s' % (out['a270_frontier'],),
             'tube certs: %(certs)d; reach W %(reach_W)d, reach W\' %(reach_Wprime)d (need T >= %(need_T_Wprime).6f)' % out['tube'],
             'slabs wholly below 31/8 (void): %s' % [b[0] for b in BELOW],
             'superseded: %s' % SUPERSEDED, 'records missing: %s' % L['records_missing']]
    txt = '\n'.join(lines) + '\n' + '\n'.join('note: ' + n for n in out['notes']) + '\n'
    open(os.path.join(RES, 'adopt242_dryrun.txt'), 'w').write(txt)
    print(txt)


if __name__ == '__main__':
    main()
