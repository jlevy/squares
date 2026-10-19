import gzip, json, sys, collections
from fractions import Fraction as Fr
path, root_file = sys.argv[1], sys.argv[2]
with gzip.open(path, 'rt', encoding='utf-8') as f:
    header = json.loads(f.readline())
    nodes = [json.loads(line) for line in f]
print('header keys', sorted(header), 'schema', header['schema'], 'labels', header.get('labels'), 'S_floor', header.get('S_floor'), 'root', header['root'])
print('nodes', len(nodes))
n = nodes[0]
print('node keys', sorted(n), 'id', n['id'], 'parent', n['parent'], 'S', n['S'], 'assume', n['assume'], 'close', n['close'])
print('rounds', len(n['rounds']))
rd = n['rounds'][0]
print('declarations', len(rd['pairs']), collections.Counter(d['mode'] for d in rd['pairs']))
print('steps', len(rd['steps']))
st = rd['steps'][0]
print('step form', st['form'], 'sense', st['sense'], 'value', st['value'], 'centre' in st, 'terms', len(st['terms']))
kinds = collections.Counter()
neg = 0
for lam, names in st['terms']:
    if Fr(lam) < 0: neg += 1
    kinds[tuple(sorted(nm.split(':')[0] for nm in names))] += 1
print('negative multipliers', neg)
for k, v in kinds.most_common(15): print('  ', v, k)
reg = json.load(open(root_file))
print('root box equal to region', n['box'] == reg['window']['box'], 'root arc equal', n['arc'] == reg['root_arc'], 'S equal', n['S'] == reg['S'])
print('qforms', sum(1 for k in n.get('forms', {}) if k.startswith('q:')), 'custom forms', sum(1 for k in n.get('forms', {}) if not k.startswith('q:')))
print('window == region window box', header['window']['box'] == reg['window']['box'])
print('label 4 root box', n['box'].get('4'), 'arc', n['arc'].get('4'))
