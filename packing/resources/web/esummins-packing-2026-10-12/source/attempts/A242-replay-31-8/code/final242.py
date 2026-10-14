"""A242 finisher -- called by run242.sh after the shards, the controls and `rows242.py finish`.
Writes the verdict block of results/replay242.md and replaces the two PENDING markers (ledger s.0 note, registry
row) by the verdict.  Edits nothing else.  Exit 0 on PASS, 2 otherwise."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ATT = os.path.abspath(os.path.join(HERE, '..'))
REPO = os.path.abspath(os.path.join(ATT, '..', '..'))
RES, LOG = os.path.join(ATT, 'results'), os.path.join(ATT, 'logs')


def load(name):
    try:
        return json.load(open(os.path.join(RES, name)))
    except Exception:                                                # noqa: BLE001
        return None


def shard_wall():
    out = []
    for i in (0, 1):
        try:
            m = re.findall(r'DONE (\d+)s', open(os.path.join(LOG, 'shard%d.log' % i)).read())
            out.append(int(m[-1]) if m else None)
        except OSError:
            out.append(None)
    return out


def replace_marker(path, old, new):
    p = os.path.join(REPO, path)
    try:
        s = open(p, encoding='utf-8', newline='').read()
    except OSError:
        return False
    if old not in s:
        return False
    open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new, 1))
    return True


def main():
    rp, co, sp = load('replay242.json'), load('controls242.json'), load('spot242.json')
    integ = open(os.path.join(RES, 'integrity242.txt')).read() if os.path.exists(os.path.join(RES, 'integrity242.txt')) else ''
    ok_rp = bool(rp and rp.get('status') == 'PASS_REPLAY_PYTHON_ALL_ROWS')
    ok_co = bool(co and co.get('status') == 'PASS_INDEPENDENT_EXACT_CONTROLS')
    ok_sp = bool(sp and sp.get('all_pass'))
    ok_in = integ.count('PASS 54 pinned files') >= 2
    ok = ok_rp and ok_co and ok_sp and ok_in
    walls = shard_wall()
    ev = (rp or {}).get('evidence_comparison', {})
    lines = ['', '## Verdict (written by code/final242.py)', '',
             '**%s** -- replay %s, controls %s, spot-check %s, integrity %s.' % (
                 'PASS' if ok else 'FAIL', (rp or {}).get('status'), (co or {}).get('status'),
                 'PASS' if ok_sp else 'FAIL', 'PASS (x2)' if ok_in else 'FAIL'), '',
             '* rows replayed %s / 12028; minimum %s (= Gamma), budget %s, surplus %s; slabs %s, cells %s' % (
                 (rp or {}).get('rows_replayed'), (rp or {}).get('minimum_units'), (rp or {}).get('budget_units'),
                 (rp or {}).get('counting_surplus_units'), (rp or {}).get('slabs'), (rp or {}).get('cells')),
             '* row-by-row against their evidence (minimum, cells, slabs): ' + '; '.join(
                 '%s: %s rows differ, histogram equal %s, totals equal %s' % (
                     k, v.get('rows_differing'), v.get('histogram_equal'), v.get('totals_equal')) for k, v in ev.items()),
             '* runtime: shard wall %s s (pure-Python kernel, 2 shards in parallel, BelowNormal); CPU %s s summed' % (
                 walls, (rp or {}).get('cpu_seconds')),
             '* controls: containment %s; boundary samples %s centres, minimum %s' % (
                 ((co or {}).get('containment') or {}).get('quadratic_inequalities'),
                 ((co or {}).get('boundary_samples') or {}).get('total_centres'),
                 ((co or {}).get('boundary_samples') or {}).get('minimum_sampled_charge'))]
    with open(os.path.join(RES, 'replay242.md'), 'a', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    tag = 'PASS' if ok else 'FAIL'
    a = replace_marker('docs/residue_ledger.md', 'T-037 replay verdict: PENDING (A242 finisher)',
                       'T-037 replay verdict: %s (A242: all 12,028 rows replayed, %s)' % (
                           tag, 'identical to their evidence row by row' if ok else 'see results/replay242.md'))
    b = replace_marker('attempts/REGISTRY.md', '| running (replay detached; verdict by final242) |',
                       '| %s |' % ('done' if ok else 'done-negative'))
    print('final242: %s; ledger marker %s, registry marker %s' % (tag, a, b))
    return 0 if ok else 2


if __name__ == '__main__':
    raise SystemExit(main())
