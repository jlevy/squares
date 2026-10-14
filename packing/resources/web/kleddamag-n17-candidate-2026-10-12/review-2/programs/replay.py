"""Independent replay of the normalized contraction chain B6 -> stop cuts -> 5 stopped rounds.

usage: replay.py GATE_RECEIPT AUDIT_JSON B6_JSON CONTINUATION_DIR

Mode A (stored models): rounds 1-5 are replayed with my own weak-duality code on the producer's stored
models (whose 52 geometric rows check_rows.py has shown to be implied by my derivation); every bound must
equal the stored one and every outgoing box must equal the next incoming box.
Mode B (my rows only): the whole chain, including the six B6 steps whose models are not stored, is replayed
with rows built by rows.py (my derivation, my rounding) and the producer's multipliers used only as hints;
the box is updated with MY bounds. Reports the final 45-core ratio.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
import rows as R

OGRID = 10**15


def outward(box52):
    return [(Fr((lo*OGRID).__floor__(), OGRID), Fr((hi*OGRID).__ceil__(), OGRID)) for lo, hi in box52]


def initial_box():
    PAD = Fr(1, 10**12)
    box = [(Fr(-1), Fr(1))]*51 + [(Fr(-1), Fr(0))]
    for j in R.DUMMY:
        box[j] = (Fr(0), Fr(0))
    box[2] = (Fr(0), Fr(8, 25) + PAD)
    box[21] = (Fr(-1, 20) - PAD, Fr(1, 5) + PAD)
    box[25] = (Fr(-1, 5) - PAD, Fr(3, 40) + PAD)
    return R.refresh(box)


def my_model(geo, labels, box, normals, stop):
    rows = [R.to_rational_row(r, box) for r in R.build_rows(geo, labels, box, normals)]
    rows += R.product_rows(box)
    if stop:
        rows.append(({21: Fr(-1), 25: Fr(-1)}, Fr(-3, 125)))
    return rows


def step(rows, box, results):
    seen = set()
    upd = list(box[:52])
    for res in results:
        i, s = res['coordinate'], res['sign']
        assert (i, s) not in seen
        seen.add((i, s))
        v = R.dual_bound(rows, box, i, s, res['weights'])
        lo, hi = upd[i]
        upd[i] = (max(lo, v), hi) if s == 1 else (lo, min(hi, -v))
    assert seen == {(i, s) for i in R.CORE + (51,) for s in (-1, 1)}
    assert all(lo <= hi for lo, hi in upd)
    return R.refresh(outward(upd))


def ratio(box):
    return max(max(abs(lo), abs(hi)) for j in R.CORE for lo, hi in [box[j]])


def stored_rows(model):
    return [({j: Fr(x) for j, x in enumerate(r['a']) if Fr(x)}, Fr(r['b'])) for r in model]


def main():
    labels = json.load(open(sys.argv[1]))['new_labels']
    audit = json.load(open(sys.argv[2]))['retained']
    normals = {}
    for key, opts in audit.items():
        l, r = map(int, key.split('-'))
        normals[(l, r)] = (opts[0][1], opts[0][2])
    b6 = json.load(open(sys.argv[3]))
    cont = sys.argv[4]
    chain_prefix = json.load(open(os.path.join(cont, 'prefix', 'stopped-chain.json')))
    rounds = [os.path.join(cont, 'prefix', f'round-0{n}') for n in (1, 2, 3)] + [os.path.join(cont, f'round-0{n}') for n in (4, 5)]

    # ---- Mode A: stored models, my dual arithmetic
    box = [tuple(map(Fr, v)) for v in chain_prefix['initial_bounds']]
    b6_final = [tuple(map(Fr, v)) for v in b6['final_bounds']]
    base = list(b6_final[:52])
    base[21] = (max(base[21][0], Fr(-17, 50000)), base[21][1])
    base[25] = (base[25][0], min(base[25][1], Fr(1, 40)))
    assert R.refresh(base) == box, 'stopped-chain initial box is not B6 with the two stop cuts'
    for rd in rounds:
        rnd = json.load(open(os.path.join(rd, 'round.json')))
        model = json.load(open(os.path.join(rd, 'model.json')))
        assert [tuple(map(Fr, v)) for v in rnd['incoming_bounds']] == box
        rows = stored_rows(model)
        for res in rnd['results']:
            v = R.dual_bound(rows, box, res['coordinate'], res['sign'], res['weights'])
            assert v == Fr(res['bound']), (rd, res['coordinate'], res['sign'])
        box = step(rows, box, rnd['results'])
        assert [tuple(map(Fr, v)) for v in rnd['final_bounds']] == box, rd
        print('mode A', os.path.basename(rd), 'ratio', float(ratio(box)), str(ratio(box)) if ratio(box) < 1 else '')
    print('mode A final ratio (exact):', ratio(box))

    # ---- Mode B: everything with my own rows
    geo = R.Geo()
    box = initial_box()
    for n, st in enumerate(b6['steps'], 1):
        rows = my_model(geo, labels, box, normals, stop=False)
        box = step(rows, box, st['results'])
        print('mode B B6 step', n, 'ratio', float(ratio(box)))
    # compare with the producer's B6
    looser = [j for j in range(52) if box[j][0] < b6_final[j][0] or box[j][1] > b6_final[j][1]]
    worst = max((max(b6_final[j][0] - box[j][0], box[j][1] - b6_final[j][1]) for j in range(52)), default=0)
    print('mode B: my B6 vs producer B6: coordinates where mine is looser:', len(looser), 'max excess', float(worst))
    base = list(box[:52])
    base[21] = (max(base[21][0], Fr(-17, 50000)), base[21][1])
    base[25] = (base[25][0], min(base[25][1], Fr(1, 40)))
    box = R.refresh(base)
    for rd in rounds:
        rnd = json.load(open(os.path.join(rd, 'round.json')))
        rows = my_model(geo, labels, box, normals, stop=True)
        box = step(rows, box, rnd['results'])
        print('mode B', os.path.basename(rd), 'ratio', float(ratio(box)))
    print('mode B final ratio:', float(ratio(box)), 'strict' if ratio(box) < 1 else 'NOT strict')


if __name__ == '__main__':
    main()
