"""Summarize run_tt.py outputs.  usage: summarize_tt.py out [out_fix]
A job counts as ALL-OK if its main output ends ALL-OK, or if it ends NOT-OK and every chart that refused cells was
re-run in out_fix/<same name> with 0 refused cells (the rerun overrides those charts; cov_check.py applies the same rule)."""
import sys, os, json, glob
main_dir = sys.argv[1]
fix_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(main_dir.rstrip('/'))), 'out_fix')
def read(f):
    L = open(f).read().split('\n'); last = [l for l in L if l.strip()][-1] if any(l.strip() for l in L) else ''
    charts = {}; cells = 0
    for l in L:
        if l.startswith('{'):
            d = json.loads(l)
            if 'fails' in d: charts[d['chart']] = d['fails']
            cells += d.get('cells', 0) + d.get('corner_cells', 0)
    return last, charts, cells
ok = notok = unfinished = fixed = 0; cells = 0; bad = []
for f in sorted(glob.glob(os.path.join(main_dir, '*.out'))):
    last, charts, c = read(f); cells += c
    if last == 'ALL-OK': ok += 1; continue
    if last != 'NOT-OK': unfinished += 1; bad.append(f + ' (unfinished)'); continue
    fx = os.path.join(fix_dir, os.path.basename(f))
    if os.path.exists(fx):
        flast, fch, fc = read(fx)
        if flast.startswith(('ALL-OK', 'NOT-OK', 'PARTIAL-')):
            charts.update(fch)
            if all(v == 0 for v in charts.values()):
                ok += 1; fixed += 1; cells += fc; print('   fixed by rerun:', fx); continue
    notok += 1; bad.append(f)
print(f'jobs ALL-OK {ok} (of which fixed by out_fix reruns {fixed}), NOT-OK {notok}, unfinished {unfinished}; cells {cells}')
for b in bad: print('  ', b)
