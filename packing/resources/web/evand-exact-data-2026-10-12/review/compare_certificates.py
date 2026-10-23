"""Compare check_theorem_c.py's receipts with the source's published grade-C certificates.

Reads the receipts (JSON lines) that check_theorem_c.py wrote and, in memory from
gradec-233.tar.zst, the source's n-N.gradec.json for the same counts.  For each count it
compares what both computed and what does not depend on a choice of basis or of
multipliers: the row set, the rank of L0, dim F, dim W, the moving squares, the
interior margin; and, loosely, the least multiplier (both come from a max-min linear
program, so they agree to rounding).  The Hessian minors are not compared: they depend on
the basis of W each program chose.  It decides nothing about any packing; it reports
agreement.

  python -I compare_certificates.py --archive gradec-233.tar.zst RECEIPTS.jsonl [...]
"""
import argparse
import hashlib
import json
import sys
import tarfile


def canon(obj):
    return hashlib.sha256(json.dumps(obj, separators=(',', ':')).encode()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--archive', required=True)
    ap.add_argument('receipts', nargs='+')
    a = ap.parse_args()
    mine = {}
    for path in a.receipts:
        for line in open(path):
            r = json.loads(line)
            mine[r['n']] = r
    report = {'counts': len(mine), 'all_valid_here': all(r.get('valid') for r in mine.values()),
              'disagreements': [], 'lambda_min_max_rel_diff': 0.0, 'margin_max_abs_diff': 0.0}
    with tarfile.open(a.archive, 'r:zst') as tf:
        for n in sorted(mine):
            r = mine[n]
            src = json.loads(tf.extractfile(f'gradec-233/certs/n-{n}.gradec.json').read())
            rows = sorted([list(x) for x in src['rows']], key=str)
            checks = {
                'valid': (src.get('valid'), r.get('valid')),
                'row_set': (canon(rows), r.get('row_set_sha256')),
                'rank_L0': (src['rank_L0'], r.get('rank_L0')),
                'dim_F': (src['dim_F'], r.get('dim_F')),
                'dim_W': (src['dim_W'], r.get('dim_W')),
                'moving_squares': (canon(sorted(src['moving_squares'])), r.get('moving_squares_sha256')),
                'load_bearing': (len(src['load_bearing_squares']), r.get('load_bearing')),
            }
            for key, (theirs, ours) in checks.items():
                if theirs != ours:
                    report['disagreements'].append({'n': n, 'field': key, 'source': theirs, 'here': ours})
            if r.get('lambda_min') is not None:
                rel = abs(r['lambda_min'] - src['lambda_min']) / max(1e-300, abs(src['lambda_min']))
                report['lambda_min_max_rel_diff'] = max(report['lambda_min_max_rel_diff'], rel)
            if r.get('margin') is not None:
                report['margin_max_abs_diff'] = max(report['margin_max_abs_diff'], abs(r['margin'] - src['margin']))
    report['agree'] = not report['disagreements']
    print(json.dumps(report, indent=1))
    sys.exit(0 if report['agree'] and report['all_valid_here'] else 1)


if __name__ == '__main__':
    main()
