"""Merge check_theorem_c.py's receipt files into one, sorted by count, and summarize them.

It decides nothing: it reads the receipts the checker wrote and prints totals (counts by
field degree and by verdict, CPU time, rows, side-end rows and how many slip along the
flat family, dimensions, the singular-value cross-check), writing the merged receipts and
the summary as JSON.  No evidence entry cites it.

  python -I summarize_run.py --merged OUT.jsonl --summary OUT.json IN.jsonl [IN.jsonl ...]
"""
import argparse
import json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--merged', required=True)
    ap.add_argument('--summary', required=True)
    ap.add_argument('--extra', default=None, help='JSON object merged into the summary (run metadata)')
    ap.add_argument('receipts', nargs='+')
    a = ap.parse_args()
    rows = {}
    for path in a.receipts:
        for line in open(path):
            r = json.loads(line)
            assert r['n'] not in rows, f"count {r['n']} twice"
            rows[r['n']] = r
    ordered = [rows[n] for n in sorted(rows)]
    with open(a.merged, 'w') as fh:
        for r in ordered:
            fh.write(json.dumps(r, sort_keys=True) + '\n')
    valid = [r for r in ordered if r.get('valid')]
    cpu = [r.get('cpu_seconds', 0.0) for r in ordered]
    gaps = [r['svd_gap'][0] / r['svd_gap'][1] for r in ordered
            if r.get('svd_gap') and r['svd_gap'][0] and r['svd_gap'][1]]
    by_degree = {}
    for r in ordered:
        by_degree[str(r.get('field_degree'))] = by_degree.get(str(r.get('field_degree')), 0) + 1
    summary = {
        'counts': len(ordered),
        'valid': len(valid),
        'not_valid': [r['n'] for r in ordered if not r.get('valid')],
        'by_field_degree': by_degree,
        'cpu_seconds_total': round(sum(cpu), 2),
        'cpu_seconds_max': max(cpu),
        'cpu_seconds_max_at': ordered[cpu.index(max(cpu))]['n'],
        'cpu_seconds_median': sorted(cpu)[len(cpu) // 2],
        'rows_total': sum(r.get('rows', 0) for r in ordered),
        'side_end_rows_total': sum(r.get('side_end_rows', 0) for r in ordered),
        'counts_with_side_end_rows': sum(1 for r in ordered if r.get('side_end_rows', 0) > 0),
        'counts_without_side_end_rows': [r['n'] for r in ordered if r.get('side_end_rows', 0) == 0],
        'counts_with_slipping_side_end_rows': sum(1 for r in ordered if r.get('side_end_rows_slipping', 0) > 0),
        'slipping_side_end_rows_total': sum(r.get('side_end_rows_slipping', 0) for r in ordered),
        'counts_with_flat_family': sum(1 for r in ordered if r.get('dim_F', 0) > 0),
        'counts_with_dim_W_positive': sum(1 for r in ordered if r.get('dim_W', 0) > 0),
        'dim_W_max': max(r.get('dim_W', 0) for r in ordered),
        'dim_F_max': max(r.get('dim_F', 0) for r in ordered),
        'lifts_solved_total': sum(r.get('lifts_solved', 0) for r in ordered),
        'dropped_zero_rows': {str(r['n']): len(r.get('dropped_zero_rows') or []) for r in ordered
                              if r.get('dropped_zero_rows')},
        'beyond_side_end_dropped': {str(r['n']): r['beyond'] for r in ordered if r.get('beyond')},
        'lone_side_end_dropped': {str(r['n']): r['lone_side_end'] for r in ordered if r.get('lone_side_end')},
        'svd_agrees_everywhere': all(r.get('svd_agrees') for r in ordered),
        'svd_smallest_gap_ratio': min(gaps) if gaps else None,
        'least_margin': min(r['margin'] for r in ordered if 'margin' in r),
        'least_margin_at': min((r['margin'], r['n']) for r in ordered if 'margin' in r)[1],
        'least_lambda_min': min(r['lambda_min'] for r in ordered if 'lambda_min' in r),
        'program_sha256': sorted({r['environment']['program_sha256'] for r in ordered}),
        'environment': ordered[0]['environment'],
    }
    if a.extra:
        summary.update(json.loads(open(a.extra).read()))
    with open(a.summary, 'w') as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
        fh.write('\n')
    print(json.dumps({k: v for k, v in summary.items() if k not in ('environment',)}, indent=1))


if __name__ == '__main__':
    main()
