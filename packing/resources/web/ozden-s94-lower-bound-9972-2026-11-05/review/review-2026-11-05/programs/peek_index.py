import gzip, json, sys
idx = json.loads(gzip.decompress(open(sys.argv[1], 'rb').read()))
print('top keys', sorted(idx))
for k, v in idx.items():
    if k != 'sources':
        print(k, json.dumps(v)[:600])
for s in idx['sources']:
    sc = s.get('scope')
    d = {kk: vv for kk, vv in s.items() if kk not in ('scope', 'summary')}
    print('---', s['id'], 'scope len', len(sc) if isinstance(sc, list) else sc, 'scope head', sc[:5] if isinstance(sc, list) else '')
    print(json.dumps(d, indent=None)[:1500])
