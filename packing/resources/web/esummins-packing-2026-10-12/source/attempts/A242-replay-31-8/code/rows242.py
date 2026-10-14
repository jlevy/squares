"""A242 -- row-sharded, RESUMABLE replay of the pinned external Python checker (exact_mixed.py / integer_sweep.py).

Per row this does exactly what replay_parallel.replay() does -- validate(c) once, then geometry(*DATA, *job),
accumulate(*arrays), need(z >= minimum_units) -- calling the external functions unmodified.  Deviations from the
documented run (verify.py): numba is not installed (pip would reach the network), so ext/shim/numba.py makes `njit`
the identity and the SAME kernel source runs uncompiled; the JavaScript secondary is not run (it downloads the
R038 upstream file and needs node); replay_parallel's Pool is replaced by two row shards (lab cap: 2 pythons).

    python code/rows242.py shard I N     rows [I*R//N, (I+1)*R//N) -> results/replay242_shard{I}of{N}.jsonl (resumes)
    python code/rows242.py finish N      merge shards, compare row by row with the release's recorded evidence
                                         (evidence/initial + evidence/portable python.json) -> results/replay242.json
"""
import hashlib, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ATT = os.path.abspath(os.path.join(HERE, '..'))
REPO = os.path.join(ATT, 'ext', 'repo')
SHIM = os.path.join(ATT, 'ext', 'shim')
RES = os.path.join(ATT, 'results')
CERT = os.path.join(REPO, 'global-certificate.json')
CERT_SHA = '57e9927da5c13f42dd8bcbf8f08c84363635fece626657ee63a810c61cd44458'
sys.path[:0] = [REPO, SHIM]
sys.setrecursionlimit(10000)


def lower_priority():
    try:
        import ctypes
        k32 = ctypes.windll.kernel32
        h = k32.GetCurrentProcess()
        k32.SetPriorityClass(h, 0x00004000)
        k32.SetProcessAffinityMask(h, 0xFFFF)
    except Exception:
        pass


def load():
    raw = open(CERT, 'rb').read()
    assert hashlib.sha256(raw).hexdigest() == CERT_SHA, 'certificate hash'
    return raw, json.loads(raw)


def shard_path(i, n):
    return os.path.join(RES, 'replay242_shard%dof%d.jsonl' % (i, n))


def shard(i, n):
    lower_priority()
    import numpy as np
    from exact_mixed import validate, geometry, accumulate, need
    raw, c = load()
    data, jobs, margin = validate(c)
    R = len(jobs)
    lo, hi = i * R // n, (i + 1) * R // n
    out = shard_path(i, n)
    done = set()
    if os.path.exists(out):
        for line in open(out):
            line = line.strip()
            if line.endswith('}'):
                done.add(json.loads(line)['row'])
    print('shard %d/%d rows [%d,%d) done %d margin %s' % (i, n, lo, hi, len(done), margin), flush=True)
    if os.path.exists(out) and os.path.getsize(out) and not open(out, 'rb').read().endswith(b'\n'):
        open(out, 'a').write('\n')                          # an interrupted partial line stays isolated
    t0 = time.monotonic()
    with open(out, 'a') as f:
        for k in range(lo, hi):
            if k in done:
                continue
            s = time.monotonic()
            ar = geometry(*data, *jobs[k])
            z, cells, win = accumulate(*ar)
            need(z >= c['minimum_units'], 'coverage fails at ' + str(k))
            row = {'row': k, 'minimum_units': int(z), 'cells': int(cells),
                   'slabs': int(np.count_nonzero(ar[-2] >= 0)), 'sec': round(time.monotonic() - s, 3)}
            f.write(json.dumps(row) + '\n')
            f.flush()
            if (k - lo) % 200 == 0:
                print('row %d min %d elapsed %.0fs' % (k, z, time.monotonic() - t0), flush=True)
    print('shard %d/%d DONE %.0fs' % (i, n, time.monotonic() - t0), flush=True)


def finish(n):
    raw, c = load()
    rows = {}
    for i in range(n):
        for line in open(shard_path(i, n)):
            line = line.strip()
            if line.endswith('}'):
                r = json.loads(line)
                rows[r['row']] = r
    R = len(c['entries'])
    missing = [k for k in range(R) if k not in rows]
    out = {'status': None, 'certificate_sha256': hashlib.sha256(raw).hexdigest(), 'intervals': R,
           'rows_replayed': len(rows), 'missing_rows': missing[:20], 'n_missing': len(missing)}
    if missing:
        out['status'] = 'INCOMPLETE'
    else:
        mins = [rows[k]['minimum_units'] for k in range(R)]
        hist = {}
        for z in mins:
            hist[str(z)] = hist.get(str(z), 0) + 1
        out.update(minimum_units=min(mins), budget_units=c['budget_units'],
                   counting_surplus_units=11 * min(mins) - c['budget_units'],
                   slabs=sum(rows[k]['slabs'] for k in range(R)), cells=sum(rows[k]['cells'] for k in range(R)),
                   cpu_seconds=round(sum(rows[k]['sec'] for k in range(R)), 1), histogram=hist,
                   argmin_rows=[k for k in range(R) if mins[k] == min(mins)])
        cmp = {}
        for tag in ('initial', 'portable'):
            ev = json.load(open(os.path.join(REPO, 'evidence', tag, 'python.json')))
            er = {r['row']: r for r in ev['rows']}
            diff = [k for k in range(R) if any(er[k][f] != rows[k][f] for f in ('minimum_units', 'cells', 'slabs'))]
            cmp[tag] = {'rows_compared': R, 'rows_differing': len(diff), 'first_diffs': diff[:10],
                        'histogram_equal': ev['histogram'] == hist,
                        'totals_equal': (ev['slabs'], ev['cells'], ev['minimum_units']) ==
                                        (out['slabs'], out['cells'], out['minimum_units'])}
        out['evidence_comparison'] = cmp
        ok = (out['minimum_units'] == c['minimum_units'] == 999962528 and c['budget_units'] == 10999479944
              and out['counting_surplus_units'] == 107864 > 0
              and all(v['rows_differing'] == 0 and v['histogram_equal'] for v in cmp.values()))
        out['status'] = 'PASS_REPLAY_PYTHON_ALL_ROWS' if ok else 'FAIL'
    json.dump(out, open(os.path.join(RES, 'replay242.json'), 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != 'histogram'}))
    return out['status']


if __name__ == '__main__':
    if sys.argv[1] == 'shard':
        shard(int(sys.argv[2]), int(sys.argv[3]))
    elif sys.argv[1] == 'finish':
        st = finish(int(sys.argv[2]))
        sys.exit(0 if st == 'PASS_REPLAY_PYTHON_ALL_ROWS' else 2)
