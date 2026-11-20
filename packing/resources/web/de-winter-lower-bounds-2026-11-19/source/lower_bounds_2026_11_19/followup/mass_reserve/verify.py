"""Enlarge a continuous measure certificate using a bound for the mass in a square's four thin edge strips."""
from fractions import Fraction
from pathlib import Path
from zipfile import ZipFile
import csv
import gzip
import hashlib
import io
import math
import json

F = Fraction
RADIUS_TWICE = F(1414213562373096, 10**15)
SOURCE_HASH = '9641ca15ac63213db22ad32854efb0bc0575d7c0beeb646fd6931f50ae183452'
assert RADIUS_TWICE ** 2 > 2

def winning_sources(archive):
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == SOURCE_HASH
    with ZipFile(archive) as source:
        transfers = json.loads(source.read('rectangles/exact_transfers.json'))
        claims = csv.DictReader(io.StringIO(source.read('exact_claims.csv').decode()))
        for row in claims:
            n, key = int(row['n']), row['certificate_id']
            if n != int(row['source_n']) or key not in transfers or row['exact_kind'] != 'rational':
                continue
            folder = key.removeprefix('irregular_')
            if not folder.startswith(('partial_', 'published_', 'refined_')):
                continue
            params = transfers[key]
            side, scale, margin = (F(params[k]) for k in ('lower','scale','margin'))
            assert F(row['rational_value_or_radicand']) == side
            data = json.loads(gzip.decompress(source.read(f'rectangles/evidence/{folder}/measure.json.gz')))
            assert not data['points'] and F(data['L']) == scale * side + 2 * margin
            yield n, key, side, scale, margin, data

def parameters(source, scale, margin):
    length = F(source['L'])
    mass = F(0)
    coefficient = F(0)
    for rectangle in source['rectangles']:
        x, y, right, top = map(F, rectangle['rectangle'])
        weight = F(rectangle['mass'])
        assert weight >= 0 and 0 <= x < right <= length and 0 <= y < top <= length
        dx = max(F(0), min(right, length-margin) - max(x, margin))
        dy = max(F(0), min(top, length-margin) - max(y, margin))
        if dx == 0 or dy == 0:
            continue
        density = weight / ((right - x) * (top - y))
        mass += density * dx * dy
        # sqrt(dx**2+dy**2) <= dx+dy for every rectangle.
        coefficient += F(math.ceil(2 * scale * density * (dx + dy) * 10**9), 10**9)
    return F(math.ceil(mass * 10**18), 10**18), coefficient

def enlargement(n, side, mass, coefficient):
    assert side > RADIUS_TWICE and coefficient > 0 and 0 < mass < n
    # Strict positive slack remains in the obstruction at a rational endpoint.
    rho = 1 - (n-mass) * F(999,1000) / (n*coefficient)
    assert 0 < rho < 1 and n * (1 - coefficient * (1-rho)) > mass
    endpoint = RADIUS_TWICE + (side - RADIUS_TWICE)/rho
    return F(math.floor(endpoint * 10**18), 10**18)

def derive(archive, stronger):
    output = {}
    for n, key, side, scale, margin, data in winning_sources(archive):
        mass, coefficient = parameters(data, scale, margin)
        t = enlargement(n,side,mass,coefficient)
        previous = stronger(n)
        if t > previous and (n not in output or t > F(output[n]['side'])):
            output[n] = dict(n=n,case=key,base=str(side),scale=str(scale),margin=str(margin),mass=str(mass),
                             strip_coefficient=str(coefficient),previous=str(previous),side=str(t),increase=str(t-previous))
    return list(output.values())

def verify(folder):
    import importlib.util
    history = folder.parent/'comparisons/benchmark.py'
    spec = importlib.util.spec_from_file_location('reserve_history',history)
    benchmark = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(benchmark)
    direct = list(csv.DictReader((folder.parent/'best_by_count.csv').open()))
    def previous(n):
        return max([benchmark.prior(n)[0]] + [F(r['exact']) for r in direct if int(r['n'])<=n])
    expected = derive(folder/'lower-bounds-56.zip',previous)
    assert expected == json.loads((folder/'claims.json').read_text())
    return expected

if __name__=='__main__':
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    records = verify(Path(__file__).resolve().parent)
    for row in records:
        print(row['n'],format(float(F(row['side'])),'.14f'),format(float(F(row['increase'])),'.4g'))
    print('Verified',len(records),'additional square counts.')
