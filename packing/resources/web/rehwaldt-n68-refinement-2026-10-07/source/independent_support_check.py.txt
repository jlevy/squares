#!/usr/bin/env python3
"""Exact centre/support-radius check of a rational square certificate.

Standalone Python standard library. No imports from the campaign.
All acceptance decisions use Fraction; decimal output is presentation only.
"""
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def radius(square, axis):
    return (abs(dot(square['u'], axis)) + abs(dot(square['v'], axis)))/2


def decimal(value):
    with localcontext() as ctx:
        ctx.prec = 85
        return str(Decimal(value.numerator)/Decimal(value.denominator))


def check(data, expected_n):
    if data.get('schema') not in ('packing-n/exact-v1', 'independent-square-certificate/v1'):
        raise ValueError('Unknown certificate schema')
    if type(data.get('n')) is not int or data['n'] != expected_n or len(data['squares']) != expected_n:
        raise ValueError('Square count mismatch')
    side = Q(data['container_side'])
    if side <= 0:
        raise ValueError('Nonpositive container side')
    squares = []
    for raw in data['squares']:
        t = Q(raw['t'])
        u = ((1-t*t)/(1+t*t), 2*t/(1+t*t))
        v = (-u[1], u[0])
        if dot(u, u) != 1 or dot(v, v) != 1 or dot(u, v) != 0:
            raise ValueError('Invalid unit directions')
        squares.append({'center':(Q(raw['x']), Q(raw['y'])), 'u':u, 'v':v})
    wall = min(side/2-abs(square['center'][d])-radius(square, axis)
               for square in squares for d, axis in enumerate(((Q(1),Q(0)),(Q(0),Q(1)))))
    margins = []
    for i, a in enumerate(squares):
        for j in range(i):
            b = squares[j]
            displacement = tuple(x-y for x,y in zip(a['center'],b['center']))
            margin = max(abs(dot(displacement, axis))-radius(a, axis)-radius(b, axis)
                         for axis in (a['u'],a['v'],b['u'],b['v']))
            margins.append(margin)
    pair = min(margins) if margins else Q(0)
    return {'valid':wall >= 0 and pair >= 0, 'n':expected_n,
            'pairs_checked':len(margins), 'acceptance_tolerance':'0',
            'container_side_rational':str(side), 'container_side_decimal':decimal(side),
            'minimum_wall_clearance_rational':str(wall), 'minimum_wall_clearance_decimal':decimal(wall),
            'minimum_pair_margin_rational':str(pair), 'minimum_pair_margin_decimal':decimal(pair),
            'method':'Exact centre/support radii on four separating axes; Fraction arithmetic'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('certificate',type=Path)
    ap.add_argument('--n',required=True,type=int)
    ap.add_argument('--output',type=Path)
    args = ap.parse_args()
    raw = args.certificate.read_bytes()
    result = check(json.loads(raw),args.n)
    result['certificate_sha256'] = hashlib.sha256(raw).hexdigest()
    rendered = json.dumps(result,indent=2)+'\n'
    print(rendered)
    if args.output:
        args.output.write_text(rendered)
    return 0 if result['valid'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
